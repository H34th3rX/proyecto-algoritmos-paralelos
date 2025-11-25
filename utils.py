"""
Utilidades para medir rendimiento y memoria
"""

import psutil
import os
import random

def generar_arreglo(tamanio=10000, min_val=1, max_val=100000):
    """
    Genera un arreglo aleatorio de números enteros
    
    Args:
        tamanio: Cantidad de elementos
        min_val: Valor mínimo
        max_val: Valor máximo
    
    Returns:
        Lista de enteros aleatorios
    """
    return [random.randint(min_val, max_val) for _ in range(tamanio)]


def obtener_uso_memoria():
    """
    Obtiene el uso actual de memoria del proceso en MB
    
    Returns:
        float: Memoria usada en MB
    """
    proceso = psutil.Process(os.getpid())
    memoria = proceso.memory_info().rss / 1024 / 1024  # Convertir a MB
    return memoria


def formatear_tiempo(segundos):
    """
    Formatea el tiempo en un formato legible
    
    Args:
        segundos: Tiempo en segundos
    
    Returns:
        str: Tiempo formateado
    """
    if segundos < 0.001:
        return f"{segundos * 1000000:.2f} µs"
    elif segundos < 1:
        return f"{segundos * 1000:.2f} ms"
    else:
        return f"{segundos:.2f} s"


def formatear_memoria(mb):
    """
    Formatea la memoria en un formato legible
    
    Args:
        mb: Memoria en MB
    
    Returns:
        str: Memoria formateada
    """
    if mb < 1:
        return f"{mb * 1024:.2f} KB"
    elif mb < 1024:
        return f"{mb:.2f} MB"
    else:
        return f"{mb / 1024:.2f} GB"