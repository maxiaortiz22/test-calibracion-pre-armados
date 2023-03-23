import numpy as np
from sys import byteorder
from array import array
import numpy as np
import pyaudio
import sounddevice as sd
from .test_hearing_level import hearing_level
from .test_frequency_accuracy import frequency_accuracy
from .test_narrow_band import narrow_band
from .test_linearity import linearity
from .test_pulse_tone import pulse_tone
from .test_warble_tone import warble_tone
import time
import pandas as pd

class Tests():
    def __init__(self, sr):

        #Parámetros para los tests:
        self.sr = sr
        self.cal_izq: list = []
        self.cal_der: list = []
        self.auricular: str = ''
        self.freqs_auri: list = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
        self.freqs_osea: list = [250, 500, 750, 1000, 1500, 2000, 3000, 4000]
        self.tot_channels = 2

        #Inicializo los resultados de los tests:
        self.hearing_level_results = {"Izquierdo": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                      "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan},
                                      "Derecho": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                      "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan}}
        
        self.frequency_accuracy_results = {"Izquierdo": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                           "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan},
                                           "Derecho": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                           "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan}}
        
        self.narrow_band_results = {"Izquierdo": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                    "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan},
                                    "Derecho": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                    "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan}}
        
        self.linearity_results = {"Izquierdo": {"65 dBHL": np.nan, "60 dBHL": np.nan, "50 dBHL": np.nan, "45 dBHL": np.nan},
                                    "Derecho": {"65 dBHL": np.nan, "60 dBHL": np.nan, "50 dBHL": np.nan, "45 dBHL": np.nan}}
        
        self.pulse_tone_results = {"Izquierdo": {'Rise time': np.nan, 'Fall time': np.nan, 'On time': np.nan, 'On/Off time': np.nan},
                                   "Derecho": {'Rise time': np.nan, 'Fall time': np.nan, 'On time': np.nan, 'On/Off time': np.nan}}

        self.warble_tone_results = {"Izquierdo": {"125":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "250":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "500":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "750":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "1000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "1500": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan},
                                                  "2000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "3000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "4000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "6000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "8000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}},
                                                  
                                    "Derecho":   {"125":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "250":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "500":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "750":  {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "1000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "1500": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan},
                                                  "2000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "3000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "4000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "6000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}, 
                                                  "8000": {'Carrier frequency [Hz]': np.nan, 'Modulating frequency [Hz]': np.nan}}}

    def set_auricular(self, auricular: str) -> None:
        self.auricular = auricular
    
    def get_auricular(self) -> str:
        return self.auricular
    
    def set_channel(self, channel: str) -> None:
        self.channel = channel

    def get_channel(self) -> str:
        return self.channel
    
    def set_freq(self, freq: int) -> None:
        self.freq = freq

    def get_freq(self) -> int:
        return self.freq
    
    def set_level(self, level: str) -> None:
        self.level = level

    def get_level(self) -> str:
        return self.level

    def get_calibration(self) -> list[float]:

        if self.channel == 'Izquierdo':
            return self.cal_izq
        elif self.channel == 'Derecho':
            return self.cal_izq
    
    def split_channels(self, data: np.ndarray) -> np.ndarray:

        if self.channel == 'Izquierdo':
            return np.array([value[0] for value in data])
        elif self.channel == 'Derecho':
            return np.array([value[1] for value in data])

    def record_calibration(self) -> None:

        #Compensaciones:
        supraural_comp: list = [45, 27, 13.5, 9, 7.5, 7.5, 9, 11.5, 12, 16, 15.5]
        circumaural_comp: list = [30.5, 18, 11, 6,  5.5, 5.5, 4.5, 2.5, 9.5, 17, 17.5]
        osea_comp: list = [8.4, 9.8, 11.2, 11.6, 13.5, 13.6, 16.3, 25]

        #Niveles de referencia:
        NIVEL_DBHL_AURI: int = 85
        NIVEL_DBHL_OSEA: int = 30

        cal_izq, cal_der = [], []

        if self.channel == 'Izquierdo':
            if self.auricular == 'Supraural (ej: JBL600)':
                comp = supraural_comp #Compensación para supraural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Siguiente frecuencia {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=self.tot_channels) #Grabo la calibración
                    cal_record = self.split_channels(cal_record)
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_izq.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Supraural de oído izquierdo cargada!')
                self.cal_izq = cal_izq

            elif self.auricular == "Circumaural (ej: JBL750)":
                comp = circumaural_comp #Compensación para circumaural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Siguiente frecuencia {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=self.tot_channels) #Grabo la calibración
                    cal_record = self.split_channels(cal_record)
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_izq.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Circumaural de oído izquierdo cargada!')
                self.cal_izq = cal_izq

            elif self.auricular == "Vincha osea":
                comp = osea_comp #Compensación para vincha ósea

                for i, freq in enumerate(self.freqs_osea):

                    print(f'Siguiente frecuencia {freq} Hz a {NIVEL_DBHL_OSEA} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=self.tot_channels) #Grabo la calibración
                    cal_record = self.split_channels(cal_record)
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_OSEA, comp=comp[i])

                    print('Tono grabado!')

                    cal_izq.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Ósea de oído izquierdo cargada!')
                self.cal_izq = cal_izq
                
            else:
                raise ValueError("No cargaste ningún auricular")
            
        elif self.channel == 'Derecho':
            if self.auricular == 'Supraural (ej: JBL600)':
                comp = supraural_comp #Compensación para supraural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Siguiente frecuencia {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=self.tot_channels) #Grabo la calibración
                    cal_record = self.split_channels(cal_record)
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_der.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Supraural de oído derecho cargada!')
                self.cal_der = cal_der

            elif self.auricular == "Circumaural (ej: JBL750)":
                comp = circumaural_comp #Compensación para circumaural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Siguiente frecuencia {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=self.tot_channels) #Grabo la calibración
                    cal_record = self.split_channels(cal_record)
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_der.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Circumaural de oído derecho cargada!')
                self.cal_der = cal_der

            elif self.auricular == "Vincha osea":
                comp = osea_comp #Compensación para vincha ósea

                for i, freq in enumerate(self.freqs_osea):

                    print(f'Siguiente frecuencia {freq} Hz a {NIVEL_DBHL_OSEA} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=self.tot_channels ) #Grabo la calibración
                    cal_record = self.split_channels(cal_record)
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_OSEA, comp=comp[i])

                    print('Tono grabado!')

                    cal_der.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Ósea de oído derecho cargada!')
                self.cal_der = cal_der
                
            else:
                raise ValueError("No cargaste ningún auricular")

    def set_hearing_level(self) -> None:
        
        record_seconds = 2
        print(f'Grabación de oído {self.channel} y frecuencia {self.freq} Hz')

        data = self.record(RECORD_SECONDS=record_seconds, CHANNELS=self.tot_channels)

        #Me quedo solo con el canal seleccionado:
        data = self.split_channels(data)

        #Obtengo el resultado de hearing level:
        cal = self.get_calibration()
        hl_value = hearing_level.hearing_level_value(cal, data, self.freq, self.auricular)

        #Obtengo la frecuencia que más apareció:
        freq = frequency_accuracy.get_max_freq(data, self.sr)

        #Guardo resultados en el diccionario correspondiente:
        self.hearing_level_results[self.channel][str(self.freq)] = hl_value
        self.frequency_accuracy_results[self.channel][str(self.freq)] = freq

        print(self.hearing_level_results)
        print(self.frequency_accuracy_results)

    def set_narrow_band(self) -> None:
        
        record_seconds = 2
        print(f'Grabación de oído {self.channel} y frecuencia {self.freq} Hz')

        data = self.record(RECORD_SECONDS=record_seconds, CHANNELS=self.tot_channels)

        #Me quedo solo con el canal seleccionado:
        data = self.split_channels(data)

        #Obtengo el resultado de narrow band:
        cal = self.get_calibration()
        nb_value = narrow_band.narrow_band_level_value(cal, data, self.freq, self.auricular)

        #Guardo resultados en el diccionario correspondiente:
        self.narrow_band_results[self.channel][str(self.freq)] = nb_value

        print(self.narrow_band_results)
    
    def set_linearity_test(self) -> None:
        
        record_seconds = 2
        print(f'Grabación de oído {self.channel}, en 1000 Hz a {self.level}')

        data = self.record(RECORD_SECONDS=record_seconds, CHANNELS=self.tot_channels)

        #Me quedo solo con el canal seleccionado:
        data = self.split_channels(data)

        #Obtengo el resultado de linearity test:
        cal = self.get_calibration()
        linearity_value = linearity.linearity_level_value(cal, data, self.auricular)

        #Guardo resultados en el diccionario correspondiente:
        self.linearity_results[self.channel][self.level] = linearity_value

        print(self.linearity_results)
    
    def set_pulse_tone(self) -> None:

        record_seconds = 5
        print(f'Grabación de oído {self.channel}.')

        data = self.record(RECORD_SECONDS=record_seconds, CHANNELS=self.tot_channels)

        #Me quedo solo con el canal seleccionado:
        data = self.split_channels(data)

        #Obtengo el resultado de linearity test:
        pt_value = pulse_tone.get_pulse_tone(data, self.sr)

        #Guardo resultados en el diccionario correspondiente:
        # {'Rise time': np.nan, 'Fall time': np.nan, 'On time': np.nan, 'On/Off time': np.nan}
        self.pulse_tone_results[self.channel]['Rise time'] = pt_value['Rise time [ms]']
        self.pulse_tone_results[self.channel]['Fall time'] = pt_value['Fall time [ms]']
        self.pulse_tone_results[self.channel]['On time'] = pt_value['On time [ms]']
        self.pulse_tone_results[self.channel]['On/Off time'] = pt_value['On/Off time [ms]']

        print(self.pulse_tone_results)

    def set_warble_tone(self) -> None:

        record_seconds = 2
        print(f'Grabación de oído {self.channel} y frecuencia {self.freq} Hz')

        data = self.record(RECORD_SECONDS=record_seconds, CHANNELS=self.tot_channels)

        #Me quedo solo con el canal seleccionado:
        data = self.split_channels(data)

        #Obtengo el resultado de warble tone:
        wt_value = warble_tone.get_frec_mod(data, self.freq, self.sr)

        #Guardo resultados en el diccionario correspondiente:
        self.warble_tone_results[self.channel][str(self.freq)]['Carrier frequency [Hz]'] = wt_value['Carrier frequency [Hz]']
        self.warble_tone_results[self.channel][str(self.freq)]['Modulating frequency [Hz]'] = wt_value['Modulating frequency [Hz]']

        print(self.warble_tone_results)

    def record(self, RECORD_SECONDS, CHANNELS):
        """
        Detect when a signal appears and start recording
        """

        print('Comienza grabación!')

        myrecording = sd.rec(int(RECORD_SECONDS * self.sr), samplerate=self.sr,
                        channels=CHANNELS, blocking=True, dtype='float32')
        
        sd.wait()

        return myrecording