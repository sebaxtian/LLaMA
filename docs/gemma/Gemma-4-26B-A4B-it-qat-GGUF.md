# **Documento Maestro de AnÃ¡lisis, AuditorÃ­a y LÃ­nea Base de Rendimiento**

> **Control de lÃ­nea base de la feature** â€” Estado inicial congelado el 11 de
> noviembre de 2026 en la rama `feat/gemma-4-26b-a4b-it-qat-gguf`. Este documento
> es la lÃ­nea base documental viva para la evoluciÃ³n de la configuraciÃ³n de
> Gemma-4-26B-A4B-it-qat-GGUF. Los resultados y perfiles descritos a continuaciÃ³n
> son evidencia histÃ³rica y configuraciones candidatas; no constituyen todavÃ­a
> una aprobaciÃ³n definitiva de optimizaciÃ³n. Las nuevas pruebas deberÃ¡n aÃ±adir o
> actualizar resultados manteniendo la trazabilidad de parÃ¡metros, mÃ©tricas y
> decisiones.

> Los requerimientos y el plan general de la feature se encuentran en
> [`Requerimientos_Feature_Gemma-4-26B-A4B-it-qat-GGUF.md`](Requerimientos_Feature_Gemma-4-26B-A4B-it-qat-GGUF.md).

## **Despliegue de Gemma-4-26B-A4B-it-qat-GGUF en Hardware HeterogÃ©neo con llama.cpp Server**

Este documento consolida la investigaciÃ³n tÃ©cnica, las auditorÃ­as de configuraciÃ³n y los resultados forenses derivados de la serie experimental de pruebas (Tests 1 al 5\) para la ejecuciÃ³n local del modelo multimodal Gemma 4 26B A4B en una estaciÃ³n de trabajo equipada con una GPU de gama media. Se establece aquÃ­ la lÃ­nea base tÃ©cnica y arquitectÃ³nica que rige el dimensionamiento de memoria, la decodificaciÃ³n especulativa multitoken y la orquestaciÃ³n del servidor de inferencia.

# **1\. Fundamentos ArquitectÃ³nicos y Plataforma de EjecuciÃ³n**

El despliegue eficiente de modelos de lenguaje masivos en hardware con limitaciones de memoria grÃ¡fica demanda una comprensiÃ³n precisa de las capas de hardware y software involucradas. La inferencia local no se limita a transferir tensores a la memoria de video; requiere una particiÃ³n simbiÃ³tica entre la memoria de video dedicada (VRAM) y la memoria principal del sistema (RAM Host), aprovechando los canales del bus PCIe sin saturar su ancho de banda.

## **1.1 Especificaciones de la Plataforma de Hardware y CompilaciÃ³n**

Las pruebas experimentales se desarrollaron de manera controlada sobre una plataforma de hardware de consumo avanzado con soporte nativo para arquitecturas de aceleraciÃ³n grÃ¡fica modernas. El entorno del sistema quedÃ³ registrado en los registros de diagnÃ³stico del servidor con los siguientes parÃ¡metros fÃ­sicos:

- **Unidad de Procesamiento GrÃ¡fico (GPU):** NVIDIA GeForce RTX 5060 Ti con 16.283 MiB (16 GB) de memoria fÃ­sica GDDR7. La arquitectura identificada corresponde a la familia Blackwell (ARCHS \= 1200), con soporte de grafos de ejecuciÃ³n (USE_GRAPHS \= 1), cuantizaciones de atenciÃ³n acelerada (FA_QUANTS \= q4_0-q4_0, q8_0-q8_0, f16-f16, bf16-bf16) y aceleraciÃ³n nativa de coma flotante de 4 bits (BLACKWELL_NATIVE_FP4 \= 1). Al momento de la inicializaciÃ³n, el sistema reportÃ³ 15.172 MiB de VRAM libre antes de la carga de tensores.
- **Unidad Central de Procesamiento (CPU) y Memoria del Sistema:** Procesador de 13Âª generaciÃ³n Intel Core i9-13900H con 14 nÃºcleos fÃ­sicos y 20 subprocesos lÃ³gicos asignados al pool de hilos de inferencia (n_threads \= 14, n_threads_batch \= 14). El sistema operativo gestiona 32.462 MiB (32 GB) de memoria RAM fÃ­sica del host, con una disponibilidad libre inicial oscilando entre 16.508 MiB y 18.268 MiB. La CPU cuenta con los conjuntos de instrucciones vectoriales SSE3, SSSE3, AVX, AVX2, F16C y FMA activos.
- **Binario del Servidor de Inferencia:** Ejecutable llama-server.exe build 12235 (identificador de commit 0a94a3f28), compilado bajo el entorno Microsoft Visual C++ (MSVC 19.51.36260.0) para arquitectura x64 con el runtime de CUDA 13.5.

## **1.2 TopologÃ­a y Modelado de Pesos de Gemma-4-26B-A4B-it**

