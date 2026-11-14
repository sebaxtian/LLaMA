# Tareas — SPEC-010

## Regla de ejecución

La Etapa 6 de esta especificación modifica el validador, su suite y dos comandos de OpenCode, y se ejecuta con dos escritores y una revisión:

1. El rol `coder` escribe `tools/sdd/validate.py`, `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/**` y el cierre de cada tarea en `specs/010-mecanismo-control-sdd/tasks.md`.
2. El orquestador redacta `.opencode/commands/sdd-implement.md` y `.opencode/commands/sdd-validate.md` como delegado del propietario, porque la allowlist del `coder` no alcanza `.opencode/`. El propietario revisa el contenido antes de G4. La formalización de la allowlist corresponde al bloque B3 y no se ejecuta en esta feature.
3. Las validaciones que requieren shell las ejecuta la sesión orquestadora y su salida literal se adjunta al reporte que recibe el `planner` para el registro.
4. Una casilla se marca solo cuando la validación de la tarea se cumple. Una validación fallida obliga a corregir el archivo y a repetir la comprobación antes del registro.
5. El `planner` escribe el recuento de `## Progreso`; el `coder` cierra las tareas de su alcance y el orquestador cierra `T-013`.
6. La Etapa 6 no modifica la base normativa, las specs publicadas, `src/` ni `llama.cpp/`. Una nota que el cambio de comando exigiera en `AGENTS.md` o en el protocolo se registra como dependencia y no se ejecuta.
7. Las etiquetas `C-01` a `C-13` identifican las comprobaciones del plan y no pertenecen a los espacios de identificadores del protocolo.

## Referencias

- `spec.md`: `SPEC-010`, versión 0.3.0, estado `planned`, compuerta G1 aprobada por `Agent Sebaxtian` en el commit firmado `f38eb6a` (2026-11-14).
- `clarify.md`: cerrado con `AMB-001` a `AMB-008` resueltos y parches aplicados a `spec.md`.
- `plan.md`: arquitectura del validador por capas, contratos de aprobación y de historial, once decisiones `DEC-001` a `DEC-011`, trece comprobaciones `C-01` a `C-13` y matriz de cobertura de 42 filas.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §5 tabla de transiciones, §6 compuertas, §11 aprobaciones, §13 G5 y G6, §14 contrato del validador.
- Informe de origen: `docs/sdd/auditoria_cumplimiento_sdd.md`, bloque B2.

## Progreso

