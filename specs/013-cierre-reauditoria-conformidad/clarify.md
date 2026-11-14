# Clarificación — SPEC-013

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-013` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `RF-010` exigía preparar el árbol y el entorno de Python y declarar exigible «el nombre del check» sin fijar las acciones de preparación, el nombre del job ni el documento donde se declara la exigibilidad; una redacción distinta por autor dejaba la compuerta G5 sin un check contrastable.
- **Pregunta:** ¿Con qué acciones se prepara el árbol, qué job y qué check se declaran exigibles y dónde se documenta la exigibilidad?
- **Respuesta:** el flujo prepara el árbol con `actions/checkout`, instala Python con `actions/setup-python` y ejecuta el validador y la suite en cada Pull Request dirigido a `main` y a `dev`. El job `verify` del flujo `SDD` es el check que se exige en las reglas de protección. La exigibilidad se documenta en `docs/Flujo_de_Trabajo_Git.md` y se aplica con la herramienta de protección existente.
- **Decisión:** corrección de `RF-010`, ajuste de `CB-009`, `CB-010` y `CA-010`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `RF-012` expresaba la sincronización como ancestría, pero el cuerpo de la comprobación conservaba la referencia al conteo simétrico y el estado vigente `48 0` de `dev` respecto de `main` quedaba como bloqueo; no estaba fijado qué salida habilita el empaquetado.
- **Pregunta:** ¿Qué condición habilita el empaquetado cuando `dev` contiene trabajo no publicado?
- **Respuesta:** la condición es de ancestría: `main` debe ser ancestro de `dev` y el tag del release debe apuntar a un commit alcanzable desde `main`. Se retira la exigencia del conteo `0 0`, que es inalcanzable con trabajo no publicado. El estado `48 0` deja de ser bloqueo y no se corrige forzando una puesta al día del historial.
- **Decisión:** corrección de `RF-012`, ajuste de `CB-003`, `CB-004` y `CA-012`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `RF-013` admitía `docs/` sin enumerar los prefijos vigentes ni la forma exacta de la rama de release, de modo que la gramática admitía una lectura más amplia que la declarada en el rango 4.
- **Pregunta:** ¿Cuál es la lista cerrada de prefijos y qué validación se aplica a `docs/`?
- **Respuesta:** la lista cerrada es `feat/`, `fix/`, `hotfix/`, `docs/` y `release/vX-Y-Z`. `docs/` se admite para cambios exclusivamente documentales, con la misma validación de minúsculas, números y guiones que los demás prefijos. Un prefijo fuera de la lista se rechaza.
- **Decisión:** corrección de `RF-013`, ajuste de `CB-001`, `CB-002` y `CA-013`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `RF-006` exigía la sección de cierre de integración en los reportes de `SPEC-008` a `SPEC-011` sin fijar los identificadores del merge ni el contenido de la línea de release, y sin declarar el efecto sobre una matriz o un dictamen no convergido.
- **Pregunta:** ¿Qué merge y qué línea de release se registran en cada uno de los cuatro reportes y qué elementos quedan intactos?
- **Respuesta:** los merges son `49caac9` para `SPEC-008`, `09eaf34` para `SPEC-009`, `94c2ea1` para `SPEC-010` y `9df8446` para `SPEC-011`, tomados del historial. La línea `Release:` queda vacía. El estado `validated` de las cuatro specs no cambia y sus matrices y dictámenes quedan intactos.
- **Decisión:** corrección de `RF-006`, ajuste de `CB-007`, `CB-008` y `CA-006`, y tabla de valores en `## Decisiones de negocio`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** `RF-007` acotaba el alcance de la comprobación de `Spec:` al último tag o al merge-base, pero no excluía los merges del alcance ni fijaba qué se informa cuando la enumeración resulta vacía; sobre `dev` la comprobación podía quedar sin efecto.
- **Pregunta:** ¿Qué commits examina la comprobación y qué se informa cuando no hay ninguno?
- **Respuesta:** se examinan los commits posteriores al último tag anotado de release o, si no existe, los posteriores al merge-base con `main`. Los merges se excluyen. La enumeración vacía se informa como no aplicable y no produce error. Sobre `dev` la comprobación examina al menos un commit cuando existe trabajo de implementación posterior al último tag.
- **Decisión:** corrección de `RF-007`, ajuste de `CB-005` y `CA-007`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `RF-008` atribuía la corrección al historial de `SPEC-012`, mientras la tabla de escritura de estados del protocolo asignaba T4 a T7 al orquestador y el orquestador carece de escritura sobre `specs/`; no estaba fijado cuál de los dos documentos se corrige.
- **Pregunta:** ¿Qué documento se corrige y qué rol escribe las transiciones T4 a T7?
- **Respuesta:** las transiciones T4 a T7 las escribe el rol `planner` sobre la verificación del orquestador, porque el `planner` es el rol con permiso de escritura en `specs/`. Se corrige §5 del protocolo en ese sentido. Las filas T4 a T6 de `SPEC-012` que atribuyen la escritura al `planner` quedan conformes y no se editan.
- **Decisión:** corrección de `RF-008`, caso borde nuevo `CB-016` y ajuste de `CA-008`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `RF-009` y §12 negaban al orquestador la escritura de artefactos, mientras §5 le atribuía T4 a T7 y `.opencode/agents/sdd.md` le concedía escritura sobre `specs/`; la contradicción no fijaba qué permiso se retira ni qué actos conserva el orquestador.
- **Pregunta:** ¿Qué conserva el orquestador y qué permiso se retira?
- **Respuesta:** el orquestador verifica compuertas, registra resultados y ejecuta el validador, `git add` y `git commit`; no redacta artefactos. Se retira su permiso de escritura sobre `specs/` en `.opencode/agents/sdd.md`. La contradicción entre §5 y §12 se elimina y la prohibición de escribir la sección de aprobaciones se conserva.
- **Decisión:** corrección de `RF-009`, ajuste de `CB-014` y `CA-009`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `RF-003` exigía retirar la tercera casilla y detectar la duplicidad marcada, pero no fijaba el número de casillas que conserva cada sección ni si la detección alcanza una casilla sin marcar.
- **Pregunta:** ¿Cuántas casillas conserva cada sección de aprobaciones y qué ocurre con una casilla adicional sin marcar?
- **Respuesta:** cada sección conserva 2 casillas, `G1` y `G4`. Una segunda casilla de la misma compuerta produce error aunque no esté marcada. Las casillas residuales de `SPEC-010` y `SPEC-011` se retiran con autorización del propietario.
- **Decisión:** corrección de `RF-003`, ajuste de `CB-006` y `CA-003`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-009

