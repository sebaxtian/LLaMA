# Informe de auditoría — conformidad del régimen v2 en el estado publicado posterior al release v0.7.0

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, implementado en `.opencode/agents/auditor.md`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-20 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), specs `SPEC-001` a `SPEC-014`, validador `tools/sdd/validate.py`, suites `tools/sdd/tests` y `tools/git/tests`, matriz de agentes de `.opencode/`, flujo de integración continua, reglas declaradas de protección de ramas, historial Git local (`.git/logs/`, `.git/refs/`, `.git/packed-refs`, `.git/config`) y registro de cambios.
- **Objeto:** emitir el veredicto de conformidad del régimen completo en el estado publicado, verificar el cierre de las siete observaciones de `docs/sdd/auditoria_final_v0_7_0.md` y decidir si subsiste alguna observación previa.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas, no aprueba compuertas, no emite línea de aprobación y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `13e85e28ff35dbeb4bbbd75bdd8526677dc682e3` (`.git/refs/heads/dev:1`) |
| Rama | `dev`, en `13e85e2`; rama de trabajo `docs/auditoria-posterior-v0-7-0` creada desde ese commit (`.git/HEAD:1`; `.git/logs/HEAD:238`) |
| Fecha de corte | 2026-11-20. El encargo fijó 2026-11-14; el corte real de esta sesión es el 2026-11-20 (`.git/logs/HEAD:238`, marca `1795186859`), y la fecha se registra por la del corte efectivo |
| Validador ejecutado | `python tools\sdd\validate.py --all`: sin entradas `[ERROR]` y con advertencias `[WARN]` de la cláusula de legado en `C-07`, `C-13` y `C-14` sobre `SPEC-001` a `SPEC-009`; código de salida `0`. `python tools\sdd\validate.py --spec SPEC-014 --gate G6`: «OK: sin hallazgos.», código de salida `0` |
| Suites ejecutadas | `python -m unittest discover -s tools\sdd\tests -q`: «Ran 167 tests», con 1 fallo —`test_inventario_del_corpus`, que nombra `docs/sdd/auditoria_posterior_v0_7_0.md` como archivo sin fila, registrado en `AUD-099`—. `python -m unittest discover -s tools\git\tests -q`: «Ran 48 tests in 21.614s» y «OK» |
| Entorno | Windows 11 (`win32`); shell con la lista blanca del rol: `git status`, `log`, `show`, `diff`, `rev-parse`, `branch` y `merge-base`, además del validador y de `unittest`. `git cat-file`, `git tag` y `git config` quedaron denegados y se sustituyeron por `git rev-parse`, `git show` y la lectura de `.git/config` |
| Rol ejecutor | `auditor` |

**Procedimiento.** Seis pasos. Primero, lectura íntegra de `docs/sdd/auditoria_final_v0_7_0.md` y de su §5.2, con la enumeración de sus siete observaciones y de sus destinatarios de cierre. Segundo, contraste de cada observación con el artefacto que la satisface, su norma aplicable y su evidencia por ruta y línea en el commit auditado. Tercero, lectura de la base v2, de las catorce specs, de su frontmatter, del índice y de los registros sin rango. Cuarto, reconstrucción del proceso de release a partir de `.git/logs/HEAD`, de los reflogs de `main` y `dev`, de `.git/refs/`, de `.git/packed-refs` y de la salida de `git show`, `git rev-parse` y `git merge-base`, contrastada con `CHANGELOG.md`, `docs/Flujo_de_Trabajo_Git.md` y `tools/sdd/validate.py`. Quinto, examen de las once dimensiones y de los tres hechos posteriores al primer empaquetado. Sexto, ejecución del validador, de la compuerta G6 y de las dos suites, con la salida transcrita.

## 2. Base normativa e inventario

La jerarquía consta de siete rangos y una categoría sin rango, declarada de forma coincidente en `docs/constitution.md:48-59`, `docs/sdd/PROTOCOLO_OPERATIVO.md:29-38` y `docs/sdd/README.md:15-24`.

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

**Inventario.** La tabla de `docs/sdd/README.md:28-63` declara 34 filas de datos: 26 archivos Markdown de la raíz del corpus, siete plantillas y el archivo de datos `firmantes_autorizados`. El árbol del commit auditado coincide con esa cifra (26 + 7 + 1), de modo que no registra archivo sin fila ni fila sin archivo **antes** de este informe. Este informe añade `docs/sdd/auditoria_posterior_v0_7_0.md` al directorio y queda sin fila en el corte; el hecho se registra en `AUD-099` y se acreditó por ejecución de la suite.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida transcrita. Una afirmación de cierre exige la norma aplicable y el artefacto que la satisface; una afirmación de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento. Ningún resultado favorable del validador se interpreta como conformidad del régimen.

**Escala de veredicto.** Cinco valores conforme a `docs/sdd/plantillas/informe_auditoria.md:29-37`: `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`. Para conservar la comparación con las versiones previas se indica también la equivalencia `CONFORME CON OBSERVACIONES` = `PARCIAL`.

