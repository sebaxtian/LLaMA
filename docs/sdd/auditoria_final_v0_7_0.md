# Informe de auditoría — reauditoría final y conformidad del régimen v2 antes del release v0.7.0

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-14 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), specs `SPEC-001` a `SPEC-013`, validador `tools/sdd/validate.py`, suites `tools/sdd/tests` y `tools/git/tests`, reglas declaradas de protección de ramas, flujo de integración continua, matriz de agentes de `.opencode/`, historial Git y registro de cambios.
- **Objeto:** determinar si las dieciséis observaciones de `docs/sdd/auditoria_cierre_v0_7_0.md` quedaron cerradas y si el régimen alcanza el veredicto `CONFORME`, con el release `v0.7.0` en estado pendiente declarado.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas, no aprueba compuertas y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `d49019050dd5e57156a95d7ee8b34e23a73886c9` (`Merge pull request #12 from sebaxtian/docs/cierre-integracion-spec-013`) |
| Rama | `docs/auditoria-final-v0-7-0`, creada desde `dev` en `d490190` (`.git/logs/HEAD:206`) |
| Fecha de corte | 2026-11-14 |
| Validador ejecutado | **No ejecutado en esta sesión.** El entorno de ejecución denegó la herramienta de shell («Permission denied: shell»), aunque el rol la admite en `.opencode/agents/auditor.md:74-79`. Las salidas transcritas que se citan provienen de `specs/013-cierre-reauditoria-conformidad/validation_report.md:14-17` y se identifican como evidencia de tercero |
| Entorno | Windows 11 (`win32`); lectura del árbol de trabajo y de los archivos de `.git`; sin ejecución de comandos |
| Rol ejecutor | `auditor` |

**Procedimiento.** Cinco pasos. Primero, lectura íntegra de `docs/sdd/auditoria_cierre_v0_7_0.md` y enumeración de sus dieciséis observaciones nuevas con su severidad de origen. Segundo, contraste de cada observación con su artefacto de cierre, su norma aplicable en el rango correspondiente y su evidencia por ruta y línea. Tercero, lectura de la base v2 completa, de las trece specs y de su frontmatter. Cuarto, verificación específica de los diez puntos del encargo: flujo de integración continua, reglas de protección y comparador, regla de sincronización, gramática de ramas, atribución de las transiciones T4 a T7, declaración de firma, ventanas de legado, cierre de integración de los reportes y consistencia documental. Quinto, contraste cruzado de `AGENTS.md`, el protocolo y el flujo Git, y de `MEMORY.md`, `specs/INDEX.md` y el frontmatter.

Los identificadores `AUD-NNN` conservan el significado que les asignan `docs/sdd/auditoria_cumplimiento_sdd.md` y `docs/sdd/auditoria_cierre_v0_7_0.md`. Las observaciones nuevas continúan la numeración por dimensión conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md:216`; la dimensión nueva de integración continua ocupa el bloque `AUD-101` a `AUD-110`.

## 2. Base normativa e inventario

La jerarquía consta de siete rangos y una categoría sin rango, declarada de forma coincidente en `docs/constitution.md:48-59`, `docs/sdd/PROTOCOLO_OPERATIVO.md:29-38` y `docs/sdd/README.md:15-24`. La correspondencia entre los tres documentos se mantiene tras las correcciones de `SPEC-013`.

| Documento | Rango | Cita de la declaración |
|---|---|---|
| `docs/constitution.md` | 1 | `docs/constitution.md:3` y `:52` |
| `AGENTS.md` | 2 | `AGENTS.md:3`; `docs/constitution.md:53` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md:3` y `:33` |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | `docs/Flujo_de_Trabajo_Git.md:3`; `docs/constitution.md:55` |
| `docs/sdd/plantillas/*.md` | 5 | `docs/constitution.md:56`; `docs/sdd/README.md:21` |
| `specs/NNN-slug/*.md` | 6 | `docs/constitution.md:57`; `docs/sdd/README.md:22` |
| `src/`, `tools/`, `tests/`, `.opencode/` | 7 | `docs/constitution.md:58`; `docs/sdd/README.md:23` |
| Guías, informes, `README.md`, `MEMORY.md`, índice y `CHANGELOG.md` | Sin rango | `docs/constitution.md:59`; `docs/sdd/README.md:24` |

**Inventario.** La tabla de `docs/sdd/README.md:28-62` declara 33 filas de datos: 25 archivos Markdown de `docs/sdd/`, siete plantillas y el archivo de datos `firmantes_autorizados`. El árbol del commit auditado coincide con esa cifra (25 + 7 + 1), de modo que no registra archivo sin fila ni fila sin archivo **antes** de este informe. Este informe añade `docs/sdd/auditoria_final_v0_7_0.md` al directorio y queda sin fila en el corte; el hecho se registra en `AUD-098` y no se presume cumplido.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida de comando transcrita. Una afirmación de cierre exige la norma aplicable y el artefacto que la satisface; una afirmación de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento. Ningún resultado favorable del validador se interpreta como conformidad del régimen.

