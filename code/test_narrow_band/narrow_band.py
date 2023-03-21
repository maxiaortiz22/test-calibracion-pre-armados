import numpy as np
import sys

def RMS(y: np.ndarray) -> np.ndarray:
    """ Calcula el valor RMS de una señal """
    return np.sqrt(np.mean(y**2))

def get_comp_value(freq: int, auricular: str) -> float:
    """Obtener el valor de la compensación según el tipo de auricular y la frecuencia"""

    comp_types = {'Supraural (ej: JBL600)' : {'125': 49.0, '250': 31.0, '500': 17.5, '750': 14.0, '1000': 13.5,
                                              '1500': 13.5, '2000': 15.0, '3000': 17.5, '4000': 17.0, '6000': 21.0, '8000': 20.5},
                  "Circumaural (ej: JBL750)": {'125': 34.5, '250': 22.0, '500': 15.0, '750': 11.0, '1000': 11.5,
                                               '1500': 11.5, '2000': 10.5, '3000': 8.5, '4000': 14.5, '6000': 22.0, '8000': 22.5}}

    return comp_types[auricular][str(freq)]

def get_cal_value(cal: list[float], freq) -> float:
    """Obtener el valor de la calibración según la frecuencia"""

    #Primero obtengo el índice:
    freqs = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    idx = freqs.index(freq)

    #Devuelvo el valor de calibración para la frecuencia especificada:
    return cal[idx]

def narrow_band_level_value(cal: list[float], data: np.ndarray, freq: int, auricular: str) -> np.ndarray:
    """Función para calcular el nivel de la señal grabada"""

    #Compensación:
    comp = get_comp_value(freq, auricular)

    #Calibro la señal:
    cal = get_cal_value(cal, freq)
    data = data / cal

    #Obtengo el valor de la señal en dBHL:

    signal_dB = 20*np.log10(RMS(data) / (20*10**(-6)) + sys.float_info.epsilon )

    signal_dBHL = np.round(signal_dB - comp, 2)

    return signal_dBHL