# **Documento Maestro de Análisis, Auditoría y Línea Base de Rendimiento**

> **Control de línea base de la feature** — Estado inicial congelado el 11 de
> noviembre de 2026 en la rama `feat/gemma-4-26b-a4b-it-qat-gguf`. Este documento
> es la línea base documental viva para la evolución de la configuración de
> Gemma-4-26B-A4B-it-qat-GGUF. Los resultados y perfiles descritos a continuación
> son evidencia histórica y configuraciones candidatas; no constituyen todavía
> una aprobación definitiva de optimización. Las nuevas pruebas deberán añadir o
> actualizar resultados manteniendo la trazabilidad de parámetros, métricas y
> decisiones.

> Los requerimientos y el plan general de la feature se encuentran en
> [`Requerimientos_Feature_Gemma-4-26B-A4B-it-qat-GGUF.md`](Requerimientos_Feature_Gemma-4-26B-A4B-it-qat-GGUF.md).

## **Despliegue de Gemma-4-26B-A4B-it-qat-GGUF en Hardware Heterogéneo con llama.cpp Server**

Este documento consolida la investigación técnica, las auditorías de configuración y los resultados forenses derivados de la serie experimental de pruebas (Tests 1 al 5\) para la ejecución local del modelo multimodal Gemma 4 26B A4B en una estación de trabajo equipada con una GPU de gama media. Se establece aquí la línea base técnica y arquitectónica que rige el dimensionamiento de memoria, la decodificación especulativa multitoken y la orquestación del servidor de inferencia.

# **1\. Fundamentos Arquitectónicos y Plataforma de Ejecución**

El despliegue eficiente de modelos de lenguaje masivos en hardware con limitaciones de memoria gráfica demanda una comprensión precisa de las capas de hardware y software involucradas. La inferencia local no se limita a transferir tensores a la memoria de video; requiere una partición simbiótica entre la memoria de video dedicada (VRAM) y la memoria principal del sistema (RAM Host), aprovechando los canales del bus PCIe sin saturar su ancho de banda.

## **1.1 Especificaciones de la Plataforma de Hardware y Compilación**

Las pruebas experimentales se desarrollaron de manera controlada sobre una plataforma de hardware de consumo avanzado con soporte nativo para arquitecturas de aceleración gráfica modernas. El entorno del sistema quedó registrado en los registros de diagnóstico del servidor con los siguientes parámetros físicos:

- **Unidad de Procesamiento Gráfico (GPU):** NVIDIA GeForce RTX 5060 Ti con 16.283 MiB (16 GB) de memoria física GDDR7. La arquitectura identificada corresponde a la familia Blackwell (ARCHS \= 1200), con soporte de grafos de ejecución (USE_GRAPHS \= 1), cuantizaciones de atención acelerada (FA_QUANTS \= q4_0-q4_0, q8_0-q8_0, f16-f16, bf16-bf16) y aceleración nativa de coma flotante de 4 bits (BLACKWELL_NATIVE_FP4 \= 1). Al momento de la inicialización, el sistema reportó 15.172 MiB de VRAM libre antes de la carga de tensores.
- **Unidad Central de Procesamiento (CPU) y Memoria del Sistema:** Procesador de 13ª generación Intel Core i9-13900H con 14 núcleos físicos y 20 subprocesos lógicos asignados al pool de hilos de inferencia (n_threads \= 14, n_threads_batch \= 14). El sistema operativo gestiona 32.462 MiB (32 GB) de memoria RAM física del host, con una disponibilidad libre inicial oscilando entre 16.508 MiB y 18.268 MiB. La CPU cuenta con los conjuntos de instrucciones vectoriales SSE3, SSSE3, AVX, AVX2, F16C y FMA activos.
- **Binario del Servidor de Inferencia:** Ejecutable llama-server.exe build 12235 (identificador de commit 0a94a3f28), compilado bajo el entorno Microsoft Visual C++ (MSVC 19.51.36260.0) para arquitectura x64 con el runtime de CUDA 13.5.

## **1.2 Topología y Modelado de Pesos de Gemma-4-26B-A4B-it**

La arquitectura Gemma 4 desarrollada por Google DeepMind e implementada por Unsloth introduce una estructura de Mezcla de Expertos (MoE) diseñada específicamente para maximizar la capacidad de razonamiento minimizando el costo computacional por token generado:

- **Conteo Total de Parámetros:** El modelo cuenta con 25.230 millones de parámetros (25.23B) distribuidos a lo largo de 30 bloques de capas transformadoras (gemma4.block_count \= 30).
- **Parámetros Activos por Token:** A pesar de su escala nominal de 26B, el mecanismo de enrutamiento dinámico selecciona únicamente 8 expertos de un total de 128 por capa (n_expert \= 128, n_expert_used \= 8). Esto equivale a una activación efectiva de entre 3.800 y 4.000 millones de parámetros (A4B) por paso de decodificación, permitiendo velocidades de inferencia comparables a las de un modelo denso de 4B.
- **Cuantización QAT (Quantization-Aware Training):** Se utiliza la variante Unsloth Dynamic Smart Q4_0 (UD-Q4_K_XL), cuyo tamaño en disco es de 13,26 GiB con una densidad de 4,51 bits por peso (BPW). El entrenamiento consciente de cuantización previene la pérdida de precisión en tareas lógicas y de código, preservando la fidelidad de coma flotante de 16 bits.
- **Proyector Multimodal:** Se integra el codificador visual mmproj-BF16.gguf bajo la arquitectura gemma4v, con un tamaño de 1.139,46 MiB en precisión bfloat16. Este módulo requiere atención no causal y cuenta con una resolución nativa orientada a procesar hasta 1.120 tokens visuales por imagen.
- **Decodificador Especulativo Multi-Token Prediction (MTP):** Se despliega el modelo borrador auxiliar mtp-gemma-4-26B-A4B-it-Q4_0.gguf bajo la arquitectura gemma4-assistant, compuesto por 4 capas de predicción (gemma4-assistant.block_count \= 4\) y 419,71 millones de parámetros en cuantización BF16/Q4_0 (225,21 MiB en memoria gráfica). Este componente predice secuencias de tokens en paralelo para ser verificadas en un único paso por el modelo base.

# **2\. Auditoría Técnica Exhaustiva de Parámetros de Configuración**

El archivo de ejecución por lotes (.bat) orquesta una suite compleja de parámetros divididos entre el motor GGML, la infraestructura HTTP del servidor y los algoritmos de muestreo. A continuación, se examina formalmente cada parámetro empleado en las secuencias experimentales contrastándolo con la documentación oficial de llama.cpp HTTP Server y la ayuda de línea de comandos de llama-server.exe \-h.

## **2.1 Validación Formal de Parámetros de Línea de Comandos**

La siguiente matriz detalla la correspondencia exacta, los alias abreviados reconocidos, el comportamiento predeterminado del servidor y la función operativa de cada directiva presente en los scripts de prueba.

