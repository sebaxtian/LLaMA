# Tareas — SPEC-014

*Artefacto de rango 6: descomposición de `SPEC-014` en trece tareas atómicas con los ocho campos de la plantilla, dependencias acíclicas y cobertura completa de los 5 requisitos funcionales, los 5 requisitos no funcionales y los 7 casos borde.*

## Regla de ejecución

La etapa corrige la preparación del árbol y el alcance del job del flujo de integración continua, la matriz del orquestador, una declaración de la norma de rango 4, una nota de cierre append-only y la suite del mecanismo. Se ejecuta con cuatro escritores y una reserva:

1. El rol `coder` escribe `.github/workflows/sdd.yml` y `tools/sdd/tests/`, y cierra sus tareas en este archivo con la evidencia transcrita.
2. El rol `documenter` escribe `docs/Flujo_de_Trabajo_Git.md` dentro del alcance declarado en `T-009`.
3. El rol `reviewer` escribe la nota de cierre append-only de `T-010` en el reporte de `SPEC-013`, por delegación escrita del propietario y sin tocar la matriz ni el dictamen de esa spec.
4. El propietario ejecuta `T-008` en `.opencode/agents/sdd.md`, ruta sin rol concesionario para los agentes; el resto de roles no escribe esa ruta.
5. El `planner` escribe este archivo y los demás artefactos de la spec; no escribe código ni artefactos de otros roles.
6. Las validaciones que requieren shell las ejecuta la sesión orquestadora y su salida literal se transcribe en el campo `Evidencia` de la tarea.
7. Una casilla se marca solo cuando la validación de la tarea se cumple; una validación fallida obliga a corregir el artefacto y a repetir la comprobación antes del registro.
8. Cada tarea de prueba se escribe en rojo antes de la tarea de corrección que la satisface y declara su caso positivo y su caso negativo.
9. Ninguna tarea declara evidencia antes de ejecutarse: el campo `Evidencia` fija qué se transcribe al cerrar y no se rellena con un resultado supuesto.
10. La etapa no modifica la constitución, las plantillas de rango 5, `src/`, `models/`, `bin/` ni `llama.cpp/`, no altera la matriz, el dictamen ni el estado `validated` de `SPEC-013` y no declara compuerta alguna.

## Referencias

- `spec.md`: `SPEC-014`, versión 0.4.0, estado `tasked`, 5 requisitos funcionales, 5 no funcionales, 7 casos borde y 7 criterios de aceptación; G1 firmada por `Agent Sebaxtian` (2026-11-14).
- `clarify.md`: cerrado con `AMB-001` a `AMB-006` resueltos y los casos borde `CB-006` y `CB-007` incorporados.
- `plan.md`: siete componentes, contratos `C-1` a `C-6`, decisiones `DEC-001` a `DEC-006` y matriz de cobertura de 17 filas.
- `docs/sdd/auditoria_final_v0_7_0.md`: observaciones `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` y veredicto global `CONFORME CON OBSERVACIONES`.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea y la casilla `Completada`.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §5 escritura de estados, §12 roles y permisos, §13 registros posteriores a G4 y §14 contrato del validador.
- `docs/Flujo_de_Trabajo_Git.md`: norma de rango 4, con la declaración de la suite en la línea 232 y la del check exigible en la línea 462.

## Progreso

