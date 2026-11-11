# Documento Maestro Consolidado: Arquitectura de IA Local y Benchmarking de eGPU (16GB VRAM)

*(Integración Dual: LM Studio & LLaMA.cpp Nativo)*

## 1\. Contexto de la Arquitectura y Caso de Uso

Este documento sirve como la fuente de verdad (Single Source of Truth) para la configuración, evaluación y operación de un entorno de Inteligencia Artificial local ejecutado sobre una arquitectura de hardware modular (Mini PC \+ eGPU). Consolida las pruebas de rendimiento operando bajo dos enfoques: interfaz gráfica (LM Studio) y motor puro nativo (LLaMA.cpp).

### 1.1. Caso de Uso Principal

El sistema está diseñado y evaluado como un entorno para actuar como asistente local privado enfocado en:

* **Programación Avanzada:** Generación, refactorización y depuración de código (enfocado en Python).  
* **Análisis de Datos:** Procesamiento de conjuntos de datos, manipulación con librerías especializadas (Pandas, Matplotlib) y razonamiento lógico.  
* **Arquitectura de Software:** Explicación de algoritmos, análisis de complejidad (Big O) y diseño de sistemas.

### 1.2. Especificaciones de Hardware

* **Host (Unidad Central):** GEEKOM Mini IT13 (Procesador Intel Core i9 de 13ª Gen).  
* **Memoria RAM del Sistema:** \~32 GB RAM DDR4/DDR5.  
* **Acelerador Gráfico (eGPU):** NVIDIA GeForce RTX 5060 Ti con **16 GB de VRAM GDDR6 dedicados**.  
* **Interfaz de Conexión:** Base DEG2 conectada a través de puerto **USB4** (40 Gbps), lo cual introduce consideraciones críticas de ancho de banda al paginar memoria.

### 1.3. Entornos de Software y Controladores

* **Sistema Operativo:** Windows 11\.  
* **Plataforma de Inferencia Gráfica:** LM Studio (v0.4.x).  
* **Plataforma de Inferencia Principal (Nativa):** `LLaMA.cpp` nativo (Servidor HTTP `llama-server.exe` y Benchmark automatizado `llama-bench.exe`).  
* **Motor Interno (Backend):** Aceleración de hardware NVIDIA CUDA 13.5 (Compute Capability 12.0).  
* **Gestión de Memoria Base:** Optimizada para aislar la carga de trabajo en la VRAM de la GPU y evitar el desbordamiento hacia la RAM del sistema mediante el bloqueo/desactivación del mapeo en memoria virtual (`mmap` / `-lm none`).

---

## 2\. Metodología de Pruebas (Benchmarking Dual)

El objetivo del plan de pruebas es determinar los límites arquitectónicos de la RTX 5060 Ti (16 GB) ejecutando LLMs de diferentes tamaños, identificando el "punto dulce" de rendimiento e ilustrando la severa penalización por el cuello de botella del cable USB4 al desbordar memoria.

### 2.1. Configuración Base Estricta (LM Studio)

Para garantizar la equidad en el benchmark gráfico, se aplicaron las siguientes configuraciones de carga para aislar la eGPU:

* **GPU Offload:** `Max` (Todas las capas asignadas a la VRAM).  
* **Offload KV Cache to GPU Memory:** `ON` (Activado).  
* **Flash Attention:** `ON` (Activado).  
* **Try mmap():** `OFF` (Desactivado \- *Crítico para evitar la duplicación de carga en la RAM del Host*).  
* **Keep Model in Memory:** `OFF` (Desactivado).

### 2.2. Equivalencia Estricta de Parámetros (LLaMA.cpp Nativo)

Para lograr un rendimiento óptimo equiparable y aislar la memoria de la eGPU, se utilizaron los siguientes parámetros base en la ejecución nativa de consola:

| Concepto | Parámetro LLaMA.cpp | Explicación Técnica |
| :---- | :---- | :---- |
| **Context Length** | `-c 8192` o `-c 4096` | Define el tamaño del contexto del prompt en tokens. |
| **GPU Offload** | `-ngl 99` | Delega el número máximo de capas a la VRAM, forzando procesamiento en GPU. |
| **Flash Attention** | `-fa on` / `-fa off` | Habilita/Deshabilita Flash Attention. Requerido `off` en arquitecturas como Gemma-2 para evitar colapso de memoria compartida CUDA. |
| **Memory Mapping** | `-lm none` | **Crítico:** Desactiva `mmap`. Previene la duplicación y fuga de memoria hacia la RAM del Host (GEEKOM). |
| **Parallel Slots** | `-np 1` | Limita a un único usuario/contexto simultáneo. Crítico en modelos \>25B para evitar colapso del asignador CUDA. |

### 2.3. Prompt Estándar de Prueba

> *Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.*

### 2.4. Métricas de Telemetría Capturadas

1. **Speed (t/s):** Velocidad de generación en tokens por segundo.  
2. **Time to First Token (TTFT):** Latencia inicial en segundos (y tiempo de evaluación de prompt).  
3. **VRAM Utilizada:** Consumo de memoria dedicada de la GPU.  
4. **Uso de RAM (Sistema):** Impacto en la memoria del GEEKOM Mini PC y desbordamiento (Shared GPU Memory).  
5. **Prompt Processing (pp128):** Ingesta de prompt pura medida con `llama-bench`.

---

## 3\. Análisis Detallado por Modelo y Categoría

### 3.1. Prueba 1: Categoría "Punto Dulce" (10B \- 15B)

* **Modelo:** Microsoft Phi-4 (14B)  
* **Cuantización:** `Q6_K` (Alta precisión, baja compresión) \| **Contexto:** 8192 tokens  
* **Tamaño Estimado:** 12.57 GB

**Métricas LM Studio:**

* **Speed:** 33.14 t/s  
* **Latencia (TTFT):** 0.22 s  
* **VRAM / RAM:** 12.7 GB dedicados / 20.0 GB RAM (63%) \- Estable.

**Métricas LLaMA.cpp (Servidor HTTP):**

* **Speed:** 32.08 t/s  
* **Latencia (TTFT):** 326.15 ms (0.32 s)  
* **VRAM / RAM:** 13.1 GB dedicados / 17.3 GB RAM (55%) \- Estable.

**Métricas LLaMA.cpp (`llama-bench` Puro \- 640 ctx):**

* **Speed (Inferencia):** 34.69 t/s (± 0.01)  
* **Ingesta de Prompt:** 1596.19 t/s

**Diagnóstico Consolidado:** El modelo operó al 100% dentro de la VRAM de la gráfica a 46 °C \- 49 °C. Representa el rendimiento ideal de la estación de trabajo. Con \~33 t/s, la fluidez es absoluta para tareas de razonamiento lógico e interactividad en tiempo real. En el entorno nativo puro (`llama-bench`), la velocidad de inferencia escaló a 34.69 t/s, con una ingesta de prompt colosal de casi 1600 tokens asimilados por segundo.

***Nota Técnica:*** En LM Studio se detectó inicialmente una fuga de memoria (98% de uso) que se corrigió desactivando `mmap()`. En LLaMA.cpp, el uso equivalente del flag `-lm none` fue un éxito absoluto, manteniendo el uso del sistema estable en 55% y reutilizando eficientemente 844 grafos sin reasignaciones.

