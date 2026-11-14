# Plan técnico — SPEC-013

*Artefacto de rango 6: diseño de las dieciséis correcciones de `SPEC-013`, con las decisiones `DEC-NNN`, los contratos de cada corrección y la matriz de cobertura de la spec.*

## Referencias

- `spec.md`: `SPEC-013`, versión 0.2.0, estado `clarified`, con dieciséis requisitos funcionales, ocho no funcionales, dieciséis casos borde y dieciocho criterios de aceptación; G1 firmada en el commit `c61432d`.
- `clarify.md`: `SPEC-013`, cerrado con `AMB-001` a `AMB-012` resueltos y los valores del cierre de integración fijados.
- `docs/sdd/auditoria_cierre_v0_7_0.md`: observaciones `AUD-008`, `AUD-015`, `AUD-024`, `AUD-036`, `AUD-037`, `AUD-045`, `AUD-046`, `AUD-056`, `AUD-065`, `AUD-073`, `AUD-074`, `AUD-085`, `AUD-086`, `AUD-095`, `AUD-096` y `AUD-097`.
- `docs/constitution.md`: rangos, prohibición de modificar requisitos para ajustarlos al código y registro de G6.
- `AGENTS.md`: cadena `RF/CB → CA → T → evidencia`, seis roles y prohibición de declarar compuertas.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §5 máquina de estados y escritura de estados, §6 compuertas, §11 aprobaciones y firma, §12 roles y permisos, §13 integración y release, §14 contrato del validador.
- `docs/Flujo_de_Trabajo_Git.md`: ramas, gramática de nombres, sincronización, tag anotado y protección remota.
- `docs/sdd/plantillas/plan.md` y `docs/sdd/plantillas/informe_auditoria.md`: forma de este artefacto y del informe que acredita el cierre.
- Estado observado del repositorio: `.github/workflows/sdd.yml` con job `verify` y sin preparación del árbol; `tools/git/protection_rules/main.json` y `dev.json` con `required_status_checks` nulo; `tools/sdd/validate.py` con `check_approval_form` que detecta la duplicidad solo cuando está marcada y con `check_commit_references` acotado a `merge-base(HEAD, dev)`; `tools/sdd/tests` con 131 pruebas; ocho tags anotados de `v0.1.0` a `v0.6.0`; 42 commits de implementación posteriores a `v0.6.0`, y el conjunto de los 42 declara la cadena `Spec: SPEC-NNN` en su cuerpo.

## Naturaleza del entregable

La spec produce una combinación declarada de documentos normativos, implementación verificable y registros de spec:

- Documentos normativos de rango 2, rango 3 y rango 4: `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `docs/Flujo_de_Trabajo_Git.md`.
- Implementación verificable de rango 7: `.github/workflows/sdd.yml`, `tools/git/protection_rules/main.json`, `tools/git/protection_rules/dev.json`, el comparador de `tools/git/verify_branch_protection.py`, `tools/sdd/validate.py`, la suite de `tools/sdd/tests/` y los archivos de rol de `.opencode/agents/`.
- Registros de spec de rango 6: la sección `## Cierre de integración` de cuatro reportes publicados y la retirada de las casillas residuales de `SPEC-010` y `SPEC-011`.
- Documentos sin rango: guías de `docs/sdd/`, `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md`.
- El contrato de esta spec en `specs/013-cierre-reauditoria-conformidad/`.

No produce scripts `.bat`, no modifica la constitución, no altera el orden de precedencia, no toca `llama.cpp/`, `models/` ni `bin/` y no cambia el estado de `SPEC-008` a `SPEC-012`.

## Arquitectura

### Componentes, responsabilidad y límite

| Componente | Artefacto | Responsabilidad | Límite | Rol que escribe |
|---|---|---|---|---|
| Flujo de integración continua | `.github/workflows/sdd.yml` | Prepara el árbol, instala Python, ejecuta el validador y la suite en cada Pull Request | No publica, no etiqueta y no usa secretos | `coder` |
| Reglas de protección | `tools/git/protection_rules/main.json`, `dev.json` y el comparador de `tools/git/verify_branch_protection.py` | Declaran exigible el check `verify` y comparan la regla declarada con la remota | Solo lectura del remoto; no modifica la configuración por una vía distinta de la herramienta existente | `coder` |
| Norma de integración | `docs/Flujo_de_Trabajo_Git.md` | Fija exigibilidad del check, gramática de cinco prefijos, sincronización por ancestría y alcance del tag | No fija reglas del ciclo SDD ni de las compuertas | `documenter` |
| Norma ejecutable | `docs/sdd/PROTOCOLO_OPERATIVO.md` | Fija escritura de T4 a T7, autoridad del orquestador, firma verificada, dos ventanas de legado y sincronización | No cambia el orden de precedencia ni el contenido de la constitución | `documenter` |
| Norma operativa | `AGENTS.md` | Declara la firma verificada y la autoridad del orquestador | Conserva su longitud declarada y sus seis roles | `documenter` como delegado del propietario |
| Matriz de agentes | `.opencode/agents/sdd.md`, `coder.md` y `documenter.md` | Siete etapas numeradas, 0 escrituras del orquestador sobre `specs/`, y escritura de las rutas que el contrato de la spec atribuye a `coder` y a `documenter` | No concede aprobación de compuerta alguna | `sdd`, única ruta con escritura sobre `.opencode/` |
| Validador | `tools/sdd/validate.py` | Cierra C-09, C-13, C-16 y C-17 según los contratos de este plan | No verifica la veracidad de la evidencia ni la conformidad del régimen | `coder` |
| Suite del mecanismo | `tools/sdd/tests/test_validate.py` y `tools/sdd/tests/test_agent_permissions.py` | Ejercita cada corrección con caso positivo y caso negativo | No escribe archivos versionados ni consulta el remoto | `coder` |
| Registros de spec validadas | Los cuatro `validation_report.md` de `SPEC-008` a `SPEC-011` | Añaden la sección de cierre de integración | Append-only: no tocan matriz ni dictamen | `reviewer` |
| Casillas residuales | `specs/010-mecanismo-control-sdd/spec.md` y `specs/011-practica-operativa-sdd/spec.md` | Retiran la tercera casilla de G4 | Sección protegida: la escribe el propietario con un commit firmado | propietario |
| Documentos sin rango | Guías de `docs/sdd/`, `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md` | Encabezados de rango, estado de specs, fila del informe e historial de releases | No fijan reglas ni declaran compuertas | `documenter` |
| Contrato de la feature | `specs/013-cierre-reauditoria-conformidad/` | Declara requisitos, decisiones, tareas y evidencia | No reescribe requisitos publicados | `planner` |

