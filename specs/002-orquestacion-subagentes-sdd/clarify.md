# Clarificación - SPEC-002

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados).

## Reapertura

- **Motivo:** dictamen `NO CONVERGIDO` del 2026-11-13 (`validation_report.md`), con las brechas B-01 a B-05 abiertas sobre RF-006 y RNF-001.
- **Versión de la spec:** 0.6.0, con estado `implementing` y revalidación completa pendiente.
- **Hallazgos nuevos:** AMB-005, AMB-006 y AMB-007.
- **Alcance:** se añadieron CA-007 a CA-010 y se documentaron decisiones de permisos y de orden de compuertas. No se alteró ningún `RF`, `RNF` ni `CB`.
- **Ratificación:** el propietario ratificó G1 el 2026-11-13 sobre la reapertura (versiones 0.5.0 y 0.6.0 de `spec.md`). G4 y G6 continúan pendientes.

### Segunda reapertura (v0.8.0)

- **Motivo:** reauditoría del commit `af7ad55` con B-01 a B-05 cerrados y brechas nuevas B-06 (CHANGELOG sin configuración final), B-07 (AMB-006 y DEC-007 sin la allowlist cargada), B-08 (falta evidencia de delegación real en `tasks.md`), B-09 (regla 1 de `sdd.md` sin exigir el código de salida) y O-03 («G2 aprobada» no verificable).
- **Versión de la spec:** 0.8.0, con estado `implementing`.
- **Hallazgos nuevos:** AMB-008.
- **Alcance:** se amplió AMB-006 y DEC-007 con la allowlist exacta y la autorización de `git add` y `git commit`; se reformuló G2 como verificada por el validador; se añadieron T-009 y T-010. No se alteró ningún `RF`, `RNF`, `CB` ni `CA`, ni la sección Aprobaciones.

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

### AMB-005

- **Descripción:** el protocolo es internamente contradictorio en el orden de las compuertas: §2 sitúa G3 al final de Implement y G4 al final de Validate, mientras §6 define G4 como autorización de la implementación. La tabla de precondiciones del orquestador adoptaba la lectura de §6 y exigía G4 antes de Implement, lo que hacía inalcanzable la etapa.
- **Pregunta:** ¿Implement se gatea con G2 o con G4, y en qué momento se aprueba G4?
- **Respuesta:** G4 es la aprobación posterior a Validate; Implement se gatea con G2. La redacción de §6 del protocolo se interpretará como aprobación de la implementación ya realizada y se corregirá en un cambio editorial posterior.
- **Decisión:** el propietario resolvió el orden G3/G4: Implement exige G2 aprobada y spec en `tasked`; G4 se solicita después de Validate. No se modifica `docs/sdd/PROTOCOLO_OPERATIVO.md` en esta spec porque esa corrección editorial queda fuera de su alcance. Se alineó CA-005 con esa resolución (la compuerta previa a Implement es G2). CB-001 se alineó asimismo a G2 por decisión del propietario el 2026-11-13, de modo que no queda ninguna referencia a G4 como precondición de Implement.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** la regla `shell` de `sdd` se declaraba solo como excepción (`allow` del validador) sin regla general previa, por lo que la política base dejaba la terminal sin acotar; una regla general `deny` habría bloqueado el propio validador.
- **Pregunta:** ¿se acota `shell` con una regla general `deny` o con una regla general `ask` más una lista blanca de solo lectura?
- **Respuesta:** regla general `shell *` con efecto `ask`, seguida de `allow` para el validador y para la allowlist exacta de `sdd`: `git status *`, `git diff *`, `git log *`, `git show *`, `git rev-parse *`, `git branch --show-current`, `git branch --all *`, `git add *`, `git commit *` y `python tools\sdd\validate.py *`. Merge, tag y push permanecen en `ask`.
- **Autorización del propietario (2026-11-13, UTC):** el propietario autorizó mantener `git add` y `git commit` como excepción documentada a la descripción «Solo lectura» de `docs/sdd/PROTOCOLO_OPERATIVO.md` §10.
- **Decisión:** `ask` como regla general, seguido de la allowlist exacta anterior y del validador. `git add *` y `git commit *` son la excepción autorizada descrita arriba. Sustituye a AMB-003 en el acotamiento de `shell`.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `planner` y `coder` no declaraban reglas `subagent`, por lo que heredaban la política base y podían delegar en otros agentes, contra el mínimo privilegio del protocolo §10.
- **Pregunta:** ¿se permite que `planner` y `coder` lancen subagentes?
- **Respuesta:** no; la capacidad de lanzar subagentes queda reservada a `sdd`.
- **Decisión:** añadir `subagent *` con efecto `deny` en `planner` y en `coder`.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** «G2 aprobada» no es verificable. §6 del protocolo reserva la aprobación humana a G1, G4 y G6, por lo que G2 no puede aprobarse por una persona. RF-006, CB-001 y CA-005 de `spec.md` usan el término «aprobada» y no se modifican.
- **Pregunta:** ¿qué significa «G2 aprobada» como precondición de Implement y cómo se comprueba?
- **Respuesta:** G2 se verifica, no se aprueba: el agente `sdd` ejecuta `python tools\sdd\validate.py --spec SPEC-NNN --gate G2` y exige código de salida `0` y la spec en `tasked`. En RF-006, CB-001 y CA-005, «aprobada» se lee como «verificada con el validador».
- **Decisión:** G2 se verifica con `python tools\sdd\validate.py --spec SPEC-NNN --gate G2`. La aprobación humana se reserva a G1, G4 y G6. Se sustituye «G2 aprobada» por «G2 verificada» en DEC-006 y en la tabla de precondiciones de `sdd.md` (T-009).
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

