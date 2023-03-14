import numpy as np
from sys import byteorder
from array import array
import numpy as np
import pyaudio
import sounddevice as sd
from .test_hearing_level import hearing_level
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

        #Inicializo los resultados de los tests:
        self.hearing_level_results = {"Izquierdo": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
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

        self.warble_tone_results = {"Izquierdo": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                    "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan},
                                    "Derecho": {"125": np.nan, "250": np.nan, "500": np.nan, "750": np.nan, "1000": np.nan, "1500": np.nan,
                                    "2000": np.nan, "3000": np.nan, "4000": np.nan, "6000": np.nan, "8000": np.nan}}

    def set_auricular(self, auricular: str) -> None:
        self.auricular = auricular
    
    def get_auricular(self) -> str:
        return self.auricular
    
    def set_channel(self, channel: str) -> None:
        self.channel = channel

    def get_channel(self) -> str:
        return self.channel

    def record_calibration(self) -> None:

        #Compensaciones:
        supraural_comp: list = [45, 27, 13.5, 9, 7.5, 7.5, 9, 11.5, 12, 16, 15.5]
        circumaural_comp: list = [30.5, 18, 11, 6,  5.5, 5.5, 4.5, 2.5, 9.5, 17, 17.5]
        osea_comp: list = [0, 8.4, 9.8, 11.2, 11.6, 13.5, 13.6, 16.3, 25, 0, 0]

        #Niveles de referencia:
        NIVEL_DBHL_AURI: int = 65
        NIVEL_DBHL_OSEA: int = 30

        cal_izq, cal_der = [], []

        if self.channel == 'Izquierdo':
            if self.auricular == 'Supraural (ej: JBL600)':
                comp = supraural_comp #Compensación para supraural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Esperando tono {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=1) #Grabo la calibración
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_izq.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Supraural cargada!')
                self.cal_izq = cal_izq

            elif self.auricular == "Circumaural (ej: JBL750)":
                comp = circumaural_comp #Compensación para circumaural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Esperando tono {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=1) #Grabo la calibración
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_izq.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Circumaural cargada!')
                self.cal_izq = cal_izq

            elif self.auricular == "Vincha osea":
                comp = osea_comp #Compensación para vincha ósea

                for i, freq in enumerate(self.freqs_osea):

                    print(f'Esperando tono {freq} Hz a {NIVEL_DBHL_OSEA} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=1) #Grabo la calibración
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_OSEA, comp=comp[i])

                    print('Tono grabado!')

                    cal_izq.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Ósea cargada!')
                self.cal_izq = cal_izq
                
            else:
                raise ValueError("No cargaste ningún auricular")
            
        elif self.channel == 'Derecho':
            if self.auricular == 'Supraural (ej: JBL600)':
                comp = supraural_comp #Compensación para supraural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Esperando tono {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=1) #Grabo la calibración
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_der.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Supraural cargada!')
                self.cal_der = cal_der

            elif self.auricular == "Circumaural (ej: JBL750)":
                comp = circumaural_comp #Compensación para circumaural

                for i, freq in enumerate(self.freqs_auri):

                    print(f'Esperando tono {freq} Hz a {NIVEL_DBHL_AURI} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=1) #Grabo la calibración
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_AURI, comp=comp[i])

                    print('Tono grabado!')

                    cal_der.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Circumaural cargada!')
                self.cal_der = cal_der

            elif self.auricular == "Vincha osea":
                comp = osea_comp #Compensación para vincha ósea

                for i, freq in enumerate(self.freqs_osea):

                    print(f'Esperando tono {freq} Hz a {NIVEL_DBHL_OSEA} dBHL')
                    cal_record = self.record(RECORD_SECONDS=2, CHANNELS=1) #Grabo la calibración
                    rms_1Pa = self.RMS_cal(cal_record, nivel_dBHL=NIVEL_DBHL_OSEA, comp=comp[i])

                    print('Tono grabado!')

                    cal_der.append(rms_1Pa)

                    time.sleep(5)
                
                print('Calibración Ósea cargada!')
                self.cal_der = cal_der
                
            else:
                raise ValueError("No cargaste ningún auricular")

    def get_linealidad_aerea(self):
        
        #AGREGAR UN TIEMPO DE ESPERA ENTRE FRECUENCIA Y FRECUENCIA EN ESTE ESTUDIO TAMBIÉN!
        record_seconds: int = 9*2 #[pasos]*[segundos]

        data = np.array([])

        for freq in self.freqs_auri:
            print(f'Frecuencia a grabar: {freq} Hz')
            data_aux = self.record(RECORD_SECONDS=record_seconds, CHANNELS=1)
            print(f'Se grabaron {len(data_aux)} muestras en esta iteración')

            print(f'Grabado {freq} Hz')
            data = np.append(data, data_aux)
            print(f'Se acumularon {len(data)} muestras')

        result = linealidad.linealidad_aerea(self.cal, data, self.sr, self.auricular)

        return result

        
    def get_linealidad_osea(self):

        record_seconds: int = 9*2 #[pasos]*[segundos]

        data = np.array([])

        for freq in self.freqs_osea:
            print(f'Frecuencia a grabar: {freq} Hz')
            data_aux = self.record(RECORD_SECONDS=record_seconds, CHANNELS=1)
            print(f'Se grabaron {len(data_aux)} muestras en esta iteración')

            print(f'Grabado {freq} Hz')
            data = np.append(data, data_aux)
            print(f'Se acumularon {len(data)} muestras')

        result = linealidad.linealidad_osea(self.cal, data, self.sr)

        return result
    
    def get_pulse_tone(self) -> pd.DataFrame:

        record_seconds = 5

        print(f'Esperando para grabar tono pulsante...')
        data = self.record(RECORD_SECONDS=record_seconds, CHANNELS=1)
        print(f'Tono grabado!')

        result = pulse_tone.get_pulse_tone(data, self.sr)

        print('Tiempos calculados!')

        return result

    def get_rta_frec(self):
        #Ver cómo realizar el cambio de la placa al ears!!!
        #https://python-sounddevice.readthedocs.io/en/0.3.7/#:~:text=On%20a%20GNU,in%2C%2016%20out)

        print('Grabando data:')

        rta_frec.get_rta_frec(f_inf=20, f_sup=20000, T=5, Fs=self.sr, A=1, P=3)

        print('Gráfico guardado: results/test_images/rta_frec.png')

    def get_ruido(self):

        noise_types = ['Ruido blanco', 'Ruido vocal', 'NBN 1kHz']
        record_seconds = 10

        data = []

        for noise in noise_types:
            print(f'Grabar {record_seconds} segundos de {noise} a 60 dBHL')
            data_aux = self.record(RECORD_SECONDS=record_seconds, CHANNELS=1)
            
            print(f'{noise} grabado!')
            
            data.append(data_aux)

            time.sleep(10)
        
        result = ruido.get_ruido(data, self.cal[4], self.sr, self.auricular)

        return result

    def get_warble_tone(self):

        record_seconds = 2
        data = []

        for freq in self.freqs_auri:
            print(f'Esperando: warble tone {freq} Hz a 60 dBHL')
            data_aux = self.record(RECORD_SECONDS=record_seconds, CHANNELS=1)
            
            print('Tono grabado!')
            
            data.append(data_aux)

            time.sleep(5)
        
        result = warble_tone.get_frec_mod(data, self.sr)

        return result
    
    def get_nivel_vocal(self):
        
        record_seconds = 40
        data = []

        listas =['Dr. Tato adultos', 'Dr. Tato niños', "SRT E IRF (masculino)", 
                 'SRT E IRF (femenino)', 'Audicom']

        for lista in listas:
            print(f'Esperando: lista {lista} a 85 dBHL')
            data_aux = self.record(RECORD_SECONDS=record_seconds, CHANNELS=1)
            
            print('Lista grabada!')
            
            data.append(data_aux)

            time.sleep(30)
        
        result = nivel_vocal.get_nivel_vocal(data, self.cal[4])

        return result
    
    def get_on_off_time(self):

        record_seconds = 7

        print(f'Se grabaran {record_seconds} s de audio, en este tiempo tiene que encender y apagar el tono en 60 dBHL')

        myrecording = sd.rec(int(record_seconds * self.sr), samplerate=self.sr,
                        channels=1, blocking=True, dtype='float32') 
        sd.wait()

        myrecording = myrecording.flatten()

        return on_off.get_on_off_time(myrecording, self.sr)

    def RMS(self, y):
        """ Calcula el valor RMS de una señal """
        return np.sqrt(np.mean(y**2))

    def RMS_cal(self, y, nivel_dBHL, comp):
        """ Calcula el valor RMS de una señal de calibración de cualquier nivel y lo paso a 94 dBSPL,
            lo que equivale a 1 Pa """

        rms = np.sqrt(np.mean(y**2)) #Obento el RMS al nivel que fue grabado

        rms_1Pa = rms / (20*10**(-6) * 10**((nivel_dBHL+comp)/20)) #Paso le RMS a 1 Pa
        
        return rms_1Pa

    def is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.THRESHOLD


    def record(self, RECORD_SECONDS, CHANNELS):
        """
        Detect when a signal appears and start recording
        """

        print('Comienza grabación!')

        myrecording = sd.rec(int(RECORD_SECONDS * self.sr), samplerate=self.sr,
                        channels=CHANNELS, blocking=True, dtype='float32')
        
        sd.wait()

        return myrecording