### Orden de las correcciones

Las correcciones se ejecutan en un orden que evita que un control corregido declare en rojo un artefacto aún sin corregir:

1. Validador y suite: C-13 con detección de duplicidad no marcada, C-16 con el alcance nuevo, C-17 con el tag declarado en estado `validated` y C-09 con el check exigible. Cada una nace con su prueba en rojo.
2. Corrección del flujo y de las reglas de protección, con la prueba de estructura del flujo y la prueba del comparador.
3. Correcciones del protocolo, de `AGENTS.md` y de la norma de integración, con sus pruebas documentales.
4. Matriz de agentes: etapas del orquestador, retirada de su escritura sobre `specs/` y concesión de las rutas que el contrato atribuye a `coder` y a `documenter`.
5. Cierre de integración de las cuatro specs validadas y retirada de las dos casillas residuales, con el commit firmado del propietario.
6. Correcciones de los documentos sin rango y del registro de cambios.
7. Regresión completa: suite en verde, validador agregado con código 0 y contraste de las cinco specs publicadas.

La retirada de las casillas residuales se ejecuta antes del cierre de la etapa Implement, porque es la única corrección que depende de una firma del propietario y su ausencia dejaría un hallazgo de C-13 abierto.

### Procedimiento de trabajo

El validador se implementa con TDD estricto: se escribe la prueba negativa, se ejecuta en rojo, se implementa el mínimo que la satisface y se cierra con la suite en verde. Los documentos y las reglas de protección siguen validación-first: se ejecuta la comprobación vigente, se transcribe la afirmación que se va a corregir, se verifica el valor nuevo contra el historial local y solo después se escribe.

## Contratos

### C-1. Flujo de integración continua

| Elemento | Valor | Regla |
|---|---|---|
| Nombre del flujo | `SDD` | Encabezado `name` del archivo |
| Disparador | `pull_request` dirigido a `dev` y a `main` | Sin `push` y sin programación |
| Job | `verify` | Es el identificador del check exigible |
| Ejecutor | `windows-latest` | Sistema objetivo del proyecto |
| Límite del job | 5 minutos | Cota superior de `RNF-002` sobre la ejecución agregada |
| Preparación del árbol | `actions/checkout@v4` como primero de los pasos | Sin esta preparación no existen los archivos que el flujo valida |
| Preparación del entorno | `actions/setup-python@v5` con `python-version` 3.12 | Versión fijada |
| Validación | `python tools\sdd\validate.py --all` | Código de salida distinto de 0 detiene el job |
| Suite | `python -m unittest discover -s tools\sdd\tests -q` con `timeout-minutes` 1 | Código de salida distinto de 0 detiene el job |
| Permisos del flujo | `contents: read` | Sin secretos y sin escritura sobre el remoto |
| Efectos remotos | 0 | Sin `push`, `tag`, `fetch`, `release` ni despliegue |

### C-2. Reglas de protección y check exigible

| Elemento | Valor |
|---|---|
| Archivos | `tools/git/protection_rules/main.json` y `tools/git/protection_rules/dev.json` |
| Estructura | `required_status_checks` como objeto con `strict: true` y `checks` con una entrada de contexto `verify` |
| Valor declarado del contexto | `verify` |
| Forma presentada por la interfaz | `SDD / verify`; la comparación toma el segmento posterior a `/ ` y lo contrasta con `verify` |
| Aplicación | `python tools/git/configure_branch_protection.py --all` |
| Verificación | `python tools/git/verify_branch_protection.py --branches-only` |
| Ausencia de la regla | C-09 registra el bloqueo de G5 con la rama y el check ausente |
| Divergencia entre el archivo y el remoto | El comparador registra la discrepancia con el contexto esperado y el observado |

El comparador de `compare_protection_dicts` se extiende para contrastar el objeto declarado: `strict` y el conjunto de contextos. Cuando el valor esperado sea nulo conserva la detección actual de comprobaciones inesperadas.

### C-3. Sincronización previa al release

| Condición | Comando | Resultado que habilita |
|---|---|---|
| `main` es ancestro de `dev` | `git merge-base --is-ancestor main dev` | Código 0 |
| El tag del release es alcanzable desde `main` | `git merge-base --is-ancestor vX.Y.Z^{commit} main` | Código 0 |
| Conteo simétrico entre ramas | — | Retirado: no se exige y no se cita |
| Falta de ancestría | — | Detiene el empaquetado e informa la relación incumplida |
| Tag no alcanzable | — | Detiene el release y no declara la sincronización cumplida |

El estado `48 0` de `dev` respecto de `main` no se trata como bloqueo cuando la ancestría se cumple y el historial no se pone al día por la fuerza.

### C-4. Gramática de nombres de rama

| Elemento | Valor |
|---|---|
| Expresión | `^(feat|fix|hotfix|docs|release)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$` |
| Prefijos admitidos | `feat/`, `fix/`, `hotfix/`, `docs/` y `release/vX-Y-Z` |
| Caracteres | Minúsculas, números y guiones |
| Longitud de `<nombre>` | De 3 a 63 caracteres, sin contar el prefijo |
| Convención de release | `vX-Y-Z` con guiones y sin puntos |
| Prefijo fuera de la lista | Rechazado con el conjunto de prefijos admitidos |

