import time
import threading

class AlgoritmoBusqueda:
    # === ALGORITMOS DE BÚSQUEDA ===
    
    @staticmethod
    def busqueda_secuencial(arr, objetivo):
        # === BÚSQUEDA SECUENCIAL IMPLEMENTACIÓN ===
        for i in range(len(arr)):
            if arr[i] == objetivo:
                return i
        return -1
    
    @staticmethod
    def busqueda_binaria(arr, objetivo):
        # === BÚSQUEDA BINARIA IMPLEMENTACIÓN ===
        arr_ordenado = sorted(arr)
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
    # === ALGORITMOS DE ORDENAMIENTO ===
    
    @staticmethod
    def burbuja(arr):
        # === BUBBLE SORT IMPLEMENTACIÓN ===
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr_copy[j] > arr_copy[j + 1]:
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
        
        return arr_copy
    
    @staticmethod
    def quicksort(arr):
        # === QUICKSORT IMPLEMENTACIÓN ===
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
        # === INSERTION SORT IMPLEMENTACIÓN ===
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
    # === EJECUTOR CON MEDICIÓN DE TIEMPO ===
    
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
        # === EJECUCIÓN EN HILO SEPARADO ===
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
    
    def _run(self):
        # === MEDICIÓN PRECISA DE TIEMPO DE EJECUCIÓN ===
        inicio = time.perf_counter()
        self.resultado = self.funcion(self.arr)
        fin = time.perf_counter()
        self.tiempo = fin - inicio
        self.completado = True
        self.progreso_actual = 100
        
        if self.callback:
            self.callback(self.nombre, self.tiempo)
    
    def _reportar_progreso(self, progreso):
        pass
    
    def esperar(self):
        # === ESPERA DE FINALIZACIÓN DEL HILO ===
        if self.thread:
            self.thread.join()