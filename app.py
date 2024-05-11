import pandas as pd
from py.funciones import (dataframe_limpio, total_cursos, conteo_por_semestre)

df = pd.read_csv('conteo-de-cursos/csv/dataframe.csv')
df = dataframe_limpio(df)

cursos = total_cursos(df)
print('Total de cursos: {}\n'.format(len(cursos)))

conteo_por_semestre(df)
