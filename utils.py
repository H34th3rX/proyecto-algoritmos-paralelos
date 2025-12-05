import psutil
import os
import random

def generar_arreglo(tamanio=10000, min_val=1, max_val=100000):
    # === GENERACIÓN DE ARREGLO ALEATORIO ===
    return [random.randint(min_val, max_val) for _ in range(tamanio)]


def obtener_uso_memoria():
    # === MEDICIÓN DE CONSUMO DE MEMORIA ===
    proceso = psutil.Process(os.getpid())
    memoria = proceso.memory_info().rss / 1024 / 1024
    return memoria


def formatear_tiempo(segundos):
    # === FORMATEO DE TIEMPO PARA LECTURA HUMANA ===
    if segundos < 0.001:
        return f"{segundos * 1000000:.2f} µs"
    elif segundos < 1:
        return f"{segundos * 1000:.2f} ms"
    else:
        return f"{segundos:.2f} s"


def formatear_memoria(mb):
    # === FORMATEO DE MEMORIA PARA LECTURA HUMANA ===
    if mb < 1:
        return f"{mb * 1024:.2f} KB"
    elif mb < 1024:
        return f"{mb:.2f} MB"
    else:
        return f"{mb / 1024:.2f} GB"