**Escala de veredicto.** Se aplica la escala de cinco valores de `docs/sdd/plantillas/informe_auditoria.md:29-37`: `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`. El informe previo empleó una variante de tres valores (`CONFORME`, `CONFORME CON OBSERVACIONES`, `NO CONFORME`); la equivalencia que se usa aquí es `CONFORME CON OBSERVACIONES` = `PARCIAL`, y se indica en el veredicto global para permitir la comparación entre versiones.

**Escala de severidad.** Cuatro niveles conforme a `docs/sdd/plantillas/informe_auditoria.md:39-46`: `Crítica` afecta la validez de una compuerta o de la base; `Alta` rompe una regla normativa sin invalidar la compuerta; `Media` produce divergencia entre documentos de distinto rango; `Baja` es un defecto de forma o de redacción.

**Estados de cierre.** `CERRADO` designa la observación cuya causa desapareció y cuenta con artefacto y evidencia. `CERRADO POR EXENCIÓN` designa la observación cuya causa se resolvió por una concesión declarada y acotada, con el efecto residual declarado por escrito. `PARCIAL` designa la observación cuya causa persiste en un subconjunto acotado. `VIGENTE` designa la observación sin tratamiento.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Observaciones |
|---|---|---|---|---|
| D1 | Autoridad normativa, vigencia y aplicabilidad de cada documento | `CONFORME` | `docs/constitution.md:48-59`; `docs/sdd/PROTOCOLO_OPERATIVO.md:29-47`; `docs/sdd/README.md:15-24`, `:28-62` | `AUD-008` cerrada; sin observación vigente |
| D2 | Ciclo de siete etapas y estado resultante | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:72-90`; `.opencode/agents/sdd.md:144-150` | `AUD-015` cerrada; sin observación vigente |
| D3 | Contratos de artefactos | `CONFORME` | `docs/sdd/plantillas/spec.md:67-72`; `docs/sdd/PROTOCOLO_OPERATIVO.md:167-203`; `tools/sdd/validate.py:447-572` | `AUD-024` cerrada; sin observación vigente |
| D4 | Compuertas G1 a G6: condición, evidencia y verificación | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:138-145`, `:302-316`; `docs/Flujo_de_Trabajo_Git.md:9-14`, `:448`, `:462`; `tools/sdd/validate.py:867-893`, `:922-997`, `:1646-1647` | `AUD-036` y `AUD-037` cerradas; `AUD-038` |
| D5 | Trazabilidad `RF/CB → CA → T → evidencia → commit → merge → release` | `CONFORME` | Seis reportes con `## Cierre de integración`; `tools/sdd/validate.py:1121-1247`, `:1280-1306` | `AUD-045` y `AUD-046` cerradas; sin observación vigente |
| D6 | Estados, transiciones e historial | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:92-132`; `tools/sdd/validate.py:93-104`, `:603-729`; `specs/012-trazabilidad-profunda-sdd/spec.md:339-341` | `AUD-056` cerrada; sin observación vigente |
| D7 | Roles y menor privilegio | `PARCIAL` | `.opencode/agents/auditor.md:1-99`; `.opencode/agents/sdd.md:44-58`, `:170-175`; `docs/sdd/PROTOCOLO_OPERATIVO.md:284-298` | `AUD-065` cerrada; `AUD-066` y `AUD-067` |
| D8 | Evidencia y verificación: existencia, suficiencia y reproducibilidad | `PARCIAL` | `.github/workflows/sdd.yml:10-25`; `specs/013-cierre-reauditoria-conformidad/validation_report.md:41`, `:80`; `docs/Flujo_de_Trabajo_Git.md:232` | `AUD-073` y `AUD-074` cerradas; `AUD-075` |
| D9 | Integración Git y release | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:300-320`; `docs/Flujo_de_Trabajo_Git.md:22-74`, `:256-264`; `CHANGELOG.md:24-26`, `:191-206` | `AUD-085` y `AUD-086` cerradas; release `v0.7.0` pendiente declarado |
| D10 | Consistencia documental operativa | `PARCIAL` | `MEMORY.md:13`; `specs/INDEX.md:7-19`; `docs/sdd/README.md:28-62`; `CHANGELOG.md:193-204` | `AUD-095` a `AUD-097` cerradas; `AUD-098` |
| D11 | Integración continua: ejecución, alcance y exigibilidad del job `verify` | `PARCIAL` | `.github/workflows/sdd.yml:1-25`; `tools/git/protection_rules/main.json`; `tools/git/protection_rules/dev.json`; `tools/git/verify_branch_protection.py:195-214`, `:325-353`; `tools/sdd/tests/test_agent_permissions.py:1041-1086` | `AUD-101` y `AUD-102` |

## 5. Hallazgos

Las tablas de §5.1 y §5.2 portan los seis campos de `docs/sdd/plantillas/informe_auditoria.md:56-65`: la columna `Dimensión` identifica la dimensión, la columna `Estado` o `Severidad` fija el veredicto y la severidad, la columna `Evidencia` cita ruta y línea, y la columna `Nota`, `Efecto observado` y `Destino` declaran la descripción y la remediación.

### 5.1 Cierre de las dieciséis observaciones de la reauditoría previa

