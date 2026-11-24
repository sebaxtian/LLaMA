# Informe de auditoría — estado integrado de `dev` previo al release v0.8.0

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, implementado en `.opencode/agents/auditor.md`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-24 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), corpus de auditoría e inventario de hallazgos, specs `SPEC-001` a `SPEC-017` con lectura completa de los cinco artefactos de `SPEC-017`, implementación verificable de `src/gemma/`, `tools/gemma/`, `tools/sdd/`, `tools/git/` y `.opencode/`, reglas de protección de ramas, registros Git locales y `CHANGELOG.md`, con corte en el commit `c49b6f3` de `dev`.
- **Carácter:** evidencia de la auditoría de conformidad previa a G6 exigida por `docs/Flujo_de_Trabajo_Git.md:16` y por `docs/constitution.md:85`; no fija reglas, no aprueba compuertas, no emite línea de aprobación y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `c49b6f32713f711948f383f4813278c978902f9b` (`git log -1 --format=%H` sobre `dev`) |
| Rama | `dev` (`git branch --show-current`) |
| Fecha de corte | 2026-11-24 |
| Validador ejecutado | `python tools\sdd\validate.py --all`: 17 comprobaciones, 0 entradas `[ERROR]`, código de salida 0; las 56 `[WARN]` corresponden a la cláusula de legado de `SPEC-001` a `SPEC-009` |
| Compuertas ejecutadas | `--spec SPEC-017 --gate G1`, `--gate G4` y `--gate G5`: las tres devuelven `OK: sin hallazgos` |
| Suites ejecutadas | `python -m unittest discover -s tools\gemma\tests -q`: «Ran 140 tests in 7.316s» y «OK». `python -m unittest discover -s tools\sdd\tests -q`: «Ran 223 tests in 1.599s» y «OK» en el corte, antes de añadir este informe; el anexo M transcribe la ejecución posterior. `python -m unittest discover -s tools\git\tests -q`: «Ran 48 tests in 22.026s» y «OK» |
| Entorno | Windows 11 (`win32`); lista blanca del rol: `git log`, `show`, `diff`, `status`, `branch`, `rev-parse`, `merge-base`, `verify-commit` por `%G?`, además del validador y de `unittest` |
| Rol ejecutor | `auditor` |

**Procedimiento.** Cuatro pasos. Primero, lectura íntegra de la base normativa de rangos 1 a 5 y de los cinco artefactos de `SPEC-017`. Segundo, lectura de las 85 filas de `docs/sdd/inventario_hallazgos.md` con verificación de la forma de la cita, del vocabulario del estado y del recálculo del veredicto por precedencia. Tercero, contraste del contrato vigente con la implementación declarada: los 22 campos de `RF-006`, los 9 ejes de `C-2`, la caché `q8_0` con `flash_attn` `on`, el presupuesto de 4 claves, el umbral de derrame de `RNF-003`, la condición de promoción de `RNF-007` y las 13 cargas históricas por debajo de `512 MiB` en `results/gemma/`. Cuarto, examen de la integración Git, del registro de G5, del control de cambios de la base y del registro de cambios, con la evidencia transcrita en §10.

## 2. Base normativa e inventario

La jerarquía consta de siete rangos y una categoría sin rango, declarada de forma coincidente en `docs/constitution.md:48-59` y en `docs/sdd/README.md:15-24`. Cada documento de la base declara su rango y su carácter en el encabezado (`docs/constitution.md:3`; `AGENTS.md:1-3`; `docs/sdd/PROTOCOLO_OPERATIVO.md:3`; `docs/Flujo_de_Trabajo_Git.md:3`; `docs/sdd/plantillas/informe_auditoria.md:3`).

| Documento | Rango | Cita |
|---|---|---|
| `docs/constitution.md` | 1 | `docs/constitution.md:52` |
| `AGENTS.md` | 2 | `docs/constitution.md:53` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | `docs/constitution.md:54` |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | `docs/constitution.md:55` |
| `docs/sdd/plantillas/*.md` | 5 | `docs/constitution.md:56` |
| `specs/NNN-slug/*.md` | 6 | `docs/constitution.md:57` |
| `src/`, `tools/`, `tests/`, `.opencode/` | 7 | `docs/constitution.md:58` |
| Guías, informes, `README.md`, `MEMORY.md`, índice y `CHANGELOG.md` | Sin rango | `docs/constitution.md:59`; `docs/sdd/README.md:24` |

**Corpus.** La tabla de inventario de `docs/sdd/README.md:28-70` declara 41 filas de datos y el árbol del corte contiene 41 archivos del corpus: 33 en `docs/sdd/`, 7 en `docs/sdd/plantillas/` y el archivo de datos `docs/sdd/firmantes_autorizados`. La fila de orden de lectura 39 registra `docs/sdd/auditoria_previa_v0_7_2.md` y la 41 `docs/sdd/auditoria_final_v0_7_2.md`; ninguna fila registra todavía el presente informe. Este informe añade un archivo 42 y su fila la escribe el rol `documenter` antes de la integración (`docs/sdd/PROTOCOLO_OPERATIVO.md:305`; `docs/sdd/plantillas/informe_auditoria.md:24`); mientras falte, `docs/sdd/README.md:76` lo califica como defecto de conformidad.