| Parámetro en Scripts         | Flag Oficial y Alias en \-h                              | Dominio / Categoría         | Comportamiento por Defecto | Validación Técnica y Función Operativa                                                                                           |
| :--------------------------- | :------------------------------------------------------- | :-------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| llama-server.exe             | _Binario Principal_                                      | Infraestructura             | N/A                        | Ejecutable optimizado con soporte de aceleración CUDA 13.5 y extensiones para arquitectura Blackwell.                            |
| \--model \<ruta\>.gguf       | \-m, \--model FNAME                                      | Parámetros Comunes          | Ninguno (Obligatorio)      | Carga los pesos del modelo base cuantizado UD-Q4_K_XL (25.23B parámetros).                                                       |
| \--mmproj \<ruta\>.gguf      | \-mm, \--mmproj FILE                                     | Servidor / Multimodal       | Deshabilitado              | Ruta al proyector de visión gemma4v en BF16 para capacidades de comprensión de imágenes.                                         |
| \--model-draft \<ruta\>.gguf | \-md, \--model-draft, \--spec-draft-model FNAME          | Decodificación Especulativa | Deshabilitado              | Carga los pesos del modelo borrador auxiliar MTP para aceleración predictiva.                                                    |
| \--spec-type draft-mtp       | \--spec-type \<tipos\>                                   | Decodificación Especulativa | default                    | Configura el esquema de decodificación especulativa optimizado para la predicción multitoken de Gemma 4\.                        |
| \--spec-draft-n-max N        | \--spec-draft-n-max N                                    | Decodificación Especulativa | 3                          | Techo de tokens que el modelo borrador puede especular por cada paso de validación del modelo principal.                         |
| \--flash-attn on             | \-fa, \--flash-attn on\|off\|auto                        | Parámetros Comunes          | auto                       | Fuerza el uso de kernels de Flash Attention optimizados en GPU para reducir el uso de memoria en contextos amplios.              |
| \--ubatch-size N             | \-ub, \--ubatch-size N                                   | Parámetros Comunes          | 512                        | Tamaño físico máximo de micro-lote. Determina la asignación de buffers de cómputo y el presupuesto de tokens para visión.        |
| \--gpu-layers all            | \-ngl, \--gpu-layers, \--n-gpu-layers N                  | Parámetros Comunes          | auto                       | Descarga las 31 capas estructurales base del modelo en los procesadores de la GPU (CUDA0).                                       |
| \--fit off                   | \-fit, \--fit on\|off                                    | Parámetros Comunes          | on                         | Desactiva el autoajuste heurístico de memoria, garantizando que el contexto de 128K no se comprima automáticamente.              |
| \-ncmoe N                    | \-ncmoe, \--n-cpu-moe N                                  | Parámetros Comunes          | 0 (Todo a VRAM)            | Mantiene los pesos MoE de las primeras N capas en la memoria RAM de la CPU, descargando las capas restantes (30 \- N) a la VRAM. |
| \--cache-idle-slots          | \--cache-idle-slots                                      | Servidor / Caché            | Habilitado si hay RAM      | Salva el estado de ranuras inactivas en el caché de contexto de la RAM principal para acelerar reanudaciones de tareas.          |
| \--reasoning on              | \-rea, \--reasoning on\|off\|auto                        | Servidor / Template         | auto                       | Activa la generación del canal de pensamiento estructurado definido en el chat template nativo de Gemma 4\.                      |
| \--ctx-size 131072           | \-c, \--ctx-size N                                       | Parámetros Comunes          | 0 (Leído del GGUF)         | Fija el tamaño de contexto en 128K tokens (131.072 posiciones), adaptando la ventana a capacidades extendidas.                   |
| \--temp 1.0                  | \--temp, \--temperature N                                | Muestreo (Sampling)         | 0.80                       | Temperatura de generación alineada con las especificaciones de ajuste de Google y Unsloth para Gemma 4\.                         |
| \--top-p 0.95                | \--top-p N                                               | Muestreo (_Sampling_)       | 0.95                       | Muestreo por núcleo (nucleus sampling) oficial recomendado para equilibrar creatividad y coherencia.                             |
| \--top-k 64                  | \--top-k N                                               | Muestreo (_Sampling_)       | 40                         | Límite superior de selección léxica recomendado por el equipo de investigación para modelos Gemma 4\.                            |
| \--parallel 1                | \-np, \--parallel N                                      | Servidor / Concurrencia     | \-1 (auto)                 | Asigna una única ranura monousuario para evitar la multiplicación de buffers KV masivos en la VRAM física.                       |
| \--log-verbosity 4           | \-lv, \--verbosity, \--log-verbosity N                   | Parámetros Comunes          | 3 (info)                   | Eleva el registro a nivel de traza detallada (trace), permitiendo capturar telemetría y perfiles de memoria.                     |
| \--cache-type-k q8_0         | \-ctk, \--cache-type-k TYPE                              | Parámetros Comunes          | f16                        | Cuantiza a 8 bits las claves del KV Cache principal, reduciendo a la mitad el consumo de memoria respecto a float16.             |
| \--cache-type-v q8_0         | \-ctv, \--cache-type-v TYPE                              | Parámetros Comunes          | f16                        | Cuantiza a 8 bits los valores del KV Cache principal. Requiere Flash Attention para operar en GPU.                               |
| \--cache-type-k-draft q8_0   | \-ctkd, \--cache-type-k-draft, \--spec-draft-type-k TYPE | Parámetros Comunes          | f16                        | Cuantiza a 8 bits las claves del KV Cache del modelo borrador MTP.                                                               |
| \--cache-type-v-draft q8_0   | \-ctvd, \--cache-type-v-draft, \--spec-draft-type-v TYPE | Parámetros Comunes          | f16                        | Cuantiza a 8 bits los valores del KV Cache del modelo borrador MTP.                                                              |
| \--alias Gemma-4-26B-A4B     | \-a, \--alias STRING                                     | Servidor / Enrutamiento     | N/A                        | Asigna el nombre público de identificación del modelo ante peticiones API compatibles con OpenAI.                                |

## **2.2 Diagnóstico de Compatibilidad en Entornos Windows Batch**

Durante la serie de pruebas se identificó una discrepancia sintáctica fundamental en los archivos de comandos por lotes de Windows (.bat / .cmd):

- **El Fallo del Carácter \# en Windows Batch:** En el Test 1, la línea inicial del script se definió como:

```sh
# This batch file is used to launch the Gemma-4-26B-A4B-it-qat-GGUF model with specific configurations.
```

A diferencia de los entornos Unix/Linux donde \# delimita comentarios, el intérprete de comandos de Windows (cmd.exe) intenta ejecutar el carácter \# como una instrucción o programa binario. Esto produjo la advertencia inmediata en el registro:
_'\#' is not recognized as an internal or external command, operable program or batch file._
Aunque llama-server.exe continuó su arranque en la siguiente línea, la sintaxis correcta en scripts Batch para Windows exige el uso de la directiva REM o el prefijo de etiqueta nula ::. A partir del Test 2, este error fue corregido mediante comentarios formales ::.

