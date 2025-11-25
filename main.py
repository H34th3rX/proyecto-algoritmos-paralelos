"""
Aplicación Principal - Carrera de Algoritmos Paralelos
Interfaz Gráfica Moderna con Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Scrollbar
import threading
import time
from carrera import CarreraAlgoritmos
from utils import generar_arreglo, formatear_tiempo, formatear_memoria

# Colores modernos (Tema oscuro)
COLOR_BG = "#1a1a2e"
COLOR_PANEL = "#16213e"
COLOR_ACCENT = "#0f3460"
COLOR_PRIMARY = "#e94560"
COLOR_SUCCESS = "#00d9ff"
COLOR_WARNING = "#f39c12"
COLOR_TEXT = "#eaeaea"
COLOR_TEXT_DIM = "#94a1b2"

# Colores para cada algoritmo
COLORES_ALGORITMOS = {
    "Burbuja": "#e74c3c",
    "QuickSort": "#3498db",
    "Inserción": "#2ecc71",
    "Búsqueda Secuencial": "#9b59b6",
    "Búsqueda Binaria": "#f39c12",
}


class BarraProgreso(tk.Canvas):
    """Barra de progreso personalizada y animada"""
    
    def __init__(self, parent, nombre, color, **kwargs):
        super().__init__(parent, bg=COLOR_PANEL, highlightthickness=0, **kwargs)
        self.nombre = nombre
        self.color = color
        self.progreso = 0
        self.tiempo = 0
        self.completado = False
        
        self.width = kwargs.get('width', 400)
        self.height = kwargs.get('height', 60)
        
        self.dibujar()
    
    def dibujar(self):
        """Dibuja la barra de progreso"""
        self.delete("all")
        
        # Fondo de la barra
        self.create_rectangle(
            10, 20, self.width - 10, self.height - 10,
            fill=COLOR_ACCENT, outline=""
        )
        
        # Barra de progreso
        if self.progreso > 0:
            ancho_progreso = (self.width - 20) * (self.progreso / 100)
            self.create_rectangle(
                10, 20, 10 + ancho_progreso, self.height - 10,
                fill=self.color, outline=""
            )
        
        # Texto del nombre
        self.create_text(
            20, 15,
            text=self.nombre,
            fill=COLOR_TEXT,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        )
        
        # Texto del tiempo
        if self.completado:
            tiempo_texto = f"✓ {formatear_tiempo(self.tiempo)}"
            color_texto = COLOR_SUCCESS
        elif self.progreso > 0:
            tiempo_texto = f"Procesando... {self.progreso:.0f}%"
            color_texto = COLOR_WARNING
        else:
            tiempo_texto = "Esperando..."
            color_texto = COLOR_TEXT_DIM
        
        self.create_text(
            self.width - 20, self.height // 2 + 5,
            text=tiempo_texto,
            fill=color_texto,
            font=("Consolas", 9, "bold"),
            anchor="e"
        )
    
    def actualizar(self, progreso=None, tiempo=None, completado=False):
        """Actualiza la barra de progreso"""
        if progreso is not None:
            self.progreso = min(progreso, 100)
        if tiempo is not None:
            self.tiempo = tiempo
        self.completado = completado
        self.dibujar()
    
    def reset(self):
        """Reinicia la barra"""
        self.progreso = 0
        self.tiempo = 0
        self.completado = False
        self.dibujar()


class AplicacionCarrera(tk.Tk):
    """Aplicación principal"""
    
    def __init__(self):
        super().__init__()
        
        self.title("🏁 Carrera de Algoritmos Paralelos")
        self.geometry("900x850")
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)  # Permitir redimensionar
        
        # Variables
        self.arreglo = []
        self.carrera = None
        self.barras = {}
        self.tiempo_inicio = 0
        self.incluir_busqueda = tk.BooleanVar(value=True)
        self.objetivo_busqueda = None
        
        self.crear_interfaz()
        self.generar_nuevo_arreglo()
    
    def crear_interfaz(self):
        """Crea toda la interfaz gráfica"""
        
        # ===== HEADER =====
        header = tk.Frame(self, bg=COLOR_PANEL, height=100)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        titulo = tk.Label(
            header,
            text="🏁 CARRERA DE ALGORITMOS",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_PRIMARY
        )
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(
            header,
            text="Simulación de Algoritmos Paralelos en Tiempo Real",
            font=("Segoe UI", 11),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_DIM
        )
        subtitulo.pack()
        
        # ===== PANEL DE INFO =====
        info_frame = tk.Frame(self, bg=COLOR_BG)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.label_tamanio = self.crear_info_box(
            info_frame, "📊 Tamaño del Arreglo", "10,000 elementos"
        )
        self.label_tamanio.pack(side="left", padx=10)
        
        self.label_estado = self.crear_info_box(
            info_frame, "⚡ Estado", "Listo para iniciar"
        )
        self.label_estado.pack(side="left", padx=10)
        
        self.label_memoria = self.crear_info_box(
            info_frame, "💾 Memoria", "0 MB"
        )
        self.label_memoria.pack(side="left", padx=10)
        
        # ===== PANEL DE CARRERAS =====
        carrera_frame = tk.Frame(self, bg=COLOR_PANEL)
        carrera_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        titulo_carrera = tk.Label(
            carrera_frame,
            text="🏃 COMPETIDORES",
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT
        )
        titulo_carrera.pack(pady=15)
        
        # Checkbox para incluir búsquedas
        check_busqueda = tk.Checkbutton(
            carrera_frame,
            text="Incluir algoritmos de búsqueda",
            variable=self.incluir_busqueda,
            command=self.actualizar_barras,
            font=("Segoe UI", 10),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            selectcolor=COLOR_ACCENT,
            activebackground=COLOR_PANEL,
            activeforeground=COLOR_TEXT
        )
        check_busqueda.pack(pady=5)
        
        # Frame para las barras
        self.barras_container = tk.Frame(carrera_frame, bg=COLOR_PANEL)
        self.barras_container.pack(pady=10)
        
        # Crear barras inicialmente
        self.actualizar_barras()
        
        # ===== PANEL DE GANADOR =====
        self.ganador_frame = tk.Frame(self, bg=COLOR_ACCENT, height=80)
        self.ganador_frame.pack(fill="x", padx=20, pady=10)
        self.ganador_frame.pack_propagate(False)
        
        self.label_ganador = tk.Label(
            self.ganador_frame,
            text="🏆 Esperando resultados...",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT
        )
        self.label_ganador.pack(expand=True)
        
        # ===== BOTONES =====
        botones_frame = tk.Frame(self, bg=COLOR_BG)
        botones_frame.pack(pady=20)
        
        self.btn_iniciar = self.crear_boton(
            botones_frame,
            text="▶ INICIAR CARRERA",
            command=self.iniciar_carrera,
            bg=COLOR_SUCCESS,
            width=20
        )
        self.btn_iniciar.pack(side="left", padx=10)
        
        self.btn_nuevo = self.crear_boton(
            botones_frame,
            text="🔄 NUEVO ARREGLO",
            command=self.generar_nuevo_arreglo,
            bg=COLOR_WARNING,
            width=20
        )
        self.btn_nuevo.pack(side="left", padx=10)
    
    def crear_info_box(self, parent, titulo, valor):
        """Crea un box de información"""
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        
        lbl_titulo = tk.Label(
            frame,
            text=titulo,
            font=("Segoe UI", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_DIM
        )
        lbl_titulo.pack(pady=(10, 0))
        
        lbl_valor = tk.Label(
            frame,
            text=valor,
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT
        )
        lbl_valor.pack(pady=(0, 10), padx=20)
        
        return lbl_valor
    
    def crear_boton(self, parent, text, command, bg, width=15):
        """Crea un botón estilizado"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=width,
            height=2
        )
        return btn
    
    def actualizar_barras(self):
        """Actualiza las barras según si se incluyen búsquedas o no"""
        # Limpiar barras existentes
        for widget in self.barras_container.winfo_children():
            widget.destroy()
        self.barras.clear()
        
        # Determinar qué algoritmos mostrar
        algoritmos_mostrar = ["Burbuja", "QuickSort", "Inserción"]
        if self.incluir_busqueda.get():
            algoritmos_mostrar.extend(["Búsqueda Secuencial", "Búsqueda Binaria"])
        
        # Crear barras
        for nombre in algoritmos_mostrar:
            color = COLORES_ALGORITMOS[nombre]
            barra = BarraProgreso(
                self.barras_container,
                nombre=nombre,
                color=color,
                width=800,
                height=60  # Reducido de 70 a 60
            )
            barra.pack(pady=8, padx=30)  # Reducido padding
            self.barras[nombre] = barra
    
    def generar_nuevo_arreglo(self):
        """Genera un nuevo arreglo aleatorio"""
        self.arreglo = generar_arreglo(10000)
        # Seleccionar un número aleatorio del arreglo para buscar
        self.objetivo_busqueda = self.arreglo[len(self.arreglo) // 2]
        
        self.label_estado.config(text="Nuevo arreglo generado")
        self.label_ganador.config(text="🏆 Esperando resultados...")
        
        # Resetear barras
        for barra in self.barras.values():
            barra.reset()
    
    def iniciar_carrera(self):
        """Inicia la carrera de algoritmos"""
        if not self.arreglo:
            messagebox.showwarning("Advertencia", "Genera un arreglo primero")
            return
        
        # Deshabilitar botón
        self.btn_iniciar.config(state="disabled")
        self.label_estado.config(text="⚡ EN CARRERA...")
        self.label_ganador.config(text="🏁 Carrera en progreso...")
        
        # Resetear barras
        for barra in self.barras.values():
            barra.reset()
        
        # Crear y iniciar carrera
        self.carrera = CarreraAlgoritmos(
            self.arreglo,
            callback_progreso=self.on_progreso,
            callback_completo=self.on_completo,
            callback_progreso_tiempo_real=self.on_progreso_tiempo_real
        )
        self.carrera.preparar_carrera(
            incluir_busqueda=self.incluir_busqueda.get(),
            objetivo_busqueda=self.objetivo_busqueda
        )
        self.tiempo_inicio = time.time()
        
        # Iniciar carrera
        self.carrera.iniciar_carrera()
    
    def on_progreso_tiempo_real(self, nombre, progreso):
        """Callback para actualizar progreso en tiempo real"""
        def update():
            if nombre in self.barras:
                self.barras[nombre].actualizar(progreso=progreso)
        
        self.after(0, update)
    
    def on_progreso(self, nombre, tiempo, completados):
        """Callback cuando un algoritmo termina"""
        def update():
            self.barras[nombre].actualizar(progreso=100, tiempo=tiempo, completado=True)
        
        self.after(0, update)
    
    def on_completo(self, resultados, memoria_consumida):
        """Callback cuando todos los algoritmos terminan"""
        def update():
            # Habilitar botón
            self.btn_iniciar.config(state="normal")
            self.label_estado.config(text="✅ Carrera completada")
            self.label_memoria.config(text=formatear_memoria(memoria_consumida))
            
            # Mostrar ganador
            if resultados:
                ganador, tiempo = resultados[0]
                self.label_ganador.config(
                    text=f"🏆 GANADOR: {ganador} - {formatear_tiempo(tiempo)}",
                    fg=COLOR_SUCCESS
                )
                
                # Mostrar clasificación completa
                mensaje = "📊 CLASIFICACIÓN FINAL:\n\n"
                for i, (nombre, tiempo) in enumerate(resultados, 1):
                    medalla = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
                    mensaje += f"{medalla} {nombre}: {formatear_tiempo(tiempo)}\n"
                
                mensaje += f"\n💾 Memoria consumida: {formatear_memoria(memoria_consumida)}"
                
                messagebox.showinfo("Resultados Finales", mensaje)
        
        self.after(0, update)


if __name__ == "__main__":
    app = AplicacionCarrera()
    app.mainloop()