- Cerradas: 0 de 15 tareas.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_validate.py` | `T-001` a `T-009`, `T-013`, `T-014` | `coder` |
| 2 | `tools/sdd/tests/fixtures/aprobacion/**` y `fixtures/autoridad/**` | `T-001` | `coder` |
| 3 | `tools/sdd/tests/fixtures/g6/**` | `T-002` | `coder` |
| 4 | `tools/sdd/tests/fixtures/cobertura/**` | `T-003` | `coder` |
| 5 | `tools/sdd/tests/fixtures/tareas/**` | `T-004` | `coder` |
| 6 | `tools/sdd/tests/fixtures/transiciones/**` | `T-005` | `coder` |
| 7 | `tools/sdd/tests/fixtures/sucesion/**` | `T-006` | `coder` |
| 8 | `tools/sdd/tests/fixtures/g5/**` | `T-007` | `coder` |
| 9 | `tools/sdd/tests/fixtures/legado/**` | `T-009` | `coder` |
| 10 | `tools/sdd/validate.py` | `T-010`, `T-011`, `T-012` | `coder` |
| 11 | `.opencode/commands/sdd-implement.md` | `T-013` | orquestador (delegado del propietario) |
| 12 | `.opencode/commands/sdd-validate.md` | `T-013` | orquestador (delegado del propietario) |
| 13 | `specs/010-mecanismo-control-sdd/tasks.md` | cierre de cada tarea y `T-015` | `coder` para las casillas y `planner` para el progreso |

`T-008`, `T-014` y `T-015` son tareas de verificación y de cierre: no producen archivos nuevos, salvo la corrección acotada que `T-014` declara si la regresión falla.

## Orden de ejecución y dependencias

- Grupo 1 (pruebas que fallan, por comprobación): `T-001` sin dependencias; `T-002`, `T-003`, `T-004`, `T-005`, `T-006`, `T-007`, `T-008` y `T-009` dependen de `T-001`.
- Grupo 2 (implementación mínima): `T-010` depende de `T-001`; `T-011` depende de `T-003`, `T-004` y `T-005`; `T-012` depende de `T-002`, `T-006`, `T-007`, `T-008` y `T-009`.
- Grupo 3 (comandos y cierre): `T-013` depende de `T-010`, `T-011` y `T-012`; `T-014` depende de `T-013`; `T-015` depende de `T-014`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo.

## Tareas

### T-001: Pruebas de aprobación de G1 y G4 y de autoría por commit firmado

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RF-010`, `RF-020`, `CB-001`, `CB-002`, `CB-003`, `CB-015`.
- **Criterio de aceptación:** `CA-006`, `CA-007`, `CA-008`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/aprobacion/{marcada,sin-marcar,fuera-de-seccion,registro-dual}/spec.md`; `tools/sdd/tests/fixtures/autoridad/{firmado,sin-firma,clave-ajena,merge}/`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k aprobacion` devuelve `OK` con las siete pruebas de la tarea.
  2. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k autoridad` devuelve `OK` con las cuatro pruebas de autoría.
  3. La prueba positiva afirma código 0 y ausencia de hallazgo de aprobación; la negativa afirma código 1 y un hallazgo que nombra `G1`, `G4` o la ubicación de la línea.
  4. La función de Git se inyecta con texto preparado de `git verify-commit` y de `ssh-keygen -lf`; ninguna prueba ejecuta consulta de red ni toca el repositorio.
  5. Los fixtures se construyen en directorio temporal y se eliminan al terminar la prueba.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-002: Pruebas de aprobación de G6 y de release menor

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-009`, `RF-014`, `CB-007`, `CB-013`.
- **Criterio de aceptación:** `CA-009`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/g6/{anotado,tag-ligero,index-divergente,release-menor-sin-auditoria}/`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k g6` devuelve `OK` con las seis pruebas de la tarea.
  2. La fixture `anotado` contiene `CHANGELOG.md` con la entrada del release y su viñeta, `specs/INDEX.md` con la fila en estado `released` y el release, y un repositorio temporal con tag anotado; devuelve código 0.
  3. La fixture `tag-ligero` devuelve código 1 con un mensaje que nombra el objeto ligero; `release-menor-sin-auditoria` devuelve código 1 con un mensaje que nombra el informe de auditoría; `index-divergente` devuelve código 1 con un mensaje que nombra `INDEX`.
  4. La comparación del componente MINOR usa el listado local de tags y no ejecuta `git ls-remote` ni consulta de red.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-003: Pruebas de cobertura como error desde G2 y advertencia antes

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/cobertura/completa/spec.md`; `tools/sdd/tests/fixtures/cobertura/faltante/spec.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k cobertura` devuelve `OK` con las tres pruebas de la tarea.
  2. `completa` con compuerta G2 devuelve código 0 y sin hallazgo de cobertura; `faltante` con compuerta G2 devuelve código 1 y nombra el identificador del requisito sin línea `Cubre:`.
  3. `faltante` con estado `draft` devuelve código 0 y un hallazgo de severidad advertencia por el mismo requisito.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-004: Pruebas de tareas abiertas en la validación agregada

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-012`, `CB-008`.
- **Criterio de aceptación:** `CA-011`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/tareas/{cerradas-released,abiertas-released,abiertas-implementing}/`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k tareas_abiertas` devuelve `OK` con las dos pruebas de la tarea.
  2. `abiertas-released` en ejecución agregada devuelve código 1 y nombra el identificador de la tarea abierta; `cerradas-released` devuelve código 0.
  3. `abiertas-implementing` devuelve código 0 con un hallazgo de severidad advertencia.
  4. La prueba invoca la ejecución agregada sobre un directorio de specs redirigido y no lectura del corpus real.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-005: Pruebas de transición admitida, transición rechazada e historial

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-015`, `RF-016`, `CB-004`, `CB-011`.
- **Criterio de aceptación:** `CA-013`, `CA-014`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/transiciones/{admitida,no-admitida,historial-coherente,historial-sin-fila}/spec.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k transicion` devuelve `OK` con dos pruebas; `-k historial` devuelve `OK` con dos pruebas más.
  2. `admitida` devuelve código 0; `no-admitida` devuelve código 1 con un mensaje que nombra el par origen y destino rechazado.
  3. `historial-sin-fila` devuelve código 1 con un mensaje que nombra la subsección y el estado sin fila; `historial-coherente` devuelve código 0.
  4. Una prueba contrasta la constante `TRANSITIONS` del validador con la tabla de §5 del protocolo y devuelve `OK` solo si los diez pares coinciden.
  5. La prueba de compuerta desde un estado de origen distinto al exigido afirma código 1 con el mensaje de estado de origen.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-006: Pruebas de sucesión recíproca

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-017`, `CB-005`, `CB-006`.
- **Criterio de aceptación:** `CA-015`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/sucesion/{reciproca,asimetrica,sin-carpeta,sin-estado}/`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k sucesion` devuelve `OK` con las dos pruebas de la tarea.
  2. `reciproca` devuelve código 0; `asimetrica` devuelve código 1 con un mensaje que nombra `supersedes` y `superseded_by`.
  3. `sin-carpeta` devuelve código 1 con un mensaje que nombra la carpeta ausente; `sin-estado` devuelve código 1 con un mensaje que nombra el estado `superseded`.
  4. Cada fixture es un par de directorios de spec en un directorio temporal, con frontmatter completo.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-007: Pruebas de G5 sin consulta de red

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-013`, `CB-012`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/g5/{merge-dos-padres,rama-presente,rama-remota-seguimiento}/`.
- **Estimación:** 25 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k g5` devuelve `OK` con las tres pruebas de la tarea.
  2. `merge-dos-padres` devuelve código 0 con la integración, el registro de validación posterior y la rama ausente.
  3. `rama-presente` devuelve código 1 con un mensaje que nombra la rama local; `rama-remota-seguimiento` devuelve código 1 con un mensaje que nombra la referencia remota de seguimiento.
  4. La ejecución de la prueba no invoca `git ls-remote` ni ninguna consulta de red, y la función de Git se inyecta con la lista de ramas preparada.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-008: Pruebas de alcance impreso y de códigos de salida

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-018`, `RNF-004`.
- **Criterio de aceptación:** `CA-016`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/valid/001-demo/spec.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k alcance` devuelve `OK` con las dos pruebas de la tarea.
  2. La ejecución agregada sobre la fixture imprime un bloque de comprobaciones ejecutadas y un bloque de comprobaciones no verificadas, y la prueba afirma la presencia de los dos rótulos.
  3. La prueba negativa afirma que una salida sin el bloque de no verificadas no se acepta como conforme.
  4. Cada hallazgo impreso ocupa una línea con severidad, ruta y comprobación, y la prueba afirma el formato.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-009: Pruebas de la ventana de legado

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `CB-014`, `RNF-006`.
- **Criterio de aceptación:** `CA-020`.
- **Archivos:** `tools/sdd/tests/test_validate.py`; `tools/sdd/tests/fixtures/legado/{spec-001-sin-historial,spec-010-sin-aprobacion}/`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k legado` devuelve `OK` con las dos pruebas de la tarea.
  2. `spec-001-sin-historial` devuelve código 0 con un hallazgo de severidad advertencia que nombra la cláusula de legado.
  3. La misma condición sobre un identificador `SPEC-010` devuelve código 1 y un hallazgo de severidad error.
  4. El identificador se inyecta en el nombre del directorio temporal, de modo que la prueba no depende de las specs publicadas del repositorio.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-010: Implementación del validador para aprobaciones y ubicación única

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-006`, `RF-007`, `RF-008`, `RF-010`, `RF-020`, `CB-001`, `CB-002`, `CB-003`, `CB-015`.
- **Criterio de aceptación:** `CA-006`, `CA-007`, `CA-008`.
- **Archivos:** `tools/sdd/validate.py`; `tools/sdd/tests/test_validate.py`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k aprobacion` devuelve `OK` y `-k autoridad` devuelve `OK`: las pruebas de `T-001` pasan de rojo a verde.
  2. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py"` conserva las 47 pruebas vigentes en verde.
  3. `python tools\sdd\validate.py --spec SPEC-010 --gate G1` devuelve código 0: la línea de G1 existe, está marcada y su commit `f38eb6a` verifica contra `docs/sdd/firmantes_autorizados`.
  4. La función `check_approval` no escribe archivos y la comprobación de firma usa `git log --no-merges -S`, `git show` y `git verify-commit --raw`, sin consulta de red.
  5. Una ejecución con la lista de firmantes ausente produce el estado `NO VERIFICABLE` y no declara la compuerta aprobada.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-011: Implementación de cobertura, tareas abiertas, transiciones e historial

- **Dependencias:** `T-003`, `T-004`, `T-005`.
- **Requisitos cubiertos:** `RF-011`, `RF-012`, `RF-015`, `RF-016`, `CB-004`, `CB-008`, `CB-011`.
- **Criterio de aceptación:** `CA-010`, `CA-011`, `CA-013`, `CA-014`.
- **Archivos:** `tools/sdd/validate.py`; `tools/sdd/tests/test_validate.py`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k cobertura` devuelve `OK`; `-k tareas_abiertas` devuelve `OK`; `-k transicion` devuelve `OK`; `-k historial` devuelve `OK`.
  2. `python tools\sdd\validate.py --spec SPEC-010 --gate G2` devuelve código 0 con la cobertura completa y el historial coherente con `status`.
  3. `python tools\sdd\validate.py --all` devuelve código 0: ninguna spec publicada pasa a error por las comprobaciones C-04, C-05, C-06 y C-07.
  4. La constante `TRANSITIONS` declara los diez pares de la tabla de §5 del protocolo y el historial se analiza por nombre de columna.
  5. La comprobación no escribe archivos y no modifica el campo `status` de ninguna spec.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-012: Implementación de G5, G6, sucesión, alcance y legado

- **Dependencias:** `T-002`, `T-006`, `T-007`, `T-008`, `T-009`.
- **Requisitos cubiertos:** `RF-009`, `RF-013`, `RF-014`, `RF-017`, `RF-018`, `RNF-004`, `RNF-006`, `CB-005`, `CB-006`, `CB-007`, `CB-012`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-012`, `CA-015`, `CA-016`, `CA-020`.
- **Archivos:** `tools/sdd/validate.py`; `tools/sdd/tests/test_validate.py`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k g5` devuelve `OK`; `-k g6` devuelve `OK`; `-k sucesion` devuelve `OK`; `-k alcance` devuelve `OK`; `-k legado` devuelve `OK`.
  2. `python tools\sdd\validate.py --all` devuelve código 0 e imprime el bloque de comprobaciones ejecutadas y el de comprobaciones no verificadas.
  3. La comprobación de G5 no invoca `git ls-remote` y la de G6 no consulta el remoto; la revisión del código confirma que las dos usan solo el historial local.
  4. `python tools\sdd\validate.py --spec SPEC-009 --gate G6` no devuelve código 1 por una comprobación nueva: la spec publicada queda amparada por la cláusula de legado.
  5. La ejecución agregada conserva el código 0 y el contrato de códigos de salida 0, 1 y 2.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-013: Comandos de implementación y de validación con separación de roles

- **Dependencias:** `T-010`, `T-011`, `T-012`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-004`, `RF-005`, `RF-006`, `RF-021`, `CB-009`, `CB-010`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-003`, `CA-004`, `CA-005`.
- **Archivos:** `.opencode/commands/sdd-implement.md`; `.opencode/commands/sdd-validate.md`; `tools/sdd/tests/test_validate.py`.
- **Estimación:** 25 min.
- **Validación:**
  1. `Select-String -Path .opencode\commands\sdd-implement.md -Pattern 'G2'` devuelve al menos una coincidencia y `-Pattern 'G4'` devuelve cero: la entrada exige G2 y no G4.
  2. El texto de `sdd-implement.md` declara la escritura de `implementing` en el inicio, la de `implemented` en el cierre y una sola evaluación de G3 fuera del bucle de tareas.
  3. `Select-String -Path .opencode\commands\sdd-validate.md -Pattern 'gate G4'` devuelve cero y el texto declara que el orquestador evalúa G4 después de la firma y escribe `validated`.
  4. `python -m unittest discover -s tools/sdd/tests -p "test_validate.py" -k comando` devuelve `OK` con las dos pruebas de texto del comando.
  5. La comprobación no ejecuta el ciclo completo: se limita a la lectura del comando y a las dos pruebas de texto.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-014: Regresión completa de la suite y de la ejecución agregada

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-019`, `RNF-001`, `RNF-002`, `RNF-003`, `RNF-005`.
- **Criterio de aceptación:** `CA-017`, `CA-018`, `CA-019`.
- **Archivos:** ninguno nuevo; corrección acotada a `tools/sdd/validate.py` y a `tools/sdd/tests/test_validate.py` si la regresión falla.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m unittest discover -s tools/sdd/tests -p "test_*.py"` devuelve `Ran 86 tests` y `OK`, con las 47 pruebas vigentes y las 39 nuevas en verde.
  2. `python tools\sdd\validate.py --all` devuelve código 0 y no modifica archivos: `git status --short` conserva el mismo listado antes y después.
  3. Dos ejecuciones consecutivas devuelven el mismo veredicto y el mismo código de salida.
  4. La ejecución agregada completa en 60 segundos o menos; el tiempo medido se transcribe en la evidencia.
  5. La revisión de importaciones confirma biblioteca estándar y ausencia de acceso a red.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-015: Cierre de alcance y traspaso al `reviewer`

- **Dependencias:** `T-014`.
- **Requisitos cubiertos:** `RF-019`, `RNF-002`.
- **Criterio de aceptación:** `CA-016`, `CA-017`.
- **Archivos:** `specs/010-mecanismo-control-sdd/tasks.md`.
- **Estimación:** 15 min.
- **Validación:**
  1. `git diff --check` no devuelve salida y `git status --short` enumera solo las rutas declaradas en `## Archivos de la etapa y escritor`.
  2. `python tools\sdd\validate.py --spec SPEC-010 --gate G3` devuelve código 0 con las quince casillas `Completada` marcadas.
  3. La matriz de cobertura de `plan.md` conserva 42 filas y cada `RF`, `RNF` y `CB` figura en el campo `Requisitos cubiertos` de al menos una tarea.
  4. El recuento de `## Progreso` declara 15 de 15 tareas cerradas y el traspaso al `reviewer` queda escrito con la ruta de la suite, el comando de la ejecución agregada y su código de salida.
- **Evidencia:** pendiente de la salida de la validación al cerrar la tarea.
- [ ] Completada.
