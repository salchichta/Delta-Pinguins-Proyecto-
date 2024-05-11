from py.cursos import arreglo_cursos


def dataframe_limpio(df):
    # Se quitan las filas con valor 'NULO' en columna 'Codigo_docente'
    df = df[df.Codigo_docente != 'NULO']

    # Quitar filas con valor 0 en 'Capacidad', 'Disponibles' y 'Ocupados'
    df = df[df[['Capacidad', 'Disponibles', 'Ocupados']].any(axis='columns')]

    # Cambiar valores de columna 'Disponibles' a 0
    df.Disponibles[df.Capacidad == 0] = 0

    # Copiar valores de columna 'Ocupados' en columna 'Capacidad'
    df.Capacidad[df.Capacidad == 0] = df.Ocupados

    # Organizar los indices del dataframe
    df = df.set_index(['Nombre_asignatura'])
    df = df.sort_index()

    return(df)


def total_cursos(df):
    cursos = set(df.index.get_level_values(0))
    return(cursos)


def conteo_por_semestre(df):
    numero_semestre = 1
    for semestre in arreglo_cursos:
        imprimir_semestre(numero_semestre, len(semestre))
        for curso in semestre:
            primer_nrc = list(set(df.loc[curso, 'Nrc']))[0]
            grupos = len(set(df.loc[curso, 'Nrc']))
            sesiones = len(df[df.Nrc == primer_nrc])
            print('{}:'.format(curso))
            print('Grupos: {}'.format(grupos))
            print('Sesiones: {} por semana\n'.format(sesiones))
        print("")
        numero_semestre += 1


def imprimir_semestre(numero_semestre, numero_cursos):
    print('\nSemestre {}: {} cursos\n'.format(numero_semestre, numero_cursos))