| Nombre | Resultado |
|---|---|
| `docs/cierre-integracion-spec-012` | Admitido |
| `feat/reauditoria-cierre` | Admitido |
| `release/v0-7-0` | Admitido |
| `docs/Cierre-Integracion` | Rechazado por mayúscula |
| `docs/ab` | Rechazado por longitud menor que 3 |
| `docs/uno_dos` | Rechazado por guion bajo |
| `chore/limpieza` | Rechazado por prefijo fuera de la lista |

### C-5. Casilla de aprobación única (C-13)

| Situación en la sección de aprobaciones | Resultado |
|---|---|
| Una casilla de `G1` y una casilla de `G4` | Conforme |
| Dos casillas de `G4`, una marcada y una sin marcar | Error `C-13` de registro dual con el recuento y la compuerta |
| Dos casillas de `G1` marcadas | Error `C-13` de registro dual |
| Casilla marcada fuera de la sección | Error de ubicación |
| Casilla marcada sin la cadena exacta o sin fecha ISO | Error de forma |

La detección cuenta las casillas de cada compuerta dentro de la sección y no depende de que la casilla adicional esté marcada. El hallazgo declara la compuerta y el recuento, y la ruta del hallazgo identifica la spec.

### C-6. Alcance de la cadena `Spec: SPEC-NNN` (C-16)

| Paso | Regla |
|---|---|
| 1 | Se resuelve el último tag anotado de release: nombre que cumple `^v\d+\.\d+\.\d+$` y cuyo tipo es `tag`, ordenado por fecha de creación descendente |
| 2 | El punto de corte es ese tag cuando es ancestro de `HEAD` |
| 3 | Sin tag aplicable, el punto de corte es el ancestro común con `main` |
| 4 | Sin tag y sin ancestro común, el alcance es vacío |
| 5 | Los commits de merge se excluyen del alcance |
| 6 | El alcance son los commits posteriores al punto de corte; con punto vacío no se aplica el recuento de 50 commits |
| 7 | Un alcance vacío se informa como no aplicable y no produce error |
| 8 | Cada commit del alcance sin la cadena produce un error con su identificador abreviado |
| 9 | La comprobación informa el punto de corte y el número de commits examinados |

Medición previa en la rama `feat/reauditoria-cierre`: el alcance `v0.6.0..HEAD` comprende 42 commits de implementación y los 42 declaran la cadena, de modo que la comprobación corregida no añade hallazgos sobre el historial integrado. Cada commit de esta spec declara `Spec: SPEC-013` en su cuerpo para conservar esa condición.

### C-7. Cierre de integración del reporte (C-17)

| Elemento | Forma | Obligatoriedad |
|---|---|---|
| Encabezado | `## Cierre de integración` al final del reporte, después del dictamen | Obligatorio en `validated` y en `released` |
| `Merge:` | `Merge: <sha de 7 a 40 caracteres hexadecimales>` | Obligatorio en `validated` y en `released` |
| `Release:` | `Release:` vacía en estado `validated`; `Release: vMAJOR.MINOR.PATCH` en `released` | Obligatoria con valor solo en `released` |
| Tag declarado en estado `validated` | Error: el release no está publicado | Error de C-17 |
| Alteración de matriz o dictamen | Prohibida | La sección es append-only |

| Spec | `Merge:` | `Release:` |
|---|---|---|
| `SPEC-008` | `49caac9` | vacía |
| `SPEC-009` | `09eaf34` | vacía |
| `SPEC-010` | `94c2ea1` | vacía |
| `SPEC-011` | `9df8446` | vacía |

### C-8. Ventanas de legado

| Ventana | Specs | Comprobaciones | Motivo | Límite |
|---|---|---|---|---|
| Estructural | `SPEC-001` a `SPEC-009` | C-01 a C-13 | Las nueve specs se cerraron antes de que la base v2 exigiera forma de aprobación, cobertura y tarea abierta | No admite una spec posterior a `SPEC-009` y no alcanza una comprobación fuera de C-01 a C-13 |
| Trazabilidad | `SPEC-008` a `SPEC-011` | C-14 a C-18 | Las cuatro specs se validaron antes de que `SPEC-012` introdujera el enlace de tarea, la evidencia y el cierre de integración | No admite `SPEC-012` ni una spec posterior y no se amplía sin una spec nueva |

Una spec fuera de la ventana que le corresponde produce error y no se degrada a advertencia. La declaración del protocolo y las constantes `LEGACY_SPECS` y `TRACE_LEGACY_SPECS` del validador coinciden fila por fila.

### C-9. Escritura de estados

| Transición | Origen | Destino | Escritor | Evidencia habilitante |
|---|---|---|---|---|
| T1 | `draft` | `clarified` | `planner` | `clarify.md` sin casillas pendientes y parches aplicados |
| T2 | `clarified` | `planned` | `planner` | Línea de G1 firmada y `plan.md` con sus decisiones |
| T3 | `planned` | `tasked` | `planner` | `tasks.md` con cobertura completa |
| T4 | `tasked` | `implementing` | `planner` | Verificación de G2 registrada por el orquestador |
| T5 | `implementing` | `implemented` | `planner` | Verificación de G3 registrada por el orquestador |
| T6 | `implemented` | `validated` | `planner` | Dictamen convergido y G4 firmada |
| T7 | `validated` | `released` | `planner` | G5 y G6 registradas |

El `planner` escribe T4, T5, T6 y T7 sobre la verificación registrada por el orquestador. Sin esa verificación, la transición no se escribe y el `planner` informa la ausencia. Las filas T4, T5 y T6 del historial de `SPEC-012` conservan fecha, evidencia y secuencia, y su estado vigente no cambia.

