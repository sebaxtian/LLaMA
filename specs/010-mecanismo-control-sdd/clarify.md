# Clarificación — SPEC-010

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-010` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `RF-016` situaba el historial de transiciones en una sección de nivel 2 que la plantilla de `spec.md` no declara, y la spec añadía `## Dependencias de la base` como sección propia. Dos secciones fuera del contrato de rango 5 convivían con las nueve secciones obligatorias.
- **Pregunta:** ¿Dónde se registra el historial de transiciones y qué ocurre con la sección de dependencias de la base?
- **Respuesta:** el historial se registra como subsección `### Historial de transiciones` dentro de `## Historial de cambios`, con las columnas Fecha, Transición, Origen, Destino, Responsable y Evidencia. La sección `## Dependencias de la base` se integra en `## Fuera de alcance` y en `## Contexto y objetivo`.
- **Decisión:** corrección de `RF-016` y de `CB-011`; se retiran las dos secciones de nivel 2 y el contenido se integra en las secciones del contrato.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `RF-005` ordenaba al comando `/sdd-validate` escribir el reporte antes de evaluar G4, sin separar el rol que escribe del rol que evalúa la compuerta ni del que escribe el estado `validated`. El protocolo atribuye la escritura de T6 al orquestador y la aprobación de G4 al propietario.
- **Pregunta:** ¿Qué rol ejecuta el comando, qué escribe, quién evalúa G4 y quién escribe `validated`?
- **Respuesta:** el comando lo ejecuta el rol `reviewer` y su única escritura es `validation_report.md`. La evaluación de G4 la ejecuta el orquestador después de que el reporte exista y de que el propietario firme la línea en `spec.md`. El comando no evalúa G4 ni escribe `validated`, y el orquestador escribe `validated` tras la aprobación firmada.
- **Decisión:** corrección de `RF-005` y de `RF-021`, con ajuste de `CA-004` y de `CA-005`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `RF-010` exigía localizar el commit que introdujo la línea de aprobación sin fijar el procedimiento, y no resolvía el caso de un commit de merge que introduce la línea en la fusión.
- **Pregunta:** ¿Con qué operaciones se localiza el commit y qué ocurre cuando el commit es de merge?
- **Respuesta:** el validador localiza el commit con `git log -S` sobre el archivo correspondiente, toma el commit más reciente que introduce la línea y verifica su firma con `git verify-commit` y la lista `docs/sdd/firmantes_autorizados`, sin red. Si el commit es de merge, inspecciona el commit no merge que introdujo la línea.
- **Decisión:** corrección de `RF-010` y caso borde nuevo `CB-015`, con ajuste de `CA-007`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `RF-013` exigía la ausencia de la rama de trabajo sin precisar si la comprobación alcanza el remoto, y `RNF-003` prohíbe el acceso a red.
- **Pregunta:** ¿Cómo se comprueba la eliminación de la rama sin consultar el remoto?
- **Respuesta:** el validador comprueba la fusión con dos padres, la ejecución posterior sin hallazgos y la ausencia de la rama en las ramas locales y en las referencias remotas de seguimiento. No ejecuta consulta de red. La ausencia de la referencia remota de seguimiento se acepta como evidencia local y la verificación remota directa queda como comprobación no verificada.
- **Decisión:** corrección de `RF-013` y de `CB-012`, con ajuste de `CA-012` y una entrada nueva en `## Fuera de alcance`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** `RF-009` exigía el informe de auditoría de conformidad «cuando el release sea menor» sin fijar cómo determina el validador esa condición.
- **Pregunta:** ¿Cómo se determina que un release es menor?
- **Respuesta:** el validador compara el componente MINOR del tag con el del tag anterior en orden SemVer. Si el MINOR aumenta, exige la referencia al informe de auditoría de conformidad en la entrada del release; si no aumenta, no la exige. La comparación usa el listado local de tags y orden de versiones, sin red.
- **Decisión:** corrección de `RF-009` y de `RF-014`, con ajuste de `CA-009`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `RNF-006` y `CB-014` limitaban la ventana de legado a `SPEC-001` a `SPEC-007`, conforme a la base v2, pero `SPEC-008` y `SPEC-009` se publicaron antes de existir el mecanismo y quedarían incumpliendo comprobaciones posteriores a su publicación.
- **Pregunta:** ¿Qué specs quedan amparadas por la ventana de legado del mecanismo?
- **Respuesta:** las comprobaciones introducidas por `SPEC-010` no devuelven código de salida 1 por incumplimiento en `SPEC-001` a `SPEC-009`; se registran como advertencia de legado. `SPEC-010` y las posteriores cumplen el mecanismo completo.
- **Decisión:** corrección de `RNF-006` y de `CB-014`, con ajuste de `CA-020`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `RF-007`, `RF-008` y `RF-009` exigían «la cadena exacta de aprobación» sin fijar la forma completa de la línea en `spec.md` ni de la viñeta en `CHANGELOG.md`.
- **Pregunta:** ¿Qué forma exacta reconoce el validador para G1, G4 y G6?
- **Respuesta:** G1 y G4 se reconocen con la forma `- [x] G1:` seguida de la cadena `- Approved by: Agent Sebaxtian` y de una fecha ISO, con su equivalente para G4. G6 se reconoce con la viñeta `- Approved by: Agent Sebaxtian` dentro de la entrada del release de `CHANGELOG.md`. El validador exige la cadena exacta y la fecha en formato ISO.
- **Decisión:** corrección de `RF-007`, `RF-008` y `RF-009`, con ajuste de `CA-007` y de `CA-009`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** la spec declaraba los actores sin asignar de forma explícita el escritor de cada transición, de modo que la escritura de estados podía quedar en un rol distinto del que el protocolo atribuye.
- **Pregunta:** ¿Qué rol escribe cada estado y quién autoriza las transiciones fuera del ciclo?
- **Respuesta:** `planner` escribe `clarified`, `planned` y `tasked`; el orquestador escribe `implementing`, `implemented` y `validated`; el propietario autoriza la cancelación, la reapertura y la sustitución. Ningún agente escribe la sección de aprobaciones.
- **Decisión:** corrección de `## Actores y permisos` y de `RF-021`; se mantiene la atribución de `RF-002`, `RF-003` y `RF-016`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-015