| AUD-NNN | Dimensión | Severidad de origen | Estado | Evidencia del cierre | Nota |
|---|---|---|---|---|---|
| AUD-008 | D1 | Baja | `CERRADO` | `docs/sdd/guia_spec_md.md:3` y `:53`; `docs/sdd/guia_clarify_md.md:3` y `:126`; `docs/sdd/referencia_7_etapas_sdd.md:3`; búsqueda de «Definition of Done» y de `CB-NUEVO` en `docs/sdd/` sin coincidencia fuera de los dos informes de auditoría | Las doce guías y las tres referencias declaran carácter no normativo y rango «Sin rango» en la línea 3; el identificador de ejemplo pasó a `CB-001` y la denominación pasó a «criterio de aceptación». Los informes y los diagramas de `docs/sdd/` no declaran rango en su encabezado; la desviación está declarada en `specs/013-cierre-reauditoria-conformidad/validation_report.md:76`, queda fuera del alcance literal de `RF-001` y no constituye defecto bajo la regla de `docs/sdd/PROTOCOLO_OPERATIVO.md:45`, porque declaran carácter |
| AUD-015 | D2 | Baja | `CERRADO` | `.opencode/agents/sdd.md:144-150` | La tabla declara siete filas numeradas de `1 Specify` a `7 Release`, con `Release` en la séptima posición; no subsiste la tabla de seis etapas que comenzaba en 2 |
| AUD-024 | D3 | Media | `CERRADO` | `specs/010-mecanismo-control-sdd/spec.md:370-371`; `specs/011-practica-operativa-sdd/spec.md:332-333`; `tools/sdd/validate.py:455-458`; `tools/sdd/tests/test_validate.py:1579-1594` | Cada sección de aprobaciones declara dos casillas, G1 y G4; el registro dual se detecta por número de casillas declaradas, con independencia de que la adicional esté marcada, y la prueba negativa lo acredita |
| AUD-036 | D4 | Media | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:332`; `AGENTS.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:341`; `tools/sdd/tests/test_agent_permissions.py:1624-1643` | La firma criptográfica del commit de aprobación y la pertenencia de la clave figuran entre las comprobaciones verificadas en el rango 3 y en el rango 2, y desaparecen de la lista de comprobaciones no verificadas |
| AUD-037 | D4 | Media | `CERRADO POR EXENCIÓN` | `docs/sdd/PROTOCOLO_OPERATIVO.md:336-339` y `:355`; `tools/sdd/validate.py:91`, `:150` y `:154`; `tools/sdd/tests/test_agent_permissions.py:1645-1662` | Las dos ventanas quedan declaradas con su conjunto de specs, su conjunto de comprobaciones, su motivo y su límite, y coinciden con las constantes del validador. La degradación de C-01 a C-13 sobre `SPEC-001` a `SPEC-009` subsiste como concesión cerrada y declarada, no como omisión: su ampliación exige una spec posterior |
| AUD-045 | D5 | Media | `CERRADO` | `specs/008-auditoria-cumplimiento-sdd/validation_report.md:141-144`; `specs/009-base-normativa-sdd/validation_report.md:124-127`; `specs/010-mecanismo-control-sdd/validation_report.md:133-136`; `specs/011-practica-operativa-sdd/validation_report.md:92-95`; `tools/sdd/validate.py:1208-1231`; `tools/sdd/tests/test_validate.py:1435-1499` | Los cuatro reportes declaran la sección con su merge propio y `Release:` vacía; el dictamen y la matriz quedan sin alteración, y un tag declarado en estado `validated` produce error |
| AUD-046 | D5 | Media | `CERRADO` | `tools/sdd/validate.py:1250-1261`, `:1264-1277` y `:1280-1306`; `tools/sdd/tests/test_validate.py:1632-1674` | El alcance se fija en el último tag anotado ancestro de `HEAD` y, en su defecto, en el ancestro común con `main`; los merges se excluyen, el número de commits examinados se informa y el alcance vacío se declara no aplicable |
| AUD-056 | D6 | Media | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:129`; `specs/012-trazabilidad-profunda-sdd/spec.md:339-341` | §5 atribuye al `planner` la escritura de T4 a T7 sobre la verificación registrada por el orquestador, con la regla de no escribir sin esa verificación. Las filas T4, T5 y T6 de `SPEC-012` ya atribuían esas transiciones al `planner`, de modo que la contradicción desapareció sin editar el historial |
| AUD-065 | D7 | Media | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:286` y `:294`; `.opencode/agents/sdd.md:57`; `.opencode/agents/sdd.md:170` y `:175`; `tools/sdd/tests/test_agent_permissions.py:860-878` | Las atribuciones de escritura del orquestador sobre `specs/` son 0 y `specs/**` figura con efecto `deny` explícito; la concesión anterior sobre `specs/*/spec.md` desapareció y la prohibición de escribir la sección de aprobaciones se conserva. La contradicción restante fuera de `specs/` se registra en `AUD-066` |
| AUD-073 | D8 | Alta | `CERRADO` | `.github/workflows/sdd.yml:10-25`; `docs/Flujo_de_Trabajo_Git.md:448` y `:462`; `tools/git/protection_rules/main.json:2-9`; `tools/git/protection_rules/dev.json:2-9`; `tools/git/verify_branch_protection.py:195-214` y `:325-353`; `tools/sdd/validate.py:867-893` y `:1646-1647` | El job `verify` prepara el árbol con `actions/checkout@v4`, instala Python 3.12, ejecuta el validador y la suite; las dos ramas declaran `"strict": true` y el contexto `verify`; el comparador detecta la ausencia del check y `G5` queda bloqueada. El alcance efectivo de la ejecución se evalúa en `AUD-101` |
| AUD-074 | D8 | Baja | `CERRADO` | `docs/Flujo_de_Trabajo_Git.md:232` | La norma de rango 4 declara la suite del mecanismo de control, el recuento de 131 pruebas del corte de la auditoría con las añadidas después y su ejecución en el job `verify`; la afirmación de inexistencia desapareció |
| AUD-085 | D9 | Alta | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:308`; `docs/Flujo_de_Trabajo_Git.md:258-264` y `:385-392`; `AGENTS.md:71`; `tools/sdd/tests/test_agent_permissions.py:1677-1687` | La sincronización se expresa como ancestría de `main` respecto de `dev` y alcanzabilidad del tag desde `main`, y declara de forma expresa que `dev` puede estar por delante sin bloquear el release. La exigencia de conteo simétrico no subsiste en documento normativo: solo permanece citada como evidencia histórica en `docs/sdd/auditoria_cierre_v0_7_0.md:135` y en `docs/sdd/auditoria_cumplimiento_sdd.md:49`, documentos sin rango que `SPEC-013` prohíbe reescribir |
| AUD-086 | D9 | Media | `CERRADO` | `docs/Flujo_de_Trabajo_Git.md:29`, `:37`, `:49`, `:55`, `:58` y `:72`; `AGENTS.md:67`; `.opencode/agents/sdd.md:144` | La gramática admite cinco prefijos y somete `docs/` a las mismas reglas de minúsculas, números y guiones y a la misma longitud de 3 a 63 caracteres; el flujo de ramas y los ejemplos incorporan `docs/cierre-integracion-spec-012` |
| AUD-095 | D10 | Baja | `CERRADO` | `MEMORY.md:13`; `specs/INDEX.md:7-19`; `specs/013-cierre-reauditoria-conformidad/spec.md:4` | Los tres soportes declaran `SPEC-001` a `SPEC-007` publicadas y `SPEC-008` a `SPEC-013` validadas, con cero divergencias de estado |
| AUD-096 | D10 | Baja | `CERRADO` | `docs/sdd/README.md:61` | La fila del informe previo existe con su ruta, su carácter de informe de auditoría, el orden de lectura 32 y el rango «Sin rango», y la tabla declara 33 filas. La recurrencia por este informe se registra en `AUD-098` |
| AUD-097 | D10 | Baja | `CERRADO` | `CHANGELOG.md:191-204` y `:206` | El historial de releases declara ocho filas de `v0.1.0` a `v0.6.0` con versión, fecha y tag, y la publicación de `v0.7.0` figura como pendiente de la línea firmada del propietario |