**Escala de severidad.** Cuatro niveles conforme a `docs/sdd/plantillas/informe_auditoria.md:39-46`: `Crítica` afecta la validez de una compuerta o de la base; `Alta` rompe una regla normativa sin invalidar la compuerta; `Media` produce divergencia entre documentos de distinto rango o entre un criterio y su evidencia; `Baja` es un defecto de forma o de redacción.

**Estados de cierre.** `CERRADO` designa la observación cuya causa desapareció y cuenta con artefacto y evidencia en el commit auditado. `PARCIAL` designa la observación cuya causa persiste en un subconjunto acotado. `VIGENTE` designa la observación sin tratamiento.

**Numeración.** Los identificadores nuevos continúan la serie por dimensión conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md:216`: D4 asigna `AUD-039`, D6 `AUD-057`, D7 `AUD-068`, D8 `AUD-076`, D9 `AUD-087` a `AUD-090` y D10 `AUD-099` y `AUD-100`. Ningún número asignado en las versiones previas se reutiliza.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Observaciones |
|---|---|---|---|---|
| D1 | Autoridad normativa, vigencia y aplicabilidad de cada documento | `CONFORME` | `docs/constitution.md:48-59`; `docs/sdd/PROTOCOLO_OPERATIVO.md:29-47`; `docs/sdd/README.md:15-24`, `:28-63`; `docs/sdd/guia_spec_md.md:3`; `docs/sdd/referencia_7_etapas_sdd.md:3` | `AUD-008` cerrada; sin observación vigente |
| D2 | Ciclo de siete etapas y estado resultante | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:72-90`; `.opencode/agents/sdd.md:142-150` | `AUD-015` cerrada; sin observación vigente |
| D3 | Contratos de artefactos y forma de cada uno | `CONFORME` | `docs/sdd/plantillas/spec.md:69-72`; `docs/sdd/plantillas/informe_auditoria.md:9-93`; `docs/sdd/PROTOCOLO_OPERATIVO.md:167-218`; `tools/sdd/validate.py:447-572` | `AUD-024` cerrada; sin observación vigente |
| D4 | Compuertas G1 a G6: condición, evidencia y verificación | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:138-145`, `:300-316`; `docs/Flujo_de_Trabajo_Git.md:9-14`, `:448`, `:462`; `tools/sdd/validate.py:778-861` | `AUD-036`, `AUD-037` y `AUD-038` cerradas; `AUD-039` |
| D5 | Trazabilidad `RF/CB → CA → T → evidencia → commit → merge → release` | `CONFORME` | Siete reportes con `## Cierre de integración` y su `Release: v0.7.0` (`specs/008` a `specs/014`); `tools/sdd/validate.py:1208-1247` | `AUD-045` y `AUD-046` cerradas; sin observación vigente |
| D6 | Estados, transiciones e historial de transiciones | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:92-132`; `specs/014-cierre-observaciones-finales/spec.md:219-230`; `tools/sdd/validate.py:603-729` | `AUD-056` cerrada; `AUD-057` |
| D7 | Roles y menor privilegio | `PARCIAL` | `.opencode/agents/sdd.md:44-55`, `:170-175`; `.opencode/agents/auditor.md:1-99`; `docs/sdd/PROTOCOLO_OPERATIVO.md:284-298` | `AUD-065`, `AUD-066` y `AUD-067` cerradas; `AUD-068` |
| D8 | Evidencia y verificación: existencia, suficiencia y reproducibilidad | `PARCIAL` | `tools/sdd/tests` (167 pruebas), `tools/git/tests` (48 pruebas); `specs/013-cierre-reauditoria-conformidad/validation_report.md:96-114`; `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335` | `AUD-073` y `AUD-074` cerradas; `AUD-075` parcial; `AUD-076` |
| D9 | Integración Git y release | `NO CONFORME` | `docs/Flujo_de_Trabajo_Git.md:256-394`; `CHANGELOG.md:13-44`; `git show -s --format=%s v0.7.0`; `git show --stat 5da6df6` | `AUD-085` y `AUD-086` cerradas; `AUD-087` a `AUD-090` |
| D10 | Consistencia documental operativa | `PARCIAL` | `MEMORY.md:13`; `specs/INDEX.md:7-20`; `docs/sdd/README.md:28-63`; `CHANGELOG.md:209-225` | `AUD-095` a `AUD-098` cerradas; `AUD-099` y `AUD-100` |
| D11 | Integración continua: ejecución, alcance y exigibilidad del job `verify` | `CONFORME` | `.github/workflows/sdd.yml:1-31`; `docs/Flujo_de_Trabajo_Git.md:232`, `:462`; `tools/git/protection_rules/main.json`, `dev.json` | `AUD-101` y `AUD-102` cerradas; sin observación vigente |

## 5. Hallazgos

### 5.1 Cierre de las siete observaciones del informe final

| AUD-NNN | Dimensión | Severidad de origen | Estado | Evidencia del cierre | Nota |
|---|---|---|---|---|---|
| `AUD-038` | D4 | Media | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:144` (fila G5 de §6) y `:302` (§13); `docs/Flujo_de_Trabajo_Git.md:448` y `:462`; `tools/sdd/tests/test_validate.py:1701` y `:1716` | La condición de G5 del rango 3 incorpora el check `verify` exigible con `strict: true` en `main` y en `dev`, y su ausencia bloquea la verificación; la prueba negativa `test_proteccion_sin_check_bloquea_g5` conserva el caso. El rango 4 mantiene el check en la tabla de protección y en el bloque de check exigible, y su fila G5 no lo enumera en la condición: el residuo se registra en `AUD-039` y no reabre `AUD-038` |
| `AUD-066` | D7 | Media | `CERRADO` | `.opencode/agents/sdd.md:44-55`; `docs/sdd/PROTOCOLO_OPERATIVO.md:286`, `:294`; `specs/014-cierre-observaciones-finales/spec.md:70-79`; `tools/sdd/tests/test_agent_permissions.py:972` y `:999` | La matriz del orquestador declara `edit` con efecto `allow` solo sobre `.opencode/**` y deniega de forma explícita `.github/**`, `opencode.jsonc` y `MEMORY.md`; las atribuciones de escritura fuera de `.opencode/**` son 0 y la contradicción con §12 desapareció |
| `AUD-067` | D7 | Baja | `CERRADO` | `docs/constitution.md:79`; `docs/sdd/PROTOCOLO_OPERATIVO.md:298`; `docs/sdd/plantillas/informe_auditoria.md:3`; `AGENTS.md:45` | Los tres documentos sitúan el rol en su implementación real de `.opencode/agents/auditor.md` y dejaron de condicionar la escritura del informe a que el rol no existiera |
| `AUD-075` | D8 | Media | `PARCIAL` | `specs/013-cierre-reauditoria-conformidad/validation_report.md:96-114`; `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335`; `specs/014-cierre-observaciones-finales/validation_report.md:20` | La nota de cierre append-only existe, transcribe el veredicto y declara 4 de 4 observaciones atendidas, de modo que la condición de decisión del propietario se cumplió. La causa persiste en un punto: las filas `RNF-001` y `CA-015` de `SPEC-013` conservan `PASADO` mientras la propia nota transcribe que su evidencia «no acredita el valor literal `CONFORME` ni la cláusula de diez de diez dimensiones». El residuo se registra en `AUD-076` |
| `AUD-098` | D10 | Media | `CERRADO` | `docs/sdd/README.md:62` (fila 33, `docs/sdd/auditoria_final_v0_7_0.md`, orden de lectura 33, «Sin rango»); `tools/sdd/tests/test_agent_permissions.py:1975-1987` | La fila del informe final existe y la tabla declara 34 filas para 34 archivos. La recurrencia por este informe se registra en `AUD-099` |
| `AUD-101` | D11 | Media | `CERRADO` | `.github/workflows/sdd.yml:15-19`; `docs/Flujo_de_Trabajo_Git.md:462`; `specs/014-cierre-observaciones-finales/validation_report.md:17` | La preparación del árbol declara `fetch-depth: 0` y `fetch-tags: true`, de modo que el punto de corte del alcance y la comprobación de la referencia a la spec disponen de historial y de etiquetas |
| `AUD-102` | D11 | Baja | `CERRADO` | `.github/workflows/sdd.yml:29-31`; `docs/Flujo_de_Trabajo_Git.md:232` y `:462`; `tools/git/tests` (48 pruebas en verde) | El job `verify` ejecuta `tools/sdd/tests` y `tools/git/tests` como pasos nombrados con `timeout-minutes: 1` cada uno, y la norma de rango 4 declara ese alcance |

