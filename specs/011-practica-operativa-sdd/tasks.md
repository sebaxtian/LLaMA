# Tareas — SPEC-011

*Artefacto de rango 6: descomposición de `SPEC-011` en trece tareas atómicas con los ocho campos de la plantilla, dependencias acíclicas y cobertura completa de los requisitos y de los casos borde.*

## Regla de ejecución

La etapa modifica configuración de agentes, un flujo de integración continua, la documentación operativa y un módulo de pruebas. Se ejecuta con tres escritores y una revisión:

1. El rol `coder` escribe `tools/sdd/tests/test_agent_permissions.py` y el cierre de cada tarea de su alcance en `specs/011-practica-operativa-sdd/tasks.md`.
2. El `documenter` escribe `AGENTS.md`, conforme a la matriz del protocolo.
3. El orquestador redacta `.opencode/agents/*.md`, `opencode.jsonc`, `.github/workflows/sdd.yml` y `MEMORY.md` como delegado del propietario, porque la allowlist del `coder` no alcanza esas rutas. El propietario revisa el contenido antes de G4.
4. Las validaciones que requieren shell las ejecuta la sesión orquestadora y su salida literal se transcribe en el campo `Evidencia` de la tarea.
5. Una casilla se marca solo cuando la validación de la tarea se cumple. Una validación fallida obliga a corregir el archivo y a repetir la comprobación antes del registro.
6. Cada tarea de prueba se escribe en rojo antes de la tarea de configuración que la satisface; una tarea de prueba declara su caso negativo.
7. La etapa no modifica la base normativa, las specs publicadas, `tools/sdd/validate.py`, `tools/sdd/tests/test_validate.py`, `src/`, `models/` ni `bin/`. Una necesidad de cambio en esas rutas se registra como dependencia y no se ejecuta.

## Referencias

- `spec.md`: `SPEC-011`, versión 0.3.0, estado `planned`, compuerta G1 aprobada por `Agent Sebaxtian` en el commit firmado `5b0d7f1` (2026-11-14).
- `clarify.md`: cerrado con `AMB-001` a `AMB-008` resueltos, tres casos borde nuevos y once parches aplicados a `spec.md`.
- `plan.md`: arquitectura de cinco capas, procedimiento de resolución de permisos, contratos de rol, configuración, flujo y pruebas, diez decisiones `DEC-001` a `DEC-010` y matriz de cobertura de treinta y ocho filas.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §4 ciclo de siete etapas, §6 compuertas, §7 trazabilidad, §12 roles y permisos, §13 integración Git y §14 contrato del validador.
- Informe de origen: `docs/sdd/auditoria_cumplimiento_sdd.md`, bloque B3.

## Progreso

- Cerradas: 0 de 13 tareas.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_agent_permissions.py` | `T-001` a `T-004` | `coder` |
| 2 | `.opencode/agents/sdd.md`, `planner.md`, `coder.md`, `reviewer.md` y `documenter.md` | `T-005` | orquestador (delegado del propietario) |
| 3 | `.opencode/agents/auditor.md` | `T-006` | orquestador (delegado del propietario) |
| 4 | `opencode.jsonc` | `T-007` | orquestador (delegado del propietario) |
| 5 | `.github/workflows/sdd.yml` | `T-008` | orquestador (delegado del propietario) |
| 6 | `AGENTS.md` | `T-009` | `documenter` |
| 7 | `MEMORY.md` | `T-010` | orquestador (delegado del propietario) |
| 8 | `specs/011-practica-operativa-sdd/tasks.md` | cierre de cada tarea, `T-011`, `T-012` y `T-013` | `coder` para las casillas y el registro de evidencia |
| 9 | `specs/011-practica-operativa-sdd/validation_report.md` | inscripción de las cinco filas de hallazgo en la etapa Validate | `reviewer` |

`T-011`, `T-012` y `T-013` son tareas de verificación y de cierre: no producen archivos fuera de `tasks.md`.

## Orden de ejecución y dependencias

- Grupo 1 (pruebas que fallan): `T-001` sin dependencias; `T-002`, `T-003` y `T-004` dependen de `T-001`.
- Grupo 2 (configuración mínima): `T-005` depende de `T-001`; `T-006` depende de `T-005`; `T-007` depende de `T-002` y de `T-005`; `T-008` depende de `T-003`; `T-009` y `T-010` dependen de `T-004`.
- Grupo 3 (verificación y cierre): `T-011` depende de `T-005`, `T-006`, `T-007`, `T-008`, `T-009` y `T-010`; `T-012` depende de `T-011`; `T-013` depende de `T-012`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo.

## Tareas

### T-001: Pruebas de resolución de permisos y de la matriz de los seis roles

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-004`, `RF-005`, `RNF-003`, `RNF-004`, `RNF-005`, `CB-001`, `CB-002`, `CB-003`, `CB-005`, `CB-014`, `CB-015`, `CB-017`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-003`, `CA-004`, `CA-005`, `CA-006`, `CA-014`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -p "test_agent_permissions.py" -q` con las pruebas `test_seis_roles_declarados`, `test_contrato_de_entrada_de_permiso`, `test_denegacion_por_defecto`, `test_especificidad_prevalece`, `test_cero_conflictos_de_igual_especificidad`, `test_escritura_del_coder`, `test_escritura_unica_del_reviewer`, `test_auditor_solo_informes`, `test_auditor_no_aprueba`, `test_allowlist_de_shell`, `test_subagentes_por_rol` y `test_prueba_no_destructiva` en rojo; casos negativos `test_denegacion_prevalece_en_igual_especificidad` con un solapamiento sintético de igual especificidad y `test_auditor_solo_informes` con la ruta `docs/sdd/guia_operativa.md` denegada.
- **Evidencia:** `tasks.md` sin prueba ejecutada: la tarea abre en rojo y su salida se transcribe al cerrar.
- [ ] Completada.

