"""
Sistema de Carrera para ejecutar algoritmos en paralelo
"""

import threading
import time
from algoritmos import AlgoritmoOrdenamiento, AlgoritmoBusqueda, EjecutorAlgoritmo
from utils import obtener_uso_memoria


class CarreraAlgoritmos:
    """
    Clase que maneja la ejecución paralela de múltiples algoritmos
    """
    
    def __init__(self, arreglo, callback_progreso=None, callback_completo=None, callback_progreso_tiempo_real=None):
        """
        Args:
            arreglo: El arreglo a procesar
            callback_progreso: Función a llamar cuando un algoritmo termina
            callback_completo: Función a llamar cuando todos terminan
            callback_progreso_tiempo_real: Función para actualizar progreso en tiempo real
        """
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
        """
        Prepara todos los algoritmos para la carrera
        
        Args:
            incluir_busqueda: Si True, incluye algoritmos de búsqueda
            objetivo_busqueda: Número a buscar en el arreglo
            solo_busqueda: Si True, solo ejecuta algoritmos de búsqueda
        """
        algoritmos = []
        
        # Si es solo búsqueda, solo agregar esos
        if solo_busqueda:
            if objetivo_busqueda is not None:
                # Wrapper para búsqueda secuencial
                def busqueda_sec_wrapper(arr):
                    return AlgoritmoBusqueda.busqueda_secuencial(arr, objetivo_busqueda)
                
                # Wrapper para búsqueda binaria
                def busqueda_bin_wrapper(arr):
                    return AlgoritmoBusqueda.busqueda_binaria(arr, objetivo_busqueda)
                
                algoritmos = [
                    ("Búsqueda Secuencial", busqueda_sec_wrapper),
                    ("Búsqueda Binaria", busqueda_bin_wrapper),
                ]
        else:
            # Algoritmos de ordenamiento
            algoritmos = [
                ("Burbuja", AlgoritmoOrdenamiento.burbuja),
                ("QuickSort", AlgoritmoOrdenamiento.quicksort),
                ("Inserción", AlgoritmoOrdenamiento.insercion),
            ]
            
            # Agregar algoritmos de búsqueda si se solicita
            if incluir_busqueda and objetivo_busqueda is not None:
                # Wrapper para búsqueda secuencial
                def busqueda_sec_wrapper(arr):
                    return AlgoritmoBusqueda.busqueda_secuencial(arr, objetivo_busqueda)
                
                # Wrapper para búsqueda binaria
                def busqueda_bin_wrapper(arr):
                    return AlgoritmoBusqueda.busqueda_binaria(arr, objetivo_busqueda)
                
                algoritmos.extend([
                    ("Búsqueda Secuencial", busqueda_sec_wrapper),
                    ("Búsqueda Binaria", busqueda_bin_wrapper),
                ])
        
        # Crear ejecutores para cada algoritmo
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
        """
        Inicia la carrera de algoritmos
        """
        if self.en_ejecucion:
            return
        
        self.en_ejecucion = True
        self.resultados = {}
        self.memoria_inicial = obtener_uso_memoria()
        
        # Iniciar todos los algoritmos al mismo tiempo
        for ejecutor in self.ejecutores:
            ejecutor.ejecutar()
        
        # Thread para monitorear cuando todos terminen
        monitor = threading.Thread(target=self._monitorear_carrera)
        monitor.start()
    
    def _on_algoritmo_completo(self, nombre, tiempo):
        """
        Callback cuando un algoritmo individual termina
        """
        self.resultados[nombre] = tiempo
        
        if self.callback_progreso:
            self.callback_progreso(nombre, tiempo, len(self.resultados))
    
    def _on_progreso_tiempo_real(self, nombre, progreso):
        """
        Callback para progreso en tiempo real
        """
        if self.callback_progreso_tiempo_real:
            self.callback_progreso_tiempo_real(nombre, progreso)
    
    def _monitorear_carrera(self):
        """
        Monitorea cuando todos los algoritmos han terminado
        """
        # Esperar a que todos terminen
        for ejecutor in self.ejecutores:
            ejecutor.esperar()
        
        self.memoria_final = obtener_uso_memoria()
        self.en_ejecucion = False
        
        # Ordenar resultados por tiempo
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
        """
        Retorna el algoritmo más rápido
        """
        if not self.resultados:
            return None
        
        return min(self.resultados.items(), key=lambda x: x[1])
    
    def obtener_clasificacion(self):
        """
        Retorna la clasificación completa ordenada por tiempo
        """
        return sorted(self.resultados.items(), key=lambda x: x[1])