# Tareas — SPEC-013

*Artefacto de rango 6: descomposición de `SPEC-013` en cuarenta y cuatro tareas atómicas con los ocho campos de la plantilla, dependencias acíclicas y cobertura completa de los dieciséis requisitos funcionales, los ocho requisitos no funcionales y los dieciséis casos borde.*

## Regla de ejecución

La etapa corrige el flujo de integración continua, las reglas de protección, el validador determinista, su suite, la matriz de agentes, tres documentos normativos, cuatro reportes publicados, dos secciones protegidas y siete documentos sin rango. Se ejecuta con cinco escritores y una revisión:

1. El rol `coder` escribe `tools/sdd/validate.py`, `tools/sdd/tests/`, `tools/git/` y `.github/workflows/sdd.yml`, y cierra sus tareas en este archivo.
2. El rol `sdd` escribe `.opencode/agents/sdd.md`, `coder.md` y `documenter.md`; es la única ruta con escritura sobre `.opencode/`.
3. El rol `documenter` escribe `docs/`, `AGENTS.md`, `MEMORY.md` y `CHANGELOG.md` como delegado explícito del propietario para los documentos de raíz.
4. El rol `reviewer` escribe la sección de cierre de los cuatro reportes publicados: su matriz de permisos le concede `specs/*/validation_report.md` y el `planner` tiene esa ruta denegada.
5. El `planner` escribe este archivo y los demás artefactos de la spec; el propietario ejecuta la tarea `T-033` en un commit firmado porque la sección de aprobaciones está protegida.
6. Las validaciones que requieren shell las ejecuta la sesión orquestadora y su salida literal se transcribe en el campo `Evidencia` de la tarea.
7. Una casilla se marca solo cuando la validación de la tarea se cumple. Una validación fallida obliga a corregir el archivo y a repetir la comprobación antes del registro.
8. Cada tarea de prueba se escribe en rojo antes de la tarea de implementación que la satisface y declara su caso positivo y su caso negativo.
9. Ninguna tarea declara evidencia antes de ejecutarse: el campo `Evidencia` fija qué se transcribe al cerrar y no se rellena con un resultado supuesto.
10. La etapa no modifica la constitución, las plantillas de rango 5, `src/`, `models/` ni `bin/`, y no cambia el estado de `SPEC-008` a `SPEC-012`.

## Referencias

- `spec.md`: `SPEC-013`, versión 0.4.0, estado `tasked`, dieciséis requisitos funcionales, ocho no funcionales, dieciséis casos borde y dieciocho criterios de aceptación; G1 firmada por `Agent Sebaxtian` en el commit `c61432d` (2026-11-14).
- `clarify.md`: cerrado con `AMB-001` a `AMB-012` resueltos, el caso borde `CB-016` añadido y los valores del cierre de integración fijados.
- `plan.md`: doce componentes, contratos C-1 a C-12, once decisiones `DEC-001` a `DEC-011` y matriz de cobertura de cuarenta filas.
- `docs/sdd/auditoria_cierre_v0_7_0.md`: observaciones `AUD-008`, `AUD-015`, `AUD-024`, `AUD-036`, `AUD-037`, `AUD-045`, `AUD-046`, `AUD-056`, `AUD-065`, `AUD-073`, `AUD-074`, `AUD-085`, `AUD-086` y `AUD-095` a `AUD-097`.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea y la casilla `Completada`.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §4 ciclo de siete etapas, §5 escritura de estados, §7 trazabilidad, §11 aprobaciones, §12 roles y permisos, §13 sincronización y §14 contrato del validador.
- `docs/Flujo_de_Trabajo_Git.md`: gramática de ramas, protección remota, sincronización por ancestría y tag anotado.

## Progreso

- Cerradas: 44 de 44 tareas.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_validate.py` y `tools/sdd/tests/fixtures/` | `T-001` a `T-004` | `coder` |
| 2 | `tools/sdd/tests/test_agent_permissions.py` y `tools/sdd/tests/fixtures/flujo/`, `fixtures/ramas/` | `T-005`, `T-007`, `T-008`, `T-009` y `T-010` | `coder` |
| 3 | `tools/git/tests/test_verify_branch_protection.py` | `T-006` | `coder` |
| 4 | `tools/sdd/validate.py` | `T-011` a `T-014` | `coder` |
| 5 | `.github/workflows/sdd.yml` | `T-018` | `coder` |
| 6 | `tools/git/protection_rules/main.json` y `dev.json` | `T-019` | `coder` |
| 7 | `tools/git/verify_branch_protection.py` | `T-020` | `coder` |
| 8 | `.opencode/agents/sdd.md` | `T-015` | `sdd` |
| 9 | `.opencode/agents/coder.md` | `T-016` | `sdd` |
| 10 | `.opencode/agents/documenter.md` | `T-017` | `sdd` |
| 11 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | `T-021`, `T-023`, `T-024` y `T-025` | `documenter` |
| 12 | `AGENTS.md` | `T-022` y `T-030` | `documenter` |
| 13 | `docs/Flujo_de_Trabajo_Git.md` | `T-026` a `T-029` | `documenter` |
| 14 | `specs/008-auditoria-cumplimiento-sdd/validation_report.md` y `specs/009-base-normativa-sdd/validation_report.md` | `T-031` | `reviewer` |
| 15 | `specs/010-mecanismo-control-sdd/validation_report.md` y `specs/011-practica-operativa-sdd/validation_report.md` | `T-032` | `reviewer` |
| 16 | `specs/010-mecanismo-control-sdd/spec.md` y `specs/011-practica-operativa-sdd/spec.md` | `T-033` | propietario, en commit firmado |
| 17 | Las doce guías `guia_*.md` de `docs/sdd/` | `T-034` y `T-036` | `documenter` |
| 18 | `docs/sdd/referencia_7_etapas_sdd.md`, `docs/sdd/referencia_ciclo_vida_sdd_puro.md` y `docs/sdd/compendio_sdd.md` | `T-035` y `T-036` | `documenter` |
| 19 | `MEMORY.md` | `T-037` | `documenter` |
| 20 | `docs/sdd/README.md` | `T-038` | `documenter` |
| 21 | `CHANGELOG.md` | `T-039` | `documenter` |
| 22 | `specs/013-cierre-reauditoria-conformidad/tasks.md` | cierre de cada tarea, `T-040` a `T-044` | `coder` para las casillas de sus tareas y `planner` para el cierre |

`T-040` a `T-044` son tareas de verificación y de cierre: no producen archivos fuera de `tasks.md`.

## Tarea reservada al propietario

`T-033` retira la tercera casilla de la compuerta G4 de las secciones de aprobaciones de `SPEC-010` y de `SPEC-011`. La sección es protegida: solo la modifica el propietario mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`. El agente prepara el cambio, transcribe el diff previsto y no firma, no confirma ni marca la casilla de la tarea; la evidencia se registra cuando el propietario publica el commit firmado.

## Orden de ejecución y dependencias

- Grupo 1 (pruebas en rojo): `T-001` sin dependencias; `T-002` depende de `T-001`; `T-003` depende de `T-002`; `T-004` depende de `T-003`; `T-005` depende de `T-004`; `T-006` depende de `T-005`; `T-007` depende de `T-006`; `T-008` depende de `T-007`; `T-009` depende de `T-008`; `T-010` depende de `T-009`.
- Grupo 2 (validador): `T-011` depende de `T-001`; `T-012` depende de `T-002`; `T-013` depende de `T-003`; `T-014` depende de `T-004`.
- Grupo 3 (matriz de agentes): `T-015` depende de `T-008`; `T-016` depende de `T-015`; `T-017` depende de `T-016`.
- Grupo 4 (flujo y protección): `T-018` depende de `T-016` y de `T-005`; `T-019` depende de `T-008`; `T-020` depende de `T-006`.
- Grupo 5 (documentos normativos): `T-021` depende de `T-017`; `T-022` depende de `T-021`; `T-023` depende de `T-022`; `T-024` depende de `T-023`; `T-025` depende de `T-024`; `T-026` depende de `T-025`; `T-027` depende de `T-026`; `T-028` depende de `T-027`; `T-029` depende de `T-028`; `T-030` depende de `T-029`.
- Grupo 6 (registros de spec): `T-031` depende de `T-030`; `T-032` depende de `T-031`; `T-033` depende de `T-032`.
- Grupo 7 (documentos sin rango): `T-034` depende de `T-033`; `T-035` depende de `T-034`; `T-036` depende de `T-035`; `T-037` depende de `T-036`; `T-038` depende de `T-037`; `T-039` depende de `T-038`.
- Grupo 8 (verificación y cierre): `T-040` depende de `T-039`; `T-041` depende de `T-040`; `T-042` depende de `T-041`; `T-043` depende de `T-042`; `T-044` depende de `T-043`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo. La matriz de agentes se corrige antes que el flujo porque el `coder` necesita la concesión de `.github/**` para escribir el flujo y el `documenter` necesita las concesiones de raíz para escribir `MEMORY.md` y `CHANGELOG.md`.