**Recuento de las siete:** 6 `CERRADO` y 1 `PARCIAL`; 0 `VIGENTE`.

### 5.2 Observaciones nuevas

| AUD-NNN | Dimensión | Severidad | Evidencia | Efecto observado | Destino |
|---|---|---|---|---|---|
| `AUD-039` | D4 | Baja | `docs/Flujo_de_Trabajo_Git.md:11` frente a `:448` y `:462`; `docs/sdd/PROTOCOLO_OPERATIVO.md:144`, `:302` | La fila G5 de la tabla de compuertas del rango 4 enumera como condición la aprobación de G4, la spec en `validated`, el Pull Request con `merge --no-ff` y la validación posterior sin hallazgos, y omite el check `verify`, que el mismo documento declara exigible en `:448` y cuyo incumplimiento `:462` hace bloquear G5. La definición de la compuerta en el rango 4 queda más estrecha que su propia regla y que la del rango 3 | Corrección de alineación del rango 4: incorporar el check a la condición de la fila sin alterar la regla ya declarada |
| `AUD-057` | D6 | Media | `specs/014-cierre-observaciones-finales/spec.md:230`; `docs/sdd/PROTOCOLO_OPERATIVO.md:119`; `CHANGELOG.md:44` | La transición T7 de `SPEC-014` se registra con la evidencia «release v0.7.0 empaquetado con tag anotado pendiente de la firma de G6», mientras el estado publicado ya existe y la línea de registro de G6 figura en la entrada del release. La evidencia transcrita no es la que §5 exige para T7 —tag anotado verificado y línea de G6 firmada—, de modo que el historial de transiciones de una spec publicada declara un estado que el propio repositorio contradice | Decisión del propietario: nota de corrección en el historial de transiciones o regularización en spec posterior, sin renumerar la spec publicada |
| `AUD-068` | D7 | Baja | `docs/sdd/PROTOCOLO_OPERATIVO.md:294`; `docs/sdd/auditoria_cumplimiento_sdd.md:935-945` | El bloque de documentos de raíz de §12 cierra con «La formalización de la allowlist de agentes para la raíz corresponde al bloque B3». El bloque B3 pertenece a la hoja de ruta de la auditoría de origen y quedó ejecutado por `SPEC-009` a `SPEC-012`; la remisión describe como pendiente una formalización ya presente en la matriz de `.opencode/agents/` y en §12 | Corrección editorial de la remisión al bloque cerrado |
| `AUD-076` | D8 | Media | `specs/013-cierre-reauditoria-conformidad/spec.md:139` y `:335`; `specs/013-cierre-reauditoria-conformidad/validation_report.md:20`, `:98-109`; `docs/sdd/auditoria_final_v0_7_0.md:172` | Las filas `RNF-001` y `CA-015` de `SPEC-013` figuran en `PASADO` con una evidencia que la nota de cierre transcribe como no acreditante del valor literal `CONFORME` ni de la cláusula de diez de diez dimensiones, y el informe final emitió `CONFORME CON OBSERVACIONES`. Un criterio marcado como superado convive con la declaración de que no se satisface, de modo que la matriz de un reporte publicado afirma más que su evidencia | Decisión del propietario sobre la fila: nota que declare el valor efectivo o regularización por spec posterior; el criterio no se reescribe para acomodarlo |
| `AUD-087` | D9 | Alta | `git rev-parse v0.7.0^{tag}` = `f4a6203`; `git show -s --format=%s v0.7.0` = `Release v0.7.0` sobre `5a3af48`; `git rev-parse v0.7.0^{commit}` = `git rev-parse main` = `5a3af48`; `git log -1 --format=%P 5a3af48` = `ad739a0` y `479e3c2`; `git log --oneline -S "AUD-0" -- CHANGELOG.md` = solo `494db2e`; `docs/Flujo_de_Trabajo_Git.md:274-278`, `:301`, `:371-383`; `tools/sdd/validate.py:855-861` | El commit publicado fue `ad739a0`, que contiene el empaquetado `5da6df6` y no contiene la cita `AUD-NNN` que `C-10` exige para un incremento MINOR; la cita entró en `494db2e`, llegó a `dev` en `479e3c2` y a `main` en el merge `5a3af48`, y el tag resuelve hoy a `5a3af48`. El tag se recreó sobre el commit corregido, conforme al hecho declarado en el encargo: `docs/Flujo_de_Trabajo_Git.md:301` prohíbe mover, eliminar o reutilizar un tag publicado y `:371-383` exige crearlo una sola vez, después de verificar en `:274-278` que no exista. El artefacto publicado cambió después de la publicación mediante el desplazamiento de su etiqueta y no por un release nuevo | Deuda aceptada del release publicado: el tag no vuelve a moverse. La corrección de contenido de un release publicado se tramita por spec posterior que fije el procedimiento —release PATCH nuevo o nota de errata— y el cierre de la observación |
| `AUD-088` | D9 | Alta | `git show --stat 5da6df6` (18 archivos, entre ellos `MEMORY.md` y `tools/sdd/tests/test_agent_permissions.py` con 62 líneas modificadas); `git log --oneline -S "ESTADOS_POSTERIORES_A_LA_VALIDACION"` = solo `5da6df6`; `tools/sdd/tests/test_agent_permissions.py:1989-2008` y `:2044`; `specs/013-cierre-reauditoria-conformidad/plan.md:226`, `:337`; `docs/sdd/PROTOCOLO_OPERATIVO.md:351`; `docs/Flujo_de_Trabajo_Git.md:336`, `:341`, `:466`; `docs/constitution.md:15` | El commit de empaquetado `chore: prepare release v0.7.0` modificó 18 archivos y, además de `CHANGELOG.md`, `specs/INDEX.md` y los frontmatter, escribió en `MEMORY.md` y en la suite del mecanismo de control. En esa suite, `test_historial_de_releases` pasó de contrastar las ocho filas que fijan `RF-016`, `CA-014` y el plan de `SPEC-013` a comparar el número de filas con el de encabezados, y la constante `ESTADOS_POSTERIORES_A_LA_VALIDACION` se introdujo admitiendo `released` junto a `validated`. La rama de empaquetado se limita a `CHANGELOG.md`, `specs/INDEX.md` y el frontmatter de las specs publicadas, y ninguna tarea de `SPEC-013` ni de `SPEC-014` declara esa modificación: la verificación de un criterio publicado se relajó sin spec, en el commit que preparó el release que esa verificación debía autorizar | Spec posterior que regularice el criterio del historial de releases y el estado admitido por la nota de cierre, con registro en `CHANGELOG.md`; no se reescribe la tarea publicada |
| `AUD-089` | D9 | Media | `specs/014-cierre-observaciones-finales/validation_report.md:52-57`; `docs/sdd/PROTOCOLO_OPERATIVO.md:312-316`; `docs/Flujo_de_Trabajo_Git.md:394`, `:398`; `CHANGELOG.md:13-44` | El reporte de la spec publicada registra la sección de cierre con `Merge:`, con la línea `Release: v0.7.0` y con una viñeta de G5, y no registra el resultado de G6; la entrada del release registra la línea de aprobación y no transcribe las tres verificaciones de release. La regla de registro de §13 y del rango 4 exige el resultado de G5 y de G6 en los dos soportes, de modo que la conformidad del release se sostiene en comprobaciones que ningún artefacto transcribe | Registro append-only del resultado de G6 por el propietario en el reporte de la spec publicada y en la entrada del release, sin alterar matriz ni dictamen |
| `AUD-090` | D9 | Alta | `git log -1 --format=%G? 494db2e` = `N`; `git verify-commit 494db2e` con código de salida `1`; `git show --stat 5da6df6` con la cita ausente; `git log --oneline -S "AUD-0" -- CHANGELOG.md` = solo `494db2e`; `docs/sdd/PROTOCOLO_OPERATIVO.md:270-274`; `docs/constitution.md:76`; `.git/config:25-26` | La cita del informe de auditoría que `C-10` exige en la entrada del release fue introducida por `494db2e`, commit sin firma, en la entrada de `CHANGELOG.md` que §11 declara sección protegida modificable solo mediante commit firmado del propietario. La línea de registro de G6 conserva su commit firmado —`git log -1 --format=%G? 5da6df6` = `G`, con firma `ED25519` válida—, pero la entrada protegida fue modificada después por un commit cuyo estado de firma es `N` | Registro de la corrección por el propietario en un commit firmado y declaración del procedimiento para una sección protegida ya publicada; el contenido no se revierte sin spec |
| `AUD-099` | D10 | Media | `docs/sdd/README.md:28-63` y `:65-69`; `python -m unittest discover -s tools\sdd\tests -q` con el fallo «`docs/sdd/README.md no registra la fila de docs/sdd/auditoria_posterior_v0_7_0.md`»; `tools/sdd/tests/test_agent_permissions.py:1757-1765`, `:1975-1987`; `.opencode/agents/auditor.md:14-16`, `:50-52` | Este informe añade `docs/sdd/auditoria_posterior_v0_7_0.md` al corpus y la tabla de inventario no porta su fila: 35 archivos frente a 34 filas. La prueba `test_inventario_del_corpus` enumera cada `*.md` de la raíz del corpus y de `plantillas/`, y la ejecución de la suite falla con el mensaje transcrito, de modo que el check `verify` del Pull Request que transporte el informe queda en rojo; el rol de auditoría no puede editar `docs/sdd/README.md`, porque `docs/**` está denegado y la única concesión alcanza `docs/sdd/auditoria_*.md` | Registrar la fila por el propietario o el `documenter` antes de integrar el informe |
| `AUD-100` | D10 | Baja | `CHANGELOG.md:225` frente a `:44`; `CHANGELOG.md:24`; `specs/INDEX.md:20` | El párrafo posterior al historial declara que «G6 permanece pendiente de la línea» de aprobación y que «el tag `v0.7.0` se crea sobre el commit publicado», en tiempo futuro, cuando la línea de registro existe en la entrada del release, el estado de `SPEC-014` es `released` y el tag está creado. Además, la viñeta de la entrada describe el cierre con el rango «`AUD-038` a `AUD-102`», que incluye números no asignados en la serie | Corrección editorial del párrafo y del rango de identificadores |

