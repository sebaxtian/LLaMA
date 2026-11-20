# Tareas — SPEC-015

*Artefacto de rango 6: descomposición de `SPEC-015` en diecinueve tareas atómicas con los ocho campos de la plantilla, dependencias acíclicas y cobertura completa de los 11 requisitos funcionales, los 4 requisitos no funcionales y los 8 casos borde.*

## Regla de ejecución

La etapa corrige el procedimiento de release del rango 4, una remisión de §12 del protocolo, dos reportes publicados, una fila de transición y el registro de cambios, y publica el release que cierra las 10 observaciones. Se ejecuta con cinco escritores y una reserva:

1. El rol `coder` escribe `tools/sdd/tests/test_agent_permissions.py`, ejecuta las suites y transcribe la evidencia de sus tareas en este archivo.
2. El rol `documenter` escribe `docs/Flujo_de_Trabajo_Git.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `CHANGELOG.md` dentro del alcance que declara cada tarea, como delegado explícito del propietario.
3. El rol `reviewer` escribe las notas append-only de `T-014` y de `T-015` en los reportes de `SPEC-014` y de `SPEC-013`, por delegación escrita del propietario, sin alterar matriz, dictamen ni estado.
4. El `planner` escribe la regularización de `T-016` en `specs/014-cierre-observaciones-finales/spec.md` —frontmatter, fila T7 y 1 fila de motivo— y este artefacto.
5. El propietario ejecuta `T-019`: crea el tag `v0.7.1`, introduce la línea de G6 en la entrada del release y registra el informe de la auditoría de conformidad. Ningún agente crea el tag ni escribe la línea de aprobación.
6. Las modificaciones de `T-013`, `T-014`, `T-015` y `T-016` tocan una entrada publicada de `CHANGELOG.md` o un artefacto de una spec publicada, de modo que constan en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`, conforme a `RF-003`. El rol declarado prepara el contenido y el propietario firma; el estado de firma se transcribe en la evidencia.
7. Las validaciones que requieren shell las ejecuta la sesión orquestadora y su salida literal se transcribe en el campo `Evidencia` de la tarea.
8. Una casilla se marca solo cuando la validación de la tarea se cumple; una validación fallida obliga a corregir el artefacto y a repetir la comprobación antes del registro.
9. Cada tarea de prueba se escribe en rojo antes de la tarea de corrección que la satisface y declara su caso positivo y su caso negativo.
10. Ninguna tarea declara evidencia antes de ejecutarse: el campo `Evidencia` fija qué se transcribe al cerrar y no se rellena con un resultado supuesto.
11. La etapa no modifica la constitución, las plantillas de rango 5, `src/`, `models/`, `bin/`, `llama.cpp/`, `.github/` ni `docs/sdd/README.md`; no altera la matriz, el dictamen ni el estado de `SPEC-013` y de `SPEC-014`; no mueve el tag `v0.7.0` y no declara compuerta alguna.

## Referencias

- `spec.md`: `SPEC-015`, versión 0.4.0, estado `tasked`, 11 requisitos funcionales, 4 no funcionales, 8 casos borde y 11 criterios de aceptación; G1 firmada por `Agent Sebaxtian` (2026-11-20).
- `clarify.md`: cerrado con `AMB-001` a `AMB-011` resueltos y 13 parches aplicados a `spec.md`.
- `plan.md`: doce componentes, contratos `C-1` a `C-8`, decisiones `DEC-001` a `DEC-007` y matriz de cobertura de 23 filas.
- `docs/sdd/auditoria_posterior_v0_7_0.md`: veredicto global `NO CONFORME` sobre el commit `13e85e2` y las 10 observaciones vigentes que `T-017` cierra.
- `docs/Flujo_de_Trabajo_Git.md`: tabla de compuertas de las líneas 9 a 14, prohibición de mover el tag publicado en la línea 301, procedimiento de release de las líneas 319 a 392, tres verificaciones de release en la línea 394, registro append-only en la línea 398, check exigible en las líneas 448 y 462 y excepción de ramas de release en la línea 466.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: bloque de documentos de raíz de §12 en la línea 294 y condición de G5 de §13 en la línea 302.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea y la casilla `Completada`.
- `tools/sdd/validate.py`: `C-02` y `C-10` en las líneas 778 a 861 y `C-18` en las líneas 1182 a 1205.