### C-10. Matriz del orquestador

| Ruta | Efecto tras la corrección |
|---|---|
| `specs/**` | `deny` explícito: 0 atribuciones de escritura sobre `specs/` |
| `specs/INDEX.md` | Sin concesión |
| `specs/*/spec.md` | Sin concesión |
| `specs/*/validation_report.md` | Sin concesión |
| `.opencode/**` | `allow`, sin cambio |
| `.github/**` | `allow`, sin cambio |
| `MEMORY.md` | `allow`, sin cambio |
| `opencode.jsonc` | `allow`, sin cambio |
| Sección de aprobaciones | Prohibición conservada en el cuerpo del rol |

El orquestador conserva la verificación de compuertas, el registro de resultados, la ejecución del validador y `git add` y `git commit` de los artefactos de control. No redacta artefacto alguno ni declara aprobación.

### C-11. Correcciones documentales acotadas

| Documento | Corrección | Valor que se escribe |
|---|---|---|
| Guías de `docs/sdd/` | Encabezado con carácter y rango | `> **Documento de referencia (no normativo).** Su rango es «Sin rango» y no fija reglas. Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.` |
| `docs/sdd/guia_spec_md.md` | Denominación del criterio | `criterio de aceptación` en lugar de la forma anterior |
| `docs/sdd/guia_clarify_md.md` | Identificador de ejemplo | `CB-001` en lugar del identificador fuera de formato |
| `docs/sdd/referencia_7_etapas_sdd.md` | Título de la referencia | El título de la etapa de validación del ciclo vigente |
| `MEMORY.md` | Estado de specs | `- Estado de specs: `SPEC-001` a `SPEC-007` publicadas; `SPEC-008` a `SPEC-012` validadas; `SPEC-013` en curso con el estado de su frontmatter.` |
| `docs/sdd/README.md` | Fila de inventario | `| `auditoria_cierre_v0_7_0.md` | `docs/sdd/auditoria_cierre_v0_7_0.md` | Informe de auditoría | 33 | Sin rango |` |
| `CHANGELOG.md` | Historial de releases | Tabla de ocho filas con `Versión`, `Fecha` y `Tag`, en orden ascendente |

Historial de releases que se escribe:

| Versión | Fecha | Tag |
|---|---|---|
| `v0.1.0` | 2026-11-10 | `v0.1.0` |
| `v0.2.0` | 2026-11-12 | `v0.2.0` |
| `v0.3.0` | 2026-11-13 | `v0.3.0` |
| `v0.3.1` | 2026-11-13 | `v0.3.1` |
| `v0.4.0` | 2026-11-13 | `v0.4.0` |
| `v0.5.0` | 2026-11-13 | `v0.5.0` |
| `v0.5.1` | 2026-11-13 | `v0.5.1` |
| `v0.6.0` | 2026-11-13 | `v0.6.0` |

Una guía que ya declara carácter y rango y no conserva identificadores fuera de formato no se modifica y su conformidad previa se registra en la evidencia de la tarea y en el reporte de validación.

### C-12. Etapas del orquestador

| Número | Etapa | Precondición | Resultado esperado |
|---|---|---|---|
| 1 | Specify | Rama creada e identificador asignado | `spec.md` en `draft` |
| 2 | Clarify | `spec.md` en `draft` | `clarify.md` cerrado |
| 3 | Plan | G1 aprobada y spec en `clarified` | `plan.md` con decisiones |
| 4 | Tasks | Spec en `planned` | `tasks.md` con cobertura completa |
| 5 | Implement | G2 verificada y spec en `tasked` | Tarea cerrada con evidencia |
| 6 | Validate | G3 completa | `validation_report.md` con dictamen |
| 7 | Release | G4 aprobada y G5 cumplida | Release publicado con tag verificado |

## Decisiones técnicas

### DEC-001

- **Decisión:** el flujo `SDD` prepara el árbol con `actions/checkout@v4` antes de `actions/setup-python@v5`, ejecuta el validador y la suite en el job `verify` para cada Pull Request dirigido a `main` y a `dev`, y el check `verify` se declara exigible en `tools/git/protection_rules/main.json` y `dev.json` con `strict: true`. La exigibilidad se documenta en `docs/Flujo_de_Trabajo_Git.md` y se aplica y verifica con `configure_branch_protection.py` y `verify_branch_protection.py`.
- **Justificación:** `RF-010`, `CB-009`, `CB-010`, `CA-010` y `AUD-073` fijan la preparación del árbol, el nombre del job y la exigibilidad; el flujo actual ejecuta el validador sin los archivos que valida y deja `required_status_checks` en `null`, de modo que su resultado no condiciona la integración. El nombre del job ya es `verify`, y conservarlo evita renombrar el check que la norma de rango 4 va a declarar.
- **Alternativas descartadas:** mantener `required_status_checks` nulo y limitar la corrección al documento, porque la exigibilidad quedaría declarada sin aplicación y `CA-010` no se satisfaría; declarar el contexto como `SDD / verify`, porque el contexto que la API contrasta es el nombre del job y la forma compuesta es una presentación de la interfaz; invocar el validador desde un paso que descargue el repositorio por su cuenta, porque duplica la preparación del árbol que `actions/checkout` ya ejecuta.

### DEC-002

- **Decisión:** la sincronización previa al release se expresa como ancestría: `main` debe ser ancestro de `dev` y el tag del release debe apuntar a un commit alcanzable desde `main`. La comprobación se ejecuta con `git merge-base --is-ancestor` y no se exige conteo alguno entre las dos ramas.
- **Justificación:** `RF-012`, `CB-003`, `CB-004` y `AUD-085` fijan la relación de ancestría y retiran la exigencia del conteo; la salida `0 0` es inalcanzable cuando `dev` contiene trabajo no publicado, y en el commit reauditado la divergencia es de 48 commits por delante y 0 por detrás, de modo que la condición declarada detendría el release v0.7.0 sin defecto real.
- **Alternativas descartadas:** conservar `git rev-list --left-right --count dev...main` con salida `0 0`, porque exige publicar el trabajo pendiente para satisfacer un conteo y convierte la verificación en un bloqueo permanente; exigir solo que `dev` no esté por detrás de `main` mediante el mismo conteo, porque mantiene la lectura de dos números donde la relación de ancestría ya es concluyente; poner al día el historial con un rebase, porque la integración por `merge --no-ff` es la única admitida y el rebase está prohibido.