**Recuento de cierre de las dieciséis:** 15 `CERRADO` y 1 `CERRADO POR EXENCIÓN` (`AUD-037`); 0 `PARCIAL` y 0 `VIGENTE`.

### 5.2 Observaciones nuevas

| AUD-NNN | Dimensión | Severidad | Evidencia | Efecto observado | Destino |
|---|---|---|---|---|---|
| AUD-038 | D4 | Media | `docs/sdd/PROTOCOLO_OPERATIVO.md:144` (fila G5 de §6) y `:302` (§13); `docs/Flujo_de_Trabajo_Git.md:448` y `:462`; `tools/sdd/validate.py:867-893` y `:1646-1647` | La condición de G5 del rango 3 no incluye el check `verify` exigible, que el rango 4 declara como condición de integración y cuyo incumplimiento el validador registra bloqueando G5. La norma que define la compuerta describe un conjunto de condiciones menor que el que la implementación exige, de modo que la lectura del verde de G5 depende de un documento desalineado | Spec de base que incorpore el check `verify` a la fila G5 de §6 y a §13 |
| AUD-066 | D7 | Media | `.opencode/agents/sdd.md:44-55`; `docs/sdd/PROTOCOLO_OPERATIVO.md:286` y `:294`; `specs/013-cierre-reauditoria-conformidad/spec.md:55-56`; `specs/013-cierre-reauditoria-conformidad/plan.md:200-214` y `:295-297` | El orquestador conserva `edit` con efecto `allow` sobre `.opencode/**`, `.github/**`, `opencode.jsonc` y `MEMORY.md`, mientras el rango 3 le niega escritura sobre documentos y código y declara que no redacta documento de raíz alguno, y el contrato de `SPEC-013` atribuye `.github/` al `coder` y `MEMORY.md` al `documenter`. La decisión técnica que conserva esas concesiones consta en el plan, de modo que la divergencia está declarada y no resuelta, y `RF-009` queda satisfecho en su cláusula de `specs/` e incumplido en la de ausencia de contradicción entre matriz y cuerpo del rol | Decisión del propietario: alinear §12 con la matriz o retirar las concesiones |
| AUD-067 | D7 | Baja | `docs/constitution.md:79`; `docs/sdd/PROTOCOLO_OPERATIVO.md:298`; `docs/sdd/plantillas/informe_auditoria.md:3`; `AGENTS.md:45`; `.opencode/agents/auditor.md:1-99` | Tres documentos de rango 1, 3 y 5 sitúan la implementación del rol de auditoría en el bloque B3 y condicionan la escritura del informe a que el rol no exista, mientras el rol está implementado y `AGENTS.md` lo declara. La condición es hoy falsa y no produce ambigüedad operativa, pero la base describe un estado superado | Corrección editorial de la atribución en los tres documentos |
| AUD-075 | D8 | Media | `specs/013-cierre-reauditoria-conformidad/validation_report.md:41` y `:80`; `specs/013-cierre-reauditoria-conformidad/spec.md:139` y `:335` | `RNF-001` y `CA-015` figuran en `PASADO` con la evidencia designada diferida a este informe. La evidencia existe ahora y no confirma la condición: las dieciséis observaciones están cerradas, pero cinco dimensiones conservan observación vigente. Además, el criterio fija por anticipado el veredicto que la auditoría debe emitir, de modo que su satisfacción depende del acto que pretende verificar y no de una condición independiente | Decisión del propietario sobre la fila y sobre el criterio; no se reabre requisito de `SPEC-013` |
| AUD-098 | D10 | Media | `docs/sdd/README.md:28-62` y `:67-68`; `tools/sdd/tests/test_agent_permissions.py:1520-1539`; `.opencode/agents/auditor.md:14-16` y `:50-52` | Este informe añade `docs/sdd/auditoria_final_v0_7_0.md` al corpus y la tabla de inventario no porta su fila. La prueba `test_inventario_del_corpus` enumera cada `*.md` del directorio y falla mientras la fila no exista, de modo que el check `verify` del Pull Request que transporte el informe queda en rojo; el rol de auditoría no puede editar `docs/sdd/README.md`, porque `docs/**` está denegado y la única concesión alcanza `docs/sdd/auditoria_*.md` | Añadir a la tabla de inventario la fila del informe por el propietario o `documenter`, antes de integrar |
| AUD-101 | D11 | Media | `.github/workflows/sdd.yml:15-16`; `tools/sdd/validate.py:1250-1261`, `:1264-1277` y `:1287-1300` | La preparación del árbol usa `actions/checkout@v4` sin `fetch-depth` ni `fetch-tags`, de modo que la copia es superficial y sin tags. `annotated_release_tags()` no devuelve tag anotado y `scope_point()` no encuentra punto de corte, con lo que la comprobación C-16 se informa como no aplicable y el job `verify` no examina commit alguno en materia de referencia a la spec | Spec de corrección del flujo que declare la profundidad y los tags |
| AUD-102 | D11 | Baja | `.github/workflows/sdd.yml:23-25`; `tools/git/tests/test_verify_branch_protection.py` y `tools/git/tests/test_remote_rejection.py` (48 casos de prueba); `docs/Flujo_de_Trabajo_Git.md:462` | El job `verify` ejecuta solo la suite de `tools/sdd/tests`; las 48 pruebas de `tools/git/tests`, incluidas las de rechazo de push directo y de fuerza sobre las ramas protegidas, no se ejecutan en job alguno y su resultado no forma parte del check exigible. La norma de rango 4 describe el check con ese alcance, de modo que la cobertura ausente no está declarada | Ampliación declarada del job o decisión del propietario sobre el alcance |