- **Descripción:** `RF-004` declaraba verificadas la firma y la pertenencia de la clave sin nombrar la clave ni el acto de verificación, y el contrato del validador y `AGENTS.md` conservaban la afirmación contraria.
- **Pregunta:** ¿Qué verifica el validador sobre la firma y qué afirmación se retira?
- **Respuesta:** el validador verifica la firma criptográfica del commit de aprobación y contrasta la clave firmante con `docs/sdd/firmantes_autorizados`. El protocolo y `AGENTS.md` declaran esa verificación y retiran la afirmación de que no se realiza.
- **Decisión:** corrección de `RF-004` y ajuste de `CA-004`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-010

- **Descripción:** `RF-005` describía 2 ventanas de legado sin declarar el motivo de cada una ni su límite, de modo que la exención podía ampliarse sin control.
- **Pregunta:** ¿Qué motivo y qué límite tiene cada ventana?
- **Respuesta:** la ventana estructural cubre `SPEC-001` a `SPEC-009` para las comprobaciones C-01 a C-13 y la ventana de trazabilidad cubre `SPEC-008` a `SPEC-011` para C-14 a C-18. Cada ventana declara su motivo y su límite en el contrato del validador y no se amplía sin una spec posterior. Una spec fuera de su ventana produce error.
- **Decisión:** corrección de `RF-005`, ajuste de `CB-011` y `CA-005`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-011

