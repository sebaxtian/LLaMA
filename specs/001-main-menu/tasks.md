# Tareas - SPEC-001

## Progreso

- [ ] 0 de 4 tareas completadas.

## Tareas

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RNF-001`.
- **Archivos:** `main.bat`.
- **Estimación:** 15 min.
- **Validación:** `main.bat` arranca sin error y resuelve la raíz con `%~dp0`.
- [ ] Completada.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`.
- **Archivos:** `main.bat`.
- **Estimación:** 30 min.
- **Validación:** con un `.bat` temporal en `src/`, `main.bat` lo lista en orden alfabético.
- [ ] Completada.

### T-003

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-003`, `RF-004`.
- **Archivos:** `main.bat`.
- **Estimación:** 30 min.
- **Validación:** una entrada inválida muestra error y re-solicita; la opción de salir termina el script.
- [ ] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-002`, `RF-005`, `RF-006`, `RNF-002`, `CB-001`, `CB-002`, `CB-003`.
- **Archivos:** `main.bat`.
- **Estimación:** 30 min.
- **Validación:** ejecuta el script elegido y retorna al menú; maneja `src/` vacío, nombres con espacios y código de salida distinto de cero.
- [ ] Completada.