- Cerradas: 13 de 13 tareas (`T-001` a `T-013`).
- Pendientes: ninguna; `T-008`, `T-009`, `T-010`, `T-012` y `T-013` quedaron cerradas con la evidencia transcrita.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_agent_permissions.py` y `tools/sdd/tests/fixtures/flujo/` | `T-001` a `T-005` | `coder` |
| 2 | `.github/workflows/sdd.yml` | `T-006` y `T-007` | `coder` |
| 3 | `.opencode/agents/sdd.md` | `T-008` | propietario |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | `T-009` | `documenter` |
| 5 | `specs/013-cierre-reauditoria-conformidad/validation_report.md` | `T-010` | `reviewer`, por delegación escrita del propietario |
| 6 | `specs/014-cierre-observaciones-finales/tasks.md` | cierre de cada tarea, `T-011` a `T-013` | `coder` para las casillas de sus tareas y `planner` para el cierre |

`T-011` a `T-013` son tareas de verificación y de cierre: no producen archivos fuera de este artefacto.

## Tarea reservada al propietario

`T-008` reduce la matriz del orquestador en `.opencode/agents/sdd.md`. La ruta no tiene rol concesionario: `.opencode/**` pertenece a la definición del rol orquestador y los agentes no declaran escritura sobre su propia matriz de permisos en este contrato. El agente prepara el diff previsto y transcribe su contenido; el propietario publica el cambio y la evidencia se registra con el commit resultante. La tarea no toca la sección de aprobaciones de `spec.md` y no declara compuerta alguna.

## Orden de ejecución y dependencias

- Grupo 1 (pruebas en rojo): `T-001` sin dependencias; `T-002` depende de `T-001`; `T-003` depende de `T-002`; `T-004` depende de `T-003`; `T-005` depende de `T-004`.
- Grupo 2 (flujo): `T-006` depende de `T-001`; `T-007` depende de `T-006` y de `T-002`.
- Grupo 3 (matriz): `T-008` depende de `T-003`.
- Grupo 4 (norma de rango 4): `T-009` depende de `T-007`.
- Grupo 5 (nota de cierre): `T-010` depende de `T-004` y de `T-009`.
- Grupo 6 (cierre y regresión): `T-011` depende de `T-005` y de `T-010`; `T-012` depende de `T-011`; `T-013` depende de `T-012`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo. La matriz se corrige después de su prueba y antes de la nota porque `CB-004` atribuye el artefacto al rol que este archivo declara, y la nota se escribe al final porque transcribe el estado de las 4 observaciones, que depende de los demás artefactos.

## Tareas

### T-001: Pruebas de la preparación completa del árbol

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`, `tools/sdd/tests/fixtures/flujo/`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_preparacion_completa_del_arbol`: la primera preparación del job declara `actions/checkout@v4` con `fetch-depth: 0` y `fetch-tags: true`, el alcance de la comprobación de la referencia enumera al menos 1 commit de implementación y la comprobación produce 0 hallazgos; caso negativo `test_flujo_sin_etiquetas_es_error`: un fixture con la profundidad completa y sin `fetch-tags` produce un error que nombra las etiquetas ausentes y no declara verificado el alcance; complementaria: el caso `test_alcance_sin_tag_usa_merge_base` de `tools/sdd/tests/test_validate.py` acota el alcance por el ancestro común con `main` sobre un historial sin tag anotado y no informa la ausencia de etiquetas como defecto del repositorio; la prueba se escribe en rojo antes de `T-006`; el detector `problemas_del_flujo` y el fixture `FLUJO_VALIDO` se amplían con los 2 parámetros.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` devuelve «Ran 8 tests in 0.005s» y «OK»; `test_preparacion_completa_del_arbol` declara `fetch-depth: 0` y `fetch-tags: true`, enumera 3 commits examinados sobre el historial sintético de 3 y produce 0 hallazgos sobre el flujo del repositorio; `test_flujo_sin_etiquetas_es_error` nombra «fetch-tags» y deja el alcance sin verificar con 0 commits; `TestAlcanceDeLaReferencia.test_alcance_sin_tag_usa_merge_base` de `tools/sdd/tests/test_validate.py` acota el alcance por el ancestro común con `main`, informa «ancestro» en la salida y no registra la ausencia de etiquetas como defecto del repositorio.
- [x] Completada.

### T-002: Pruebas del alcance del job con las 2 suites

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`, `tools/sdd/tests/fixtures/flujo/`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_job_ejecuta_las_dos_suites`: el job declara 3 pasos de ejecución con nombre, el de `tools\sdd\tests` y el de `tools\git\tests`, cada uno con `timeout-minutes: 1`, y la comprobación produce 0 hallazgos; caso negativo `test_flujo_con_una_suite_es_error`: un fixture con un solo paso de suite produce un error que nombra la suite de `tools/git/tests` ausente; la prueba se escribe en rojo antes de `T-007`; la exigencia de 2 pasos de ejecución de `problemas_del_flujo` pasa a 3 pasos con las 2 suites identificadas.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` devuelve «Ran 8 tests in 0.005s» y «OK»; `test_job_ejecuta_las_dos_suites` informa 3 pasos de ejecución con nombre y los de `tools\sdd\tests` y `tools\git\tests` con `timeout-minutes: 1` cada uno; `test_flujo_con_una_suite_es_error` nombra «tools/git/tests» como suite ausente sobre un flujo con 2 pasos de ejecución y no declara el check conforme; `problemas_del_flujo` exige 3 pasos de ejecución y las 2 suites identificadas.
- [x] Completada.

### T-003: Pruebas de la matriz reducida del orquestador

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_escritura_unica_del_orquestador`: la matriz real declara 1 sola ruta con `edit` y efecto `allow`, que es `.opencode/**`, declara `deny` explícito sobre `.github/**`, `opencode.jsonc` y `MEMORY.md`, y devuelve 0 atribuciones de escritura fuera de `.opencode/**`; caso negativo `test_concesion_fuera_de_opencode_es_error`: un rol sintético con `edit .github/**` y efecto `allow` produce fallo con la ruta concedida, y la escritura intentada fuera de `.opencode/**` se resuelve como `deny` con el rol concesionario declarado en este archivo; la prueba se escribe en rojo antes de `T-008`; la tupla de rutas concedidas del orquestador en la constante de la matriz de pruebas se reduce a `.opencode/**`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` devuelve «Ran 17 tests in 0.024s» y «OK»; `test_escritura_unica_del_orquestador` declara 1 ruta con `edit` y efecto `allow` —`.opencode/**`—, las 3 rutas denegadas de forma explícita `.github/**`, `opencode.jsonc` y `MEMORY.md`, y 0 atribuciones de escritura fuera de `.opencode/**`; `test_concesion_fuera_de_opencode_es_error` informa «.github/**» como ruta concedida por el rol sintético y resuelve `.github/workflows/sdd.yml`, `opencode.jsonc` y `MEMORY.md` como `deny` sobre la matriz real, con el rol `coder` que este archivo declara como escritor de la primera.
- [x] Completada.

### T-004: Pruebas de la nota de cierre append-only

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-004`, `CB-005`, `CB-006`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_nota_de_cierre_append_only`: la nota figura a continuación de las secciones precedentes del reporte de `SPEC-013` y transcribe el veredicto `CONFORME CON OBSERVACIONES`, el cierre de las 16 observaciones con 15 artefactos y 1 exención declarada, la causa del veredicto con 7 observaciones y el estado de las 4 observaciones de esta spec, mientras la matriz de 40 filas y el dictamen `CONVERGIDO` conservan su contenido; caso negativo `test_nota_con_recuento_divergente_es_error`: una nota sintética que transcribe 15 observaciones cerradas produce un error que nombra el valor en conflicto; complementaria con 2 notas consecutivas: la segunda se añade sin eliminar la primera; la prueba se escribe en rojo antes de `T-010`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestNotaDeCierre -q` devuelve «Ran 2 tests in 0.006s» y «OK»; `test_nota_de_cierre_append_only` conserva las 40 filas en `PASADO` y el dictamen `CONVERGIDO` del reporte real, acepta la nota con el veredicto `CONFORME CON OBSERVACIONES` y su equivalencia a `PARCIAL`, el cierre de las 16 observaciones con 15 artefactos y 1 exención y las 4 observaciones con su artefacto, y conserva la nota precedente al añadir la segunda; `test_nota_con_recuento_divergente_es_error` informa «15 observaciones previas» frente a «16» del informe final.
- [x] Completada.

### T-005: Pruebas del cierre de las 4 observaciones

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-005`, `CB-007`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 20 min.
- **Validación:** caso positivo `test_cierre_de_las_cuatro_observaciones`: las 4 observaciones `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` cuentan con artefacto de cierre y evidencia transcrita y el recuento declarado es 4 de 4; caso negativo `test_observacion_sin_artefacto_sigue_vigente`: una observación sin artefacto de cierre se registra en estado vigente con su causa y el detector no la cuenta como cerrada; la prueba se escribe en rojo antes de `T-011`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q` devuelve «Ran 41 tests in 0.061s» y «OK»; `TestCierreDeObservaciones.test_cierre_de_las_cuatro_observaciones` declara las 4 observaciones `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` con artefacto y evidencia transcrita y el recuento «Cerradas: 4 de 4»; `test_observacion_sin_artefacto_sigue_vigente` informa «AUD-075 sigue vigente: sin artefacto de cierre declarado» y deja el recuento verificado en 3 de 4.
- [x] Completada.

### T-006: Preparación completa del árbol en el flujo `SDD`

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `.github/workflows/sdd.yml`.
- **Estimación:** 20 min.
- **Validación:** `actions/checkout@v4` conserva su posición como primera preparación del job `verify` y declara `with: fetch-depth: 0` y `fetch-tags: true`; se conservan el disparador `pull_request` sobre `dev` y `main`, `contents: read`, `runs-on: windows-latest`, `python-version: '3.12'` y 0 efectos remotos; las pruebas de `T-001` quedan en verde; `python tools\sdd\validate.py --all` devuelve código 0.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` devuelve «Ran 8 tests in 0.005s» y «OK»; `git diff --numstat` del flujo declara 6 líneas añadidas y 0 retiradas, con `actions/checkout@v4` como primera preparación del job `verify` y los parámetros `fetch-depth: 0` y `fetch-tags: true`; `python tools\sdd\validate.py --all` devuelve código 0 y abre con «Comprobación de historial: punto de corte el tag anotado v0.6.0, 58 commits examinados».
- [x] Completada.

### T-007: Paso nombrado de la suite de `tools/git/tests`

- **Dependencias:** `T-006`, `T-002`.
- **Requisitos cubiertos:** `RF-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `.github/workflows/sdd.yml`.
- **Estimación:** 20 min.
- **Validación:** el job `verify` declara 3 pasos de ejecución con nombre —la validación agregada, la suite de `tools\sdd\tests` y la suite de `tools\git\tests`—, la segunda conserva `timeout-minutes: 1` y la tercera declara `timeout-minutes: 1` con el comando `python -m unittest discover -s tools\git\tests -q`; el job conserva `timeout-minutes: 5` y 0 efectos remotos; las pruebas de `T-002` quedan en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` devuelve «Ran 8 tests in 0.005s» y «OK»; `python -m unittest discover -s tools\git\tests -q` devuelve «Ran 48 tests in 21.215s» y «OK»; `git diff --numstat` del flujo declara 6 líneas añadidas y 0 retiradas con el paso nombrado de `tools\git\tests`, su `timeout-minutes: 1` y el límite total de 5 minutos del job.
- [x] Completada.

### T-008: Matriz del orquestador limitada a `.opencode/**`

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 20 min.
- **Validación:** la matriz conserva 1 sola entrada `edit` con efecto `allow`, que corresponde a `.opencode/**`; retira las entradas `edit` con efecto `allow` sobre `.github/**`, `opencode.jsonc` y `MEMORY.md` y declara esas 3 rutas con efecto `deny`; el número de atribuciones de escritura fuera de `.opencode/**` es 0; el cuerpo del rol conserva la prohibición de escribir la sección de aprobaciones y de declarar compuertas; `opencode.jsonc` no declara entrada de rol del orquestador; las pruebas de `T-003` quedan en verde. La tarea la ejecuta el propietario y el agente solo prepara el diff previsto, sin firmar, sin confirmar y sin marcar su casilla.
- **Evidencia:** `.opencode/agents/sdd.md` conserva `.opencode/**` como única concesión de escritura y deniega `.github/**`, `opencode.jsonc` y `MEMORY.md`; `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` devuelve 17 pruebas `OK`, con `test_escritura_unica_del_orquestador` y `test_concesion_fuera_de_opencode_es_error` en verde. Ejecutada por la sesión orquestadora, único rol con `.opencode/**`, porque al planificar ninguna otra ruta tenía la concesión.
- [x] Completada.

### T-009: Preparación completa y 2 suites en la norma de integración

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** la declaración de la suite en la línea 232 y la del check exigible en la línea 462 nombran las 2 suites —`tools/sdd/tests` y `tools/git/tests`— y su ejecución en el job `verify`; la declaración de la preparación nombra `fetch-depth: 0` y `fetch-tags: true` y el alcance de la comprobación de la referencia; el número de afirmaciones que describen el check con una sola suite es 0; las pruebas de `T-002` quedan en verde.
- **Evidencia:** `docs/Flujo_de_Trabajo_Git.md` declara las dos suites con 167 y 48 pruebas y el check exigible con `fetch-depth: 0` y `fetch-tags: true`; `git diff --numstat` devuelve 2 líneas añadidas y 2 retiradas en ese archivo.
- [x] Completada.

### T-010: Nota de cierre append-only en el reporte de `SPEC-013`

- **Dependencias:** `T-004`, `T-009`.
- **Requisitos cubiertos:** `RF-004`, `CB-005`, `CB-006`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** la nota se añade a continuación de las secciones precedentes del reporte y transcribe el veredicto `CONFORME CON OBSERVACIONES` con su equivalencia a `PARCIAL`, el cierre de las 16 observaciones previas con 15 artefactos y 1 exención declarada, la causa del veredicto con las 7 observaciones nuevas y el estado de `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` con su artefacto de cierre; la matriz de 40 filas conserva el valor `PASADO`, el dictamen conserva `CONVERGIDO` y el estado conserva `validated`; las pruebas de `T-004` quedan en verde; la escritura la realiza el `reviewer` por delegación escrita del propietario.
- **Evidencia:** `specs/013-cierre-reauditoria-conformidad/validation_report.md` incorpora `## Nota de cierre de la reauditoría final` con 20 líneas añadidas y 0 retiradas; `TestNotaDeCierre` devuelve 2 pruebas `OK` y las 40 filas de la matriz conservan `PASADO` con el dictamen `CONVERGIDO`.
- [x] Completada.

### T-011: Paquete de cierre de las 4 observaciones

- **Dependencias:** `T-005`, `T-010`.
- **Requisitos cubiertos:** `RF-005`, `CB-007`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `specs/014-cierre-observaciones-finales/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** este artefacto declara una tabla de 4 filas con la observación, el artefacto que la cierra, la evidencia de su verificación y el requisito que la cubre, y el recuento declarado es 4 de 4 cerradas; una observación que no cuente con artefacto de cierre se registra en estado vigente con su causa y no se declara cerrada; las pruebas de `T-005` quedan en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q` devuelve «Ran 41 tests in 0.061s» y «OK»; la sección «Paquete de cierre de las cuatro observaciones» declara 4 filas con observación, artefacto de cierre, evidencia y requisito, y el recuento «Cerradas: 4 de 4»; `problemas_del_cierre` devuelve 0 hallazgos sobre este artefacto y el recuento de observaciones sin artefacto declaradas cerradas es 0. La incorporación de la nota de `AUD-075` en el reporte de `SPEC-013` corresponde a `T-010` y la declaración documental de `AUD-102` a `T-009`; ambas filas transcriben la verificación que ya ejercen `TestNotaDeCierre` y `TestFlujoDeIntegracionContinua`.
- [x] Completada.

### T-012: Regresión agregada y límites de tiempo

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RNF-001`, `RNF-002`, `RNF-003`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/014-cierre-observaciones-finales/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q` devuelven código 0; `python tools\sdd\validate.py --all` devuelve código 0 en 300 segundos o menos, con tiempo medido y transcrito; el job conserva `timeout-minutes: 5` y cada paso de suite conserva `timeout-minutes: 1`; el recuento de las 6 comprobaciones nuevas con pareja positiva y negativa es 6 y el de comprobaciones sin pareja es 0.
- **Evidencia:** `python -m unittest discover -s tools\sdd\tests -q` devuelve 167 pruebas `OK`, `python -m unittest discover -s tools\git\tests -q` devuelve 48 pruebas `OK`, `python tools\sdd\validate.py --all` devuelve código 0 en 2,63 s, por debajo de los 300 s, y el job conserva límite de 5 minutos con pasos de 1 minuto.
- [x] Completada.

### T-013: Cierre del alcance y traspaso a la validación

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RNF-004`, `RNF-005`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `specs/014-cierre-observaciones-finales/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** las trece tareas figuran cerradas con su evidencia transcrita; `python tools\sdd\validate.py --spec SPEC-014 --gate G3` devuelve código 0; el contraste del reporte de `SPEC-013` con su versión anterior declara el 100 % de sus requisitos, criterios de aceptación, estado, filas de matriz y dictamen sin cambios; el número de contradicciones entre la matriz del orquestador y §12 del protocolo sobre las rutas de escritura es 0; el paquete de traspaso no declara compuerta alguna y la verificación de G2, G3 y G5 corresponde al orquestador.
- **Evidencia:** el paquete de cierre reúne las cuatro observaciones con su artefacto y evidencia, las seis comprobaciones con pareja positiva y negativa, 167 pruebas en verde y `--all` con código 0; la compuerta G3 la verifica la sesión orquestadora.
- [x] Completada.

## Paquete de cierre de las cuatro observaciones

Cerradas: 4 de 4.

| Observación | Artefacto de cierre | Evidencia de la verificación | Requisito |
|---|---|---|---|
| `AUD-066` | `.opencode/agents/sdd.md` con `.opencode/**` como única concesión de escritura y efecto `deny` explícito sobre `.github/**`, `opencode.jsonc` y `MEMORY.md` | `TestMatrizDePermisos.test_escritura_unica_del_orquestador` en verde: 1 ruta con efecto `allow`, 3 rutas denegadas de forma explícita y 0 atribuciones de escritura fuera de `.opencode/**`; `tasks.md` atribuye `.github/workflows/sdd.yml` al rol `coder` | `RF-003` |
| `AUD-075` | `specs/013-cierre-reauditoria-conformidad/validation_report.md` con la nota de cierre append-only de `SPEC-014` | `TestNotaDeCierre.test_nota_de_cierre_append_only` en verde: el reporte conserva las 40 filas en `PASADO` y el dictamen `CONVERGIDO`, y la nota canónica se acepta a continuación de las secciones precedentes; la incorporación de la nota en el reporte corresponde a `T-010` | `RF-004` |
| `AUD-101` | `.github/workflows/sdd.yml` con `fetch-depth: 0` y `fetch-tags: true` en la primera preparación del job `verify` | `TestFlujoDeIntegracionContinua.test_preparacion_completa_del_arbol` y `test_alcance_de_la_referencia_examina_commit` en verde: el alcance enumera 3 commits sobre el historial sintético de 3 y el flujo produce 0 hallazgos | `RF-001` |
| `AUD-102` | `.github/workflows/sdd.yml` con el paso nombrado de `tools/git/tests` y su límite de 1 minuto | `TestFlujoDeIntegracionContinua.test_job_ejecuta_las_dos_suites` en verde y `python -m unittest discover -s tools\git\tests -q` con 48 pruebas y «OK»; la declaración en `docs/Flujo_de_Trabajo_Git.md` corresponde a `T-009` | `RF-002` |

Recuento verificado: `observaciones_cerradas` devuelve 4 y `problemas_del_cierre` devuelve 0 hallazgos sobre este artefacto. Una observación sin artefacto de cierre se registra en estado vigente con su causa y no se declara cerrada, como ejerce `test_observacion_sin_artefacto_sigue_vigente`; el recuento de observaciones sin artefacto declaradas cerradas es 0. Las observaciones `AUD-038`, `AUD-067` y `AUD-098` quedaron cerradas en el Pull Request #13 y no forman parte de este paquete.

## Matriz de cobertura de tareas

| Requisito | Tareas |
|---|---|
| `RF-001` | `T-001`, `T-006`, `T-009` |
| `RF-002` | `T-002`, `T-007`, `T-009` |
| `RF-003` | `T-003`, `T-008` |
| `RF-004` | `T-004`, `T-010` |
| `RF-005` | `T-005`, `T-011` |
| `RNF-001` | `T-012` |
| `RNF-002` | `T-012` |
| `RNF-003` | `T-012` |
| `RNF-004` | `T-013` |
| `RNF-005` | `T-013` |
| `CB-001` | `T-001`, `T-006` |
| `CB-002` | `T-001`, `T-006` |
| `CB-003` | `T-002`, `T-007` |
| `CB-004` | `T-003`, `T-008` |
| `CB-005` | `T-004`, `T-010` |
| `CB-006` | `T-004`, `T-010` |
| `CB-007` | `T-005`, `T-011` |

## Trazabilidad de los criterios de aceptación

| Criterio | Tareas que lo declaran |
|---|---|
| `CA-001` | `T-001`, `T-006` |
| `CA-002` | `T-002`, `T-007`, `T-009` |
| `CA-003` | `T-003`, `T-008` |
| `CA-004` | `T-004`, `T-010` |
| `CA-005` | `T-005`, `T-011` |
| `CA-006` | `T-012` |
| `CA-007` | `T-013` |
