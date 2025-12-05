import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Scrollbar
import threading
import time
import random
from carrera import CarreraAlgoritmos
from utils import generar_arreglo, formatear_tiempo, formatear_memoria

# === CONFIGURACIÓN DE COLORES ===
COLOR_BG = "#1a1a2e"
COLOR_PANEL = "#16213e"
COLOR_ACCENT = "#0f3460"
COLOR_PRIMARY = "#e94560"
COLOR_SUCCESS = "#00d9ff"
COLOR_WARNING = "#f39c12"
COLOR_TEXT = "#eaeaea"
COLOR_TEXT_DIM = "#94a1b2"

# === COLORES POR ALGORITMO ===
COLORES_ALGORITMOS = {
    "Burbuja": "#e74c3c",
    "QuickSort": "#3498db",
    "Inserción": "#2ecc71",
    "Búsqueda Secuencial": "#9b59b6",
    "Búsqueda Binaria": "#f39c12",
}


class BarraProgreso(tk.Canvas):
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
        self.delete("all")
        
        self.create_rectangle(
            10, 20, self.width - 10, self.height - 10,
            fill=COLOR_ACCENT, outline=""
        )
        
        if self.progreso > 0:
            ancho_progreso = (self.width - 20) * (self.progreso / 100)
            self.create_rectangle(
                10, 20, 10 + ancho_progreso, self.height - 10,
                fill=self.color, outline=""
            )
        
        self.create_text(
            20, 15,
            text=self.nombre,
            fill=COLOR_TEXT,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        )
        
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
        if progreso is not None:
            self.progreso = min(progreso, 100)
        if tiempo is not None:
            self.tiempo = tiempo
        self.completado = completado
        self.dibujar()
    
    def reset(self):
        self.progreso = 0
        self.tiempo = 0
        self.completado = False
        self.dibujar()


