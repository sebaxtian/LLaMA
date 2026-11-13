# Clarificación - SPEC-002

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** la spec exigía doble modo de ejecución para `planner` y `coder`, pero no definía el valor de configuración.
- **Pregunta:** ¿se usa `mode: all` o `mode: subagent`?
- **Respuesta:** `mode: all`, para no romper los comandos `sdd-*` que los invocan como agentes primarios.
- **Decisión:** `mode: all` en `planner` y `coder`.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** la spec no definía el conjunto exacto de subagentes lanzables por `sdd`.
- **Pregunta:** ¿se permite `explore` además de `planner`, `coder` y `reviewer`?
- **Respuesta:** sí; `explore` es de solo lectura y sirve para reconocimiento del repositorio.
- **Decisión:** permitir `planner`, `coder`, `reviewer` y `explore`; denegar el resto.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** la spec no definía si `sdd` conserva ejecución de comandos en la terminal.
- **Pregunta:** ¿`sdd` puede ejecutar el validador determinista?
- **Respuesta:** sí, limitado al comando del validador.
- **Decisión:** regla `shell` acotada a `python tools\sdd\validate.py *`.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** la spec no definía cómo se demuestra la disponibilidad de subagentes, porque el validador no inspecciona `.opencode/`.
- **Pregunta:** ¿cómo se evidencia CA-001 y CA-002?
- **Respuesta:** verificación manual en la TUI del agente `sdd`, registrada en `tasks.md`.
- **Decisión:** evidencia manual documentada más la validación determinista del proyecto.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

Ninguno adicional; se conservan `CB-001`, `CB-002` y `CB-003`.

## Parches aplicados a spec.md

- [x] Precisado RNF-001 con el orden de reglas (generales antes de excepciones).
- [x] Añadido CB-003 (fallo del validador durante la verificación de compuerta).
- [x] Añadido CA-006 (comandos `sdd-*` siguen operando como primarios).
- [x] Añadido RF-007 (contexto mínimo en la solicitud al subagente).

## Decisiones de negocio

- El orquestador no redacta artefactos: delega en el agente especializado de cada etapa.
- Las compuertas siguen siendo humanas; la delegación no autoriza aprobaciones.
- `explore` se admite por su carácter de solo lectura.