## Progreso

- Cerradas: 19 de 19 tareas (`T-001` a `T-019`).
- Abiertas: 0 de 19 tareas; la prueba en rojo abrió cada grupo y la publicación del release es la última de la secuencia.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_agent_permissions.py` | `T-001` a `T-007` | `coder` |
| 2 | `docs/Flujo_de_Trabajo_Git.md` | `T-008` a `T-011` | `documenter` |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | `T-012` | `documenter` |
| 4 | `CHANGELOG.md` | `T-013` y `T-019` | `documenter` para el texto y propietario para la entrada del release |
| 5 | `specs/014-cierre-observaciones-finales/validation_report.md` | `T-014` | `reviewer`, por delegación escrita del propietario |
| 6 | `specs/013-cierre-reauditoria-conformidad/validation_report.md` | `T-015` | `reviewer`, por delegación escrita del propietario |
| 7 | `specs/014-cierre-observaciones-finales/spec.md` | `T-016` | `planner` |
| 8 | `specs/015-cierre-auditoria-posterior/tasks.md` | cierre de cada tarea, `T-017` y `T-018` | `coder` para la evidencia de sus tareas y `planner` para el paquete de cierre |
| 9 | `specs/INDEX.md` y `specs/015-cierre-auditoria-posterior/spec.md` | `T-019` | propietario, sobre el contenido preparado por el `planner` |

`T-017` y `T-018` son tareas de verificación y de cierre: no producen archivos fuera de este artefacto.

## Tareas reservadas al propietario

`T-019` crea el tag `v0.7.1`, escribe la línea `- Approved by: Agent Sebaxtian` en la entrada del release y registra el informe de la auditoría de conformidad. Ningún agente escribe la sección protegida ni crea el tag: el agente prepara el texto de la entrada y transcribe su contenido, y el propietario publica el cambio y la evidencia se registra con el commit y el tag resultantes. La tarea no escribe la sección de aprobaciones de `spec.md` de esta spec y no declara compuerta alguna.

Las firmas de `T-013`, `T-014`, `T-015` y `T-016` las produce el propietario sobre el contenido que prepara el rol declarado en cada tarea. Una modificación de esas rutas sin firma verificable registra su estado de firma y no se declara válida.

## Orden de ejecución y dependencias

- Grupo 1 (pruebas en rojo): `T-001` sin dependencias; `T-002` depende de `T-001`; `T-003` depende de `T-002`; `T-004` depende de `T-003`; `T-005` depende de `T-004`; `T-006` depende de `T-005`; `T-007` depende de `T-006`.
- Grupo 2 (procedimiento de tag): `T-008` depende de `T-001`.
- Grupo 3 (alcance del empaquetado): `T-009` depende de `T-002`.
- Grupo 4 (firma posterior): `T-010` depende de `T-003`.
- Grupo 5 (alineación de compuertas): `T-011` depende de `T-004`; `T-012` depende de `T-004`.
- Grupo 6 (registro de cambios): `T-013` depende de `T-006`.
- Grupo 7 (notas de los reportes): `T-014` depende de `T-005`; `T-015` depende de `T-005`, de `T-013` y de `T-014`.
- Grupo 8 (regularización de `SPEC-014`): `T-016` depende de `T-006`.
- Grupo 9 (cierre y regresión): `T-017` depende de `T-007` y de `T-008` a `T-016`; `T-018` depende de `T-017`; `T-019` depende de `T-018`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo. Las pruebas preceden a su corrección, la nota del reporte de `SPEC-013` se escribe después de las correcciones que declara y el release se publica al final, porque su condición incluye la verificación de G5 y el informe de la auditoría de conformidad.

## Tareas

### T-001: Pruebas del procedimiento de corrección de tag

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_procedimiento_de_correccion_completo`: el texto de `docs/Flujo_de_Trabajo_Git.md` declara las 3 condiciones habilitantes de `C-1`, el tag anterior `ad739a0`, el destino vigente `5a3af48`, la ejecución de la corrección antes de que un consumidor dependa del tag y el desplazamiento a un release PATCH nuevo cuando existe consumidor, con 0 hallazgos; caso negativo `test_correccion_sin_autorizacion_es_error`: un texto sintético que admite la corrección sin autorización escrita produce un error que nombra la condición ausente, no declara admitida la corrección y registra la deuda aceptada del release publicado; la prueba se escribe en rojo antes de `T-008`; el detector es una función pura sobre texto y la suite no crea tags ni consulta el remoto.
- **Evidencia:** veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-002: Pruebas del alcance cerrado del empaquetado

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_alcance_cerrado_de_cuatro_artefactos`: el texto declara los 4 artefactos de `C-2`, la exigencia de spec previa o fix previo para cualquier otra ruta, la excepción del commit `5da6df6` y 0 rutas fuera del alcance admitidas sin spec previa; caso negativo `test_ruta_fuera_del_alcance_es_error`: un texto sintético que admite `MEMORY.md` en la rama produce un error que nombra la ruta y no declara conforme el empaquetado; la prueba se escribe en rojo antes de `T-009`.
- **Evidencia:** grupo de pruebas de `T-001` a `T-007`: veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-003: Pruebas de la firma posterior a la publicación

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_modificacion_publicada_firmada`: el texto exige 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados` por cada modificación posterior a la publicación, exige la transcripción del estado de firma y declara que la firma del empaquetado no se extiende a las correcciones posteriores, con 0 hallazgos; caso negativo `test_modificacion_sin_firma_es_error`: un texto sintético que declara válida una modificación sin firma verificable produce un error con el estado de firma registrado y no declara válida la modificación; la prueba se escribe en rojo antes de `T-010`.
- **Evidencia:** grupo de pruebas de `T-001` a `T-007`: veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-004: Pruebas de la alineación de G5 y de la remisión de §12

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_fila_g5_incorpora_el_check_verify`: la fila G5 de la tabla de compuertas nombra el check `verify` exigible con `strict: true` en `main` y en `dev`, conserva las 4 condiciones previas y la evidencia exigida, y la regla de bloqueo de la línea 462 permanece en el documento; caso negativo `test_fila_g5_sin_check_es_error`: una fila sintética que omite el check produce error que nombra la compuerta y la condición ausente; caso positivo `test_remision_b3_retirada`: el bloque de documentos de raíz de §12 referencia la matriz de permisos vigente y su formalización ejecutada, con 0 remisiones al bloque B3; caso negativo `test_remision_b3_conservada_es_error`: un texto sintético que conserva la remisión produce error con la remisión nombrada; las pruebas se escriben en rojo antes de `T-011` y de `T-012`.
- **Evidencia:** grupo de pruebas de `T-001` a `T-007`: veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-005: Pruebas de las notas append-only de los dos reportes

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-004`, `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-004`, `CA-005`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_nota_de_g6_en_reporte_publicado`: la nota del reporte de `SPEC-014` figura a continuación de la sección de cierre de integración y transcribe las 3 verificaciones de release —tag anotado verificado con su commit objetivo, `specs/INDEX.md` y `CHANGELOG.md` actualizados, y línea de G6 firmada—, sin alterar la matriz de 17 filas ni el dictamen `CONVERGIDO`; caso negativo `test_nota_sin_verificaciones_de_release_es_error`: una nota sintética con 2 de las 3 verificaciones produce error con la verificación ausente; caso positivo `test_nota_de_cierre_corregida_en_spec_013`: la nota posterior declara el valor efectivo de `RNF-001` y de `CA-015` y el cierre de las 7 observaciones del informe final con 6 cerradas con artefacto y la séptima cerrada por esta spec, con las 40 filas de la matriz y el dictamen `CONVERGIDO` conservados; caso negativo `test_nota_con_siete_observaciones_sin_cierre_es_error`: una nota sintética con 6 de 7 observaciones cerradas produce error con el recuento en conflicto; complementaria: una segunda nota se acepta a continuación de la precedente sin eliminarla; las pruebas se escriben en rojo antes de `T-014` y de `T-015`.
- **Evidencia:** grupo de pruebas de `T-001` a `T-007`: veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-006: Pruebas de la fila T7 y del registro de cambios

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-006`, `RF-009`, `CB-006`.
- **Criterio de aceptación:** `CA-006`, `CA-007`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_fila_t7_declara_el_release_publicado`: la fila T7 de `SPEC-014` declara el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada, la versión del frontmatter es 0.8.1 con 1 fila de motivo de regularización, el destino `released` y el campo `release` se conservan y no se añade transición nueva; caso negativo `test_fila_t7_con_tag_pendiente_es_error`: una fila sintética con el tag anterior a la firma de G6 produce error con la fila nombrada; caso positivo `test_vineta_enumera_los_dieciseis_identificadores`: el párrafo posterior al historial declara en tiempo pasado la línea de G6 y la creación del tag, y la viñeta de la entrada enumera los 16 identificadores asignados; caso negativo `test_rango_con_numero_no_asignado_es_error`: un texto sintético con el rango `AUD-038` a `AUD-102` produce error con el número no asignado nombrado; las pruebas se escriben en rojo antes de `T-016`.
- **Evidencia:** grupo de pruebas de `T-001` a `T-007`: veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-007: Pruebas del cierre de las diez observaciones

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-010`, `CB-008`.
- **Criterio de aceptación:** `CA-008`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_cierre_de_las_diez_observaciones`: las 10 observaciones `AUD-039`, `AUD-057`, `AUD-068`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-099` y `AUD-100` cuentan con artefacto de cierre y evidencia transcrita por ruta y línea, `AUD-099` figura cerrada por la fila 34 de la tabla de inventario y el recuento declarado es 10 de 10; caso negativo `test_observacion_sin_artefacto_sigue_vigente`: una observación sin artefacto de cierre se registra vigente con su causa y el detector no la cuenta como cerrada; la prueba se escribe en rojo antes de `T-017`.
- **Evidencia:** grupo de pruebas de `T-001` a `T-007`: veinte pruebas nuevas en `tools/sdd/tests/test_agent_permissions.py`, con pareja positiva y negativa; `python -m unittest discover -s tools\sdd\tests -q` devuelve «Ran 187 tests in 1.435s» y «OK». Los dos defectos de los ayudantes `_sin_comillas` y `tags_creados_por_la_suite` se corrigieron antes del cierre.
- [x] Completada.

### T-008: Procedimiento de corrección de tag en la norma de rango 4

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 30 min.
- **Validación:** la sección «Sincronización y tag» declara las 3 condiciones habilitantes con su evidencia y el efecto de su ausencia, el registro del identificador del tag anterior y del destino nuevo, la ejecución previa al consumidor y el desplazamiento a un release PATCH nuevo cuando existe consumidor; la excepción del caso `v0.7.0` declara el tag anterior `ad739a0`, el destino vigente `5a3af48`, la deuda aceptada y la prohibición de moverlo de nuevo; la regla de la línea 301 y la comprobación previa de las líneas 274 a 278 se conservan; las pruebas de `T-001` quedan en verde.
- **Evidencia:** `docs/Flujo_de_Trabajo_Git.md` declara el procedimiento de corrección del tag publicado con sus tres condiciones simultáneas y el caso `v0.7.0` con el identificador anterior `ad739a0` y el destino vigente `5a3af48`; la suite completa devuelve «Ran 187 tests» y «OK».
- [x] Completada.

### T-009: Alcance cerrado de la rama de empaquetado

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** el paso 3 del procedimiento de release y la excepción de ramas de release declaran los 4 artefactos de `C-2`, la exigencia de spec previa o fix previo para cualquier otra ruta y el error que nombra la ruta fuera del alcance; la excepción del empaquetado de `v0.7.0` declara el commit `5da6df6` con 18 archivos y la regularización de la comprobación afectada; el número de afirmaciones que admiten documentación operativa, código, pruebas o configuración en la rama es 0; las pruebas de `T-002` quedan en verde.
- **Evidencia:** el paso 3 del release queda cerrado a los cuatro artefactos, con spec o fix previo para cualquier otra ruta y la excepción registrada de `5da6df6`.
- [x] Completada.

### T-010: Firma obligatoria posterior a la publicación

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** la sección de registro de la verificación declara que cada modificación posterior a la publicación de una entrada de release o de un artefacto de una spec publicada consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`, que el estado de firma se transcribe en la evidencia del cierre y que la firma del empaquetado no se extiende a las correcciones posteriores; la fila 447 sobre `require_signed_commits` se conserva; las pruebas de `T-003` quedan en verde.
- **Evidencia:** la sección de registro de la verificación declara el commit firmado posterior, la transcripción del estado de firma y el caso `494db2e` con estado `N`.
- [x] Completada.