- **Descripción:** `RF-011`, `RF-014`, `RF-015` y `RF-016` corregían afirmaciones documentales sin fijar el alcance exacto de cada corrección ni el límite superior del historial de releases.
- **Pregunta:** ¿Qué se corrige en cada documento y hasta qué release se completa el historial?
- **Respuesta:** `docs/Flujo_de_Trabajo_Git.md` declara la suite, sus 131 pruebas y su ejecución en el job `verify`. `MEMORY.md` coincide con `specs/INDEX.md` y con el frontmatter de cada spec. `docs/sdd/README.md` registra la fila del informe de reauditoría. `CHANGELOG.md` completa el historial hasta el release anterior a `v0.7.0`, con los 8 tags publicados de `v0.1.0` a `v0.6.0`.
- **Decisión:** corrección de `RF-011`, `RF-014`, `RF-015` y `RF-016`, y ajuste de `CB-013`, `CA-011` y `CA-014`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-012

- **Descripción:** `RF-002` exigía 7 etapas sin fijar sus nombres ni la numeración inicial, y la definición del rol orquestador numeraba 6 filas desde 2 Specify y omitía Release.
- **Pregunta:** ¿Cómo se numeran y se nombran las 7 etapas en la definición del rol orquestador?
- **Respuesta:** la tabla declara 7 etapas numeradas de 1 a 7: 1 Specify, 2 Clarify, 3 Plan, 4 Tasks, 5 Implement, 6 Validate y 7 Release. Se corrige la numeración y la omisión.
- **Decisión:** corrección de `RF-002` y ajuste de `CA-002`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-016

`SI el orquestador no ha registrado la verificación de la compuerta que habilita una transición de T4 a T7, ENTONCES el `planner` NO DEBE escribir la transición y DEBE informar la verificación ausente.`

## Parches aplicados a `spec.md`