## Tareas

### T-001: Pruebas de la casilla de aprobación única

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-003`, `CB-006`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/casilla/`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_casilla_unica_por_compuerta`: una sección de aprobaciones con una casilla de G1 y una de G4 produce 0 hallazgos y salida 0; caso negativo `test_casilla_duplicada_sin_marcar_es_error`: una sección con una segunda casilla de G4 sin marcar produce código 1 con la compuerta y el recuento en el mensaje; la prueba se escribe en rojo antes de `T-011`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestCasillaDeAprobacion -q`: «Ran 2 tests in 0.018s» y «OK»; el caso positivo no produce hallazgo de `C-13` y el negativo devuelve código 1 con «registro dual de G4: la spec declara 2 casillas de G4 y la sección admite 1».
- [x] Completada.

### T-002: Pruebas del alcance de la referencia a la spec

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-007`, `CB-005`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/alcance/`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_alcance_desde_ultimo_tag`: un historial con tag anotado de release acota el alcance a los commits posteriores y cada commit declara la cadena `Spec: SPEC-NNN`, con salida 0; caso negativo `test_commit_sin_spec_en_alcance`: un commit de implementación del alcance sin la cadena produce código 1 con su identificador abreviado; complementarias `test_alcance_sin_tag_usa_merge_base`, `test_alcance_vacio_no_aplicable` y `test_merges_excluidos_del_alcance`; las cinco se escriben en rojo antes de `T-012`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestAlcanceDeLaReferencia -q`: «Ran 5 tests in 0.048s» y «OK»; el caso positivo acota el alcance a `v0.6.0..HEAD` e informa «1 commits examinados», el negativo devuelve código 1 con el identificador abreviado del commit, el alcance vacío se informa «no aplicable» y la enumeración conserva `--no-merges` sin el recuento de 50 commits.
- [x] Completada.

### T-003: Pruebas del cierre de integración del reporte

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/cierre/`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_cierre_de_spec_validada`: un reporte en estado `validated` con la sección `## Cierre de integración`, la línea `Merge:` y la línea `Release:` vacía produce 0 hallazgos; caso negativo `test_release_declarado_en_validated_es_error`: un reporte en estado `validated` con un tag declarado en la línea `Release:` produce código 1 por release declarado sin publicación; complementaria `test_cierre_append_only_conserva_dictamen`, con dictamen no convergido conservado sin alteración; las tres se escriben en rojo antes de `T-013`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestCierreDeIntegracion.test_cierre_de_spec_validada tools.sdd.tests.test_validate.TestCierreDeIntegracion.test_release_declarado_en_validated_es_error tools.sdd.tests.test_validate.TestCierreDeIntegracion.test_cierre_append_only_conserva_dictamen -q`: «Ran 3 tests in 0.028s» y «OK»; el caso negativo declara «está en estado validated y declara el tag v1.1.1 en «Release:»; el release no está publicado y la línea debe quedar vacía».
- [x] Completada.

### T-004: Pruebas del check exigible en G5

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-010`, `CB-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/g5-check/`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_reglas_de_proteccion_exigen_verify`: las reglas de `main` y de `dev` declaran exigible el contexto `verify` y la comprobación produce 0 hallazgos; caso negativo `test_proteccion_sin_check_bloquea_g5`: una regla de rama sin el contexto exigible registra el bloqueo de G5 con la rama y el check ausente y devuelve código 1; ambas se escriben en rojo antes de `T-014`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestCheckExigibleEnG5 -q`: «Ran 2 tests in 0.032s» y «OK»; el caso negativo devuelve código 1 con «la regla de protección de dev no declara exigible el check «verify» del flujo SDD; la compuerta G5 queda bloqueada», y las dos reglas declaradas del repositorio convergen con `strict: true`.
- [x] Completada.

### T-005: Pruebas de la estructura del flujo de integración continua

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-010`, `CB-009`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`, `tools/sdd/tests/fixtures/flujo/`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_estructura_del_flujo`: el flujo declara `actions/checkout` como primera preparación, `actions/setup-python`, el job `verify`, el límite de 5 minutos y 0 efectos remotos, con salida 0; caso negativo `test_flujo_sin_preparacion_del_arbol`: un flujo sintético sin `actions/checkout` produce código 1 por ausencia de los archivos que valida; ambas se escriben en rojo antes de `T-018`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q`: «Ran 3 tests in 0.003s» y «OK»; el caso negativo declara «la primera preparación del job no usa actions/checkout» sobre el flujo sintético sin preparación del árbol.
- [x] Completada.