**Ejecución de la Prueba (LM Studio):**

```py
# Python CSV Sales Analysis
Model: microsoft/phi-4
Created: 11/9/2026, 1:32:42 PM
Exported from: LM Studio 0.4.28+2

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
A continuación se presenta un script en Python que realiza las tareas solicitadas:

import pandas as pd
import matplotlib.pyplot as plt

def calculate_sales_by_category(csv_file):
 """
 Lee datos de ventas desde un archivo CSV, calcula el total de ventas por categoría,
 y genera un gráfico de barras.

 :param csv_file: Ruta al archivo CSV que contiene los datos de ventas.
 """

 try:
 # Paso 1: Leer el archivo CSV en un DataFrame
 df = pd.read_csv(csv_file)

 # Comprobar si las columnas necesarias existen
 required_columns = ['Category', 'Sales']
 if not all(column in df.columns for column in required_columns):
 raise ValueError("El archivo CSV no contiene todas las columnas requeridas: 'Category' y 'Sales'.")

 # Paso 2: Calcular el total de ventas por categoría
 sales_by_category = df.groupby('Category')['Sales'].sum()

 # Paso 3: Generar un gráfico de barras de los totales de ventas por categoría
 plt.figure(figsize=(10, 6))
 sales_by_category.plot(kind='bar')
 plt.title("Total de Ventas por Categoría")
 plt.xlabel("Categoría")
 plt.ylabel("Ventas Totales")
 plt.xticks(rotation=45)
 plt.tight_layout() # Ajusta los límites para que todo el texto sea visible
 plt.show()

 except FileNotFoundError:
 print(f"Error: El archivo '{csv_file}' no fue encontrado.")
 except pd.errors.EmptyDataError:
 print("Error: El archivo CSV está vacío o mal formado.")
 except ValueError as ve:
 print(f"Valor Error: {ve}")
 except Exception as e:
 # Manejo de excepciones generales para cualquier otro error inesperado
 print(f"Ha ocurrido un error inesperado: {e}")

def main():
 """
 Función principal que ejecuta el script.
 """

 csv_file = 'ventas.csv' # Cambia esto a la ruta correcta del archivo CSV

 calculate_sales_by_category(csv_file)

# Ejecutar la función principal
if __name__ == "__main__":
 main()

### Explicación de la complejidad temporal (Big O):

1. **Lectura del archivo CSV:** `pd.read_csv()` es una operación cuya complejidad puede aproximarse a \(O(n)\), donde \(n\) es el número de filas en el archivo, ya que se lee cada fila y se almacena en un DataFrame.

2. **Agrupamiento (`groupby`) y suma (`sum`):** Estas operaciones también tienen una complejidad aproximada a \(O(n)\) porque se procesa cada fila del DataFrame para calcular las sumas por categoría.

3. **Generación del gráfico:** El proceso de crear un gráfico con `matplotlib` depende del número de grupos (categorías), lo cual es típicamente mucho menor que el número total de filas, resultando en una complejidad prácticamente constante \(O(k)\) donde \(k\) es el número de categorías. Por lo tanto, la generación del gráfico no afecta significativamente la eficiencia general.

En resumen, dado que las operaciones principales son lineales respecto al tamaño del conjunto de datos (`n`), podemos considerar que la complejidad temporal total del script es \(O(n)\).
```

**Ejecución de la Prueba (LLaMA.cpp Nativo):**

```py
# Python CSV Sales Analysis
Model: microsoft/phi-4
Created: 11/10/2026, 1:16:00 PM
Exported from: LLaMA.cpp Server 0.9.0-dev (build 12235, commit 0a94a3f28)

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
¡Por supuesto! A continuación se muestra un script en Python que logra lo que solicitas: lee un archivo CSV con datos de ventas, calcula el total de ventas por categoría usando pandas y genera un gráfico de barras utilizando matplotlib. El script incluye manejo de excepciones, comentarios explicativos paso a paso y una función principal bien estructurada.

import pandas as pd
import matplotlib.pyplot as plt

def calculate_sales_by_category(csv_file):
 """
 Lee un archivo CSV con datos de ventas, calcula el total de ventas por categoría
 y genera un gráfico de barras.

 Parámetros:
 csv_file (str): Ruta al archivo CSV que contiene los datos de ventas.
 """
 try:
 # Paso 1: Cargar los datos del archivo CSV en un DataFrame de pandas
 # El archivo CSV se espera que tenga columnas 'Category' y 'Sales'
 df = pd.read_csv(csv_file)
 
 # Paso 2: Calcular el total de ventas por categoría
 # Sumamos las ventas agrupadas por la columna 'Category'
 sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
 
 # Paso 3: Generar un gráfico de barras del total de ventas por categoría
 plt.figure(figsize=(10, 6)) # Establecer el tamaño de la figura
 plt.bar(sales_by_category['Category'], sales_by_category['Sales'], color='skyblue')
 plt.title('Total de Ventas por Categoría')
 plt.xlabel('Categoría')
 plt.ylabel('Ventas Totales')
 plt.xticks(rotation=45) # Rotar las etiquetas de los ejes X para mejor legibilidad
 plt.tight_layout() # Ajustar automáticamente los márgenes
 plt.show()
 
 except FileNotFoundError:
 print(f"Error: El archivo {csv_file} no se encontró. Por favor, verifica la ruta.")
 except pd.errors.EmptyDataError:
 print("Error: El archivo CSV está vacío.")
 except pd.errors.ParserError:
 print("Error: El archivo CSV no se pudo analizar. Verifica el formato del archivo.")
 except KeyError as e:
 print(f"Error: Faltan columnas esperadas en el archivo CSV. {e}")
 except Exception as e:
 print(f"Ocurrió un error inesperado: {e}")

def main():
 """
 Función principal que define la ruta del archivo CSV y llama a la función de cálculo.
 """
 csv_file = 'sales_data.csv' # Ruta al archivo CSV con los datos de ventas
 calculate_sales_by_category(csv_file)

if __name__ == "__main__":
 main()

### Explicación de la Complejidad Temporal (Big O)

1. **Cargar el archivo CSV**: El tiempo de carga de un archivo CSV a un DataFrame de pandas es \(O(n)\), donde \(n\) es el número de filas en el archivo. Esto se debe a que pandas debe leer y almacenar cada fila en la memoria.

2. **Agrupar y sumar**: La operación `groupby` seguida de `sum` es \(O(n \log n)\) en el peor caso, donde \(n\) es el número de filas. Esto se debe a que el agrupamiento puede requerir una operación de ordenamiento internamente, aunque pandas es optimizado para ser eficiente en tales operaciones.

3. **Generar el gráfico**: La creación de un gráfico de barras con matplotlib es \(O(m)\), donde \(m\) es el número de categorías únicas (resultados del agrupamiento). Esto implica trazar \(m\) barras en el gráfico.

En resumen, el script tiene una complejidad temporal general de \(O(n \log n)\), dominada por la operación de agrupamiento y suma.
```

&nbsp;