### T-002: Pruebas de la configuración global y de la precedencia

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-011`, `RNF-006`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -p "test_agent_permissions.py" -q` con `test_configuracion_global` en rojo; caso negativo: un archivo sintético con una credencial literal en el encabezado produce el fallo de la prueba.
- **Evidencia:** `tasks.md` sin prueba ejecutada: la tarea abre en rojo y su salida se transcribe al cerrar.
- [ ] Completada.

### T-003: Pruebas de estructura y de límites del flujo de integración continua

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-006`, `RF-007`, `RNF-001`, `RNF-002`, `RNF-007`, `RNF-008`, `CB-006`, `CB-007`, `CB-016`.
- **Criterio de aceptación:** `CA-007`, `CA-008`, `CA-015`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -p "test_agent_permissions.py" -q` con `test_estructura_del_flujo` y `test_flujo_sin_efectos_remotos` en rojo; caso negativo: un flujo sintético con continuación en error y con una instrucción de push produce el fallo de las dos pruebas.
- **Evidencia:** `tasks.md` sin prueba ejecutada: la tarea abre en rojo y su salida se transcribe al cerrar.
- [ ] Completada.

### T-004: Pruebas de la documentación operativa

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `CB-012`.
- **Criterio de aceptación:** `CA-016`, `CA-017`, `CA-011`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -p "test_agent_permissions.py" -q` con `test_documentacion_operativa` en rojo; caso negativo: un texto sintético con 71 líneas útiles y con una mención de `main.bat` pendiente produce el fallo de la prueba.
- **Evidencia:** `tasks.md` sin prueba ejecutada: la tarea abre en rojo y su salida se transcribe al cerrar.
- [ ] Completada.

### T-005: Matriz de permisos, shell y subagentes en los cinco roles existentes

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-004`, `RF-005`, `CB-004`, `CB-005`, `CB-017`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-005`, `CA-006`, `CA-014`.
- **Archivos:** `.opencode/agents/sdd.md`, `.opencode/agents/planner.md`, `.opencode/agents/coder.md`, `.opencode/agents/reviewer.md`, `.opencode/agents/documenter.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -p "test_agent_permissions.py" -q` con las pruebas de los cinco roles en verde y `git status --short` sin cambios fuera de los cinco archivos declarados.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de la suite y la del estado del árbol de trabajo.
- [ ] Completada.

### T-006: Rol `auditor` con escritura limitada a los informes

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-003`, `RNF-005`, `CB-003`, `CB-014`, `CB-015`.
- **Criterio de aceptación:** `CA-003`, `CA-004`.
- **Archivos:** `.opencode/agents/auditor.md`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -p "test_agent_permissions.py" -q` con `test_auditor_solo_informes` y `test_auditor_no_aprueba` en verde, y `python tools\sdd\validate.py --all` con código de salida 0.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de la suite y la del validador.
- [ ] Completada.

### T-007: Configuración global y precedencia en `opencode.jsonc`

- **Dependencias:** `T-002`, `T-005`.
- **Requisitos cubiertos:** `RF-002`, `RF-011`, `RNF-006`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `opencode.jsonc`.
- **Estimación:** 20 min.
- **Validación:** `test_configuracion_global` en verde, `git diff --check` sin hallazgos y `git status --short` sin cambios fuera de `opencode.jsonc`; la comprobación es de lectura sobre el archivo y no escribe en el repositorio.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de la prueba y la del estado del árbol de trabajo.
- [ ] Completada.

### T-008: Flujo de integración continua

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-006`, `RF-007`, `RNF-001`, `RNF-002`, `RNF-007`, `RNF-008`, `CB-006`, `CB-007`, `CB-016`.
- **Criterio de aceptación:** `CA-007`, `CA-008`, `CA-015`.
- **Archivos:** `.github/workflows/sdd.yml`.
- **Estimación:** 30 min.
- **Validación:** `test_estructura_del_flujo` y `test_flujo_sin_efectos_remotos` en verde, ejecución local de los dos comandos del flujo con código de salida 0 y medición del tiempo de cada uno por debajo de su límite; `git status --short` sin cambios fuera de `.github/workflows/sdd.yml`.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de las dos pruebas y con el tiempo medido de cada paso.
- [ ] Completada.