### 5.3 Hechos posteriores al primer empaquetado

| Hecho | ¿Constituye observación? | Severidad | Destino |
|---|---|---|---|
| El tag `v0.7.0` se recreó sobre `main` después de corregir la cita de auditoría que G6 exige para un incremento MINOR | Sí: `AUD-087` | Alta | Deuda aceptada del release publicado; el tag no se mueve de nuevo y la corrección se tramita por spec posterior |
| Dos pruebas de `tools/sdd/tests` se generalizaron dentro de la rama de empaquetado porque fijaban ocho releases y el estado `validated` | Sí: `AUD-088` | Alta | Spec posterior con la regularización del criterio y registro en `CHANGELOG.md` |
| `main` recibió la corrección en un commit posterior al primer tag | No por sí solo: un commit posterior a un release es lícito y no exige etiqueta nueva, y la corrección llegó a `main` por el Pull Request #19. Se registra como el mecanismo que produjo `AUD-087` y `AUD-090` | No aplica | Se documenta en el cierre de `AUD-087` y de `AUD-090` |

### 5.4 Recuento

| Clase | Recuento |
|---|---|
| Observaciones del informe final examinadas | 7 |
| Cerradas con evidencia | 6 |
| Parciales | 1 (`AUD-075`) |
| Vigentes de las siete | 0 |
| Observaciones nuevas | 10 |
| Nuevas de severidad `Crítica` | 0 |
| Nuevas de severidad `Alta` | 3 (`AUD-087`, `AUD-088`, `AUD-090`) |
| Nuevas de severidad `Media` | 4 (`AUD-057`, `AUD-076`, `AUD-089`, `AUD-099`) |
| Nuevas de severidad `Baja` | 3 (`AUD-039`, `AUD-068`, `AUD-100`) |
| Hallazgos vigentes del régimen en este corte | 10 |

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría (`docs/constitution.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:278`).