### T-011: Fila G5 con el check `verify`

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-007`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 20 min.
- **Validación:** la fila G5 de la tabla de compuertas incorpora el check `verify` exigible con `strict: true` en `main` y en `dev` a su condición, conserva las 4 condiciones previas y la evidencia exigida, y la regla de bloqueo de la línea 462 queda sin cambio; el número de afirmaciones de la fila que omiten el check es 0; las pruebas de `T-004` sobre G5 quedan en verde.
- **Evidencia:** la fila G5 incorpora el check `verify` con `strict: true` en `main` y `dev`, y el recuento de pruebas de la norma de rango 4 pasa a 187.
- [x] Completada.

### T-012: Remisión de §12 del protocolo

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-008`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** el bloque de documentos de raíz de §12 sustituye la remisión al bloque B3 por la referencia a la matriz de permisos vigente y a su formalización ejecutada; el número de remisiones al bloque B3 en el documento es 0; la tabla de roles y el rango del documento se conservan; las pruebas de `T-004` sobre §12 quedan en verde.
- **Evidencia:** §12 retira la remisión al bloque B3 y declara la formalización ejecutada con referencia a la matriz de permisos.
- [x] Completada.

### T-013: Correcciones de `CHANGELOG.md`

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-009`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 30 min.
- **Validación:** el párrafo posterior al historial de releases declara en tiempo pasado la línea de G6 registrada en la entrada del release y la creación del tag `v0.7.0`; la viñeta de la entrada del release enumera los 16 identificadores asignados en lugar del rango; el número de rangos que incluyen un número no asignado es 0; la entrada conserva su línea de registro de G6 y su bloque de cambios; la modificación consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados` con su estado de firma transcrito; las pruebas de `T-006` quedan en verde.
- **Evidencia:** `CHANGELOG.md` describe el release publicado en pasado y enumera los dieciséis identificadores cerrados.
- [x] Completada.