### 3.2. Prueba 2: Categoría "Mediano-Pesado" (20B \- 24B)

* **Modelo:** Mistral Codestral 22B-v0.1  
* **Cuantización:** `Q4_K_M` \| **Contexto:** 8192 tokens  
* **Tamaño Estimado:** 13.95 GB

**Métricas LM Studio:**

* **Speed:** 29.22 t/s  
* **Latencia (TTFT):** 0.30 s  
* **VRAM / RAM:** 14.5 GB dedicados / 20.4 GB RAM (64%) \- Estable.

**Métricas LLaMA.cpp (Servidor HTTP):**

* **Speed:** 27.99 t/s  
* **Latencia (TTFT):** 312.18 ms (0.31 s)  
* **VRAM / RAM:** 14.8 GB dedicados / 16.9 GB RAM (53%) \- Estable.

**Métricas LLaMA.cpp (`llama-bench` Puro \- 640 ctx):**

* **Speed (Inferencia):** 29.48 t/s (± 0.19)  
* **Ingesta de Prompt:** 1164.11 t/s

**Diagnóstico Consolidado:** Equilibrio observado en esta prueba, con un uso de \~14.8 GB de VRAM y sin desbordamiento hacia la memoria del sistema bajo la configuración documentada. Mantuvo una velocidad de inferencia de \~28 a 29.5 t/s y una latencia baja. Estos resultados describen esta ejecución concreta y no constituyen una garantía para otros archivos GGUF, versiones o contextos. La temperatura operó de forma estable a 49 °C.

**Ejecución de la Prueba (LM Studio):**

```py
# Python CSV Sales Analysis
Model: mistralai/codestral-22b-v0.1
Created: 11/9/2026, 2:00:24 PM
Exported from: LM Studio 0.4.28+2

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
¡Claro! Voy a escribir un script en Python que realice las tareas descritas. A continuación, te muestro el código:

# Importamos las bibliotecas necesarias
import pandas as pd
import matplotlib.pyplot as plt

def main():
 try:
 # Leemos el archivo CSV con los datos de ventas
 data = pd.read_csv('ventas.csv')

 # Calculamos el total de ventas por categoría
 sales_by_category = data.groupby('Categoria')['Total'].sum()

 # Generamos un gráfico de barras con los resultados
 plt.figure(figsize=(10, 6))
 sales_by_category.plot(kind='bar', color='skyblue')
 plt.title('Ventas totales por categoría')
 plt.xlabel('Categoría')
 plt.ylabel('Total de ventas')
 plt.xticks(rotation=45)
 plt.tight_layout()
 plt.show()
 except FileNotFoundError:
 print("El archivo 'ventas.csv' no se encontró. Asegúrate de que esté en el directorio correcto.")
 except Exception as e:
 print(f"Ocurrió un error inesperado: {e}")

# Llamamos a la función principal para ejecutar el script
main()

Este script comienza importando las bibliotecas `pandas` y `matplotlib.pyplot`. Luego, define una función `main`, que lee un archivo CSV de ventas, calcula el total de ventas por categoría usando la función `groupby` y `sum` de pandas, y genera un gráfico de barras utilizando matplotlib.

En cuanto a la complejidad temporal (Big O) de esta solución:
- La lectura del archivo CSV tiene una complejidad temporal de O(n), donde n es el número de filas en el archivo.
- El cálculo del total de ventas por categoría utilizando `groupby` y `sum` también tiene una complejidad temporal de O(n).
- La generación del gráfico de barras con matplotlib es generalmente rápida, pero en el peor caso, puede tener una complejidad temporal de O(n), donde n es el número de categorías.

Por lo tanto, la complejidad temporal total de esta solución sería O(n) en el peor caso escenario.
```

**Ejecución de la Prueba (LLaMA.cpp Nativo):**

```py
# Python CSV Sales Analysis
Model: mistralai/codestral-22b-v0.1
Created: 11/10/2026, 1:19:00 PM
Exported from: LLaMA.cpp Server 0.9.0-dev (build 12235, commit 0a94a3f28)

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
# Importamos las librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt

def calcular_ventas_por_categoria(nombre_archivo):
 try:
 # Leemos el archivo CSV y almacenamos los datos en un DataFrame
 datos = pd.read_csv(nombre_archivo)

 # Verificamos si la columna 'Categoria' y 'Ventas' están presentes en el DataFrame
 if 'Categoria' not in datos.columns or 'Ventas' not in datos.columns:
 raise ValueError("El archivo CSV no contiene las columnas 'Categoria' y 'Ventas'")

 # Calculamos el total de ventas por categoría
 ventas_por_categoria = datos.groupby('Categoria')['Ventas'].sum()

 return ventas_por_categoria
 except FileNotFoundError:
 print(f"El archivo '{nombre_archivo}' no existe")
 except Exception as e:
 print(f"Ocurrió un error: {e}")

def graficar_ventas_por_categoria(ventas_por_categoria):
 try:
 # Creamos un gráfico de barras utilizando matplotlib
 plt.bar(ventas_por_categoria.index, ventas_por_categoria.values)
 plt.xlabel('Categoría')
 plt.ylabel('Ventas')
 plt.title('Ventas por Categoría')
 plt.show()
 except Exception as e:
 print(f"Ocurrió un error al generar el gráfico: {e}")

def main():
 # Nombre del archivo CSV
 nombre_archivo = 'ventas.csv'

 # Calculamos las ventas por categoría
 ventas_por_categoria = calcular_ventas_por_categoria(nombre_archivo)

 if ventas_por_categoria is not None:
 # Graficamos las ventas por categoría
 graficar_ventas_por_categoria(ventas_por_categoria)

if __name__ == '__main__':
 main()

En este código, la complejidad temporal es O(n log n), donde n es el número de filas en el archivo CSV. Esto se debe a que la función `groupby` de pandas tiene una complejidad temporal de O(n log n) en el peor caso.
```

&nbsp;

### 3.3. Prueba 3: Categoría "Pesos Pesados" (25B \- 28B)

* **Modelo:** Google Gemma-2-27B-It  
* **Cuantización:** `Q3_K_L` (Compresión agresiva) \| **Contexto:** 8192 tokens  
* **Tamaño Estimado:** 15.84 GB

**Métricas LM Studio:**

* **Speed:** 6.41 t/s (Caída de \~78% vs Codestral)  
* **Latencia (TTFT):** 3.04 s  
* **VRAM / RAM:** 15.5 GB dedicados / RAM con Desbordamiento de 2.4 GB (Cuello USB4).

**Métricas LLaMA.cpp (Servidor HTTP `-fa off`, `-np 1`):**

* **Speed:** 2.18 t/s  
* **Latencia (TTFT):** 3.67 s  
* **VRAM / RAM:** 15.6 GB dedicados / RAM con Desbordamiento de 2.6 GB (Cuello USB4).

**Métricas LLaMA.cpp (`llama-bench` Puro \- 640 ctx, `-fa off`):**

* **Speed (Inferencia):** 25.16 t/s (± 0.10)  
* **Ingesta de Prompt:** 904.39 t/s

