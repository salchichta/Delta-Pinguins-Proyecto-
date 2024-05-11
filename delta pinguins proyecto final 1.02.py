import random
import os
from tabulate import tabulate
from funciones import mostrarAgregadas

agregadas = []
revisados = []   # Para que no se elijan 2 NRC de una misma materia

x = [    # Linea de tiempo en la semana de clases
    ".", ".", ".", ".", ".", ".", ".", ".",
    ".", ".", ".", ".", ".", ".", ".", ".",
    ".", ".", ".", ".", ".", ".", ".", ".",
    ".", ".", ".", ".", ".", ".", ".", ".",
    ".", ".", ".", ".", ".", ".", ".", ".",
    ".", ".", ".", ".", ".", ".", ".", "."]

nrc = []
dias = []
cantidadDias = []
cantidadHoras = []
indices = []

nrcP = []
diasP = []
cantidadDiasP = []
cantidadHorasP = []
indicesP = []

materias = [
    [  # Ciencias Básicas
        ["Cálculo diferencial",
         [["1367", 4, ["L", "Mi", "J"], [[0], [16, 17], [24]]],
          ["1378", 4, ["L", "M", "Mi"], [[4, 5], [12], [20, 21]]],
             ["1383", 4, ["J", "L", "Mi"], [[24, 25], [1], [17]]],
             ["1389", 4, ["V", "M", "Mi"], [[33, 34], [10], [18]]],
             ["1392", 4, ["L", "Mi", "V"], [[0], [16, 17], [32]]],
             ["1395", 4, ["M", "Mi", "V"], [[11], [19], [35, 36]]],
             ["1418", 4, ["L", "Mi", "J"], [[2], [18], [26, 27]]],
             ["1438", 4, ["M", "Mi", "V"], [[10], [18, 19], [34]]],
             ["1458", 4, ["Mi", "J", "V"], [[16], [24], [32, 33]]],
             ["1462", 4, ["L", "J", "Mi"], [[2, 3], [27], [20]]]
          ]],
        ["Química general",
         [["2092", 3, ["Mi", "J"], [[18], [26, 27]]],
          ["2098", 3, ["L", "Mi"], [[5], [21, 22]]],
             ["2102", 3, ["J", "L"], [[24, 25], [1]]],
             ["2112", 3, ["Mi", "V"], [[17, 18], [34]]]
          ]],
        ["Matemáticas básicas",
         [["1602", 2, ["V", "L", "J"], [[32, 33], [1], [25]]],
          ["1604", 2, ["V", "M", "Mi"], [[33, 34], [10], [18]]],
             ["1606", 2, ["L", "Mi", "V"], [[0], [16], [32, 33]]],
             ["1608", 2, ["Mi", "J", "V"], [[18], [26], [34, 35]]],
             ["1617", 2, ["Mi", "J", "V"], [[19, 20], [28], [36]]],
             ["1625", 2, ["M", "J", "V"], [[11], [27, 28], [35]]],
             ["1626", 2, ["Mi", "L", "M"], [[18, 19], [4], [12]]]
          ]],
        ["Álgebra lineal",
         [["2068",  3, ["L", "M"], [[2], [10, 11]]],
          ["2069",  3, ["L", "Mi"], [[0], [16, 17]]],
             ["2070", 3, ["L", "Mi"], [[2, 3], [19]]]
          ]],
        ["Cálculo integral",
         [["1475", 4, ["V", "L", "M"], [[35, 36], [4], [12]]],
          ["1485", 4, ["V", "L", "M"], [[32, 33], [1], [9]]]
          ]],
        ["Física I",
         [["1716", 4, ["L", "M", "J"], [[3], [11], [27, 28]]],
          ["1730", 4, ["L", "J", "V"], [[1], [25], [33, 34]]],
             ["1731", 4, ["M", "J", "V"], [[9], [25], [33, 34]]],
             ["1735", 4, ["Mi", "L", "M"], [[18, 19], [3], [11]]]
          ]],
        ["Cálculo vectorial",
         [["1500", 4, ["L", "Mi", "J"], [[0], [16, 17], [24]]],
          ["1502", 4, ["Mi", "L", "M"], [[19], [4], [12, 13]]],
             ["1503", 4, ["L", "Mi", "J"], [[1, 2], [18], [26]]],
             ["1505", 4, ["Mi", "J", "V"], [[20], [28], [36, 37]]],
             ["1511", 4, ["J", "L", "M"], [[26, 27], [3], [11]]],
             ["1512", 4, ["Mi", "J", "V"], [[18], [26], [34, 35]]]
          ]],
        ["Física II",
         [["1744", 4, ["V", "L", "M"], [[35, 36], [4], [12]]],
          ["1746", 4, ["L", "M", "Mi"], [[0], [8], [16, 17]]],
             ["1748", 4, ["L", "Mi", "V"], [[2], [18, 19], [34]]],
             ["1756", 4, ["L", "M", "J"], [[0], [8], [24, 25]]]
          ]],
        ["Estadística y probabilidad",
         [["1582", 3, ["J", "Mi", "V"], [[28, 29], [21], [37]]],
          ["1583", 3, ["M", "L", "J"], [[10, 11], [3], [27]]],
             ["1592", 3, ["J", "L", "M"], [[27, 28], [4], [12]]]
          ]],
        ["Ecuaciones diferenciales y en diferencia",
         [["1525", 3, ["L", "Mi", "J"], [[3, 4], [19], [27]]],
          ["1527", 3, ["L", "M", "J"], [[3], [11], [27, 28]]],
             ["1529", 3, ["Mi", "L", "M"], [[19, 20], [4], [12]]],
             ["1532", 3, ["Mi", "J", "V"], [[20], [28], [36, 37]]]
          ]]],
    [  # Ing. de Sistemas
        ["Fundamentos de programación",
         [["1474", 3, ["L", "Mi"], [[0], [16, 17]]],
          ["1490", 3, ["Mi", "L"], [[16, 17], [1]]]
          ]],
        ["Programación",
         [["1535", 3, ["Mi", "M"], [[16], [9, 10]]],
          ["1550", 3, ["L", "J"], [[0], [26, 27]]],
             ["1552", 3, ["L", "M"], [[4], [12, 13]]]
          ]],
        ["Estructura de datos",
         [["2469", 3, ["L", "M"], [[5, 6], [14, 15]]]
          ]],
        ["Procesamiento numérico",
         [["2373", 3, ["M", "J"], [[16, 17], [26]]]
          ]],
        ["Tópicos especiales de ciencias computacionales",
         [["1169", 3, ["M", "L"], [[8, 9], [1]]]
          ]],
        ["Comunicaciones y redes",
         [["1155", 3, ["J", "L"], [[24, 25], [1]]]
          ]],
        ["Inteligencia artificial",
         [["1141", 3, ["M", "J"], [[12], [28, 29]]]
          ]],
        ["Sistemas operativos",
         [["1163", 3, ["M", "J"], [[10], [26, 27]]]
          ]]],
    [  # Humanidades y otros
        ["Taller de comprensión lectora",
         [["1157", 3, ["L", "Mi"], [[2], [19, 20]]],
          ["1170", 3, ["M", "V"], [[10], [34, 35]]],
             ["1185", 3, ["V", "Mi"], [[33, 34], [19]]],
             ["1190", 3, ["Mi", "V"], [[16], [32, 33]]],
             ["1193", 3, ["Mi", "V"], [[17], [34, 35]]]
          ]],
        ["Taller de escritura académica",
         [["1698", 3, ["M", "V"], [[8], [32, 33]]]
          ]],
        ["Constitución política",
         [["1263", 2, ["L"], [[2, 3]]],
          ["1267", 2, ["Mi"], [[18, 19]]],
             ["1272", 2, ["V"], [[34, 35]]],
             ["1273", 2, ["M"], [[10, 11]]],
             ["1259", 2, ["L"], [[3, 4]]]
          ]],
        ["Ética",
         [["1227", 2, ["L"], [[0, 1]]],
          ["1228", 2, ["L"], [[2, 3]]],
             ["1234", 2, ["Mi"], [[18, 19]]],
             ["1236", 2, ["V"], [[32, 33]]],
             ["1238", 2, ["V"], [[34, 35]]]
          ]],
        ["Inglés I",
         [["1732", 2, ["L", "M", "Mi", "J"], [[4], [12], [20], [28]]],
          ["1692", 2, ["L", "M", "Mi", "J"], [[0], [8], [16], [24]]],
             ["1702", 2, ["L", "Mi", "J", "V"], [[1], [18], [26], [34]]],
             ["1706", 2, ["L", "M", "J", "V"], [[3], [11], [27], [35]]]
          ]],
        ["Inglés II",
         [["1754", 2, ["L", "M", "Mi", "J"], [[4], [12], [20], [28]]],
          ["1757", 2, ["L", "M", "Mi", "J"], [[3], [11], [19], [27]]],
             ["1745", 2, ["M", "Mi", "J", "V"], [[11], [19], [27], [35]]],
             ["1866", 2, ["L", "M", "Mi", "J"], [[2], [10], [18], [26]]],
             ["1875", 2, ["L", "M", "Mi", "V"], [[1], [9], [17], [33]]],
             ["1883", 2, ["V", "Mi"], [[36, 37], [22, 23]]],
             ["1751", 2, ["L", "M", "Mi", "J"], [[4], [12], [20], [28]]],
             ["1772", 2, ["M", "Mi", "J", "V"], [[8], [16], [24], [32]]],
             ["1777", 2, ["L", "M", "J", "V"], [[1], [9], [25], [33]]]
          ]],
        ["Inglés III",
         [["1956", 2, ["M", "Mi", "J", "V"], [[8], [16], [24], [32]]],
          ["1932", 2, ["M", "L"], [[12, 13], [6, 7]]],
             ["1933", 2, ["L", "M", "Mi", "J"], [[4], [15], [20], [28]]],
             ["1935", 2, ["L", "M", "Mi", "J"], [[5], [13], [21], [29]]],
             ["1937", 2, ["L", "Mi", "J", "V"], [[2], [18], [26], [34]]],
             ["1927", 2, ["L", "M", "Mi", "J"], [[3], [11], [19], [27]]],
             ["1968", 2, ["Mi", "V"], [[12, 13], [38, 39]]]
          ]],
        ["Inglés IV",
         [["1993", 2, ["L", "M", "Mi", "J"], [[5], [13], [21], [29]]],
          ["2024", 2, ["M", "Mi", "J", "V"], [[10], [18], [26], [34]]],
             ["2000", 2, ["J", "V"], [[28, 29], [36, 37]]],
             ["2005", 2, ["L", "M", "J", "V"], [[3], [11], [27], [35]]],
             ["2008", 2, ["L", "M", "J", "V"], [[0], [8], [24], [32]]],
             ["2012", 2, ["L", "Mi", "J", "V"], [[3], [19], [27], [35]]],
             ["1975", 2, ["L", "M", "Mi", "J"], [[1], [9], [17], [25]]],
             ["2027", 2, ["M", "V"], [[12, 13], [38, 39]]],
             ["2572", 2, ["M", "V"], [[12, 13], [38, 39]]]
          ]],
        ["Inglés V",
         [["2034", 2, ["L", "M", "Mi", "J"], [[4], [12], [20], [28]]],
          ["2036", 2, ["L", "M", "Mi", "J"], [[5], [13], [21], [29]]],
             ["2037", 2, ["L", "M", "Mi", "J"], [[3], [10], [18], [26]]],
             ["2033", 2, ["L", "M", "J", "V"], [[0], [8], [24], [32]]],
             ["2040", 2, ["L", "M", "Mi", "J"], [[6], [14], [22], [30]]]
          ]],
        ["Entorno económico",
         [["1896", 3, ["Mi", "V"], [[19], [35, 36]]]
          ]],
        ["Formulación y evaluación de proyectos",
         [["1248", 3, ["J", "L"], [[27, 28], [4]]],
          ["1261", 3, ["L", "Mi"], [[0, 1], [16]]]
          ]]]]