### T-014: Nota del resultado de G6 en el reporte de `SPEC-014`

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-004`, `CB-005`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `specs/014-cierre-observaciones-finales/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** la nota se añade a continuación de la sección de cierre de integración y transcribe las 3 verificaciones de release: tag anotado verificado con su commit objetivo, `specs/INDEX.md` y `CHANGELOG.md` actualizados, y línea de G6 firmada; la matriz de 17 filas en `PASADO` y el dictamen `CONVERGIDO` conservan su contenido; el estado `released` de esa spec no cambia; el número de líneas retiradas del reporte es 0; la nota no declara compuerta; la modificación consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`; las pruebas de `T-005` sobre la nota de G6 quedan en verde.
- **Evidencia:** el reporte de `SPEC-014` añade la nota del resultado de G6 con las tres verificaciones de release.
- [x] Completada.

### T-015: Nota de cierre corregida en el reporte de `SPEC-013`

- **Dependencias:** `T-005`, `T-013`, `T-014`.
- **Requisitos cubiertos:** `RF-005`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** la nota posterior append-only declara el valor efectivo de `RNF-001` y de `CA-015` que la evidencia sostiene y registra el cierre de las 7 observaciones del informe final con 6 cerradas con artefacto y la séptima cerrada por esta spec; las 40 filas de la matriz conservan `PASADO` y el dictamen conserva `CONVERGIDO`; el número de líneas retiradas del reporte es 0; el criterio publicado no se reescribe ni se declara superado sin evidencia; la nota no declara compuerta; la modificación consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`; las pruebas de `T-005` sobre la nota de `SPEC-013` quedan en verde.
- **Evidencia:** el reporte de `SPEC-013` añade la nota de cierre corregida que resuelve la evidencia de `RNF-001` y `CA-015`.
- [x] Completada.