| Compuerta | Evidencia observada | Límite de esta auditoría |
|---|---|---|
| G1 | Catorce specs con exactamente dos casillas en su sección de aprobaciones, G1 y G4, por ejemplo `specs/013-cierre-reauditoria-conformidad/spec.md:361-362` y `specs/014-cierre-observaciones-finales/spec.md:203-204`; `tools/sdd/validate.py:447-475` comprueba forma, fecha ISO y ubicación; `tools/sdd/tests/test_validate.py:1579-1594` acredita el rechazo de la casilla duplicada | Las firmas de los catorce commits de G1 no se verificaron una por una; la aprobación corresponde al propietario |
| G4 | Línea marcada de G4 en las catorce specs y dictamen `CONVERGIDO` en el reporte de cada una, por ejemplo `specs/014-cierre-observaciones-finales/validation_report.md:47`; la fila de `RNF-001` de `SPEC-013` se evalúa en `AUD-076` | Las firmas de los catorce commits de G4 no se verificaron una por una; la aprobación corresponde al propietario |
| G6 | `git rev-parse v0.7.0^{tag}` devuelve `f4a6203`, luego el tag es un objeto anotado; `git show -s --format=%s v0.7.0` muestra el mensaje `Release v0.7.0` sobre `Merge pull request #19 from sebaxtian/dev`; `git rev-parse v0.7.0^{commit}` y `git rev-parse main` devuelven `5a3af48`; `git merge-base --is-ancestor main dev` devuelve `0`; `git verify-commit 5da6df6` devuelve firma `ED25519` válida con la clave de `docs/sdd/firmantes_autorizados:4-5`; `python tools\sdd\validate.py --spec SPEC-014 --gate G6` devuelve «OK: sin hallazgos»; la entrada del release en `CHANGELOG.md:13-44` porta la línea de registro en `:44`, la cita del informe en `:23` y los identificadores en `:24`; el informe final tiene fila propia en el inventario (`docs/sdd/README.md:62`) | El desplazamiento del tag consta en `AUD-087`, la modificación sin firma de la entrada protegida en `AUD-090` y la falta de transcripción del resultado en `AUD-089`; ninguna de las tres se resuelve con un veredicto favorable del validador |

