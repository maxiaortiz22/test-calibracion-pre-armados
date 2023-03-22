import numpy as np
import sys

def RMS(y: np.ndarray) -> np.ndarray:
    """ Calcula el valor RMS de una señal """
    return np.sqrt(np.mean(y**2))

def get_comp_value(auricular: str) -> float:
    """Obtener el valor de la compensación según el tipo de auricular y la frecuencia"""

    comp_types = {'Supraural (ej: JBL600)' : 7.5,
                  "Circumaural (ej: JBL750)": 5.5}

    return comp_types[auricular]

def get_cal_value(cal: list[float]) -> float:
    """Obtener el valor de la calibración según la frecuencia"""

    #Devuelvo el valor de calibración para la frecuencia de 1000 Hz:
    return cal[4]

def linearity_level_value(cal: list[float], data: np.ndarray, auricular: str) -> np.ndarray:
    """Función para calcular el nivel de la señal grabada"""

    #Compensación:
    comp = get_comp_value(auricular)

    #Calibro la señal:
    cal = get_cal_value(cal)
    data = data / cal

    #Obtengo el valor de la señal en dBHL:

    signal_dB = 20*np.log10(RMS(data) / (20*10**(-6)) + sys.float_info.epsilon )

    signal_dBHL = np.round(signal_dB - comp, 2)

    return signal_dBHL