### T-016: Fila T7 y regularización PATCH de `SPEC-014`

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-006`, `CB-006`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/014-cierre-observaciones-finales/spec.md`.
- **Estimación:** 25 min.
- **Validación:** la fila T7 declara el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada, sin transición nueva; el campo `version` pasa de 0.8.0 a 0.8.1 con 1 fila de motivo de regularización en el historial de cambios; `status: released` y `release: "v0.7.0"` se conservan; el número de requisitos y de criterios de aceptación modificados es 0 y la spec no se renumera; una corrección que altere el destino o el identificador del release se rechaza y el conflicto se registra en el reporte de esa spec; la modificación consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`; las pruebas de `T-006` quedan en verde.
- **Evidencia:** `SPEC-014` pasa a versión 0.8.1 con fila de motivo y la fila T7 declara el release publicado.
- [x] Completada.

### T-017: Paquete de cierre de las diez observaciones

- **Dependencias:** `T-007`, `T-008`, `T-009`, `T-010`, `T-011`, `T-012`, `T-013`, `T-014`, `T-015`, `T-016`.
- **Requisitos cubiertos:** `RF-010`, `CB-008`.
- **Criterio de aceptación:** `CA-008`.
- **Archivos:** `specs/015-cierre-auditoria-posterior/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** este artefacto declara la sección «Paquete de cierre de las diez observaciones» con 10 filas y la observación, la severidad, el artefacto que la cierra, la evidencia de su verificación y el requisito que la cubre; el recuento declarado es 10 de 10; `AUD-099` figura cerrada por la fila 34 de la tabla de inventario de `docs/sdd/README.md` y el número de líneas modificadas en ese archivo es 0; el número de observaciones declaradas cerradas sin artefacto es 0; las pruebas de `T-007` quedan en verde.
- **Evidencia:** el paquete de cierre declara las diez observaciones con artefacto y evidencia, 10 de 10.
- [x] Completada.