### 5.3 Recuento

| Clase | Recuento |
|---|---|
| Observaciones de la reauditoría previa | 16 |
| Cerradas con evidencia | 15 |
| Cerradas por exención declarada | 1 |
| Parciales | 0 |
| Vigentes | 0 |
| Observaciones nuevas | 7 |
| Observaciones nuevas de severidad `Crítica` | 0 |
| Observaciones nuevas de severidad `Alta` | 0 |
| Observaciones nuevas de severidad `Media` | 5 |
| Observaciones nuevas de severidad `Baja` | 2 |
| Hallazgos vigentes totales del régimen | 7 |

### 5.4 Comprobaciones específicas del encargo

| Comprobación | Resultado | Evidencia |
|---|---|---|
| El flujo prepara el árbol y ejecuta validador y suite en el job `verify` | Cumple | `.github/workflows/sdd.yml:10-25`: job `verify`, `actions/checkout@v4` como primera preparación, `actions/setup-python@v5` con 3.12, `python tools\sdd\validate.py --all` y `python -m unittest discover -s tools\sdd\tests -q`; disparo en `pull_request` sobre `dev` y `main` (`:3-5`); el alcance efectivo de la ejecución se registra en `AUD-101` y `AUD-102` |
| `main.json` y `dev.json` declaran `strict: true` y el contexto `verify`, y el comparador lo detecta | Cumple | `tools/git/protection_rules/main.json:2-9`; `tools/git/protection_rules/dev.json:2-9`; `tools/git/verify_branch_protection.py:195-214` normaliza `SDD / verify` al nombre del job y `:325-353` compara `strict` y el conjunto de contextos, con hallazgo cuando difieren |
| La regla de sincronización usa ancestría y alcanzabilidad del tag, sin conteo `0 0` | Cumple | `docs/sdd/PROTOCOLO_OPERATIVO.md:308`; `docs/Flujo_de_Trabajo_Git.md:258-264` y `:385-392`; `AGENTS.md:71`; la búsqueda de `rev-list --left-right` en `docs/` solo devuelve los dos informes de auditoría, documentos sin rango que la propia `SPEC-013` declara no reescribir |
| La gramática de ramas admite `docs/*` | Cumple | `docs/Flujo_de_Trabajo_Git.md:49` con cinco prefijos en la expresión, `:55` y `:58` con la misma regla de longitud y `:72` con el ejemplo; `AGENTS.md:67`; `tools/sdd/tests/test_agent_permissions.py:1139-1168` ejercita la admisión y los dos rechazos de `docs/` |
| Las transiciones T4 a T7 las escribe el `planner` y el orquestador no escribe artefactos | Cumple en la tabla y en el cuerpo del rol; divergencia de matriz en `AUD-066` | `docs/sdd/PROTOCOLO_OPERATIVO.md:129` y `:286`; `.opencode/agents/sdd.md:170` y `:175`; la contradicción residual fuera de `specs/` consta en `AUD-066` |
| La firma del commit de aprobación se declara verificada | Cumple por declaración; ejecución no verificada en esta sesión | `docs/sdd/PROTOCOLO_OPERATIVO.md:332` y `:341`; `AGENTS.md:77`; `docs/sdd/firmantes_autorizados:4-5` con una clave `ssh-ed25519` para dos identidades; la comprobación exige `git verify-commit` y `ssh-keygen -lf` (§9) |
| Las dos ventanas de legado están declaradas con motivo y límite | Cumple | `docs/sdd/PROTOCOLO_OPERATIVO.md:336-339` con las columnas `Motivo` y `Límite`; `:355` con la cláusula de cierre; coincidencia con `tools/sdd/validate.py:91` y `:150` verificada por `tools/sdd/tests/test_agent_permissions.py:1645-1662` |
| Los reportes de `SPEC-008` a `SPEC-013` declaran su cierre de integración | Cumple en seis de seis | `specs/008-auditoria-cumplimiento-sdd/validation_report.md:141-144`; `009:124-127`; `010:133-136`; `011:92-95`; `specs/012-trazabilidad-profunda-sdd/validation_report.md:83-86`; `specs/013-cierre-reauditoria-conformidad/validation_report.md:89-94` |
| `AGENTS.md`, el protocolo y el flujo Git no se contradicen | Cumple en las cinco afirmaciones corregidas; dos divergencias registradas | Coinciden en firma verificada (`AGENTS.md:77`; protocolo `:332`), autoridad del orquestador (`AGENTS.md:46`; protocolo `:286` y `:294`), ancestría (`AGENTS.md:71`; protocolo `:308`; flujo `:258-264`), gramática de cinco prefijos (`AGENTS.md:67`; flujo `:29` y `:49`) y ventanas de legado (protocolo `:336-339` y `:355`; validador `:91` y `:150`). Divergen en la condición de G5 (`AUD-038`) y en la matriz de escritura del orquestador (`AUD-066`) |
| `MEMORY.md`, `specs/INDEX.md` y los frontmatter coinciden | Cumple | `MEMORY.md:13`; `specs/INDEX.md:7-19`; `specs/013-cierre-reauditoria-conformidad/spec.md:4`; la comprobación ejecutable es `tools/sdd/tests/test_agent_permissions.py:1484-1514`, con el caso negativo que nombra documento y spec |
| Release `v0.7.0` | Pendiente declarado, no hallazgo | `CHANGELOG.md:11-26` mantiene `Unreleased` con el registro de G6 pendiente de la línea firmada; `CHANGELOG.md:206` declara la publicación pendiente; el historial de tags del corte alcanza `v0.6.0` (`CHANGELOG.md:204`) |

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría (`docs/constitution.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:278`).