`SI el commit que introdujo la línea de aprobación es un commit de merge, ENTONCES el validador DEBE inspeccionar el commit no merge que introdujo la línea y DEBE verificar la firma de ese commit.`

## Parches aplicados a `spec.md`

- [x] `RF-016` y `CB-011`: el historial de transiciones pasa a la subsección `### Historial de transiciones` de `## Historial de cambios` — afecta a `RF-016`, `CB-011`, `CA-002` y `CA-014`.
- [x] Se retiran las secciones de nivel 2 `## Historial de transiciones` y `## Dependencias de la base` y su contenido se integra en `## Contexto y objetivo` y en `## Fuera de alcance` — afecta a `RF-016`.
- [x] La tabla de trazabilidad con el informe de auditoría pasa a subsección `### Trazabilidad con el informe de auditoría` de `## Contexto y objetivo`, de modo que la spec conserva las nueve secciones del contrato de rango 5 — afecta a la estructura de `spec.md`.
- [x] `RF-005` y `RF-021`: separación entre el rol `reviewer` y el orquestador, y escritura de `validated` tras la aprobación firmada — afecta a `RF-005`, `RF-021`, `CA-004` y `CA-005`.
- [x] `RF-010` y `CB-015`: localización del commit con `git log -S`, verificación con `git verify-commit` y tratamiento del commit de merge — afecta a `RF-010`, `CB-015` y `CA-007`.
- [x] `RF-013` y `CB-012`: G5 se comprueba sobre las ramas locales y las referencias remotas de seguimiento, sin consulta de red — afecta a `RF-013`, `CB-012` y `CA-012`.
- [x] `RF-009` y `RF-014`: detección del release menor por comparación del componente MINOR con el tag anterior — afecta a `RF-009`, `RF-014` y `CA-009`.
- [x] `RNF-006` y `CB-014`: la ventana de legado cubre `SPEC-001` a `SPEC-009` — afecta a `RNF-006`, `CB-014` y `CA-020`.
- [x] `RF-007`, `RF-008` y `RF-009`: forma exacta de la casilla de G1 y G4 y de la viñeta de G6 — afecta a `RF-007`, `RF-008`, `RF-009`, `CA-007` y `CA-009`.
- [x] `## Actores y permisos`: el rol `reviewer` ejecuta el comando `/sdd-validate` y el orquestador evalúa G4 — afecta a `RF-005` y a `RF-021`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-14 y `status` `clarified`; fila nueva en el historial de cambios y fila T1 en `### Historial de transiciones` — afecta a `RF-016`.

## Decisiones de negocio

- El mecanismo de control se implementa sobre la base v2 sin modificarla: ninguna comprobación exige cambiar la constitución, `AGENTS.md`, el protocolo, el flujo Git ni las plantillas.
- La autoría de una aprobación se acredita por la firma del commit que introduce la línea y por la lista `docs/sdd/firmantes_autorizados`; una línea escrita sin esa firma no acredita la compuerta.
- Las operaciones Git de localización y de verificación del commit de aprobación se nombran en `RF-010` porque la condición de la compuerta depende de la forma de localización. El requisito no fija rutas de código de producción.
- G5 no consulta el remoto: la ausencia de la referencia remota de seguimiento se acepta como evidencia local y la consulta remota directa queda como comprobación no verificada, conforme a `RNF-003`.
- La ventana de legado cubre `SPEC-001` a `SPEC-009`; `SPEC-010` y las posteriores cumplen el mecanismo completo.
- Una comprobación que exigiera un cambio en la base se registra como dependencia y no se ejecuta en esta feature.