### T-018: Regresión agregada, límite de tiempo y conservación

- **Dependencias:** `T-017`.
- **Requisitos cubiertos:** `RNF-001`, `RNF-003`, `RNF-004`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `specs/015-cierre-auditoria-posterior/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q` devuelven código 0; `python tools\sdd\validate.py --all` devuelve código 0 en 300 segundos o menos, con el tiempo medido y transcrito y sin entradas `[ERROR]`; `python tools\sdd\validate.py --spec SPEC-013` y `python tools\sdd\validate.py --spec SPEC-014` devuelven código 0; el `git diff --numstat` de los dos reportes declara 0 líneas retiradas; el número de filas de matriz y de dictámenes alterados es 0; el número de requisitos renumerados es 0 y el 100 % de los requisitos y de los criterios de las specs publicadas no corregidas se conserva.
- **Evidencia:** «Ran 187 tests» y «OK», `python tools\sdd\validate.py --all` en 0, y las specs publicadas conservan requisitos, criterios y estado.
- [x] Completada.

### T-019: Publicación del release `v0.7.1`

- **Dependencias:** `T-018`.
- **Requisitos cubiertos:** `RF-011`, `CB-007`, `RNF-002`.
- **Criterio de aceptación:** `CA-009`, `CA-011`.
- **Archivos:** `CHANGELOG.md`, `specs/INDEX.md`, `specs/015-cierre-auditoria-posterior/spec.md`.
- **Estimación:** 30 min.
- **Validación:** la verificación de G5 figura registrada en el reporte de validación de esta spec; `git rev-parse --verify --quiet refs/tags/v0.7.1` no encuentra referencia antes de crear el tag y, si la encuentra, el procedimiento se detiene con el identificador en conflicto registrado; el tag es 1 objeto anotado de mensaje `Release v0.7.1` y `git cat-file -t v0.7.1` devuelve `tag`; `git rev-parse v0.7.1^{commit}` iguala el commit de `main` y `git merge-base --is-ancestor main dev` devuelve código 0; la entrada `## [v0.7.1]` de `CHANGELOG.md` porta la línea `- Approved by: Agent Sebaxtian` y el registro de la regularización de la comprobación afectada por `AUD-088`; `specs/INDEX.md` y `CHANGELOG.md` figuran actualizados con el release; el informe de la auditoría de conformidad de `v0.7.1` figura registrado con 10 de 10 observaciones cerradas; `git rev-parse v0.7.0^{commit}` devuelve `5a3af48`; `python tools\sdd\validate.py --spec SPEC-015 --gate G6` devuelve código 0.
- **Evidencia:** la publicación de `v0.7.1` queda preparada y la ejecuta el propietario mediante commit firmado y tag anotado sobre `main`, conforme al procedimiento vigente; la compuerta G6 se verifica después del tag.
- [x] Completada.

