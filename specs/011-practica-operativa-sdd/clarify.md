# Clarificación — SPEC-011

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-011` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `RF-002` enumeraba tres reglas de precedencia sin declarar que una concesión de escritura no autoriza a declarar compuertas, y `RF-011` situaba el orden de precedencia en `opencode.jsonc` sin fijar el efecto de una concesión global sobre una denegación de rol.
- **Pregunta:** ¿Qué reglas resuelven el solapamiento de permisos, dónde se declaran y qué efecto tiene una concesión global sobre una denegación de rol?
- **Respuesta:** cuatro reglas: la denegación explícita prevalece sobre cualquier concesión, la ruta más específica prevalece sobre la más general, la ruta no declarada está denegada y una concesión de escritura no autoriza a declarar compuertas. Se declaran en la spec y se reflejan en `opencode.jsonc`; una concesión global no amplía una denegación de rol.
- **Decisión:** corrección de `RF-002` y de `RF-011`, con ajuste de `CA-002` y de `CA-013`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `RF-003` limitaba la escritura a «el informe de auditoría de `docs/sdd/`» sin fijar el nombre de archivo, y `RNF-005` exigía una sola ruta sin declarar la forma del rol ni su política de shell y de subagentes.
- **Pregunta:** ¿Cómo se materializa el rol de auditoría, cuál es su ruta exacta de escritura y qué shell y subagentes admite?
- **Respuesta:** se crea `.opencode/agents/auditor.md` con `mode: subagent`; lectura de la base normativa y de las specs; escritura limitada a los informes de auditoría bajo `docs/sdd/auditoria_*.md`; shell de solo lectura con git de lectura y el validador; subagentes denegados; no modifica requisitos, código, configuración ni base normativa; no aprueba compuertas.
- **Decisión:** corrección de `RF-003` y de `RNF-005`, caso borde nuevo `CB-015` y ajuste de `CA-003` y de `CA-004`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `RF-006` nombraba «un Pull Request» sin fijar ramas de destino, entorno de ejecución, comandos ni límites de tiempo, y `RNF-001` fijaba un umbral conjunto sin desglose por etapa.
- **Pregunta:** ¿Qué dispara el flujo de integración continua, en qué entorno se ejecuta, qué ejecuta y con qué límites de tiempo?
- **Respuesta:** se crea `.github/workflows/sdd.yml` para Pull Request dirigidos a `dev` y a `main`, en `windows-latest` con Python 3.12; ejecuta `python tools\sdd\validate.py --all` y `python -m unittest discover -s tools\sdd\tests -q`; sin secretos, sin push, sin tags y sin operaciones remotas; el conjunto completa en 300 segundos o menos y la suite en 60 segundos o menos.
- **Decisión:** corrección de `RF-006` y de `RNF-001`, requisitos nuevos `RNF-007` y `RNF-008`, caso borde nuevo `CB-016` y ajuste de `CA-007`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `RF-008` y `RF-009` exigían verificar los hallazgos y registrar el cierre sin fijar el artefacto donde se registra ni el hecho concreto que acredita cada hallazgo.
- **Pregunta:** ¿Dónde se registra el cierre de `AUD-081` a `AUD-084` y de `AUD-091`, y qué hecho acredita cada uno?
- **Respuesta:** el cierre se registra en el reporte de validación con una fila por hallazgo, y el hecho que lo acredita es: `dev` contiene `main` (`AUD-081`); la referencia `origin/release/v0-6-0` no existe (`AUD-082`); la rama Gemma permanece local, no publicada y con decisión registrada (`AUD-083`); los seis documentos están versionados (`AUD-084`); `MEMORY.md` no contiene hechos obsoletos (`AUD-091`). Un hecho no acreditado mantiene el hallazgo abierto con el motivo consignado.
- **Decisión:** corrección de `RF-008` y de `RF-009`, con ajuste de `CA-009`, `CA-010` y `CA-011`. Sin caso borde nuevo: `CB-008` a `CB-012` ya cubren la no acreditación.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** el alcance excluía `AGENTS.md` y no se pronunciaba sobre `MEMORY.md`, mientras el mapa de agentes conservaba cinco roles y el contexto operativo no mencionaba la integración continua.
- **Pregunta:** ¿Se actualizan `AGENTS.md` y `MEMORY.md`, y con qué límite?
- **Respuesta:** `AGENTS.md` añade `auditor` al mapa de agentes y conserva entre 30 y 70 líneas útiles; `MEMORY.md` actualiza la lista de agentes y menciona la integración continua. No se altera regla alguna de la base normativa; cualquier otro cambio de `AGENTS.md` exige una spec de base.
- **Decisión:** requisitos nuevos `RF-012` y `RF-013`, criterios nuevos `CA-016` y `CA-017`, y ajuste de `## Fuera de alcance` y de `## Contexto y objetivo`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `RF-001` exigía reglas de shell por rol sin fijar la allowlist de cada uno, de modo que el menor privilegio seguía sin ser contrastable y `AUD-061` permanecía abierto.
- **Pregunta:** ¿Qué comandos de shell admite cada rol y con qué alcance de escritura?
- **Respuesta:** `planner` deniega el shell salvo la lectura de git y el validador; `coder` admite los comandos de prueba y de validación y la escritura en `src/`, `tests/`, `tools/` y `tasks.md`, y deniega el resto; `reviewer` admite solo la lectura de git y el validador, sin shell de escritura; `documenter` tiene el shell denegado; `sdd` conserva la allowlist de git de lectura, `git add`, `git commit` y el validador; `auditor` admite la lectura de git y el validador.
- **Decisión:** corrección de `RF-001`, caso borde nuevo `CB-017`, ajuste de `CA-001` y criterio nuevo `CA-014`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `RF-012` y `RF-013` tocan documentos de la base, entre ellos `AGENTS.md` de rango 2, sin declarar el límite entre alineación factual y cambio de regla.
- **Pregunta:** ¿La actualización del mapa de agentes modifica la base normativa?
- **Respuesta:** no. La constitución ya declara seis roles de agente; la spec alinea el mapa y el contexto operativo con ese hecho y no altera regla alguna. Un cambio de regla de la base se registra como dependencia y exige una spec de base.
- **Decisión:** corrección de `## Fuera de alcance` y de `## Contexto y objetivo`; sin requisito nuevo.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `RF-011` situaba la precedencia global en `opencode.jsonc` sin declarar que el archivo es configuración del cliente y no documento de la base, ni la prohibición de incorporar credenciales.
- **Pregunta:** ¿Cómo se trata `opencode.jsonc` y qué límite tiene su modificación?
- **Respuesta:** `opencode.jsonc` es configuración del cliente y no documento de la base; se modifica para reflejar la precedencia y las protecciones de permisos, sin credenciales ni secretos, y su concesión global no amplía una denegación de rol.
- **Decisión:** corrección de `RF-011`, requisito nuevo `RNF-006`, ajuste de `CA-013` y una entrada nueva en `## Fuera de alcance`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-015