### T-009: Mapa de agentes de `AGENTS.md`

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-012`.
- **Criterio de aceptación:** `CA-016`.
- **Archivos:** `AGENTS.md`.
- **Estimación:** 15 min.
- **Validación:** `test_documentacion_operativa` en verde, recuento de líneas útiles entre 30 y 70, mención del rol `auditor` en el mapa y `git diff --stat AGENTS.md` con variación neta de tres líneas como máximo.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de la prueba y el recuento de líneas.
- [ ] Completada.

### T-010: Lista de agentes e integración continua en `MEMORY.md`

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-013`, `CB-012`.
- **Criterio de aceptación:** `CA-017`, `CA-011`.
- **Archivos:** `MEMORY.md`.
- **Estimación:** 15 min.
- **Validación:** `test_documentacion_operativa` en verde, mención de los seis roles y de la integración continua, y contraste de cada hecho declarado con el estado del repositorio.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de la prueba y el contraste de hechos.
- [ ] Completada.

### T-011: Cierre de `AUD-081` a `AUD-084` y de `AUD-091`

- **Dependencias:** `T-005`, `T-006`, `T-007`, `T-008`, `T-009`, `T-010`.
- **Requisitos cubiertos:** `RF-008`, `RF-009`, `CB-008`, `CB-009`, `CB-010`, `CB-011`.
- **Criterio de aceptación:** `CA-009`, `CA-010`, `CA-011`.
- **Archivos:** `specs/011-practica-operativa-sdd/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** las cinco verificaciones de solo lectura con su salida literal y su código de salida: divergencia entre `dev` y `main` con salida `0 0`; listado de la referencia remota del release anterior sin resultados; listado de la rama Gemma con resultado local y verificación de su referencia remota sin resultado; estado del árbol de trabajo sobre `docs/sdd/` sin entradas; contraste de `MEMORY.md` sin hechos obsoletos. Una verificación cuyo hecho no se cumpla se registra como hallazgo abierto con el motivo.
- **Evidencia:** `tasks.md` sin verificación ejecutada: la tarea se cierra con la transcripción literal de las cinco salidas y de su código de salida.
- [ ] Completada.

### T-012: Regresión de la suite completa y del validador agregado

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RF-010`, `RNF-003`, `CB-013`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `specs/011-practica-operativa-sdd/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` con 111 pruebas en verde y `python tools\sdd\validate.py --all` con código de salida 0; el módulo de configuración completa en 60 segundos o menos y una segunda ejecución devuelve el mismo resultado.
- **Evidencia:** `tasks.md` sin validación ejecutada: la tarea se cierra con la salida de la suite, la del validador y el tiempo medido.
- [ ] Completada.

### T-013: Cierre de alcance y traspaso al `reviewer`

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-010`, `RNF-003`, `CB-013`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `specs/011-practica-operativa-sdd/tasks.md`.
- **Estimación:** 15 min.
- **Validación:** `git status --short` con las únicas rutas declaradas en la tabla de archivos de la etapa, el recuento de tareas cerradas igual a trece y la entrega al `reviewer` de la evidencia de `T-011` para inscribir las cinco filas de hallazgo en el reporte de validación.
- **Evidencia:** `tasks.md` sin cierre ejecutado: la tarea se cierra con la salida del estado del árbol de trabajo y la del recuento de progreso.
- [ ] Completada.