**G2, G3 y G5.** Su verificación corresponde al orquestador y no constituye aprobación (`docs/sdd/PROTOCOLO_OPERATIVO.md:136`). La evidencia disponible es la declaración de las transiciones T4, T5 y T7 en `specs/014-cierre-observaciones-finales/spec.md:227-230`, el registro de G5 en `specs/014-cierre-observaciones-finales/validation_report.md:57` y el cierre de integración de los siete reportes publicados.

## 7. Veredicto global

**Recuento de hallazgos vigentes:** 10 observaciones nuevas abiertas (0 `Crítica`, 3 `Alta`, 4 `Media` y 3 `Baja`); de las siete observaciones del informe final, 6 quedaron cerradas y 1 es parcial, con su residuo registrado en `AUD-076` y sin doble cómputo.

**Regla aplicada.** Una dimensión es `CONFORME` cuando no conserva observación abierta; es `PARCIAL` cuando conserva al menos una observación abierta de severidad `Media` o `Baja` con efecto declarado; es `NO CONFORME` cuando conserva una observación de severidad `Alta` o `Crítica`.

| Dimensión | Veredicto | Observación que lo sostiene |
|---|---|---|
| D1 | `CONFORME` | Ninguna vigente; `AUD-008` cerrada |
| D2 | `CONFORME` | Ninguna vigente; `AUD-015` cerrada |
| D3 | `CONFORME` | Ninguna vigente; `AUD-024` cerrada |
| D4 | `PARCIAL` | `AUD-039` (Baja) |
| D5 | `CONFORME` | Ninguna vigente; `AUD-045` y `AUD-046` cerradas |
| D6 | `PARCIAL` | `AUD-057` (Media) |
| D7 | `PARCIAL` | `AUD-068` (Baja) |
| D8 | `PARCIAL` | `AUD-075` (parcial) y `AUD-076` (Media) |
| D9 | `NO CONFORME` | `AUD-087`, `AUD-088` y `AUD-090` (Alta); `AUD-089` (Media) |
| D10 | `PARCIAL` | `AUD-099` (Media) y `AUD-100` (Baja) |
| D11 | `CONFORME` | Ninguna vigente; `AUD-101` y `AUD-102` cerradas |