# **3\. Consolidación y Análisis Forense Comparativo de las Pruebas (Tests 1 al 5\)**

La serie de pruebas experimentales documenta una trayectoria metódica de optimización orientada a alcanzar el máximo rendimiento sostenido en tokens por segundo sin provocar inestabilidad en el controlador gráfico. Cada prueba aportó telemetría precisa sobre las interacciones entre los parámetros del servidor y el hardware.

## **3.1 Análisis Individual de las Pruebas Ejecutadas**

### **Test 1: Configuración Inicial, Borrador Extendido (n-max 6\) y Micro-lote Base**

- **Configuración Clave:** \-ncmoe 8, \--spec-draft-n-max 6, \--ubatch-size 512 (implícito), \--flash-attn activado automáticamente por el servidor al detectar cache-type-v q8_0.
- **Resultado del Servidor:** El servidor asignó 10.306,91 MiB a los tensores en CUDA0 y mantuvo 8 capas MoE en RAM host. Procesó un prompt masivo de 65.497 tokens alcanzando 376,97 tokens/s en evaluación de prompt (PP). La generación de salida de 5.387 tokens registró una velocidad media de **60,33 tokens/s**.
- **Comportamiento Especulativo:** La tasa de aceptación global fue de **85,11%** (4.504 tokens aceptados de 5.292 borradores) con una longitud media aceptada de **6,11 tokens por paso**. Sin embargo, la tasa de aceptación por posición fue decreciente: (0.948, 0.906, 0.875, 0.834, 0.790, 0.753). En la sexta posición, uno de cada cuatro tokens fue descartado.
- **Cuellos de Botella:** Aparición del error sintáctico '\#' en la consola. Advertencia de recorte de presupuesto de visión: cap image_max_tokens (original=1120) to 512 (n_ubatch \= 512).

### **Test 2: Corrección Sintáctica y Estabilización Predictiva (n-max 3\)**

- **Configuración Clave:** Corrección de cabecera a ::, reducción preventiva a \--spec-draft-n-max 3, \-ncmoe 8, \--ubatch-size 512 (implícito).
- **Resultado del Servidor:** Procesamiento limpio sin errores en cmd.exe. El prompt de 70.964 tokens se evaluó a **363,06 tokens/s** (generando 10 checkpoints de contexto intermedios). La generación de 5.285 tokens se sostuvo en **54,42 tokens/s**.
- **Comportamiento Especulativo:** La tasa de aceptación global se disparó al **93,93%** (3.900 aceptados de 4.152 generados), con una consistencia notablemente superior por posición: (0.967, 0.943, 0.908). Todas las predicciones del borrador mantuvieron una fiabilidad por encima del 90%.
- **Observación de Memoria:** La memoria VRAM final en CUDA0 registró 44 MiB libres, situando el hardware en el límite exacto de saturación física.

### **Test 3: El Fenómeno del Colapso por Paginado PCIe (VRAM Overflow)**

- **Configuración Clave:** Inclusión explícita de \--flash-attn on, elevación de \--ubatch-size 1120 para cubrir la resolución nativa de visión, manteniendo \-ncmoe 8 y \--spec-draft-n-max 3\.
- **Diagnóstico del Fallo de Rendimiento:** Al elevar ubatch-size a 1.120, el buffer de cómputo en CUDA0 creció de 826,64 MiB a **1.040,27 MiB** (+213,63 MiB) y el KV Cache para ventanas deslizantes SWA creció en \+79,68 MiB.
- **Impacto en el Sistema:** La memoria de video física de la RTX 5060 Ti se agotó por completo (0 MiB libres reportados en el log). El subsistema gráfico de Windows (WDDM) intervino paginando tensores activos a la memoria RAM compartida a través del bus PCIe.
- **Consecuencias en el Rendimiento:**
  - La velocidad de prompt (PP) para los 70.964 tokens cayó de 363,06 t/s a **51,09 tokens/s** (una pérdida del 86%).
  - La velocidad de generación (TG) se desplomó de 54,42 t/s a **6,04 tokens/s** (un colapso de rendimiento de \~9x).
  - El tiempo de generación para 5.469 tokens pasó de 1 minuto con 37 segundos a **15 minutos con 5 segundos**, totalizando una respuesta de **38 minutos con 15 segundos** (frente a menos de 5 minutos en el Test 2).