Ninguno adicional; se conservan `CB-001`, `CB-002` y `CB-003`.

## Parches aplicados a spec.md

- [x] Precisado RNF-001 con el orden de reglas (generales antes de excepciones).
- [x] Añadido CB-003 (fallo del validador durante la verificación de compuerta).
- [x] Añadido CA-006 (comandos `sdd-*` siguen operando como primarios).
- [x] Añadido RF-007 (contexto mínimo en la solicitud al subagente).
- [x] Añadida la línea «Cubre:» a CA-001 a CA-006 para completar la trazabilidad `RF/CB → CA`.
- [x] Añadido CA-007 (verificación de compuerta previa con el validador y parada ante código distinto de `0`), cubre RF-006 y CB-003.
- [x] Añadido CA-008 (solicitud con spec, etapa y resultado esperado, y bloqueo por ambigüedad registrado), cubre RF-007 y CB-002.
- [x] Añadido CA-009 (reglas generales antes de las excepciones en la configuración cargada), cubre RNF-001.
- [x] Añadido CA-010 (entrada en `CHANGELOG.md` bajo `Unreleased` antes de la release), cubre RNF-002.
- [x] Actualizado el frontmatter a `implementing` y versión 0.5.0, con la fila correspondiente en el historial de cambios.
- [x] Alineado CA-005 con AMB-005: la compuerta previa a `coder` es G2; G4 se solicita al final de Validate.
- [x] CB-001 alineado a G2 (antes G4).
- [x] Sin cambios en RF-001 a RF-007, RNF-001 ni RNF-002 durante la reapertura.
- [x] Segunda reapertura (v0.8.0): frontmatter a `implementing`, versión 0.8.0 y fila correspondiente en el historial de cambios de `spec.md`.
- [x] AMB-006 ampliado con la allowlist exacta y la autorización del propietario (2026-11-13, UTC) para `git add` y `git commit` como excepción a §10. Cubre B-07.
- [x] AMB-008 añadido: G2 se verifica con `python tools\sdd\validate.py --spec SPEC-NNN --gate G2`; la aprobación humana queda reservada a G1, G4 y G6 (§6). Cubre O-03.
- [x] DEC-006 y DEC-007 de `plan.md` alineados con AMB-006 y AMB-008; matriz de cobertura con T-009 y T-010.
- [x] Añadidas a `tasks.md` las tareas T-009 (`sdd.md`, cubre B-09) y T-010 (`CHANGELOG.md`, cubre B-06). Su ejecución se registra en `tasks.md`; no son parches de `spec.md`.

## Decisiones de negocio

- El orquestador no redacta artefactos: delega en el agente especializado de cada etapa.
- Las compuertas siguen siendo humanas; la delegación no autoriza aprobaciones.
- `explore` se admite por su carácter de solo lectura.