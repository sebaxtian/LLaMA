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

- Cerradas: 0 de 13 tareas.

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
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` con el recuento de pruebas y «OK»; el caso positivo declara `fetch-depth: 0` y `fetch-tags: true` y al menos 1 commit examinado; el negativo nombra `fetch-tags` ausente y la complementaria informa el ancestro común con `main`.
- [ ] Completada.

### T-002: Pruebas del alcance del job con las 2 suites

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`, `tools/sdd/tests/fixtures/flujo/`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_job_ejecuta_las_dos_suites`: el job declara 3 pasos de ejecución con nombre, el de `tools\sdd\tests` y el de `tools\git\tests`, cada uno con `timeout-minutes: 1`, y la comprobación produce 0 hallazgos; caso negativo `test_flujo_con_una_suite_es_error`: un fixture con un solo paso de suite produce un error que nombra la suite de `tools/git/tests` ausente; la prueba se escribe en rojo antes de `T-007`; la exigencia de 2 pasos de ejecución de `problemas_del_flujo` pasa a 3 pasos con las 2 suites identificadas.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` con el recuento de pruebas y «OK»; el caso positivo informa las 2 suites como pasos nombrados con su límite de 1 minuto; el negativo nombra la suite ausente y no declara el check conforme.
- [ ] Completada.

