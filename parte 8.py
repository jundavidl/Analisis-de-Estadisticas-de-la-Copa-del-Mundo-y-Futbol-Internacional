
CAMPOS_SIN_PROMEDIO = ["Year"]




def campos_numericos(registros):

    numericos = []
    for campo in registros[0]:
        es_numerico = True
        for registro in registros:
            if isinstance(registro[campo], str):
                es_numerico = False
                break
        if es_numerico:
            numericos.append(campo)
    return numericos


def campos_texto(registros):
    """Lista de campos que no son numericos."""
    numericos = campos_numericos(registros)
    textos = []
    for campo in registros[0]:
        if campo not in numericos:
            textos.append(campo)
    return textos


def valores_unicos(registros, campo):
    
    unicos = set()
    for registro in registros:
        unicos.add(registro[campo])
    return unicos



def buscar(registros, termino):
   
    termino = termino.lower().strip()
    encontrados = []
    for registro in registros:
        for valor in registro.values():
            if termino in str(valor).lower():
                encontrados.append(registro)
                break
    return encontrados


def filtrar_mayor_que(registros, campo, limite):
    
    resultado = []
    for registro in registros:
        if registro[campo] > limite:
            resultado.append(registro)
    return resultado


def filtrar_igual(registros, campo, valor):
    
    valor = str(valor).lower().strip()
    resultado = []
    for registro in registros:
        if str(registro[campo]).lower() == valor:
            resultado.append(registro)
    return resultado



def calcular_estadisticas(registros, campo):
    
    maximo = registros[0][campo]
    minimo = registros[0][campo]
    suma = 0
    cantidad = 0
    for registro in registros:
        valor = registro[campo]
        if valor > maximo:
            maximo = valor
        if valor < minimo:
            minimo = valor
        suma += valor
        cantidad += 1
    return {
        "campo": campo,
        "maximo": maximo,
        "minimo": minimo,
        "promedio": round(suma / cantidad, 2),
        "registros": cantidad,
    }


def segundo_elemento(par):
  
    return par[1]


def agrupar_por_categoria(registros, campo):
 
    conteo = {}
    for registro in registros:
        valor = registro[campo]
        conteo[valor] = conteo.get(valor, 0) + 1

    pares = list(conteo.items())
    pares.sort(key=segundo_elemento, reverse=True)

    resultado = []
    for valor, cantidad in pares:
        resultado.append({"valor": valor, "cantidad": cantidad})
    return resultado


def comparar_grupos(registros, campo, valor_a, valor_b):
    
    numericos = campos_numericos(registros)
    comparacion = []
    for valor in [valor_a, valor_b]:
        grupo = filtrar_igual(registros, campo, valor)
        fila = {"grupo": valor.strip(), "registros": len(grupo)}
        if len(grupo) > 0:
            fila["grupo"] = grupo[0][campo]   # nombre tal como esta en el dataset
            for c in numericos:
                if c not in CAMPOS_SIN_PROMEDIO:
                    fila[c] = calcular_estadisticas(grupo, c)["promedio"]
        comparacion.append(fila)
    return comparacion



def generar_resumen(registros):
   
    resumen = {
        "total": len(registros),
        "mundiales": len(valores_unicos(registros, "Year")),
    }

    unicos = {}
    for campo in campos_texto(registros):
        unicos[campo] = len(valores_unicos(registros, campo))
    resumen["valores_unicos"] = unicos

    extremos = {}
    for campo in campos_numericos(registros):
        stats = calcular_estadisticas(registros, campo)
        extremos[campo] = {"maximo": stats["maximo"], "minimo": stats["minimo"]}
    resumen["campos_numericos"] = extremos
    return resumen
