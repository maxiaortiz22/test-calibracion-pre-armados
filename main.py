import code.audio_tests as audio_tests
import customtkinter
from tkinter import *
from code.informe import informe
from code.test_warble_tone.warble_tone import FcError

def calibracion() -> None:

    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Grbando las calibraciones!")
    root.update_idletasks()

    #Genero la calibración:
    tests.record_calibration()

    progress.set(1)
    progress_label.set(f"Calibraciones grabadas!")
    root.update_idletasks()

def linealidad_aerea() -> None:

    global result_linealidad_aerea
    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Test linealidad aérea...")
    root.update_idletasks()

    result_linealidad_aerea = tests.get_linealidad_aerea()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def linealidad_osea() -> None:

    global result_linealidad_osea
    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Test linealidad ósea...")
    root.update_idletasks()

    result_linealidad_osea = tests.get_linealidad_osea()

    progress.set(0.2)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def tono_pulsante() -> None:

    global reslut_tono_pulsante
    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Test tono pulsante...")
    root.update_idletasks()

    reslut_tono_pulsante = tests.get_pulse_tone()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def warble_tone() -> None:

    global result_warble_tone
    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Test warble tone...")
    root.update_idletasks()

    result_warble_tone = tests.get_warble_tone()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def nivel_vocal() -> None:

    global result_nivel_vocal
    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Test nivel vocal...")
    root.update_idletasks()

    result_nivel_vocal = tests.get_nivel_vocal()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def ruido() -> None:

    global result_ruido
    global progress_label
    global root

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    progress.set(0.2)
    progress_label.set(f"Test ruido...")
    root.update_idletasks()

    result_ruido = tests.get_ruido()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()

def on_off_time() -> None:

    global result_on_off
    global progress_label
    global root

    progress.set(0.2)
    progress_label.set(f"Test On/Off time...")
    root.update_idletasks()
    
    result_on_off = tests.get_on_off_time()

    progress.set(1)
    progress_label.set(f"Test grabado!")
    root.update_idletasks()
    

def gen_informe() -> None:

    global progress_label
    global root

    version_app = input('Versión de la app utilizada: ')
    celular = input('Dispositivo usado en la prueba: ')
    calibracion_usada = input('Calibración utilizada: ')
    id_informe = input('ID del informe: ')

    informe.gen_informe(result_linealidad_aerea,
                        result_linealidad_osea,
                        reslut_tono_pulsante,
                        result_warble_tone,
                        result_nivel_vocal,
                        result_ruido,
                        result_on_off,
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

    global root

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    root = customtkinter.CTk()
    root.title("Test de calibración de pre-armados")
    root.geometry("670x580")
    root.iconbitmap('logo.ico')

    recomendacion0 = customtkinter.CTkLabel(root, text='Seleccione el tipo de auricular:')
    recomendacion0.grid(row=0, column=1, pady=5, padx=10)
    tipo_auricular = customtkinter.CTkOptionMenu(root, values=["Supraural (ej: JBL600)", "Circumaural (ej: JBL750)", "Vincha osea"])
    tipo_auricular.grid(row=2, column=1, pady=5, padx=10)
    tipo_auricular.set("Supraural (ej: JBL600)")

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
    hearing_level = customtkinter.CTkButton(root, text="Nivel auditivo", command=linealidad_osea)
    hearing_level.grid(row=7, column=0, pady=5, padx=10)

    hearing_level_frec = customtkinter.CTkOptionMenu(root, values=["125", "250", "500", "750", "1000", "1500",
                                                                 "2000", "3000", "4000", "6000", "8000"])
    hearing_level_frec.grid(row=7, column=2, pady=5, padx=10)

    narrow_band = customtkinter.CTkButton(root, text="Nivel de banda estrecha", command=linealidad_aerea)
    narrow_band.grid(row=8, column=0, pady=5, padx=10)

    narrow_band_frec = customtkinter.CTkOptionMenu(root, values=["125", "250", "500", "750", "1000", "1500",
                                                                 "2000", "3000", "4000", "6000", "8000"])
    narrow_band_frec.grid(row=8, column=2, pady=5, padx=10)

    linearity = customtkinter.CTkButton(root, text="Linealidad", command=on_off_time)
    linearity.grid(row=9, column=0, pady=5, padx=10)

    linearity_level = customtkinter.CTkOptionMenu(root, values=["65 dBHL", "60 dBHL", "50 dBHL", "45 dBHL"])
    linearity_level.grid(row=8, column=2, pady=5, padx=10)

    record_tono_pulsante = customtkinter.CTkButton(root, text="Tono pulsante", command=tono_pulsante)
    record_tono_pulsante.grid(row=10, column=0, pady=5, padx=10)

    record_warble_tone = customtkinter.CTkButton(root, text="Warble tone", command=warble_tone)
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

    calculate = customtkinter.CTkButton(root, text="Informe", command=gen_informe)
    calculate.grid(row=15, column=1, pady=5, padx=10)

    root.mainloop()