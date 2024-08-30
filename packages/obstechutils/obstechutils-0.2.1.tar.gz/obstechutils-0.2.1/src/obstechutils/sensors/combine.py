from obstechutils.stats import MeasurementType

import re
import numpy as np
from typing import Callable

def combine_measurements(
    m: list[MeasurementType],
    quantity: Callable = lambda s: re.sub(s, '_[A-Za-z0-9]+$', ''),
    average_fun: Callable = np.mean
):
    """Combine measurements from different sensors

Arguments

    m [list[dict]]:
        List of measurements
    quantity [Callable]:
        A function that gives the quantity (e.g. 'temperature' or
        'pressure') from a measurement key (e.g. 'temperature_aag1',
        'pressure_nm150')
    average_fun: Callable = np.mean

    """
    # measurements from different sensors have distinct keys
    # since they end with _sensorID
    m = {**m for m in measurements}
    
    all_quantities = np.unique([quantity(key) for key in m.keys()])

    m_combined = { 
        q: average_fun([m[k] for k in m.keys() if quantity(k) == q])
            for q in all_quantitites
    }