La arquitectura Gemma 4 desarrollada por Google DeepMind e implementada por Unsloth introduce una estructura de Mezcla de Expertos (MoE) diseÃ±ada especÃ­ficamente para maximizar la capacidad de razonamiento minimizando el costo computacional por token generado:

- **Conteo Total de ParÃ¡metros:** El modelo cuenta con 25.230 millones de parÃ¡metros (25.23B) distribuidos a lo largo de 30 bloques de capas transformadoras (gemma4.block_count \= 30).
- **ParÃ¡metros Activos por Token:** A pesar de su escala nominal de 26B, el mecanismo de enrutamiento dinÃ¡mico selecciona Ãºnicamente 8 expertos de un total de 128 por capa (n_expert \= 128, n_expert_used \= 8). Esto equivale a una activaciÃ³n efectiva de entre 3.800 y 4.000 millones de parÃ¡metros (A4B) por paso de decodificaciÃ³n, permitiendo velocidades de inferencia comparables a las de un modelo denso de 4B.
- **CuantizaciÃ³n QAT (Quantization-Aware Training):** Se utiliza la variante Unsloth Dynamic Smart Q4_0 (UD-Q4_K_XL), cuyo tamaÃ±o en disco es de 13,26 GiB con una densidad de 4,51 bits por peso (BPW). El entrenamiento consciente de cuantizaciÃ³n previene la pÃ©rdida de precisiÃ³n en tareas lÃ³gicas y de cÃ³digo, preservando la fidelidad de coma flotante de 16 bits.
- **Proyector Multimodal:** Se integra el codificador visual mmproj-BF16.gguf bajo la arquitectura gemma4v, con un tamaÃ±o de 1.139,46 MiB en precisiÃ³n bfloat16. Este mÃ³dulo requiere atenciÃ³n no causal y cuenta con una resoluciÃ³n nativa orientada a procesar hasta 1.120 tokens visuales por imagen.
- **Decodificador Especulativo Multi-Token Prediction (MTP):** Se despliega el modelo borrador auxiliar mtp-gemma-4-26B-A4B-it-Q4_0.gguf bajo la arquitectura gemma4-assistant, compuesto por 4 capas de predicciÃ³n (gemma4-assistant.block_count \= 4\) y 419,71 millones de parÃ¡metros en cuantizaciÃ³n BF16/Q4_0 (225,21 MiB en memoria grÃ¡fica). Este componente predice secuencias de tokens en paralelo para ser verificadas en un Ãºnico paso por el modelo base.

# **2\. AuditorÃ­a TÃ©cnica Exhaustiva de ParÃ¡metros de ConfiguraciÃ³n**

El archivo de ejecuciÃ³n por lotes (.bat) orquesta una suite compleja de parÃ¡metros divididos entre el motor GGML, la infraestructura HTTP del servidor y los algoritmos de muestreo. A continuaciÃ³n, se examina formalmente cada parÃ¡metro empleado en las secuencias experimentales contrastÃ¡ndolo con la documentaciÃ³n oficial de llama.cpp HTTP Server y la ayuda de lÃ­nea de comandos de llama-server.exe \-h.

## **2.1 ValidaciÃ³n Formal de ParÃ¡metros de LÃ­nea de Comandos**

La siguiente matriz detalla la correspondencia exacta, los alias abreviados reconocidos, el comportamiento predeterminado del servidor y la funciÃ³n operativa de cada directiva presente en los scripts de prueba.

