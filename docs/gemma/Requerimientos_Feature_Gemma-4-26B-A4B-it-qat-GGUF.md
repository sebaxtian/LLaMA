# Requerimientos base de la feature Gemma-4-26B-A4B-it-qat-GGUF

## 1. Propósito

Este documento define el alcance inicial, los requerimientos y el plan de trabajo
para desarrollar iterativamente la configuración de ejecución local del modelo
`Gemma-4-26B-A4B-it-qat-GGUF`.

La feature permanecerá abierta hasta que el propietario confirme que la
configuración es satisfactoria para su caso de uso. La optimización no se
considerará definitiva únicamente por los resultados históricos ya documentados.

El documento específico:

```text
docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md
```

es la línea base documental viva de la feature y deberá evolucionar conforme se
realicen nuevas pruebas, mediciones y decisiones de configuración.

## 2. Plataforma objetivo

- Sistema operativo: Windows 11.
- GPU: NVIDIA RTX 5060 Ti con 16 GB de VRAM.
- Conexión de GPU: eGPU mediante USB4.
- CPU: Intel Core i9 de 13.ª generación.
- Memoria del sistema: aproximadamente 32 GB de RAM.
- Backend: CUDA 13.5.
- Motor de inferencia: `llama-server.exe` de llama.cpp.
- Caso de uso: programación en Python, análisis de datos y arquitectura de
  software.

## 3. Alcance de la feature

La feature comprende:

1. Preparar una rama de trabajo independiente desde `dev`.
2. Congelar el estado actual como línea base histórica.
3. Revisar y corregir el script de ejecución del modelo.
4. Validar rutas, dependencias, compatibilidad y ejecución real.
5. Experimentar iterativamente con memoria, contexto, micro-lote, Flash
   Attention y decodificación especulativa.
6. Registrar en la documentación específica cada prueba y decisión.
7. Mantener separadas las configuraciones candidatas, los resultados medidos y
   la configuración finalmente aprobada.

No forma parte de esta fase inicial:

- Modificar archivos dentro de `llama.cpp/`.
- Versionar modelos GGUF, binarios, DLL o dependencias locales.
- Actualizar `CHANGELOG.md`, `README.md` o el documento maestro de benchmarks.
- Declarar una configuración como optimizada definitiva.

Estos cambios se realizarán únicamente al cierre de la feature, después de la
confirmación expresa del propietario.

## 4. Artefactos locales esperados

El modelo requiere los siguientes archivos locales, que deben permanecer fuera
del control de versiones:

- Modelo principal `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`.
- Proyector multimodal `mmproj-BF16.gguf`.
- Modelo draft MTP `mtp-gemma-4-26B-A4B-it-Q4_0.gguf`.
- Ejecutable local `llama-server.exe` y sus dependencias.

## 5. Fases y tareas de trabajo

### Fase 1: Preparación de la rama y línea base

#### Tarea 1. Crear la rama de trabajo

Crear exactamente desde `dev` la rama:

```text
feat/gemma-4-26b-a4b-it-qat-gguf
```

Los archivos locales existentes deben conservarse y no deben incorporarse
modelos, binarios ni contenido de `llama.cpp`.

#### Tarea 2. Congelar la línea base inicial

Registrar el estado inicial de:

- Rama, commit de origen y estado del árbol Git.
- Script actual de ejecución.
- Documento específico de Gemma 4.
- Modelo principal, `mmproj` y modelo draft disponibles localmente.
- Binario de `llama-server` utilizado.
- Versión o commit de llama.cpp asociado.
- Configuración histórica documentada.
- Resultados experimentales existentes.
- Riesgos, limitaciones y tareas pendientes.

Esta tarea se registra mediante el primer commit histórico de la feature.

### Fase 2: Corrección estructural del script

3. Resolver las rutas mediante `%~dp0` y variables explícitas.
4. Validar la existencia del ejecutable, modelo principal, `mmproj` y modelo
   draft antes de iniciar.
5. Revisar todos los parámetros frente al binario real, la arquitectura Gemma 4
   y las restricciones del proyecto.

### Fase 3: Validación funcional inicial

6. Confirmar la carga correcta de todos los componentes.
7. Confirmar que las opciones utilizadas son aceptadas por el binario real.
8. Ejecutar una prueba controlada textual y, cuando corresponda, multimodal.

### Fase 4: Optimización iterativa

9. Definir métricas comunes para todas las pruebas.
10. Comparar perfiles de `-ncmoe`, inicialmente `9` y `10`.
11. Comparar contexto y tamaños de micro-lote.
12. Evaluar `draft-mtp` y `--spec-draft-n-max`.
13. Evaluar `--flash-attn on/off` cuando la comparación sea válida.
14. Comprobar el impacto de `-lm none` si el objetivo es evitar mmap.

### Fase 5: Evolución documental

15. Actualizar el documento específico después de cada prueba relevante.
16. Separar hechos medidos, hipótesis, configuraciones candidatas y decisiones.
17. Mantener un historial de configuraciones descartadas y motivos.

### Fase 6: Cierre posterior

Esta fase solo comenzará cuando el propietario confirme que está satisfecho:

18. Consolidar la configuración final.
19. Registrar los resultados finales.
20. Actualizar `CHANGELOG.md` bajo `Unreleased`.
21. Actualizar `README.md`.
22. Actualizar el documento maestro de benchmarks.
23. Ejecutar las validaciones finales y preparar la integración de la rama.

## 6. Métricas mínimas por prueba

Cada prueba relevante debe registrar, cuando esté disponible:

- Fecha y nombre de la prueba.
- Versión del binario y commit de llama.cpp.
- Modelo y cuantización utilizados.
- Contexto configurado.
- Número de slots.
- Valor de `-ncmoe`.
- Tamaño de `ubatch`.
- Estado de Flash Attention.
- Configuración de speculative decoding.
- Tiempo de carga.
- VRAM utilizada y libre.
- RAM utilizada.
- Velocidad de prompt y generación en tokens por segundo.
- Estabilidad del servidor.
- Desbordamiento o paginación hacia memoria compartida.
- Calidad funcional de la respuesta.
- Errores, advertencias y observaciones.

`llama-bench` no sustituye la validación del servidor con contexto largo.

## 7. Criterios de validación

Antes de considerar aprobada una configuración se debe comprobar:

- Que el ejecutable y todos los modelos requeridos existan.
- Que el script funcione desde cualquier directorio.
- Que las opciones sean compatibles con el binario real.
- Que la cuantización corresponda al archivo utilizado.
- Que la carga textual y multimodal funcione cuando aplique.
- Que el consumo de VRAM y RAM sea conocido.
- Que no exista desbordamiento no documentado hacia memoria compartida.
- Que el rendimiento sea adecuado al caso de uso, no solo máximo en una prueba
  aislada.
- Que la versión concreta de llama.cpp quede registrada.

## 8. Estado inicial y regla de evolución

La documentación histórica existente en
`docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md` constituye el punto de partida,
pero sus perfiles son configuraciones históricas candidatas. La configuración
actual no debe considerarse definitiva hasta repetir las validaciones necesarias
con el binario y los archivos locales disponibles.

Cada cambio posterior deberá preservar la trazabilidad entre configuración,
medición, conclusión y siguiente tarea. La feature continuará abierta hasta la
aprobación explícita del propietario.
