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


