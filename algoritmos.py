"""
Algoritmos de Búsqueda y Ordenamiento
Proyecto Final - Algoritmos Paralelos
"""

import time
import threading

class AlgoritmoBusqueda:
    """Clase base para algoritmos de búsqueda"""
    
    @staticmethod
    def busqueda_secuencial(arr, objetivo):
        """
        Búsqueda Secuencial
        
        PSEUDOCÓDIGO:
        1. Para cada elemento en el arreglo:
        2.   Si elemento == objetivo:
        3.     Retornar índice
        4. Retornar -1 (no encontrado)
        
        Complejidad: O(n)
        """
        for i in range(len(arr)):
            if arr[i] == objetivo:
                return i
        return -1
    
    @staticmethod
    def busqueda_binaria(arr, objetivo):
        """
        Búsqueda Binaria (requiere arreglo ordenado)
        
        PSEUDOCÓDIGO:
        1. inicio = 0, fin = tamaño - 1
        2. Mientras inicio <= fin:
        3.   medio = (inicio + fin) / 2
        4.   Si arr[medio] == objetivo:
        5.     Retornar medio
        6.   Si arr[medio] < objetivo:
        7.     inicio = medio + 1
        8.   Sino:
        9.     fin = medio - 1
        10. Retornar -1 (no encontrado)
        
        Complejidad: O(log n)
        """
        arr_ordenado = sorted(arr)  # Necesita estar ordenado
        inicio = 0
        fin = len(arr_ordenado) - 1
        
        while inicio <= fin:
            medio = (inicio + fin) // 2
            if arr_ordenado[medio] == objetivo:
                return medio
            elif arr_ordenado[medio] < objetivo:
                inicio = medio + 1
            else:
                fin = medio - 1
        return -1


class AlgoritmoOrdenamiento:
    """Clase base para algoritmos de ordenamiento"""
    
    @staticmethod
    def burbuja(arr):
        """
        Algoritmo de Ordenamiento de la Burbuja (Bubble Sort)
        
        PSEUDOCÓDIGO:
        1. Para i desde 0 hasta n-1:
        2.   Para j desde 0 hasta n-i-1:
        3.     Si arr[j] > arr[j+1]:
        4.       Intercambiar arr[j] y arr[j+1]
        
        Complejidad: O(n²)
        """
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr_copy[j] > arr_copy[j + 1]:
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
        
        return arr_copy
    
    @staticmethod
    def quicksort(arr):
        """
        Quick Sort
        
        PSEUDOCÓDIGO:
        1. Si el arreglo tiene 0 o 1 elemento:
        2.   Retornar el arreglo
        3. Seleccionar un pivote (último elemento)
        4. Particionar el arreglo:
        5.   menores = elementos < pivote
        6.   iguales = elementos == pivote
        7.   mayores = elementos > pivote
        8. Retornar quicksort(menores) + iguales + quicksort(mayores)
        
        Complejidad: O(n log n) promedio, O(n²) peor caso
        """
        arr_copy = arr.copy()
        
        if len(arr_copy) <= 1:
            return arr_copy
        
        pivote = arr_copy[-1]
        menores = [x for x in arr_copy[:-1] if x < pivote]
        iguales = [x for x in arr_copy if x == pivote]
        mayores = [x for x in arr_copy[:-1] if x > pivote]
        
        return AlgoritmoOrdenamiento.quicksort(menores) + iguales + AlgoritmoOrdenamiento.quicksort(mayores)
    
    @staticmethod
    def insercion(arr):
        """
        Método de Inserción (Insertion Sort)
        
        PSEUDOCÓDIGO:
        1. Para i desde 1 hasta n:
        2.   clave = arr[i]
        3.   j = i - 1
        4.   Mientras j >= 0 y arr[j] > clave:
        5.     arr[j+1] = arr[j]
        6.     j = j - 1
        7.   arr[j+1] = clave
        
        Complejidad: O(n²)
        """
        arr_copy = arr.copy()
        
        for i in range(1, len(arr_copy)):
            clave = arr_copy[i]
            j = i - 1
            
            while j >= 0 and arr_copy[j] > clave:
                arr_copy[j + 1] = arr_copy[j]
                j -= 1
            
            arr_copy[j + 1] = clave
        
        return arr_copy


