---
name: llama-validation
description: Validación de scripts .bat y configuraciones de modelo para llama.cpp en Windows 11 con eGPU 16 GB VRAM.
---

# Validación de ejecuciones llama.cpp

Carga esta skill para validar scripts `.bat` y configuraciones de modelo.

## Reglas de script

- Resolver la raíz con `%~dp0`; no depender del directorio actual ni del `PATH`.
- Seleccionar explícitamente el ejecutable y el `.gguf`; verificar que existan antes de ejecutar.
- No asumir que `llama.exe` o el modelo están en el `PATH`.
- Mantener separados binarios precompilados (`bin/`) de artefactos de compilación.

## Parámetros iniciales por tamaño

- `-ngl 99`, `-lm none`.
- 10B–15B: `-c 8192`.
- 20B–24B: validar VRAM antes de contextos largos.
- 25B–28B: `-c 4096 -np 1`; Gemma con `-fa off`.
- 30B–35B: cuantización Q3, `-c 4096`, `-np 1`.

## Criterios de validación

Antes de declarar un script funcional u optimizado, comprobar:

- Ejecutable y modelo existen.
- Configuración corresponde al modelo.
- VRAM y RAM consumidas; desbordamiento a memoria compartida.
- Tokens por segundo.
- Versión concreta de llama.cpp.

`llama-bench` no sustituye la validación de un servidor con contexto largo.
