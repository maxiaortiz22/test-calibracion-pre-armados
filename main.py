import code.audio_tests as audio_tests
import customtkinter
from tkinter import *
from code.informe import informe
from code.test_warble_tone.warble_tone import FcError
import sounddevice as sd

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def retornoStream() -> None:

    global progress_label
    global root

    duration = 5.0 # 5 segundos

    progress.set(0.2)
    progress_label.set(f"Retorno...")
    root.update_idletasks()

    with sd.Stream(channels=2, dtype='float32', callback=callback):
        sd.sleep(int(duration * 1000))
    
    progress.set(1)
    progress_label.set(f"")
    root.update_idletasks()

def calibracion() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)
    #Especifico el dispositivo de entrada:
    input_microphone = input_device.get()
    sd.default.device = str(input_microphone)
    #Especifico el canal de medición:
    channel_selected = channel.get()
    tests.set_channel(channel_selected)

    progress.set(0.2)
    progress_label.set(f"Grbando las calibraciones!")
    root.update_idletasks()

    #Genero la calibración:
    tests.record_calibration()

    progress.set(1)
    progress_label.set(f"Calibraciones grabadas!")
    root.update_idletasks()

def hearingLevel() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)
    #Especifico el canal de medición:
    channel_selected = channel.get()
    tests.set_channel(channel_selected)
    #Frecuencia:
    freq = int(hearing_level_frec.get())
    tests.set_freq(freq)
    #Especifico el dispositivo de entrada:
    input_microphone = input_device.get()
    sd.default.device = str(input_microphone)

    progress.set(0.2)
    progress_label.set(f"Test hearing level {freq} Hz...")
    root.update_idletasks()

    tests.set_hearing_level()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def narrowBand() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)
    #Especifico el canal de medición:
    channel_selected = channel.get()
    tests.set_channel(channel_selected)
    #Frecuencia:
    freq = int(narrow_band_frec.get())
    tests.set_freq(freq)
    #Especifico el dispositivo de entrada:
    input_microphone = input_device.get()
    sd.default.device = str(input_microphone)

    progress.set(0.2)
    progress_label.set(f"Test narrow band {freq} Hz...")
    root.update_idletasks()

    tests.set_narrow_band()

    progress.set(0.2)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def linearityTest() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)
    #Especifico el canal de medición:
    channel_selected = channel.get()
    tests.set_channel(channel_selected)
    #nievel:
    level = linearity_level.get()
    tests.set_level(level)
    #Especifico el dispositivo de entrada:
    input_microphone = input_device.get()
    sd.default.device = str(input_microphone)

    progress.set(0.2)
    progress_label.set(f"Test de linealidad...")
    root.update_idletasks()

    tests.set_linearity_test()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def pulseTone() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)
    #Especifico el canal de medición:
    channel_selected = channel.get()
    tests.set_channel(channel_selected)
    #Especifico el dispositivo de entrada:
    input_microphone = input_device.get()
    sd.default.device = str(input_microphone)

    progress.set(0.2)
    progress_label.set(f"Test pulse tone...")
    root.update_idletasks()

    tests.set_pulse_tone()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def warbleTone() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)
    #Especifico el canal de medición:
    channel_selected = channel.get()
    tests.set_channel(channel_selected)
    #Frecuencia:
    freq = int(warble_tone_frec.get())
    tests.set_freq(freq)
    #Especifico el dispositivo de entrada:
    input_microphone = input_device.get()
    sd.default.device = str(input_microphone)

    progress.set(0.2)
    progress_label.set(f"Test warble tone...")
    root.update_idletasks()

    tests.set_warble_tone()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()
    

def genInforme() -> None:

    global progress_label
    global root

    version_app = input('Versión de la app utilizada: ')
    celular = input('Dispositivo usado en la prueba: ')
    calibracion_usada = input('Calibración utilizada: ')
    id_informe = input('ID del informe: ')

    result_hearingLevel = tests.hearing_level_results
    result_frequency_accuracy_results = tests.frequency_accuracy_results
    result_narrowBand = tests.narrow_band_results
    reslut_linearityTest = tests.linearity_results
    result_pulseTone = tests.pulse_tone_results
    result_warbleTone = tests.warble_tone_results

    informe.gen_informe(result_hearingLevel,
                        result_frequency_accuracy_results,
                        result_narrowBand,
                        reslut_linearityTest,
                        result_pulseTone,
                        result_warbleTone,
                        version_app,
                        celular,
                        calibracion_usada,
                        id_informe)

    progress.set(1)
    progress_label.set(f"Informe generado!")
    root.update_idletasks()
                        
    print('Informe generado!')