### DEC-003

- **Decisión:** la gramática de nombres de rama admite cinco prefijos —`feat/`, `fix/`, `hotfix/`, `docs/` y `release/vX-Y-Z`— con una sola expresión, la misma validación de minúsculas, números y guiones y la misma longitud de 3 a 63 caracteres sobre `<nombre>`. `docs/` se reserva a los cambios exclusivamente documentales.
- **Justificación:** `RF-013`, `CB-001`, `CB-002`, `CA-013` y `AUD-086` fijan la lista cerrada y la validación común; la solicitud de integración número 10 se integró desde `docs/cierre-integracion-spec-012`, una rama que la gramática vigente rechaza, de modo que la norma de rango 4 describía una práctica distinta de la observada.
- **Alternativas descartadas:** escribir una expresión por prefijo, porque duplica la validación y permite que una rama cumpla una regla y no otra; admitir `docs/` por la excepción editorial sin incorporarlo a la gramática, porque la excepción no crea prefijos y la rama seguiría fuera de la norma; admitir cualquier prefijo de una palabra seguida de `/`, porque abre la lista y `CA-013` exige rechazar un prefijo fuera de los cinco.

### DEC-004

- **Decisión:** el cierre de integración de `SPEC-008`, `SPEC-009`, `SPEC-010` y `SPEC-011` se añade como sección append-only al final de su reporte, con el merge de la tabla de C-7 y la línea `Release:` vacía; el estado `validated`, la matriz y el dictamen no cambian. La escribe el `reviewer`, único rol con escritura declarada sobre `specs/*/validation_report.md`.
- **Justificación:** `RF-006`, `CB-007`, `CB-008`, `CA-006` y `AUD-045` fijan la sección, los cuatro identificadores y la conservación del estado; el protocolo §13 exige el registro de G5 en el reporte y la ventana de legado degrada hoy la ausencia a advertencia, de modo que el registro de G5 de cuatro specs validadas no consta en el soporte declarado.
- **Alternativas descartadas:** asignar la sección al `planner`, porque su matriz deniega de forma explícita `specs/*/validation_report.md` y la atribución sería inejecutable; registrar el merge solo en `CHANGELOG.md`, porque el protocolo fija dos soportes y el reporte es el que acredita G5 de la spec afectada; reabrir las cuatro specs para declarar el cierre como cambio de contrato, porque introduce un cambio de requisito que `RNF-005` prohíbe.

### DEC-005

- **Decisión:** el alcance de la comprobación de `Spec:` se resuelve con el último tag anotado de release y, en su defecto, con el ancestro común con `main`; los merges se excluyen y un alcance vacío se informa como no aplicable sin error. Se retira el recuento de los últimos 50 commits.
- **Justificación:** `RF-007`, `CB-005`, `CA-007` y `AUD-046` fijan el punto de corte y la enumeración vacía; con `HEAD` en `dev` el cálculo anterior por `merge-base(HEAD, dev)` dejaba el rango vacío y el verde de la ejecución agregada no examinaba commit alguno. La medición previa del alcance `v0.6.0..HEAD` sobre esta rama comprende 42 commits y los 42 declaran la cadena, de modo que la corrección no introduce errores sobre el historial integrado.
- **Alternativas descartadas:** conservar el recuento de 50 commits como último recurso, porque un rango sin tag y sin ancestro común examinaría commits ajenos al cambio y `CB-005` exige informar la comprobación como no aplicable; usar `git describe` sin filtrar el tipo, porque devuelve tags ligeros y el contrato de release exige tags anotados; mantener `merge-base(HEAD, dev)` como primer criterio, porque sobre la rama de integración produce el rango vacío que `AUD-046` registra.

### DEC-006

- **Decisión:** la escritura de las transiciones T4, T5, T6 y T7 corresponde al `planner` sobre la verificación registrada por el orquestador. La tabla de §5 y la definición del rol orquestador se corrigen en ese sentido; las filas T4, T5 y T6 del historial de `SPEC-012` no se editan y su estado vigente no cambia.
- **Justificación:** `RF-008`, `CB-016`, `CA-008` y `AUD-056` fijan la atribución y la conservación del historial; el `planner` es el rol con escritura sobre `specs/**`, mientras el orquestador no tiene permiso de escribir artefactos, de modo que la atribución anterior era inejecutable sin contradecir la matriz de permisos.
- **Alternativas descartadas:** corregir las filas de `SPEC-012` para atribuirlas al orquestador, porque la spec está validada, su historial registra la fecha y la evidencia de cada transición y `RNF-005` prohíbe alterar sus requisitos, criterios y estado; dejar la tabla de §5 sin cambio y mantener la contradicción, porque `CB-014` exige que la transición quede atribuida al rol que `tasks.md` declara y la contradicción anula esa garantía; atribuir T4 a T7 al propietario, porque la aprobación y la verificación son actos distintos de la escritura del historial.

### DEC-007