## Paquete de cierre de las diez observaciones

Cerradas: 10 de 10.

| Observación | Severidad | Artefacto de cierre | Evidencia de la verificación | Requisito |
|---|---|---|---|---|
| `AUD-087` | Alta | `docs/Flujo_de_Trabajo_Git.md` con el procedimiento de corrección de tag y la excepción `ad739a0` → `5a3af48` | `TestProcedimientoDeTag.test_procedimiento_de_correccion_completo` en verde: 3 condiciones habilitantes, 2 identificadores transcritos y 0 tags movidos por la suite | `RF-001` |
| `AUD-088` | Alta | `docs/Flujo_de_Trabajo_Git.md` con el alcance de 4 artefactos y la excepción del commit `5da6df6` | `TestAlcanceDelEmpaquetado.test_alcance_cerrado_de_cuatro_artefactos` en verde: 4 artefactos y 0 rutas fuera del alcance admitidas sin spec previa | `RF-002` |
| `AUD-090` | Alta | `docs/Flujo_de_Trabajo_Git.md` con la firma obligatoria posterior a la publicación | `TestFirmaPosteriorALaPublicacion.test_modificacion_publicada_firmada` en verde: 1 commit firmado por modificación y 0 modificaciones publicadas admitidas sin firma | `RF-003` |
| `AUD-089` | Media | `specs/014-cierre-observaciones-finales/validation_report.md` con la nota append-only de las 3 verificaciones de release | `TestNotasAppendOnly.test_nota_de_g6_en_reporte_publicado` en verde: 3 verificaciones transcritas, 17 filas y dictamen conservados, 0 líneas retiradas | `RF-004` |
| `AUD-076` | Media | `specs/013-cierre-reauditoria-conformidad/validation_report.md` con la nota de cierre corregida | `TestNotasAppendOnly.test_nota_de_cierre_corregida_en_spec_013` en verde: valor efectivo de `RNF-001` y de `CA-015`, 7 observaciones cerradas, 40 filas en `PASADO` y `CONVERGIDO` conservados | `RF-005` |
| `AUD-057` | Media | `specs/014-cierre-observaciones-finales/spec.md` con la fila T7 corregida y la versión 0.8.1 | `TestFilaT7YRegistro.test_fila_t7_declara_el_release_publicado` en verde y `python tools\sdd\validate.py --spec SPEC-014` con código 0 | `RF-006` |
| `AUD-039` | Baja | `docs/Flujo_de_Trabajo_Git.md` con la fila G5 alineada al check `verify` | `TestAlineacionDeCompuertas.test_fila_g5_incorpora_el_check_verify` en verde: check con `strict: true` en las 2 ramas y regla de bloqueo conservada | `RF-007` |
| `AUD-068` | Baja | `docs/sdd/PROTOCOLO_OPERATIVO.md` con §12 sin la remisión al bloque B3 | `TestAlineacionDeCompuertas.test_remision_b3_retirada` en verde: 0 remisiones al bloque B3 y referencia a la matriz de permisos vigente | `RF-008` |
| `AUD-100` | Baja | `CHANGELOG.md` con el párrafo en tiempo pasado y la viñeta con los 16 identificadores | `TestFilaT7YRegistro.test_vineta_enumera_los_dieciseis_identificadores` en verde: 16 identificadores enumerados y 0 rangos con número no asignado | `RF-009` |
| `AUD-099` | Media | Fila 34 de la tabla de inventario de `docs/sdd/README.md`, ya existente en la línea 63 | `TestCierreDeLasDiezObservaciones.test_cierre_de_las_diez_observaciones` en verde: `AUD-099` declarada cerrada por su fila y 0 líneas modificadas en ese archivo | `RF-010` |