### T-003: Pruebas de la matriz reducida del orquestador

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_escritura_unica_del_orquestador`: la matriz real declara 1 sola ruta con `edit` y efecto `allow`, que es `.opencode/**`, declara `deny` explícito sobre `.github/**`, `opencode.jsonc` y `MEMORY.md`, y devuelve 0 atribuciones de escritura fuera de `.opencode/**`; caso negativo `test_concesion_fuera_de_opencode_es_error`: un rol sintético con `edit .github/**` y efecto `allow` produce fallo con la ruta concedida, y la escritura intentada fuera de `.opencode/**` se resuelve como `deny` con el rol concesionario declarado en este archivo; la prueba se escribe en rojo antes de `T-008`; la tupla de rutas concedidas del orquestador en la constante de la matriz de pruebas se reduce a `.opencode/**`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` con el recuento de pruebas y «OK»; el caso positivo declara 1 ruta con efecto `allow` y 3 rutas denegadas; el negativo informa la ruta concedida y la resolución `deny` con el rol concesionario.
- [ ] Completada.

### T-004: Pruebas de la nota de cierre append-only

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-004`, `CB-005`, `CB-006`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_nota_de_cierre_append_only`: la nota figura a continuación de las secciones precedentes del reporte de `SPEC-013` y transcribe el veredicto `CONFORME CON OBSERVACIONES`, el cierre de las 16 observaciones con 15 artefactos y 1 exención declarada, la causa del veredicto con 7 observaciones y el estado de las 4 observaciones de esta spec, mientras la matriz de 40 filas y el dictamen `CONVERGIDO` conservan su contenido; caso negativo `test_nota_con_recuento_divergente_es_error`: una nota sintética que transcribe 15 observaciones cerradas produce un error que nombra el valor en conflicto; complementaria con 2 notas consecutivas: la segunda se añade sin eliminar la primera; la prueba se escribe en rojo antes de `T-010`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q` con el recuento de pruebas y «OK»; el caso positivo conserva las 40 filas y el dictamen y declara las 4 observaciones con su artefacto; el negativo informa el recuento transcrito y el del informe final; la complementaria conserva la nota precedente.
- [ ] Completada.

### T-005: Pruebas del cierre de las 4 observaciones

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-005`, `CB-007`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 20 min.
- **Validación:** caso positivo `test_cierre_de_las_cuatro_observaciones`: las 4 observaciones `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` cuentan con artefacto de cierre y evidencia transcrita y el recuento declarado es 4 de 4; caso negativo `test_observacion_sin_artefacto_sigue_vigente`: una observación sin artefacto de cierre se registra en estado vigente con su causa y el detector no la cuenta como cerrada; la prueba se escribe en rojo antes de `T-011`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q` con el recuento de pruebas y «OK»; el caso positivo declara 4 de 4 con artefacto por observación; el negativo informa el identificador de la observación vigente y su causa.
- [ ] Completada.

### T-006: Preparación completa del árbol en el flujo `SDD`

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `.github/workflows/sdd.yml`.
- **Estimación:** 20 min.
- **Validación:** `actions/checkout@v4` conserva su posición como primera preparación del job `verify` y declara `with: fetch-depth: 0` y `fetch-tags: true`; se conservan el disparador `pull_request` sobre `dev` y `main`, `contents: read`, `runs-on: windows-latest`, `python-version: '3.12'` y 0 efectos remotos; las pruebas de `T-001` quedan en verde; `python tools\sdd\validate.py --all` devuelve código 0.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` con «OK»; `git diff --numstat` del flujo declara las líneas añadidas de los 2 parámetros; la ejecución de `--all` informa el punto de corte con al menos 1 commit examinado y devuelve código 0.
- [ ] Completada.

### T-007: Paso nombrado de la suite de `tools/git/tests`

- **Dependencias:** `T-006`, `T-002`.
- **Requisitos cubiertos:** `RF-002`, `CB-003`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `.github/workflows/sdd.yml`.
- **Estimación:** 20 min.
- **Validación:** el job `verify` declara 3 pasos de ejecución con nombre —la validación agregada, la suite de `tools\sdd\tests` y la suite de `tools\git\tests`—, la segunda conserva `timeout-minutes: 1` y la tercera declara `timeout-minutes: 1` con el comando `python -m unittest discover -s tools\git\tests -q`; el job conserva `timeout-minutes: 5` y 0 efectos remotos; las pruebas de `T-002` quedan en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q` con «OK»; `python -m unittest discover -s tools\git\tests -q` devuelve el recuento de 48 pruebas y «OK»; `git diff --numstat` del flujo declara las líneas añadidas del paso nuevo.
- [ ] Completada.

### T-008: Matriz del orquestador limitada a `.opencode/**`

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 20 min.
- **Validación:** la matriz conserva 1 sola entrada `edit` con efecto `allow`, que corresponde a `.opencode/**`; retira las entradas `edit` con efecto `allow` sobre `.github/**`, `opencode.jsonc` y `MEMORY.md` y declara esas 3 rutas con efecto `deny`; el número de atribuciones de escritura fuera de `.opencode/**` es 0; el cuerpo del rol conserva la prohibición de escribir la sección de aprobaciones y de declarar compuertas; `opencode.jsonc` no declara entrada de rol del orquestador; las pruebas de `T-003` quedan en verde. La tarea la ejecuta el propietario y el agente solo prepara el diff previsto, sin firmar, sin confirmar y sin marcar su casilla.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` con «OK»; `git show --numstat` del commit del propietario declara las líneas retiradas de las 3 concesiones y las líneas añadidas de las 3 denegaciones; el contraste con la tabla de §12 del protocolo declara 0 contradicciones.
- [ ] Completada.

### T-009: Preparación completa y 2 suites en la norma de integración

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** la declaración de la suite en la línea 232 y la del check exigible en la línea 462 nombran las 2 suites —`tools/sdd/tests` y `tools/git/tests`— y su ejecución en el job `verify`; la declaración de la preparación nombra `fetch-depth: 0` y `fetch-tags: true` y el alcance de la comprobación de la referencia; el número de afirmaciones que describen el check con una sola suite es 0; las pruebas de `T-002` quedan en verde.
- **Evidencia:** `git diff --numstat` de la norma declara las líneas añadidas y las retiradas; la búsqueda de las 2 rutas de suite en las líneas 232 y 462 devuelve las coincidencias esperadas; el recuento de afirmaciones con una sola suite es 0.
- [ ] Completada.

### T-010: Nota de cierre append-only en el reporte de `SPEC-013`

- **Dependencias:** `T-004`, `T-009`.
- **Requisitos cubiertos:** `RF-004`, `CB-005`, `CB-006`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** la nota se añade a continuación de las secciones precedentes del reporte y transcribe el veredicto `CONFORME CON OBSERVACIONES` con su equivalencia a `PARCIAL`, el cierre de las 16 observaciones previas con 15 artefactos y 1 exención declarada, la causa del veredicto con las 7 observaciones nuevas y el estado de `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` con su artefacto de cierre; la matriz de 40 filas conserva el valor `PASADO`, el dictamen conserva `CONVERGIDO` y el estado conserva `validated`; las pruebas de `T-004` quedan en verde; la escritura la realiza el `reviewer` por delegación escrita del propietario.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q` con «OK»; `git diff --numstat` del reporte declara solo líneas añadidas y 0 líneas retiradas; el recuento de filas de la matriz es 40 con valor `PASADO` y el dictamen conserva `CONVERGIDO`.
- [ ] Completada.

### T-011: Paquete de cierre de las 4 observaciones

- **Dependencias:** `T-005`, `T-010`.
- **Requisitos cubiertos:** `RF-005`, `CB-007`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `specs/014-cierre-observaciones-finales/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** este artefacto declara una tabla de 4 filas con la observación, el artefacto que la cierra, la evidencia de su verificación y el requisito que la cubre, y el recuento declarado es 4 de 4 cerradas; una observación que no cuente con artefacto de cierre se registra en estado vigente con su causa y no se declara cerrada; las pruebas de `T-005` quedan en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q` con «OK»; la tabla de cierre declara 4 filas con artefacto y evidencia y el recuento es 4 de 4; el recuento de observaciones sin artefacto declaradas cerradas es 0.
- [ ] Completada.

### T-012: Regresión agregada y límites de tiempo

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RNF-001`, `RNF-002`, `RNF-003`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/014-cierre-observaciones-finales/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q` devuelven código 0; `python tools\sdd\validate.py --all` devuelve código 0 en 300 segundos o menos, con tiempo medido y transcrito; el job conserva `timeout-minutes: 5` y cada paso de suite conserva `timeout-minutes: 1`; el recuento de las 6 comprobaciones nuevas con pareja positiva y negativa es 6 y el de comprobaciones sin pareja es 0.
- **Evidencia:** salida de las 2 suites con su recuento y «OK»; ejecución de `--all` con el tiempo medido y código 0; lectura de los 3 límites de tiempo; recuento de 6 comprobaciones con pareja y 0 sin pareja.
- [ ] Completada.

### T-013: Cierre del alcance y traspaso a la validación

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RNF-004`, `RNF-005`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `specs/014-cierre-observaciones-finales/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** las trece tareas figuran cerradas con su evidencia transcrita; `python tools\sdd\validate.py --spec SPEC-014 --gate G3` devuelve código 0; el contraste del reporte de `SPEC-013` con su versión anterior declara el 100 % de sus requisitos, criterios de aceptación, estado, filas de matriz y dictamen sin cambios; el número de contradicciones entre la matriz del orquestador y §12 del protocolo sobre las rutas de escritura es 0; el paquete de traspaso no declara compuerta alguna y la verificación de G2, G3 y G5 corresponde al orquestador.
- **Evidencia:** salida de `--spec SPEC-014 --gate G3` con código 0; `git diff --numstat` del reporte de `SPEC-013` con solo líneas añadidas; recuento de requisitos, criterios y filas alterados en `SPEC-013` igual a 0; recuento de contradicciones de la matriz igual a 0.
- [ ] Completada.

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