**Diagnóstico Consolidado:** Esta prueba demarcó el límite arquitectónico. En el escenario web/HTTP con contexto largo (8192), al exceder el espacio de la VRAM, el sistema forzó la paginación a través del puerto USB4. Este cuello de botella desplomó la velocidad a un rango de 2.18 t/s \- 6.41 t/s y dejó la GPU "fría" a 43 °C (esperando datos de memoria principal). Sin embargo, `llama-bench` reveló un dato fascinante: al reservar memoria para un contexto diminuto (640 tokens totales), el modelo cupo exactamente en la VRAM y aceleró a **25.16 t/s**. Esto demuestra que la GPU tiene el poder bruto necesario, pero el ancho de banda del USB4 colapsa el rendimiento si se activa la memoria compartida.

***Nota Técnica:** Para correr Gemma-2 nativamente fue indispensable desactivar Flash Attention (`-fa off`) y limitar los slots a 1 (`-np 1`) para evitar el colapso del asignador CUDA.*

**Ejecución de la Prueba (LM Studio):**

```py
# Python CSV Sales Analysis
Model: google/gemma-2-27b
Created: 11/9/2026, 2:25:14 PM
Exported from: LM Studio 0.4.28+2

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
import pandas as pd
import matplotlib.pyplot as plt

def generar_grafico_ventas(archivo_csv):
 """
 Lee un archivo CSV con datos de ventas, calcula el total de ventas por categoría y genera un gráfico de barras.

 Args:
 archivo_csv (str): Ruta al archivo CSV.

 Returns:
 None
 """
 try:
 # Leer el archivo CSV usando pandas
 df = pd.read_csv(archivo_csv)

 # Agrupar las ventas por categoría y calcular la suma de cada grupo
 ventas_por_categoria = df.groupby('Categoría')['Ventas'].sum()

 # Crear un gráfico de barras utilizando matplotlib
 plt.bar(ventas_por_categoria.index, ventas_por_categoria.values)
 plt.xlabel("Categorías")
 plt.ylabel("Total de Ventas")
 plt.title("Total de Ventas por Categoría")
 plt.show()

 except FileNotFoundError:
 print(f"Error: El archivo {archivo_csv} no se encontró.")
 except Exception as e:
 print(f"Error al procesar el archivo: {e}")


if __name__ == "__main__":
 # Nombre del archivo CSV que contiene los datos de ventas
 nombre_archivo = "ventas.csv"

 # Llamar a la función para generar el gráfico
 generar_grafico_ventas(nombre_archivo)


**Explicación:**

1. **Importación de bibliotecas**: Se importan las bibliotecas necesarias: pandas para manipular datos y matplotlib para crear gráficos.

2. **Función `generar_grafico_ventas`**:

 - Toma el nombre del archivo CSV como argumento.
 - Utiliza un bloque `try...except` para manejar posibles errores durante la lectura del archivo o el procesamiento de los datos.
 - Lee el archivo CSV usando `pd.read_csv()`.
 - Agrupa las ventas por categoría utilizando `groupby()` y calcula la suma de las ventas de cada grupo con `sum()`.
 - Crea un gráfico de barras utilizando `plt.bar()`, estableciendo las etiquetas para los ejes y el título del gráfico. Finalmente, muestra el gráfico con `plt.show()`.

3. **Función principal (`if __name__ == "__main__":`)**:

 - Define el nombre del archivo CSV que se utilizará.
 - Llama a la función `generar_grafico_ventas()` para procesar el archivo y generar el gráfico.


**Complejidad Temporal (Big O):**

- La lectura del archivo CSV con `pd.read_csv()` generalmente tiene una complejidad temporal de **O(n)**, donde 'n' es el número de filas en el archivo.
- El agrupamiento y la suma de las ventas por categoría con `groupby()` y `sum()` también tienen una complejidad temporal de **O(n)** en promedio.
- La creación del gráfico de barras con matplotlib tiene una complejidad temporal que depende del número de categorías, pero generalmente se considera **O(m)**, donde 'm' es el número de categorías únicas.

En general, la complejidad temporal total de este script sería **O(n + m)**, dominada por la lectura del archivo CSV y el procesamiento de los datos.
```

**Ejecución de la Prueba (LLaMA.cpp Nativo):**

```py
# Python CSV Sales Analysis
Model: google/gemma-2-27b
Created: 11/10/2026, 1:21:00 PM
Exported from: LLaMA.cpp Server 0.9.0-dev (build 12235, commit 0a94a3f28)

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
import pandas as pd
import matplotlib.pyplot as plt

def generar_grafico_ventas_por_categoria(nombre_archivo):
 """
 Lee un archivo CSV, calcula el total de ventas por categoría y genera un gráfico de barras.

 Args:
 nombre_archivo (str): El nombre del archivo CSV a leer.

 Returns:
 None
 """
 try:
 # Leer el archivo CSV utilizando pandas
 df = pd.read_csv(nombre_archivo)

 # Agrupar las ventas por categoría y calcular la suma total para cada categoría
 ventas_por_categoria = df.groupby('Categoria')['Ventas'].sum()

 # Generar un gráfico de barras
 plt.bar(ventas_por_categoria.index, ventas_por_categoria.values)
 plt.xlabel('Categoría')
 plt.ylabel('Total de Ventas')
 plt.title('Total de Ventas por Categoría')
 plt.show()

 except FileNotFoundError:
 print(f"Error: El archivo {nombre_archivo} no se encontró.")
 except Exception as e:
 print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
 nombre_archivo_csv = 'ventas.csv' # Reemplaza con el nombre real del archivo
 generar_grafico_ventas_por_categoria(nombre_archivo_csv)

**Explicación del código:**

1. **Importación de bibliotecas:** Se importan las bibliotecas `pandas` para el manejo de datos y `matplotlib.pyplot` para la generación de gráficos.
2. **Función `generar_grafico_ventas_por_categoria`:**
 - Toma el nombre del archivo CSV como argumento.
 - Utiliza un bloque `try-except` para manejar posibles errores durante la lectura del archivo o el procesamiento de datos.
 - Lee el archivo CSV utilizando `pd.read_csv`.
 - Agrupa las ventas por categoría utilizando `groupby('Categoria')` y calcula la suma total de ventas para cada categoría con `sum()`.
 - Genera un gráfico de barras utilizando `plt.bar`, configurando etiquetas para los ejes y el título del gráfico.
 - Muestra el gráfico con `plt.show()`.
 - Maneja excepciones `FileNotFoundError` (si el archivo no se encuentra) y `Exception` (para otros errores).

3. **Función principal (`if __name__ == "__main__":`)**:
 - Define el nombre del archivo CSV a procesar.
 - Llama a la función `generar_grafico_ventas_por_categoria` para realizar el análisis y generar el gráfico.

**Complejidad temporal (Big O):**

- La lectura del archivo CSV con `pd.read_csv` tiene una complejidad O(n), donde n es el número de filas en el archivo.
- El agrupamiento y la suma de ventas por categoría con `groupby` y `sum` también tienen una complejidad O(n).
- La generación del gráfico de barras con `plt.bar` depende de la biblioteca matplotlib y su implementación interna, pero generalmente se considera O(n) para n barras.

Por lo tanto, la complejidad temporal general de este código es **O(n)**, donde n es el número de filas en el archivo CSV.
```