**Veredicto global:** `NO CONFORME`.

**Fundamento.** El régimen mejoró en el corte respecto del informe final: las siete observaciones de ese informe recibieron tratamiento y seis desaparecieron con artefacto y evidencia; el flujo de integración continua prepara el árbol con historial completo y etiquetas y ejecuta las dos suites (D11 `CONFORME`), la condición de G5 del rango 3 incorporó el check exigible (D4 sin observación de origen) y la matriz del orquestador quedó limitada a `.opencode/**` (D7 sin observación de origen). El valor `NO CONFORME` proviene de D9: el proceso de release del estado publicado presenta tres rupturas normativas de severidad `Alta` —el tag publicado se recreó para incorporar la cita que `C-10` exige (`AUD-087`), el commit de empaquetado modificó la suite del mecanismo de control y `MEMORY.md` fuera del alcance de `release/vX-Y-Z` y sin spec (`AUD-088`), y la cita se introdujo en la entrada protegida mediante un commit sin firma (`AUD-090`)— más una brecha de registro de la verificación de G6 (`AUD-089`). Las seis observaciones restantes son de sección documental y de fila de validación, y ninguna invalida una compuerta por sí sola.

**Alcance del veredicto.** El veredicto califica el régimen en `13e85e2`, no la calidad del release como entrega. Un tag publicado que se mueve no se repara moviéndolo de nuevo: la reparación es declarativa, con spec posterior y con el registro que `AUD-089` y `AUD-090` exigen.

**Declaración expresa.** Este informe no aprueba compuerta alguna: no declara G1, G2, G3, G4, G5 ni G6, no emite línea de aprobación y no sustituye la firma del propietario ni su verificación. Registra el resultado de una auditoría de conformidad y se limita a la evidencia citada. Un resultado favorable del validador o de la suite no acredita la conformidad del régimen ni autoriza un release.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| Registrar la fila de `docs/sdd/auditoria_posterior_v0_7_0.md` en la tabla de inventario de `docs/sdd/README.md` | `AUD-099` | corrección | Escritura del propietario o de `documenter`; desbloquea la integración de este informe |
| Declarar el procedimiento de corrección de un release publicado y cerrar el desplazamiento del tag con nota de errata o release PATCH | `AUD-087` | spec posterior | Decisión del propietario; el tag no se mueve |
| Regularizar el criterio del historial de releases y el estado admitido por la nota de cierre, con registro en `CHANGELOG.md` | `AUD-088` | spec posterior | `AUD-087` resuelto en su parte declarativa |
| Registrar la corrección de la entrada protegida en un commit firmado y fijar el procedimiento para una sección protegida ya publicada | `AUD-090` | registro del propietario | Decisión del propietario |
| Registrar de forma append-only el resultado de G6 en el reporte de la spec publicada y en la entrada del release | `AUD-089` | registro del propietario | `AUD-090` resuelto |
| Resolver la fila de `RNF-001` y `CA-015` de `SPEC-013` con el valor que la evidencia sostiene | `AUD-076` y el residuo de `AUD-075` | decisión del propietario | Ninguna |
| Corregir la evidencia de T7 en el historial de transiciones de `SPEC-014` | `AUD-057` | decisión del propietario | Ninguna |
| Incorporar el check `verify` a la condición de la fila G5 del rango 4 | `AUD-039` | corrección de alineación | Ninguna |
| Retirar la remisión al bloque B3 de §12 del protocolo | `AUD-068` | editorial | Ninguna |
| Corregir el párrafo del historial de releases y el rango de identificadores de la entrada `v0.7.0` | `AUD-100` | editorial | Ninguna |

## 9. Limitaciones

| Elemento | Causa | Evidencia o comprobación que faltaría |
|---|---|---|
| Firmas de los commits de G1 y G4 de las catorce specs | La sesión verificó la firma del commit de G6 y no recorrió los veintiocho commits de aprobación de las specs | Resultado de C-03 para los commits de G1 y de G4 de cada spec, con la huella contrastada contra `docs/sdd/firmantes_autorizados` |
| Archivo de firmantes que Git consulta | `.git/config:25-26` declara `allowedSignersFile` en `C:\Users\sebax\.ssh\allowed_signers`, fuera del repositorio, y no en `docs/sdd/firmantes_autorizados`. Las dos líneas de clave del archivo local son idénticas a las de `docs/sdd/firmantes_autorizados:4-5`, de modo que la firma válida corresponde a una clave de la lista versionada por coincidencia de contenido, no por configuración | Configuración que apunte la verificación a la lista versionada, o registro de la comprobación de identidad entre ambos archivos |
| Destino anterior del tag `v0.7.0` | Las etiquetas no llevan reflog en esta configuración; el objeto de etiqueta no conserva su destino previo. La reconstrucción se sostiene en el hecho declarado en el encargo, en la fecha y en el contenido de `ad739a0` frente a `5a3af48`, y en la salida de `git log --oneline -S "AUD-0" -- CHANGELOG.md`, que atribuye la cita a un solo commit posterior al empaquetado | Registro del remoto (`git ls-remote --tags origin`) y bitácora de la operación de etiquetado |
| Propiedad de dos padres de los merges citados | Se verificaron los padres de `5a3af48` y de `13e85e2`; los de `49caac9`, `09eaf34`, `94c2ea1`, `9df8446`, `b87e32c`, `e55fca1` y `b018ab8` no se consultaron uno por uno | Salida de `git log --merges -1 --format=%P` para cada identificador citado |
| Estado remoto de la protección de ramas | La configuración remota no forma parte del repositorio y esta auditoría no consultó la API de reglas | Salida de `python tools/git/verify_branch_protection.py` con token válido |
| Ejecución efectiva del job `verify` en GitHub | Se acreditó por lectura del flujo y de las reglas declaradas, y la suite local falla por `AUD-099`; no se observó una ejecución del job | Registro de una ejecución con el punto de corte y el número de commits examinados |
| Fecha del corte | El encargo fijó 2026-11-14 y la sesión se ejecuta el 2026-11-20; el informe registra la fecha efectiva y declara la diferencia | Confirmación del propietario si la fecha nominal debe prevalecer |

