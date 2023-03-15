import numpy as np
import sys

def RMS(y: np.ndarray) -> np.ndarray:
    """ Calcula el valor RMS de una señal """
    return np.sqrt(np.mean(y**2))

def get_comp_value(freq: int, auricular: str) -> float:
    """Obtener el valor de la compensación según el tipo de auricular y la frecuencia"""

    comp_types = {'Supraural (ej: JBL600)' : {'125': 45, '250': 27, '500': 13.5, '750': 9, '1000': 7.5,
                                              '1500': 7.5, '2000': 9, '3000': 11.5, '4000': 12, '6000': 16, '8000': 15.5},
                  "Circumaural (ej: JBL750)": {'125': 30.5, '250': 18, '500': 11, '750': 6, '1000': 5.5,
                                               '1500': 5.5, '2000': 4.5, '3000': 2.5, '4000': 9.5, '6000': 17, '8000': 17.5}}

    return comp_types[auricular][str(freq)]

def get_cal_value(cal: list[float], freq) -> float:
    """Obtener el valor de la calibración según la frecuencia"""

    #Primero obtengo el índice:
    freqs = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    idx = freqs.index(freq)

    #Devuelvo el valor de calibración para la frecuencia especificada:
    return cal[idx]

def hearing_level_value(cal: list[float], data: np.ndarray, freq: int, auricular: str) -> np.ndarray:
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