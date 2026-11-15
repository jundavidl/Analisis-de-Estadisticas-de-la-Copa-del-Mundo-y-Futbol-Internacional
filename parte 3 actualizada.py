"""
DataLab - Entrega 2: menu con buscar, estadisticas, filtrar y agrupar.
"""
import analisis
import archivos

ARCHIVO_DATOS = "fifa_completo.csv"
MAX_FILAS = 40      # maximo de filas que se imprimen de una vez


def imprimir_tabla(filas):
    """Imprime una lista de diccionarios como tabla alineada.
    Si hay muchas filas, solo muestra las primeras MAX_FILAS."""
    if len(filas) == 0:
        return
    columnas = list(filas[0].keys())
    visibles = filas[:MAX_FILAS]

    anchos = []
    for c in columnas:
        ancho = len(str(c))
        for fila in visibles:
            if len(str(fila[c])) > ancho:
                ancho = len(str(fila[c]))
        anchos.append(ancho)

    encabezado = ""
    for i in range(len(columnas)):
        encabezado += str(columnas[i]).ljust(anchos[i]) + "  "
    print(encabezado)
    print("-" * len(encabezado))
    for fila in visibles:
        linea = ""
        for i in range(len(columnas)):
            linea += str(fila[columnas[i]]).ljust(anchos[i]) + "  "
        print(linea)

    if len(filas) > MAX_FILAS:
        print("... y " + str(len(filas) - MAX_FILAS)
              + " mas (guardalos para verlos todos).")


def elegir_de_lista(opciones, mensaje):
    """Muestra una lista numerada y devuelve la opcion elegida,
    o None si la entrada no es valida."""
    print(mensaje)
    for i in range(len(opciones)):
        print("  " + str(i + 1) + ") " + str(opciones[i]))
    texto = input("Numero: ").strip()
    if texto.isdigit() and 1 <= int(texto) <= len(opciones):
        return opciones[int(texto) - 1]
    print("Opcion no valida.")
    return None


def opcion_buscar(registros):
    termino = input("Termino a buscar (equipo, anio, etc.): ").strip()
    if termino == "":
        print("Escribe algo para buscar.")
        return
    encontrados = analisis.buscar(registros, termino)
    imprimir_tabla(encontrados)
    print("Se encontraron " + str(len(encontrados)) + " registros.")


def opcion_estadisticas(registros):
    campo = elegir_de_lista(analisis.campos_numericos(registros), "Campos numericos:")
    if campo is None:
        return
    stats = analisis.calcular_estadisticas(registros, campo)
    print("Maximo: " + str(stats["maximo"]) + " · Minimo: " + str(stats["minimo"])
          + " · Promedio: " + str(stats["promedio"]))


def opcion_filtrar(registros):
    campo = elegir_de_lista(analisis.campos_numericos(registros), "Campos numericos:")
    if campo is None:
        return
    texto = input("Mostrar registros donde " + campo + " sea mayor que: ").strip()
    limite = archivos.convertir_valor(texto)
    if isinstance(limite, str):
        print("Debes escribir un numero.")
        return
    resultado = analisis.filtrar_mayor_que(registros, campo, limite)
    imprimir_tabla(resultado)
    print("Se encontraron " + str(len(resultado)) + " registros.")


def opcion_agrupar(registros):
    campos = analisis.campos_texto(registros)
    if "Year" in registros[0]:
        campos.append("Year")
    campo = elegir_de_lista(campos, "Agrupar por:")
    if campo is None:
        return
    grupos = analisis.agrupar_por_categoria(registros, campo)
    imprimir_tabla(grupos)
    print("Hay " + str(len(grupos)) + " valores distintos de " + campo + ".")


def mostrar_menu():
    print()
    print("=== DataLab - Mundiales de la FIFA ===")
    print("1. Buscar")
    print("2. Estadisticas basicas")
    print("3. Filtrar por condicion (mayor que)")
    print("4. Agrupar por categoria")
    print("9. Salir")


def main():
    if not archivos.existe_archivo(ARCHIVO_DATOS):
        print("No se encontro " + ARCHIVO_DATOS + " en la carpeta del proyecto.")
        return
    encabezados, registros = archivos.cargar_dataset(ARCHIVO_DATOS)
    print("Dataset cargado: " + ARCHIVO_DATOS + " (" + str(len(registros)) + " registros)")

    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            opcion_buscar(registros)
        elif opcion == "2":
            opcion_estadisticas(registros)
        elif opcion == "3":
            opcion_filtrar(registros)
        elif opcion == "4":
            opcion_agrupar(registros)
        elif opcion == "9":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")



main()
