"""
archivos.py - Entrega 2 (Analizador)
Todo lo que lee o escribe archivos (CSV y JSON) vive aqui.
Aqui NO se hace analisis de datos: eso esta en analisis.py.
"""
import csv
import json
import os
from datetime import datetime

# Carpeta donde esta este archivo. Asi el programa funciona sin importar
# desde que carpeta se ejecute.
CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(CARPETA, "resultados")
ARCHIVO_HISTORIAL = os.path.join(CARPETA, "historial.csv")
ARCHIVO_RESUMEN = os.path.join(CARPETA, "resumen.json")


# ----------------------------------------------------------------------
# Conversion y carga del dataset
# ----------------------------------------------------------------------

def existe_archivo(nombre):
    """True si el archivo existe dentro de la carpeta del proyecto."""
    return os.path.exists(os.path.join(CARPETA, nombre))


def convertir_valor(texto):
    """Convierte un texto a int o float si representa un numero.
    Si no, lo devuelve como texto sin espacios sobrantes."""
    limpio = texto.strip()
    sin_signo = limpio[1:] if limpio.startswith("-") else limpio
    if sin_signo.isdigit():
        return int(limpio)
    if sin_signo.replace(".", "", 1).isdigit():
        return float(limpio)
    return limpio


def cargar_dataset(nombre_archivo):
    """Lee el CSV del dataset con csv.reader.
    Devuelve (encabezados, registros):
      - encabezados: lista con los nombres de las columnas.
      - registros: LISTA DE DICCIONARIOS, uno por fila, para acceder a
        cada dato por el nombre de su columna (registro["Team"])."""
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


# ----------------------------------------------------------------------
# CSV y JSON genericos
# ----------------------------------------------------------------------

def guardar_csv(ruta, filas):
    """Escribe una lista de diccionarios en un CSV (con encabezado)."""
    archivo = open(ruta, "w", encoding="utf-8", newline="")
    escritor = csv.writer(archivo)
    if len(filas) > 0:
        columnas = list(filas[0].keys())
        escritor.writerow(columnas)
        for fila in filas:
            escritor.writerow([fila[c] for c in columnas])
    archivo.close()


def cargar_csv(ruta):
    """Lee un CSV escrito por guardar_csv y devuelve una lista de diccionarios."""
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
    """Escribe cualquier lista o diccionario en un archivo JSON."""
    archivo = open(ruta, "w", encoding="utf-8")
    json.dump(datos, archivo, indent=2, ensure_ascii=False)
    archivo.close()


def cargar_json(ruta):
    """Lee un archivo JSON y devuelve la lista o diccionario que contiene."""
    archivo = open(ruta, encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()
    return datos


# ----------------------------------------------------------------------
# Resultados guardados (Funcionalidad obligatoria 1)
# ----------------------------------------------------------------------

def a_filas(datos):
    """Convierte un resultado a lista de diccionarios para poder escribirlo
    como CSV. Una lista ya esta lista; un diccionario se vuelve una tabla
    de dos columnas (campo, valor)."""
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
    """Devuelve la lista (ordenada) de archivos guardados en resultados/."""
    if not os.path.exists(CARPETA_RESULTADOS):
        return []
    nombres = []
    for nombre in os.listdir(CARPETA_RESULTADOS):
        if nombre.endswith(".csv") or nombre.endswith(".json"):
            nombres.append(nombre)
    nombres.sort()
    return nombres


def cargar_resultado(nombre_archivo):
    """Carga un resultado guardado antes, sin reprocesar el dataset."""
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    if nombre_archivo.endswith(".json"):
        return cargar_json(ruta)
    return cargar_csv(ruta)


# ----------------------------------------------------------------------
# Resumen del dataset (opcional)
# ----------------------------------------------------------------------

def guardar_resumen(resumen):
    guardar_json(ARCHIVO_RESUMEN, resumen)


def cargar_resumen():
    return cargar_json(ARCHIVO_RESUMEN)


# ----------------------------------------------------------------------
# Historial de consultas (Funcionalidad obligatoria 2)
# ----------------------------------------------------------------------

def registrar_consulta(descripcion, cantidad):
    """Agrega una linea al historial.csv: fecha y hora, consulta y cantidad
    de resultados. Crea el archivo (con encabezado) si todavia no existe."""
    existe = os.path.exists(ARCHIVO_HISTORIAL)
    archivo = open(ARCHIVO_HISTORIAL, "a", encoding="utf-8", newline="")
    escritor = csv.writer(archivo)
    if not existe:
        escritor.writerow(["fecha", "consulta", "resultados"])
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    escritor.writerow([fecha, descripcion, cantidad])
    archivo.close()


def leer_historial():
    """Devuelve el historial como lista de listas [fecha, consulta, resultados]
    (sin la fila de encabezado). Si no hay historial, devuelve []."""
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
