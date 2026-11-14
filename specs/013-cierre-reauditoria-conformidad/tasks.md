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

- Cerradas: 0 de 44 tareas.

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
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions.TestDocumentacionOperativa -q` con el resultado de los siete nombres de la tabla del plan.
- [ ] Completada.

### T-008: Pruebas de la matriz de agentes y de las etapas del orquestador

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-002`, `RF-009`, `CB-014`.
- **Criterio de aceptación:** `CA-002`, `CA-009`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** caso positivo `test_tabla_de_etapas_del_orquestador`: la tabla de `.opencode/agents/sdd.md` declara siete etapas numeradas de 1 Specify a 7 Release, y `test_escritura_del_coder` y `test_escritura_del_documenter` admiten `.github/**`, `MEMORY.md` y `CHANGELOG.md`; caso negativo `test_escritura_del_orquestador`: un rol sintético con una concesión de escritura sobre `specs/**` produce fallo con la ruta concedida, y la matriz real devuelve 0 atribuciones sobre `specs/`; las cuatro se escriben en rojo antes de `T-015`.
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` con las cuatro pruebas y el recuento de rutas denegadas.
- [ ] Completada.

### T-009: Pruebas de los documentos normativos corregidos

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-004`, `RF-005`, `RF-008`, `RF-012`.
- **Criterio de aceptación:** `CA-004`, `CA-005`, `CA-008`, `CA-012`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** casos positivos `test_contrato_de_firma_verificada`, `test_ventanas_de_legado`, `test_tabla_de_escritura_de_estados` y `test_sincronizacion_por_ancestria`, que verifican la declaración de la firma verificada, las dos ventanas con motivo y límite, la escritura de T4 a T7 por el `planner` y la ancestría sin conteo; caso negativo: cada prueba falla sobre una copia sintética que conserva la afirmación anterior, esto es, la firma no verificada, la ventana sin motivo, la atribución al orquestador y la exigencia de la salida `0 0`; las ocho comprobaciones se escriben en rojo antes de `T-021`.
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions -q` con las cuatro parejas y el texto de cada caso negativo.
- [ ] Completada.

### T-010: Pruebas de los documentos sin rango

- **Dependencias:** `T-009`.
- **Requisitos cubiertos:** `RF-001`, `RF-014`, `RF-015`, `RF-016`.
- **Criterio de aceptación:** `CA-001`, `CA-014`.
- **Archivos:** `tools/sdd/tests/test_agent_permissions.py`.
- **Estimación:** 30 min.
- **Validación:** casos positivos `test_guias_del_corpus`, `test_consistencia_documental`, `test_inventario_del_corpus` y `test_historial_de_releases`, que verifican el encabezado de cada guía con carácter y rango, la coincidencia de `MEMORY.md` con `specs/INDEX.md` y con el frontmatter, la fila del informe de reauditoría y las ocho filas del historial; caso negativo: cada prueba falla sobre una copia sintética con una guía sin rango, un estado divergente, un archivo sin fila y un release sin fila, e informa el documento y el valor en conflicto; las ocho comprobaciones se escriben en rojo antes de `T-034`.
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions -q` con las cuatro parejas y el recuento de divergencias detectadas en cada caso negativo.
- [ ] Completada.

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
- **Evidencia:** Se transcribe al cerrar: bloque de alcance de `python tools\sdd\validate.py --all` con el punto de corte, el recuento de commits examinados y el código de salida.
- [ ] Completada.

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
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` y recuento de rutas denegadas del rol orquestador.
- [ ] Completada.

### T-016: Escritura del `coder` sobre `.github/`

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `.opencode/agents/coder.md`.
- **Estimación:** 15 min.
- **Validación:** la matriz del `coder` concede `edit .github/**` y conserva la denegación explícita sobre `specs/`, `docs/`, `.opencode/` y los documentos de raíz; `test_escritura_del_coder` en verde.
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` con la prueba del `coder` en verde.
- [ ] Completada.

### T-017: Escritura del `documenter` sobre los documentos de raíz

- **Dependencias:** `T-016`.
- **Requisitos cubiertos:** `RF-014`, `RF-015`, `RF-016`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `.opencode/agents/documenter.md`.
- **Estimación:** 15 min.
- **Validación:** la matriz del `documenter` concede `edit MEMORY.md` y `edit CHANGELOG.md` y conserva la denegación explícita sobre `specs/`, `src/`, `tools/`, `.opencode/` y `.github/`; el cuerpo del rol declara la delegación del propietario para los documentos de raíz; `test_escritura_del_documenter` en verde.
- **Evidencia:** Se transcribe al cerrar: salida de `python -m unittest tools.sdd.tests.test_agent_permissions.TestMatrizDePermisos -q` con la prueba del `documenter` en verde.
- [ ] Completada.

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
- **Evidencia:** Se transcribe al cerrar: texto de las dos listas de §14 y salida de la prueba que contrasta la afirmación.
- [ ] Completada.

### T-022: Declaración de la firma verificada en la norma operativa

- **Dependencias:** `T-021`.
- **Requisitos cubiertos:** `RF-004`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `AGENTS.md`.
- **Estimación:** 15 min.
- **Validación:** la sección de validación declara que el validador verifica la firma del commit de aprobación y la pertenencia de la clave firmante, y no conserva la afirmación que declara esas verificaciones no realizadas; el documento conserva entre 30 y 70 líneas útiles y sus seis roles.
- **Evidencia:** Se transcribe al cerrar: párrafo corregido de la sección de validación y recuento de líneas útiles del archivo.
- [ ] Completada.

### T-023: Declaración de las dos ventanas de legado

- **Dependencias:** `T-022`.
- **Requisitos cubiertos:** `RF-005`, `CB-011`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §14 y §15 declaran la ventana estructural de `SPEC-001` a `SPEC-009` para C-01 a C-13 y la ventana de trazabilidad de `SPEC-008` a `SPEC-011` para C-14 a C-18, cada una con su motivo y su límite, y una spec fuera de su ventana produce error sin degradación; `test_ventanas_de_legado` en verde y coincidencia fila por fila con las constantes del validador.
- **Evidencia:** Se transcribe al cerrar: tabla de las dos ventanas del protocolo y salida de la prueba que la contrasta con `LEGACY_SPECS` y `TRACE_LEGACY_SPECS`.
- [ ] Completada.

### T-024: Atribución de la escritura de T4 a T7

- **Dependencias:** `T-023`.
- **Requisitos cubiertos:** `RF-008`, `CB-016`.
- **Criterio de aceptación:** `CA-008`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** §5 atribuye al `planner` la escritura de T4, T5, T6 y T7 sobre la verificación registrada por el orquestador e informa la ausencia de esa verificación como impedimento de la transición; las filas T4 a T6 del historial de `SPEC-012` no se editan y su estado vigente no cambia; `test_tabla_de_escritura_de_estados` en verde.
- **Evidencia:** Se transcribe al cerrar: párrafo de escritura de estados de §5 y salida de `git diff --numstat` de `specs/012-trazabilidad-profunda-sdd/spec.md` con 0 líneas modificadas.
- [ ] Completada.

### T-025: Autoridad del orquestador sin escritura de artefactos

- **Dependencias:** `T-024`.
- **Requisitos cubiertos:** `RF-009`, `CB-014`.
- **Criterio de aceptación:** `CA-009`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §12 declara que el orquestador verifica compuertas, registra resultados, ejecuta el validador y `git add` y `git commit` de los artefactos de control, no redacta artefacto alguno y conserva la prohibición de escribir la sección de aprobaciones; el número de atribuciones de escritura sobre `specs/` es 0 y la contradicción con el cuerpo del rol queda en 0; la prueba de la matriz de agentes en verde.
- **Evidencia:** Se transcribe al cerrar: fila del orquestador en la tabla de §12 y salida de la prueba de escritura del orquestador con 0 rutas concedidas bajo `specs/`.
- [ ] Completada.

### T-026: Exigibilidad del check `verify` en la norma de integración

- **Dependencias:** `T-025`.
- **Requisitos cubiertos:** `RF-010`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 20 min.
- **Validación:** la sección de protección declara exigible el check `verify` del flujo `SDD` en `main` y en `dev`, cita `configure_branch_protection.py` y `verify_branch_protection.py`, y registra que la ausencia del check exigible bloquea G5.
- **Evidencia:** Se transcribe al cerrar: párrafo de exigibilidad del check y su concordancia con el contexto declarado en los dos archivos de reglas.
- [ ] Completada.

### T-027: Suite del mecanismo en la norma de integración

- **Dependencias:** `T-026`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-011`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 15 min.
- **Validación:** la afirmación sobre la ausencia de suite automatizada para la raíz queda sustituida por la declaración de la suite del mecanismo de control, sus 131 pruebas y su ejecución en el job `verify`; el número de afirmaciones que niegan su existencia es 0; `test_documentacion_operativa` en verde.
- **Evidencia:** Se transcribe al cerrar: párrafo corregido, búsqueda del texto anterior con 0 coincidencias y salida de la prueba documental.
- [ ] Completada.

### T-028: Sincronización previa al release por ancestría

- **Dependencias:** `T-027`.
- **Requisitos cubiertos:** `RF-012`, `CB-003`, `CB-004`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 30 min.
- **Validación:** la sincronización se expresa con `git merge-base --is-ancestor main dev` y con `git merge-base --is-ancestor vX.Y.Z^{commit} main`; el conteo simétrico y la exigencia de la salida `0 0` quedan retirados; el estado `48 0` de `dev` respecto de `main` no se trata como bloqueo; la falta de ancestría detiene el empaquetado y un tag no alcanzable detiene el release; `test_sincronizacion_por_ancestria` en verde.
- **Evidencia:** Se transcribe al cerrar: bloque de sincronización corregido, búsqueda de `rev-list --left-right` con 0 coincidencias y salida de las dos comprobaciones de ancestría sobre el historial local.
- [ ] Completada.

### T-029: Gramática de cinco prefijos en la norma de integración

- **Dependencias:** `T-028`.
- **Requisitos cubiertos:** `RF-013`, `CB-001`, `CB-002`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** la expresión declarada es `^(feat|fix|hotfix|docs|release)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$`; la lista admitida es de cinco prefijos; `docs/` se admite para cambios exclusivamente documentales con la misma validación y la misma longitud; un prefijo fuera de la lista se rechaza; las pruebas de `T-007` en verde.
- **Evidencia:** Se transcribe al cerrar: bloque de gramática corregido, la tabla de siete nombres con su resultado y salida de la prueba documental.
- [ ] Completada.

### T-030: Gramática de cinco prefijos en la norma operativa

- **Dependencias:** `T-029`.
- **Requisitos cubiertos:** `RF-013`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `AGENTS.md`.
- **Estimación:** 15 min.
- **Validación:** la sección de Git declara las ramas de trabajo `feat/*`, `fix/*`, `hotfix/*` y `docs/*` junto con las ramas de empaquetado `release/vX-Y-Z`, en minúsculas, números y guiones; el número de prefijos admitidos es 5 y la norma no conserva una lista de tres prefijos de trabajo.
- **Evidencia:** Se transcribe al cerrar: viñeta corregida de la sección de Git y recuento de prefijos declarados.
- [ ] Completada.

### T-031: Cierre de integración de `SPEC-008` y `SPEC-009`

- **Dependencias:** `T-030`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/008-auditoria-cumplimiento-sdd/validation_report.md`, `specs/009-base-normativa-sdd/validation_report.md`.
- **Estimación:** 20 min.
- **Validación:** cada reporte declara al final la sección `## Cierre de integración` con `Merge: 49caac9` para `SPEC-008` y `Merge: 09eaf34` para `SPEC-009`, y con la línea `Release:` vacía; la matriz y el dictamen quedan sin alteración; `python tools\sdd\validate.py --spec SPEC-008` y `--spec SPEC-009` no registran hallazgo de `C-17`.
- **Evidencia:** Se transcribe al cerrar: sección añadida de los dos reportes, salida de `git diff --numstat` con solo líneas añadidas y salida de las dos validaciones por spec.
- [ ] Completada.

### T-032: Cierre de integración de `SPEC-010` y `SPEC-011`

- **Dependencias:** `T-031`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/010-mecanismo-control-sdd/validation_report.md`, `specs/011-practica-operativa-sdd/validation_report.md`.
- **Estimación:** 20 min.
- **Validación:** cada reporte declara al final la sección `## Cierre de integración` con `Merge: 94c2ea1` para `SPEC-010` y `Merge: 9df8446` para `SPEC-011`, y con la línea `Release:` vacía; la matriz y el dictamen quedan sin alteración; las cuatro specs de `SPEC-008` a `SPEC-011` conservan el estado `validated`.
- **Evidencia:** Se transcribe al cerrar: sección añadida de los dos reportes, salida de `git diff --numstat` con solo líneas añadidas y estados de las cuatro specs en `specs/INDEX.md`.
- [ ] Completada.

### T-033: Retirada de las casillas residuales de G4

- **Dependencias:** `T-032`.
- **Requisitos cubiertos:** `RF-003`, `CB-006`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `specs/010-mecanismo-control-sdd/spec.md`, `specs/011-practica-operativa-sdd/spec.md`.
- **Estimación:** 20 min.
- **Validación:** cada sección de aprobaciones conserva dos casillas, G1 y G4, y ninguna más; la tercera casilla con el marcador de plantilla queda retirada; `python tools\sdd\validate.py --spec SPEC-010` y `--spec SPEC-011` no registran hallazgo de `C-13`; el cambio lo publica el propietario en un commit firmado y el agente solo prepara el diff, sin firmar, sin confirmar y sin marcar la casilla de esta tarea.
- **Evidencia:** Se transcribe al cerrar: diff preparado de las dos secciones, identificador del commit firmado del propietario y salida de las dos validaciones por spec sin hallazgo de `C-13`.
- [ ] Completada.

### T-034: Encabezado de carácter y rango en las guías del corpus

- **Dependencias:** `T-033`.
- **Requisitos cubiertos:** `RF-001`, `CB-012`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/guia_*.md`, que alcanza las doce guías del corpus: `guia_maestra_sdd.md`, `guia_constitution_md.md`, `guia_agents_md.md`, la guía de notación EARS, `guia_spec_md.md`, `guia_clarify_md.md`, `guia_plan_md.md`, `guia_tasks_md.md`, `guia_fase_implement_tdd.md`, `guia_subagentes_opencode_sdd.md`, `guia_skills_agentes_sdd.md` y `guia_servidores_mcp.md`.
- **Estimación:** 30 min.
- **Validación:** las doce guías declaran en el encabezado su carácter no normativo y el rango «Sin rango» con la remisión a `PROTOCOLO_OPERATIVO.md`; una guía que ya cumple la declaración no se modifica y su conformidad previa se registra; `test_guias_del_corpus` en verde con 0 guías sin declaración.
- **Evidencia:** Se transcribe al cerrar: recuento de guías con encabezado conforme, relación de las guías no modificadas por conformidad previa y salida de la prueba documental.
- [ ] Completada.

### T-035: Encabezado de carácter y rango en las referencias del corpus

- **Dependencias:** `T-034`.
- **Requisitos cubiertos:** `RF-001`, `CB-012`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/referencia_7_etapas_sdd.md`, `docs/sdd/referencia_ciclo_vida_sdd_puro.md`, `docs/sdd/compendio_sdd.md`.
- **Estimación:** 15 min.
- **Validación:** las tres referencias declaran en el encabezado su carácter no normativo y el rango «Sin rango»; una referencia que ya cumple la declaración no se modifica y su conformidad previa se registra; el número de archivos del corpus sin declaración de rango en el encabezado es 0.
- **Evidencia:** Se transcribe al cerrar: encabezado resultante de cada referencia y recuento de archivos del corpus con declaración vigente.
- [ ] Completada.

### T-036: Correcciones de las tres guías señaladas por la reauditoría

- **Dependencias:** `T-035`.
- **Requisitos cubiertos:** `RF-001`, `CB-012`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/guia_spec_md.md`, `docs/sdd/guia_clarify_md.md`, `docs/sdd/referencia_7_etapas_sdd.md`.
- **Estimación:** 25 min.
- **Validación:** la denominación «Definition of Done» queda sustituida por «criterio de aceptación» en las tres apariciones de `guia_spec_md.md`; el identificador fuera de formato de `guia_clarify_md.md` queda sustituido por `CB-001`; el título del criterio de `referencia_7_etapas_sdd.md` coincide con la plantilla de rango 5; el número de identificadores de ejemplo con menos de tres dígitos es 0.
- **Evidencia:** Se transcribe al cerrar: las cinco sustituciones aplicadas, búsqueda de «Definition of Done» con 0 coincidencias y salida de la prueba documental.
- [ ] Completada.

### T-037: Estado de las specs en el contexto operativo

- **Dependencias:** `T-036`.
- **Requisitos cubiertos:** `RF-014`, `CB-013`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `MEMORY.md`.
- **Estimación:** 15 min.
- **Validación:** la línea de estado declara `SPEC-001` a `SPEC-007` publicadas, `SPEC-008` a `SPEC-012` validadas y `SPEC-013` con el estado de su frontmatter; el número de divergencias con `specs/INDEX.md` y con el frontmatter de cada spec es 0; `test_consistencia_documental` en verde.
- **Evidencia:** Se transcribe al cerrar: línea de estado corregida y salida de la prueba que contrasta los tres soportes.
- [ ] Completada.

### T-038: Fila del informe de reauditoría en el índice del corpus

- **Dependencias:** `T-037`.
- **Requisitos cubiertos:** `RF-015`, `CB-013`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `docs/sdd/README.md`.
- **Estimación:** 15 min.
- **Validación:** la tabla de inventario registra la fila del informe `docs/sdd/auditoria_cierre_v0_7_0.md` con su ruta, su carácter de informe de auditoría, su orden de lectura y el rango «Sin rango»; el número de archivos del corpus sin fila es 0; `test_inventario_del_corpus` en verde.
- **Evidencia:** Se transcribe al cerrar: fila añadida, recuento de filas de datos y salida de la prueba de inventario.
- [ ] Completada.

### T-039: Historial de releases del registro de cambios

- **Dependencias:** `T-038`.
- **Requisitos cubiertos:** `RF-016`, `CB-013`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 25 min.
- **Validación:** el historial declara ocho filas con versión, fecha y tag de `v0.1.0` a `v0.6.0` en orden ascendente, hasta el release anterior a `v0.7.0`; el número de releases publicados sin fila es 0; la entrada de `v0.7.0` permanece en `Unreleased`; `test_historial_de_releases` en verde.
- **Evidencia:** Se transcribe al cerrar: tabla del historial con las ocho filas y salida de la prueba que la contrasta con los ocho tags anotados.
- [ ] Completada.

### T-040: Regresión de la suite y del corpus

- **Dependencias:** `T-039`.
- **Requisitos cubiertos:** `RNF-002`, `RNF-003`, `RNF-006`.
- **Criterio de aceptación:** `CA-016`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` devuelve las 131 pruebas vigentes más las nuevas en verde con código 0; `python tools\sdd\validate.py --all` devuelve código 0 en 300 segundos o menos; dos ejecuciones consecutivas sobre el mismo commit presentan 0 diferencias en el conjunto de hallazgos; la ejecución no accede a red, servicio externo ni credencial y conserva los códigos de salida 0, 1 y 2.
- **Evidencia:** Se transcribe al cerrar: salida de la suite con el recuento y el tiempo, salida de la validación agregada con el código de salida, comparación de las dos ejecuciones y tiempo medido del job `verify`.
- [ ] Completada.

### T-041: Contraste de las cinco specs publicadas

- **Dependencias:** `T-040`.
- **Requisitos cubiertos:** `RNF-005`, `CB-015`.
- **Criterio de aceptación:** `CA-017`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** `git diff` de `SPEC-008` a `SPEC-012` contra su versión anterior muestra como diferencia solo la sección de cierre añadida y las dos casillas retiradas; el 100 % de sus requisitos, criterios de aceptación y estados queda sin cambios; una observación que exija cambiar un requisito publicado queda registrada como detenida y tramitada por una spec nueva.
- **Evidencia:** Se transcribe al cerrar: salida de `git diff --numstat` de las cinco specs, relación de las líneas modificadas y recuento de requisitos, criterios y estados alterados igual a 0.
- [ ] Completada.

### T-042: Consistencia de los documentos de rango 2, rango 3 y rango 4

- **Dependencias:** `T-041`.
- **Requisitos cubiertos:** `RNF-007`, `RNF-008`.
- **Criterio de aceptación:** `CA-018`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** el contraste de las afirmaciones corregidas en `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `docs/Flujo_de_Trabajo_Git.md` arroja 0 contradicciones, y el 100 % de los documentos corregidos conserva en su encabezado su rango y su carácter; las pruebas de `T-009` y `T-010` en verde.
- **Evidencia:** Se transcribe al cerrar: relación de afirmaciones contrastadas con su resultado, recuento de contradicciones igual a 0 y encabezado de cada documento corregido.
- [ ] Completada.

### T-043: Pareja positiva y negativa de cada comprobación nueva

- **Dependencias:** `T-042`.
- **Requisitos cubiertos:** `RNF-004`.
- **Criterio de aceptación:** `CA-016`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** cada una de las cuatro comprobaciones corregidas y de las comprobaciones documentales nuevas declara al menos una prueba positiva y una negativa en la suite del mecanismo de control; el recuento de comprobaciones sin pareja es 0 y el de pruebas nuevas coincide con el declarado en `T-001` a `T-010`.
- **Evidencia:** Se transcribe al cerrar: tabla de comprobación, prueba positiva y prueba negativa, más el recuento de pruebas nuevas de la suite.
- [ ] Completada.

### T-044: Cierre del alcance y traspaso a la validación

- **Dependencias:** `T-043`.
- **Requisitos cubiertos:** `RNF-001`.
- **Criterio de aceptación:** `CA-015`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/tasks.md`.
- **Estimación:** 25 min.
- **Validación:** las cuarenta y cuatro tareas figuran cerradas con su evidencia transcrita; `python tools\sdd\validate.py --spec SPEC-013 --gate G3` devuelve código 0; el paquete de traspaso reúne los cuatro artefactos de la spec, las dieciséis observaciones con su artefacto de cierre y la salida agregada, y no declara compuerta alguna.
- **Evidencia:** Se transcribe al cerrar: recuento de tareas cerradas, salida de `python tools\sdd\validate.py --spec SPEC-013 --gate G3` con su código y relación de las dieciséis observaciones con el artefacto que las cierra.
- [ ] Completada.

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