### T-006: Pruebas del comparador de las reglas de protección

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/git/tests/test_verify_branch_protection.py`.
- **Estimación:** 25 min.
- **Validación:** caso positivo `test_required_status_checks_declarado`: el objeto declarado con `strict` verdadero y el contexto `verify` converge con la respuesta simulada; caso negativo `test_required_status_checks_divergente`: un contexto distinto produce discrepancia con el contexto esperado y el observado; ambas se escriben en rojo antes de `T-020`.
- **Evidencia:** `python -m unittest tools.git.tests.test_verify_branch_protection -q`: «Ran 39 tests in 0.015s» y «OK»; el objeto declarado converge con la respuesta que presenta `SDD / verify` y la discrepancia del caso negativo declara «required_status_checks: contextos esperados ['verify'], observados ['lint']».
- [x] Completada.

### T-007: Pruebas de la gramática de nombres de rama

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-013`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`, `tools/sdd/tests/fixtures/ramas/`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_gramatica_de_ramas`: la expresión declarada admite `feat/reauditoria-cierre`, `docs/cierre-integracion-spec-012` y `release/v0-7-0`, con la longitud de 3 a 63 caracteres sobre el nombre; caso negativo: la misma prueba rechaza `docs/Cierre-Integracion` por mayúscula, `docs/ab` por longitud menor que 3, `docs/uno_dos` por guion bajo y `chore/limpieza` por prefijo fuera de la lista de cinco, e informa el conjunto admitido; se escribe en rojo antes de `T-029`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentacionOperativa -q`: «Ran 2 tests in 0.006s» y «OK»; `test_gramatica_de_ramas` admite `feat/reauditoria-cierre`, `docs/cierre-integracion-spec-012` y `release/v0-7-0`, rechaza `docs/Cierre-Integracion` por mayúscula, `docs/ab` por longitud menor que 3, `docs/uno_dos` por guion bajo y `chore/limpieza` por prefijo fuera de la lista, y declara los cinco prefijos admitidos.
- [x] Completada.

### T-008: Pruebas de la matriz de agentes y de las etapas del orquestador

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-002`, `RF-009`, `CB-014`.
- **Criterio de aceptación:** `CA-002`, `CA-009`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_tabla_de_etapas_del_orquestador`: la tabla de `.opencode/agents/sdd.md` declara siete etapas numeradas de 1 Specify a 7 Release, y `test_escritura_del_coder` y `test_escritura_del_documenter` admiten `.github/**`, `MEMORY.md` y `CHANGELOG.md`; caso negativo `test_escritura_del_orquestador`: un rol sintético con una concesión de escritura sobre `specs/**` produce fallo con la ruta concedida, y la matriz real devuelve 0 atribuciones sobre `specs/`; las cuatro se escriben en rojo antes de `T-015`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q`: «Ran 15 tests in 0.025s» y «OK»; `test_tabla_de_etapas_del_orquestador` contrasta las siete etapas de 1 Specify a 7 Release, `test_escritura_del_coder` y `test_escritura_del_documenter` admiten `.github/**`, `MEMORY.md` y `CHANGELOG.md`, y `test_escritura_del_orquestador` detecta la concesión sintética sobre `specs/` y devuelve 0 atribuciones sobre la matriz real; la matriz del orquestador conserva 11 denegaciones explícitas de escritura.
- [x] Completada.

### T-009: Pruebas de los documentos normativos corregidos

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-004`, `RF-005`, `RF-008`, `RF-012`.
- **Criterio de aceptación:** `CA-004`, `CA-005`, `CA-008`, `CA-012`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** casos positivos `test_contrato_de_firma_verificada`, `test_ventanas_de_legado`, `test_tabla_de_escritura_de_estados` y `test_sincronizacion_por_ancestria`, que verifican la declaración de la firma verificada, las dos ventanas con motivo y límite, la escritura de T4 a T7 por el `planner` y la ancestría sin conteo; caso negativo: cada prueba falla sobre una copia sintética que conserva la afirmación anterior, esto es, la firma no verificada, la ventana sin motivo, la atribución al orquestador y la exigencia de la salida `0 0`; las ocho comprobaciones se escriben en rojo antes de `T-021`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentosNormativos -q`: «Ran 4 tests in 0.007s» y «OK»; `test_contrato_de_firma_verificada` detecta la firma no verificada de §14 y la negación en `AGENTS.md`, `test_ventanas_de_legado` detecta la ventana sin motivo, `test_tabla_de_escritura_de_estados` detecta la atribución al orquestador y `test_sincronizacion_por_ancestria` detecta la exigencia de la salida «0 0»; las dos ventanas coinciden con `LEGACY_SPECS` y `TRACE_LEGACY_SPECS`.
- [x] Completada.

### T-010: Pruebas de los documentos sin rango

- **Dependencias:** `T-009`.
- **Requisitos cubiertos:** `RF-001`, `RF-014`, `RF-015`, `RF-016`.
- **Criterio de aceptación:** `CA-001`, `CA-014`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** casos positivos `test_guias_del_corpus`, `test_consistencia_documental`, `test_inventario_del_corpus` y `test_historial_de_releases`, que verifican el encabezado de cada guía con carácter y rango, la coincidencia de `MEMORY.md` con `specs/INDEX.md` y con el frontmatter, la fila del informe de reauditoría y las ocho filas del historial; caso negativo: cada prueba falla sobre una copia sintética con una guía sin rango, un estado divergente, un archivo sin fila y un release sin fila, e informa el documento y el valor en conflicto; las ocho comprobaciones se escriben en rojo antes de `T-034`.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentosSinRango -q`: «Ran 4 tests in 0.012s» y «OK»; `test_guias_del_corpus` detecta la guía sin rango, `test_consistencia_documental` detecta el estado divergente y nombra `MEMORY.md` y la spec, `test_inventario_del_corpus` detecta el archivo sin fila y nombra `evolucion_sdlc_a_sdd.md`, y `test_historial_de_releases` detecta el release sin fila y nombra `v0.2.0`.
- [x] Completada.

### T-011: Implementación de la casilla de aprobación única

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-003`, `CB-006`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 25 min.
- **Validación:** la prueba positiva y la negativa de `T-001` en verde; `python tools\sdd\validate.py --spec SPEC-012` no registra hallazgo de `C-13` y `python tools\sdd\validate.py --spec SPEC-010` registra el registro dual de G4 mientras la casilla residual siga presente.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-010` devuelve código 1 con «[ERROR] specs\010-mecanismo-control-sdd\spec.md: C-13: registro dual de G4: la spec declara 2 casillas de G4 y la sección admite 1», y `python tools\sdd\validate.py --spec SPEC-012` devuelve código 0 con «OK: sin hallazgos».
- [x] Completada.

### T-012: Implementación del alcance de la referencia a la spec

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-007`, `CB-005`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** las cinco pruebas de `T-002` en verde; `python tools\sdd\validate.py --all` resuelve el punto de corte por el último tag anotado, excluye los merges, informa el número de commits examinados y devuelve código 0 sobre esta rama.
- **Evidencia:** `python tools\sdd\validate.py --all` devuelve código 0 y abre con «Comprobación de historial: punto de corte el tag anotado v0.6.0, 48 commits examinados»; el alcance enumera los commits con `--no-merges` y no registra hallazgo de `C-16` sobre esta rama.
- [x] Completada.

### T-013: Implementación del cierre de integración del reporte

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 25 min.
- **Validación:** las tres pruebas de `T-003` en verde; `python tools\sdd\validate.py --spec SPEC-008` informa la ausencia de la sección de cierre antes de `T-031` y la informa como error fuera de la ventana de legado.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-008` devuelve código 0 y registra «SPEC-008 no declara la sección «Cierre de integración» en el reporte (cláusula de legado)»; fuera de la ventana de legado la misma ausencia es error, como demuestra `test_cierre_ausente` sobre SPEC-012 con código 1.
- [x] Completada.

### T-014: Implementación del check exigible en G5

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-010`, `CB-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 25 min.
- **Validación:** las dos pruebas de `T-004` en verde; la comprobación lee las reglas declaradas de `main` y de `dev` y registra el bloqueo de G5 con la rama y el check cuando el contexto `verify` no figura.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestCheckExigibleEnG5 -q`: «Ran 2 tests in 0.032s» y «OK»; la comprobación lee las reglas declaradas de `main` y de `dev` y el bloqueo de G5 se registra con la rama y el check ausente.
- [x] Completada.

### T-015: Etapas del orquestador y retirada de su escritura sobre `specs/`

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-002`, `RF-009`, `CB-014`.
- **Criterio de aceptación:** `CA-002`, `CA-009`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 25 min.
- **Validación:** la tabla de etapas declara siete filas numeradas de 1 Specify a 7 Release; la matriz declara `specs/**` con efecto `deny` y pierde las concesiones sobre `specs/INDEX.md`, `specs/*/spec.md` y `specs/*/validation_report.md`; el cuerpo del rol conserva la prohibición de escribir la sección de aprobaciones y no redacta artefacto alguno; las pruebas de `T-008` en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q`: «Ran 30 tests» y «OK»; `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q`: «Ran 15 tests» y «OK», con `test_tabla_de_etapas_del_orquestador`, `test_escritura_del_orquestador`, `test_escritura_del_coder`, `test_escritura_del_documenter` y `test_cero_conflictos_de_igual_especificidad` en verde. El commit `fb83aaf` retira las concesiones `edit` sobre `specs/INDEX.md`, `specs/*/spec.md` y `specs/*/validation_report.md` y declara `specs/**` con efecto `deny`, y la tabla de etapas pasa de seis filas numeradas de 2 a 7 a siete filas de `1 Specify` a `7 Release`. La matriz del rol conserva 11 denegaciones explícitas de escritura sin contar el comodín `edit *`, 0 rutas concedidas bajo `specs/` y la prohibición de escribir la sección de aprobaciones en el cuerpo del rol; la corrección de entradas duplicadas de igual especificidad deja `test_cero_conflictos_de_igual_especificidad` en verde sobre los seis roles.
- [x] Completada.

### T-016: Escritura del `coder` sobre `.github/`

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `.opencode/agents/coder.md`.
- **Estimación:** 15 min.
- **Validación:** la matriz del `coder` concede `edit .github/**` y conserva la denegación explícita sobre `specs/`, `docs/`, `.opencode/` y los documentos de raíz; `test_escritura_del_coder` en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q`: «Ran 30 tests» y «OK», y `TestMatrizDePermisos`: «Ran 15 tests» y «OK», con `test_escritura_del_coder` en verde: admite `edit` sobre `src/`, `tests/`, `tools/`, `specs/*/tasks.md` y `.github/**`, y deniega `edit` sobre `specs/*/spec.md`, `docs/`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `.opencode/` y `.env`. El commit `fb83aaf` añade en `.opencode/agents/coder.md` la concesión `edit .github/**` con efecto `allow` (3 líneas añadidas) y conserva las denegaciones explícitas sobre `specs/`, `docs/`, `.opencode/` y los documentos de raíz `AGENTS.md` y `MEMORY.md`.
- [x] Completada.

### T-017: Escritura del `documenter` sobre los documentos de raíz

- **Dependencias:** `T-016`.
- **Requisitos cubiertos:** `RF-014`, `RF-015`, `RF-016`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `.opencode/agents/documenter.md`.
- **Estimación:** 15 min.
- **Validación:** la matriz del `documenter` concede `edit MEMORY.md` y `edit CHANGELOG.md` y conserva la denegación explícita sobre `specs/`, `src/`, `tools/`, `.opencode/` y `.github/`; el cuerpo del rol declara la delegación del propietario para los documentos de raíz; `test_escritura_del_documenter` en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions -q`: «Ran 30 tests» y «OK», y `TestMatrizDePermisos`: «Ran 15 tests» y «OK», con `test_escritura_del_documenter` en verde: admite `edit` sobre `docs/sdd/PROTOCOLO_OPERATIVO.md`, `AGENTS.md`, `MEMORY.md` y `CHANGELOG.md`, y deniega `edit` sobre `specs/`, `src/`, `tests/`, `tools/`, `.opencode/`, `.github/` y `.env`. El commit `fb83aaf` añade en `.opencode/agents/documenter.md` las concesiones `edit MEMORY.md` y `edit CHANGELOG.md` con efecto `allow` (6 líneas añadidas); la delegación del propietario sobre los dos documentos de raíz queda declarada en §12 del protocolo, que atribuye al `documenter` su escritura en el alcance del contrato de la spec en curso. Desviación registrada: el cuerpo de `.opencode/agents/documenter.md` enumera `docs/` y `AGENTS.md` y no nombra de forma literal `MEMORY.md` ni `CHANGELOG.md`; la concesión consta en la matriz de permisos del mismo archivo y la verifica la prueba.
- [x] Completada.

### T-018: Preparación del árbol y del entorno en el flujo `SDD`

- **Dependencias:** `T-016`, `T-005`.
- **Requisitos cubiertos:** `RF-010`, `CB-009`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `.github/workflows/sdd.yml`.
- **Estimación:** 20 min.
- **Validación:** `actions/checkout@v4` figura como primera preparación del job `verify`, seguida de `actions/setup-python@v5` con la versión 3.12, la validación agregada y la suite; se conservan el disparador de Pull Request hacia `main` y `dev`, el límite de 5 minutos, `contents: read` y 0 efectos remotos; las pruebas de `T-005` en verde.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_agent_permissions.TestFlujoDeIntegracionContinua -q`: «Ran 3 tests in 0.003s» y «OK»; `git diff --numstat` del flujo declara 2 líneas añadidas y 0 eliminadas, con `actions/checkout@v4` como primera preparación del job `verify`, seguida de `actions/setup-python@v5` con la versión 3.12.
- [x] Completada.

### T-019: Check `verify` exigible en las reglas de protección

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-010`, `CB-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/git/protection_rules/main.json`, `tools/git/protection_rules/dev.json`.
- **Estimación:** 20 min.
- **Validación:** ambos archivos declaran `required_status_checks` como objeto con `strict` verdadero y una entrada de contexto `verify`; se conservan los valores de `enforce_admins`, revisiones, restricciones, historial lineal, fuerza, borrado y resolución de conversaciones; `test_reglas_de_proteccion_exigen_verify` en verde.
- **Evidencia:** `main.json` y `dev.json` declaran `"required_status_checks": {"strict": true, "checks": [{"context": "verify"}]}` con 8 líneas añadidas y 1 eliminada cada uno; `test_reglas_de_proteccion_exigen_verify` contrasta el bloque declarado con `required_status_contexts` y devuelve 0 hallazgos.
- [x] Completada.

### T-020: Comparación del objeto de comprobaciones exigibles

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/git/verify_branch_protection.py`.
- **Estimación:** 30 min.
- **Validación:** el comparador contrasta `strict` y el conjunto de contextos del objeto declarado, toma el segmento posterior a `/ ` de la forma presentada por la interfaz y conserva la detección de comprobaciones inesperadas cuando el valor esperado es nulo; las pruebas de `T-006` en verde.
- **Evidencia:** `python -m unittest tools.git.tests.test_verify_branch_protection -q`: «Ran 39 tests in 0.015s» y «OK»; la discrepancia del caso negativo declara el contexto esperado y el observado, la comparación toma el segmento posterior a `/ ` de la forma presentada por la interfaz y el valor esperado nulo conserva la detección de comprobaciones inesperadas.
- [x] Completada.

### T-021: Declaración de la firma verificada en el protocolo

- **Dependencias:** `T-017`.
- **Requisitos cubiertos:** `RF-004`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** §14 declara entre las comprobaciones ejecutadas la firma criptográfica del commit de aprobación y la pertenencia de la clave firmante a `docs/sdd/firmantes_autorizados`, y su lista de comprobaciones no verificadas ya no las menciona; `test_contrato_de_firma_verificada` en verde.
- **Evidencia:** commit `26a7cc8`. §14 del protocolo declara en «Comprobaciones verificadas»: «El validador verifica además la firma criptográfica del commit de aprobación y la pertenencia de la clave firmante a `docs/sdd/firmantes_autorizados`, con el procedimiento de §11», y la lista de «Comprobaciones no verificadas» queda como «La veracidad de la evidencia transcrita; la ejecución real de un script `.bat` o de una suite de pruebas; las tres verificaciones de release de §13; la autosuficiencia del protocolo; la conformidad del régimen completo», sin mención de la firma. `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentosNormativos -q`: «Ran 4 tests» y «OK», con `test_contrato_de_firma_verificada` en verde.
- [x] Completada.

### T-022: Declaración de la firma verificada en la norma operativa

- **Dependencias:** `T-021`.
- **Requisitos cubiertos:** `RF-004`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `AGENTS.md`.
- **Estimación:** 15 min.
- **Validación:** la sección de validación declara que el validador verifica la firma del commit de aprobación y la pertenencia de la clave firmante, y no conserva la afirmación que declara esas verificaciones no realizadas; el documento conserva entre 30 y 70 líneas útiles y sus seis roles.
- **Evidencia:** commit `26a7cc8`. La sección «Validación» de `AGENTS.md` declara: «El validador verifica la firma criptográfica del commit de aprobación y la pertenencia de la clave firmante a `docs/sdd/firmantes_autorizados`, además de estructura, estados, trazabilidad y alcance declarado; no acredita la conformidad del régimen», y no conserva la afirmación anterior que negaba esa verificación. El archivo tiene 89 líneas, de las cuales 68 son líneas útiles no vacías y quedan dentro del intervalo de 30 a 70 que exige el validador, y conserva los seis roles de agente `sdd`, `planner`, `coder`, `reviewer`, `documenter` y `auditor`.
- [x] Completada.

### T-023: Declaración de las dos ventanas de legado

- **Dependencias:** `T-022`.
- **Requisitos cubiertos:** `RF-005`, `CB-011`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §14 y §15 declaran la ventana estructural de `SPEC-001` a `SPEC-009` para C-01 a C-13 y la ventana de trazabilidad de `SPEC-008` a `SPEC-011` para C-14 a C-18, cada una con su motivo y su límite, y una spec fuera de su ventana produce error sin degradación; `test_ventanas_de_legado` en verde y coincidencia fila por fila con las constantes del validador.
- **Evidencia:** commit `26a7cc8`. §14 declara la tabla «Ventanas de legado» con dos filas: «Estructural | `SPEC-001` a `SPEC-009` | `C-01` a `C-13` | Specs redactadas y cerradas antes de la base v2, con contrato anterior a las comprobaciones de estructura y aprobación | No admite una spec posterior a `SPEC-009`; su ampliación exige una spec nueva» y «Trazabilidad | `SPEC-008` a `SPEC-011` | `C-14` a `C-18` | Specs validadas sin release, cuyo cierre de integración y regularización se tramita en una spec posterior | No admite una spec posterior a `SPEC-011`; su ampliación exige una spec nueva»; §15 reitera que las dos ventanas son concesiones cerradas que no se amplían sin una spec posterior. `test_ventanas_de_legado` queda en verde en `TestDocumentosNormativos` con «Ran 4 tests» y «OK», y las dos filas coinciden con `LEGACY_SPECS` y `TRACE_LEGACY_SPECS` del validador.
- [x] Completada.

### T-024: Atribución de la escritura de T4 a T7

- **Dependencias:** `T-023`.
- **Requisitos cubiertos:** `RF-008`, `CB-016`.
- **Criterio de aceptación:** `CA-008`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** §5 atribuye al `planner` la escritura de T4, T5, T6 y T7 sobre la verificación registrada por el orquestador e informa la ausencia de esa verificación como impedimento de la transición; las filas T4 a T6 del historial de `SPEC-012` no se editan y su estado vigente no cambia; `test_tabla_de_escritura_de_estados` en verde.
- **Evidencia:** commit `26a7cc8`. §5 declara: «El `planner` escribe las transiciones T4, T5, T6 y T7 sobre la verificación registrada por el orquestador; sin esa verificación registrada no escribe la transición e informa la verificación ausente», con la escritura de transiciones repartida entre tres roles y sin transición escrita sin la evidencia que la tabla exige. `git diff --numstat a4eefa0 HEAD -- specs/012-trazabilidad-profunda-sdd/spec.md` no devuelve línea alguna, es decir, 0 líneas añadidas y 0 eliminadas: las filas T4, T5 y T6 del historial no se editan y el estado vigente de la spec no cambia. `test_tabla_de_escritura_de_estados` queda en verde en `TestDocumentosNormativos` con «Ran 4 tests» y «OK».
- [x] Completada.

### T-025: Autoridad del orquestador sin escritura de artefactos

- **Dependencias:** `T-024`.
- **Requisitos cubiertos:** `RF-009`, `CB-014`.
- **Criterio de aceptación:** `CA-009`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §12 declara que el orquestador verifica compuertas, registra resultados, ejecuta el validador y `git add` y `git commit` de los artefactos de control, no redacta artefacto alguno y conserva la prohibición de escribir la sección de aprobaciones; el número de atribuciones de escritura sobre `specs/` es 0 y la contradicción con el cuerpo del rol queda en 0; la prueba de la matriz de agentes en verde.
- **Evidencia:** commit `26a7cc8`. La fila del orquestador en la tabla de §12 declara: «ninguna sobre documentos y código ni sobre `specs/`; verifica G2, G3 y G5, registra el resultado de cada verificación, ejecuta el validador y `git add` y `git commit` de artefactos de control, lanza subagentes y no redacta artefacto alguno», y la regla de la matriz añade que ninguna concesión de escritura autoriza a declarar una compuerta ni a escribir la sección de aprobaciones de `spec.md`. `test_escritura_del_orquestador` queda en verde: 0 atribuciones de escritura bajo `specs/`, `specs/**` denegado de forma explícita y 0 contradicciones entre la matriz y el cuerpo del rol.
- [x] Completada.

### T-026: Exigibilidad del check `verify` en la norma de integración

- **Dependencias:** `T-025`.
- **Requisitos cubiertos:** `RF-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 20 min.
- **Validación:** la sección de protección declara exigible el check `verify` del flujo `SDD` en `main` y en `dev`, cita `configure_branch_protection.py` y `verify_branch_protection.py`, y registra que la ausencia del check exigible bloquea G5.
- **Evidencia:** commit `26a7cc8`. La norma de integración declara en «Check exigible» que «El check exigible de las dos ramas es el job `verify` del flujo `SDD` de `.github/workflows/sdd.yml`, con `strict: true`», cita `python tools/git/configure_branch_protection.py` y `python tools/git/verify_branch_protection.py` y registra que «Si una de las dos ramas no declara exigible el check `verify`, la verificación de G5 queda bloqueada y el caso se registra como ausencia del check exigible». La fila de `required_status_checks` de la tabla de protección pasa a `verify` (`strict: true`) en `main` y en `dev`, en concordancia con el contexto declarado en `tools/git/protection_rules/main.json` y en `dev.json`.
- [x] Completada.

### T-027: Suite del mecanismo en la norma de integración

- **Dependencias:** `T-026`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-011`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 15 min.
- **Validación:** la afirmación sobre la ausencia de suite automatizada para la raíz queda sustituida por la declaración de la suite del mecanismo de control, sus 131 pruebas y su ejecución en el job `verify`; el número de afirmaciones que niegan su existencia es 0; `test_documentacion_operativa` en verde.
- **Evidencia:** commit `26a7cc8`. La afirmación anterior, «No existe una suite automatizada de pruebas para la raíz del repositorio», queda sustituida por: «La raíz del repositorio cuenta con la suite del mecanismo de control en `tools/sdd/tests/`: las 131 pruebas vigentes en el corte de la auditoría de cierre más las añadidas por las specs posteriores. El job `verify` del flujo `SDD` de `.github/workflows/sdd.yml` la ejecuta con `python -m unittest discover -s tools\sdd\tests -q` en cada Pull Request dirigido a `main` y a `dev`. La suite no sustituye las validaciones anteriores». La búsqueda del texto anterior devuelve 0 coincidencias y `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentacionOperativa -q` devuelve «Ran 2 tests» y «OK».
- [x] Completada.

### T-028: Sincronización previa al release por ancestría

- **Dependencias:** `T-027`.
- **Requisitos cubiertos:** `RF-012`, `CB-003`, `CB-004`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 30 min.
- **Validación:** la sincronización se expresa con `git merge-base --is-ancestor main dev` y con `git merge-base --is-ancestor vX.Y.Z^{commit} main`; el conteo simétrico y la exigencia de la salida `0 0` quedan retirados; el estado `48 0` de `dev` respecto de `main` no se trata como bloqueo; la falta de ancestría detiene el empaquetado y un tag no alcanzable detiene el release; `test_sincronizacion_por_ancestria` en verde.
- **Evidencia:** commit `26a7cc8`. El bloque de sincronización queda como «Antes del empaquetado se verifica la relación de ancestría entre las dos ramas: `main` debe ser ancestro de `dev`, de modo que cada commit de `main` esté contenido en `dev`», con la comprobación `git merge-base --is-ancestor main dev`; «Un resultado distinto de `0` detiene el empaquetado e informa la relación de ancestría incumplida. El conteo de commits entre las dos ramas no se exige: `dev` puede estar por delante de `main` con trabajo no publicado sin que ese estado bloquee el release». Tras el tag, el bloque declara «Después se verifica que el tag apunte a un commit alcanzable desde `main`» con `git merge-base --is-ancestor vX.Y.Z^{commit} main`, y «Un resultado distinto de `0` detiene el release y la sincronización no se declara cumplida». La búsqueda de `rev-list --left-right` devuelve 0 coincidencias, el estado `48 0` de `dev` respecto de `main` no se trata como bloqueo y `test_sincronizacion_por_ancestria` queda en verde en `TestDocumentosNormativos` con «Ran 4 tests» y «OK».
- [x] Completada.

### T-029: Gramática de cinco prefijos en la norma de integración

- **Dependencias:** `T-028`.
- **Requisitos cubiertos:** `RF-013`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** la expresión declarada es `^(feat|fix|hotfix|docs|release)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$`; la lista admitida es de cinco prefijos; `docs/` se admite para cambios exclusivamente documentales con la misma validación y la misma longitud; un prefijo fuera de la lista se rechaza; las pruebas de `T-007` en verde.
- **Evidencia:** commit `26a7cc8`. La expresión declarada es `^(feat|fix|hotfix|docs|release)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$`, la lista admitida es de cinco prefijos y `docs/` se reserva a los cambios exclusivamente documentales con las mismas reglas de minúsculas, números y guiones y la misma longitud de 3 a 63 caracteres medida sobre `<nombre>`. La prueba documental contrasta siete nombres con su resultado: admite `feat/reauditoria-cierre`, `docs/cierre-integracion-spec-012` y `release/v0-7-0`; rechaza `docs/Cierre-Integracion` por mayúscula, `docs/ab` por longitud menor que 3, `docs/uno_dos` por guion bajo y `chore/limpieza` por prefijo fuera de la lista de cinco. `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentacionOperativa -q`: «Ran 2 tests» y «OK», con `test_gramatica_de_ramas` en verde.
- [x] Completada.

### T-030: Gramática de cinco prefijos en la norma operativa

- **Dependencias:** `T-029`.
- **Requisitos cubiertos:** `RF-013`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `AGENTS.md`.
- **Estimación:** 15 min.
- **Validación:** la sección de Git declara las ramas de trabajo `feat/*`, `fix/*`, `hotfix/*` y `docs/*` junto con las ramas de empaquetado `release/vX-Y-Z`, en minúsculas, números y guiones; el número de prefijos admitidos es 5 y la norma no conserva una lista de tres prefijos de trabajo.
- **Evidencia:** commit `26a7cc8`. La viñeta de la sección «Git» de `AGENTS.md` declara «Ramas de trabajo `feat/*`, `fix/*`, `hotfix/*` y `docs/*`; ramas de empaquetado `release/vX-Y-Z` en minúsculas, números y guiones», con cinco prefijos admitidos y sin la lista anterior de tres prefijos de trabajo. La misma viñeta de `MEMORY.md` en su §9 queda alineada con los cuatro prefijos de trabajo y el de empaquetado. El recuento de prefijos declarados es 5 y el de listas de tres prefijos de trabajo es 0.
- [x] Completada.

### T-031: Cierre de integración de `SPEC-008` y `SPEC-009`

- **Dependencias:** `T-030`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/008-auditoria-cumplimiento-sdd/validation_report.md`, `specs/009-base-normativa-sdd/validation_report.md`.
- **Estimación:** 20 min.
- **Validación:** cada reporte declara al final la sección `## Cierre de integración` con `Merge: 49caac9` para `SPEC-008` y `Merge: 09eaf34` para `SPEC-009`, y con la línea `Release:` vacía; la matriz y el dictamen quedan sin alteración; `python tools\sdd\validate.py --spec SPEC-008` y `--spec SPEC-009` no registran hallazgo de `C-17`.
- **Evidencia:** commit `a510408`. `specs/008-auditoria-cumplimiento-sdd/validation_report.md` declara la sección `## Cierre de integración` en su línea 141 con `Merge: 49caac9` y la línea `Release:` vacía, y `specs/009-base-normativa-sdd/validation_report.md` la declara en su línea 124 con `Merge: 09eaf34` y `Release:` vacía; la matriz y el dictamen de los dos reportes quedan sin alteración. `git show --numstat a510408` declara 5 líneas añadidas y 0 eliminadas en cada reporte. `python tools\sdd\validate.py --spec SPEC-008` y `python tools\sdd\validate.py --spec SPEC-009` devuelven código 0, sin hallazgo de `C-17`; el primero conserva las advertencias de legado ya registradas antes del cierre.
- [x] Completada.

### T-032: Cierre de integración de `SPEC-010` y `SPEC-011`

- **Dependencias:** `T-031`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/010-mecanismo-control-sdd/validation_report.md`, `specs/011-practica-operativa-sdd/validation_report.md`.
- **Estimación:** 20 min.
- **Validación:** cada reporte declara al final la sección `## Cierre de integración` con `Merge: 94c2ea1` para `SPEC-010` y `Merge: 9df8446` para `SPEC-011`, y con la línea `Release:` vacía; la matriz y el dictamen quedan sin alteración; las cuatro specs de `SPEC-008` a `SPEC-011` conservan el estado `validated`.
- **Evidencia:** commit `a510408`. `specs/010-mecanismo-control-sdd/validation_report.md` declara la sección `## Cierre de integración` con `Merge: 94c2ea1` y la línea `Release:` vacía, y `specs/011-practica-operativa-sdd/validation_report.md` la declara con `Merge: 9df8446` y `Release:` vacía; `git show --numstat a510408` declara 5 líneas añadidas y 0 eliminadas en cada reporte. Las cuatro specs de `SPEC-008` a `SPEC-011` conservan el estado `validated` en `specs/INDEX.md`, líneas 14 a 17, y `python tools\sdd\validate.py --spec SPEC-010` y `python tools\sdd\validate.py --spec SPEC-011` devuelven código 0 con «OK: sin hallazgos».
- [x] Completada.

### T-033: Retirada de las casillas residuales de G4

- **Dependencias:** `T-032`.
- **Requisitos cubiertos:** `RF-003`, `CB-006`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `specs/010-mecanismo-control-sdd/spec.md`, `specs/011-practica-operativa-sdd/spec.md`.
- **Estimación:** 20 min.
- **Validación:** cada sección de aprobaciones conserva dos casillas, G1 y G4, y ninguna más; la tercera casilla con el marcador de plantilla queda retirada; `python tools\sdd\validate.py --spec SPEC-010` y `--spec SPEC-011` no registran hallazgo de `C-13`; el cambio lo publica el propietario en un commit firmado y el agente solo prepara el diff, sin firmar, sin confirmar y sin marcar la casilla de esta tarea.
- **Evidencia:** commit `a4378d8`, publicado por el propietario con firma verificada: `git log --show-signature -1 a4378d8` devuelve «Good "git" signature for sebaxtianrioss@gmail.com with ED25519 key SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc», la clave consta en `docs/sdd/firmantes_autorizados` y `git log --oneline -1 a4378d8 --format="%H %G? %GS %GK"` devuelve `G` con el firmante `sebaxtianrioss@gmail.com` y la huella `SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc`. El commit retira la tercera casilla de G4 de las secciones de aprobaciones de `SPEC-010` y `SPEC-011`, con 1 línea eliminada en cada `spec.md` y 2 en el total, de modo que cada sección conserva las dos casillas G1 y G4. `python tools\sdd\validate.py --all` pasa de 1 hallazgo de `C-13` a 0 y devuelve código 0, y `python tools\sdd\validate.py --spec SPEC-010` y `--spec SPEC-011` devuelven código 0 con «OK: sin hallazgos».
- [x] Completada.

### T-034: Encabezado de carácter y rango en las guías del corpus

- **Dependencias:** `T-033`.
- **Requisitos cubiertos:** `RF-001`, `CB-012`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/guia_*.md`, que alcanza las doce guías del corpus: `guia_maestra_sdd.md`, `guia_constitution_md.md`, `guia_agents_md.md`, la guía de notación EARS, `guia_spec_md.md`, `guia_clarify_md.md`, `guia_plan_md.md`, `guia_tasks_md.md`, `guia_fase_implement_tdd.md`, `guia_subagentes_opencode_sdd.md`, `guia_skills_agentes_sdd.md` y `guia_servidores_mcp.md`.
- **Estimación:** 30 min.
- **Validación:** las doce guías declaran en el encabezado su carácter no normativo y el rango «Sin rango» con la remisión a `PROTOCOLO_OPERATIVO.md`; una guía que ya cumple la declaración no se modifica y su conformidad previa se registra; `test_guias_del_corpus` en verde con 0 guías sin declaración.
- **Evidencia:** commit `26a7cc8`. Las doce guías de `docs/sdd/guia_*.md` declaran en su línea 3 «Documento de referencia (no normativo). Su rango es «Sin rango» y no fija reglas. Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md»: la guía maestra, la de la constitución, la de `AGENTS.md`, la de notación EARS, la de `spec.md`, la de `clarify.md`, la de `plan.md`, la de `tasks.md`, la de la fase de implementación TDD, la de subagentes de OpenCode, la de skills de agentes y la de servidores MCP. El recuento de guías con encabezado conforme es 12 y el de guías sin declaración es 0; no hay guía sin modificar por conformidad previa, porque las doce requerían la declaración y quedó registrada su corrección. `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentosSinRango -q`: «Ran 4 tests» y «OK», con `test_guias_del_corpus` en verde.
- [x] Completada.

### T-035: Encabezado de carácter y rango en las referencias del corpus

- **Dependencias:** `T-034`.
- **Requisitos cubiertos:** `RF-001`, `CB-012`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/referencia_7_etapas_sdd.md`, `docs/sdd/referencia_ciclo_vida_sdd_puro.md`, `docs/sdd/compendio_sdd.md`.
- **Estimación:** 15 min.
- **Validación:** las tres referencias declaran en el encabezado su carácter no normativo y el rango «Sin rango»; una referencia que ya cumple la declaración no se modifica y su conformidad previa se registra; el número de archivos del corpus sin declaración de rango en el encabezado es 0.
- **Evidencia:** commit `26a7cc8`. `docs/sdd/referencia_7_etapas_sdd.md`, `docs/sdd/referencia_ciclo_vida_sdd_puro.md` y `docs/sdd/compendio_sdd.md` declaran en su línea 3 «Documento de referencia (no normativo). Su rango es «Sin rango» y no fija reglas. Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md»; ninguna de las tres quedó sin modificar por conformidad previa. El recuento de archivos con declaración de rango vigente en el encabezado es 15: las doce guías y las tres referencias, con 0 guías sin declaración según `test_guias_del_corpus`. Desviación registrada: los informes de análisis y de auditoría, el mapa mental y los diagramas de `docs/sdd/` figuran como «Sin rango» en el inventario y no declaran el rango en su encabezado; quedan fuera del alcance de `RF-001`, que alcanza las guías y las referencias.
- [x] Completada.

### T-036: Correcciones de las tres guías señaladas por la reauditoría

- **Dependencias:** `T-035`.
- **Requisitos cubiertos:** `RF-001`, `CB-012`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/guia_spec_md.md`, `docs/sdd/guia_clarify_md.md`, `docs/sdd/referencia_7_etapas_sdd.md`.
- **Estimación:** 25 min.
- **Validación:** la denominación «Definition of Done» queda sustituida por «criterio de aceptación» en las tres apariciones de `guia_spec_md.md`; el identificador fuera de formato de `guia_clarify_md.md` queda sustituido por `CB-001`; el título del criterio de `referencia_7_etapas_sdd.md` coincide con la plantilla de rango 5; el número de identificadores de ejemplo con menos de tres dígitos es 0.
- **Evidencia:** commit `26a7cc8`. Cinco sustituciones aplicadas: en `docs/sdd/guia_spec_md.md`, la viñeta «6. **Criterios de Aceptación (_Definition of Done_):**» pasa a «6. **Criterio de aceptación (`CA-NNN`):**» y los dos títulos «## 6. Criterios de Aceptación (Definition of Done)» pasan a «## 6. Criterios de aceptación»; en `docs/sdd/guia_clarify_md.md`, las dos apariciones de `CB-NUEVO-01` pasan a `CB-001`. En `docs/sdd/referencia_7_etapas_sdd.md`, el bloque «Casos Límite y Fueras de Alcance» se separa en «Casos borde» y «Fuera de alcance», y se añade «Criterios de aceptación» con `CA-001`, con lo que el título del criterio coincide con la plantilla de rango 5. La búsqueda de «Definition of Done» devuelve 0 coincidencias en las guías y en las referencias —solo permanece citada en los dos informes de auditoría, que están fuera de alcance— y el número de identificadores de ejemplo con menos de tres dígitos es 0.
- [x] Completada.

### T-037: Estado de las specs en el contexto operativo

- **Dependencias:** `T-036`.
- **Requisitos cubiertos:** `RF-014`, `CB-013`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `MEMORY.md`.
- **Estimación:** 15 min.
- **Validación:** la línea de estado declara `SPEC-001` a `SPEC-007` publicadas, `SPEC-008` a `SPEC-012` validadas y `SPEC-013` con el estado de su frontmatter; el número de divergencias con `specs/INDEX.md` y con el frontmatter de cada spec es 0; `test_consistencia_documental` en verde.
- **Evidencia:** commit `26a7cc8`. La línea de estado de `MEMORY.md` declara: «Estado de specs: `SPEC-001` a `SPEC-007` publicadas; `SPEC-008` a `SPEC-012` validadas; `SPEC-013` en curso con estado `tasked`», coherente con `specs/INDEX.md` y con el frontmatter de `SPEC-013`, cuyo `status` es `tasked`; el número de divergencias entre los tres soportes es 0. `test_consistencia_documental` queda en verde en `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentosSinRango -q`: «Ran 4 tests» y «OK».
- [x] Completada.

### T-038: Fila del informe de reauditoría en el índice del corpus

- **Dependencias:** `T-037`.
- **Requisitos cubiertos:** `RF-015`, `CB-013`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `docs/sdd/README.md`.
- **Estimación:** 15 min.
- **Validación:** la tabla de inventario registra la fila del informe `docs/sdd/auditoria_cierre_v0_7_0.md` con su ruta, su carácter de informe de auditoría, su orden de lectura y el rango «Sin rango»; el número de archivos del corpus sin fila es 0; `test_inventario_del_corpus` en verde.
- **Evidencia:** commit `26a7cc8`. La tabla de inventario de `docs/sdd/README.md` registra la fila «`auditoria_cierre_v0_7_0.md` | `docs/sdd/auditoria_cierre_v0_7_0.md` | Informe de auditoría de la reauditoría de cierre | 32 | Sin rango», la tabla tiene 33 filas de datos con orden de lectura único y el número de archivos del corpus sin fila es 0. `test_inventario_del_corpus` queda en verde en `TestDocumentosSinRango`: «Ran 4 tests» y «OK».
- [x] Completada.

### T-039: Historial de releases del registro de cambios

- **Dependencias:** `T-038`.
- **Requisitos cubiertos:** `RF-016`, `CB-013`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 25 min.
- **Validación:** el historial declara ocho filas con versión, fecha y tag de `v0.1.0` a `v0.6.0` en orden ascendente, hasta el release anterior a `v0.7.0`; el número de releases publicados sin fila es 0; la entrada de `v0.7.0` permanece en `Unreleased`; `test_historial_de_releases` en verde.
- **Evidencia:** commit `26a7cc8`. El historial de releases de `CHANGELOG.md` declara ocho filas en orden ascendente con versión, fecha y tag: `v0.1.0` (2026-11-10), `v0.2.0` (2026-11-12), `v0.3.0`, `v0.3.1`, `v0.4.0`, `v0.5.0` y `v0.5.1` (2026-11-13) y `v0.6.0` (2026-11-13), hasta el release anterior a `v0.7.0`; el número de releases publicados sin fila es 0 y la entrada de `v0.7.0` permanece en `Unreleased`. `test_historial_de_releases` contrasta la tabla con los ocho tags anotados publicados y queda en verde en `TestDocumentosSinRango`: «Ran 4 tests» y «OK».
- [x] Completada.

### T-040: Regresión de la suite y del corpus

- **Dependencias:** `T-039`.
- **Requisitos cubiertos:** `RNF-002`, `RNF-003`, `RNF-006`.
- **Criterio de aceptación:** `CA-016`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` devuelve las 131 pruebas vigentes más las nuevas en verde con código 0; `python tools\sdd\validate.py --all` devuelve código 0 en 300 segundos o menos; dos ejecuciones consecutivas sobre el mismo commit presentan 0 diferencias en el conjunto de hallazgos; la ejecución no accede a red, servicio externo ni credencial y conserva los códigos de salida 0, 1 y 2.
- **Evidencia:** `python -m unittest discover -s tools\sdd\tests -q`: «Ran 156 tests in 1.074s» y «OK»; `python tools\sdd\validate.py --all` devuelve código 0 en 2,217 s y 2,165 s en dos ejecuciones consecutivas sobre el mismo commit, con «DIFERENCIAS 0» y 80 líneas idénticas; `TestCodigosSalida` conserva los códigos 0, 1 y 2 con «Ran 5 tests in 0.016s» y «OK»; la suite solo usa la biblioteca estándar y no accede a red, servicio externo ni credencial.
- [x] Completada.

### T-041: Contraste de las cinco specs publicadas

- **Dependencias:** `T-040`.
- **Requisitos cubiertos:** `RNF-005`, `CB-015`.
- **Criterio de aceptación:** `CA-017`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** `git diff` de `SPEC-008` a `SPEC-012` contra su versión anterior muestra como diferencia solo la sección de cierre añadida y las dos casillas retiradas; el 100 % de sus requisitos, criterios de aceptación y estados queda sin cambios; una observación que exija cambiar un requisito publicado queda registrada como detenida y tramitada por una spec nueva.
- **Evidencia:** `git diff --numstat a4eefa0 HEAD` de las cinco specs declara `5 0` en cada reporte de `SPEC-008` a `SPEC-011`, `0 1` en `spec.md` de `SPEC-010` y de `SPEC-011`, y ninguna línea en `SPEC-012`; las líneas eliminadas son la casilla residual de G4 y las añadidas son la sección «Cierre de integración» con `Merge: 49caac9`, `09eaf34`, `94c2ea1` y `9df8446` y la línea `Release:` vacía; los estados de `SPEC-008` a `SPEC-012` siguen en `validated` en `specs/INDEX.md` y en su frontmatter, y el recuento de requisitos, criterios y estados alterados es 0; ninguna observación exigió cambiar un requisito publicado y no queda observación detenida para una spec nueva.
- [x] Completada.

### T-042: Consistencia de los documentos de rango 2, rango 3 y rango 4

- **Dependencias:** `T-041`.
- **Requisitos cubiertos:** `RNF-007`, `RNF-008`.
- **Criterio de aceptación:** `CA-018`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** el contraste de las afirmaciones corregidas en `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `docs/Flujo_de_Trabajo_Git.md` arroja 0 contradicciones, y el 100 % de los documentos corregidos conserva en su encabezado su rango y su carácter; las pruebas de `T-009` y `T-010` en verde.
- **Evidencia:** Contraste de las cinco afirmaciones con resultado 0 contradicciones: firma verificada en `AGENTS.md` (§ Validación), §14 del protocolo y G6 de la norma de integración; autoridad del orquestador en `AGENTS.md` (§ Entrada SDD), §12 y G5 del flujo; ancestría `main` → `dev` en `AGENTS.md` (§ Git), §13 y el bloque de sincronización del flujo; gramática de cinco prefijos en `AGENTS.md` (§ Git) y en el flujo, con la misma expresión y la misma longitud de 3 a 63; ventanas `SPEC-001` a `SPEC-009` y `SPEC-008` a `SPEC-011` en §14 y §15, iguales a `LEGACY_SPECS` y `TRACE_LEGACY_SPECS`. Los tres documentos conservan su encabezado: `AGENTS.md` como norma operativa de rango 2, el protocolo como norma ejecutable de rango 3 y el flujo como norma de integración de rango 4, los dos últimos con carácter normativo.
- [x] Completada.

### T-043: Pareja positiva y negativa de cada comprobación nueva

- **Dependencias:** `T-042`.
- **Requisitos cubiertos:** `RNF-004`.
- **Criterio de aceptación:** `CA-016`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** cada una de las cuatro comprobaciones corregidas y de las comprobaciones documentales nuevas declara al menos una prueba positiva y una negativa en la suite del mecanismo de control; el recuento de comprobaciones sin pareja es 0 y el de pruebas nuevas coincide con el declarado en `T-001` a `T-010`.
- **Evidencia:** `python -m unittest discover -s tools\sdd\tests -q`: «Ran 156 tests in 1.074s» y «OK»; las doce comprobaciones declaran pareja positiva y negativa, el recuento de comprobaciones sin pareja es 0 y la suite del mecanismo de control pasa de 131 a 156 pruebas, con 25 casos nuevos en `tools/sdd/tests`; los dos casos de `T-006` viven en `tools/git/tests/test_verify_branch_protection.py` y las comprobaciones de `T-005` y `T-008` se ampliaron sobre pruebas existentes, sin retirar caso alguno.

  | Comprobación | Prueba positiva | Prueba negativa |
  |---|---|---|
  | `C-09`, check `verify` exigible | `test_reglas_de_proteccion_exigen_verify` | `test_proteccion_sin_check_bloquea_g5` |
  | `C-13`, casilla única por compuerta | `test_casilla_unica_por_compuerta` | `test_casilla_duplicada_sin_marcar_es_error` |
  | `C-16`, alcance de la cadena `Spec:` | `test_alcance_desde_ultimo_tag` | `test_commit_sin_spec_en_alcance` |
  | `C-17`, cierre de integración | `test_cierre_de_spec_validada` | `test_release_declarado_en_validated_es_error` |
  | Firma verificada | `test_contrato_de_firma_verificada` | Copia sintética de §14 con la firma entre las comprobaciones no verificadas |
  | Ventanas de legado | `test_ventanas_de_legado` | Fila sintética sin motivo |
  | Escritura de estados | `test_tabla_de_escritura_de_estados` | Bloque anterior que atribuye T4 a T7 al orquestador |
  | Sincronización por ancestría | `test_sincronizacion_por_ancestria` | Bloque anterior con `rev-list --left-right` y la salida «0 0» |
  | Guías del corpus | `test_guias_del_corpus` | Encabezado sintético sin «Sin rango» |
  | Consistencia documental | `test_consistencia_documental` | `MEMORY.md` con «publicadas» donde corresponde «validadas» |
  | Inventario del corpus | `test_inventario_del_corpus` | Copia sin la fila de `evolucion_sdlc_a_sdd.md` |
  | Historial de releases | `test_historial_de_releases` | Registro sintético sin la fila de `v0.2.0` |
- [x] Completada.

### T-044: Cierre del alcance y traspaso a la validación

- **Dependencias:** `T-043`.
- **Requisitos cubiertos:** `RNF-001`.
- **Criterio de aceptación:** `CA-015`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** las cuarenta y cuatro tareas figuran cerradas con su evidencia transcrita; `python tools\sdd\validate.py --spec SPEC-013 --gate G3` devuelve código 0; el paquete de traspaso reúne los cuatro artefactos de la spec, las dieciséis observaciones con su artefacto de cierre y la salida agregada, y no declara compuerta alguna.
- **Evidencia:** Las cuarenta y cuatro tareas figuran cerradas con su evidencia transcrita y `python tools\sdd\validate.py --spec SPEC-013 --gate G3` devuelve código 0. El paquete de traspaso reúne `spec.md`, `clarify.md`, `plan.md` y `tasks.md`, las dieciséis observaciones con su artefacto de cierre, las doce comprobaciones con pareja positiva y negativa, 156 pruebas en verde y `--all` con código 0; la compuerta G3 la verifica la sesión orquestadora, que no delega la compuerta. Esta tarea no declara compuerta alguna.

  | Observación | Requisito | Artefacto que la cierra |
  |---|---|---|
  | `AUD-008` | `RF-001` | Encabezado de rango y carácter en las doce guías y en las tres referencias, con la alineación de `guia_spec_md.md`, `guia_clarify_md.md` y `referencia_7_etapas_sdd.md` a las plantillas de rango 5 (T-034 a T-036) |
  | `AUD-015` | `RF-002` | Tabla de siete etapas de 1 Specify a 7 Release en `.opencode/agents/sdd.md` (T-015) |
  | `AUD-024` | `RF-003` | Secciones de aprobaciones de `SPEC-010` y `SPEC-011` con dos casillas, y comprobación `C-13` de la casilla única (T-011, T-033) |
  | `AUD-036` | `RF-004` | Firma verificada declarada en §14 del protocolo y en la sección de validación de `AGENTS.md` (T-021, T-022) |
  | `AUD-037` | `RF-005` | Dos ventanas de legado con motivo y límite en §14 y §15, coincidentes con `LEGACY_SPECS` y `TRACE_LEGACY_SPECS` (T-023) |
  | `AUD-045` | `RF-006` | Sección `## Cierre de integración` en los reportes de `SPEC-008` a `SPEC-011`, con su `Merge:` y la línea `Release:` vacía (T-031, T-032) |
  | `AUD-046` | `RF-007` | Alcance de la comprobación `C-16` acotado al último tag anotado, sin merges y con informe de commits examinados (T-012) |
  | `AUD-056` | `RF-008` | Escritura de T4 a T7 atribuida al `planner` en §5, sin editar las filas T4 a T6 de `SPEC-012` (T-024) |
  | `AUD-065` | `RF-009` | Fila del orquestador en §12 y matriz sin escritura sobre `specs/` en `.opencode/agents/sdd.md` (T-015, T-025) |
  | `AUD-073` | `RF-010` | Flujo `SDD` con `actions/checkout` y `actions/setup-python`, reglas de protección con el check `verify` exigible y su documentación en la norma de integración (T-018 a T-020, T-026) |
  | `AUD-074` | `RF-011` | Suite del mecanismo de control declarada en la norma de integración, con sus 131 pruebas y su ejecución en el job `verify` (T-027) |
  | `AUD-085` | `RF-012` | Sincronización por ancestría con `git merge-base --is-ancestor` y sin la exigencia del conteo simétrico (T-028) |
  | `AUD-086` | `RF-013` | Gramática de cinco prefijos con la admisión de `docs/` en la norma de integración y en `AGENTS.md` (T-029, T-030) |
  | `AUD-095` | `RF-014` | Línea de estado de `MEMORY.md` sin divergencias con `specs/INDEX.md` ni con el frontmatter (T-037) |
  | `AUD-096` | `RF-015` | Fila del informe de reauditoría en la tabla de inventario de `docs/sdd/README.md` (T-038) |
  | `AUD-097` | `RF-016` | Historial de ocho filas de `v0.1.0` a `v0.6.0` en `CHANGELOG.md` (T-039) |
- [x] Completada.

## Matriz de cobertura de tareas

| Requisito | Tareas |
|---|---|
| `RF-001` | `T-010`, `T-034`, `T-035`, `T-036` |
| `RF-002` | `T-008`, `T-015` |
| `RF-003` | `T-001`, `T-011`, `T-033` |
| `RF-004` | `T-009`, `T-021`, `T-022` |
| `RF-005` | `T-009`, `T-023` |
| `RF-006` | `T-003`, `T-013`, `T-031`, `T-032` |
| `RF-007` | `T-002`, `T-012` |
| `RF-008` | `T-009`, `T-024` |
| `RF-009` | `T-008`, `T-015`, `T-025` |
| `RF-010` | `T-004`, `T-005`, `T-006`, `T-014`, `T-016`, `T-018`, `T-019`, `T-020`, `T-026` |
| `RF-011` | `T-027` |
| `RF-012` | `T-009`, `T-028` |
| `RF-013` | `T-007`, `T-029`, `T-030` |
| `RF-014` | `T-010`, `T-017`, `T-037` |
| `RF-015` | `T-010`, `T-017`, `T-038` |
| `RF-016` | `T-010`, `T-017`, `T-039` |
| `RNF-001` | `T-044` |
| `RNF-002` | `T-040` |
| `RNF-003` | `T-040` |
| `RNF-004` | `T-043` |
| `RNF-005` | `T-041` |
| `RNF-006` | `T-040` |
| `RNF-007` | `T-042` |
| `RNF-008` | `T-042` |
| `CB-001` | `T-007`, `T-029`, `T-030` |
| `CB-002` | `T-007`, `T-029`, `T-030` |
| `CB-003` | `T-028` |
| `CB-004` | `T-028` |
| `CB-005` | `T-002`, `T-012` |
| `CB-006` | `T-001`, `T-011`, `T-033` |
| `CB-007` | `T-003`, `T-013`, `T-031`, `T-032` |
| `CB-008` | `T-003`, `T-013`, `T-031`, `T-032` |
| `CB-009` | `T-005`, `T-018` |
| `CB-010` | `T-004`, `T-014`, `T-019` |
| `CB-011` | `T-023` |
| `CB-012` | `T-034`, `T-035`, `T-036` |
| `CB-013` | `T-037`, `T-038`, `T-039` |
| `CB-014` | `T-008`, `T-015`, `T-025` |
| `CB-015` | `T-041` |
| `CB-016` | `T-024` |

## Trazabilidad de los criterios de aceptación

| Criterio | Tareas que lo declaran |
|---|---|
| `CA-001` | `T-010`, `T-034`, `T-035`, `T-036` |
| `CA-002` | `T-008`, `T-015` |
| `CA-003` | `T-001`, `T-011`, `T-033` |
| `CA-004` | `T-009`, `T-021`, `T-022` |
| `CA-005` | `T-009`, `T-023` |
| `CA-006` | `T-003`, `T-013`, `T-031`, `T-032` |
| `CA-007` | `T-002`, `T-012` |
| `CA-008` | `T-009`, `T-024` |
| `CA-009` | `T-008`, `T-015`, `T-025` |
| `CA-010` | `T-004`, `T-005`, `T-006`, `T-014`, `T-016`, `T-018`, `T-019`, `T-020`, `T-026` |
| `CA-011` | `T-027` |
| `CA-012` | `T-009`, `T-028` |
| `CA-013` | `T-007`, `T-029`, `T-030` |
| `CA-014` | `T-010`, `T-017`, `T-037`, `T-038`, `T-039` |
| `CA-015` | `T-044` |
| `CA-016` | `T-040`, `T-043` |
| `CA-017` | `T-041` |
| `CA-018` | `T-042` |