- **Decisión:** el orquestador verifica compuertas, registra el resultado de cada verificación, ejecuta el validador y ejecuta `git add` y `git commit` de los artefactos de control; no redacta artefacto alguno. Su matriz pasa a declarar `specs/**` con efecto `deny` y pierde las concesiones sobre `specs/INDEX.md`, `specs/*/spec.md` y `specs/*/validation_report.md`. La prohibición de escribir la sección de aprobaciones se conserva en el cuerpo del rol.
- **Justificación:** `RF-009`, `CB-014`, `CA-009` y `AUD-065` fijan la separación entre la escritura de estado y la sección protegida; hoy §5 le atribuye T4 a T7, §12 le niega la escritura de documentos y `.opencode/agents/sdd.md` le concede la edición de `specs/*/spec.md`, de modo que la matriz y el cuerpo del rol se contradicen y la concesión alcanza la sección protegida.
- **Alternativas descartadas:** conservar la concesión sobre `specs/*/spec.md` y confiar en la prohibición del cuerpo, porque la concesión alcanza la sección de aprobaciones y la denegación explícita de la ruta es la única garantía verificable; retirar también las concesiones sobre `.opencode/**` y `.github/**`, porque no son artefactos de spec y su retirada impediría corregir el propio flujo de integración; conservar `specs/INDEX.md` como excepción, porque el índice es parte de `specs/` y el requisito exige 0 atribuciones sobre la ruta.

### DEC-008

- **Decisión:** la validación de la casilla de aprobación cuenta las casillas de cada compuerta dentro de la sección y registra un error de registro dual cuando hay más de una, con independencia de la marca. Las casillas residuales de `SPEC-010` y `SPEC-011` se retiran en la sección protegida con un commit firmado del propietario.
- **Justificación:** `RF-003`, `CB-006`, `CA-003` y `AUD-024` fijan el recuento y la detección de la casilla sin marcar; la comprobación actual solo detecta la duplicidad marcada, de modo que una tercera casilla con el marcador de plantilla queda fuera del control y dos specs validadas portan tres casillas en una sección que admite dos.
- **Alternativas descartadas:** detectar la duplicidad sin marcar mediante una comprobación nueva fuera de C-13, porque la ubicación única ya reside en C-13 y una segunda comprobación del mismo objeto abriría un identificador de ventana que `RF-005` no declara; retirar las casillas residuales desde el `planner`, porque la sección protegida solo la modifica el propietario con un commit firmado y la edición produciría un registro sin valor; admitir la casilla sin marcar como inofensiva, porque una segunda marca de G4 quedaría fuera del control de duplicidad.

### DEC-009

- **Decisión:** el contrato del validador declara dos ventanas de legado cerradas, con su conjunto de specs, su conjunto de comprobaciones, su motivo y su límite: la estructural alcanza `SPEC-001` a `SPEC-009` para C-01 a C-13, y la de trazabilidad alcanza `SPEC-008` a `SPEC-011` para C-14 a C-18. Una spec fuera de su ventana produce error.
- **Justificación:** `RF-005`, `CB-011`, `CA-005` y `AUD-037` fijan las dos ventanas y su límite; el validador ya acota las constantes a esos dos conjuntos y el protocolo no las declara, de modo que la exención existe sin motivo escrito y su amplitud depende de la lectura del código. La declaración por escrito convierte la exención en una concesión cerrada y contrastable.
- **Alternativas descartadas:** unificar las nueve specs en una sola ventana que alcance C-01 a C-18, porque obligaría a regularizar cuatro specs validadas fuera del alcance de esta spec y reabriría `RNF-005`; retirar la degradación y exigir las comprobaciones sobre las nueve specs, porque convertiría en error la historia cerrada que la cláusula de legado protege; declarar la ventana solo en el código, porque la norma de rango 3 quedaría sin el motivo y el límite que el requisito exige.

### DEC-010

- **Decisión:** las correcciones documentales se limitan a las afirmaciones señaladas: encabezado de carácter y rango en las guías, denominación del criterio de aceptación, identificador de ejemplo, título de la referencia del ciclo, estado de specs de `MEMORY.md`, fila del informe en `docs/sdd/README.md` y tabla del historial de releases en `CHANGELOG.md`. Cada afirmación se comprueba antes de escribirla y su verificación se repite con una prueba de documento.
- **Justificación:** `RF-001`, `RF-011`, `RF-014`, `RF-015`, `RF-016`, `RNF-008` y `AUD-008`, `AUD-074`, `AUD-095`, `AUD-096` y `AUD-097` fijan el alcance; las guías no son normativas y su corrección no puede cambiar el rango que la base les atribuye, de modo que la escritura se acota a la declaración del encabezado y a la forma de los ejemplos.
- **Alternativas descartadas:** reescribir las guías para alinearlas con las plantillas, porque excede el alcance de las dieciséis observaciones y el contenido didáctico no es un defecto de conformidad; elevar las guías a un rango normativo, porque contradice la tabla de autoridad de la base v2; completar el historial de releases hasta `v0.7.0`, porque ese release se ejecuta después de esta spec y su entrada permanece en `Unreleased`.

### DEC-011

