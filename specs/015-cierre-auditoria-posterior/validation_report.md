# Reporte de validación — SPEC-015

*Artefacto de rango 6 escrito por el subagente `reviewer`: audita la convergencia de `SPEC-015` sobre el commit validado y no declara compuerta. Después de G4 el documento es append-only: el registro de G5 y de G6 se añade sin alterar la matriz ni el dictamen.*

<!-- Este reporte no porta casilla ni sección de firma del propietario: el registro de G4 vive en la sección de aprobaciones de `spec.md`. -->

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/cierre-auditoria-posterior`.
- Commit validado: `9750fed`, con G3 verificada por el orquestador y la transición T4 registrada en el historial de `spec.md`.
- Estado de la spec: versión 0.5.0, con 11 requisitos funcionales, 4 requisitos no funcionales, 8 casos borde y 11 criterios de aceptación; 19 tareas cerradas en `tasks.md`. La fila de `specs/INDEX.md` línea 21 declara `implemented`, el frontmatter de `spec.md` línea 4 declara `implementing` y la transición T5 a `implemented` queda a cargo del `planner` en paralelo; `MEMORY.md` línea 13 conserva `tasked`, de modo que los tres soportes divergen en el árbol de trabajo de esta revisión y la divergencia se registra para su regularización antes de G4.
- Herramientas: Python 3.12 declarado en `.github/workflows/sdd.yml`, con `unittest` de la biblioteca estándar, `git` en Windows y el validador determinista `tools/sdd/validate.py`.
- Suite de `tools/sdd/tests`: «Ran 187 tests» y «OK», transcrito por el orquestador y en la evidencia de `T-001` a `T-018`; veinte pruebas nuevas respecto de las 167 del corte de `SPEC-014`.
- Suite de `tools/git/tests`: «Ran 48 tests» y «OK», verificada por el orquestador.
- Ejecución agregada: `python tools\sdd\validate.py --all` devuelve código 0, sin entradas `[ERROR]`, y dos ejecuciones consecutivas sobre el commit validado no presentan diferencias en el conjunto de hallazgos, ambas verificadas por el orquestador.
- Ejecución de la spec: `python tools\sdd\validate.py --spec SPEC-015` transcrita de la verificación del orquestador, con código 0 y sin entradas `[ERROR]`; esta sesión no la reejecuta por ausencia de shell.
- Alcance de esta revisión: la sesión del subagente `reviewer` no dispone de shell, de modo que la evidencia de ejecución se transcribe de la verificación registrada por el orquestador y del campo `Evidencia` de `tasks.md`, y la convergencia de los 23 requisitos se contrasta por lectura de los artefactos con su ruta y su línea.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | `TestProcedimientoDeTag.test_procedimiento_de_correccion_completo` y `test_correccion_sin_autorizacion_es_error`, en la suite de 187 pruebas en verde; lectura de `docs/Flujo_de_Trabajo_Git.md` líneas 305 y 307 | el procedimiento exige las 3 condiciones habilitantes de forma simultánea —autorización escrita, registro del identificador anterior y ausencia de consumidores—, fija la ejecución antes de que un consumidor dependa del tag y el desplazamiento a un release PATCH nuevo; el caso `v0.7.0` figura como excepción con el tag anterior `ad739a0`, el destino vigente `5a3af48` y la deuda aceptada del release publicado | PASADO |
| `RF-002` | `CA-002` | `TestAlcanceDelEmpaquetado.test_alcance_cerrado_de_cuatro_artefactos` y `test_ruta_fuera_del_alcance_es_error`; lectura de `docs/Flujo_de_Trabajo_Git.md` líneas 340, 375 y 474 | el paso 3 del release se limita a `CHANGELOG.md`, `specs/INDEX.md`, el frontmatter de las specs publicadas y la línea `Release:` de los reportes publicados, exige spec previa o fix previo para cualquier otra ruta y detiene el empaquetado con la ruta nombrada; la excepción del commit `5da6df6` con 18 archivos queda registrada con la regularización de la comprobación afectada | PASADO |
| `RF-003` | `CA-003` | `TestFirmaPosteriorALaPublicacion.test_modificacion_publicada_firmada` y `test_modificacion_sin_firma_es_error`; lectura de `docs/Flujo_de_Trabajo_Git.md` línea 406 | cada modificación posterior a la publicación consta en 1 commit firmado con una clave de `docs/sdd/firmantes_autorizados` y su estado de firma se transcribe en la evidencia del cierre; el caso registrado es el commit `494db2e` con estado de firma `N`, no admitido como modificación válida | PASADO |
| `RF-004` | `CA-004` | `TestNotasAppendOnly.test_nota_de_g6_en_reporte_publicado` y `test_nota_sin_verificaciones_de_release_es_error`; lectura de `specs/014-cierre-observaciones-finales/validation_report.md` líneas 59 a 70 | la nota append-only transcribe las 3 verificaciones de release —ancestría `main` → `dev` con código 0, tag anotado `f4a6203` de mensaje `Release v0.7.0` con commit objetivo `5a3af48`, y `specs/INDEX.md` y `CHANGELOG.md` actualizados con la línea de G6 firmada—; las 17 filas y el dictamen de ese reporte conservan su contenido, el estado `released` no cambia y la nota no registra compuerta | PASADO |
| `RF-005` | `CA-005` | `TestNotasAppendOnly.test_nota_de_cierre_corregida_en_spec_013` y `test_nota_con_siete_observaciones_sin_cierre_es_error`; lectura de `specs/013-cierre-reauditoria-conformidad/validation_report.md` líneas 116 a 126 | la nota posterior declara el valor efectivo `PARCIAL` de `RNF-001` y de `CA-015`, con la causa de las 5 de 11 dimensiones con observación vigente, y el cierre de las 7 observaciones del informe final con 6 cerradas con artefacto y `AUD-075` cerrada por esta spec; las 40 filas conservan `PASADO` y el dictamen conserva `CONVERGIDO` | PASADO |
| `RF-006` | `CA-006` | `TestFilaT7YRegistro.test_fila_t7_declara_el_release_publicado` y `test_fila_t7_con_tag_pendiente_es_error`; lectura de `specs/014-cierre-observaciones-finales/spec.md` líneas 4, 5, 10, 218 y 231 | la fila T7 declara el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada; la versión pasa a 0.8.1 con la fila de motivo de regularización, se conservan `status: released`, `release: "v0.7.0"`, los requisitos y los criterios, y no se añade transición nueva | PASADO |
| `RF-007` | `CA-007` | `TestAlineacionDeCompuertas.test_fila_g5_incorpora_el_check_verify` y `test_fila_g5_sin_check_es_error`; lectura de `docs/Flujo_de_Trabajo_Git.md` líneas 11, 456 y 470 | la fila G5 incorpora el check `verify` exigible con `strict: true` en `main` y en `dev` sin alterar la regla de bloqueo de la línea 470, que declara la verificación de G5 bloqueada cuando una de las dos ramas no lo exige; la tabla de protección conserva `required_status_checks` con `verify` y `strict: true` en las dos ramas | PASADO |
| `RF-008` | `CA-007` | `TestAlineacionDeCompuertas.test_remision_b3_retirada` y `test_remision_b3_conservada_es_error`; lectura de `docs/sdd/PROTOCOLO_OPERATIVO.md` línea 294 | el bloque de documentos de raíz de §12 sustituye la remisión al bloque B3 por la declaración de que la formalización de la allowlist está ejecutada y consta en la matriz de permisos vigente de los seis roles; el número de remisiones al bloque B3 en el documento es 0 y la tabla de roles de §12 conserva su contenido | PASADO |
| `RF-009` | `CA-007` | `TestFilaT7YRegistro.test_vineta_enumera_los_dieciseis_identificadores` y `test_rango_con_numero_no_asignado_es_error`; lectura de `CHANGELOG.md` líneas 17 y 225 | el párrafo posterior al historial de releases declara en tiempo pasado la línea de G6 registrada y la creación del tag `v0.7.0` sobre `5a3af48`; la viñeta de la entrada enumera los 16 identificadores asignados —`AUD-038`, `AUD-057`, `AUD-066`, `AUD-067`, `AUD-068`, `AUD-075`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-098`, `AUD-099`, `AUD-100`, `AUD-101` y `AUD-102`— y el rango con un número no asignado es 0 | PASADO |
| `RF-010` | `CA-008` | `TestCierreDeLasDiezObservaciones.test_cierre_de_las_diez_observaciones` y `test_observacion_sin_artefacto_sigue_vigente`; lectura de `specs/015-cierre-auditoria-posterior/tasks.md` líneas 284 a 301 y de `docs/sdd/README.md` línea 63 | las 10 observaciones figuran con su artefacto de cierre y su evidencia por ruta y línea, con el recuento «Cerradas: 10 de 10»; `AUD-099` figura cerrada por la fila 34 de la tabla de inventario, sin modificación de ese archivo; el número de observaciones declaradas cerradas sin artefacto es 0 | PASADO |
| `RF-011` | `CA-009` | `docs/Flujo_de_Trabajo_Git.md` líneas 380 a 400 y `tasks.md` `T-019`; `git rev-parse --verify --quiet refs/tags/v0.7.1` como comprobación previa declarada | el procedimiento de release declara la comprobación de ausencia del tag antes de crearlo, el objeto anotado con mensaje `Release vX.Y.Z`, la ancestría del tag en `main`, las tres verificaciones de release y la detención del release ante una verificación fallida; `T-019` registra la publicación como acto del propietario sobre el texto preparado y `CHANGELOG.md` línea 11 conserva `## [Unreleased]` para la entrada de `v0.7.1`. El registro material del tag se transcribe al publicar, según la nota de la sección de brechas | PASADO |
| `RNF-001` | `CA-010` | `git diff --numstat` de los dos reportes publicados y lectura de `specs/013-cierre-reauditoria-conformidad/validation_report.md` línea 124 y de `specs/014-cierre-observaciones-finales/validation_report.md` línea 68 | las dos notas son append-only: las 40 filas de `SPEC-013` y las 17 filas de `SPEC-014` conservan `PASADO` y sus dictámenes conservan `CONVERGIDO`; el número de filas de matriz y de dictámenes alterados por esta spec es 0 | PASADO |
| `RNF-002` | `CA-011` | `docs/Flujo_de_Trabajo_Git.md` líneas 382 a 389 y `docs/sdd/PROTOCOLO_OPERATIVO.md` línea 308 | el procedimiento fija que `git cat-file -t vX.Y.Z` devuelve `tag`, que `git tag -n` muestra el mensaje `Release vX.Y.Z` y que `git rev-parse vX.Y.Z^{commit}` devuelve el commit objetivo, y que `git merge-base --is-ancestor main dev` acredita la ancestría; la forma exigida para `v0.7.1` es 1 objeto anotado de mensaje `Release v0.7.1` sobre un commit de `main` ancestro de `dev`. El objeto del tag se verifica al publicar, según la nota de la sección de brechas | PASADO |
| `RNF-003` | `CA-010` | `python tools\sdd\validate.py --all` con la duración medida y transcrita en `T-018` | la ejecución agregada devuelve código 0 por debajo del umbral de 300 segundos, sin entradas `[ERROR]`, y el umbral se contrasta con la duración registrada en la evidencia de la tarea | PASADO |
| `RNF-004` | `CA-010` | `python tools\sdd\validate.py --all`, `--spec SPEC-013` y `--spec SPEC-014`, y lectura de `specs/INDEX.md` líneas 20 y 21 | las tres ejecuciones devuelven código 0; las specs publicadas que no son objeto de corrección declarada conservan sus requisitos y criterios, el 100 % de ellos se conserva en `SPEC-001` a `SPEC-014`, y el número de requisitos renumerados es 0, con los identificadores `SPEC-001` a `SPEC-015` sin reutilización | PASADO |
| `CB-001` | `CA-001` | `TestProcedimientoDeTag.test_correccion_sin_autorizacion_es_error` | una corrección sin autorización escrita del propietario produce error que nombra la condición ausente, no mueve ni recrea el tag y deja la observación como deuda aceptada del release publicado, conforme a `docs/Flujo_de_Trabajo_Git.md` línea 305 | PASADO |
| `CB-002` | `CA-001` | `TestProcedimientoDeTag.test_procedimiento_de_correccion_completo` | con un consumidor que depende del tag, la corrección no se admite y se desplaza a un release PATCH nuevo con su propio tag; el texto declara la condición y el cauce de sustitución | PASADO |
| `CB-003` | `CA-002` | `TestAlcanceDelEmpaquetado.test_ruta_fuera_del_alcance_es_error` | un texto que admite `MEMORY.md` en la rama de empaquetado produce un error que nombra la ruta y no declara conforme el empaquetado; `docs/Flujo_de_Trabajo_Git.md` línea 340 declara la detención y el registro del hallazgo | PASADO |
| `CB-004` | `CA-003` | `TestFirmaPosteriorALaPublicacion.test_modificacion_sin_firma_es_error` | una modificación posterior sin firma verificable produce el registro del estado de firma y no se declara válida, con el caso `494db2e` y estado `N` transcrito en `docs/Flujo_de_Trabajo_Git.md` línea 406 | PASADO |
| `CB-005` | `CA-004` | `TestNotasAppendOnly.test_nota_de_g6_en_reporte_publicado` y lectura de `specs/014-cierre-observaciones-finales/validation_report.md` líneas 57 a 70 | la nota nueva se añade a continuación de la sección de cierre de integración sin eliminar la precedente, con 0 líneas retiradas, y la matriz y el dictamen conservan su contenido | PASADO |
| `CB-006` | `CA-006` | `TestFilaT7YRegistro.test_fila_t7_declara_el_release_publicado` y lectura de `specs/014-cierre-observaciones-finales/spec.md` líneas 4 y 10 | el destino `released` y el campo `release: "v0.7.0"` se conservan en la corrección de la fila T7; una corrección que altere el destino o el identificador del release se rechaza y el conflicto se registra en el reporte de esa spec | PASADO |
| `CB-007` | `CA-009` | `docs/Flujo_de_Trabajo_Git.md` líneas 377 a 381 y 400 | el procedimiento exige `git rev-parse --verify --quiet refs/tags/vX.Y.Z` antes de crear el tag, declara que el comando no debe encontrar una referencia y detiene el release ante una verificación fallida, de modo que un tag existente detiene la publicación con su identificador en conflicto registrado | PASADO |
| `CB-008` | `CA-008` | `TestCierreDeLasDiezObservaciones.test_observacion_sin_artefacto_sigue_vigente` | una observación sin artefacto de cierre se registra vigente con su causa y el detector no la cuenta como cerrada, con el recuento verificado por debajo de 10 de 10 sobre el texto sintético | PASADO |