`SI el rol `auditor` recibe una solicitud de escribir en una ruta de `docs/sdd/` cuyo nombre no cumple el patrón `auditoria_*.md`, ENTONCES la operación DEBE quedar denegada y el hallazgo DEBE registrarse en el informe de auditoría.`

### CB-016

`SI un Pull Request se dirige a una rama distinta de `dev` o de `main`, ENTONCES el flujo de integración continua NO DEBE ejecutarse y la verificación DEBE quedar a cargo de la ejecución local del validador y de la suite.`

### CB-017

`SI un rol solicita un comando de shell fuera de su allowlist, ENTONCES la operación DEBE quedar denegada y el hallazgo DEBE registrarse con el rol y el comando solicitado.`

## Parches aplicados a `spec.md`

- [x] `RF-002` y `RF-011`: precedencia de cuatro reglas, con la prohibición de declarar compuertas por una concesión de escritura, y reflejo del orden en `opencode.jsonc` sin ampliación de una denegación de rol — afecta a `RF-002`, `RF-011`, `CA-002` y `CA-013`.
- [x] `RF-003` y `RNF-005`: el rol `auditor` se declara como subagente con shell de solo lectura, subagentes denegados y escritura limitada a `docs/sdd/auditoria_*.md` — afecta a `RF-003`, `RNF-005`, `CA-003` y `CA-004`.
- [x] `RF-006` y `RNF-001`: disparadores por rama de destino, entorno Windows con Python 3.12, umbral de 300 segundos para el conjunto y de 60 segundos para la suite — afecta a `RF-006`, `RNF-001`, `RNF-007`, `RNF-008` y `CA-007`.
- [x] `RF-008` y `RF-009`: registro del cierre en el reporte de validación y hecho que acredita cada hallazgo — afecta a `RF-008`, `RF-009`, `CA-009`, `CA-010` y `CA-011`.
- [x] `RF-012` y `RF-013`: alcance de la actualización de `AGENTS.md` y de `MEMORY.md`, con la longitud de 30 a 70 líneas útiles y la prohibición de conservar un hecho obsoleto — afecta a `RF-012`, `RF-013`, `CA-016`, `CA-017` y `## Fuera de alcance`.
- [x] `RF-001`: allowlist de comandos de shell por rol y política de subagentes — afecta a `RF-001`, `CB-017`, `CA-001` y `CA-014`.
- [x] `RNF-006`: prohibición de credenciales y de secretos en la configuración de permisos — afecta a `RNF-006` y `CA-013`.
- [x] Casos borde nuevos `CB-015`, `CB-016` y `CB-017` incorporados al cuerpo de la spec — afecta a `CB-015`, `CB-016`, `CB-017`, `CA-003`, `CA-014` y `CA-015`.
- [x] `## Fuera de alcance` y `## Contexto y objetivo`: se retira `AGENTS.md` de la exclusión, se limita su cambio al mapa de agentes, se declara `opencode.jsonc` como configuración y se registra como dependencia cualquier cambio de regla de la base — afecta a `RF-011`, `RF-012` y `RF-013`.
- [x] `### Trazabilidad con el informe de auditoría`: nota que vincula `RF-012` y `RF-013` con su criterio y declara que no responden a un hallazgo del informe — afecta a `RF-012` y a `RF-013`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-14 y `status` `clarified`; fila nueva en el historial de cambios y fila T1 en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- El rol de auditoría no aprueba compuertas: la aprobación de G1, G4 y G6 sigue siendo del propietario mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`.
- La integración continua es la única verificación automática de la integración que esta spec establece; la instalación de un hook local de Git queda fuera de alcance.
- El flujo no ejecuta operaciones remotas: la comprobación del estado del remoto se limita a las referencias de seguimiento locales y la consulta directa al remoto queda como comprobación no verificada.
- La configuración de permisos no admite secretos: `.env` permanece fuera de la lectura y de la edición de cada agente y la plantilla versionable sigue siendo `example.env`.
- Los cierres de `AUD-081` a `AUD-084` y de `AUD-091` se acreditan con hechos verificables y no con la afirmación de que la corrección se ejecutó; un hecho no acreditado mantiene el hallazgo abierto.
- `AGENTS.md` y `MEMORY.md` se alinean con los seis roles que la constitución declara y con el estado operativo del repositorio; la alineación no altera regla alguna y un cambio de regla exige una spec de base.
- La precedencia se declara en la spec y en `opencode.jsonc`; el permiso efectivo no depende del orden de resolución del cliente.
- El comando literal de cada verificación se registra en este artefacto y no en `spec.md`, de modo que el contrato de la feature conserva la forma de la plantilla de rango 5.