| ParÃ¡metro en Scripts         | Flag Oficial y Alias en \-h                              | Dominio / CategorÃ­a         | Comportamiento por Defecto | ValidaciÃ³n TÃ©cnica y FunciÃ³n Operativa                                                                                           |
| :--------------------------- | :------------------------------------------------------- | :-------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| llama-server.exe             | _Binario Principal_                                      | Infraestructura             | N/A                        | Ejecutable optimizado con soporte de aceleraciÃ³n CUDA 13.5 y extensiones para arquitectura Blackwell.                            |
| \--model \<ruta\>.gguf       | \-m, \--model FNAME                                      | ParÃ¡metros Comunes          | Ninguno (Obligatorio)      | Carga los pesos del modelo base cuantizado UD-Q4_K_XL (25.23B parÃ¡metros).                                                       |
| \--mmproj \<ruta\>.gguf      | \-mm, \--mmproj FILE                                     | Servidor / Multimodal       | Deshabilitado              | Ruta al proyector de visiÃ³n gemma4v en BF16 para capacidades de comprensiÃ³n de imÃ¡genes.                                         |
| \--model-draft \<ruta\>.gguf | \-md, \--model-draft, \--spec-draft-model FNAME          | DecodificaciÃ³n Especulativa | Deshabilitado              | Carga los pesos del modelo borrador auxiliar MTP para aceleraciÃ³n predictiva.                                                    |
| \--spec-type draft-mtp       | \--spec-type \<tipos\>                                   | DecodificaciÃ³n Especulativa | default                    | Configura el esquema de decodificaciÃ³n especulativa optimizado para la predicciÃ³n multitoken de Gemma 4\.                        |
| \--spec-draft-n-max N        | \--spec-draft-n-max N                                    | DecodificaciÃ³n Especulativa | 3                          | Techo de tokens que el modelo borrador puede especular por cada paso de validaciÃ³n del modelo principal.                         |
| \--flash-attn on             | \-fa, \--flash-attn on\|off\|auto                        | ParÃ¡metros Comunes          | auto                       | Fuerza el uso de kernels de Flash Attention optimizados en GPU para reducir el uso de memoria en contextos amplios.              |
| \--ubatch-size N             | \-ub, \--ubatch-size N                                   | ParÃ¡metros Comunes          | 512                        | TamaÃ±o fÃ­sico mÃ¡ximo de micro-lote. Determina la asignaciÃ³n de buffers de cÃ³mputo y el presupuesto de tokens para visiÃ³n.        |
| \--gpu-layers all            | \-ngl, \--gpu-layers, \--n-gpu-layers N                  | ParÃ¡metros Comunes          | auto                       | Descarga las 31 capas estructurales base del modelo en los procesadores de la GPU (CUDA0).                                       |
| \--fit off                   | \-fit, \--fit on\|off                                    | ParÃ¡metros Comunes          | on                         | Desactiva el autoajuste heurÃ­stico de memoria, garantizando que el contexto de 128K no se comprima automÃ¡ticamente.              |
| \-ncmoe N                    | \-ncmoe, \--n-cpu-moe N                                  | ParÃ¡metros Comunes          | 0 (Todo a VRAM)            | Mantiene los pesos MoE de las primeras N capas en la memoria RAM de la CPU, descargando las capas restantes (30 \- N) a la VRAM. |
| \--cache-idle-slots          | \--cache-idle-slots                                      | Servidor / CachÃ©            | Habilitado si hay RAM      | Salva el estado de ranuras inactivas en el cachÃ© de contexto de la RAM principal para acelerar reanudaciones de tareas.          |
| \--reasoning on              | \-rea, \--reasoning on\|off\|auto                        | Servidor / Template         | auto                       | Activa la generaciÃ³n del canal de pensamiento estructurado definido en el chat template nativo de Gemma 4\.                      |
| \--ctx-size 131072           | \-c, \--ctx-size N                                       | ParÃ¡metros Comunes          | 0 (LeÃ­do del GGUF)         | Fija el tamaÃ±o de contexto en 128K tokens (131.072 posiciones), adaptando la ventana a capacidades extendidas.                   |
| \--temp 1.0                  | \--temp, \--temperature N                                | Muestreo (Sampling)         | 0.80                       | Temperatura de generaciÃ³n alineada con las especificaciones de ajuste de Google y Unsloth para Gemma 4\.                         |
| \--top-p 0.95                | \--top-p N                                               | Muestreo (_Sampling_)       | 0.95                       | Muestreo por nÃºcleo (nucleus sampling) oficial recomendado para equilibrar creatividad y coherencia.                             |
| \--top-k 64                  | \--top-k N                                               | Muestreo (_Sampling_)       | 40                         | LÃ­mite superior de selecciÃ³n lÃ©xica recomendado por el equipo de investigaciÃ³n para modelos Gemma 4\.                            |
| \--parallel 1                | \-np, \--parallel N                                      | Servidor / Concurrencia     | \-1 (auto)                 | Asigna una Ãºnica ranura monousuario para evitar la multiplicaciÃ³n de buffers KV masivos en la VRAM fÃ­sica.                       |
| \--log-verbosity 4           | \-lv, \--verbosity, \--log-verbosity N                   | ParÃ¡metros Comunes          | 3 (info)                   | Eleva el registro a nivel de traza detallada (trace), permitiendo capturar telemetrÃ­a y perfiles de memoria.                     |
| \--cache-type-k q8_0         | \-ctk, \--cache-type-k TYPE                              | ParÃ¡metros Comunes          | f16                        | Cuantiza a 8 bits las claves del KV Cache principal, reduciendo a la mitad el consumo de memoria respecto a float16.             |
| \--cache-type-v q8_0         | \-ctv, \--cache-type-v TYPE                              | ParÃ¡metros Comunes          | f16                        | Cuantiza a 8 bits los valores del KV Cache principal. Requiere Flash Attention para operar en GPU.                               |
| \--cache-type-k-draft q8_0   | \-ctkd, \--cache-type-k-draft, \--spec-draft-type-k TYPE | ParÃ¡metros Comunes          | f16                        | Cuantiza a 8 bits las claves del KV Cache del modelo borrador MTP.                                                               |
| \--cache-type-v-draft q8_0   | \-ctvd, \--cache-type-v-draft, \--spec-draft-type-v TYPE | ParÃ¡metros Comunes          | f16                        | Cuantiza a 8 bits los valores del KV Cache del modelo borrador MTP.                                                              |
| \--alias Gemma-4-26B-A4B     | \-a, \--alias STRING                                     | Servidor / Enrutamiento     | N/A                        | Asigna el nombre pÃºblico de identificaciÃ³n del modelo ante peticiones API compatibles con OpenAI.                                |

