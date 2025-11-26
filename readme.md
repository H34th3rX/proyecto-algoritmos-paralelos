# 🏁 Carrera de Algoritmos Paralelos

Proyecto Final - Algoritmos Paralelos

## 📋 Descripción

Aplicación de escritorio que simula una "carrera" entre diferentes algoritmos de ordenamiento, ejecutándolos todos en paralelo sobre el mismo arreglo de 10,000 elementos. La aplicación muestra en tiempo real el progreso de cada algoritmo y determina cuál es el más rápido.

## 🎯 Objetivos

### Objetivo General
Implementar y comparar el rendimiento de diferentes algoritmos de búsqueda y ordenamiento ejecutándose en paralelo.

### Objetivos Específicos
- Implementar algoritmos de ordenamiento (Burbuja, QuickSort, Inserción)
- Ejecutar los algoritmos en paralelo usando threading
- Medir y comparar tiempos de ejecución
- Medir consumo de memoria del proceso
- Visualizar los resultados en una interfaz gráfica moderna

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Tkinter** - Interfaz gráfica
- **Threading** - Ejecución paralela
- **Psutil** - Medición de memoria
- **PyInstaller** - Generación de ejecutable

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/H34th3rX/proyecto-algoritmos-paralelos.git
cd proyecto-algoritmos-paralelos
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Generar ejecutable (.exe)
```bash
pyinstaller --onefile --windowed --name="CarreraAlgoritmos" main.py
```

El ejecutable se generará en la carpeta `dist/`

## 📊 Algoritmos Implementados

### Algoritmos de Ordenamiento

1. **Burbuja (Bubble Sort)**
   - Complejidad: O(n²)
   - Método: Comparación e intercambio de elementos adyacentes

2. **QuickSort**
   - Complejidad: O(n log n) promedio
   - Método: Divide y conquista con pivote

3. **Inserción (Insertion Sort)**
   - Complejidad: O(n²)
   - Método: Inserción ordenada elemento por elemento

### Algoritmos de Búsqueda

1. **Búsqueda Secuencial**
   - Complejidad: O(n)

2. **Búsqueda Binaria**
   - Complejidad: O(log n)

## 📁 Estructura del Proyecto

```
proyecto-algoritmos-paralelos/
│
├── main.py              # Aplicación principal con UI
├── algoritmos.py        # Implementación de algoritmos
├── carrera.py          # Sistema de ejecución paralela
├── utils.py            # Utilidades (memoria, tiempo)
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## 🎨 Características de la Interfaz

- ✨ Diseño moderno con tema oscuro
- 📊 Barras de progreso animadas en tiempo real
- 🏆 Visualización del algoritmo ganador
- 💾 Medición de memoria consumida
- 🎯 Resultados detallados con clasificación

## 📈 Resultados

La aplicación muestra:
- Tiempo de ejecución de cada algoritmo
- Clasificación por velocidad
- Memoria RAM consumida durante el proceso
- Algoritmo ganador destacado

## 👥 Autor

[Tu Nombre]

## 📄 Licencia

Este proyecto es parte de un proyecto académico.