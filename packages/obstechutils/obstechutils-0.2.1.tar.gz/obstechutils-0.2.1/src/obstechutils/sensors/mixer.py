from __future__ import annotations

from obstechutils.dataclasses import strictdataclass, Field, autoconverted
from obstechutils.mqtt import MQTTClient
from obstechutils.types import TimeDeltaType, TypeAlias
from obstechutils import logging
from obstechutils.types import LockType
from obstechutils.precise_timing import synchronised_call

from typing import Callable

from threading import Lock as _Lock
import copy
from time import time
import numpy as np

AveragerType: TypeAlias = Callable[list[float], float]
SingleSensorDataType: TypeAlias = dict[str, float | str]
SensorDataType: TypeAlias = dict[str, SingleSensorDataType]
MixType: TypeAlias = dict[str, float | str]
PostProcFuncType: TypeAlias = Callable[[MixType], None]
PreProcFuncType: TypeAlias = Callable[[SensorDataType], None]

def inaction(x: MixType | SensorDataType) -> None: 
    ...

class BasicSensorFuser:

    """Determine the past variance of each measurement series to determine
an average. Some care has been taken for robustness:
    * absent/invalid measurement values will be properly dealt with
    * new sensors can appear during the time series

A Kálmán filtre would certainly be better but I don't understand it.  A
quick test on normal data show that it works well to find the optimal
weights on noisy, constant data.

    """

    def __init__(self, last_states=20):

        self._nstates = last_states
        self._last_mean = np.nan
        self._weights = {}
        self._last_states = {}

    @property
    def current_weights(self):
        return np.array(list(self._weights.values()))

    @property
    def current_std(self):
        return 1 / self.current_weights ** 0.5

    @property
    def last_mean(self):
        return self._last_mean

    def __call__(self, measurements: dict[str, float]) -> float:

        nm = len(measurements)
        last_states = self._last_states

        # discard oldest values and prepare to receive a new value
        # at array index 0. Put last_mean there in case not all sensors
        # are provided
        
        for sensor, last_state in last_states.items():
            last_state[1:] = last_state[:-1]
            last_state[0] = np.nan

        if not measurements:
            return np.nan

        # inspect all measurements

        for sensor, value in measurements.items():

            # if it's a newly seen sensor, add it

            try:
                last_states = self._last_states[sensor]
            except:
                last_states = np.full((self._nstates,), np.nan)
                self._last_states[sensor] = last_states
         
            # update value

            last_states[0] = value if np.isfinite(value) else np.nan
            
            # update variance
            
            var = np.ma.masked_invalid(last_states).var(ddof=1)
            self._weights[sensor] = 1 / var if var > 0 else np.nan

        # if deviation is undetermined (e.g. new sensor), replace it by 
        # the mean variance of other sensors, and if not available at all, 
        # use 1.

        weights = list(self._weights.values()) 
        default_weight = np.ma.masked_invalid(weights).mean()
        if not np.isfinite(default_weight):
            default_weight = 1.0

        for sensor, weight in self._weights.items():
            if not np.isfinite(weight):
                self._weights[sensor] = default_weight
                
        # determine average

        weights = self.current_weights
        values = [measurements.get(k, np.nan) for k in self._last_states]
        values = np.ma.masked_invalid(values)
        print(weights)

        mean = np.ma.average(values, weights=weights)
        self._last_mean = mean

        return mean