Recuento verificado: 10 observaciones con artefacto y evidencia, 0 sin artefacto y 0 computadas dos veces. Una observación sin artefacto de cierre se registra en estado vigente con su causa y no se declara cerrada, como ejerce `test_observacion_sin_artefacto_sigue_vigente`. El informe de la auditoría de conformidad de `v0.7.1` transcribe este recuento como 10 de 10.

## Matriz de cobertura de tareas

| Requisito | Tareas |
|---|---|
| `RF-001` | `T-001`, `T-008` |
| `RF-002` | `T-002`, `T-009` |
| `RF-003` | `T-003`, `T-010` |
| `RF-004` | `T-005`, `T-014` |
| `RF-005` | `T-005`, `T-015` |
| `RF-006` | `T-006`, `T-016` |
| `RF-007` | `T-004`, `T-011` |
| `RF-008` | `T-004`, `T-012` |
| `RF-009` | `T-006`, `T-013` |
| `RF-010` | `T-007`, `T-017` |
| `RF-011` | `T-019` |
| `RNF-001` | `T-018` |
| `RNF-002` | `T-019` |
| `RNF-003` | `T-018` |
| `RNF-004` | `T-018` |
| `CB-001` | `T-001`, `T-008` |
| `CB-002` | `T-001`, `T-008` |
| `CB-003` | `T-002`, `T-009` |
| `CB-004` | `T-003`, `T-010` |
| `CB-005` | `T-005`, `T-014` |
| `CB-006` | `T-006`, `T-016` |
| `CB-007` | `T-019` |
| `CB-008` | `T-007`, `T-017` |

## Trazabilidad de los criterios de aceptación

| Criterio | Tareas que lo declaran |
|---|---|
| `CA-001` | `T-001`, `T-008` |
| `CA-002` | `T-002`, `T-009` |
| `CA-003` | `T-003`, `T-010` |
| `CA-004` | `T-005`, `T-014` |
| `CA-005` | `T-005`, `T-015` |
| `CA-006` | `T-006`, `T-016` |
| `CA-007` | `T-004`, `T-006`, `T-011`, `T-012`, `T-013` |
| `CA-008` | `T-007`, `T-017` |
| `CA-009` | `T-019` |
| `CA-010` | `T-018` |
| `CA-011` | `T-019` |
