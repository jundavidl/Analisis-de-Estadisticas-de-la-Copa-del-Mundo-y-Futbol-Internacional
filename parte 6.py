"""
Version 6: opcion opcional Agrupar por categoria.
Dataset: Mundiales de la FIFA (1930-2022).
"""


def cargar_dataset(ruta):
    """Lee el CSV con open() y split(). Devuelve (encabezados, filas).
    Cada fila es una lista de textos."""
    archivo = open(ruta, encoding="utf-8")
    encabezados = []
    filas = []
    primera = True
    for linea in archivo:
        linea = linea.strip()
        if linea == "":
            continue
        partes = linea.split(",")
        if primera:
            encabezados = partes
            primera = False
        else:
            filas.append(partes)
    archivo.close()
    return encabezados, filas


def es_numero(texto):
    """True si el texto representa un numero (entero o decimal, con o sin signo)."""
    limpio = texto.strip()
    if limpio.startswith("-"):
        limpio = limpio[1:]
    limpio = limpio.replace(".", "", 1)
    return limpio.isdigit()


def columnas_numericas(encabezados, filas):
    """Devuelve la lista de indices de las columnas cuyo valor es numerico
    en TODAS las filas."""
    indices = []
    for i in range(len(encabezados)):
        todas_numericas = True
        for fila in filas:
            if not es_numero(fila[i]):
                todas_numericas = False
                break
        if todas_numericas:
            indices.append(i)
    return indices


def imprimir_tabla(encabezados, filas):
    """Imprime las filas alineadas en columnas, con su encabezado."""
    anchos = []
    for i in range(len(encabezados)):
        ancho = len(encabezados[i])
        for fila in filas:
            if len(fila[i]) > ancho:
                ancho = len(fila[i])
        anchos.append(ancho)

    linea = ""
    for i in range(len(encabezados)):
        linea += encabezados[i].ljust(anchos[i]) + "  "
    print(linea)
    print("-" * len(linea))

    for fila in filas:
        linea = ""
        for i in range(len(fila)):
            linea += fila[i].ljust(anchos[i]) + "  "
        print(linea)


def buscar(filas, termino):
    """Devuelve las filas que contienen el termino en cualquiera de sus
    campos (sin distinguir mayusculas de minusculas)."""
    termino = termino.lower().strip()
    encontradas = []
    for fila in filas:
        for campo in fila:
            if termino in campo.lower():
                encontradas.append(fila)
                break  # ya coincidio, no repetir la fila
    return encontradas


def calcular_estadisticas(filas, indice):
    """Calcula maximo, minimo y promedio de la columna `indice`
    usando un bucle y variables acumuladoras. Devuelve (max, min, promedio)."""
    maximo = float(filas[0][indice])
    minimo = float(filas[0][indice])
    suma = 0.0
    cantidad = 0
    for fila in filas:
        valor = float(fila[indice])
        if valor > maximo:
            maximo = valor
        if valor < minimo:
            minimo = valor
        suma += valor
        cantidad += 1
    promedio = suma / cantidad
    return maximo, minimo, promedio


def filtrar_mayor_que(filas, indice, limite):
    """Devuelve las filas donde la columna numerica `indice` supera `limite`."""
    resultado = []
    for fila in filas:
        if float(fila[indice]) > limite:
            resultado.append(fila)
    return resultado


def agrupar_por_categoria(filas, indice):
    """Cuenta cuantos registros hay por cada valor distinto de la columna de
    texto `indice`. Devuelve dos listas paralelas (valores, conteos)
    ordenadas de mayor a menor conteo."""
    valores = []
    conteos = []
    for fila in filas:
        valor = fila[indice]
        if valor in valores:
            posicion = valores.index(valor)
            conteos[posicion] += 1
        else:
            valores.append(valor)
            conteos.append(1)

    # Ordenamiento por seleccion (de mayor a menor), hecho a mano
    n = len(valores)
    for i in range(n):
        mayor = i
        for j in range(i + 1, n):
            if conteos[j] > conteos[mayor]:
                mayor = j
        conteos[i], conteos[mayor] = conteos[mayor], conteos[i]
        valores[i], valores[mayor] = valores[mayor], valores[i]
    return valores, conteos


def elegir_columna(encabezados, indices, mensaje):
    """Muestra las columnas disponibles y devuelve el indice elegido,
    o -1 si la entrada no es valida."""
    print(mensaje)
    for i in indices:
        print("  " + str(i) + ") " + encabezados[i])
    texto = input("Numero de columna: ").strip()
    if texto.isdigit() and int(texto) in indices:
        return int(texto)
    print("Opcion no valida.")
    return -1


def opcion_buscar(encabezados, filas):
    termino = input("Termino a buscar (equipo, anio, etc.): ")
    encontradas = buscar(filas, termino)
    if len(encontradas) > 0:
        imprimir_tabla(encabezados, encontradas)
    print("Se encontraron " + str(len(encontradas)) + " registros.")


def opcion_estadisticas(encabezados, filas):
    numericas = columnas_numericas(encabezados, filas)
    indice = elegir_columna(encabezados, numericas, "Columnas numericas:")
    if indice == -1:
        return
    maximo, minimo, promedio = calcular_estadisticas(filas, indice)
    print(encabezados[indice] + " -> Maximo: " + str(maximo)
          + " · Minimo: " + str(minimo)
          + " · Promedio: " + str(round(promedio, 2)))


def opcion_filtrar(encabezados, filas):
    numericas = columnas_numericas(encabezados, filas)
    indice = elegir_columna(encabezados, numericas, "Columnas numericas:")
    if indice == -1:
        return
    texto = input("Mostrar registros donde " + encabezados[indice] + " sea mayor que: ").strip()
    if not es_numero(texto):
        print("Debes escribir un numero.")
        return
    resultado = filtrar_mayor_que(filas, indice, float(texto))
    if len(resultado) > 0:
        imprimir_tabla(encabezados, resultado)
    print("Se encontraron " + str(len(resultado)) + " registros.")


def opcion_agrupar(encabezados, filas):
    numericas = columnas_numericas(encabezados, filas)
    # Las columnas de texto son las que NO son numericas
    textuales = []
    for i in range(len(encabezados)):
        if i not in numericas:
            textuales.append(i)
    # Year tambien sirve para agrupar (cuantos equipos por mundial)
    if 0 not in textuales:
        textuales.append(0)
    indice = elegir_columna(encabezados, textuales, "Agrupar por:")
    if indice == -1:
        return
    valores, conteos = agrupar_por_categoria(filas, indice)
    for i in range(len(valores)):
        print(valores[i] + ": " + str(conteos[i]))


def mostrar_menu():
    print()
    print("=== DataLab - Mundiales de la FIFA ===")
    print("1. Buscar")
    print("2. Estadisticas basicas")
    print("3. Filtrar por condicion (mayor que)")
    print("4. Agrupar por categoria")
    print("5. Salir")


def main():
    encabezados, filas = cargar_dataset("fifa_pequeno.csv")
    print("Dataset cargado: fifa_pequeno.csv (" + str(len(filas)) + " registros)")

    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            opcion_buscar(encabezados, filas)
        elif opcion == "2":
            opcion_estadisticas(encabezados, filas)
        elif opcion == "3":
            opcion_filtrar(encabezados, filas)
        elif opcion == "4":
            opcion_agrupar(encabezados, filas)
        elif opcion == "5":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")



main()