sumaCreditos = 0

while True:
    try:
        os.system('cls')
        print("*****GENERADOR DE HORARIOS*****")
        mostrarAgregadas(agregadas)
        print("1.Agregar una materia")
        print("2.Generar horario")
        op = int(input("Opción: "))
        if(op == 1):
            while True:
                try:
                    os.system('cls')
                    print("*****AGREGAR UNA MATERIA*****")
                    print("1.Ciencias básicas")
                    print("2.Ingeniería de sistemas")
                    print("3.Humanidades y otros")
                    op2 = int(input("Opción: "))
                    if(op2 == 1):
                        while True:
                            try:
                                os.system('cls')
                                print("*****CIENCIAS BÁSICAS*****")
                                # Lista las materias de ciencias básicas
                                for i in range(len(materias[0])):
                                    print(f"{i+1}.{materias[0][i][0]}")
                                op3 = int(input("Opción: "))
                                # Comprueba una opción numérica válida
                                if(op3 > 0 and op3 <= len(materias[0])):
                                    # Comprueba que no se pase de 18 créditos y procede a agregar materias
                                    if(sumaCreditos + materias[0][op3-1][1][0][1] <= 18):
                                        # Se van sumando los créditos delas materias que agregamos
                                        sumaCreditos += materias[0][op3-1][1][0][1]
                                        # Se agrega a materias un conjunto con los nombres de las materias y la dirección a su lista NRC
                                        agregadas.append([materias[0][op3-1][0], [0, op3-1, 1]])
                                        print(f"La suma actual de los créditos es: {sumaCreditos}")
                                        input(
                                            "\nMateria agregada exitosamente, presione Enter para continuar...")
                                        break
                                    else:
                                        input(
                                            "\nNo puede pasarse de 18 créditos, presione Enter para continuar...")
                                        break
                                else:
                                    input(
                                        "\nNo ha digitado una opción válida, presione Enter para continuar...")
                            except ValueError:
                                input("\nNo ha digitado una opción válida, presione Enter para continuar...")
                    elif(op2 == 2):
                        while True:
                            try:
                                os.system('cls')
                                # Se repite lo mismo que en la opción 1
                                print("*****INGENIERÍA DE SISTEMAS*****")
                                for i in range(len(materias[1])):
                                    print(f"{i+1}.{materias[1][i][0]}")
                                op3 = int(input("Opción: "))
                                if(op3 > 0 and op3 <= len(materias[1])):
                                    if(sumaCreditos + materias[1][op3-1][1][0][1] <= 18):
                                        sumaCreditos += materias[1][op3-1][1][0][1]
                                        agregadas.append([materias[1][op3-1][0], [1, op3-1, 1]])
                                        print(f"La suma actual de los créditos es: {sumaCreditos}")
                                        input(
                                            "\nMateria agregada exitosamente, presione Enter para continuar...")
                                        break
                                    else:
                                        input(
                                            "\nNo puede pasarse de 18 créditos, presione Enter para continuar...")
                                        break
                                else:
                                    input(
                                        "\nNo ha digitado una opción válida, presione Enter para continuar...")
                            except ValueError:
                                input("\nNo ha digitado una opción válida, presione Enter para continuar...")
                    elif(op2 == 3):
                        while True:
                            try:
                                os.system('cls')
                                # Se repite lo mismo que en la opción 1
                                print("*****HUMANIDADES Y OTROS*****")
                                for i in range(len(materias[2])):
                                    print(f"{i+1}.{materias[2][i][0]}")
                                op3 = int(input("Opción: "))
                                if(op3 > 0 and op3 <= len(materias[2])):
                                    if(sumaCreditos + materias[2][op3-1][1][0][1] <= 18):
                                        sumaCreditos += materias[2][op3-1][1][0][1]
                                        agregadas.append([materias[2][op3-1][0], [2, op3-1, 1]])
                                        print(f"La suma actual de los créditos es: {sumaCreditos}")
                                        input(
                                            "\nMateria agregada exitosamente, presione Enter para continuar...")
                                        break
                                    else:
                                        input(
                                            "\nNo puede pasarse de 18 créditos, presione Enter para continuar...")
                                        break
                                else:
                                    input(
                                        "\nNo ha digitado una opción válida, presione Enter para continuar...")
                            except ValueError:
                                input("\nNo ha digitado una opción válida, presione Enter para continuar...")
                    else:
                        input("\nNo ha digitado una opción válida, presione Enter para continuar...")

                    # *****INICIO PRUEBA***** Comprobamos si agregadas tiene la forma: agregadas = [[nombreMateria],[direcciónListaNRC]]
                    # print(agregadas)
                    # input()
                    # *****FIN PRUEBA*****

                    if(op2 > 0 and op2 <= 3):
                        break
                except ValueError:  # Cuando se sale del tercer menú, enseguida se sale del segundo también y queda en el inicio.
                    input("\nNo ha digitado una opción válida, presione Enter para continuar...")
        elif(op == 2):
            iteraciones = 100000    # número de iteraciones
            while True:
                seCruza = []    # Vector que guarda las materias que se cruzan con todas las demás
                cond3 = True
                # Paso 1: Generar solución aleatoria x
                for i in range(len(agregadas)):    # 0 hasta número de materias agregadas - 1

                    # Al ejecutar más de una vez el paso 1, verifica las materias que ya tienen un NRC inicial asignado
                    for z in range(len(revisados)):
                        if(agregadas[i] == revisados[z]):
                            cond3 = False
                            break
                        else:
                            cond3 = True
                    if(not cond3):
                        continue

                    # Número de NRCs en la materia
                    for j in range(len(materias[agregadas[i][1][0]][agregadas[i][1][1]][agregadas[i][1][2]])):
                        # Se van eligiendo uno por uno los NRC de la materia
                        nrcAlAzar = materias[agregadas[i][1][0]
                                             ][agregadas[i][1][1]][agregadas[i][1][2]][j][0]
                        # Los numeros de cada día que se ve en la semana
                        diasAlAzar = materias[agregadas[i][1][0]
                                              ][agregadas[i][1][1]][agregadas[i][1][2]][j][3]
                        cantidadHorasNrcAlAzar = []    # Cuantas horas se ven en cada día de la semana
                        for k in range(len(diasAlAzar)):
                            cantidadHorasNrcAlAzar.append(len(diasAlAzar[k]))

                        for k in range(len(diasAlAzar)):    # Se define si se cruza con otra materia
                            for a in range(cantidadHorasNrcAlAzar[k]):
                                if(x[diasAlAzar[k][a]] == "."):
                                    cond = True
                                else:
                                    cond = False
                                    break
                            if(not cond):
                                break
                        if(not cond):    # Decide si se busca otro NRC
                            # Si todos los NRC de alguna materia se cruzan
                            if(j == len(materias[agregadas[i][1][0]][agregadas[i][1][1]][agregadas[i][1][2]]) - 1):
                                seCruza.append(i)
                            continue
                        elif(cond):    # Agrega las materias al horario
                            for k in range(len(diasAlAzar)):
                                for a in range(cantidadHorasNrcAlAzar[k]):
                                    x[diasAlAzar[k][a]] = nrcAlAzar
                            nrc.append(nrcAlAzar)
                            indices.append(j)    # NRC en la lista de NRC de la materia
                            dias.append(diasAlAzar)
                            cantidadDias.append(len(diasAlAzar))
                            cantidadHoras.append(cantidadHorasNrcAlAzar)
                            break
                    revisados.append(agregadas[i])
                if(len(seCruza) > 0):
                    print("")
                    for i in range(len(seCruza)):
                        print(
                            f"Todos  los NRC de '{agregadas[seCruza[i]][0]}' se cruzan con otra materia. Por favor intente con otra.")
                        agregadas[seCruza[i]] = "."
                    for i in range(len(agregadas)-1, -1, -1):
                        if(agregadas[i] == "."):
                            agregadas.pop(i)
                    input()
                    cond2 = False
                    break
                else:
                    cond2 = True
                    break

            if(cond2):

                # Paso 2: Perturbar x para obtener xp
                while (iteraciones > 0):
                    xp = x[:]    # Crear la x perturbada.
                    nrcP = nrc[:]
                    indicesP = indices[:]
                    diasP = dias[:]
                    cantidadDiasP = cantidadDias[:]
                    cantidadHorasP = cantidadHoras[:]

                    while True:
                        indElem1 = random.randrange(len(nrc))
                        indElem2 = random.randrange(len(nrc))
                        elem1 = nrc[indElem1]    # NRCs que vamos a borrar
                        elem2 = nrc[indElem2]
                        if(elem1 != elem2):
                            break

                    for i in range(len(xp)):    # Se borran los NRC de la solución (0-47)
                        if(xp[i] == elem1):
                            xp[i] = "."
                        elif(xp[i] == elem2):
                            xp[i] = "."

                    condP1 = False
                    condP2 = False
                    condP3 = False
                    # Si los dos son True, significa que no se cruzan con las otras materias del horario

                    while not condP1:
                        indiceAlAzarP1 = random.randrange(
                            len(materias[agregadas[indElem1][1][0]][agregadas[indElem1][1][1]][agregadas[indElem1][1][2]]))
                        nrcAlAzarP1 = materias[agregadas[indElem1][1][0]][agregadas[indElem1]
                                                                          [1][1]][agregadas[indElem1][1][2]][indiceAlAzarP1][0]
                        diasAlAzarP1 = materias[agregadas[indElem1][1][0]][agregadas[indElem1]
                                                                           [1][1]][agregadas[indElem1][1][2]][indiceAlAzarP1][3]
                        cantidadHorasNrcAlAzarP1 = []
                        for b in range(len(diasAlAzarP1)):
                            cantidadHorasNrcAlAzarP1.append(len(diasAlAzarP1[b]))

                        for c in range(len(diasAlAzarP1)):    # Se define si se cruza con otra materia
                            for d in range(cantidadHorasNrcAlAzarP1[c]):
                                if(xp[diasAlAzarP1[c][d]] == "."):
                                    condP1 = True
                                else:
                                    condP1 = False
                                    break
                            if(not condP1):
                                break

                    while not condP2:
                        indiceAlAzarP2 = random.randrange(
                            len(materias[agregadas[indElem2][1][0]][agregadas[indElem2][1][1]][agregadas[indElem2][1][2]]))
                        nrcAlAzarP2 = materias[agregadas[indElem2][1][0]][agregadas[indElem2]
                                                                          [1][1]][agregadas[indElem2][1][2]][indiceAlAzarP2][0]
                        diasAlAzarP2 = materias[agregadas[indElem2][1][0]][agregadas[indElem2]
                                                                           [1][1]][agregadas[indElem2][1][2]][indiceAlAzarP2][3]
                        cantidadHorasNrcAlAzarP2 = []
                        for b in range(len(diasAlAzarP2)):
                            cantidadHorasNrcAlAzarP2.append(len(diasAlAzarP2[b]))

                        for c in range(len(diasAlAzarP2)):    # Se define si se cruza con otra materia
                            for d in range(cantidadHorasNrcAlAzarP2[c]):
                                if(xp[diasAlAzarP2[c][d]] == "."):
                                    condP2 = True
                                else:
                                    condP2 = False
                                    break
                            if(not condP2):
                                break

                    for i in range(len(diasAlAzarP1)):
                        for j in range(cantidadHorasNrcAlAzarP1[i]):
                            for k in range(len(diasAlAzarP2)):
                                for m in range(cantidadHorasNrcAlAzarP2[k]):
                                    if(diasAlAzarP1[i][j] != diasAlAzarP2[k][m]):
                                        condP3 = True
                                    else:
                                        condP3 = False
                                        break
                                if(not condP3):
                                    break
                            if(not condP3):
                                break
                        if(not condP3):
                            break

                    if(not condP3):
                        continue
                    elif(condP3):
                        indicesP[indElem1] = indiceAlAzarP1
                        nrcP[indElem1] = nrcAlAzarP1
                        diasP[indElem1] = diasAlAzarP1
                        cantidadDiasP[indElem1] = len(diasAlAzarP1)
                        cantidadHorasP[indElem1] = cantidadHorasNrcAlAzarP1
                        for e in range(len(diasAlAzarP1)):
                            for f in range(cantidadHorasNrcAlAzarP1[e]):
                                xp[diasAlAzarP1[e][f]] = nrcAlAzarP1

                        indicesP[indElem2] = indiceAlAzarP2
                        nrcP[indElem2] = nrcAlAzarP2
                        diasP[indElem2] = diasAlAzarP2
                        cantidadDiasP[indElem2] = len(diasAlAzarP2)
                        cantidadHorasP[indElem2] = cantidadHorasNrcAlAzarP2
                        for e in range(len(diasAlAzarP2)):
                            for f in range(cantidadHorasNrcAlAzarP2[e]):
                                xp[diasAlAzarP2[e][f]] = nrcAlAzarP2

                    # Paso 3: calcular función objetivo zx y zxp y compararlas
                    zx = 0    # Función objetivo con respecto a x
                    horas = []

                    for i in range(len(x)):
                        if(x[i] != "."):
                            horas.append(i)
                    horas.reverse()

                    for i in range(len(horas)):
                        if(i == len(horas)-1):  # Parar de sumar cuando se llega al último índice
                            break
                        else:
                            # Sumar las distancias entre las ciudades
                            zx += (horas[i] - horas[i+1])

                    zxp = 0    # Función objetivo con respecto a x
                    horasp = []

                    for i in range(len(xp)):
                        if(xp[i] != "."):
                            horasp.append(i)
                    horasp.reverse()

                    for i in range(len(horasp)):
                        if(i == len(horasp)-1):  # Parar de sumar cuando se llega al último índice
                            break
                        else:
                            # Sumar las distancias entre las ciudades
                            zxp += (horasp[i] - horasp[i+1])

                    # *****INICIO PRUEBA*****
                    # print(f"zx:{zx}        zxp:{zxp}")
                    # input()
                    # *****FIN PRUEBA*****

                    if(zxp < zx):
                        # Paso 3.1: Actualizar valor de x
                        x = xp[:]
                        nrc = nrcP[:]
                        dias = diasP[:]
                        cantidadDias = cantidadDiasP[:]
                        cantidadHoras = cantidadHorasP[:]
                        indices = indicesP[:]
                    iteraciones -= 1
                # print(indices)
                # print(nrc)
                # print(dias)
                # print(cantidadDias)
                # print(cantidadHoras)
                # print(x)

            if(cond2):
                semanas = [[0, 8, 16, 24, 32, 40], [1, 9, 17, 25, 33, 41], [2, 10, 18, 26, 34, 42], [3, 11, 19, 27, 35, 43], [
                    4, 12, 20, 28, 36, 44], [5, 13, 21, 29, 37, 45], [6, 14, 22, 30, 38, 46], [7, 15, 23, 31, 39, 47]]
                horario = [[], [], [], [], [], [], [], []]

                for i in range(8):
                    for j in range(6):
                        horario[i].append(x[semanas[i][j]])

                print("*****GENERAR HORARIO*****")
                print("\nNRC de las materias:")
                for i in range(len(nrc)):
                    print(f"  - {nrc[i]}: {agregadas[i][0]}")
                print("\nEl mejor horario para usted es:")
                print(tabulate(horario, headers=['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado'], showindex=[
                      "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9"]))
                input()
    except ValueError:
        input("\nNo ha digitado una opción válida, presione Enter para continuar...")
