import numpy as np
from scipy.fft import rfft, rfftfreq

def get_max_freq(data: np.ndarray, fs: int):
    """Función para devolver la frecuencia máxima de una señal de audio"""

    #Obtengo la transformada:
    yf = np.abs(rfft(data))
    xf = rfftfreq(data.size, 1 / fs)

    #Obtengo la frecuencia con mayor nivel:
    idx = np.argmax(yf)

    return xf[idx]