- **Decisión:** la matriz de escritura de `.opencode/agents/` se alinea con los actores que `spec.md` declara: el `coder` recibe `edit .github/**` y el `documenter` recibe `edit MEMORY.md` y `edit CHANGELOG.md`, con la misma denegación explícita sobre `specs/`, `src/`, `tools/` y `.opencode/`. La corrección incluye las pruebas que fijan cada permiso y la alineación del diccionario de la matriz de pruebas.
- **Justificación:** `spec.md` atribuye al `coder` la escritura en `.github/` y al `documenter` la redacción de `MEMORY.md` y `CHANGELOG.md`, mientras la matriz vigente deniega esas tres rutas; por la precedencia de §2 del protocolo, el documento de rango 6 prevalece sobre la implementación de rango 7 y la divergencia se corrige en el código. Sin la corrección, dos de las diez correcciones no tendrían escritor con permiso y `CB-014` quedaría incumplido.
- **Alternativas descartadas:** asignar el flujo de integración y el registro de cambios al orquestador, porque `RF-009` le retira la escritura de artefactos y su matriz quedaría como único escritor de dos documentos que el contrato atribuye a otros roles; dejar la matriz sin cambio y ejecutar las correcciones con el propietario, porque el propietario declara aprobaciones y no es un rol de agente, de modo que la etapa Implement quedaría sin responsable; corregir solo `coder.md` y dejar `CHANGELOG.md` en `Unreleased`, porque `RF-016` exige el historial de ocho filas y el documento quedaría sin escritor.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Casilla de aprobación | `test_casilla_duplicada_sin_marcar_es_error`, `test_casilla_unica_por_compuerta` y `test_tercera_casilla_de_g4_en_spec_010` en `test_validate.py` | La casilla adicional sin marcar produce error `C-13`; la sección con dos casillas no produce hallazgo; `SPEC-010` y `SPEC-011` quedan sin hallazgo tras la retirada |
| Alcance de `Spec:` | `test_alcance_desde_ultimo_tag`, `test_alcance_sin_tag_usa_merge_base`, `test_alcance_vacio_no_aplicable`, `test_merges_excluidos_del_alcance` y `test_commit_sin_spec_en_alcance` | El alcance se resuelve por tag anotado y por ancestro común; los merges no se examinan; un alcance vacío no produce error y un commit sin la cadena produce error con su identificador |
| Cierre de integración | `test_cierre_de_spec_validada`, `test_release_declarado_en_validated_es_error` y `test_cierre_append_only_conserva_dictamen` | `validated` con `Release:` vacía no produce hallazgo; un tag declarado produce error; el dictamen no convergido se conserva |
| Check exigible en G5 | `test_reglas_de_proteccion_exigen_verify` y `test_proteccion_sin_check_bloquea_g5` | Las dos ramas declaran el contexto; la ausencia produce el bloqueo de G5 con la rama y el check |
| Estructura del flujo | `test_estructura_del_flujo` y `test_flujo_sin_preparacion_del_arbol` | El flujo declara `actions/checkout`, dos pasos de ejecución y los límites; el flujo sintético sin preparación produce hallazgo |
| Comparador de protección | `test_required_status_checks_declarado` y `test_required_status_checks_divergente` en `tools/git/tests/test_verify_branch_protection.py` | El objeto declarado converge con el remoto; un contexto distinto produce discrepancia con los dos valores |
| Gramática de ramas | `test_gramatica_de_ramas` | Los cinco prefijos se admiten con la longitud de 3 a 63 caracteres; una mayúscula, un guion bajo, una longitud menor que 3 y un prefijo ajeno se rechazan |
| Matriz de agentes | `test_escritura_del_orquestador`, `test_escritura_del_coder`, `test_escritura_del_documenter` y `test_tabla_de_etapas_del_orquestador` | El orquestador no escribe bajo `specs/`; el `coder` escribe `.github/`; el `documenter` escribe los dos documentos de raíz; la tabla declara siete etapas de 1 a 7 |
| Documentos normativos | `test_contrato_de_firma_verificada`, `test_ventanas_de_legado`, `test_tabla_de_escritura_de_estados`, `test_sincronizacion_por_ancestria` y `test_documentacion_operativa` | La firma figura entre las comprobaciones verificadas; las dos ventanas coinciden con las constantes; la tabla atribuye T4 a T7 al `planner`; la sincronización no cita el conteo; la suite se declara existente |
| Documentos sin rango | `test_guias_del_corpus`, `test_consistencia_documental` y `test_inventario_del_corpus` | Cada guía declara carácter y rango; `MEMORY.md` coincide con `INDEX.md` y con el frontmatter; el informe de reauditoría tiene fila y no queda archivo sin fila |
| Historial de releases | `test_historial_de_releases` | Las ocho filas declaran versión, fecha y tag en orden ascendente |
| Regresión de la suite | `python -m unittest discover -s tools\sdd\tests -q` | La suite vigente más las pruebas nuevas en verde, con código 0 |
| Regresión del corpus | `python tools\sdd\validate.py --all` | Código 0, sin errores, con las advertencias de legado declaradas y sin advertencia de cierre en `SPEC-008` a `SPEC-011` |
| Protección remota | `python tools\git\verify_branch_protection.py --branches-only` | Convergencia con el archivo declarado en `main` y en `dev`, con el check `verify` exigible |
| Contraste de las specs publicadas | `git diff` de `SPEC-008` a `SPEC-012` contra su versión anterior | Diferencia limitada a la sección de cierre añadida y a las casillas retiradas; 100 % de requisitos, criterios y estados sin cambio |
| Determinismo | Dos ejecuciones de `python tools\sdd\validate.py --all` sobre el mismo commit | 0 diferencias en el conjunto de hallazgos |
| Duración | Tiempo medido de la ejecución agregada y del job `verify` | 300 segundos o menos en la ejecución agregada |
| Sin red | Revisión de las llamadas del validador y del comparador | Sin acceso a red, servicio externo ni credencial; códigos de salida 0, 1 y 2 conservados |

