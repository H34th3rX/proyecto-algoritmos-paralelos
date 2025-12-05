import threading
import time
from algoritmos import AlgoritmoOrdenamiento, AlgoritmoBusqueda, EjecutorAlgoritmo
from utils import obtener_uso_memoria


class CarreraAlgoritmos:
    # === GESTIÓN DE CARRERA DE ALGORITMOS PARALELOS ===
    
    def __init__(self, arreglo, callback_progreso=None, callback_completo=None, callback_progreso_tiempo_real=None):
        self.arreglo = arreglo
        self.callback_progreso = callback_progreso
        self.callback_completo = callback_completo
        self.callback_progreso_tiempo_real = callback_progreso_tiempo_real
        self.ejecutores = []
        self.resultados = {}
        self.memoria_inicial = 0
        self.memoria_final = 0
        self.en_ejecucion = False
    
    def preparar_carrera(self, incluir_busqueda=False, objetivo_busqueda=None, solo_busqueda=False):
        # === PREPARACIÓN DE ALGORITMOS PARA EJECUCIÓN ===
        algoritmos = []
        
        if solo_busqueda:
            if objetivo_busqueda is not None:
                # === ARREGLO ORDENADO PARA BÚSQUEDA BINARIA ===
                arr_ordenado = sorted(self.arreglo.copy())
                
                def busqueda_sec_wrapper(arr):
                    # Búsqueda secuencial en arreglo ordenado
                    return AlgoritmoBusqueda.busqueda_secuencial(arr_ordenado, objetivo_busqueda)
                
                def busqueda_bin_wrapper(arr):
                    # Búsqueda binaria en arreglo ordenado
                    return AlgoritmoBusqueda.busqueda_binaria(arr_ordenado, objetivo_busqueda)
                
                algoritmos = [
                    ("Búsqueda Secuencial", busqueda_sec_wrapper),
                    ("Búsqueda Binaria", busqueda_bin_wrapper),
                ]
        else:
            algoritmos = [
                ("Burbuja", AlgoritmoOrdenamiento.burbuja),
                ("QuickSort", AlgoritmoOrdenamiento.quicksort),
                ("Inserción", AlgoritmoOrdenamiento.insercion),
            ]
            
            if incluir_busqueda and objetivo_busqueda is not None:
                arr_ordenado = sorted(self.arreglo.copy())
                
                def busqueda_sec_wrapper(arr):
                    return AlgoritmoBusqueda.busqueda_secuencial(arr_ordenado, objetivo_busqueda)
                
                def busqueda_bin_wrapper(arr):
                    return AlgoritmoBusqueda.busqueda_binaria(arr_ordenado, objetivo_busqueda)
                
                algoritmos.extend([
                    ("Búsqueda Secuencial", busqueda_sec_wrapper),
                    ("Búsqueda Binaria", busqueda_bin_wrapper),
                ])
        
        self.ejecutores = []
        for nombre, funcion in algoritmos:
            ejecutor = EjecutorAlgoritmo(
                nombre=nombre,
                funcion=funcion,
                arr=self.arreglo,
                callback=self._on_algoritmo_completo,
                callback_progreso=self._on_progreso_tiempo_real
            )
            self.ejecutores.append(ejecutor)
    
    def iniciar_carrera(self):
        # === INICIO DE EJECUCIÓN PARALELA ===
        if self.en_ejecucion:
            return
        
        self.en_ejecucion = True
        self.resultados = {}
        self.memoria_inicial = obtener_uso_memoria()
        
        for ejecutor in self.ejecutores:
            ejecutor.ejecutar()
        
        monitor = threading.Thread(target=self._monitorear_carrera)
        monitor.start()
    
    def _on_algoritmo_completo(self, nombre, tiempo):
        # === REGISTRO DE RESULTADO INDIVIDUAL ===
        self.resultados[nombre] = tiempo
        
        if self.callback_progreso:
            self.callback_progreso(nombre, tiempo, len(self.resultados))
    
    def _on_progreso_tiempo_real(self, nombre, progreso):
        if self.callback_progreso_tiempo_real:
            self.callback_progreso_tiempo_real(nombre, progreso)
    
    def _monitorear_carrera(self):
        # === MONITOREO DE FINALIZACIÓN Y CÁLCULO DE RESULTADOS ===
        for ejecutor in self.ejecutores:
            ejecutor.esperar()
        
        self.memoria_final = obtener_uso_memoria()
        self.en_ejecucion = False
        
        resultados_ordenados = sorted(
            self.resultados.items(),
            key=lambda x: x[1]
        )
        
        if self.callback_completo:
            self.callback_completo(
                resultados_ordenados,
                self.memoria_final - self.memoria_inicial
            )
    
    def obtener_ganador(self):
        # === OBTENCIÓN DEL ALGORITMO MÁS RÁPIDO ===
        if not self.resultados:
            return None
        
        return min(self.resultados.items(), key=lambda x: x[1])
    
    def obtener_clasificacion(self):
        # === OBTENCIÓN DE CLASIFICACIÓN COMPLETA ===
        return sorted(self.resultados.items(), key=lambda x: x[1])