| Compuerta | Evidencia observada | Límite de esta auditoría |
|---|---|---|
| G1 | Línea marcada de G1 en la sección de aprobaciones de las trece specs, por ejemplo `specs/013-cierre-reauditoria-conformidad/spec.md:361`; `tools/sdd/validate.py:447-475` comprueba forma, fecha ISO y ubicación | La firma del commit no se verificó por ejecución; la aprobación corresponde al propietario |
| G2 | `tasked` con cobertura completa en las specs posteriores a la base v2, con la verificación impresa por el validador según `specs/013-cierre-reauditoria-conformidad/validation_report.md:16` | Verificación automática no ejecutada en esta sesión |
| G3 | 44 tareas cerradas con evidencia en `specs/013-cierre-reauditoria-conformidad/tasks.md` y 48 en las siete specs publicadas | Verificación automática no ejecutada en esta sesión |
| G4 | Línea marcada de G4 en `specs/013-cierre-reauditoria-conformidad/spec.md:362` y reporte con dictamen `CONVERGIDO` en `specs/013-cierre-reauditoria-conformidad/validation_report.md:84`; la fila de `RNF-001` se evalúa en `AUD-075` | Declarante y firma no verificables aquí; la aprobación corresponde al propietario |
| G5 | Seis reportes con `## Cierre de integración` y su línea `Merge:`; merges citados `49caac9`, `09eaf34`, `94c2ea1`, `9df8446`, `b87e32c` y `e55fca1`, alcanzables desde `dev` según `.git/logs/HEAD:125-205` | La propiedad de dos padres de cada merge no se reejecutó; el estado del remoto no se consultó |
| G6 | Ocho tags anotados hasta `v0.6.0` con su entrada de release y su línea de aprobación; `v0.7.0` no existe y su G6 no está declarada | La auditoría no declara G6 ni crea el tag; la autorización corresponde al propietario |