**Specs.** `specs/INDEX.md:7-23` declara 17 filas. `SPEC-001` a `SPEC-016` figuran `released` con su tag; `SPEC-017` figura `validated` en la fila 23, sin release, y su `spec.md:4-5` declara `status: validated` y `version: 0.15.0`, valores coincidentes.

**Inventario de hallazgos.** `docs/sdd/inventario_hallazgos.md:33-114` porta 82 filas para 82 identificadores `AUD-001` a `AUD-110`, y la sección de `:160-162` añade 3 filas para `AUD-111` a `AUD-113`. El recuento de estados es 77 en `cerrado`, 3 en `cerrado` en el registro separado, 5 en `cerrado por ratificación` y 0 en `parcial`, `vigente` o `cerrado por exención`; 0 filas carecen de regla citada o de evidencia de cierre. El anexo de `docs/sdd/inventario_hallazgos.md:144-146` declara 0 observaciones y 0 tratamientos, y `:150` declara el veredicto `CONFORME`. Ninguna fila se refiere a `SPEC-017`.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida transcrita. Una afirmación de cumplimiento exige el artefacto y su ubicación; una de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento.

**Regla citada.** Cada hallazgo cita la regla que incumple con la forma `ruta §capítulo:línea`, conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md §16:387`. El juicio que no alcanza una regla de los rangos 1 o 3 se registra como observación, queda fuera del recuento y no computa como hallazgo abierto.

Escala de veredicto (`docs/sdd/plantillas/informe_auditoria.md:32-40`): `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`.

Escala de severidad (`docs/sdd/plantillas/informe_auditoria.md:42-49`): `Crítica` afecta la validez de una compuerta o de la base; `Alta` rompe una regla normativa sin invalidar la compuerta; `Media` produce divergencia entre documentos de distinto rango; `Baja` es un defecto de forma, de redacción o de cita.

**Numeración.** Este informe no asigna `AUD-NNN`. El espacio se reserva a los hallazgos con fila en el inventario (`docs/sdd/PROTOCOLO_OPERATIVO.md:221`) y el rol de auditoría no escribe filas (`docs/sdd/PROTOCOLO_OPERATIVO.md:305`). Los hallazgos se registran como `H-01` a `H-05` y las observaciones como `OBS-NNN`; la fila de cada `H-NN` corresponde al `documenter` antes de la integración, con el identificador inmediato al último asignado.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Hallazgos |
|---|---|---|---|---|
| D1 | Autoridad normativa y control de cambios de la base | `NO CONFORME` | `docs/constitution.md:83-87`; `docs/sdd/PROTOCOLO_OPERATIVO.md:123`, `:137`, `:379`; `git show c5d1b1d -- docs/sdd/PROTOCOLO_OPERATIVO.md` | `H-02` |
| D2 | Ciclo de siete etapas, estados y compuertas | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:72-135`; `specs/017-configuracion-gemma-4-26b-a4b/spec.md:4-5`, `:332-350`; `--gate G1`, `G4` y `G5` con `OK: sin hallazgos` | Ninguno vigente |
| D3 | Contratos de los artefactos de la spec y versionado | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:172-208`, `:231-247`; `specs/017-configuracion-gemma-4-26b-a4b/spec.md:310-328` | `H-05` |
| D4 | Trazabilidad `RF/CB → CA → T → evidencia` | `CONFORME` | `specs/017-configuracion-gemma-4-26b-a4b/spec.md:49-299`; `tasks.md:33-967` (81 tareas, 81 casillas marcadas, 0 pendientes); `validation_report.md:16-48` (29 de 29 filas en `PASADO`) | Ninguno vigente |
| D5 | Contrato vigente de `SPEC-017` y su implementación declarada | `CONFORME` | `spec.md:71` (22 campos), `:144` (`RNF-003`), `:160` (`RNF-007`), `:249` (`CA-007`), `:178` (`CB-004`); `plan.md:106-120` (9 ejes), `:157-188` (`C-6`), `:400-410` (`DEC-028`, `DEC-029`), `:418-422` (`DEC-031`); `src/gemma/perfiles/*.json`; `results/gemma/` con 33 registros | Ninguno vigente |
| D6 | Aprobaciones y firmas | `CONFORME` | `spec.md:305-306`; commit `10d06f8` → `G`; commit `eacb2a1` → `G`; `--gate G4` con la comprobación «firma del commit de aprobación y clave autorizada» en verde | Ninguno vigente |
| D7 | Roles y menor privilegio | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:289-305`; `.opencode/agents/*.md`; `plan.md:57`; `tasks.md:11-12` | Ninguno vigente |
| D8 | Integración Git y registro de G5 | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:149`, `:309-313`, `:321-323`; `docs/Flujo_de_Trabajo_Git.md:239-257`; `validation_report.md:86-89` | `H-03` |
| D9 | Registro de cambios y condición de release | `NO CONFORME` | `docs/constitution.md:42`, `:83`; `docs/Flujo_de_Trabajo_Git.md:229`, `:430`, `:441`; `CHANGELOG.md:11-13` | `H-01` |
| D10 | Consistencia documental operativa | `PARCIAL` | `MEMORY.md:13`; `specs/INDEX.md:23`; `spec.md:4`; `docs/Flujo_de_Trabajo_Git.md:235`, `:484` | `H-04` |
| D11 | Inventario de hallazgos y cálculo del veredicto | `CONFORME` | `docs/sdd/inventario_hallazgos.md:33-114`, `:150`, `:160-162`; `--all` con la comprobación «inventario de hallazgos: compleción, regla citada y veredicto» en verde | Ninguno vigente |

El veredicto global no se obtiene de esta matriz sino del cálculo de precedencia sobre las filas del inventario; la diferencia entre ambos se declara en §7.

**Riesgos y límites declarados del contrato.** Los tres límites que `SPEC-017` declara se verificaron en el corte y se sostienen: (a) `ctx_size` `131072` consta medido en `20261124T192712Z`/`192807Z` y **no adoptado**, porque la desviación de `rendimiento.json:41-46` conserva `comparacion` en `null` y `C-3` aplica el valor inicial `4096` (`spec.md:327`, `plan.md:420`, `validation_report.md:71`); (b) **ningún perfil se promueve**: los 3 manifiestos declaran `"estado": "candidato"`, `"aprobacion": null` y `"designacion": null`, de modo que `RNF-007` se cumple como prohibición de promoción y no como umbral alcanzado; (c) la **carga vigente no existe**: la última carga con propósito `carga` de `resiliencia` es `20261122T203814Z-resiliencia-carga-inicial` con `56 MiB` libres y `rendimiento` no tiene ninguna, conforme a `DEC-031` y a la observación `O-13` del reporte. El recuento independiente de `results/gemma/` devuelve exactamente 13 registros con el campo 14 por debajo de `512 MiB` —`56`, `133`, `133`, `25`, `25`, `25`, `25`, `25`, `389`, `53`, `389`, `389` y `336` MiB—, que coincide con `AMB-014`, con `CA-007` y con `DEC-031`.

## 5. Hallazgos

### H-01 — El registro de cambios no porta entrada alguna en `Unreleased` con un release menor preparado

- **Dimensión:** D9.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Alta`.
- **Regla citada:** `docs/constitution.md §5:42`.
- **Evidencia:** `docs/constitution.md:42`; `CHANGELOG.md:11-13`; `git log -1 --format=%h -- CHANGELOG.md` → `fc18c02` (2026-11-20); `git diff v0.7.2 --stat -- CHANGELOG.md` sin salida; `docs/Flujo_de_Trabajo_Git.md:229`, `:430`, `:441`; `specs/017-configuracion-gemma-4-26b-a4b/spec.md:4-5`; `git show --stat c5d1b1d`; corte `c49b6f3` del 2026-11-24.
- **Descripción:** el rango 1 exige registrar cada cambio relevante en `CHANGELOG.md` bajo `Unreleased` hasta publicar el release, y el rango 4 condiciona el release a que `Unreleased` contenga al menos una entrada `- ` y prohíbe crear versión o tag si está vacío. En el corte, `## [Unreleased]` (`CHANGELOG.md:11`) está vacío y la sección siguiente es `## [v0.7.2] - 2026-11-21` (`:13`): el archivo no se modifica desde el empaquetado de `v0.7.2` (`fc18c02`), de modo que ni la feature completa de `SPEC-017` —39 rutas y 16 555 líneas añadidas entre `src/gemma/`, `tools/gemma/`, `docs/gemma/` y la propia spec— ni la modificación de la base que `H-02` describe constan en el registro de cambios. El defecto no es de redacción del empaquetado: el paso 3 del flujo admite en `A1` la entrada del release y su historial, no la creación del contenido que la precondición de `:430` presume acumulado.
- **Remediación:** registrar bajo `Unreleased` los cambios de `SPEC-017` y el cambio de la base de `H-02`, con su identificador de spec y sus rutas, antes de abrir la rama de empaquetado; el empaquetado convierte después esa sección en `v0.8.0` con fecha UTC y `- Approved by: Agent Sebaxtian`, y la condición se cierra cuando `Unreleased` conserva al menos una entrada y la entrada del release transcribe el contenido acumulado.

### H-02 — La transición `T11` se integró en el rango 3 desde un commit de feature, sin spec y sin versión ni entrada de registro

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Alta`.
- **Regla citada:** `docs/constitution.md §8:84`.
- **Evidencia:** `docs/constitution.md:83-84`; `docs/sdd/PROTOCOLO_OPERATIVO.md:19`, `:123`, `:133`, `:137`, `:379`; `git show --stat c5d1b1d`; `git show c5d1b1d -- docs/sdd/PROTOCOLO_OPERATIVO.md tools/sdd/validate.py tools/sdd/tests/test_validate.py`; `tools/sdd/validate.py:110`; `specs/017-configuracion-gemma-4-26b-a4b/plan.md:32`; `tasks.md:11`, `:24`; corte `c49b6f3` del 2026-11-24.
- **Descripción:** el rango 1 exige spec aprobada previa, incremento de la versión del documento y entrada en `CHANGELOG.md` bajo `Unreleased` para todo cambio de la base, y prohíbe integrarlo sin spec salvo que sea exclusivamente editorial. El commit `c5d1b1d`, sellado `feat(spec-017): configuracion medible de Gemma-4-26B-A4B-it-qat-GGUF`, incorpora la transición `T11` a la tabla de `§5` del protocolo (`docs/sdd/PROTOCOLO_OPERATIVO.md:123`), la constante homónima del validador (`tools/sdd/validate.py:110`), 65 líneas de prueba en `tools/sdd/tests/test_validate.py` —que elevan la suite del mecanismo de 222 a 223 pruebas—, el párrafo de reapertura de la clarificación y el bloque de reglas de `:133`. El cambio altera reglas y no es editorial: adiciona una transición al conjunto cerrado de `§5` y modifica el recuento que la prueba `test_tabla_transitions_coincide_con_protocolo` fijaba en diez. Su habilitación consta en la **Constancia de corrección** de `:137`, que declara la incorporación «por corrección autorizada directamente por el propietario, sin spec intermedia»; esa constancia no puede habilitar la vía, porque el rango 3 desarrolla el rango 1 «y no las amplía ni las atenúa» (`:19`) y porque la única excepción que el rango 1 admite es el cambio editorial. Concurren dos defectos del mismo acto: el cambio de la base se integró sin spec y sin entrada de registro (`H-01` lo mide en el archivo), y las rutas `docs/sdd/PROTOCOLO_OPERATIVO.md`, `tools/sdd/validate.py` y `tools/sdd/tests/test_validate.py` no figuran en el campo `Archivos` de tarea alguna de `tasks.md`, que declara `tools/gemma/`, `src/gemma/` y `docs/gemma/` como alcance de escritura (`plan.md:32`, `tasks.md:11`).
- **Remediación:** regularizar el cambio con una spec aprobada que lo declare y lo versione, o con un acta de ratificación firmada por el propietario con el identificador de `c5d1b1d` y el de la constancia, y registrar el cambio en `CHANGELOG.md` bajo `Unreleased`; la condición se cierra cuando el rango 3 no conserva una regla introducida por una vía que el rango 1 no admite y cuando el recuento de pruebas que declara el rango 4 coincide con la suite.

### H-03 — El registro de G5 del corte declara la rama de trabajo presente y su corrección prevista excede la modificación admitida del empaquetado

- **Dimensión:** D8.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Media`.
- **Regla citada:** `docs/sdd/PROTOCOLO_OPERATIVO.md §6:149`.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:149`, `:313`, `:321-323`, `:367`; `docs/Flujo_de_Trabajo_Git.md:250-257`, `:352`; `specs/017-configuracion-gemma-4-26b-a4b/validation_report.md:86`, `:89`; `git show c49b6f3:specs/017-configuracion-gemma-4-26b-a4b/validation_report.md`; `git diff -- specs/017-configuracion-gemma-4-26b-a4b/validation_report.md`; `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf` sin salida; `git branch -r --list origin/feat/gemma-4-26b-a4b-it-qat-gguf` sin salida; `git rev-parse --short dev` → `c49b6f3`; corte `c49b6f3` del 2026-11-24.
- **Descripción:** la evidencia exigida a G5 incluye el listado de ramas sin la rama integrada, y el rango 4 declara que si el listado conserva la rama la eliminación no está confirmada y G5 no se registra. En el commit auditado, `validation_report.md:89` registra G5 con el merge `7a6bbe4` y afirma que la rama `feat/gemma-4-26b-a4b-it-qat-gguf` «todavía [está] presente en local, donde es la rama actual» y que «`dev` local [apunta] a `844a5b0`, de modo que la sincronización local queda pendiente»; `:86` declara `Merge: 7a6bbe4`. El estado del repositorio en el corte es el contrario: la rama no existe en local ni como referencia remota, `dev` local es `c49b6f3` —el merge del PR #40, con dos padres `7a6bbe4` y `bddc922`— y el validador posterior devuelve `OK: sin hallazgos`. Las condiciones de G5 se cumplen, pero el registro que las acredita declara la condición de eliminación sin confirmar, de modo que en el corte el artefacto no porta la evidencia que `§6:149` exige. La corrección existe en el árbol de trabajo sin commit —`Merge:` pasa a `c49b6f3` y la viñeta de G5 pasa a declarar la eliminación local— y el rol no la registra: si se confirma en `release/v0-8-0`, excede la modificación admitida de `A6` en `§15`, que limita el reporte de una spec publicada a la línea `Release:` con el tag.
- **Remediación:** confirmar la corrección del registro de G5 fuera de la rama de empaquetado —en `dev` por Pull Request con un commit que no altere la matriz ni el dictamen, conforme a `§13:323`— y dejar en `A6` solo la línea `Release:` con el tag; la condición se cierra cuando el reporte del commit integrado declara el merge con dos padres, el validador posterior, el listado de ramas sin la rama y `Merge:` igual al commit que porta el registro.

### H-04 — `MEMORY.md` declara `SPEC-017` en `implemented` y atribuye ese estado al índice que declara `validated`

- **Dimensión:** D10.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Baja`.
- **Regla citada:** `docs/constitution.md §6:66`.
- **Evidencia:** `MEMORY.md:13`; `specs/INDEX.md:23`; `specs/017-configuracion-gemma-4-26b-a4b/spec.md:4`; `docs/sdd/README.md:24`; `git show 283c4dc -- specs/INDEX.md`; `git show --stat 283c4dc`.
- **Descripción:** `MEMORY.md:13` afirma que `SPEC-017` cursa «en `implemented`, conforme a `specs/INDEX.md:23`», mientras el frontmatter de la spec declara `status: validated` y la fila 23 del índice declara `validated`. La categoría sin rango no fija reglas y su contradicción con un documento normativo se resuelve a favor del documento normativo, con la corrección aplicada en el documento sin rango; la frase agrava el defecto porque invoca como fuente una línea que declara el valor contrario. El desfase nace de la secuencia del propio ciclo: `083ab05` escribió `implemented` cuando la spec pasó a ese estado y `283c4dc` promovió la spec a `0.15.0` `validated` y actualizó el índice sin tocar `MEMORY.md`, de modo que la divergencia se introdujo en el cierre de Validate y no en la implementación.
- **Remediación:** actualizar `MEMORY.md:13` al estado `validated`, con release `v0.8.0` pendiente y sin tag, citando `specs/INDEX.md:23`; la condición se cierra cuando las tres superficies declaran el mismo estado.

### H-05 — El historial de cambios de `SPEC-017` omite la versión `0.7.0` y colapsa dos etapas de contrato en una fila

- **Dimensión:** D3.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Baja`.
- **Regla citada:** `docs/sdd/PROTOCOLO_OPERATIVO.md §9:244`.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:234`, `:243-245`; `specs/017-configuracion-gemma-4-26b-a4b/spec.md:317-318`, `:346-347`; `git show 10d06f8 -- specs/017-configuracion-gemma-4-26b-a4b/spec.md`; `git show c5d1b1d:specs/017-configuracion-gemma-4-26b-a4b/spec.md`; `specs/016-cierre-auditoria-v0-7-1/spec.md:445-457`.
- **Descripción:** la regla de versionado hace incrementar MINOR en cada etapa que cambia el contrato —clarify, plan, tasks y validación— y el procedimiento obliga a escribir la fila del historial con versión, fecha y descripción por cada cambio, de modo que dos revisiones independientes obtienen el mismo número. El historial de `SPEC-017` salta de `0.6.0` (`spec.md:317`, cierre de la clarificación del 2026-11-23) a `0.8.0` (`:318`, «Plan y tareas actualizados»), y el salto se introdujo en `10d06f8`, que elevó la versión de `0.6.0` a `0.11.0` y escribió de una vez las filas `0.8.0` a `0.11.0`. La tabla de transiciones registra `T2` `clarified` → `planned` y `T3` `planned` → `tasked` como filas distintas y fechadas el 2026-11-24 (`:346-347`), de modo que la etapa Plan consumió un MINOR —`0.7.0`— que ninguna fila del historial declara: la versión existe en la aritmética de la serie y no en el registro, y la fila `0.8.0` describe dos etapas con una sola entrada. El historial de `SPEC-016` conserva las trece filas correlativas de `0.1.0` a `0.9.4`, de modo que la práctica del corpus no admite el hueco.
- **Remediación:** añadir la fila `0.7.0` del 2026-11-24 con la transición `clarified` → `planned` y la referencia a `plan.md` actualizado, y reducir la fila `0.8.0` a la etapa Tasks; la condición se cierra cuando cada etapa de contrato tiene su fila y la serie no conserva huecos.

### Observaciones

| N.º | Severidad | Observación | Tratamiento |
|---|---|---|---|
| `OBS-001` | `Baja` | La sección `## Referencias` de `plan.md:7-8` sigue describiendo el estado anterior: declara `spec.md` «versión 0.13.0 … estado `tasked`» y `clarify.md` «con `AMB-001` a `AMB-012` resueltos, 12 parches aplicados … y 10 decisiones de negocio», mientras `clarify.md` registra 14 ambigüedades, 20 parches y 12 decisiones, y `spec.md` es 0.15.0 `validated`. El cuerpo del plan sí está alineado con `DEC-027` a `DEC-031`, con `C-6` de 22 campos, `C-2` de 9 ejes y `C-9` de 4 claves, de modo que el defecto alcanza solo a la sección de referencias. | Propuesta: actualizar la sección en la corrección editorial siguiente, sin alterar decisiones ni contratos. Sin decisión del propietario en el corte. |
| `OBS-002` | `Baja` | `validation_report.md:7` declara «Contrato validado: `spec.md` 0.14.1 en estado `implemented`», y `spec.md:318` registra que `G4` se aprobó sobre el contrato `0.14.2` en `eacb2a1`. La diferencia es de un PATCH editorial —la corrección de `O-10` y la constancia de `O-13`—, sin cambio de requisitos, casos borde ni criterios, de modo que no alcanza la convergencia del dictamen; el reporte, sin embargo, no nombra la versión sobre la que se aprobó. | Propuesta: registrar la equivalencia de los contratos 0.14.1 y 0.14.2 en la nota append-only del reporte. Sin decisión del propietario en el corte. |
| `OBS-003` | `Baja` | `docs/Flujo_de_Trabajo_Git.md:235` y `:484` describen la suite del mecanismo «con 222 pruebas», y la ejecución del corte devuelve «Ran 223 tests»: la prueba añadida en `tools/sdd/tests/test_validate.py` por `c5d1b1d` elevó el recuento. La cifra es descriptiva y no fija una regla, de modo que el defecto es de redacción y no de alineación normativa. | Propuesta: sustituir la cifra por una remisión a la ejecución de la suite o actualizarla a 223 en la corrección editorial siguiente. Sin decisión del propietario en el corte. |
| `OBS-004` | `Baja` | `clarify.md:126` afirma que «la configuración vigente sí cumple el umbral» porque «la última carga registrada del perfil `resiliencia` declara `3889 MiB` libres en `20261124T190907Z-resiliencia-comparacion-ncmoe`», y ese registro declara `proposito: comparacion`; el criterio de `estado.py` que `DEC-031` fija selecciona `20261122T203814Z-resiliencia-carga-inicial` con `56 MiB`. La observación `O-13` del reporte y la fila `0.14.2` de `spec.md` ya la registran. | Tratada por el propietario en `083ab05`: la fila `0.14.2` de `spec.md:327` y `DEC-031` de `plan.md:420-422` declaran la lectura vigente y la ausencia de una carga que permita promover; `RNF-007` no se incumple porque ningún perfil se promueve. |
| `OBS-005` | `Baja` | El commit `083ab05` concentra en un solo acto la aprobación G4, la corrección editorial de `plan.md`, `tasks.md` y `spec.md`, la reescritura de 134 líneas del reporte, la actualización de `specs/INDEX.md` y la de `MEMORY.md`. La firma acredita la autoría del propietario sobre el acto y las rutas pertenecen a la spec en curso; la concentración explica que el reporte conserve la versión 0.14.1 en su encabezado y que `MEMORY.md` quedara un estado por detrás. | Propuesta: separar en adelante el commit de aprobación de los cambios editoriales de los artefactos que aprueba. Sin decisión del propietario en el corte. |

Las cinco observaciones son de severidad `Baja` y no computan como hallazgo abierto ni impiden el veredicto calculado; cuatro de ellas no tienen tratamiento registrado y una consta tratada en `083ab05`.

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría (`docs/constitution.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:283`).

| Compuerta | Veredicto | Evidencia | Límite de esta auditoría |
|---|---|---|---|
| G1 | `CONFORME` | Casilla `G1` marcada en `spec.md:305` con la fecha 2026-11-24; el commit `10d06f8` devuelve `G` con la identidad del propietario y `--gate G1` responde `OK: sin hallazgos` con la comprobación de firma en verde; el contrato aprobado es el `0.11.0` y las filas `0.12.0` a `0.15.0` no modifican requisitos, casos borde ni criterios de aceptación | La aprobación corresponde al propietario; este informe no la declara ni reproduce la línea de registro |
| G4 | `CONFORME` | Casilla `G4` marcada en `spec.md:306` con la fecha 2026-11-24; el commit `eacb2a1` devuelve `G`; dictamen `CONVERGIDO` con 29 de 29 filas en `PASADO` (`validation_report.md:48`, `:81`); `--gate G4` responde `OK: sin hallazgos` | La aprobación corresponde al propietario; el reporte declara el contrato 0.14.1 y la aprobación cubre el 0.14.2 (`OBS-002`) |
| G5 | `CONFORME` | Merge `c49b6f3` con dos padres (`7a6bbe4` y `bddc922`); `git branch --list` y `git branch -r --list` sin resultado para `feat/gemma-4-26b-a4b-it-qat-gguf`; validador posterior sin `[ERROR]`; check `verify` con `strict: true` en `tools/git/protection_rules/main.json:3-8` y en `dev.json:3-8`; `--gate G5` responde `OK: sin hallazgos` | La verificación corresponde al orquestador y no constituye aprobación; el registro que la acredita en el corte está desactualizado (`H-03`) |
| G6 | `NO CONFORME` | `CHANGELOG.md:11-13` sin entrada `v0.8.0` y con `Unreleased` vacío; `specs/INDEX.md:23` sin columna `Release`; `git rev-parse --verify --quiet refs/tags/v0.8.0` sin salida; `validation_report.md:87` con la línea `Release:` vacía | No emitido: la condición no se cumple por `H-01` y por el presente veredicto, y su aprobación corresponde al propietario |

## 7. Veredicto global

**Veredicto calculado desde el inventario.** `CONFORME`. Recuento sobre las 85 filas —82 en la tabla de §4 y 3 en el registro de §8—: 0 hallazgos abiertos, 80 en `cerrado`, 5 en `cerrado por ratificación` y 0 en `parcial`, `vigente` o `cerrado por exención`, con 0 filas sin regla citada y 0 filas sin evidencia de cierre. La precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME` se aplica en ese orden y el primer valor que se cumple es `CONFORME`, que coincide con el declarado en `docs/sdd/inventario_hallazgos.md:150`; no hay diferencia que registrar entre el cálculo y la declaración del inventario, y ninguna fila del inventario alcanza a `SPEC-017`.

**Veredicto del estado auditado.** `NO CONFORME`. Este informe emite cinco hallazgos abiertos —`H-01` de severidad `Alta`, `H-02` de severidad `Alta`, `H-03` de severidad `Media`, `H-04` de severidad `Baja` y `H-05` de severidad `Baja`— y ninguno consta en el inventario. La causa de la diferencia es estructural y ya fue declarada por el informe previo al release `v0.7.2`: `RF-011` de `SPEC-016` limita la tabla de `§4` a los 5 informes de auditoría anteriores y el rol de auditoría no escribe filas, de modo que el cálculo de precedencia solo alcanza las 85 filas heredadas. La fila que sostiene la diferencia no existe; se transcribe la ausencia de fila para `H-01` a `H-05` y la de la fila del corpus de este informe (`docs/sdd/README.md:76`).

**Condición de release.** No se satisface. `docs/Flujo_de_Trabajo_Git.md:16` y `docs/constitution.md:85` exigen que la auditoría previa a G6 declare el veredicto `CONFORME` sobre el estado integrado en `dev`, y `:16` declara que un veredicto distinto de `CONFORME` impide la publicación, conserva la spec en `validated` y transcribe el motivo con el hallazgo que lo sostiene. El motivo es `H-01`, que deja vacía la precondición de `Unreleased` del propio release, y `H-02`, que mantiene en el rango 3 una regla introducida por una vía que el rango 1 no admite; `H-03`, `H-04` y `H-05` no bloquean por sí mismos pero quedan abiertos. El cálculo mecánico del inventario devuelve `CONFORME` porque no alcanza estos cinco hallazgos, y ese resultado no se invoca como certificado de conformidad.

**Declaración expresa.** Este informe no aprueba compuerta alguna: no declara G1, G2, G3, G4, G5 ni G6, no emite línea de aprobación y no sustituye la firma del propietario. Un resultado favorable del validador o de las suites acredita estructura, coherencia interna y trazabilidad declarada, y no la conformidad del régimen ni la autorización de un release.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| Registrar bajo `Unreleased` los cambios de `SPEC-017` y el cambio del rango 3, y convertir la sección en `v0.8.0` al empaquetar | `H-01` | corrección del `documenter` y empaquetado | Autorización del propietario y registro previo a la rama `release/v0-8-0` |
| Regularizar la incorporación de `T11` con spec aprobada o con acta de ratificación firmada, y registrar el cambio en `CHANGELOG.md` | `H-02` | spec posterior o acta del propietario | Decisión del propietario; incluye alinear el recuento de pruebas del rango 4 (`OBS-003`) |
| Confirmar fuera de la rama de empaquetado el registro de G5 con el merge `c49b6f3`, el validador posterior y la rama ausente | `H-03` | corrección del orquestador en `dev` | Pull Request hacia `dev`; deja en `A6` solo la línea `Release:` |
| Actualizar `MEMORY.md:13` al estado `validated` con release pendiente | `H-04` | corrección del `documenter` | Cierre del ciclo y de `H-01` |
| Añadir la fila `0.7.0` de `2026-11-24` al historial de cambios y reducir la fila `0.8.0` a la etapa Tasks | `H-05` | corrección editorial de `spec.md` | Autorización del propietario |
| Registrar la fila de `docs/sdd/auditoria_release_v0_8_0.md` en la tabla de inventario del corpus y la fila correspondiente de cada `H-NN` en `docs/sdd/inventario_hallazgos.md` | Requisito del corpus y cálculo del veredicto | corrección del `documenter` | Escritura del `documenter` antes de la integración |
| Actualizar la sección de referencias de `plan.md`, la nota del contrato 0.14.1 del reporte y la separación del commit de aprobación | `OBS-001`, `OBS-002`, `OBS-005` | corrección editorial o spec posterior | Autorización del propietario |

## 9. Limitaciones

- El inventario de hallazgos no admite filas de este informe: la tabla de `§4` se limita a los 5 informes anteriores y la escritura de filas corresponde al `documenter`, de modo que los cinco hallazgos emitidos no computan en el cálculo de precedencia hasta que se registren.
- La verificación de la veracidad de la evidencia transcrita no forma parte de las comprobaciones del validador (`docs/sdd/PROTOCOLO_OPERATIVO.md:348`); este informe contrasta la cita con el archivo y la línea, ejecuta las tres suites del corte y no acredita la ejecución histórica que cada fila de tarea declara.
- La firma del merge `c49b6f3` devuelve `E`, que señala una firma que no se puede comprobar con las claves disponibles en el repositorio; la firma no es exigible para un merge y los cuatro commits examinados —`10d06f8`, `eacb2a1`, `083ab05` y `283c4dc`— devuelven `G`.
- La eliminación remota de la rama de trabajo se acreditó con `git branch -r --list origin/feat/gemma-4-26b-a4b-it-qat-gguf` sin resultado y no con `git ls-remote --heads origin`, que la lista blanca del rol en esta sesión no admite; el registro del reporte transcribe una consulta al remoto que este informe no reprodujo.
- No se ejecutó la prueba de carga del servidor ni la sonda de contexto: el corte no dispone de la GPU ni de los 4 artefactos locales, de modo que el contraste del contrato se sostiene sobre los 33 registros de `results/gemma/`, los manifiestos de `src/gemma/perfiles/` y las 140 pruebas de la feature, y no sobre una medición nueva.
- La conformidad del régimen completo y la suficiencia del protocolo quedan fuera del alcance de un informe de conformidad puntual (`docs/sdd/PROTOCOLO_OPERATIVO.md:352`).
- La presencia de este informe deja en rojo la prueba `test_inventario_del_corpus` de `tools/sdd/tests` con «`docs/sdd/README.md` no registra la fila de `docs/sdd/auditoria_release_v0_8_0.md`» (anexo M). El fallo es el efecto declarado de la escritura del rol y se cierra con la fila del corpus que redacta el `documenter`; hasta entonces el check `verify` queda en rojo y la integración del informe está detenida, conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md:305`.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | «Comprobación de historial: punto de corte el tag anotado v0.7.2, 10 commits examinados»; 17 comprobaciones; 0 `[ERROR]`; 56 `[WARN]` de la cláusula de legado; código 0 | `python tools\sdd\validate.py --all` |
| B | `OK: sin hallazgos` en `--spec SPEC-017`, `--gate G1`, `--gate G4` y `--gate G5`; el último activa las comprobaciones «firma del commit de aprobación y clave autorizada» y «G5: merge de dos padres en `dev`, integración de la rama, validación posterior y rama ausente» | `python tools\sdd\validate.py --spec SPEC-017 [--gate Gx]` |
| C | «Ran 140 tests in 7.316s» y «OK»; «Ran 223 tests in 1.599s» y «OK» en el corte, antes de añadir este informe; «Ran 48 tests in 22.026s» y «OK». Entre las líneas de la suite de la feature: `test_promocion_con_derrame_de_511_mib_es_elegible: derrame=511 MiB estado=('aprobado', None)`, `test_promocion_con_derrame_de_512_mib_es_elegible: derrame=512 MiB`, `test_promocion_con_derrame_de_513_mib_no_es_elegible: … elegible=False`, `test_comprobacion_3_enumera_los_9_ejes: detalle=9 opciones enumeradas por el binario: cache_type_k --cache-type-k, cache_type_v --cache-type-v, ctx_size --ctx-size, flash_attn --flash-attn, gpu_layers --n-gpu-layers, load_mode --load-mode, ncmoe --n-cpu-moe, parallel --parallel, ubatch --ubatch-size` y `test_presupuesto_con_clave_retirada_es_rechazado` | `python -m unittest discover -s tools\gemma\tests -q`; `-s tools\sdd\tests -q`; `-s tools\git\tests -q` |
| D | `10d06f8` → `G`, `sebaxtianrioss@gmail.com`, «renovar G1 sobre el contrato 0.11.0»; `eacb2a1` → `G`, «registrar la aprobacion G4»; `083ab05` → `G`; `283c4dc` → `G`; `c49b6f3` → `E` | `git log -1 --format='%H %G? %GS %s'` sobre cada commit |
| E | `c49b6f3` con padres `7a6bbe4` y `bddc922`; `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf` y `git branch -r --list origin/feat/gemma-4-26b-a4b-it-qat-gguf` sin salida; `git rev-parse --short dev` → `c49b6f3` | `git log -1 --format='%H %P %s'`; `git branch` |
| F | `refs/tags/v0.8.0` inexistente (`exit 1` con `--verify --quiet`); `v0.7.2` resuelve a `a9e7019`; `git merge-base --is-ancestor main dev` con código 0 | `git rev-parse`; `git merge-base` |
| G | 33 registros en `results/gemma/` —11 en `rendimiento/` y 22 en `resiliencia/`—; exactamente 13 con el campo 14 por debajo de `512 MiB`; el registro `20261122T203814Z-resiliencia-carga-inicial` declara `proposito: carga`, 21 filas y `56 MiB`; `20261124T190907Z-resiliencia-comparacion-ncmoe` declara `proposito: comparacion`, 22 filas, campo 14 `3889 MiB`, campo 19 `4346 MiB` y campo 22 `4071.38 MiB` (derrame `274.62 MiB`) | Lectura de `results/gemma/**` |
| H | `rendimiento.json` y `resiliencia.json` declaran 9 ejes con `cache_type_k` y `cache_type_v` en `q8_0`, el presupuesto de 4 claves, `estado: candidato`, `aprobacion: null` y `designacion: null`; `rendimiento.json:41-46` conserva la desviación `ctx_size` `4096` → `131072` con `comparacion` en `null`; `parametros_iniciales.json:6-8` declara `flash_attn` `on` con la fuente de `DEC-029` | Lectura de `src/gemma/perfiles/` |
| I | `spec.md:4-5` en `validated` 0.15.0 y `specs/INDEX.md:23` en `validated` frente a `MEMORY.md:13` en `implemented`; `CHANGELOG.md:11-13` con `Unreleased` vacío y `v0.7.2` como última entrada; `git diff v0.7.2 --stat -- CHANGELOG.md` sin salida | Lectura contrastada de las cuatro rutas y `git diff` |
| J | `c5d1b1d` incorpora a `docs/sdd/PROTOCOLO_OPERATIVO.md` la fila `T11`, el párrafo de reapertura, el bloque de reglas y la «Constancia de corrección» del 2026-11-23; añade `"T11": (("tasked", "implementing", "implemented", "validated"), "draft")` a `TRANSITIONS` de `tools/sdd/validate.py` y 65 líneas a `tools/sdd/tests/test_validate.py` | `git show c5d1b1d -- docs/sdd/PROTOCOLO_OPERATIVO.md tools/sdd/validate.py tools/sdd/tests/test_validate.py` |
| K | 82 filas en `inventario_hallazgos.md:33-114` y 3 en `:160-162`; 77 `cerrado`, 3 `cerrado` en el registro separado, 5 `cerrado por ratificación` y 0 abiertos; veredicto declarado `CONFORME` en `:150`; 0 observaciones y 0 tratamientos en `:144-146` | Lectura de `docs/sdd/inventario_hallazgos.md` |
| L | 41 filas en la tabla de inventario del corpus (`docs/sdd/README.md:28-70`) frente a 41 archivos del corpus; ninguna fila registra `docs/sdd/auditoria_release_v0_8_0.md` | Lectura de `docs/sdd/README.md` y listado de `docs/sdd/` |
| M | «Ran 223 tests in 1.626s» y «FAILED (failures=1)»: `test_inventario_del_corpus` devuelve «`docs/sdd/README.md` no registra la fila de `docs/sdd/auditoria_release_v0_8_0.md`». El fallo es el efecto declarado de este informe y se cierra con la fila 42 que escribe el `documenter` | `python -m unittest discover -s tools\sdd\tests -q` con este informe presente |