Ningún elemento de esta lista se presume cumplido.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | Identificación del commit auditado, de la rama y de la rama de trabajo | `13e85e28ff35dbeb4bbbd75bdd8526677dc682e3`; `.git/refs/heads/dev:1`; `.git/logs/HEAD:237-238` |
| B | Tag anotado verificado: tipo, mensaje, commit objetivo y alcance desde `main` | `git rev-parse v0.7.0^{tag}` = `f4a6203`; `git show -s --format=%s v0.7.0` = `Release v0.7.0` sobre `Merge pull request #19 from sebaxtian/dev`; `git rev-parse v0.7.0^{commit}` = `git rev-parse main` = `5a3af48`; `git merge-base --is-ancestor main dev` = `0` |
| C | Secuencia del empaquetado y de la corrección posterior | `git show --stat 5da6df6` (18 archivos); `git log -1 --format=%P 5a3af48` = `ad739a0` y `479e3c2`; `git log -1 --format=%P 13e85e2` = `479e3c2` y `5a3af48`; `git log --oneline -S "AUD-0" -- CHANGELOG.md` = `494db2e`; `.git/logs/HEAD:225-237` |
| D | Reflogs de las ramas base | `.git/logs/refs/heads/main:11-12`; `.git/logs/refs/heads/dev:42-43` |
| E | Entrada del release y línea de registro de G6 | `CHANGELOG.md:13-44`, con la cita del informe en `:23` y los identificadores en `:24`; historial en `:209-225` |
| F | Condición de `C-10` que exige la cita de auditoría en un incremento MINOR | `tools/sdd/validate.py:855-861`; `:811-838` para tipo, mensaje y commit objetivo del tag |
| G | Prohibición de mover un tag publicado y verificación previa a crearlo | `docs/Flujo_de_Trabajo_Git.md:274-278`, `:301`, `:371-383`, `:394` |
| H | Generalización de las dos pruebas en el commit de empaquetado | `git log --oneline -S "ESTADOS_POSTERIORES_A_LA_VALIDACION"`; `tools/sdd/tests/test_agent_permissions.py:1989-2008`, `:2044`; criterio publicado en `specs/013-cierre-reauditoria-conformidad/plan.md:226`, `:337` |
| I | Nota de cierre de la reauditoría final y filas de `RNF-001` y `CA-015` | `specs/013-cierre-reauditoria-conformidad/validation_report.md:96-114`; `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335` |
| J | Cierre de integración de la spec publicada | `specs/014-cierre-observaciones-finales/validation_report.md:52-57` |
| K | Inventario del corpus, regla de inventario y fallo ejecutado de la suite | `docs/sdd/README.md:28-63`, `:65-69`; `python -m unittest discover -s tools\sdd\tests -q` con «Ran 167 tests» y el fallo `test_inventario_del_corpus` |
| L | Flujo de integración continua corregido | `.github/workflows/sdd.yml:1-31`; `docs/Flujo_de_Trabajo_Git.md:232`, `:462` |
| M | Matriz del orquestador limitada a `.opencode/**` | `.opencode/agents/sdd.md:44-55`, `:170-175` |
| N | Estado de firma de los commits citados | `git log -1 --format=%G? 5da6df6` = `G`; `git log -1 --format=%G? 494db2e` = `N`; `git verify-commit 494db2e` con código `1`; `allowedSignersFile` en `.git/config:25-26` |
| O | Remisión al bloque B3 y su hoja de ruta de origen | `docs/sdd/PROTOCOLO_OPERATIVO.md:294`; `docs/sdd/auditoria_cumplimiento_sdd.md:935-945` |
| P | Salidas del validador y de la compuerta | `python tools\sdd\validate.py --all` sin `[ERROR]` y con `[WARN]` de legado; `python tools\sdd\validate.py --spec SPEC-014 --gate G6` = «OK: sin hallazgos.»; `python -m unittest discover -s tools\git\tests -q` = «Ran 48 tests» y «OK» |