- El validador se implementa con TDD: cada corrección nace con su prueba negativa en rojo, se implementa el mínimo que la satisface y se cierra con la suite en verde.
- Las correcciones documentales siguen validación-first: se transcribe la afirmación vigente, se verifica el valor nuevo contra el historial local y solo después se escribe.
- La verificación previa de los cuatro merges y de los dos tags se ejecuta con consultas de solo lectura al historial antes de transcribir valor alguno.
- La retirada de las dos casillas residuales se verifica con `python tools\sdd\validate.py --spec SPEC-010` y `--spec SPEC-011` después del commit firmado del propietario.
- No se produce script `.bat`, de modo que no aplica la declaración previa de comando, salida y métricas de la validación-first de scripts.
- La salida de cada ejecución se transcribe en la evidencia de su tarea y en el reporte de validación de esta spec.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | Guías de `docs/sdd/` (encabezado, denominación e identificadores) | `test_guias_del_corpus` y contraste por archivo con la constancia de conformidad previa |
| `RF-002` | Tabla de etapas de `.opencode/agents/sdd.md` | `test_tabla_de_etapas_del_orquestador` |
| `RF-003` | C-13 en `tools/sdd/validate.py` y secciones de aprobaciones de `SPEC-010` y `SPEC-011` | `test_casilla_duplicada_sin_marcar_es_error`, `test_casilla_unica_por_compuerta` y `--spec SPEC-010` con `--spec SPEC-011` |
| `RF-004` | §14 del protocolo y `AGENTS.md` | `test_contrato_de_firma_verificada` |
| `RF-005` | §14 del protocolo y constantes `LEGACY_SPECS` y `TRACE_LEGACY_SPECS` | `test_ventanas_de_legado` y `test_legado_spec_nueva_error_con_codigo_1` |
| `RF-006` | C-17 en `tools/sdd/validate.py` y cuatro reportes publicados | `test_cierre_de_spec_validada`, `test_release_declarado_en_validated_es_error` y `--all` |
| `RF-007` | C-16 en `tools/sdd/validate.py` | `test_alcance_desde_ultimo_tag`, `test_alcance_sin_tag_usa_merge_base`, `test_alcance_vacio_no_aplicable`, `test_merges_excluidos_del_alcance` y `test_commit_sin_spec_en_alcance` |
| `RF-008` | §5 del protocolo y §12 del rol orquestador | `test_tabla_de_escritura_de_estados` y `git diff` del historial de `SPEC-012` |
| `RF-009` | §12 del protocolo y `.opencode/agents/sdd.md` | `test_escritura_del_orquestador` |
| `RF-010` | `.github/workflows/sdd.yml`, reglas de protección y norma de rango 4 | `test_estructura_del_flujo`, `test_reglas_de_proteccion_exigen_verify` y `verify_branch_protection.py --branches-only` |
| `RF-011` | Norma de rango 4 (suite del mecanismo) | `test_documentacion_operativa` |
| `RF-012` | Norma de rango 4 y §13 del protocolo | `test_sincronizacion_por_ancestria`, `git merge-base --is-ancestor main dev` y `git merge-base --is-ancestor v0.6.0^{commit} main` |
| `RF-013` | Norma de rango 4 y `AGENTS.md` | `test_gramatica_de_ramas` |
| `RF-014` | `MEMORY.md` | `test_consistencia_documental` |
| `RF-015` | `docs/sdd/README.md` | `test_inventario_del_corpus` |
| `RF-016` | `CHANGELOG.md` | `test_historial_de_releases` |
| `RNF-001` | Informe de la reauditoría posterior | Informe del rol de auditoría con veredicto por dimensión y recuento de observaciones |
| `RNF-002` | Ejecución agregada y job `verify` | Tiempo medido y transcrito, con el límite de 5 minutos del job |
| `RNF-003` | Validador | Dos ejecuciones sobre el mismo commit con 0 diferencias |
| `RNF-004` | `tools/sdd/tests/` | Recuento de las pruebas nuevas con su pareja positiva y negativa |
| `RNF-005` | `SPEC-008` a `SPEC-012` | `git diff` de cada spec contra su versión anterior |
| `RNF-006` | Validador y comparador | Revisión de las llamadas y ejecución de `test_codigo_0_sin_hallazgos`, `test_codigo_1_error_de_validacion` y `test_codigo_2_error_de_uso_sin_argumentos` |
| `RNF-007` | Documentos de rango 2, rango 3 y rango 4 | `test_contrato_de_firma_verificada`, `test_sincronizacion_por_ancestria` y `test_documentacion_operativa` |
| `RNF-008` | Encabezados de los documentos corregidos | `test_guias_del_corpus` y contraste del encabezado de cada documento |
| `CB-001` | Gramática de ramas | `test_gramatica_de_ramas` con mayúscula, guion bajo y carácter especial |
| `CB-002` | Gramática de ramas | `test_gramatica_de_ramas` con longitud menor que 3 y mayor que 63 |
| `CB-003` | Norma de rango 4 y §13 del protocolo | `git merge-base --is-ancestor main dev` y contraste del texto que detiene el empaquetado |
| `CB-004` | Norma de rango 4 y §13 del protocolo | `git merge-base --is-ancestor v0.6.0^{commit} main` y contraste del texto que detiene el release |
| `CB-005` | C-16 en `tools/sdd/validate.py` | `test_alcance_vacio_no_aplicable` |
| `CB-006` | C-13 en `tools/sdd/validate.py` | `test_casilla_duplicada_sin_marcar_es_error` |
| `CB-007` | C-17 y sección append-only del reporte | `test_cierre_append_only_conserva_dictamen` |
| `CB-008` | C-17 en `tools/sdd/validate.py` | `test_release_declarado_en_validated_es_error` |
| `CB-009` | `.github/workflows/sdd.yml` | `test_flujo_sin_preparacion_del_arbol` y ejecución de la validación agregada sobre un árbol sin `specs/` |
| `CB-010` | C-09 y reglas de protección | `test_proteccion_sin_check_bloquea_g5` |
| `CB-011` | Constantes de las dos ventanas | `test_legado_spec_nueva_error_con_codigo_1` |
| `CB-012` | Guías de `docs/sdd/` | `test_guias_del_corpus` sobre una guía ya conforme y constancia en la evidencia de la tarea |
| `CB-013` | `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md` | `test_consistencia_documental` e `test_inventario_del_corpus` |
| `CB-014` | `.opencode/agents/sdd.md` | `test_escritura_del_orquestador` con el caso sintético de la concesión añadida |
| `CB-015` | Frontera de la corrección sobre specs publicadas | `git diff` de `SPEC-008` a `SPEC-012` y revisión de la frontera declarada en `tasks.md` |
| `CB-016` | §5 del protocolo y C-9 de este plan | `test_tabla_de_escritura_de_estados` y la regla de la verificación ausente |