&nbsp;

### 3.4. Prueba 4: Categoría "El Jefe Final" (30B \- 35B)

* **Modelo:** Qwen2.5-Coder-32B-Instruct  
* **Cuantización:** `Q3_K_M` \| **Contexto:** 4096 tokens (Reducido por seguridad)  
* **Tamaño Estimado:** 15.94 GB

**Métricas LM Studio:**

* **Speed:** 8.54 t/s  
* **Latencia (TTFT):** 3.72 s  
* **VRAM / RAM:** 15.6 GB dedicados / Desbordamiento de 0.8 GB a memoria de GPU compartida.

**Métricas LLaMA.cpp (Servidor HTTP `-np 1`):**

* **Speed:** 2.59 t/s  
* **Latencia (TTFT):** 12.31 s  
* **VRAM / RAM:** 15.5 GB dedicados / Desbordamiento de 1.3 GB a memoria de GPU compartida.

**Métricas LLaMA.cpp (`llama-bench` Puro \- 640 ctx):**

* **Speed (Inferencia):** 23.37 t/s (± 0.23)  
* **Ingesta de Prompt:** 726.92 t/s

**Diagnóstico Consolidado:** Prueba de estrés superada con concesiones. A diferencia de Gemma-2, Qwen soporta Flash Attention nativo, pero para ejecutar 32B fue mandatorio recortar el contexto a 4096 tokens y aceptar un desbordamiento hacia la memoria RAM (0.8 GB \- 1.3 GB). La velocidad web colapsó severamente (2.59 t/s \- 8.54 t/s). Nuevamente, la prueba aislada `llama-bench` demostró que este modelo colosal es capaz de superar los 23 t/s si el usuario restringe la memoria de contexto al mínimo absoluto. Ideal para flujos de tareas asíncronas.

**Ejecución de la Prueba (LM Studio):**

```py
# Python CSV Sales Analysis
Model: qwen2.5-coder-32b-instruct
Created: 11/9/2026, 2:56:23 PM
Exported from: LM Studio 0.4.28+2

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
import pandas as pd
import matplotlib.pyplot as plt

def leer_y_procesar_csv(archivo):
 """
 Esta función lee un archivo CSV con datos de ventas y calcula el total de ventas por categoría.
 
:param archivo: Nombre del archivo CSV a procesar.
 :return: DataFrame agrupado por categorías con el total de ventas.
 """
 try:
 # Leer el archivo csv en un dataframe
 df = pd.read_csv(archivo)
 
# Verificar si las columnas 'categoria' y 'venta' están presentes en el dataframe
 if not {'categoria', 'venta'}.issubset(df.columns):
 raise KeyError("El dataframe debe contener al menos las columnas 'categoria' y 'venta'.")
 
# Agrupar por la columna de categoría y sumar los valores de ventas
 df_agrupado = df.groupby('categoria')['venta'].sum().reset_index()
 
return df_agrupado
 
except FileNotFoundError:
 print(f"No se encontró el archivo: {archivo}")
 
except KeyError as e:
 print(e)

 except Exception as e:
 print("Ocurrió un error inesperado:", str(e))

def generar_grafico_barras(df):
 """
 Esta función genera y muestra un gráfico de barras para las ventas agrupadas por categoría.

 :param df: DataFrame con categorías y sus totales de ventas correspondientes.
 """
 try:
 # Configurar el tamaño del plot
 plt.figure(figsize=(10, 6))
 
# Generar la barra de gráficos
 plt.bar(df['categoria'], df['venta'])

 # Añadir título y etiquetas a los ejes
 plt.title("Total de Ventas por Categoría")
 plt.xlabel("Categorías")
 plt.ylabel("Ventas Totales")

 # Rotar las categorías en el eje x para mejor visibilidad
 plt.xticks(rotation=45, ha="right")

 # Mostrar la figura
 plt.show()
 
except Exception as e:
 print("Ocurrió un error al generar el gráfico:", str(e))
 
def main():
 """
 Función principal que ejecuta el proceso completo de lectura del archivo CSV,
 cálculo de ventas por categoría y generación del gráfico correspondiente.
 """
 # Nombre del archivo csv (cambiar según corresponda)
 nombre_archivo = "ventas.csv"

 # Leer el archivo csv, calcular las ventas totales por cada categoría y generar un dataframe agrupado
 df_ventas_agrupadas = leer_y_procesar_csv(nombre_archivo)

 # Si los datos se leyeron correctamente, procedemos a generar la gráfica de barras
 if isinstance(df_ventas_agrupadas, pd.DataFrame):
 generar_grafico_barras(df_ventas_agrupadas)

if __name__ == "__main__":
 main()

**Explicación breve de la complejidad temporal (Big O)**
- La función `leer_y_procesar_csv` tiene una complejidad de O(n), donde n es el número de líneas en el archivo CSV. Esto se debe a que cada fila se procesa una vez para crear el DataFrame, y luego cada fila se agrupa por categoría.
 
- La función `generar_grafico_barras` también tiene una complejidad de O(m), donde m es el número de categorías únicas en los datos. Esto se debe a que se dibuja una barra por cada categoría.

En resumen, la complejidad total del programa dependerá del tamaño del archivo CSV (n) y del número de categorías únicas (m). Sin embargo, generalmente n será mucho mayor que m, por lo que podríamos decir que el tiempo de ejecución total es proporcional a O(n).
```

**Ejecución de la Prueba (LLaMA.cpp Nativo):**