## **2.2 DiagnÃ³stico de Compatibilidad en Entornos Windows Batch**

Durante la serie de pruebas se identificÃ³ una discrepancia sintÃ¡ctica fundamental en los archivos de comandos por lotes de Windows (.bat / .cmd):

- **El Fallo del CarÃ¡cter \# en Windows Batch:** En el Test 1, la lÃ­nea inicial del script se definiÃ³ como:

```sh
# This batch file is used to launch the Gemma-4-26B-A4B-it-qat-GGUF model with specific configurations.
```

A diferencia de los entornos Unix/Linux donde \# delimita comentarios, el intÃ©rprete de comandos de Windows (cmd.exe) intenta ejecutar el carÃ¡cter \# como una instrucciÃ³n o programa binario. Esto produjo la advertencia inmediata en el registro:
_'\#' is not recognized as an internal or external command, operable program or batch file._
Aunque llama-server.exe continuÃ³ su arranque en la siguiente lÃ­nea, la sintaxis correcta en scripts Batch para Windows exige el uso de la directiva REM o el prefijo de etiqueta nula ::. A partir del Test 2, este error fue corregido mediante comentarios formales ::.

# **3\. ConsolidaciÃ³n y AnÃ¡lisis Forense Comparativo de las Pruebas (Tests 1 al 5\)**

La serie de pruebas experimentales documenta una trayectoria metÃ³dica de optimizaciÃ³n orientada a alcanzar el mÃ¡ximo rendimiento sostenido en tokens por segundo sin provocar inestabilidad en el controlador grÃ¡fico. Cada prueba aportÃ³ telemetrÃ­a precisa sobre las interacciones entre los parÃ¡metros del servidor y el hardware.

## **3.1 AnÃ¡lisis Individual de las Pruebas Ejecutadas**

### **Test 1: ConfiguraciÃ³n Inicial, Borrador Extendido (n-max 6\) y Micro-lote Base**

- **ConfiguraciÃ³n Clave:** \-ncmoe 8, \--spec-draft-n-max 6, \--ubatch-size 512 (implÃ­cito), \--flash-attn activado automÃ¡ticamente por el servidor al detectar cache-type-v q8_0.
- **Resultado del Servidor:** El servidor asignÃ³ 10.306,91 MiB a los tensores en CUDA0 y mantuvo 8 capas MoE en RAM host. ProcesÃ³ un prompt masivo de 65.497 tokens alcanzando 376,97 tokens/s en evaluaciÃ³n de prompt (PP). La generaciÃ³n de salida de 5.387 tokens registrÃ³ una velocidad media de **60,33 tokens/s**.
- **Comportamiento Especulativo:** La tasa de aceptaciÃ³n global fue de **85,11%** (4.504 tokens aceptados de 5.292 borradores) con una longitud media aceptada de **6,11 tokens por paso**. Sin embargo, la tasa de aceptaciÃ³n por posiciÃ³n fue decreciente: (0.948, 0.906, 0.875, 0.834, 0.790, 0.753). En la sexta posiciÃ³n, uno de cada cuatro tokens fue descartado.
- **Cuellos de Botella:** ApariciÃ³n del error sintÃ¡ctico '\#' en la consola. Advertencia de recorte de presupuesto de visiÃ³n: cap image_max_tokens (original=1120) to 512 (n_ubatch \= 512).

### **Test 2: CorrecciÃ³n SintÃ¡ctica y EstabilizaciÃ³n Predictiva (n-max 3\)**

- **ConfiguraciÃ³n Clave:** CorrecciÃ³n de cabecera a ::, reducciÃ³n preventiva a \--spec-draft-n-max 3, \-ncmoe 8, \--ubatch-size 512 (implÃ­cito).
- **Resultado del Servidor:** Procesamiento limpio sin errores en cmd.exe. El prompt de 70.964 tokens se evaluÃ³ a **363,06 tokens/s** (generando 10 checkpoints de contexto intermedios). La generaciÃ³n de 5.285 tokens se sostuvo en **54,42 tokens/s**.
- **Comportamiento Especulativo:** La tasa de aceptaciÃ³n global se disparÃ³ al **93,93%** (3.900 aceptados de 4.152 generados), con una consistencia notablemente superior por posiciÃ³n: (0.967, 0.943, 0.908). Todas las predicciones del borrador mantuvieron una fiabilidad por encima del 90%.
- **ObservaciÃ³n de Memoria:** La memoria VRAM final en CUDA0 registrÃ³ 44 MiB libres, situando el hardware en el lÃ­mite exacto de saturaciÃ³n fÃ­sica.

### **Test 3: El FenÃ³meno del Colapso por Paginado PCIe (VRAM Overflow)**

