# Reporte de validación — SPEC-014

*Artefacto de rango 6: matriz de trazabilidad y dictamen de `SPEC-014` sobre el commit validado. No porta casilla ni sección de firma del propietario: el registro de G4 corresponde a la sección de aprobaciones de `spec.md`, y la sección de cierre de integración se añade después de esa aprobación.*

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/cierre-observaciones-finales`.
- Commit validado: `cf9caf5`, implementación con G3 verificada por el orquestador. Los dos commits documentales posteriores de la rama —`5cb863e`— solo registran la transición de `spec.md` y la fila de `specs/INDEX.md`, sin cambio de comportamiento.
- Herramientas: Python 3 con `unittest` de la biblioteca estándar —el flujo declara la versión 3.12—, `git` y `python tools\sdd\validate.py`.
- Suites ejecutadas en esta revisión: `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 167 tests in 1.162s» y «OK»; `python -m unittest discover -s tools\git\tests -q` devuelve «Ran 48 tests in 21.965s» y «OK».

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | `TestFlujoDeIntegracionContinua.test_preparacion_completa_del_arbol` y lectura de `.github/workflows/sdd.yml` líneas 15 a 19 | «Ran 8 tests» y «OK»; `actions/checkout@v4` es la primera preparación del job `verify` y declara `fetch-depth: 0` y `fetch-tags: true`; la comprobación produce 0 hallazgos sobre el flujo del repositorio y el alcance enumera 3 commits de implementación sobre el historial sintético de 3 | PASADO |
| `RF-002` | `CA-002` | `TestFlujoDeIntegracionContinua.test_job_ejecuta_las_dos_suites` y lectura de `.github/workflows/sdd.yml` líneas 24 a 31 | «Ran 8 tests» y «OK»; el job `verify` declara 3 pasos de ejecución con nombre —la validación agregada, `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q`—, con las 2 suites identificadas y 0 suites fuera del job | PASADO |
| `RF-003` | `CA-003` | `TestMatrizDePermisos.test_escritura_unica_del_orquestador` y lectura de `.opencode/agents/sdd.md` líneas 44 a 55 | «Ran 17 tests» y «OK»; `.opencode/**` es la única entrada `edit` con efecto `allow`, las rutas `.github/**`, `opencode.jsonc` y `MEMORY.md` declaran `deny` explícito y las atribuciones de escritura fuera de `.opencode/**` son 0 | PASADO |
| `RF-004` | `CA-004` | `TestNotaDeCierre.test_nota_de_cierre_append_only` y lectura de la sección «Nota de cierre de la reauditoría final» del reporte de `SPEC-013` | «Ran 2 tests» y «OK»; la nota figura a continuación de la sección de cierre de integración con el veredicto `CONFORME CON OBSERVACIONES` y su equivalencia a `PARCIAL`, el cierre de las 16 observaciones con 15 artefactos y 1 exención declarada, la causa de las 7 observaciones nuevas y el estado de las 4 observaciones de esta spec; el diff del reporte declara 20 líneas añadidas y 0 retiradas | PASADO |
| `RF-005` | `CA-005` | `TestCierreDeObservaciones.test_cierre_de_las_cuatro_observaciones` y el paquete de cierre de `tasks.md` | «Ran 2 tests» y «OK»; `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` figuran con artefacto de cierre y evidencia transcrita, y el recuento declarado es «Cerradas: 4 de 4» | PASADO |
| `RNF-001` | `CA-006` | `python tools\sdd\validate.py --all` | código 0 en 2,63 s según `T-012`, por debajo del umbral de 300 s; esta revisión ejecutó el comando dos veces con código 0 y sin diferencias en el conjunto de hallazgos | PASADO |
| `RNF-002` | `CA-006` | lectura de `.github/workflows/sdd.yml` y de `docs/Flujo_de_Trabajo_Git.md` línea 232 | el job `verify` conserva `timeout-minutes: 5` en la línea 13 y cada uno de los 2 pasos de suite declara `timeout-minutes: 1` en las líneas 27 y 30 | PASADO |
| `RNF-003` | `CA-006` | `TestFlujoDeIntegracionContinua` (8 pruebas), `TestMatrizDePermisos` (17), `TestNotaDeCierre` (2) y `TestCierreDeObservaciones` (2) | cada comprobación nueva declara pareja positiva y negativa: `test_preparacion_completa_del_arbol` y `test_flujo_sin_etiquetas_es_error`, `test_job_ejecuta_las_dos_suites` y `test_flujo_con_una_suite_es_error`, `test_escritura_unica_del_orquestador` y `test_concesion_fuera_de_opencode_es_error`, `test_nota_de_cierre_append_only` y `test_nota_con_recuento_divergente_es_error`, `test_cierre_de_las_cuatro_observaciones` y `test_observacion_sin_artefacto_sigue_vigente`; `T-012` declara 6 comprobaciones con pareja y 0 sin pareja, y las 4 clases devuelven «OK» | PASADO |
| `RNF-004` | `CA-007` | `git diff --numstat 0ec38bc HEAD -- specs/013-cierre-reauditoria-conformidad` y lectura del reporte de esa spec | `20 0` en `validation_report.md` y sin líneas en `spec.md`, `clarify.md`, `plan.md` ni `tasks.md`; el frontmatter conserva `status: validated` y `version: 0.7.0`, las 40 filas de la matriz conservan `PASADO` y el dictamen conserva `CONVERGIDO` en la línea 84 | PASADO |
| `RNF-005` | `CA-007` | `TestMatrizDePermisos` y lectura de §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md`, línea 286 | «Ran 17 tests» y «OK»; §12 niega al orquestador la escritura sobre documentos, código y `specs/`, la matriz declara 1 concesión de escritura —`.opencode/**`— y el número de contradicciones sobre rutas de escritura entre matriz y protocolo es 0 | PASADO |
| `CB-001` | `CA-001` | `TestFlujoDeIntegracionContinua.test_flujo_sin_etiquetas_es_error` | sobre un flujo con profundidad completa y sin descarga de etiquetas, la comprobación informa «fetch-tags» como etiqueta ausente y deja el alcance de la referencia a la spec sin verificar, con 0 commits examinados | PASADO |
| `CB-002` | `CA-001` | `tools.sdd.tests.test_validate.TestAlcanceDeLaReferencia.test_alcance_sin_tag_usa_merge_base` | sobre un historial sin tag anotado, el alcance se acota por el ancestro común con `main`, la salida informa «ancestro» y la ausencia de etiquetas no se registra como defecto del repositorio | PASADO |
| `CB-003` | `CA-002` | `docs/Flujo_de_Trabajo_Git.md` líneas 232 y 462 y `tools.sdd.tests.test_validate.TestCheckExigibleEnG5` | la norma declara que el fallo de la suite de `tools/git/tests` deja el check `verify` en rojo y bloquea G5; `test_proteccion_sin_check_bloquea_g5` devuelve código 1 con el check ausente y la rama nombrada, y las 2 clases ejecutadas devuelven «Ran 7 tests» y «OK» | PASADO |
| `CB-004` | `CA-003` | `TestMatrizDePermisos.test_concesion_fuera_de_opencode_es_error` | un rol sintético con `edit .github/**` y efecto `allow` produce fallo con la ruta concedida; sobre la matriz real, `.github/workflows/sdd.yml`, `opencode.jsonc` y `MEMORY.md` se resuelven `deny` y `tasks.md` atribuye la primera al rol `coder` | PASADO |
| `CB-005` | `CA-004` | `TestNotaDeCierre.test_nota_de_cierre_append_only` | una segunda nota se acepta a continuación de la precedente sin eliminarla y sin alterar la matriz ni el dictamen del reporte | PASADO |
| `CB-006` | `CA-004` | `TestNotaDeCierre.test_nota_con_recuento_divergente_es_error` | una nota sintética que transcribe «15 observaciones previas» frente a las «16» del informe final produce un error que nombra el valor en conflicto y no declara la nota conforme | PASADO |
| `CB-007` | `CA-005` | `TestCierreDeObservaciones.test_observacion_sin_artefacto_sigue_vigente` | informa «AUD-075 sigue vigente: sin artefacto de cierre declarado», deja el recuento verificado en 3 de 4 y no declara cerrada la observación | PASADO |

Las 17 filas se corresponden con 5 requisitos funcionales, 5 requisitos no funcionales y 7 casos borde. El único valor que converge es `PASADO`; cualquier otro valor abre una brecha en la sección siguiente.

## Brechas

Sin brechas abiertas: las 17 filas de la matriz figuran en `PASADO`, las dos ejecuciones del validador devuelven código 0 sin entradas `[ERROR]` sobre esta spec, las dos suites quedan en verde y las 13 tareas de `tasks.md` figuran cerradas con evidencia transcrita.

- **Cierre de las observaciones por su artefacto.** El cierre se acredita por el artefacto que satisface cada observación y por la evidencia transcrita, no por una declaración de conjunto: `AUD-066` por `.opencode/agents/sdd.md`, con `.opencode/**` como única concesión de escritura del orquestador; `AUD-075` por la nota de cierre append-only del reporte de `SPEC-013`; `AUD-101` por `.github/workflows/sdd.yml`, con `fetch-depth: 0` y `fetch-tags: true`; y `AUD-102` por el paso nombrado de `tools/git/tests` en ese mismo flujo y por su declaración en `docs/Flujo_de_Trabajo_Git.md`. El recuento declarado es 4 de 4 y el número de observaciones declaradas cerradas sin artefacto es 0.
- **`SPEC-013` conserva matriz, dictamen y estado.** El diff de esa spec sobre la base `0ec38bc` solo devuelve 20 líneas añadidas y 0 retiradas en `validation_report.md`; las 40 filas de su matriz conservan `PASADO`, su dictamen conserva `CONVERGIDO` y su frontmatter conserva `status: validated` con versión 0.7.0. La nota de cierre se añade al final y no reabre requisito alguno de esa spec.
- **Registro del cierre de integración pendiente de G5.** Esta revisión no escribe la sección de cierre de integración, porque su registro corresponde al cierre de G5 sobre la base integrada. La comprobación `C-17` la exige a partir del estado `validated`, de modo que esa sección debe añadirse en la etapa siguiente sin alterar la matriz ni el dictamen de este reporte.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos y casos borde con evidencia PASADO).
- [ ] NO CONVERGIDO.

> El dictamen `CONVERGIDO` indica que la matriz cumple el 100 % de requisitos y casos borde con evidencia `PASADO`. No aprueba G4: la aprobación corresponde al propietario y su registro vive en la sección de aprobaciones de `spec.md`.

## Cierre de integración

Merge: b018ab8
Release:

- G5: merge b018ab8 con dos padres; validación posterior a la integración sin hallazgos; rama feat/cierre-observaciones-finales eliminada en local y en remoto.