@strictdataclass
class DataMixer(MQTTClient):
    """
EXAMPLE USE

    def add_sky_temperature(data: SensorDataType):
        ...
        
    mixer = DataMixer.from_credentials(
                user='generic_obstech',
                topics=['/ElSauce/Weather/Sensors/#'],
                default_publish_topic='/ElSauce/Weather/Mixer',
                pre_processing=add_sky_temperature,
            )

    # start processing regularly in the background
    mixer.start_processing() 

    # start the infinite MQTT loop to receive messages
    mixer.connect()
    mixer.loop_forever()

OPTIONAL KEYWORD ARGUMENTS

    polling_period [TimeDelta, default 1min]
        Every polling_period, received MQTT messages from different data
        sources will be received.

    polling_offset [TimeDelta, default 5s]
        Offset with respect to a round UCT time when polling should occur.

    mixing_method [dict[str, Callable]]
        For each quantity (e.g. temperature, pressure), indicates a function
        that performs the mixing.  By default, np.mean is used.  If a function 
        other than min, max or numpy array functions are used, it needs to 
        accept data in the format {sensor_id: value}.
    
    mix_post_processing [Callable]
        Does post-processing on the mixed quantities, for instance if derived
        quantities must be added.  By default, does nothing.

    mix_post_processing [Callable]
        Does post-processing on the mixed quantities, for instance if derived
        quantities must be added.  By default, does nothing.

    """

    # Mixing occurs on the 5th second of every minute.   We target
    # every sensor to average in the previous minute from measurements at
    # seconds 2, 4, ..., 58 so this should be more than enough to have all
    # sensors ready.

    id: str = 'mixer'
    polling_period: TimeDeltaType = '1min'
    polling_offset: TimeDeltaType = '5s'
    default_mixing_method: AveragerType = BasicSensorFuser(last_states=20)
    mixing_method: dict[str, AveragerType] = Field(default_factory=lambda: {})
    
    pre_processing: PreProcFuncType = Field(default_factory=lambda: inaction)
    post_processing: PostProcFuncType = Field(default_factory=lambda: inaction)    
    _lock: LockType = Field(default_factory=lambda: _Lock(), repr=False)
    _sensor_data: dict = Field(default_factory=lambda: {}, repr=False)

    # @classmethod
    # def from_credentials(cls, *, user: str, **kwargs) -> DataMixer:
    # 
    #   mqtt = MQTTClient.from_credentials(user=user)
    #    kwargs = {**var(mqtt), **kwargs}
    #    return cls(**kwargs)
        
    def on_message(self, obj, userdata, message) -> None:

        """Receive messages.  

        Messages sent with paylod "OK" will be understood as a confirmation
        processing is correctly working, and the OK message will be
        forwarded to /ElSauce/IsRunning/mixer, confirming that both
        threads (periodic execution and MQTT loop) are running as intended.


        Other messages are expected to #/sensors containing the sensor
        data to be merged.

        """

        logger = logging.getLogger()

        print('ON MESSAGE', message.topic)
        payload = message.payload.decode()

        if payload == "OK":
            self.publish(topic='/ElSauce/IsRunning/mixer', payload='OK')
            print('Got OK')
            return

        sensor = message.topic.split('/')[-1]
        logger.debug(f'received MQTT message for sensor: {sensor}')

        with self._lock:
            self._sensor_data[sensor] = json.loads(payload)
        
    def mix_last_data(self) -> None:

        logger = logging.getLogger()

        # get a copy of data and remove it 
        logger.info('mixer: acquire the data published during interval')

        with self._lock:
            data = copy.deepcopy(self._sensor_data)
            for key in self._sensor_data:
                self._sensor_data[key] = {}

        # pre-processing, of interest if cross sensor calibration is
        # needed.
        logger.debug(f'mixer: sensors are: {", ".join(data.keys())}')
           
        self.pre_processing(data)

        # find all existing quantities

        quantities = np.unique([list(d) for d in data.values()])
        mix = {}

        logger.debug(f'mixer: quantities are: {", ".join(quantities)}')

        # mix sensor data here 

        for q in quantities:
            
            default_average = self.default_averaging_method
            average = self.averaging_method.get(q, default_average)
            if average is None: 
                continue

            measurements = {k: v.get(q, np.nan) for k, v in data.items()}
            print(q, measurements)  
            if average in (np.mean, np.median, np.min, np.max, np.sum, min, max):
                values = [v for k, v in measurements.items() if np.isfinite(v)]
                value = average(values) if len(values) else np.nan
            else:
                value = average(measurements)
           
            print(q, value)
 
            mix[q] = value

        self.post_processing(mix)
        
        logger.info('mixer: processing done')

        # publish mix, do a reentrant call to on_message to make sure
        # we're running OK
        self.publish_json(payload=mix)
        ok_topic = self.topics[0].rstrip('#/')
        self.publish(topic=f"{ok_topic}/processing", payload='OK')        

    def start_processing(self) -> None:

        """Start mixing the data in the background at regular intervals."""
        
        @synchronised_call(
            initial_delay=self.polling_offset,
            interval=self.polling_period,
            sync_offset=self.polling_offset,
            threaded=True,
        )
        def periodic_processing() -> None:

            print('periodic processing')           
            logger = logging.getLogger()
 
            try:
                logger.debug('single_step')
                self.mix_last_data()
            except Exception as e:
                logger.error(f'error mixing sensor data: {e}') 
                raise
     
        periodic_processing()