```py
# Python CSV Sales Analysis
Model: qwen2.5-coder-32b-instruct
Created: 11/10/2026, 1:23:00 PM
Exported from: LLaMA.cpp Server 0.9.0-dev (build 12235, commit 0a94a3f28)

### User
Escribe un script en Python que lea un archivo CSV con datos de ventas, calcule el total de ventas por categoría usando pandas, y genere un gráfico de barras utilizando matplotlib. El código debe incluir manejo de excepciones, comentarios explicativos paso a paso, y una función principal bien estructurada. Finalmente, explica brevemente la complejidad temporal (Big O) de tu solución.

### Assistant
Para crear un script en Python que cumple con tus requerimientos, primero debemos asegurarnos de que tenemos las bibliotecas necesarias instaladas: `pandas` y `matplotlib`. Podemos instalarlas usando `pip` si no están disponibles:

pip install pandas matplotlib

A continuación, proporciono el código del script:

import pandas as pd
import matplotlib.pyplot as plt

def plot_sales_by_category(filename):
 """
 Función principal que lee un archivo CSV, calcula el total de ventas por categoría
 y genera un gráfico de barras.
 :param filename: Nombre del archivo CSV
 """
 try:
 # Leer el archivo CSV usando pandas
 sales_data = pd.read_csv(filename)

 # Verificar si las columnas necesarias están en el DataFrame
 if 'category' not in sales_data.columns or 'sales' not in sales_data.columns:
 raise ValueError("El archivo CSV debe contener las columnas 'category' y 'sales'.")

 # Calcular el total de ventas por categoría
 sales_by_category = sales_data.groupby('category')['sales'].sum().reset_index()

 # Crear un gráfico de barras
 plt.figure(figsize=(10, 6))
 plt.bar(sales_by_category['category'], sales_by_category['sales'], color='skyblue')
 plt.xlabel('Categoría')
 plt.ylabel('Total de Ventas')
 plt.title('Total de Ventas por Categoría')
 plt.xticks(rotation=45)
 plt.tight_layout()

 # Mostrar el gráfico
 plt.show()

 except FileNotFoundError:
 print(f"Error: El archivo '{filename}' no fue encontrado.")
 except pd.errors.EmptyDataError:
 print("Error: El archivo CSV está vacío.")
 except pd.errors.ParserError:
 print("Error: No se pudo analizar el archivo CSV.")
 except ValueError as ve:
 print(f"Error de valor: {ve}")
 except Exception as e:
 print(f"Ocurrió un error inesperado: {e}")

def main():
 # Nombre del archivo CSV a procesar
 filename = 'sales_data.csv'

 # Llamar a la función principal
 plot_sales_by_category(filename)

if __name__ == "__main__":
 main()

### Explicación paso a paso:

1. **Importaciones**: Importamos `pandas` y `matplotlib.pyplot` para la manipulación de datos y la generación de gráficos, respectivamente.
2. **Definición de la función `plot_sales_by_category`**: Esta función recibe el nombre del archivo CSV como argumento.
3. **Manejo de excepciones**: Se han implementado varias excepciones para manejar posibles errores durante la lectura del archivo, como archivos no encontrados, datos vacíos o errores de análisis.
4. **Lectura del archivo CSV**: Se utiliza `pandas.read_csv` para cargar los datos del archivo en un DataFrame.
5. **Verificación de columnas**: Se verifica que el archivo CSV contenga las columnas necesarias ('category' y 'sales').
6. **Cálculo de ventas por categoría**: Se utiliza `groupby` y `sum` para calcular el total de ventas por cada categoría.
7. **Generación del gráfico**: Se crea un gráfico de barras con `matplotlib.pyplot` para visualizar los resultados.
8. **Definición de la función principal `main`**: Se define la función `main` que llama a `plot_sales_by_category` con el nombre del archivo.
9. **Ejecución del script**: Se verifica que el script se está ejecutando como el programa principal y se llama a `main`.

### Complejidad Temporal (Big O):

La complejidad temporal del script es principalmente determinada por la lectura del archivo CSV y el procesamiento de los datos. La lectura del archivo CSV y la agrupación de datos son las operaciones más costosas. 

- **Lectura del archivo CSV**: O(n), donde n es el número de filas en el archivo.
- **Agrupamiento y suma de ventas por categoría**: O(m), donde m es el número de categorías únicas.
- **Generación del gráfico**: La generación del gráfico es generalmente O(k), donde k es el número de categorías únicas que se representan en el gráfico.

En resumen, la complejidad temporal del script es O(n + m + k), siendo n el número de filas en el archivo CSV, m el número de categorías únicas, y k el número de categorías únicas que se muestran en el gráfico. Dado que n suele ser mucho mayor que m y k, la complejidad del script puede aproximarse a O(n).
```

---

## 4\. Consolidación de Rendimiento y Desviación Arquitectónica

### 4.1. Matriz de Rendimiento: LM Studio Gráfico

| Categoría | Modelo Evaluado (Cuantización) | Tokens Contexto | Latencia Inicial | Velocidad Inferencia | Uso VRAM (GPU) | Desbordamiento RAM |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Punto Dulce (14B)** | Phi-4 14B (`Q6_K`) | 8192 | **0.22 s** | **33.14 t/s** | 12.7 GB | **0.0 GB** |
| **Mediano-Pesado (22B)** | Codestral 22B (`Q4_K_M`) | 8192 | **0.30 s** | **29.22 t/s** | 14.5 GB | **0.0 GB** |
| **Pesos Pesados (27B)** | Gemma-2-27B (`Q3_K_L`) | 8192 | 3.04 s | 6.41 t/s | 15.5 GB | 2.4 GB (Cuello USB4) |
| **Jefe Final (32B)** | Qwen2.5-32B (`Q3_K_M`) | 4096 | 3.72 s | 8.54 t/s | 15.6 GB | 0.8 GB (Cuello USB4) |

### 4.2. Matriz de Rendimiento: LLaMA.cpp Nativo (Server HTTP vs Bench Puro)

| Categoría / Modelo (Cuantización) | Velocidad Real (`llama-server`) | Velocidad Pura (`llama-bench`) | Latencia Inicial HTTP (TTFT) | Ingesta de Prompt Pura | Comportamiento VRAM (Límite 16 GB eGPU) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Punto Dulce**: Phi-4 14B (`Q6_K`) | **32.08 t/s** | **34.69 t/s** | 0.32 s | 1596.19 t/s | **Óptimo:** 13.1 GB en VRAM. Sin desbordamiento. |
| **Mediano-Pesado**: Codestral 22B (`Q4_K_M`) | **27.99 t/s** | **29.48 t/s** | 0.31 s | 1164.11 t/s | **Límite Seguro:** 14.8 GB en VRAM. Sin desbordamiento. |
| **Pesos Pesados**: Gemma-2-27B (`Q3_K_L`) | **2.18 t/s** | **25.16 t/s** | 3.67 s | 904.39 t/s | **Cuello de Botella (Server):** Desborda 2.6 GB a RAM. **Óptimo (Bench):** Cabe justo por contexto mínimo. |
| **El Jefe Final**: Qwen2.5-32B (`Q3_K_M`) | **2.59 t/s** | **23.37 t/s** | 12.31 s | 726.92 t/s | **Cuello de Botella (Server):** Desborda 1.3 GB a RAM. **Óptimo (Bench):** Cabe justo por contexto mínimo. |

### 4.3. Análisis de Desviación Arquitectónica

1. **La Sobrecarga de Red y API (Modelos 14B \- 22B):** Para los modelos que caben completamente en la VRAM (Phi-4 y Codestral), la diferencia entre el motor puro C++ y los servidores HTTP/Gráficos es de apenas \~1.5 a 2.5 t/s. Esto demuestra que la implementación HTTP de LLaMA.cpp (y LM Studio sobre él) es extremadamente ligera y el overhead local es despreciable.  
2. **La Trampa del Contexto (Modelos 27B \- 32B):** Gemma-2 y Qwen2.5 saltaron masivamente de \~2 t/s a **\~25 t/s y \~23 t/s** en la prueba `llama-bench`. Esto sucede porque la prueba automatizada solo reserva caché KV para 640 tokens, logrando encajar todo el modelo de \>25B dentro de los 16 GB físicos. En los servidores, reservar 4096 u 8192 tokens fuerza a paginar gigabytes hacia la RAM del GEEKOM, destrozando el rendimiento por el ancho de banda limitado del USB4.  
3. **Velocidad de Ingesta (Prompt Processing):** Las métricas revelan una capacidad colosal gracias a Flash Attention. Procesar casi **1600 tokens por segundo** en Phi-4 permite asimilar documentos de código extensos instantáneamente.

---

## 5\. Catálogo de Modelos Sugeridos para Caso de Uso (Noviembre 2026\)