class EjecutorAlgoritmo:
    """Clase para ejecutar algoritmos y medir su rendimiento"""
    
    def __init__(self, nombre, funcion, arr, callback=None, callback_progreso=None):
        self.nombre = nombre
        self.funcion = funcion
        self.arr = arr
        self.callback = callback
        self.callback_progreso = callback_progreso
        self.tiempo = 0
        self.resultado = None
        self.thread = None
        self.completado = False
        self.progreso_actual = 0
    
    def ejecutar(self):
        """Ejecuta el algoritmo en un thread separado"""
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
    
    def _run(self):
        """Método interno para ejecutar y medir tiempo"""
        inicio = time.perf_counter()
        
        # Ejecutar el algoritmo SIN seguimiento de progreso para no afectar tiempos
        self.resultado = self.funcion(self.arr)
        
        fin = time.perf_counter()
        self.tiempo = fin - inicio
        self.completado = True
        self.progreso_actual = 100
        
        # Llamar al callback si existe
        if self.callback:
            self.callback(self.nombre, self.tiempo)
    
    def _reportar_progreso(self, progreso):
        """Reporta el progreso actual (DESHABILITADO para no afectar tiempos)"""
        # Ya no se usa - los tiempos deben ser puros
        pass
    
    def _burbuja_con_progreso(self, arr):
        """Burbuja con reporte de progreso"""
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        for i in range(n):
            # Reportar progreso cada 5% para no saturar
            if i % (n // 20) == 0:
                progreso = (i / n) * 100
                self._reportar_progreso(progreso)
            
            for j in range(0, n - i - 1):
                if arr_copy[j] > arr_copy[j + 1]:
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
        
        return arr_copy
    
    def _quicksort_con_progreso(self, arr):
        """QuickSort con reporte de progreso aproximado"""
        arr_copy = arr.copy()
        self.qs_total = len(arr_copy)
        self.qs_procesados = 0
        self.qs_ultimo_reporte = 0
        
        def quicksort_recursivo(sub_arr):
            if len(sub_arr) <= 1:
                self.qs_procesados += len(sub_arr)
                # Solo reportar cada 5%
                if self.qs_procesados - self.qs_ultimo_reporte > self.qs_total * 0.05:
                    progreso = (self.qs_procesados / self.qs_total) * 100
                    self._reportar_progreso(progreso)
                    self.qs_ultimo_reporte = self.qs_procesados
                return sub_arr
            
            pivote = sub_arr[-1]
            menores = [x for x in sub_arr[:-1] if x < pivote]
            iguales = [x for x in sub_arr if x == pivote]
            mayores = [x for x in sub_arr[:-1] if x > pivote]
            
            self.qs_procesados += len(iguales)
            if self.qs_procesados - self.qs_ultimo_reporte > self.qs_total * 0.05:
                progreso = (self.qs_procesados / self.qs_total) * 100
                self._reportar_progreso(progreso)
                self.qs_ultimo_reporte = self.qs_procesados
            
            return quicksort_recursivo(menores) + iguales + quicksort_recursivo(mayores)
        
        return quicksort_recursivo(arr_copy)
    
    def _insercion_con_progreso(self, arr):
        """Inserción con reporte de progreso"""
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        for i in range(1, n):
            # Reportar progreso cada 5%
            if i % (n // 20) == 0:
                progreso = (i / n) * 100
                self._reportar_progreso(progreso)
            
            clave = arr_copy[i]
            j = i - 1
            
            while j >= 0 and arr_copy[j] > clave:
                arr_copy[j + 1] = arr_copy[j]
                j -= 1
            
            arr_copy[j + 1] = clave
        
        return arr_copy
    
    def _busqueda_secuencial_con_progreso(self, arr):
        """Búsqueda secuencial con progreso"""
        objetivo = self.funcion(arr)  # Obtener el objetivo de la función original
        n = len(arr)
        
        for i in range(n):
            if i % 100 == 0:  # Reportar cada 100 elementos
                progreso = (i / n) * 100
                self._reportar_progreso(progreso)
            
            if arr[i] == objetivo:
                self._reportar_progreso(100)
                return i
        
        return -1
    
    def _busqueda_binaria_con_progreso(self, arr):
        """Búsqueda binaria con progreso"""
        objetivo = self.funcion(arr)  # Obtener el objetivo
        arr_ordenado = sorted(arr)
        inicio = 0
        fin = len(arr_ordenado) - 1
        iteraciones = 0
        max_iteraciones = 20  # log2(10000) ≈ 13
        
        while inicio <= fin:
            iteraciones += 1
            progreso = (iteraciones / max_iteraciones) * 100
            self._reportar_progreso(min(progreso, 95))
            
            medio = (inicio + fin) // 2
            if arr_ordenado[medio] == objetivo:
                self._reportar_progreso(100)
                return medio
            elif arr_ordenado[medio] < objetivo:
                inicio = medio + 1
            else:
                fin = medio - 1
        
        return -1
    
    def esperar(self):
        """Espera a que el thread termine"""
        if self.thread:
            self.thread.join()