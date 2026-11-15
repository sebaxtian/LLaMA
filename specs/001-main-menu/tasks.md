# Tareas - SPEC-001

## Progreso

- [x] 4 de 4 tareas completadas.

## Tareas

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RNF-001`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `main.bat`.
- **Estimación:** 15 min.
- **Validación:** `main.bat` arranca sin error y resuelve la raíz con `%~dp0`.
- **Evidencia:** Reporte de validación de SPEC-001, matriz de trazabilidad, fila RNF-001: «arranca desde cualquier directorio»; dictamen CONVERGIDO.
- [x] Completada.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `main.bat`.
- **Estimación:** 30 min.
- **Validación:** con un `.bat` temporal en `src/`, `main.bat` lo lista en orden alfabético.
- **Evidencia:** Reporte de validación de SPEC-001, matriz de trazabilidad, fila RF-001: «lista `my test.bat` y `smoke_test.bat` en orden alfabético»; dictamen CONVERGIDO.
- [x] Completada.

### T-003

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-003`, `RF-004`.
- **Criterio de aceptación:** `CA-001`, `CA-003`.
- **Archivos:** `main.bat`.
- **Estimación:** 30 min.
- **Validación:** una entrada inválida muestra error y re-solicita; la opción de salir termina el script.
- **Evidencia:** Reporte de validación de SPEC-001, matriz de trazabilidad, filas RF-003 y RF-004: «la opción de salir está presente y termina» y «`abc` y `9` muestran "Opcion no valida" y re-solicitan»; dictamen CONVERGIDO.
- [x] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-002`, `RF-005`, `RF-006`, `RNF-002`, `CB-001`, `CB-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`, `CA-004`, `CA-005`.
- **Archivos:** `main.bat`.
- **Estimación:** 30 min.
- **Validación:** ejecuta el script elegido y retorna al menú; maneja `src/` vacío, nombres con espacios y código de salida distinto de cero.
- **Evidencia:** Reporte de validación de SPEC-001, matriz de trazabilidad, filas RF-002, RF-005, RF-006, RNF-002, CB-001, CB-002 y CB-003: «ejecuta el script del número seleccionado», «mensaje "No hay scripts disponibles" y solo salir» y «`my test.bat` se ejecuta con ruta citada»; dictamen CONVERGIDO.
- [x] Completada.

## Evidencia

- Prueba de humo con `src/smoke_test.bat`: listado, ejecución y retorno al menú.
- Prueba con `src/my test.bat` (espacios): ejecución correcta y propagación del código de salida 5.
- Prueba con entrada `abc` y `9` (fuera de rango): mensaje de opción no válida y re-solicitud.
- Prueba con `src/` sin `.bat`: mensaje informativo y solo opción de salida.