Las 23 filas se corresponden con 11 requisitos funcionales, 4 requisitos no funcionales y 8 casos borde. El único valor que converge es `PASADO`; cualquier otro valor abre una brecha en la sección siguiente.

## Brechas

Sin brechas abiertas: las 23 filas de la matriz figuran en `PASADO`, las dos suites quedan en verde, la ejecución agregada y la ejecución de la spec devuelven código 0 sin entradas `[ERROR]`, y las 19 tareas de `tasks.md` figuran cerradas con evidencia transcrita.

### Nota del cierre de las diez observaciones

El cierre se acredita por el artefacto que satisface cada observación y por su evidencia transcrita, no por una declaración de conjunto:

- `AUD-087` por el procedimiento de corrección de tag de `docs/Flujo_de_Trabajo_Git.md` líneas 305 y 307, con las 3 condiciones exigidas y los 2 identificadores `ad739a0` y `5a3af48` transcritos.
- `AUD-088` por el alcance cerrado de 4 artefactos de `docs/Flujo_de_Trabajo_Git.md` líneas 340, 375 y 474, con la excepción del commit `5da6df6`.
- `AUD-090` por la firma obligatoria posterior a la publicación de `docs/Flujo_de_Trabajo_Git.md` línea 406, con el caso `494db2e` y estado `N`.
- `AUD-089` por la nota append-only de las 3 verificaciones de release en `specs/014-cierre-observaciones-finales/validation_report.md` líneas 59 a 70.
- `AUD-076` por la nota de cierre corregida en `specs/013-cierre-reauditoria-conformidad/validation_report.md` líneas 116 a 126, con las 40 filas y el dictamen conservados.
- `AUD-057` por la fila T7 y la versión 0.8.1 de `specs/014-cierre-observaciones-finales/spec.md` líneas 5, 218 y 231.
- `AUD-039` por la fila G5 de `docs/Flujo_de_Trabajo_Git.md` línea 11, con el check `verify` exigible con `strict: true` en las dos ramas.
- `AUD-068` por §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md` línea 294, sin remisión al bloque B3.
- `AUD-100` por el párrafo y la viñeta de `CHANGELOG.md` líneas 17 y 225, con los 16 identificadores asignados.
- `AUD-099` por la fila 34 del informe en la tabla de inventario de `docs/sdd/README.md` línea 63, ya existente y sin modificación por esta spec.

El recuento declarado en el paquete de cierre de `tasks.md` es 10 de 10, sin doble cómputo y sin observación cerrada sin artefacto.

### Nota sobre `RNF-001` y `CA-015` de `SPEC-013`

El valor efectivo de las dos filas diferidas es `PARCIAL`, equivalente a `CONFORME CON OBSERVACIONES` en la escala de `docs/sdd/plantillas/informe_auditoria.md`: el informe final registra 0 observaciones abiertas de las 16 y 5 de las 11 dimensiones con observación vigente, de modo que el valor literal `CONFORME` y la cláusula «10 de 10 dimensiones sin observación vigente» no se satisfacen. La fila publicada conserva su contenido en `PASADO` y el criterio no se reescribe; la declaración del valor efectivo consta en la nota append-only de las líneas 116 a 126 de ese reporte y el número de líneas retiradas de ese documento es 0.

### Nota sobre la evidencia del tag `v0.7.1`

`RF-011`, `RNF-002` y `CB-007` alcanzan a la publicación del release `v0.7.1`, cuyo tag crea el propietario en la etapa Release con la declaración de G6, de modo que en el commit validado `9750fed` el objeto anotado no existe aún. La evidencia disponible y transcrita es la condición de control del requisito: el procedimiento de `docs/Flujo_de_Trabajo_Git.md` líneas 377 a 400 con la comprobación de ausencia del tag, el tipo `tag`, el mensaje `Release vX.Y.Z`, el commit objetivo y la ancestría en `main`; la preparación de `T-019`; y la conservación de `## [Unreleased]` en `CHANGELOG.md` línea 11 para la entrada de `v0.7.1`. La transcripción del objeto `v0.7.1`, de su mensaje y de su commit objetivo se añade a este documento en la etapa Release, con el registro de G6 y sin alterar la matriz ni el dictamen.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos y casos borde con evidencia PASADO).
- [ ] NO CONVERGIDO.

> El dictamen `CONVERGIDO` indica que la matriz cumple el 100 % de requisitos y casos borde con evidencia `PASADO`. No aprueba G4: la aprobación corresponde al propietario y su registro vive en la sección de aprobaciones de `spec.md`.

## Cierre de integración

Merge: 4dd07f5
Release: v0.7.1

- G5: merge 4dd07f5 con dos padres; validación posterior a la integración sin hallazgos; rama feat/cierre-auditoria-posterior eliminada en local y en remoto.
