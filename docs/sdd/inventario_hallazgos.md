# Inventario de hallazgos

Registro sin rango del corpus: documento de referencia no normativo que conserva 1 fila por hallazgo `AUD-NNN` emitido por los 5 informes de auditoría de `docs/sdd/`, conforme a `RF-011` de `SPEC-016`. No fija reglas, no sustituye al rol de auditoría y se apoya en la tabla de autoridad de `docs/sdd/README.md`.

## 1. Objeto

El documento reúne en una sola tabla los 82 identificadores que los 5 informes de auditoría del corpus emitieron, con los 8 campos obligatorios de `RF-011`, el estado que declara el informe más reciente y la evidencia de cierre por ruta y línea. La tabla de cierre de §5 registra los 16 hallazgos del corte de `SPEC-016` con su artefacto y su evidencia, y el anexo de §6 registra el juicio sin regla citada fuera del recuento de hallazgos.

## 2. Derivación y convenciones

- **Fuente.** Los 5 informes de origen y su fecha de corte: `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14), `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14), `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14), `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) y `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21).
- **Extracción.** El conjunto se obtiene de la primera celda de cada fila de tabla de los 5 informes, que porta el identificador `AUD-NNN`. El corte produce 82 identificadores distintos, sin reutilización y sin renumeración; 1 identificador ya emitido conserva su número aunque el informe posterior le declare un estado nuevo.
- **Orden de corte.** El estado de una fila es el que declara el informe más reciente de la serie en el orden anterior. La regla tiene 2 excepciones declaradas: las 5 exenciones históricas, que pasan a `cerrado por ratificación` con el acta del propietario en `docs/sdd/ratificacion_historica.md`, y los 11 hallazgos del corte, que se declaran `cerrado` solo cuando el artefacto consta, conforme a `CB-001`.
- **Vocabulario cerrado del estado.** El campo `Estado` admite 5 valores: `cerrado`, `parcial`, `vigente`, `cerrado por exención` y `cerrado por ratificación`. Son estados cerrados `cerrado` y `cerrado por ratificación`; son estados abiertos `parcial`, `vigente` y `cerrado por exención`.
- **Cita normativa.** El campo `Regla normativa citada` usa la forma `ruta §capítulo:línea` de §16 del protocolo. La constitución de rango 1 (§1 a §10) y el protocolo de rango 3 (§1 a §16) son las 2 normas de la base con capítulos numerados, de modo que la cita se ancla en la norma de rango 1 o de rango 3 que el hallazgo incumple; el informe de origen suele citarla como `ruta:línea`, sin capítulo.
- **Evidencia.** El campo `Evidencia de cierre` transcribe la primera ruta y línea que el informe declara como evidencia del cierre, o el identificador del commit firmado que ratifica. Cuando el artefacto es código, la línea corresponde al corte del informe que la transcribe y el campo `Informe que declara el estado` identifica ese informe.
- **Identificador del documento.** Este registro consta en la tabla de inventario de `docs/sdd/README.md` con el orden de lectura 36 y el rango «Sin rango».
- **Acta de ratificación.** El acta `docs/sdd/ratificacion_historica.md` consta en la tabla de inventario de `docs/sdd/README.md` con el orden de lectura 38 y el rango «Sin rango»; su ratificación se firmó en el commit `9042ae6` y su efecto consta en §5.

## 3. Composición de los cuatro bloques

- **Bloque 1.** Dimensiones D1 a D5 de `docs/sdd/auditoria_cumplimiento_sdd.md`: `AUD-001` a `AUD-007`, `AUD-011` a `AUD-014`, `AUD-021` a `AUD-023`, `AUD-031` a `AUD-035` y `AUD-041` a `AUD-044`. 23 filas.
- **Bloque 2.** Dimensiones D6 a D10 de `docs/sdd/auditoria_cumplimiento_sdd.md`: `AUD-051` a `AUD-055`, `AUD-061` a `AUD-064`, `AUD-071`, `AUD-072`, `AUD-081` a `AUD-084`, `AUD-091`, `AUD-093` y `AUD-094`. 18 filas.
- **Bloque 3.** 16 hallazgos de `docs/sdd/auditoria_cierre_v0_7_0.md` y 7 de `docs/sdd/auditoria_final_v0_7_0.md`: `AUD-008`, `AUD-015`, `AUD-024`, `AUD-036`, `AUD-037`, `AUD-038`, `AUD-045`, `AUD-046`, `AUD-056`, `AUD-065`, `AUD-066`, `AUD-067`, `AUD-073`, `AUD-074`, `AUD-075`, `AUD-085`, `AUD-086`, `AUD-095`, `AUD-096`, `AUD-097`, `AUD-098`, `AUD-101` y `AUD-102`. 23 filas.
- **Bloque 4.** 10 hallazgos de `docs/sdd/auditoria_posterior_v0_7_0.md` y 8 de `docs/sdd/auditoria_final_v0_7_1.md`: `AUD-039`, `AUD-057`, `AUD-068`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-099`, `AUD-100`, `AUD-103`, `AUD-104`, `AUD-105`, `AUD-106`, `AUD-107`, `AUD-108`, `AUD-109` y `AUD-110`. 18 filas.

