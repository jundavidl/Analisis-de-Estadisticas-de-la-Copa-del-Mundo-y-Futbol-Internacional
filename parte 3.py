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


def opcion_buscar(encabezados, filas):
    termino = input("Termino a buscar (equipo, anio, etc.): ")
    if termino.strip() == "":
        print("Escribe algo para buscar.")
        return
    encontradas = buscar(filas, termino)
    if len(encontradas) > 0:
        imprimir_tabla(encabezados, encontradas)
    print("Se encontraron " + str(len(encontradas)) + " registros.")


def mostrar_menu():
    print()
    print("=== DataLab - Mundiales de la FIFA ===")
    print("1. Buscar")
    print("5. Salir")


def main():
    encabezados, filas = cargar_dataset("fifa_pequeno.csv")
    print("Dataset cargado: fifa_pequeno.csv (" + str(len(filas)) + " registros)")

    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            opcion_buscar(encabezados, filas)
        elif opcion == "5":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")



main()