## 7. Veredicto global

**Recuento de hallazgos vigentes:** 7 observaciones nuevas abiertas (0 `Crítica`, 0 `Alta`, 5 `Media` y 2 `Baja`) y 0 de las dieciséis observaciones previas sin cerrar.

**Regla aplicada.** Una dimensión es `PARCIAL` cuando conserva al menos una observación abierta de severidad `Media` o `Baja` cuyo efecto queda declarado; es `NO CONFORME` cuando conserva una observación de severidad `Alta` o `Crítica`, o una observación previa abierta. Ninguna dimensión registra observación de severidad `Alta` ni `Crítica` en este corte, y las dos que sostenían el `NO CONFORME` del informe previo —`AUD-073` en D8 y `AUD-085` en D9— están cerradas con artefacto y evidencia.

| Dimensión | Veredicto | Observación que lo sostiene |
|---|---|---|
| D1 | `CONFORME` | Ninguna vigente; `AUD-008` cerrada |
| D2 | `CONFORME` | Ninguna vigente; `AUD-015` cerrada |
| D3 | `CONFORME` | Ninguna vigente; `AUD-024` cerrada |
| D4 | `PARCIAL` | `AUD-038` (Media) |
| D5 | `CONFORME` | Ninguna vigente; `AUD-045` y `AUD-046` cerradas |
| D6 | `CONFORME` | Ninguna vigente; `AUD-056` cerrada |
| D7 | `PARCIAL` | `AUD-066` (Media) y `AUD-067` (Baja) |
| D8 | `PARCIAL` | `AUD-075` (Media) |
| D9 | `CONFORME` | Ninguna vigente; `AUD-085` y `AUD-086` cerradas; release pendiente declarado |
| D10 | `PARCIAL` | `AUD-098` (Media) |
| D11 | `PARCIAL` | `AUD-101` (Media) y `AUD-102` (Baja) |

**Veredicto global:** `CONFORME CON OBSERVACIONES`, equivalente a `PARCIAL` en la escala de `docs/sdd/plantillas/informe_auditoria.md:29-37`.

**Fundamento.** Las dieciséis observaciones de la reauditoría previa quedaron cerradas: quince con artefacto y evidencia, y `AUD-037` por exención declarada con motivo y límite. El defecto que impedía ejecutar el repositorio desde el flujo de integración continua desapareció (`AUD-073`) y la comprobación de sincronización dejó de exigir una salida imposible (`AUD-085`), de modo que las dos condiciones de severidad `Alta` que sostenían el `NO CONFORME` anterior ya no existen. El régimen no alcanza el valor `CONFORME` en sentido estricto porque permanecen siete observaciones abiertas de severidad `Media` y `Baja`: la condición de G5 del rango 3 no incorpora el check exigible (D4), la matriz del orquestador conserva escritura fuera de `specs/` y la base describe un rol de auditoría no implementado (D7), una fila de validación se apoya en evidencia diferida que no la confirma (D8), el corpus queda con un archivo sin fila mientras el rol que lo produce no puede editarlo (D10), y el job `verify` no ejerce las comprobaciones dependientes de Git ni la suite de `tools/git/tests` (D11). Ninguna de esas siete invalida una compuerta, y la primera acción de la hoja de ruta desbloquea la integración de este informe.

**Declaración expresa.** Este informe no aprueba compuerta alguna: no declara G1, G2, G3, G4, G5 ni G6, no emite línea de aprobación y no sustituye la firma del propietario ni su verificación. Registra el resultado de una reauditoría de conformidad y se limita a la evidencia citada. Un resultado favorable del validador o de la suite no acredita la conformidad del régimen ni autoriza un release.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| Registrar la fila de `docs/sdd/auditoria_final_v0_7_0.md` en la tabla de inventario de `docs/sdd/README.md` | `AUD-098` | corrección | Escritura del propietario o de `documenter`; desbloquea la integración de este informe |
| Incorporar el check `verify` a la fila G5 de §6 y a §13 del protocolo | `AUD-038` | spec de base | Ninguna |
| Decidir entre alinear §12 con la matriz del orquestador o retirar las concesiones sobre `.opencode/**`, `.github/**`, `opencode.jsonc` y `MEMORY.md` | `AUD-066` | spec de base | Decisión del propietario |
| Declarar la profundidad y los tags en `actions/checkout` del flujo `SDD` | `AUD-101` | corrección | Spec del flujo de integración continua |
| Decidir el alcance del job `verify` respecto de `tools/git/tests` | `AUD-102` | corrección o decisión | `AUD-101` |
| Resolver la fila de `RNF-001` y `CA-015` en `SPEC-013` sin reabrir requisito publicado | `AUD-075` | decisión de propietario | Ninguna |
| Corregir la atribución del bloque B3 en la constitución, el protocolo y la plantilla de auditoría | `AUD-067` | editorial | Ninguna |
| Ejecutar el validador y las dos suites sobre el commit del release y transcribir la salida en la entrada de `CHANGELOG.md` | Verificación de G6 | release | `AUD-098` resuelto y firmas verificadas |
| Registrar en la entrada del release de `CHANGELOG.md` el identificador de este informe, junto con la línea firmada de G6 | `docs/constitution.md:85-86`; `docs/sdd/PROTOCOLO_OPERATIVO.md:365-367` | release | Este informe registrado en el inventario y firmas verificadas |