## 4. Tabla de hallazgos

La tabla es única y continua, porque la comprobación lee la primera tabla de la sección. El orden sigue los cuatro bloques de §3 y, dentro de cada bloque, el identificador ascendente. 82 filas para 82 identificadores.

| Identificador | Dimensión | Severidad | Informe de origen | Regla normativa citada | Estado | Evidencia de cierre | Informe que declara el estado |
|---|---|---|---|---|---|---|---|
| `AUD-001` | D1 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §6:59` | cerrado | `docs/sdd/README.md:24` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-002` | D1 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §6:54` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:33` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-003` | D1 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §6:66` | cerrado por ratificación | acta `docs/sdd/ratificacion_historica.md:21-27` con los commits ratificados `494db2e` y `564bac4`, firmada en el commit `9042ae6` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14), elevado por el acta |
| `AUD-004` | D1 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §9:222` | cerrado por ratificación | acta `docs/sdd/ratificacion_historica.md:21-27` con los commits ratificados `494db2e` y `564bac4`, firmada en el commit `9042ae6` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14), elevado por el acta |
| `AUD-005` | D1 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §6:66` | cerrado por ratificación | acta `docs/sdd/ratificacion_historica.md:21-27` con los commits ratificados `494db2e` y `564bac4`, firmada en el commit `9042ae6` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14), elevado por el acta |
| `AUD-006` | D1 | Baja | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §6:59` | cerrado | `docs/sdd/README.md:5` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-007` | D1 | Baja | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §3:65` | cerrado | `docs/sdd/README.md:70` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-011` | D2 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §4:70` | cerrado | `.opencode/commands/sdd-implement.md:8` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-012` | D2 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:142` | cerrado | `.opencode/commands/sdd-implement.md:14` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-013` | D2 | Crítica | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:143` | cerrado | `.opencode/commands/sdd-validate.md:12` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-014` | D2 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:126` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:126` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-021` | D3 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §8:203` | cerrado | `docs/sdd/plantillas/spec.md:69` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-022` | D3 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §8:193` | cerrado | `docs/sdd/plantillas/tasks.md:15` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-023` | D3 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §8:205` | cerrado | `docs/sdd/plantillas/informe_analitico.md:1-44` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-031` | D4 | Crítica | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §2:18` | cerrado | `tools/sdd/validate.py:441-465` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-032` | D4 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:141` | cerrado | `tools/sdd/validate.py:569-573` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-033` | D4 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:142` | cerrado | `tools/sdd/validate.py:576-588` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-034` | D4 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:143` | cerrado | `tools/sdd/validate.py:539-549` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-035` | D4 | Crítica | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:136` | cerrado | `tools/sdd/validate.py:858-933` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-041` | D5 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §7:156` | cerrado | `tools/sdd/validate.py:1057-1088` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-042` | D5 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §8:195` | cerrado | `docs/sdd/plantillas/tasks.md:19` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-043` | D5 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §7:149` | cerrado | `tools/sdd/validate.py:1200-1204` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-044` | D5 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §7:149` | cerrado | `specs/001-main-menu/validation_report.md:36-37` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-051` | D6 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:132` | cerrado | `tools/sdd/validate.py:92-103` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-052` | D6 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:126` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:126` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-053` | D6 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:121` | cerrado por ratificación | acta `docs/sdd/ratificacion_historica.md:21-27` con los commits ratificados `494db2e` y `564bac4`, firmada en el commit `9042ae6` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14), elevado por el acta |
| `AUD-054` | D6 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:122` | cerrado | `tools/sdd/validate.py:691-729` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-055` | D6 | Baja | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §9:226` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:222-238` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-061` | D7 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §2:19` | cerrado | `.opencode/agents/sdd.md:65-103` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-062` | D7 | Crítica | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §7:75` | cerrado | `docs/constitution.md:74-77` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-063` | D7 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §7:79` | cerrado | `.opencode/agents/auditor.md:1-99` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-064` | D7 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:296` | cerrado | `.opencode/agents/planner.md:45-49` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-071` | D8 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §2:20` | cerrado | `.github/workflows/sdd.yml:1-23` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-072` | D8 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §8:195` | cerrado | `docs/sdd/plantillas/tasks.md:19` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-081` | D9 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:310` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:310` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-082` | D9 | Baja | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:308` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:308` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-083` | D9 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §15:370` | cerrado | `CHANGELOG.md:62` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-084` | D9 | Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §9:94` | cerrado | `docs/sdd/README.md:29` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-091` | D10 | Baja | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/constitution.md §6:66` | cerrado | `MEMORY.md:40` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-093` | D10 | Baja | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §3:65` | cerrado | `docs/sdd/README.md:39` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-094` | D10 | Alta | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §14:347` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:334` | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) |
| `AUD-008` | D1 | Baja | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/constitution.md §6:66` | cerrado | `docs/sdd/guia_spec_md.md:3` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-015` | D2 | Baja | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §4:70` | cerrado | `.opencode/agents/sdd.md:144-150` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-024` | D3 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §8:172` | cerrado | `specs/010-mecanismo-control-sdd/spec.md:370-371` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-036` | D4 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §14:334` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:332` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-037` | D4 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §14:336` | cerrado por ratificación | acta `docs/sdd/ratificacion_historica.md:21-27` con los commits ratificados `494db2e` y `564bac4`, firmada en el commit `9042ae6` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14), elevado por el acta |
| `AUD-038` | D4 | Media | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:144` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:144` | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) |
| `AUD-045` | D5 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:316` | cerrado | `specs/008-auditoria-cumplimiento-sdd/validation_report.md:141-144` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-046` | D5 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §14:334` | cerrado | `tools/sdd/validate.py:1250-1261` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-056` | D6 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:129` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:129` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-065` | D7 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:286` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:286` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-066` | D7 | Media | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:294` | cerrado | `.opencode/agents/sdd.md:44-55` | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) |
| `AUD-067` | D7 | Baja | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:298` | cerrado | `docs/constitution.md:79` | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) |
| `AUD-073` | D8 | Alta | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/constitution.md §2:20` | cerrado | `.github/workflows/sdd.yml:10-25` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-074` | D8 | Baja | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/constitution.md §5:39` | cerrado | `docs/Flujo_de_Trabajo_Git.md:232` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-075` | D8 | Media | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/constitution.md §2:20` | cerrado | `specs/013-cierre-reauditoria-conformidad/validation_report.md:116-126` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-085` | D9 | Alta | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:310` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:308` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-086` | D9 | Media | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/constitution.md §9:94` | cerrado | `docs/Flujo_de_Trabajo_Git.md:29` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-095` | D10 | Baja | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/constitution.md §6:66` | cerrado | `MEMORY.md:13` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-096` | D10 | Baja | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:300` | cerrado | `docs/sdd/README.md:61` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-097` | D10 | Baja | `docs/sdd/auditoria_cierre_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:314` | cerrado | `CHANGELOG.md:238` | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) |
| `AUD-098` | D10 | Media | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:300` | cerrado | `docs/sdd/README.md:62` | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) |
| `AUD-101` | D11 | Media | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/constitution.md §2:20` | cerrado | `.github/workflows/sdd.yml:15-19` | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) |
| `AUD-102` | D11 | Baja | `docs/sdd/auditoria_final_v0_7_0.md` (2026-11-14) | `docs/constitution.md §2:20` | cerrado | `.github/workflows/sdd.yml:29-31` | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) |
| `AUD-039` | D4 | Baja | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §6:144` | cerrado | `docs/Flujo_de_Trabajo_Git.md:11` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-057` | D6 | Media | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:119` | cerrado | `specs/014-cierre-observaciones-finales/spec.md:218` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-068` | D7 | Baja | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:294` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:294` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-076` | D8 | Media | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §16:378` | cerrado | `specs/013-cierre-reauditoria-conformidad/validation_report.md:120-121` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-087` | D9 | Alta | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:312` | cerrado | `docs/Flujo_de_Trabajo_Git.md:305` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-088` | D9 | Alta | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §15:353` | cerrado | `CHANGELOG.md:21` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-089` | D9 | Media | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:316` | cerrado | `CHANGELOG.md:42-43`, que registra el resultado de G5 y el de G6 en la entrada `v0.7.1`, y nota append-only `specs/015-cierre-auditoria-posterior/validation_report.md:98` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-090` | D9 | Alta | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/constitution.md §7:76` | cerrado | acta `docs/sdd/ratificacion_historica.md:17`, que ratifica la modificación de `564bac4` sobre artefactos publicados, firmada en el commit `9042ae6` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el acta del commit `9042ae6` |
| `AUD-099` | D10 | Media | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:300` | cerrado | `docs/sdd/README.md:63` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-100` | D10 | Baja | `docs/sdd/auditoria_posterior_v0_7_0.md` (2026-11-20) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:316` | cerrado | `CHANGELOG.md:255` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) |
| `AUD-103` | D9 | Media | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §15:353` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:353` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-104` | D9 | Alta | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/constitution.md §7:76` | cerrado | acta `docs/sdd/ratificacion_historica.md:17` y `:19`, con las tres rutas que modificó `564bac4` sin firma ratificadas en el commit `9042ae6` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el acta del commit `9042ae6` |
| `AUD-105` | D9 | Media | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:316` | cerrado | `CHANGELOG.md:40-46`, sección «Registro del release» de la entrada `v0.7.1` con el resultado de G5, el de G6 y el objeto del tag, y `specs/015-cierre-auditoria-posterior/validation_report.md:97-100` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-106` | D9 | Media | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §13:308` | cerrado | `git branch --list 'release/*'` sin salida; `.git/refs/heads/` no conserva el directorio `release/` y `.git/packed-refs` no declara `refs/heads/release/*`; regla del paso 8 en `docs/Flujo_de_Trabajo_Git.md:381-385` y verificación por listado vacío en `:250-257` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-107` | D10 | Media | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:300` | cerrado | `docs/sdd/README.md:64` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por la fila del corpus |
| `AUD-108` | D6 | Baja | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §5:119` | cerrado | `specs/014-cierre-observaciones-finales/spec.md:232` y `specs/015-cierre-auditoria-posterior/spec.md:292`, con el tag sobre el commit de merge publicado en `main` y el commit de empaquetado como ancestro | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-109` | D8 | Alta | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §16:378` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:378` y `docs/sdd/plantillas/spec.md:80`: ninguna spec fija el veredicto, el recuento ni las dimensiones de un informe posterior; el valor efectivo de las dos filas diferidas consta en `specs/013-cierre-reauditoria-conformidad/validation_report.md:120` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |
| `AUD-110` | D7 | Media | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21) | `docs/sdd/PROTOCOLO_OPERATIVO.md §12:300` | cerrado | `docs/sdd/PROTOCOLO_OPERATIVO.md:300` | `docs/sdd/auditoria_final_v0_7_1.md` (2026-11-21), cerrado por el artefacto de `SPEC-016` |

## 5. Tabla de cierre de los dieciséis hallazgos

Los 11 hallazgos del corte se declaran `cerrado` solo cuando el artefacto consta con su evidencia por ruta y línea, conforme a `CB-001`; los 5 que conservan una exención histórica se declaran `cerrado por ratificación` con el acta del propietario de `docs/sdd/ratificacion_historica.md`, conforme a `RF-014`. La tabla no altera el informe de origen.

| Hallazgo | Artefacto de cierre | Evidencia | Estado |
|---|---|---|---|
| `AUD-088` | `docs/sdd/PROTOCOLO_OPERATIVO.md` §15 y `CHANGELOG.md` | `CHANGELOG.md:21` | cerrado |
| `AUD-089` | `CHANGELOG.md`, entrada `v0.7.1`, sección «Registro del release» | `CHANGELOG.md:42-43` | cerrado |
| `AUD-090` | `docs/sdd/ratificacion_historica.md`, acta firmada en el commit `9042ae6` | `docs/sdd/ratificacion_historica.md:17` | cerrado |
| `AUD-103` | `docs/sdd/PROTOCOLO_OPERATIVO.md` §15 | `docs/sdd/PROTOCOLO_OPERATIVO.md:353` | cerrado |
| `AUD-104` | `docs/sdd/ratificacion_historica.md`, acta firmada en el commit `9042ae6` | `docs/sdd/ratificacion_historica.md:19` | cerrado |
| `AUD-105` | `CHANGELOG.md`, entrada `v0.7.1`, sección «Registro del release», y la nota del reporte de `SPEC-015` | `CHANGELOG.md:40-46` | cerrado |
| `AUD-106` | Eliminación de las ramas de empaquetado `release/v0-7-0` y `release/v0-7-1` en local | `docs/Flujo_de_Trabajo_Git.md:250-257` | cerrado |
| `AUD-107` | `docs/sdd/README.md`, fila de orden de lectura 35 | `docs/sdd/README.md:64` | cerrado |
| `AUD-108` | Filas T7 corregidas de `SPEC-014` y de `SPEC-015` | `specs/014-cierre-observaciones-finales/spec.md:232` | cerrado |
| `AUD-109` | §16 de `docs/sdd/PROTOCOLO_OPERATIVO.md` y la lista de prohibiciones de `docs/sdd/plantillas/spec.md` | `docs/sdd/PROTOCOLO_OPERATIVO.md:378` | cerrado |
| `AUD-110` | `docs/sdd/PROTOCOLO_OPERATIVO.md` §12 | `docs/sdd/PROTOCOLO_OPERATIVO.md:300` | cerrado |
| `AUD-003` | `docs/sdd/ratificacion_historica.md` | acta firmada en el commit `9042ae6` con los commits ratificados `494db2e` y `564bac4`, `docs/sdd/ratificacion_historica.md:21-27` | cerrado por ratificación |
| `AUD-004` | `docs/sdd/ratificacion_historica.md` | acta firmada en el commit `9042ae6` con los commits ratificados `494db2e` y `564bac4`, `docs/sdd/ratificacion_historica.md:21-27` | cerrado por ratificación |
| `AUD-005` | `docs/sdd/ratificacion_historica.md` | acta firmada en el commit `9042ae6` con los commits ratificados `494db2e` y `564bac4`, `docs/sdd/ratificacion_historica.md:21-27` | cerrado por ratificación |
| `AUD-037` | `docs/sdd/ratificacion_historica.md` | acta firmada en el commit `9042ae6` con los commits ratificados `494db2e` y `564bac4`, `docs/sdd/ratificacion_historica.md:21-27` | cerrado por ratificación |
| `AUD-053` | `docs/sdd/ratificacion_historica.md` | acta firmada en el commit `9042ae6` con los commits ratificados `494db2e` y `564bac4`, `docs/sdd/ratificacion_historica.md:21-27` | cerrado por ratificación |

## 6. Anexo de observaciones y tratamientos

La observación es el juicio que no cita la regla normativa que se incumple, conforme a `RF-012` y a `CB-009`. Queda fuera del recuento de hallazgos y su severidad no computa como hallazgo abierto.

- **Observaciones registradas en el corte:** 0. Los 5 informes de origen emiten sus juicios con la norma citada, de modo que ningún juicio del corte queda sin regla y la sección declara la ausencia de forma expresa.
- **Tratamientos registrados:** 0, porque no hay observación que tratar. La fecha y el identificador del commit del tratamiento se transcriben cuando el propietario registre una observación sin regla citada.
- **Efecto en el recuento:** 0 filas del anexo computan como hallazgo abierto y 0 observaciones de severidad `Alta` o `Media` quedan sin tratamiento.

## 7. Veredicto calculado desde las filas

Veredicto calculado: `CONFORME`. Recuento sobre las 82 filas: 0 hallazgos abiertos, 77 hallazgos cerrados, 5 cerrados por ratificación y 0 cerrados por exención.

La precedencia de la tabla de `RF-013` se aplica en este orden y el primer valor que se cumple es el resultado: `NO CONFORME` con 1 o más hallazgos abiertos de severidad `Crítica` o `Alta`, después `NO VERIFICABLE`, después `PARCIAL` y después `CONFORME`. Los tres valores anteriores no se alcanzan porque no hay hallazgo abierto de severidad `Alta` ni `Crítica`, ninguna fila carece de regla citada o de evidencia de cierre, y no queda observación de severidad `Alta` o `Media` sin tratamiento en el anexo de §6; el resultado es `CONFORME` con 0 hallazgos abiertos. La cifra y el estado de cada fila se actualizan con el artefacto de la tarea que lo aporte, y el rol de auditoría emite el veredicto del régimen sobre este registro.
