

def cargar_dataset(ruta):
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


def mostrar_menu():
    print()
    print("=== DataLab - Mundiales de la FIFA ===")
    print("5. Salir")


def main():
    encabezados, filas = cargar_dataset("fifa_pequeno.csv")
    print("Dataset cargado: fifa_pequeno.csv (" + str(len(filas)) + " registros)")
    imprimir_tabla(encabezados, filas[:10])

    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "5":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")



main()
