from __future__ import annotations

from obstechutils.sensors.meteosensor import MeteoSensor
from obstechutils.sensors.pyrgeometer import PyrgeometerCalibrator
from obstechutils.dataclasses import strictdataclass
from obstechutils.stats import MeasurementBinner, MeasurementType
from obstechutils import logging

import numpy as np
import time
from astropy.time import Time

from typing import ClassVar

@strictdataclass
class AAG(MeteoSensor):
            
    timeout: float = 1.0
    baudrate: int = 9600
    id: str = 'aag'
    binner: MeasurementBinner = MeasurementBinner()
    cloud_calib: PyrgeometerCalibrator | None = None
    read_wind: bool = False 

    ANSWER_LENGTH: ClassVar[dict[str, int]] = {
        'C!': 60, 'V!': 30, 'T!': 30, 'S!': 30, 'E!': 30, 'v!': 30,
    }

    def read_device(self, cmd):
       
        # Except for wind readings (deactivated by default), this calls
        # takes ~ 0.1 s if successful on the first try, but might take
        # up to ~ 1.2s if not
 
        ntries = 2
        for i in range(ntries):
            try:
                self.flush_input()
                self.flush_output()
                self.send(cmd)
                answer_size = self.ANSWER_LENGTH[cmd]
                rcv = self.receive(size=answer_size)
                rcv = rcv[3:].split('\x11')[0].split()
                rcv = [x.split('!')[0] for x in rcv]
                rcv = [int(x) for x in rcv]
                return rcv
            except Exception as e:
                print(f'device error: {e}')
                if i < ntries-1:
                    self.reconnect()
                else:
                    raise

    def measurement(self):

        # A measurement lasts about 1.5s if wind is read and 0.5s otherwise
        # (the default), in most cases.  It could last significantly more if
        # there are recurrent errors, but timeout on read ensures it won't
        # block.

        logger = logging.getLogger('obstechutils')

        try:
            temperature = 0.01 * self.read_device('T!')[0]
            temperature_ir = 0.01 * self.read_device('S!')[0]
            rain_freq = self.read_device('E!')[0]
            try:
                d5, d6, d7 = self.read_device('C!')
            except:
                d5, d6, d7 = 0, 0, 0

            wind = self.read_device('V!') if self.read_wind else []

        except Exception as e:
            logger.warn(f"could not read AAG sensor: {e}")
            return {}

        # a bit mysterious here
        d6 = 56/(1023 / min(max(d6, 1), 1022) - 1)
        d7 = 56/(1023 / min(max(d6, 1), 1022) - 1)
        d7 = 1/(np.log10(d7)/3450 + 1 / (273.15 + 25)) - 273.15

        m = dict(
            unix_time = Time.now().unix,
            temperature = temperature,
            temperature_ir = temperature_ir,
            voltage = d5,
            rain_freq = d6,
            light = d7,
        )
        
        # check if wind is obtained
        if len(wind):
            m['wind_speed'] = wind[0] / 3.6 

        return m

    def after_averaging(self, m: MeasurementType) -> MeasurementType:

        if (cal := self.cloud_calib) is not None:

            temperature = m['temperature']
            temperature_ir = m['temperature_ir']
            temperature_sky = cal.sky_temperature(temperature, temperature_ir)
            m['temperature_sky'] = temperature_sky

        return m