- **ConfiguraciÃ³n Clave:** InclusiÃ³n explÃ­cita de \--flash-attn on, elevaciÃ³n de \--ubatch-size 1120 para cubrir la resoluciÃ³n nativa de visiÃ³n, manteniendo \-ncmoe 8 y \--spec-draft-n-max 3\.
- **DiagnÃ³stico del Fallo de Rendimiento:** Al elevar ubatch-size a 1.120, el buffer de cÃ³mputo en CUDA0 creciÃ³ de 826,64 MiB a **1.040,27 MiB** (+213,63 MiB) y el KV Cache para ventanas deslizantes SWA creciÃ³ en \+79,68 MiB.
- **Impacto en el Sistema:** La memoria de video fÃ­sica de la RTX 5060 Ti se agotÃ³ por completo (0 MiB libres reportados en el log). El subsistema grÃ¡fico de Windows (WDDM) intervino paginando tensores activos a la memoria RAM compartida a travÃ©s del bus PCIe.
- **Consecuencias en el Rendimiento:**
  - La velocidad de prompt (PP) para los 70.964 tokens cayÃ³ de 363,06 t/s a **51,09 tokens/s** (una pÃ©rdida del 86%).
  - La velocidad de generaciÃ³n (TG) se desplomÃ³ de 54,42 t/s a **6,04 tokens/s** (un colapso de rendimiento de \~9x).
  - El tiempo de generaciÃ³n para 5.469 tokens pasÃ³ de 1 minuto con 37 segundos a **15 minutos con 5 segundos**, totalizando una respuesta de **38 minutos con 15 segundos** (frente a menos de 5 minutos en el Test 2).

### **Test 4: La SoluciÃ³n Maestra (-ncmoe 9\) y RÃ©cord de Rendimiento**

- **ConfiguraciÃ³n Clave:** Incremento de \-ncmoe 8 a **\-ncmoe 9**, manteniendo \--ubatch-size 1120, \--flash-attn on y \--spec-draft-n-max 3\.
- **Mecanismo de ResoluciÃ³n:** Trasladar una Ãºnica capa adicional de expertos MoE hacia la RAM del procesador redujo el tamaÃ±o de los tensores del modelo en CUDA0 de 10.306,91 MiB a **9.898,54 MiB**, liberando con exactitud matemÃ¡tica **408,37 MiB de VRAM**.
- **Resultados HistÃ³ricos Registrados:** Al alojar el buffer de cÃ³mputo de 1.040,27 MiB Ã­ntegramente en la memoria de la tarjeta sin recurrir al bus PCIe, la velocidad de evaluaciÃ³n de prompt alcanzÃ³ su rÃ©cord histÃ³rico: **555,25 tokens/s** (1,80 ms/token).
- **GeneraciÃ³n y Multimodalidad:** La generaciÃ³n de texto se restableciÃ³ a **52,42 tokens/s sostenidos** (5.513 tokens generados en 1 min 45 s). Las imÃ¡genes complejas se decodificaron en resoluciÃ³n completa en 858 ms y 1.069 ms sin recortes de tokens visuales, completando todo el flujo en solo **3 minutos y 52 segundos**.

### **Test 5: Margen de Resiliencia y Estabilidad en ProducciÃ³n (-ncmoe 10\)**

- **ConfiguraciÃ³n Clave:** Ajuste a **\-ncmoe 10**, manteniendo \--ubatch-size 1120, \--flash-attn on y \--spec-draft-n-max 3\.
- **Mecanismo y AsignaciÃ³n:** Se movieron 10 capas MoE a la RAM host (ocupando 4.479 MiB en memoria del sistema). El peso del modelo en VRAM descendiÃ³ a **9.490,16 MiB** (liberando otros 408,38 MiB adicionales respecto al Test 4).
- **EvaluaciÃ³n de Rendimiento y Margen:** Al finalizar la tarea, la GPU reportÃ³ **344 MiB de VRAM fÃ­sica libre garantizada**. La evaluaciÃ³n de prompt se mantuvo en un nivel de alto rendimiento (**465,80 tokens/s**) y la generaciÃ³n alcanzÃ³ **48,85 tokens/s** (5.768 tokens generados), completando 76.732 tokens en 4 minutos y 30 segundos con un 93,24% de aceptaciÃ³n en el modelo borrador.

## **3.2 Matriz Comparativa Multidimensional Consolidada**

La siguiente tabla resume y contrasta las variables de configuraciÃ³n, el dimensionamiento de memoria y las mÃ©tricas de velocidad extraÃ­das directamente de los registros de telemetrÃ­a de cada una de las pruebas.