if __name__ == '__main__':

    #Instancio la clase con los tests:
    sr = 44100
    tests = audio_tests.Tests(sr)

    #Obtengo los dispositivos de entrada disponibles:
    input_devices = []
    for device in sd.query_devices():
        if 'Input' in device['name']:
            input_devices.append(device['name'])

    global root

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    root = customtkinter.CTk()
    root.title("Test de calibración de pre-armados")
    root.geometry("680x580")
    root.iconbitmap('logo.ico')

    recomendacion_entrada = customtkinter.CTkLabel(root, text='Seleccione el dispositivo de entrada:')
    recomendacion_entrada.grid(row=0, column=0, pady=5, padx=10)
    input_device = customtkinter.CTkOptionMenu(root, values=input_devices)
    input_device.grid(row=1, column=0, pady=5, padx=10)
    #tipo_auricular.set("Supraural (ej: JBL600)")

    recomendacion0 = customtkinter.CTkLabel(root, text='Seleccione el tipo de auricular:')
    recomendacion0.grid(row=0, column=1, pady=5, padx=10)
    tipo_auricular = customtkinter.CTkOptionMenu(root, values=["Supraural (ej: JBL600)", "Circumaural (ej: JBL750)", "Vincha osea"])
    tipo_auricular.grid(row=1, column=1, pady=5, padx=10)
    tipo_auricular.set("Supraural (ej: JBL600)")

    recomendacion_retorno = customtkinter.CTkLabel(root, text='Escuchar retorno:')
    recomendacion_retorno.grid(row=0, column=2, pady=5, padx=10)
    retorno = customtkinter.CTkButton(root, text="Retorno", command=retornoStream)
    retorno.grid(row=1, column=2, pady=5, padx=10)

    recomendacion1 = customtkinter.CTkLabel(root, text='Calibrar cada vez que mueva la ganancia')
    recomendacion1.grid(row=4, column=0, pady=5, padx=10)

    cal_low = customtkinter.CTkButton(root, text="Calibración", command=calibracion)
    cal_low.grid(row=5, column=0, pady=5, padx=10)

    recomendacion_channel = customtkinter.CTkLabel(root, text='Elija el canal')
    recomendacion_channel.grid(row=4, column=2, pady=5, padx=10)

    channel = customtkinter.CTkOptionMenu(root, values=["Izquierdo", "Derecho"])
    channel.grid(row=5, column=2, pady=5, padx=10)

    recomendacion1 = customtkinter.CTkLabel(root, text='Pruebas:')
    recomendacion1.grid(row=6, column=0, pady=5, padx=10)

    recomendacion1_test = customtkinter.CTkLabel(root, text='Ajuste de medición:')
    recomendacion1_test.grid(row=6, column=2, pady=5, padx=10)

    #De este mismo voy a sacar el Frequency Accuracy Test:
    hearing_level = customtkinter.CTkButton(root, text="Nivel auditivo", command=hearingLevel)
    hearing_level.grid(row=7, column=0, pady=5, padx=10)

    hearing_level_frec = customtkinter.CTkOptionMenu(root, values=["125", "250", "500", "750", "1000", "1500",
                                                                 "2000", "3000", "4000", "6000", "8000"])
    hearing_level_frec.grid(row=7, column=2, pady=5, padx=10)

    narrow_band = customtkinter.CTkButton(root, text="Nivel de banda estrecha", command=narrowBand)
    narrow_band.grid(row=8, column=0, pady=5, padx=10)

    narrow_band_frec = customtkinter.CTkOptionMenu(root, values=["125", "250", "500", "750", "1000", "1500",
                                                                 "2000", "3000", "4000", "6000", "8000"])
    narrow_band_frec.grid(row=8, column=2, pady=5, padx=10)

    linearity = customtkinter.CTkButton(root, text="Linealidad", command=linearityTest)
    linearity.grid(row=9, column=0, pady=5, padx=10)

    linearity_level = customtkinter.CTkOptionMenu(root, values=["65 dBHL", "60 dBHL", "50 dBHL", "45 dBHL"])
    linearity_level.grid(row=9, column=2, pady=5, padx=10)

    record_tono_pulsante = customtkinter.CTkButton(root, text="Tono pulsante", command=pulseTone)
    record_tono_pulsante.grid(row=10, column=0, pady=5, padx=10)

    record_warble_tone = customtkinter.CTkButton(root, text="Warble tone", command=warbleTone)
    record_warble_tone.grid(row=11, column=0, pady=5, padx=10)

    warble_tone_frec = customtkinter.CTkOptionMenu(root, values=["125", "250", "500", "750", "1000", "1500",
                                                                 "2000", "3000", "4000", "6000", "8000"])
    warble_tone_frec.grid(row=11, column=2, pady=5, padx=10)

    global progress_label
    progress_label = StringVar()
    progress_label.set("")
    recomendacion2 = customtkinter.CTkLabel(root, textvariable=progress_label)
    recomendacion2.grid(row=13, column=1, pady=5, padx=10)

    progress = customtkinter.CTkProgressBar(root)
    progress.grid(row=14, column=1, pady=5, padx=10)
    progress.set(0)

    calculate = customtkinter.CTkButton(root, text="Informe", command=genInforme)
    calculate.grid(row=15, column=1, pady=5, padx=10)

    root.mainloop()