class AplicacionCarrera(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Carrera de Algoritmos Paralelos")
        self.geometry("1000x850")
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)
        
        # === VARIABLES DE CONTROL ===
        self.arreglo = []
        self.carrera = None
        self.barras = {}
        self.tiempo_inicio = 0
        self.objetivo_busqueda = None
        self.modo_actual = "ordenamiento"
        
        # === INICIALIZACIÓN ===
        self.crear_interfaz()
        self.generar_nuevo_arreglo()
    
    def crear_interfaz(self):
        # === INTERFAZ GRÁFICA ===
        header = tk.Frame(self, bg=COLOR_PANEL, height=100)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        titulo = tk.Label(
            header,
            text="CARRERA DE ALGORITMOS",
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
        
        # === PANEL DE INFORMACIÓN ===
        info_container = tk.Frame(self, bg=COLOR_BG)
        info_container.pack(fill="x", padx=20, pady=10)
        
        info_frame = tk.Frame(info_container, bg=COLOR_BG)
        info_frame.pack(side="left", fill="x", expand=True)
        
        self.label_tamanio = self.crear_info_box(
            info_frame, "Tamaño del Arreglo", "10,000 elementos"
        )
        self.label_tamanio.pack(side="left", padx=10)
        
        self.label_estado = self.crear_info_box(
            info_frame, "Estado", "Listo para iniciar"
        )
        self.label_estado.pack(side="left", padx=10)
        
        self.label_memoria = self.crear_info_box(
            info_frame, "Memoria", "0 MB"
        )
        self.label_memoria.pack(side="left", padx=10)
        
        muestra_frame = tk.Frame(info_container, bg=COLOR_PANEL, width=250)
        muestra_frame.pack(side="right", padx=10, fill="y")
        
        tk.Label(
            muestra_frame,
            text="Muestra del Arreglo",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_DIM
        ).pack(pady=(5, 0))
        
        self.label_muestra = tk.Label(
            muestra_frame,
            text="[...]",
            font=("Consolas", 8),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            wraplength=230,
            justify="left"
        )
        self.label_muestra.pack(pady=(0, 5), padx=10)
        
        # === SELECTOR DE MODO ===
        modo_frame = tk.Frame(self, bg=COLOR_PANEL, height=70)
        modo_frame.pack(fill="x", padx=20, pady=10)
        modo_frame.pack_propagate(False)
        
        tk.Label(
            modo_frame,
            text="Selecciona el tipo de carrera:",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT
        ).pack(pady=(10, 5))
        
        botones_modo = tk.Frame(modo_frame, bg=COLOR_PANEL)
        botones_modo.pack()
        
        self.btn_modo_orden = tk.Button(
            botones_modo,
            text="ORDENAMIENTO",
            command=lambda: self.cambiar_modo("ordenamiento"),
            bg=COLOR_SUCCESS,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=1
        )
        self.btn_modo_orden.pack(side="left", padx=5)
        
        self.btn_modo_busqueda = tk.Button(
            botones_modo,
            text="BÚSQUEDA",
            command=lambda: self.cambiar_modo("busqueda"),
            bg=COLOR_ACCENT,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=1
        )
        self.btn_modo_busqueda.pack(side="left", padx=5)
        
        # === PANEL DE BARRAS DE PROGRESO ===
        carrera_frame = tk.Frame(self, bg=COLOR_PANEL, height=350)
        carrera_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.titulo_carrera = tk.Label(
            carrera_frame,
            text="COMPETIDORES - ORDENAMIENTO",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT
        )
        self.titulo_carrera.pack(pady=10)
        
        self.barras_container = tk.Frame(carrera_frame, bg=COLOR_PANEL)
        self.barras_container.pack(pady=5, fill="both", expand=True)
        
        self.actualizar_barras()
        
        # === PANEL DE GANADOR ===
        self.ganador_frame = tk.Frame(self, bg=COLOR_ACCENT, height=70)
        self.ganador_frame.pack(fill="x", padx=20, pady=10)
        self.ganador_frame.pack_propagate(False)
        
        self.label_ganador = tk.Label(
            self.ganador_frame,
            text="Esperando resultados...",
            font=("Segoe UI", 13, "bold"),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT
        )
        self.label_ganador.pack(expand=True)
        
        # === BOTONES DE CONTROL ===
        botones_frame = tk.Frame(self, bg=COLOR_BG, height=60)
        botones_frame.pack(fill="x", pady=10)
        botones_frame.pack_propagate(False)
        
        self.btn_iniciar = self.crear_boton(
            botones_frame,
            text="INICIAR CARRERA",
            command=self.iniciar_carrera,
            bg=COLOR_SUCCESS,
            width=20
        )
        self.btn_iniciar.pack(side="left", padx=(250, 10))
        
        self.btn_nuevo = self.crear_boton(
            botones_frame,
            text="NUEVO ARREGLO",
            command=self.generar_nuevo_arreglo,
            bg=COLOR_WARNING,
            width=20
        )
        self.btn_nuevo.pack(side="left", padx=10)
    
    def crear_info_box(self, parent, titulo, valor):
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
    
    def cambiar_modo(self, modo):
        # === CAMBIO ENTRE MODO ORDENAMIENTO Y BÚSQUEDA ===
        self.modo_actual = modo
        
        if modo == "ordenamiento":
            self.btn_modo_orden.config(bg=COLOR_SUCCESS)
            self.btn_modo_busqueda.config(bg=COLOR_ACCENT)
            self.titulo_carrera.config(text="COMPETIDORES - ORDENAMIENTO")
        else:
            self.btn_modo_orden.config(bg=COLOR_ACCENT)
            self.btn_modo_busqueda.config(bg=COLOR_SUCCESS)
            if self.objetivo_busqueda is not None:
                self.titulo_carrera.config(text=f"COMPETIDORES - BÚSQUEDA (Objetivo: {self.objetivo_busqueda})")
            elif self.arreglo:
                self.objetivo_busqueda = random.choice(self.arreglo)
                self.titulo_carrera.config(text=f"COMPETIDORES - BÚSQUEDA (Objetivo: {self.objetivo_busqueda})")
        
        self.actualizar_barras()
        
    def actualizar_barras(self):
        # === ACTUALIZACIÓN DE BARRAS DE PROGRESO ===
        for widget in self.barras_container.winfo_children():
            widget.destroy()
        self.barras.clear()
        
        if self.modo_actual == "ordenamiento":
            algoritmos_mostrar = ["Burbuja", "QuickSort", "Inserción"]
        else:
            algoritmos_mostrar = ["Búsqueda Secuencial", "Búsqueda Binaria"]
        
        for nombre in algoritmos_mostrar:
            color = COLORES_ALGORITMOS[nombre]
            barra = BarraProgreso(
                self.barras_container,
                nombre=nombre,
                color=color,
                width=900,
                height=60
            )
            barra.pack(pady=8, padx=30)
            self.barras[nombre] = barra
    
    def actualizar_muestra_arreglo(self):
        # === ACTUALIZACIÓN DE MUESTRA DEL ARREGLO ===
        if self.arreglo:
            muestra = str(self.arreglo[:15])[1:-1]
            if len(self.arreglo) > 15:
                muestra += ", ..."
            self.label_muestra.config(text=muestra)
    
    def generar_nuevo_arreglo(self):
        # === GENERACIÓN DE NUEVO ARREGLO ALEATORIO ===
        self.arreglo = generar_arreglo(10000)
        self.objetivo_busqueda = random.choice(self.arreglo)
        
        self.label_estado.config(text="Nuevo arreglo generado")
        self.label_ganador.config(text="Esperando resultados...")
        
        if self.modo_actual == "busqueda":
            self.titulo_carrera.config(text=f"COMPETIDORES - BÚSQUEDA (Objetivo: {self.objetivo_busqueda})")
        
        self.actualizar_muestra_arreglo()
        
        for barra in self.barras.values():
            barra.reset()
    
    def iniciar_carrera(self):
        # === INICIO DE CARRERA DE ALGORITMOS PARALELOS ===
        if not self.arreglo:
            messagebox.showwarning("Advertencia", "Genera un arreglo primero")
            return
        
        self.btn_iniciar.config(state="disabled")
        self.btn_modo_orden.config(state="disabled")
        self.btn_modo_busqueda.config(state="disabled")
        
        if self.modo_actual == "ordenamiento":
            self.label_estado.config(text="ORDENANDO...")
        else:
            self.label_estado.config(text=f"BUSCANDO...")
            self.titulo_carrera.config(text=f"COMPETIDORES - BÚSQUEDA (Objetivo: {self.objetivo_busqueda})")
        
        self.label_ganador.config(text="Carrera en progreso...")
        
        for barra in self.barras.values():
            barra.reset()
        
        self.carrera = CarreraAlgoritmos(
            self.arreglo,
            callback_progreso=self.on_progreso,
            callback_completo=self.on_completo,
            callback_progreso_tiempo_real=self.on_progreso_tiempo_real
        )
        
        if self.modo_actual == "ordenamiento":
            self.carrera.preparar_carrera(incluir_busqueda=False)
        else:
            self.carrera.preparar_carrera(
                incluir_busqueda=True,
                objetivo_busqueda=self.objetivo_busqueda,
                solo_busqueda=True
            )
        
        self.tiempo_inicio = time.time()
        
        self.animando = True
        threading.Thread(target=self.animar_barras, daemon=True).start()
        
        self.carrera.iniciar_carrera()
    
    def animar_barras(self):
        # === ANIMACIÓN DE BARRAS DE PROGRESO ===
        velocidades = {
            "QuickSort": 0.8,
            "Búsqueda Binaria": 0.9,
            "Búsqueda Secuencial": 0.5,
            "Inserción": 0.15,
            "Burbuja": 0.08,
        }
        
        while self.animando and self.carrera and self.carrera.en_ejecucion:
            for ejecutor in self.carrera.ejecutores:
                if not ejecutor.completado and ejecutor.nombre in self.barras:
                    tiempo_transcurrido = time.time() - self.tiempo_inicio
                    velocidad = velocidades.get(ejecutor.nombre, 0.5)
                    progreso_visual = min(tiempo_transcurrido * velocidad * 10, 95)
                    
                    def actualizar(nombre=ejecutor.nombre, prog=progreso_visual):
                        if nombre in self.barras:
                            self.barras[nombre].actualizar(progreso=prog)
                    
                    self.after(0, actualizar)
            
            time.sleep(0.05)
        
        self.animando = False
    
    def on_progreso_tiempo_real(self, nombre, progreso):
        # === CALLBACK PARA PROGRESO EN TIEMPO REAL ===
        pass
    
    def on_progreso(self, nombre, tiempo, completados):
        # === CALLBACK CUANDO ALGORITMO TERMINA ===
        def update():
            self.barras[nombre].actualizar(progreso=100, tiempo=tiempo, completado=True)
        
        self.after(0, update)
    
    def on_completo(self, resultados, memoria_consumida):
        # === CALLBACK CUANDO TODOS LOS ALGORITMOS TERMINAN ===
        def update():
            self.animando = False
            
            self.btn_iniciar.config(state="normal")
            self.btn_modo_orden.config(state="normal")
            self.btn_modo_busqueda.config(state="normal")
            
            self.label_estado.config(text="Carrera completada")
            self.label_memoria.config(text=formatear_memoria(memoria_consumida))
            
            # === DETERMINACIÓN DEL GANADOR ===
            if resultados:
                ganador, tiempo = resultados[0]
                self.label_ganador.config(
                    text=f"GANADOR: {ganador} - {formatear_tiempo(tiempo)}",
                    fg=COLOR_SUCCESS
                )
                
                tipo = "ORDENAMIENTO" if self.modo_actual == "ordenamiento" else "BÚSQUEDA"
                mensaje = f"CLASIFICACIÓN FINAL - {tipo}:\n\n"
                for i, (nombre, tiempo) in enumerate(resultados, 1):
                    medalla = ["1.", "2.", "3."][i-1] if i <= 3 else f"{i}."
                    mensaje += f"{medalla} {nombre}: {formatear_tiempo(tiempo)}\n"
                
                mensaje += f"\nMemoria consumida: {formatear_memoria(memoria_consumida)}"
                
                messagebox.showinfo("Resultados Finales", mensaje)
        
        self.after(0, update)


if __name__ == "__main__":
    app = AplicacionCarrera()
    app.mainloop()