Este catálogo contiene configuraciones propuestas para programación avanzada en Python, análisis de datos y arquitectura de software, adaptadas como hipótesis de trabajo a la arquitectura RTX 5060 Ti 16GB (eGPU USB4). No representa un inventario local ni una validación individual de todos los modelos listados.

### Estado de validación

- **Probado:** modelo y configuración ejecutados localmente con métricas documentadas en las matrices de la sección 4.
- **Estimado:** comportamiento calculado a partir del tamaño, cuantización y límites de VRAM; requiere ejecución local.
- **Recomendado:** candidato de búsqueda para el caso de uso; todavía no validado en esta arquitectura.
- **Pendiente:** modelo, archivo GGUF o script aún no disponible localmente.

Salvo que un modelo aparezca en las matrices de rendimiento de la sección 4, las entradas de este catálogo deben interpretarse como **Recomendadas** o **Pendientes**, no como configuraciones optimizadas o validadas.

### 5.1. Categoría "Punto Dulce" (10B a 15B)

*Propuesta LLaMA.cpp: Máxima asimilación de contexto. Esta categoría puede ser adecuada para bases de código extensas y cuantizaciones altas (`Q6_K` o `Q8_0`), pero la velocidad y el contexto deben validarse con cada archivo GGUF.*

*Propuesta LM Studio: Priorizar la velocidad interactiva con GPU Offload al máximo. La cuantización `Q6_K` puede ofrecer una buena relación entre precisión y consumo, pero requiere validación local.*

* **[Pendiente de validación] `gemma-4-12B-coder-fable5`:** Candidato para análisis de datos e integración de frameworks. El consumo de memoria y el contexto disponible deben comprobarse localmente.  
* **[Pendiente de validación] `DeepSeek-Coder-V3-14B`:** Candidato para infraestructura, Bash y bases de datos SQL. La ingesta y el rendimiento deben comprobarse localmente.  
* **[Pendiente de validación] `ministral-3-14b-reasoning`:** Candidato para diseño de arquitecturas de software y depuración lógica. La fluidez en C++ debe comprobarse localmente.  
* **[Pendiente de validación] `Qwen3-14B-Coder-Instruct`:** Candidato para proyectos con varios scripts interconectados. La capacidad de contexto y el tiempo de procesamiento deben comprobarse localmente.  
* **[Pendiente de validación] `Llama-4-11B-Code-Instruct`:** Candidato para conversaciones de programación de múltiples turnos. La retención de historial y la velocidad deben comprobarse localmente.

### 5.2. Categoría "Mediano-Pesado" (20B a 24B)

*Propuesta LLaMA.cpp: Categoría de equilibrio entre capacidad y consumo. `Q4_K_M` puede situarse cerca del límite de VRAM; el rendimiento y la ausencia de desbordamiento deben comprobarse por modelo.*

*Propuesta LM Studio: Configuración candidata para uso diario. Requiere descargar la cuantización `Q4_K_M` y verificar que "Try mmap()" esté apagado, además de medir el consumo real.*

* **[Pendiente de validación] `mistral-small-3.2`:** Candidato de Mistral para procesamiento de archivos extensos. El consumo de caché y la estabilidad térmica deben comprobarse localmente.  
* **[Pendiente de validación] `Qwen3-22B-Coder-Instruct`:** Candidato para flujos de Data Science con Pandas, NumPy, Scikit-learn y Matplotlib. La retención de tablas debe comprobarse localmente.  
* **[Pendiente de validación] `Llama-4-22B-Code-Instruct`:** Candidato para una configuración `Q4_K_M` dentro del límite de 16 GB. El consumo real y la capacidad de contexto deben comprobarse localmente.  
* **[Pendiente de validación] `InternLM3-20B-Chat`:** Candidato para Function Calling y estructuración JSON. Estas capacidades deben comprobarse localmente.  
* **[Pendiente de validación] `DeepSeek-Coder-V3-24B`:** Candidato para refactorizar código heredado o transcribir scripts entre lenguajes. La calidad y el consumo deben comprobarse localmente.

### 5.3. Categoría "Pesos Pesados" (25B a 28B)

*Propuesta LLaMA.cpp: Precisión alta bajo restricciones estrictas. Las pruebas de esta categoría deben utilizar contexto reducido y `-np 1`; el rendimiento con contextos largos debe medirse por separado debido al posible cuello de botella USB4.*

*Propuesta LM Studio: Uso analítico con cuantización `Q3_K_L` y contexto limitado. La velocidad y la paginación de memoria son estimaciones que deben comprobarse localmente.*

* **[Pendiente de validación] `Phi-4-Pro-27B` (Microsoft):** Candidato para problemas algorítmicos complejos y modelado de lógica de negocio. La calidad de generación debe comprobarse localmente.  
* **[Pendiente de validación] `gemma-4-26B-A4B-it`:** Candidato para refactorización profunda. Se propone `-fa off`, sujeto a validación local.  
* **[Pendiente de validación] `Qwen3.8-27B-Coder`:** Candidato para generación de aplicaciones web. La compatibilidad con Flash Attention y la latencia deben comprobarse localmente.  
* **[Pendiente de validación] `DeepSeek-Coder-V3-27B`:** Candidato para contexto profundo y auditorías de seguridad. La calidad y el rendimiento deben comprobarse localmente.  
* **[Pendiente de validación] `Llama-4-27B-Code-Instruct`:** Candidato para depuración de arquitecturas complejas. La calidad debe comprobarse localmente.

### 5.4. Categoría "El Jefe Final" (30B a 35B)

*Propuesta LLaMA.cpp: Capacidad extrema al límite físico. Se propone cuantización agresiva (`Q3_K_M`), contexto recortado (`-c 4096`) y `-np 1`; el desbordamiento de RAM y el rendimiento deben medirse con cada modelo. Uso previsto: analítico o por lotes.*

*Propuesta LM Studio: Capacidad extrema al límite físico de la máquina. Se propone limitar manualmente el "Context Length" a 4096 tokens y utilizar `Q3_K_M`; el resultado debe validarse localmente.*

* **[Pendiente de validación] `Qwen3-32B-Agentic-Coder`:** Candidato para flujos agénticos. El rendimiento y la utilidad deben comprobarse localmente considerando el cuello de botella USB4.  
* **[Pendiente de validación] `Codestral-2-35B-Instruct`:** Candidato para scripts Python y APIs REST. El consumo y el rendimiento deben comprobarse localmente.  
* **[Pendiente de validación] `DeepSeek-Coder-V3-33B`:** Candidato para matemáticas y algoritmos. La calidad y la latencia deben comprobarse localmente.  
* **[Pendiente de validación] `Llama-4-34B-Code-Instruct`:** Candidato para diseño de arquitecturas de software. La calidad debe comprobarse localmente.  
* **[Pendiente de validación] `Command-R-35B-v2` (Cohere):** Candidato para RAG local. La extracción de información y el consumo deben comprobarse localmente.

&nbsp;

## **6\. Guía de Búsqueda y Configuración de Modelos en Hugging Face (`huggingface.co/models`)**