| DimensiÃ³n Analizada             | Test 1 (Inicial)  | Test 2 (Estable Base) | Test 3 (SaturaciÃ³n PCIe) | Test 4 (RÃ©cord Ã“ptimo)  | Test 5 (Resiliencia)  |
| :------------------------------ | :---------------- | :-------------------- | :----------------------- | :---------------------- | :-------------------- |
| **Cabecera de Script**          | Error \#          | Correcto ::           | Correcto ::              | Correcto ::             | Correcto ::           |
| **Capas MoE en CPU (-ncmoe)**   | 8 capas           | 8 capas               | 8 capas                  | **9 capas**             | **10 capas**          |
| **Capas MoE en GPU (CUDA0)**    | 22 capas          | 22 capas              | 22 capas                 | **21 capas**            | **20 capas**          |
| **TamaÃ±o Micro-lote (-ub)**     | 512 (por defecto) | 512 (por defecto)     | 1.120 (explÃ­cito)        | **1.120 (explÃ­cito)**   | **1.120 (explÃ­cito)** |
| **Borrador MÃ¡ximo (n-max)**     | 6 tokens          | 3 tokens              | 3 tokens                 | 3 tokens                | 3 tokens              |
| **Modelo en VRAM (CUDA0)**      | 10.306,91 MiB     | 10.306,91 MiB         | 10.306,91 MiB            | **9.898,54 MiB**        | **9.490,16 MiB**      |
| **Modelo en RAM Host (CPU)**    | 3.663,25 MiB      | 3.663,25 MiB          | 3.663,25 MiB             | **4.071,62 MiB**        | **4.479,00 MiB**      |
| **Buffer CÃ³mputo GPU**          | 826,64 MiB        | 826,64 MiB            | 1.040,27 MiB             | 1.040,27 MiB            | 1.040,27 MiB          |
| **VRAM Libre al Cierre**        | \~44 MiB          | 44 MiB                | **0 MiB (Desbordada)**   | 0 MiB (Al lÃ­mite)       | **344 MiB (Libres)**  |
| **Presupuesto VisiÃ³n (mmproj)** | Recortado a 512   | Recortado a 512       | 1.120 (Completo)         | **1.120 (Completo)**    | **1.120 (Completo)**  |
| **Tokens del Prompt**           | 65.497 tokens     | 70.964 tokens         | 70.964 tokens            | 70.964 tokens           | 70.964 tokens         |
| **Velocidad Prompt (PP)**       | 376,97 t/s        | 363,06 t/s            | 51,09 t/s _(Paginado)_   | **555,25 t/s (RÃ©cord)** | 465,80 t/s            |
| **Tokens Generados**            | 5.387 tokens      | 5.285 tokens          | 5.469 tokens             | 5.513 tokens            | 5.768 tokens          |
| **Velocidad GeneraciÃ³n (TG)**   | 60,33 t/s         | 54,42 t/s             | 6,04 t/s _(Paginado)_    | **52,42 t/s**           | 48,85 t/s             |
| **Tasa AceptaciÃ³n MTP**         | 85,11%            | **93,93%**            | 92,13%                   | 92,86%                  | 93,24%                |
| **Tiempo de GeneraciÃ³n**        | 1 min 29 s        | 1 min 37 s            | 15 min 05 s              | **1 min 45 s**          | 1 min 58 s            |
| **Tiempo Total del Flujo**      | 4 min 23 s        | 4 min 52 s            | 38 min 15 s              | **3 min 52 s (MÃ­nimo)** | 4 min 30 s            |

# **4\. Desglose AnatÃ³mico del Consumo de Memoria (VRAM vs. RAM Host)**

El comportamiento de la inferencia heterogÃ©nea depende de la correcta distribuciÃ³n de cuatro estructuras de datos crÃ­ticas: los tensores del modelo, las ranuras de KV Cache, los buffers de cÃ³mputo y los mÃ³dulos auxiliares de visiÃ³n y decodificaciÃ³n especulativa.

## **4.1 MecÃ¡nica y ParticiÃ³n de Pesos MoE mediante \-ncmoe**

En modelos densos tradicionales, la totalidad de los parÃ¡metros de una capa debe residir en el mismo dispositivo de cÃ³mputo. En arquitecturas de Mezcla de Expertos como Gemma 4 26B A4B, llama.cpp descompone los tensores de cada capa transformadora:

- **Capas Base y AtenciÃ³n:** Las matrices de proyecciÃ³n de atenciÃ³n y normalizaciones se mantienen Ã­ntegramente en la GPU (offloaded 31/31 layers to GPU).
- **Tensores MoE de AlimentaciÃ³n Hacia Adelante (FFN):** Cada bloque MoE consta de pares de tensores de compresiÃ³n y proyecciÃ³n hacia los expertos. El comando \-ncmoe N ordena al servidor mapear los tensores de expertos de las primeras N capas en la memoria RAM del sistema (CPU_Mapped model buffer). A partir de los registros de carga, se evidencia que cada capa MoE adicional derivada a la CPU libera exactamente:

_136,13 MiB \+ 272,25 MiB â‰ˆ 408,38 MiB de VRAM en CUDA0_
Esta propiedad permite ajustar con granularidad milimÃ©trica el espacio libre en la tarjeta grÃ¡fica para dar cabida a buffers dinÃ¡micos de contexto o micro-lotes sin desperdiciar memoria.

## **4.2 Dimensionamiento de la Memoria de Contexto (KV Cache)**