### **Test 4: La Solución Maestra (-ncmoe 9\) y Récord de Rendimiento**

- **Configuración Clave:** Incremento de \-ncmoe 8 a **\-ncmoe 9**, manteniendo \--ubatch-size 1120, \--flash-attn on y \--spec-draft-n-max 3\.
- **Mecanismo de Resolución:** Trasladar una única capa adicional de expertos MoE hacia la RAM del procesador redujo el tamaño de los tensores del modelo en CUDA0 de 10.306,91 MiB a **9.898,54 MiB**, liberando con exactitud matemática **408,37 MiB de VRAM**.
- **Resultados Históricos Registrados:** Al alojar el buffer de cómputo de 1.040,27 MiB íntegramente en la memoria de la tarjeta sin recurrir al bus PCIe, la velocidad de evaluación de prompt alcanzó su récord histórico: **555,25 tokens/s** (1,80 ms/token).
- **Generación y Multimodalidad:** La generación de texto se restableció a **52,42 tokens/s sostenidos** (5.513 tokens generados en 1 min 45 s). Las imágenes complejas se decodificaron en resolución completa en 858 ms y 1.069 ms sin recortes de tokens visuales, completando todo el flujo en solo **3 minutos y 52 segundos**.

### **Test 5: Margen de Resiliencia y Estabilidad en Producción (-ncmoe 10\)**

- **Configuración Clave:** Ajuste a **\-ncmoe 10**, manteniendo \--ubatch-size 1120, \--flash-attn on y \--spec-draft-n-max 3\.
- **Mecanismo y Asignación:** Se movieron 10 capas MoE a la RAM host (ocupando 4.479 MiB en memoria del sistema). El peso del modelo en VRAM descendió a **9.490,16 MiB** (liberando otros 408,38 MiB adicionales respecto al Test 4).
- **Evaluación de Rendimiento y Margen:** Al finalizar la tarea, la GPU reportó **344 MiB de VRAM física libre garantizada**. La evaluación de prompt se mantuvo en un nivel de alto rendimiento (**465,80 tokens/s**) y la generación alcanzó **48,85 tokens/s** (5.768 tokens generados), completando 76.732 tokens en 4 minutos y 30 segundos con un 93,24% de aceptación en el modelo borrador.

## **3.2 Matriz Comparativa Multidimensional Consolidada**

La siguiente tabla resume y contrasta las variables de configuración, el dimensionamiento de memoria y las métricas de velocidad extraídas directamente de los registros de telemetría de cada una de las pruebas.

| Dimensión Analizada             | Test 1 (Inicial)  | Test 2 (Estable Base) | Test 3 (Saturación PCIe) | Test 4 (Récord Óptimo)  | Test 5 (Resiliencia)  |
| :------------------------------ | :---------------- | :-------------------- | :----------------------- | :---------------------- | :-------------------- |
| **Cabecera de Script**          | Error \#          | Correcto ::           | Correcto ::              | Correcto ::             | Correcto ::           |
| **Capas MoE en CPU (-ncmoe)**   | 8 capas           | 8 capas               | 8 capas                  | **9 capas**             | **10 capas**          |
| **Capas MoE en GPU (CUDA0)**    | 22 capas          | 22 capas              | 22 capas                 | **21 capas**            | **20 capas**          |
| **Tamaño Micro-lote (-ub)**     | 512 (por defecto) | 512 (por defecto)     | 1.120 (explícito)        | **1.120 (explícito)**   | **1.120 (explícito)** |
| **Borrador Máximo (n-max)**     | 6 tokens          | 3 tokens              | 3 tokens                 | 3 tokens                | 3 tokens              |
| **Modelo en VRAM (CUDA0)**      | 10.306,91 MiB     | 10.306,91 MiB         | 10.306,91 MiB            | **9.898,54 MiB**        | **9.490,16 MiB**      |
| **Modelo en RAM Host (CPU)**    | 3.663,25 MiB      | 3.663,25 MiB          | 3.663,25 MiB             | **4.071,62 MiB**        | **4.479,00 MiB**      |
| **Buffer Cómputo GPU**          | 826,64 MiB        | 826,64 MiB            | 1.040,27 MiB             | 1.040,27 MiB            | 1.040,27 MiB          |
| **VRAM Libre al Cierre**        | \~44 MiB          | 44 MiB                | **0 MiB (Desbordada)**   | 0 MiB (Al límite)       | **344 MiB (Libres)**  |
| **Presupuesto Visión (mmproj)** | Recortado a 512   | Recortado a 512       | 1.120 (Completo)         | **1.120 (Completo)**    | **1.120 (Completo)**  |
| **Tokens del Prompt**           | 65.497 tokens     | 70.964 tokens         | 70.964 tokens            | 70.964 tokens           | 70.964 tokens         |
| **Velocidad Prompt (PP)**       | 376,97 t/s        | 363,06 t/s            | 51,09 t/s _(Paginado)_   | **555,25 t/s (Récord)** | 465,80 t/s            |
| **Tokens Generados**            | 5.387 tokens      | 5.285 tokens          | 5.469 tokens             | 5.513 tokens            | 5.768 tokens          |
| **Velocidad Generación (TG)**   | 60,33 t/s         | 54,42 t/s             | 6,04 t/s _(Paginado)_    | **52,42 t/s**           | 48,85 t/s             |
| **Tasa Aceptación MTP**         | 85,11%            | **93,93%**            | 92,13%                   | 92,86%                  | 93,24%                |
| **Tiempo de Generación**        | 1 min 29 s        | 1 min 37 s            | 15 min 05 s              | **1 min 45 s**          | 1 min 58 s            |
| **Tiempo Total del Flujo**      | 4 min 23 s        | 4 min 52 s            | 38 min 15 s              | **3 min 52 s (Mínimo)** | 4 min 30 s            |