- [x] `RF-010`: preparación del árbol con `actions/checkout`, instalación de Python con `actions/setup-python`, job `verify` del flujo `SDD` y exigibilidad documentada en `docs/Flujo_de_Trabajo_Git.md` — afecta a `RF-010`, `CB-009`, `CB-010` y `CA-010`.
- [x] `RF-012`: ancestría en lugar de conteo simétrico y estado `48 0` sin carácter de bloqueo — afecta a `RF-012` y `CA-012`.
- [x] `RF-013` y `CA-013`: lista cerrada de 5 prefijos con `release/vX-Y-Z` y `docs/` con la validación de minúsculas, números y guiones — afecta a `RF-013`, `CB-001`, `CB-002` y `CA-013`.
- [x] `RF-006` y `CA-006`: sección `## Cierre de integración` con la línea `Merge:` de los 4 identificadores y la línea `Release:` vacía, con la tabla de valores en el cuerpo — afecta a `RF-006`, `CB-007`, `CB-008` y `CA-006`.
- [x] `RF-007` y `CA-007`: exclusión de merges del alcance, examen de al menos 1 commit sobre `dev` y enumeración vacía informada como no aplicable — afecta a `RF-007`, `CB-005` y `CA-007`.
- [x] `RF-008` y `CA-008`: escritura de T4 a T7 por el `planner` sobre la verificación del orquestador, con las filas de `SPEC-012` sin edición y su estado intacto — afecta a `RF-008` y `CA-008`.
- [x] `RF-009` y `CA-009`: orquestador que verifica, ejecuta validador, `git add` y `git commit` y no redacta artefactos, con 0 atribuciones de escritura sobre `specs/` y la retirada del permiso en `.opencode/agents/sdd.md` — afecta a `RF-009`, `CB-014` y `CA-009`.
- [x] `RF-003` y `CA-003`: 2 casillas por sección de aprobaciones y error ante una segunda casilla de la misma compuerta aunque no esté marcada — afecta a `RF-003`, `CB-006` y `CA-003`.
- [x] `RF-004` y `CA-004`: firma criptográfica del commit de aprobación verificada con la clave de `docs/sdd/firmantes_autorizados` y retirada de la afirmación contraria — afecta a `RF-004` y `CA-004`.
- [x] `RF-005` y `CA-005`: 2 ventanas de legado con su conjunto de specs, su conjunto de comprobaciones, su motivo y su límite, sin ampliación sin spec posterior — afecta a `RF-005`, `CB-011` y `CA-005`.
- [x] `RF-011` y `CA-011`: suite, 131 pruebas y ejecución en el job `verify` del flujo `SDD` — afecta a `RF-011` y `CA-011`.
- [x] `RF-014`, `RF-015`, `RF-016` y `CA-014`: estado de `MEMORY.md`, fila del informe de reauditoría en `docs/sdd/README.md` e historial de releases hasta el release anterior a `v0.7.0` — afecta a `RF-014`, `RF-015`, `RF-016`, `CB-013` y `CA-014`.
- [x] `RF-002` y `CA-002`: 7 etapas numeradas de 1 Specify a 7 Release, con 1 Specify como primera fila — afecta a `RF-002` y `CA-002`.
- [x] Caso borde nuevo `CB-016` incorporado al cuerpo de la spec y enlazado en la línea `Cubre:` de `CA-008` — afecta a `CB-016` y `CA-008`.
- [x] `## Actores y permisos` y `## Resultado esperado`: escritura de T4 a T7 por el `planner`, actos del orquestador y exigibilidad del check `verify` — afecta a `RF-009` y `RF-010`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-14 y `status` `clarified`; fila nueva en `## Historial de cambios` y fila T1 en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- El check exigible de la integración continua es el job `verify` del flujo `SDD`; su nombre es parte del contrato y no se renombra sin una spec posterior.
- La ancestría sustituye al conteo: `main` ancestro de `dev` y tag del release alcanzable desde `main`. El estado `48 0` deja de ser bloqueo y el historial no se pone al día por la fuerza para satisfacer un conteo.
- `docs/` se admite como prefijo de trabajo para cambios exclusivamente documentales, con la misma gramática que los demás prefijos y con la misma longitud de 3 a 63 caracteres.
- Las 2 ventanas de legado son concesiones cerradas: la estructural alcanza `SPEC-001` a `SPEC-009` para C-01 a C-13 y la de trazabilidad alcanza `SPEC-008` a `SPEC-011` para C-14 a C-18. Ninguna se amplía sin una spec posterior.
- La escritura de T4 a T7 corresponde al `planner` porque es el rol con permiso de escritura en `specs/`; el orquestador verifica, registra y ejecuta `git add` y `git commit`, y no redacta.
- El cierre de integración de `SPEC-008` a `SPEC-011` es append-only: se añade la sección sin tocar matriz ni dictamen, y el estado `validated` se conserva.
- El historial de releases de `CHANGELOG.md` se completa hasta el release anterior a `v0.7.0`, que es el último publicado. `v0.7.0` queda fuera de esta spec.
- La corrección de una afirmación documental no cambia el rango ni el carácter del documento que la contiene.
- El validador acredita estructura, coherencia y trazabilidad declarada; no acredita la conformidad del régimen ni sustituye la firma del propietario en G1 ni en G4.

Valores fijados del cierre de integración:

| Spec | `Merge:` | `Release:` |
|---|---|---|
| `SPEC-008` | `49caac9` | vacía |
| `SPEC-009` | `09eaf34` | vacía |
| `SPEC-010` | `94c2ea1` | vacía |
| `SPEC-011` | `9df8446` | vacía |

Tags anotados publicados que el historial de `CHANGELOG.md` debe declarar: `v0.1.0`, `v0.2.0`, `v0.3.0`, `v0.3.1`, `v0.4.0`, `v0.5.0`, `v0.5.1` y `v0.6.0`, en ese orden y con 8 filas.