La asignaciÃ³n de memoria para la ventana de contexto de 128K tokens (--ctx-size 131072\) se gestiona mediante dos tipos de atenciÃ³n en Gemma 4:

- **1\. AtenciÃ³n Completa (No-SWA):** Aplicada en 5 capas del modelo, asignando un total de 131.072 celdas. Con la cuantizaciÃ³n \--cache-type-k q8_0 y \--cache-type-v q8_0, el buffer asignado en CUDA0 es de:

_K (q8_0): 680,00 MiB \+ V (q8_0): 680,00 MiB \= 1.360,00 MiB_

- **2\. AtenciÃ³n de Ventana Deslizante (SWA):** Aplicada en las 25 capas restantes. La longitud de la ventana es de 1.024 tokens.
  - Con ubatch-size 512, el buffer SWA requiere 1.536 celdas, ocupando **159,38 MiB** (79,69 MiB para K y 79,69 MiB para V).
  - Con ubatch-size 1120, el buffer SWA se expande a 2.304 celdas, ocupando **239,06 MiB** (119,53 MiB para K y 119,53 MiB para V).
- **3\. CachÃ© del Modelo Borrador MTP:** Al disponer de un contexto de 131.072 tokens en 4 capas de predicciÃ³n, su propio KV Cache cuantizado a q8_0 reserva:
  - Buffer no-SWA: **272,00 MiB** (136,00 MiB para K y 136,00 MiB para V).
  - Buffer SWA: **19,12 MiB** (9,56 MiB para K y 9,56 MiB para V).

## **4.3 ExpansiÃ³n del Buffer de CÃ³mputo por TamaÃ±o de Micro-lote (n_ubatch)**

El micro-lote define el nÃºmero de tokens evaluados en paralelo en un grafo de ejecuciÃ³n CUDA Ãºnico. Al pasar de 512 a 1.120:

- El buffer de cÃ³mputo en CUDA0 (sched_reserve compute buffer) escala de **826,64 MiB a 1.040,27 MiB** (+213,63 MiB).
- El buffer de cÃ³mputo en CPU Host escala de **151,53 MiB a 333,11 MiB** (+181,58 MiB).

El incremento combinado en VRAM entre el buffer de cÃ³mputo y el KV Cache ampliado fue de aproximadamente **293,31 MiB**, excediendo los 44 MiB libres que quedaban en el Test 2 y provocando el fallo de paginado en el Test 3\.

# **5\. DinÃ¡mica AlgorÃ­tmica de la DecodificaciÃ³n Especulativa (MTP)**

La tÃ©cnica Multi-Token Prediction (MTP) implementada mediante el flag \--spec-type draft-mtp constituye el motor principal de aceleraciÃ³n de generaciÃ³n, multiplicando por mÃ¡s de dos la velocidad estÃ¡ndar de decodificaciÃ³n.

## **5.1 Eficiencia y Tasa de AceptaciÃ³n por PosiciÃ³n**

La viabilidad de la decodificaciÃ³n especulativa depende de la precisiÃ³n del modelo borrador. Si un token predicho en la posiciÃ³n k es rechazado por el modelo base, todos los tokens subsiguientes (k+1, â€¦, n) se descartan automÃ¡ticamente, consumiendo cÃ³mputo de verificaciÃ³n sin aportar a la salida final. Los registros de telemetrÃ­a muestran el siguiente desglose de probabilidades de acceptance empÃ­ricas por posiciÃ³n:

```
Test 1 (n-max 6): [P1: 94.8% | P2: 90.6% | P3: 87.5% | P4: 83.4% | P5: 79.0% | P6: 75.3%] -> Global: 85.11%
Test 2 (n-max 3): [P1: 96.7% | P2: 94.3% | P3: 90.8%] -> Global: 93.93%
Test 4 (n-max 3): [P1: 96.1% | P2: 92.9% | P3: 89.6%] -> Global: 92.86%
Test 5 (n-max 3): [P1: 96.4% | P2: 93.5% | P3: 89.8%] -> Global: 93.24%
```

## **5.2 AnÃ¡lisis Comparativo: n-max 3 frente a n-max 6**

- **RÃ©gimen de GeneraciÃ³n de CÃ³digo y Estructuras Repetitivas (n-max 6):** En tareas de cÃ³digo fuente (como el desarrollo del juego de Tetris en HTML/JavaScript registrado en el Test 1), la sintaxis es predecible. Esto permitiÃ³ que n-max 6 alcanzara una velocidad punta de **60,33 tokens/s**, con una longitud de aceptaciÃ³n media de 6,11 tokens por paso. No obstante, en un 25% de las llamadas el sexto token resultÃ³ fallido, obligando al modelo base a recalcular.
- **RÃ©gimen Conversacional y de Razonamiento General (n-max 3):** Configurar el techo en 3 tokens proporciona un balance superior de consistencia. Con mÃ¡s del 90% de aceptaciÃ³n en todas las posiciones y una media de \~3,8 tokens aceptados por verificaciÃ³n, se evitan ciclos ociosos de cÃ³mputo y se asegura una velocidad fluida de entre **48 y 54 tokens/s**, ideal para sesiones prolongadas y tareas de razonamiento analÃ­tico.

