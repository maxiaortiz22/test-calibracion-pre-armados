from fpdf import FPDF
import datetime
import pandas as pd

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('code/informe/usound.jpg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Informe de calidad de audio', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')

def gen_informe(result_hearingLevel,
                result_frequency_accuracy_results,
                result_narrowBand,
                reslut_linearityTest,
                result_pulseTone,
                result_warbleTone,
                version_app,
                celular,
                calibracion_usada,
                id_informe):

    #Genero los cambios en la data para poder volcarlo en el informe:

    #Filtro hearing level:
    hl_left = result_hearingLevel['Izquierdo']
    hl_right = result_hearingLevel['Derecho']

    hl_left_df = pd.DataFrame({'Frecuencia [Hz]': list(hl_left.keys()),
                               'Nivel [dBHL]': [hl_left[key] for key in hl_left.keys()]})
    
    hl_right_df = pd.DataFrame({'Frecuencia [Hz]': list(hl_right.keys()),
                               'Nivel [dBHL]': [hl_right[key] for key in hl_right.keys()]})
    
    #Filtro frequency accuracy:
    fa_left = result_frequency_accuracy_results['Izquierdo']
    fa_right = result_frequency_accuracy_results['Derecho']

    fa_left_df = pd.DataFrame({'Frecuencia [Hz]': list(fa_left.keys()),
                               'Medición [Hz]': [fa_left[key] for key in fa_left.keys()]})
    
    fa_right_df = pd.DataFrame({'Frecuencia [Hz]': list(fa_right.keys()),
                               'Medición [Hz]': [fa_right[key] for key in fa_right.keys()]})
    
    #Filtro narrow band:
    nb_left = result_narrowBand['Izquierdo']
    nb_right = result_narrowBand['Derecho']

    nb_left_df = pd.DataFrame({'Frecuencia [Hz]': list(nb_left.keys()),
                               'Nivel [dBHL]': [nb_left[key] for key in nb_left.keys()]})
    
    nb_right_df = pd.DataFrame({'Frecuencia [Hz]': list(nb_right.keys()),
                               'Nivel [dBHL]': [nb_right[key] for key in nb_right.keys()]})
    
    #Filtro linearity:
    ln_left = reslut_linearityTest['Izquierdo']
    ln_right = reslut_linearityTest['Derecho']

    ln_left_df = pd.DataFrame({'Nivel esperado [dBHL]': list(ln_left.keys()),
                               'Medición [dBHL]': [ln_left[key] for key in ln_left.keys()]})
    
    ln_right_df = pd.DataFrame({'Nivel esperado [dBHL]': list(ln_right.keys()),
                               'Medición [dBHL]': [ln_right[key] for key in ln_right.keys()]})
    
    #Filtro pulse tone:
    pt_left = result_pulseTone['Izquierdo']
    pt_right = result_pulseTone['Derecho']

    pt_left_df = pd.DataFrame({'Tiempo': list(pt_left.keys()),
                               'Medición [ms]': [pt_left[key] for key in pt_left.keys()]})
    
    pt_right_df = pd.DataFrame({'Tiempo': list(pt_right.keys()),
                               'Medición [ms]': [pt_right[key] for key in pt_right.keys()]})
    
    #Filtro warble tone:
    wt_left = result_warbleTone['Izquierdo']
    wt_right = result_warbleTone['Derecho']

    wt_left_df = pd.DataFrame({'Frecuencia [Hz]': list(wt_left.keys()),
                               'Carrier frequency [Hz]': [wt_left[key]['Carrier frequency [Hz]'] for key in wt_left.keys()],
                               'Modulating frequency [Hz]': [wt_left[key]['Modulating frequency [Hz]'] for key in wt_left.keys()]})
    
    wt_right_df = pd.DataFrame({'Frecuencia [Hz]': list(wt_right.keys()),
                                'Carrier frequency [Hz]': [wt_right[key]['Carrier frequency [Hz]'] for key in wt_right.keys()],
                                'Modulating frequency [Hz]': [wt_right[key]['Modulating frequency [Hz]'] for key in wt_right.keys()]})

    
    #Filtro 

    # Inicio el informe:

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)
    # open the text file in read mode
    e = datetime.datetime.now()
    pdf.cell(0, 5, f'Informe generado el {e.strftime("%d-%m-%Y %H:%M:%S")} - {id_informe}', 0, 1, 'L')

    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.cell(0, 5, f'Versión de la app analizada: {version_app}', 0, 1, 'L')
    pdf.cell(0, 5, f'Dispositivo movil utilizado: {celular}', 0, 1, 'L')
    pdf.cell(0, 5, f'Calibración utilizada: {calibracion_usada}', 0, 1, 'L')

    pdf.cell(0, 5, '', 0, 1, 'L')

    #Test hearing level:
    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de hearing level:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca corroborar la calibración del test aéreo en todas sus ' + 
                       'frecuencias a 60 dBHL.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, f'Izquierdo', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 43
    h = 7

    columnNameList = list(hl_left_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(hl_left_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(hl_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(hl_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(hl_left_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')
    pdf.cell(0, 5, f'Derecho', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    columnNameList = list(hl_right_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(hl_right_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(hl_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(hl_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(hl_right_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))
    
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    #Test frequency accuracy:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de precisión de frecuencia:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca encontrar la precisión de la frecuencia de ' + 
                       'los tonos emitidos.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, f'Izquierdo', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 43
    h = 7

    columnNameList = list(fa_left_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(fa_left_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(fa_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(fa_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(fa_left_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')
    pdf.cell(0, 5, f'Derecho', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    columnNameList = list(fa_right_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(fa_right_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(fa_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(fa_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(fa_right_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))
    
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    #Test de narrow band:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de narrow band:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca corroborar la calibración del narrow band noise para todas las frecuencias.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, f'Izquierdo', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 43
    h = 7

    columnNameList = list(nb_left_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(nb_left_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(nb_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(nb_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(nb_left_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')
    pdf.cell(0, 5, f'Derecho', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    columnNameList = list(nb_right_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(nb_right_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(nb_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(nb_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(nb_right_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))
    
    pdf.cell(90, 5, ' ', 0, 2, 'C')


    #Test de linealidad:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de linealidad:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca evaluar la linealidad del audiómetro para la frecuencia de 1000 Hz:',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, f'Izquierdo', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 43
    h = 7

    columnNameList = list(ln_left_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(ln_left_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(ln_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(ln_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(ln_left_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')
    pdf.cell(0, 5, f'Derecho', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    columnNameList = list(ln_right_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(ln_right_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(ln_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(ln_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(ln_right_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))
    
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    #Test de pulse tone:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de tono pulsante', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca encontrar los tiempos de Rise time, Fall time, ' + 
                       'On time y On/Off time del tono pulsante.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, f'Izquierdo', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 43
    h = 7

    columnNameList = list(pt_left_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(pt_left_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(pt_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(pt_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(pt_left_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')
    pdf.cell(0, 5, f'Derecho', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    columnNameList = list(pt_right_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(pt_right_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(pt_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(pt_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(pt_right_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))
    
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.image('results/test_images/pulse_tone.png', x=None, y=None, w=0, h=0, type='', link='')

    #Test de warble tone:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de tono modulado:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='Para este test se buscan las frecuencia de mensaje y moduladora del Warble Tone.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, f'Izquierdo', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 49
    h = 7

    columnNameList = list(wt_left_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(wt_left_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(wt_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(wt_left_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(wt_left_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')
    pdf.cell(0, 5, f'Derecho', 0, 1, 'C')
    pdf.cell(0, 5, '', 0, 1, 'L')

    columnNameList = list(wt_right_df.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(wt_right_df)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(wt_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(wt_right_df['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(wt_right_df['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))
    
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.output(name=f'results/Informe de calibración de Audio {id_informe}.pdf')