Esta sección establece los criterios de búsqueda estandarizados para identificar, filtrar y seleccionar archivos GGUF en **Hugging Face** adaptados al caso de uso de programación en Python, análisis de datos (Pandas/Matplotlib) y a las limitaciones físicas de la arquitectura GEEKOM Mini IT13 \+ NVIDIA RTX 5060 Ti (16 GB VRAM sobre USB4).

### **6.1. Estrategia General de Búsqueda en Hugging Face**

Para localizar modelos compatibles en el repositorio oficial (`https://huggingface.co/models`), se deben aplicar los siguientes filtros de búsqueda general:

* **Filtro de Librería/Formato:** Buscar siempre el sufijo `GGUF` (ej. `Qwen2.5-Coder-32B-Instruct-GGUF` o creadores reconocidos como `lmstudio-community`, `unsloth`, `bartowski`, o `ggml-org`).  
* **Tipo de Tarea / Filtro izquierdo:** Seleccionar la etiqueta de arquitectura `text-generation` o `coding`.  
* **Criterio de Selección de Archivos (.gguf):** Evitar archivos monolíticos gigantes o cuantizaciones extremas no probadas (`Q2_K`, `IQ1_S`). Priorizar cuantizaciones del tipo `K-quant` (`Q4_K_M`, `Q6_K`) o cuantizaciones equilibradas de bajo tamaño (`Q3_K_L`, `Q3_K_M`).

### **6.2. Generalización por Categoría de Modelos**

#### **Categoría 1: "Punto Dulce" (10B a 15B Parámetros)**

* **Perfil de Búsqueda en Hugging Face:** Buscar modelos con nombres que contengan `11B`, `12B`, `14B` o `15B` orientados a *Instruct*, *Coder* o *Reasoning* (ej. `Phi-4`, `DeepSeek-Coder-14B`, `Qwen2.5-14B-Instruct`).  
* **Rango de Parámetros:** 10,000,000,000 a 15,000,000,000 parámetros.  
* **Cuantización Inicial Recomendada:** `Q6_K` (permite alta precisión con un tamaño estimado de \~11 GB a 13 GB). También se admite `Q8_0` si el modelo base es menor a 12B; ambas opciones requieren validación local.  
* **Configuración Adaptada al Hardware:**  
  * *VRAM Estimada:* 12 GB \- 13.5 GB (Cabe al 100% en los 16 GB de la eGPU).  
  * *Contexto Máximo Seguro:* 8192 tokens.  
  * *Parámetros LLaMA.cpp:* `-ngl 99 -fa on -lm none -c 8192 -np 4` (Soporta múltiples slots concurrentes gracias a su bajo consumo de memoria).  
  * *Comportamiento Esperado:* Máxima velocidad interactiva (\>30 t/s) y altísima velocidad de ingesta de prompt (\>1100 t/s). Cero paginación por USB4.

#### **Categoría 2: "Mediano-Pesado" (20B a 24B Parámetros)**

* **Perfil de Búsqueda en Hugging Face:** Buscar modelos con etiquetas `22B` o `24B` (ej. `Codestral-22B`, `DeepSeek-Coder-V2-Lite-Instruct` o equivalentes de la familia Llama/Mistral).  
* **Rango de Parámetros:** 20,000,000,000 a 24,000,000,000 parámetros.  
* **Cuantización Inicial Recomendada:** `Q4_K_M` (equilibrio propuesto de compresión; tamaño estimado de \~12.5 GB \- 14 GB, dejando espacio limitado para el caché de contexto). Evitar cuantizaciones `Q5_K` o superiores inicialmente y validar el consumo real.  
* **Configuración Adaptada al Hardware:**  
  * *VRAM Estimada:* 14.2 GB \- 14.8 GB (Apunta al límite superior del margen de seguridad de la VRAM de 16 GB).  
  * *Contexto Máximo Seguro:* 8192 tokens.  
  * *Parámetros LLaMA.cpp:* `-ngl 99 -fa on -lm none -c 8192 -np 1` (Se recomienda restringir a 1 slot concurrente si se emplean contextos de 8192 tokens completos).  
  * *Comportamiento Esperado:* Inferencia de grado empresarial (\~28 a 30 t/s) sin detonar tráfico a través de la interfaz USB4.

#### **Categoría 3: "Pesos Pesados" (25B a 28B Parámetros)**

* **Perfil de Búsqueda en Hugging Face:** Buscar modelos rotulados como `27B` (ej. `Gemma-2-27B-It`, `Gemma-2-27B` variantes de código).  
* **Rango de Parámetros:** 25,000,000,000 a 28,000,000,000 parámetros.  
* **Cuantización Inicial Recomendada:** `Q3_K_L` o `Q3_K_M` (cuantización agresiva de 3 bits con capas grandes preservadas; tamaño aproximado de \~13.5 GB a 15.5 GB). Requiere validación local.  
* **Configuración Adaptada al Hardware:**  
  * *VRAM Estimada:* 15.5 GB (Saturación total del búfer físico de la tarjeta gráfica).  
  * *Contexto Máximo Seguro:* Variable (Requiere limitar el contexto a 4096 o usar `llama-bench` con contextos cortos para evitar el cuello de botella del USB4).  
  * *Parámetros LLaMA.cpp:* `-ngl 99 -fa off -lm none -c 4096 -np 1` (*Nota Crítica:* En arquitecturas tipo Gemma-2, desactivar Flash Attention `-fa off` es obligatorio para evitar errores de memoria compartida CUDA).  
  * *Comportamiento Esperado:* Alto rendimiento computacional bruto de inferencia si el contexto es bajo (\~25 t/s), pero caída severa a un solo dígito de t/s si el caché KV excede la VRAM e hiper-ventila el ancho de banda USB4.

#### **Categoría 4: "El Jefe Final" (30B a 35B Parámetros)**

* **Perfil de Búsqueda en Hugging Face:** Buscar modelos etiquetados como `32B`, `33B` o `35B` (ej. `Qwen2.5-Coder-32B-Instruct`, `Command-R-35B`, `Codestral-35B`).  
* **Rango de Parámetros:** 30,000,000,000 a 35,000,000,000 parámetros.  
* **Cuantización Inicial Recomendada:** `Q3_K_M` o `Q3_K_S` (compresión pesada propuesta para intentar encajar el modelo base en \~14.5 GB \- 15.8 GB). Requiere validación local y puede producir desbordamiento hacia RAM.  
* **Configuración Adaptada al Hardware:**  
  * *VRAM Estimada:* 15.6 GB \- 15.9 GB (Límite físico absoluto de la máquina).  
  * *Contexto Máximo Seguro:* Estrictamente 4096 tokens (o menor) para mitigar el desbordamiento hacia la memoria compartida del sistema.  
  * *Parámetros LLaMA.cpp:* `-ngl 99 -fa on -lm none -c 4096 -np 1` (A diferencia de Gemma, Qwen sí admite Flash Attention encendido `-fa on`).  
  * *Comportamiento Esperado:* Uso operativo estrictamente asíncrono, analítico o por lotes (Batching). Se aceptan velocidades de desbordamiento de 2 a 8 t/s a cambio de la máxima profundidad de razonamiento abstracto y diseño algorítmico local.

&nbsp;
