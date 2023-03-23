from scipy.fft import rfft, rfftfreq
import numpy as np
from scipy.signal import find_peaks
from statistics import mode
from scipy.signal import butter, sosfilt

class FcError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'FcError: {self.message}'
        else:
            return 'FcError: no se encontró la frecuencia de mensaje'

def filtered_signals(data: np.ndarray, band: int, fs: float) -> np.ndarray:

    order = 4

    lowcut = band/np.sqrt(2) #Frecuencia de corte inferior bandas de octava
    highcut = band*np.sqrt(2) #Frecuencia de corte  superior bandas de octava

    sos = butter(order, [lowcut, highcut], fs=fs, btype='bandpass', output='sos')

    filtered_audio = sosfilt(sos, data)

    return filtered_audio

def get_frec_mod(data: np.ndarray, freq: int, fs: float) -> dict[str, float]:

    fc, fm = 0, 0

    filtered_data = filtered_signals(data, freq, fs)

    audio = filtered_data / np.max(np.abs(filtered_data))
    
    N = len(audio)
    yf = np.array(rfft(audio))
    xf = rfftfreq(N, 1 / fs)

    yf = 20 * np.log10(np.abs(yf) / np.max(np.abs(yf)))

    local_max_idx, _ = find_peaks(yf, height=-30) #Revisar el valor de height

    xf_max_list = [xf[i] for i in local_max_idx]

    fm_calc = []
    for t in range(len(xf_max_list)-1):
        fm_calc.append(xf_max_list[t+1]-xf_max_list[t])

    fm = mode(fm_calc) #Me quedo con el valor que más se repita, esperando que este sea el correcto!

    fc = freq

    data = {'Carrier frequency [Hz]': fc,
            'Modulating frequency [Hz]': fm}

    return data