# **4\. Desglose Anatómico del Consumo de Memoria (VRAM vs. RAM Host)**

El comportamiento de la inferencia heterogénea depende de la correcta distribución de cuatro estructuras de datos críticas: los tensores del modelo, las ranuras de KV Cache, los buffers de cómputo y los módulos auxiliares de visión y decodificación especulativa.

## **4.1 Mecánica y Partición de Pesos MoE mediante \-ncmoe**

En modelos densos tradicionales, la totalidad de los parámetros de una capa debe residir en el mismo dispositivo de cómputo. En arquitecturas de Mezcla de Expertos como Gemma 4 26B A4B, llama.cpp descompone los tensores de cada capa transformadora:

- **Capas Base y Atención:** Las matrices de proyección de atención y normalizaciones se mantienen íntegramente en la GPU (offloaded 31/31 layers to GPU).
- **Tensores MoE de Alimentación Hacia Adelante (FFN):** Cada bloque MoE consta de pares de tensores de compresión y proyección hacia los expertos. El comando \-ncmoe N ordena al servidor mapear los tensores de expertos de las primeras N capas en la memoria RAM del sistema (CPU_Mapped model buffer). A partir de los registros de carga, se evidencia que cada capa MoE adicional derivada a la CPU libera exactamente:

_136,13 MiB \+ 272,25 MiB ≈ 408,38 MiB de VRAM en CUDA0_
Esta propiedad permite ajustar con granularidad milimétrica el espacio libre en la tarjeta gráfica para dar cabida a buffers dinámicos de contexto o micro-lotes sin desperdiciar memoria.

## **4.2 Dimensionamiento de la Memoria de Contexto (KV Cache)**

La asignación de memoria para la ventana de contexto de 128K tokens (--ctx-size 131072\) se gestiona mediante dos tipos de atención en Gemma 4:

- **1\. Atención Completa (No-SWA):** Aplicada en 5 capas del modelo, asignando un total de 131.072 celdas. Con la cuantización \--cache-type-k q8_0 y \--cache-type-v q8_0, el buffer asignado en CUDA0 es de:

_K (q8_0): 680,00 MiB \+ V (q8_0): 680,00 MiB \= 1.360,00 MiB_

- **2\. Atención de Ventana Deslizante (SWA):** Aplicada en las 25 capas restantes. La longitud de la ventana es de 1.024 tokens.
  - Con ubatch-size 512, el buffer SWA requiere 1.536 celdas, ocupando **159,38 MiB** (79,69 MiB para K y 79,69 MiB para V).
  - Con ubatch-size 1120, el buffer SWA se expande a 2.304 celdas, ocupando **239,06 MiB** (119,53 MiB para K y 119,53 MiB para V).
- **3\. Caché del Modelo Borrador MTP:** Al disponer de un contexto de 131.072 tokens en 4 capas de predicción, su propio KV Cache cuantizado a q8_0 reserva:
  - Buffer no-SWA: **272,00 MiB** (136,00 MiB para K y 136,00 MiB para V).
  - Buffer SWA: **19,12 MiB** (9,56 MiB para K y 9,56 MiB para V).

## **4.3 Expansión del Buffer de Cómputo por Tamaño de Micro-lote (n_ubatch)**

El micro-lote define el número de tokens evaluados en paralelo en un grafo de ejecución CUDA único. Al pasar de 512 a 1.120:

- El buffer de cómputo en CUDA0 (sched_reserve compute buffer) escala de **826,64 MiB a 1.040,27 MiB** (+213,63 MiB).
- El buffer de cómputo en CPU Host escala de **151,53 MiB a 333,11 MiB** (+181,58 MiB).

El incremento combinado en VRAM entre el buffer de cómputo y el KV Cache ampliado fue de aproximadamente **293,31 MiB**, excediendo los 44 MiB libres que quedaban en el Test 2 y provocando el fallo de paginado en el Test 3\.

# **5\. Dinámica Algorítmica de la Decodificación Especulativa (MTP)**

La técnica Multi-Token Prediction (MTP) implementada mediante el flag \--spec-type draft-mtp constituye el motor principal de aceleración de generación, multiplicando por más de dos la velocidad estándar de decodificación.

## **5.1 Eficiencia y Tasa de Aceptación por Posición**

La viabilidad de la decodificación especulativa depende de la precisión del modelo borrador. Si un token predicho en la posición k es rechazado por el modelo base, todos los tokens subsiguientes (k+1, …, n) se descartan automáticamente, consumiendo cómputo de verificación sin aportar a la salida final. Los registros de telemetría muestran el siguiente desglose de probabilidades de acceptance empíricas por posición:

```
Test 1 (n-max 6): [P1: 94.8% | P2: 90.6% | P3: 87.5% | P4: 83.4% | P5: 79.0% | P6: 75.3%] -> Global: 85.11%
Test 2 (n-max 3): [P1: 96.7% | P2: 94.3% | P3: 90.8%] -> Global: 93.93%
Test 4 (n-max 3): [P1: 96.1% | P2: 92.9% | P3: 89.6%] -> Global: 92.86%
Test 5 (n-max 3): [P1: 96.4% | P2: 93.5% | P3: 89.8%] -> Global: 93.24%
```

## **5.2 Análisis Comparativo: n-max 3 frente a n-max 6**

- **Régimen de Generación de Código y Estructuras Repetitivas (n-max 6):** En tareas de código fuente (como el desarrollo del juego de Tetris en HTML/JavaScript registrado en el Test 1), la sintaxis es predecible. Esto permitió que n-max 6 alcanzara una velocidad punta de **60,33 tokens/s**, con una longitud de aceptación media de 6,11 tokens por paso. No obstante, en un 25% de las llamadas el sexto token resultó fallido, obligando al modelo base a recalcular.
- **Régimen Conversacional y de Razonamiento General (n-max 3):** Configurar el techo en 3 tokens proporciona un balance superior de consistencia. Con más del 90% de aceptación en todas las posiciones y una media de \~3,8 tokens aceptados por verificación, se evitan ciclos ociosos de cómputo y se asegura una velocidad fluida de entre **48 y 54 tokens/s**, ideal para sesiones prolongadas y tareas de razonamiento analítico.

# **6\. Línea Base y Guía de Despliegue en Producción**

Con base en la evidencia empírica acumulada, se establecen dos perfiles oficiales de despliegue listos para producción, diseñados específicamente para la arquitectura combinada **NVIDIA RTX 5060 Ti 16GB \+ Intel Core i9-13900H (32GB RAM)**.

## **6.1 Perfil A: Rendimiento Máximo Absoluto (Script Test 4\)**

Este perfil está destinado a maximizar la velocidad tanto en el prellenado de contexto como en la generación de texto. Debe utilizarse cuando la estación de trabajo opere como un servidor de inferencia dedicado, sin aplicaciones gráficas 3D o navegadores pesados con aceleración por hardware abiertos concurrentemente.

```sh
:: ==============================================================================
:: LÍNEA BASE DE PRODUCCIÓN: PERFIL RENDIMIENTO MÁXIMO
:: Modelo: Gemma-4-26B-A4B-it-qat-GGUF (UD-Q4_K_XL)
:: Hardware: NVIDIA GeForce RTX 5060 Ti 16GB (CUDA 13.5) + Intel i9-13900H
:: Parámetros destacados: -ncmoe 9 | --ubatch-size 1120 | --spec-draft-n-max 3
:: ==============================================================================
..\..\bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64\llama-server.exe ^
  --model ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf ^
  --mmproj ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\mmproj-BF16.gguf ^
  --model-draft ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\mtp-gemma-4-26B-A4B-it-Q4_0.gguf ^
  --spec-type draft-mtp ^
  --spec-draft-n-max 3 ^
  --flash-attn on ^
  --ubatch-size 1120 ^
  --gpu-layers all ^
  --fit off ^
  -ncmoe 9 ^
  --cache-idle-slots ^
  --reasoning on ^
  --ctx-size 131072 ^
  --temp 1.0 ^
  --top-p 0.95 ^
  --top-k 64 ^
  --parallel 1 ^
  --log-verbosity 4 ^
  --cache-type-k q8_0 ^
  --cache-type-v q8_0 ^
  --cache-type-k-draft q8_0 ^
  --cache-type-v-draft q8_0 ^
  --alias Gemma-4-26B-A4B
```