## 9. Limitaciones

| Elemento | Causa | Evidencia o comprobación que faltaría |
|---|---|---|
| Ejecución del validador | El entorno de ejecución denegó la herramienta de shell; `python tools\sdd\validate.py --all` no se ejecutó en esta sesión, aunque el rol la admite en `.opencode/agents/auditor.md:74-75` | Salida literal del validador con su código de salida sobre `d490190` |
| Ejecución de las suites | Misma causa; los recuentos de 156 pruebas en `tools/sdd/tests` y 48 en `tools/git/tests` se obtuvieron por lectura y no por ejecución | Salida literal de `python -m unittest discover -s tools\sdd\tests -q` y de la suite de `tools/git/tests` |
| Verificación de las firmas de aprobación | Exige `git verify-commit` y `ssh-keygen -lf`, no ejecutados | Resultado de C-03 para los commits de G1 y G4 de las trece specs, con la huella contrastada contra `docs/sdd/firmantes_autorizados` |
| Propiedad de dos padres de los merges citados | Sin shell no se pudo leer `git show -s --format=%P`; la evidencia disponible es la secuencia de `.git/logs/HEAD:125-205` | Salida de `git log --merges -1 --format=%P` para `49caac9`, `09eaf34`, `94c2ea1`, `9df8446`, `b87e32c`, `e55fca1` y `d490190` |
| Estado remoto de la protección de ramas | La configuración remota no forma parte del repositorio y esta auditoría no consultó la API de reglas | Salida de `python tools/git/verify_branch_protection.py` con token válido |
| Comportamiento efectivo de `actions/checkout` en el flujo | `AUD-101` se sostiene en la ausencia de `fetch-depth` y `fetch-tags` en `.github/workflows/sdd.yml:15-16` y en el camino de código que informa «no aplicable»; la ejecución del flujo en GitHub no se observó | Registro de una ejecución del job `verify` con el punto de corte impreso por el validador |
| Contenido de `.env` | Fuera del alcance declarado | Procedimiento de gestión de secretos verificable |

Ningún elemento de esta lista se presume cumplido. La ausencia de la salida del validador y de la verificación de firmas impide acreditar por ejecución lo que los artefactos declaran, y esa ausencia no se sustituye por una suposición.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | Identificación del commit auditado y de la rama de trabajo | `d49019050dd5e57156a95d7ee8b34e23a73886c9`; `.git/logs/HEAD:205-206` |
| B | Secuencia de integración del cierre: `e55fca1` como merge de `feat/reauditoria-cierre`, `d490190` como merge de `docs/cierre-integracion-spec-013` | `.git/logs/HEAD:201-205` |
| C | Seis reportes con `## Cierre de integración`, su `Merge:` y su `Release:` vacía | `specs/008` a `specs/013`; rutas y líneas citadas en §5.1 y §5.4 |
| D | Declaración de las dos ventanas de legado con motivo y límite, y su coincidencia con las constantes del validador | `docs/sdd/PROTOCOLO_OPERATIVO.md:336-339`; `tools/sdd/validate.py:91` y `:150` |
| E | Flujo de integración continua: job `verify`, preparación del árbol, validador y suite | `.github/workflows/sdd.yml:1-25` |
| F | Reglas declaradas de protección con `strict: true` y contexto `verify`, y su comparación | `tools/git/protection_rules/main.json:2-9`; `tools/git/protection_rules/dev.json:2-9`; `tools/git/verify_branch_protection.py:195-214` y `:325-353` |
| G | Recuento de 156 pruebas en `tools/sdd/tests` y de 48 en `tools/git/tests` | Búsqueda de `def test_` en ambas rutas |
| H | Inventario del corpus: 33 filas de datos y 25 archivos Markdown más siete plantillas y el archivo de datos en el corte | `docs/sdd/README.md:28-62`; directorio `docs/sdd/` |
| I | Historial de releases con ocho filas y la publicación de `v0.7.0` declarada pendiente | `CHANGELOG.md:191-206` |
| J | Contrato de la auditoría de conformidad previa al release menor | `docs/constitution.md:85-86`; `docs/sdd/PROTOCOLO_OPERATIVO.md:365-367`; `docs/sdd/plantillas/informe_auditoria.md:1-93` |
