import streamlit as st
import pandas as pd
import numpy as np

def getData():
    df = pd.read_excel('calculadoraHorarios.xlsx')
    rename = {'Materias que puede dar cada profesor': 'Materias profesor', 
              'Disponibilidad de horario de cada profesor': 'Horarios profesor'}
    df.rename(columns=rename,inplace=True)
    return df


def getMaterias(df):
    materias = df[['Profesores','Materias profesor']]
    materias.set_index('Profesores',inplace=True)

    for i in range(len(df.index)):
        materias['Materias profesor'][i] = list(materias['Materias profesor'][i])

    materias = materias.explode('Materias profesor')
    materias = pd.get_dummies(materias,prefix='',prefix_sep='')
    materias = materias.groupby(level=0).sum()

    return materias

def getHorarios(df):
    horarios = df[['Profesores','Horarios profesor']]
    horarios.set_index('Profesores',inplace=True)

    horarios = horarios.astype({'Horarios profesor':'string'})
    hlist =[]

    for i in range(len(df.index)):
        hlist.append(list(horarios['Horarios profesor'][i]))

    horarios['Horarios'] = hlist
    horarios.drop(columns='Horarios profesor',inplace=True)

    horarios = horarios.explode('Horarios')
    horarios = pd.get_dummies(horarios,prefix='',prefix_sep='')
    horarios = horarios.groupby(level=0).sum()
    for i in range(len(df.index)):
        horarios.iloc[i] *= df['Costos Profesores'].iloc[i]

    for i in range(len(df.index)):
        for j in range(len(df.index)):
            if (horarios[str(i+1)][j] > 0):
                horarios[str(i+1)][j] += df['Costos Horarios'][i]
    horarios.replace(0, np.nan, inplace=True)

    return horarios

def minimoMateria(materia,materias,horarios):
    profesores = materias[materias[materia] == 1].index
    select = [x in profesores for x in horarios.index]
    k = horarios[select]
    hor = k.min().idxmin()
    prof = k[k[hor] == k.min().min()].index[0]
    horarios.loc[:,hor][prof] = np.nan
    return (materia,prof,hor,k.min().min())

def getHorarioOptimo(df):
    materias = getMaterias(df)
    horarios = getHorarios(df)

    minimos = []

    for i in range(len(df.index)):
        minimos.append(minimoMateria(df['Materias'].iloc[i],materias,horarios))

    seleccion = pd.DataFrame(minimos, columns=['Materia','Profesor','Horario','Costo'])
    seleccion.loc[:,'Costo'] = seleccion['Costo'] + df['Costos Materias']

    salones = df[['Salones','Costos Salones']]
    salones = salones.sort_values(by='Costos Salones')

    sel_hor = seleccion['Horario'].value_counts()
    seleccion['Salon'] = 'x'
    sel_salon = []

    for horario in sel_hor.index:
        indice = seleccion[seleccion['Horario'] == str(horario)].index
        for i in range(len(indice)):
            seleccion.loc[indice[i],'Salon'] = salones['Salones'].iloc[i]
            seleccion.loc[indice[i],'Costo'] += salones['Costos Salones'].iloc[i]
    
    return seleccion

st.set_page_config(
    page_title='Horario Óptimo',
    layout='wide',
)

st.title('Calculadora de Horario Óptimo')

st.text('''Esta calculadora te permitirá encontrar la programación de horario óptima para las clases. Ya se encuentra un horario 
preestablecido, pero puedes modificar las restricciones de horarios, materias y costos, así como los nombres de los 
profesores.''')
        
st.text('Para que la calculadora funcione correctamente, deben escribirse los nombres de los profesores alfabéticamente.')

df = getData()
dfEditado = st.experimental_data_editor(df)
horarioFinal = getHorarioOptimo(dfEditado)
horarioFinal.to_excel('horarioFinal.xlsx',index=False)

st.text('De acuerdo a la información presentada, el horario óptimo es el siguiente.')

st.dataframe(horarioFinal)

costo = horarioFinal['Costo'].sum()*1000
st.text(f'El costo asociado a este horario es de {costo}')

with open('horarioFinal.xlsx', "rb") as template_file:
        template_byte = template_file.read()

st.download_button(label="Descargar horario",
                    data=template_byte,
                    file_name="horarioFinal.xlsx",
                    mime='application/octet-stream')
