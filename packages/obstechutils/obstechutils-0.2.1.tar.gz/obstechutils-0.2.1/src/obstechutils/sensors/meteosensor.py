from __future__ import annotations

from obstechutils.connection import SerialConnection
from obstechutils.dataclasses import strictdataclass, Field
from obstechutils.mqtt import MQTTClient
from obstechutils.precise_timing import average as average_function
from obstechutils import logging
from obstechutils.stats import MeasurementType, MeasurementBinner
from obstechutils.types import TimeDeltaType

from abc import ABC, abstractmethod

@strictdataclass
class MeteoSensor(SerialConnection, ABC):

    vendor_id: int
    product_id: int            
    mqtt: MQTTClient | None = None 
    interval: TimeDeltaType = '1min'
    sampling: TimeDeltaType = Field(default='4s', ge='4s')
    sync: str = 'utc'
    binner: MeasurementBinner = MeasurementBinner()

    def loop_forever(self) -> None:

        logger = logging.getLogger()
        
        if self.mqtt is None:
            raise RuntimeError('No MQTT client set to publish results to')
        self.mqtt.connect() 
        
        self.connect()

        while True:

            m = self.average_measurement()
            if not m:
                msg = 'no average measurement for weather sensor {self.id}'
                logger.error(msg)
                continue

            avg_name = 'last_minute' if self.interval.sec == 60 else 'average'
            topic = f'/ElSauce/Weather/Sensors/{self.id}'
            self.mqtt.publish_json(topic=topic, payload=m)

    def average_measurement(self) -> MeasurementType:

        logger = logging.getLogger()

        averager = average_function(
            interval=self.interval, sampling=self.sampling, sync=self.sync,
            averaging_fun=self.binner, return_times=True,
        )
        def measurement_function():
            m = self.measurement()
            if m and self.mqtt is not None:
                topic = f'/ElSauce/IsRunning/{self.id}'
                self.mqtt.publish(topic=topic, payload='OK')
            return m
        from astropy.time import Time
        logger.info(f'ready to start averaging at {Time.now().isot}')

        (date_start, date_end), dates, m = averager(measurement_function)()

        m['date_start'] = date_start.isot
        m['date_end'] = date_end.isot
        m['n_measurements'] = len(dates)
        m['average_type'] = self.binner.average_type

        logger.info(
            f"sensor {self.id}: measurement average for "
            f"{m['date_start']} - {m['date_end']}: {m['n_measurements']} points"
        )

        m = self.after_averaging(m)
        m = {f'{self.id}_{key}': val for key, val in m.items()}
        print(m)
        return m

    @abstractmethod
    def measurement(self) -> MeasurementType: ...

    def after_averaging(self, m: MeasurementType) -> MeasurementType:
        return m