- **Métricas Esperadas:**
  - Evaluación de Prompt (PP): **\~550 tokens/s**.
  - Generación de Tokens (TG): **\~52 tokens/s**.
  - Consumo VRAM en CUDA0: \~12.549 MiB (ajustado al 100% de la capacidad utilizable sin desbordamiento).

## **6.2 Perfil B: Alta Resiliencia y Estabilidad de Entorno Compartido (Script Test 5\)**

Este perfil está diseñado para estaciones de trabajo de uso diario, donde coexisten herramientas de diseño, ventanas de navegador con múltiples pestañas y entornos de desarrollo. Al garantizar 344 MiB de holgura en VRAM, se elimina cualquier riesgo de que una demanda repentina de memoria de otra aplicación desencadene el paginado a RAM por PCIe.

```sh
:: ==============================================================================
:: LÍNEA BASE DE PRODUCCIÓN: PERFIL ALTA RESILIENCIA
:: Modelo: Gemma-4-26B-A4B-it-qat-GGUF (UD-Q4_K_XL)
:: Hardware: NVIDIA GeForce RTX 5060 Ti 16GB (CUDA 13.5) + Intel i9-13900H
:: Parámetros destacados: -ncmoe 10 | --ubatch-size 1120 | --spec-draft-n-max 3
:: ==============================================================================
..\..\bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64\llama-server.exe ^
  --model ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf ^
  --mmproj ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\mmproj-BF16.gguf ^
  --model-draft ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\mtp-gemma-4-26B-A4B-it-Q4_0.gguf ^
  --spec-type draft-mtp ^
  --spec-draft-n-max 3 ^
  --flash-attn on ^
  --ubatch-size 1120 ^
  --gpu-layers all ^
  --fit off ^
  -ncmoe 10 ^
  --cache-idle-slots ^
  --reasoning on ^
  --ctx-size 131072 ^
  --temp 1.0 ^
  --top-p 0.95 ^
  --top-k 64 ^
  --parallel 1 ^
  --log-verbosity 4 ^
  --cache-type-k q8_0 ^
  --cache-type-v q8_0 ^
  --cache-type-k-draft q8_0 ^
  --cache-type-v-draft q8_0 ^
  --alias Gemma-4-26B-A4B
```

- **Métricas Esperadas:**
  - Evaluación de Prompt (PP): **\~465 tokens/s**.
  - Generación de Tokens (TG): **\~48 tokens/s**.
  - Holgura de Seguridad VRAM: **\>340 MiB libres**.

## **6.3 Protocolo de Diagnóstico Rápido para Anomalías de Rendimiento**

Si en algún momento el rendimiento del servidor experimenta una caída repentina durante la operación, se debe aplicar el siguiente protocolo de diagnóstico:

- **1\. Monitoreo de la Velocidad de Prompt:** Si en solicitudes extensas (\>20.000 tokens) la velocidad cae por debajo de 100 tokens/s, verifique en el registro la asignación de memoria al cierre. Si el valor de memoria libre en CUDA0 es 0 MiB y el tiempo de evaluación se dispara, significa que una asignación externa forzó el paginado PCIe. La solución inmediata es cambiar de \-ncmoe 9 a \-ncmoe 10\.
- **2\. Revisión de Resoluciones de Imagen:** Si se requiere procesar imágenes panorámicas de ultra alta definición y el servidor advierte sobre el recorte a 512 tokens, confirme que \--ubatch-size 1120 esté activo en el comando de arranque.

**3\. Control del Presupuesto de Razonamiento:** Por defecto, el chat template asigna un presupuesto máximo de razonamiento (budget=2147483647). Para tareas breves o interfaces de chat donde no se requiera un desglose analítico extenso, se puede incorporar el flag \--reasoning-budget (por ejemplo, \--reasoning-budget 1024\) para restringir la longitud del pensamiento interno y acelerar la respuesta.

## Configuración candidata

| Perfil | Estado |
| --- | --- |
| `rendimiento` | `Estado: candidato` |
| `sin_especulativa` | `Estado: candidato` |
| `resiliencia` | `Estado: candidato` |

## Resultado medido

Ningún perfil cuenta todavía con un registro de medición que sostenga este estado.

## Configuración aprobada

Ningún perfil está aprobado.
