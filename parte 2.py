

import csv
import json
import os
from datetime import datetime


CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(CARPETA, "resultados")
ARCHIVO_HISTORIAL = os.path.join(CARPETA, "historial.csv")
ARCHIVO_RESUMEN = os.path.join(CARPETA, "resumen.json")



def existe_archivo(nombre):
    
    return os.path.exists(os.path.join(CARPETA, nombre))


def convertir_valor(texto):

    limpio = texto.strip()
    sin_signo = limpio[1:] if limpio.startswith("-") else limpio
    if sin_signo.isdigit():
        return int(limpio)
    if sin_signo.replace(".", "", 1).isdigit():
        return float(limpio)
    return limpio


def cargar_dataset(nombre_archivo):
    
    ruta = os.path.join(CARPETA, nombre_archivo)
    archivo = open(ruta, encoding="utf-8", newline="")
    lector = csv.reader(archivo)
    encabezados = next(lector)
    registros = []
    for fila in lector:
        if len(fila) == 0:      # linea vacia
            continue
        registro = {}
        for i in range(len(encabezados)):
            registro[encabezados[i]] = convertir_valor(fila[i])
        registros.append(registro)
    archivo.close()
    return encabezados, registros




def guardar_csv(ruta, filas):

    archivo = open(ruta, "w", encoding="utf-8", newline="")
    escritor = csv.writer(archivo)
    if len(filas) > 0:
        columnas = list(filas[0].keys())
        escritor.writerow(columnas)
        for fila in filas:
            escritor.writerow([fila[c] for c in columnas])
    archivo.close()


def cargar_csv(ruta):

    archivo = open(ruta, encoding="utf-8", newline="")
    lector = csv.reader(archivo)
    columnas = next(lector, None)
    filas = []
    if columnas is not None:
        for fila in lector:
            if len(fila) == 0:
                continue
            registro = {}
            for i in range(len(columnas)):
                registro[columnas[i]] = convertir_valor(fila[i])
            filas.append(registro)
    archivo.close()
    return filas


def guardar_json(ruta, datos):
  
    archivo = open(ruta, "w", encoding="utf-8")
    json.dump(datos, archivo, indent=2, ensure_ascii=False)
    archivo.close()


def cargar_json(ruta):

    archivo = open(ruta, encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()
    return datos




def a_filas(datos):
    
    if isinstance(datos, list):
        return datos
    filas = []
    for clave in datos:
        filas.append({"campo": clave, "valor": str(datos[clave])})
    return filas


def limpiar_nombre(nombre, formato):
    """Deja el nombre de archivo seguro: sin extension repetida y solo con
    letras, numeros, guion y guion bajo."""
    nombre = nombre.strip()
    if nombre.lower().endswith("." + formato):
        nombre = nombre[:-(len(formato) + 1)]
    limpio = ""
    for caracter in nombre:
        if caracter.isalnum() or caracter in "-_":
            limpio += caracter
        else:
            limpio += "_"
    if limpio == "":
        limpio = "resultado"
    return limpio


def guardar_resultado(nombre, formato, datos):
    """Guarda `datos` en resultados/<nombre>.<formato> (csv o json).
    Si el archivo ya existe, se reemplaza. Devuelve la ruta escrita."""
    if not os.path.exists(CARPETA_RESULTADOS):
        os.makedirs(CARPETA_RESULTADOS)
    nombre = limpiar_nombre(nombre, formato)
    ruta = os.path.join(CARPETA_RESULTADOS, nombre + "." + formato)
    if formato == "json":
        guardar_json(ruta, datos)
    else:
        guardar_csv(ruta, a_filas(datos))
    return ruta


def listar_resultados():

    if not os.path.exists(CARPETA_RESULTADOS):
        return []
    nombres = []
    for nombre in os.listdir(CARPETA_RESULTADOS):
        if nombre.endswith(".csv") or nombre.endswith(".json"):
            nombres.append(nombre)
    nombres.sort()
    return nombres


def cargar_resultado(nombre_archivo):
  
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    if nombre_archivo.endswith(".json"):
        return cargar_json(ruta)
    return cargar_csv(ruta)



def guardar_resumen(resumen):
    guardar_json(ARCHIVO_RESUMEN, resumen)


def cargar_resumen():
    return cargar_json(ARCHIVO_RESUMEN)



def registrar_consulta(descripcion, cantidad):

    existe = os.path.exists(ARCHIVO_HISTORIAL)
    archivo = open(ARCHIVO_HISTORIAL, "a", encoding="utf-8", newline="")
    escritor = csv.writer(archivo)
    if not existe:
        escritor.writerow(["fecha", "consulta", "resultados"])
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    escritor.writerow([fecha, descripcion, cantidad])
    archivo.close()


def leer_historial():

    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []
    archivo = open(ARCHIVO_HISTORIAL, encoding="utf-8", newline="")
    lector = csv.reader(archivo)
    next(lector, None)          # saltar el encabezado
    entradas = []
    for fila in lector:
        if len(fila) == 3:
            entradas.append(fila)
    archivo.close()
    return entradas
