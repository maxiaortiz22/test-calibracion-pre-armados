import numpy as np
from scipy.fft import rfft, rfftfreq

def get_max_freq(data: np.ndarray, fs: int):
    """Función para devolver la frecuencia máxima de una señal de audio"""

    #Obtengo la transformada:
    yf = rfft(data)
    yf = 20 * np.log10(np.abs(yf) / np.max(np.abs(yf)))
    xf = rfftfreq(data.size, 1 / fs)

    #Obtengo la frecuencia con mayor nivel:
    idx = np.argmax(yf)

    return xf[idx]