# **6\. LÃ­nea Base y GuÃ­a de Despliegue en ProducciÃ³n**

Con base en la evidencia empÃ­rica acumulada, se establecen dos perfiles oficiales de despliegue listos para producciÃ³n, diseÃ±ados especÃ­ficamente para la arquitectura combinada **NVIDIA RTX 5060 Ti 16GB \+ Intel Core i9-13900H (32GB RAM)**.

## **6.1 Perfil A: Rendimiento MÃ¡ximo Absoluto (Script Test 4\)**

Este perfil estÃ¡ destinado a maximizar la velocidad tanto en el prellenado de contexto como en la generaciÃ³n de texto. Debe utilizarse cuando la estaciÃ³n de trabajo opere como un servidor de inferencia dedicado, sin aplicaciones grÃ¡ficas 3D o navegadores pesados con aceleraciÃ³n por hardware abiertos concurrentemente.

```sh
:: ==============================================================================
:: LÃNEA BASE DE PRODUCCIÃ“N: PERFIL RENDIMIENTO MÃXIMO
:: Modelo: Gemma-4-26B-A4B-it-qat-GGUF (UD-Q4_K_XL)
:: Hardware: NVIDIA GeForce RTX 5060 Ti 16GB (CUDA 13.5) + Intel i9-13900H
:: ParÃ¡metros destacados: -ncmoe 9 | --ubatch-size 1120 | --spec-draft-n-max 3
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

- **MÃ©tricas Esperadas:**
  - EvaluaciÃ³n de Prompt (PP): **\~550 tokens/s**.
  - GeneraciÃ³n de Tokens (TG): **\~52 tokens/s**.
  - Consumo VRAM en CUDA0: \~12.549 MiB (ajustado al 100% de la capacidad utilizable sin desbordamiento).

## **6.2 Perfil B: Alta Resiliencia y Estabilidad de Entorno Compartido (Script Test 5\)**

Este perfil estÃ¡ diseÃ±ado para estaciones de trabajo de uso diario, donde coexisten herramientas de diseÃ±o, ventanas de navegador con mÃºltiples pestaÃ±as y entornos de desarrollo. Al garantizar 344 MiB de holgura en VRAM, se elimina cualquier riesgo de que una demanda repentina de memoria de otra aplicaciÃ³n desencadene el paginado a RAM por PCIe.

```sh
:: ==============================================================================
:: LÃNEA BASE DE PRODUCCIÃ“N: PERFIL ALTA RESILIENCIA
:: Modelo: Gemma-4-26B-A4B-it-qat-GGUF (UD-Q4_K_XL)
:: Hardware: NVIDIA GeForce RTX 5060 Ti 16GB (CUDA 13.5) + Intel i9-13900H
:: ParÃ¡metros destacados: -ncmoe 10 | --ubatch-size 1120 | --spec-draft-n-max 3
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

- **MÃ©tricas Esperadas:**
  - EvaluaciÃ³n de Prompt (PP): **\~465 tokens/s**.
  - GeneraciÃ³n de Tokens (TG): **\~48 tokens/s**.
  - Holgura de Seguridad VRAM: **\>340 MiB libres**.

## **6.3 Protocolo de DiagnÃ³stico RÃ¡pido para AnomalÃ­as de Rendimiento**

Si en algÃºn momento el rendimiento del servidor experimenta una caÃ­da repentina durante la operaciÃ³n, se debe aplicar el siguiente protocolo de diagnÃ³stico:

- **1\. Monitoreo de la Velocidad de Prompt:** Si en solicitudes extensas (\>20.000 tokens) la velocidad cae por debajo de 100 tokens/s, verifique en el registro la asignaciÃ³n de memoria al cierre. Si el valor de memoria libre en CUDA0 es 0 MiB y el tiempo de evaluaciÃ³n se dispara, significa que una asignaciÃ³n externa forzÃ³ el paginado PCIe. La soluciÃ³n inmediata es cambiar de \-ncmoe 9 a \-ncmoe 10\.
- **2\. RevisiÃ³n de Resoluciones de Imagen:** Si se requiere procesar imÃ¡genes panorÃ¡micas de ultra alta definiciÃ³n y el servidor advierte sobre el recorte a 512 tokens, confirme que \--ubatch-size 1120 estÃ© activo en el comando de arranque.

**3\. Control del Presupuesto de Razonamiento:** Por defecto, el chat template asigna un presupuesto mÃ¡ximo de razonamiento (budget=2147483647). Para tareas breves o interfaces de chat donde no se requiera un desglose analÃ­tico extenso, se puede incorporar el flag \--reasoning-budget (por ejemplo, \--reasoning-budget 1024\) para restringir la longitud del pensamiento interno y acelerar la respuesta.
