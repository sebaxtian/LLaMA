# Reporte de validación - SPEC-001

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/main-menu`.
- Script validado: `main.bat`.
- Herramientas: cmd.exe, Python 3.15.2.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| RF-001 | CA-001 | listado de `src/*.bat` | lista `my test.bat` y `smoke_test.bat` en orden alfabético | PASADO |
| RF-002 | CA-002 | `call` del script elegido | ejecuta el script del número seleccionado | PASADO |
| RF-003 | CA-001 | opción `[0] Salir` | la opción de salir está presente y termina | PASADO |
| RF-004 | CA-003 | entrada inválida | `abc` y `9` muestran "Opcion no valida" y re-solicitan | PASADO |
| RF-005 | CA-004 | `src/` sin `.bat` | mensaje "No hay scripts disponibles" y solo salir | PASADO |
| RF-006 | CA-005 | retorno al menú | el menú se vuelve a mostrar tras ejecutar | PASADO |
| RNF-001 | CA-001 | raíz con `%~dp0` | arranca desde cualquier directorio | PASADO |
| RNF-002 | CA-002 | verificación previa | comprueba existencia antes de `call` | PASADO |
| CB-001 | CA-004 | `src/` vacío | maneja `src/` sin `.bat` | PASADO |
| CB-002 | CA-002 | nombre con espacios | `my test.bat` se ejecuta con ruta citada | PASADO |
| CB-003 | CA-005 | código de salida distinto de cero | `my test.bat` con `exit /b 5` informa código 5 y retorna | PASADO |

## Brechas

- Ninguna.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos con evidencia PASADO).

## Aprobación

- [x] G4: - Approved by: Agent Sebaxtian (2026-11-12).