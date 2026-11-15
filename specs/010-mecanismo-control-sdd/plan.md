# Plan técnico — SPEC-010

## Referencias

- `spec.md`: `SPEC-010`, versión 0.2.0, estado `clarified`, compuerta G1 aprobada por `Agent Sebaxtian` en el commit firmado `f38eb6a` (2026-11-14).
- `clarify.md`: `SPEC-010`, cerrado con `AMB-001` a `AMB-008` resueltos y once parches aplicados a `spec.md`.
- `docs/constitution.md`: norma suprema de rango 1; fija especificación previa, determinismo, trazabilidad, aprobación por commit firmado y menor privilegio.
- `AGENTS.md`: norma operativa de rango 2; fija los comandos del validador y la validación previa a la integración.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma ejecutable de rango 3; §5 fija la tabla de transiciones, §6 las seis compuertas, §11 el formato de aprobación, §13 G5 y G6, y §14 el contrato del validador.
- `docs/Flujo_de_Trabajo_Git.md`: procedimiento de integración y release de rango 4; fija `merge --no-ff`, la eliminación de la rama y las tres verificaciones del tag.
- `docs/sdd/plantillas/plan.md`: plantilla aplicada al presente documento.
- `docs/sdd/auditoria_cumplimiento_sdd.md`: informe de auditoría `SPEC-008`; su bloque B2 origina los dieciséis hallazgos que la spec resuelve.
- `tools/sdd/validate.py`: validador vigente, de biblioteca estándar y un solo archivo.
- `tools/sdd/tests/test_validate.py`: suite vigente con 47 pruebas en verde.
- `.opencode/commands/sdd-implement.md` y `.opencode/commands/sdd-validate.md`: comandos vigentes con las condiciones de entrada y la circularidad que la spec corrige.

## Naturaleza del entregable

La feature produce código ejecutable y dos comandos de texto:

| Componente | Naturaleza | Operación |
|---|---|---|
| `tools/sdd/validate.py` | Código Python de biblioteca estándar | Ampliación con trece comprobaciones nuevas y un catálogo de alcance |
| `tools/sdd/tests/` | Suite `unittest` y fixtures temporales | Pruebas positivas y negativas por comprobación |
| `.opencode/commands/sdd-implement.md` | Comando de texto con precondición y escritura de estados | Reescritura de la condición de entrada y del cierre de etapa |
| `.opencode/commands/sdd-validate.md` | Comando de texto con separación de roles | Reescritura del orden reporte, evaluación y estado |

No se produce cambio alguno en la base normativa. Una nota que el cambio de comando exigiera en `AGENTS.md` o en el protocolo se registra como dependencia y no se ejecuta, porque la base v2 está cerrada.

## Arquitectura

El validador permanece como un único módulo sin dependencias externas. La ampliación se organiza por responsabilidad y cada comprobación recibe de la capa de proceso únicamente texto ya leído y el resultado de las consultas Git que necesita. Esa separación permite probar la lógica sin repositorio, sin claves y sin red.

### Capas

| Capa | Responsabilidad | No hace |
|---|---|---|
| Entrada | Analiza argumentos, resuelve rutas y códigos de salida 0, 1 y 2 | No decide compuertas |
| Lectura | Lee `spec.md`, `clarify.md`, `plan.md`, `tasks.md`, `validation_report.md`, `CHANGELOG.md` y `specs/INDEX.md` | No escribe archivos |
| Git | Ejecuta las consultas de localización, firma, fusión y tags mediante una función inyectable | No consulta el remoto |
| Comprobación | Funciones puras por comprobación que devuelven hallazgos con severidad | No imprime |
| Salida | Imprime un hallazgo por línea y las dos listas de alcance | No modifica el veredicto |

### Componentes del validador

| Componente | Función | Comprobaciones |
|---|---|---|
| Catálogo de compuertas | Constantes `GATE_STATES`, `TRANSITIONS` y `LEGACY_SPECS` | C-06, C-12 |
| Aprobaciones | `find_approval(gate, text, section)`, `check_approval(spec, gate)` | C-01, C-02, C-13 |
| Autoría | `select_approval_commit(ruta, aguja, seccion)`, `verify_signature(sha)`, `authorized_fingerprints()` | C-03 |
| Cobertura | `coverage_gaps(body)` con severidad derivada de la etapa | C-04 |
| Tareas | `incomplete_tasks(text)` con severidad derivada del estado | C-05 |
| Transiciones | `parse_transition_history(text)` y `check_transitions(status, filas)` | C-06, C-07 |
| Sucesión | `check_supersession(spec_dir, indice)` | C-08 |
| G5 | `check_g5(spec, repo)` | C-09 |
| G6 | `check_g6(spec, repo, changelog, indice)` | C-10 |
| Alcance | `print_scope(ejecutadas, no_verificadas)` | C-11 |
| Legado | `severity_for(spec_id, comprobacion)` | C-12 |
| Ubicación única | `check_single_location(textos)` | C-13 |

### Flujo de ejecución

1. `--all`: resuelve la lista de specs, ejecuta las comprobaciones de estructura y las nuevas que no dependen de compuerta, imprime hallazgos y, al final, las dos listas de alcance. No declara compuerta alguna.
2. `--spec SPEC-NNN`: ejecuta las comprobaciones de estructura y las de la etapa declarada por `status`.
3. `--spec SPEC-NNN --gate Gx`: añade las comprobaciones de la compuerta, la de aprobación con firma cuando la compuerta es G1, G4 o G6, y la de estado de origen.
4. `--spec SPEC-NNN --gate G4 --git`: añade las comprobaciones de rama, alcance y cuerpo del commit que ya existen.
5. `--next-id`: sin cambios.

### Límites

- El validador no escribe, no mueve y no elimina archivos (`RNF-005`).
- El validador no consulta el remoto: G5 se apoya en `refs/remotes/origin/<rama>` y G6 en el listado local de tags.
- El validador no acredita conformidad del régimen ni aprobación de compuerta (`RF-018`).
- El validador no ejecuta los comandos de `.opencode/`; las comprobaciones de comando son de texto y de integración ligera (`DEC-008`).

### Catálogo de comprobaciones nuevas

| # | Comprobación | Modo |
|---|---|---|
| C-01 | Casilla de G1 y de G4 en `spec.md`, marcada, con cadena exacta y fecha ISO | Error en su compuerta y en estado que la exige |
| C-02 | Viñeta de G6 dentro de la entrada del release en `CHANGELOG.md` | Error con G6 y en estado `released` |
| C-03 | Commit de la línea localizado, no merge, con firma que verifica y clave autorizada | Error en su compuerta |
| C-04 | Cobertura `RF`/`CB` → `Cubre:` | Error desde G2; advertencia antes |
| C-05 | Tareas abiertas con la validación agregada | Error en `implemented`, `validated` y `released` |
| C-06 | Estado como destino de una transición admitida desde la última fila | Error |
| C-07 | Historial de transiciones con columnas, filas y coherencia con `status` | Error; advertencia en legado |
| C-08 | Reciprocidad de `supersedes` y `superseded_by` y coherencia con el estado | Error |
| C-09 | G5: dos padres, validación posterior y rama ausente en local y en seguimiento remoto | Error con G5 |
| C-10 | G6: aprobación, tag anotado, mensaje, commit objetivo, `INDEX`, `CHANGELOG` y auditoría del release menor | Error con G6 |
| C-11 | Impresión de comprobaciones ejecutadas y no verificadas | Obligatoria en cada ejecución |
| C-12 | Ventana de legado para `SPEC-001` a `SPEC-009` | Degrada a advertencia |
| C-13 | Ubicación única de la aprobación y ausencia de casilla en el reporte | Error; advertencia en legado |

## Contratos

### Formato de aprobación

| Compuerta | Archivo | Forma reconocida | Comprobación |
|---|---|---|---|
| G1 | `spec.md` | Casilla marcada con el identificador `G1`, la cadena exacta `- Approved by: Agent Sebaxtian` y fecha `YYYY-MM-DD` | C-01, C-03 |
| G4 | `spec.md` | Casilla marcada con el identificador `G4`, la misma cadena y la misma fecha | C-01, C-03 |
| G6 | `CHANGELOG.md` | Viñeta con la cadena exacta dentro de la entrada `## [vX.Y.Z]` del release de la spec | C-02, C-03 |

Reglas del contrato:

- La forma se admite solo dentro de la sección de aprobaciones de `spec.md` y dentro de la entrada del release de `CHANGELOG.md`.
- Una línea con la cadena exacta en otra sección se reporta como registro fuera de ubicación (C-13).
- La fecha se valida con el formato `YYYY-MM-DD` y como fecha de calendario.
- El validador no escribe ni corrige la línea; un cambio de forma exige al propietario.

### Localización y verificación del commit

Contrato de la función de autoría:

| Paso | Operación | Resultado |
|---|---|---|
| 1 | `git log --no-merges -S<aguja> --format=%H -- <ruta>` | Lista de commits candidatos, del más reciente al más antiguo |
| 2 | `git show <sha>:<ruta>` y comprobación de la sección | Confirma que la línea está en la sección de aprobaciones o en la entrada del release |
| 3 | `git verify-commit --raw <sha>` | Código 0 y texto con la huella `SHA256:<...>` de la clave firmante |
| 4 | `ssh-keygen -lf docs/sdd/firmantes_autorizados` | Lista de huellas autorizadas |
| 5 | Comparación de huellas | Aprobación acreditada si la huella del paso 3 figura en el paso 4 |

- La aguja de G1 y de G4 es la casilla marcada con su identificador; la de G6 es la viñeta con la cadena exacta.
- El paso 2 descarta una mención de la forma en otro lugar del mismo archivo.
- `--no-merges` selecciona el commit no merge que introdujo la línea y resuelve `CB-015`.
- La ausencia de `git`, de `ssh-keygen` o de la lista de firmantes produce el estado `NO VERIFICABLE`: la compuerta no se declara aprobada y la comprobación figura en la lista de no verificadas.

### Historial de transiciones

Subsección `### Historial de transiciones` de `## Historial de cambios` en `spec.md`.

| Columna | Contenido | Regla |
|---|---|---|
| Fecha | `YYYY-MM-DD` | Fecha del cambio de estado |
| Transición | Identificador `T1` a `T10` o la palabra `creación` | Coincide con el par origen y destino de la tabla admitida |
| Origen | Estado previo entre comillas invertidas | Igual al destino de la fila anterior |
| Destino | Estado nuevo entre comillas invertidas | Igual a `status` en la última fila |
| Responsable | Rol que escribe la transición | Pertenece al conjunto declarado por `AMB-008` |
| Evidencia | Hecho verificable que habilita la transición | No vacío |

Reglas de comprobación:

- La primera fila es la creación, con origen vacío y destino `draft`.
- Cada fila encadena su origen con el destino de la anterior.
- La última fila declara el estado vigente del frontmatter.
- Una spec sin la subsección y sin historial se admite solo en la ventana de legado y produce advertencia (C-12).

### Registro de G5 y G6 en el reporte

Después de G4 el reporte es append-only. El registro se añade como subsección `### Registro de G5 y G6` bajo `## Dictamen`, con una fila por compuerta:

| Compuerta | Forma de la fila |
|---|---|
| G5 | `- G5: merge <sha>; validación posterior: sin hallazgos; rama <rama> eliminada: sí` |
| G6 | `- G6: tag <vX.Y.Z> verificado; auditoría: <AUD-NNN>` |

- La subsección no altera la matriz ni el dictamen.
- Una fila de G5 con validación posterior distinta de `sin hallazgos` no habilita la compuerta.
- La fila de G6 se exige cuando el release es menor.

### Comandos

`/sdd-implement`:

| Paso | Contenido exigido |
|---|---|
| Precondición | Verificación G2 registrada sin hallazgos y `status` en `tasked`; una spec en otro estado se rechaza |
| Inicio | Escribe `implementing` y la fila T4 antes de la primera tarea |
| Ejecución | Una tarea pendiente por invocación, con prueba que falla primero |
| Cierre de tarea | Marca la tarea con evidencia; no evalúa G3 |
| Cierre de etapa | Con la última tarea cerrada y las pruebas en verde, ejecuta G3 una sola vez, escribe `implemented` y la fila T5 |

`/sdd-validate`:

| Paso | Contenido exigido |
|---|---|
| Precondición | G3 completa y `status` en `implemented` |
| Ejecución | Ejecuta las validaciones declaradas salvo G4 y escribe `validation_report.md` |
| Prohibición | No evalúa G4, no escribe `validated` y no escribe casilla de aprobación |
| Después del reporte | El propietario firma G4 en `spec.md` y el orquestador ejecuta G4; con aprobación escribe `validated` y la fila T6 |

### Salida del validador

| Elemento | Forma |
|---|---|
| Hallazgo | Una línea con severidad, ruta y comprobación |
| Bloque de alcance | Dos listas: comprobaciones ejecutadas y comprobaciones no verificadas |
| Código 0 | Sin hallazgos de severidad error |
| Código 1 | Al menos un hallazgo de severidad error |
| Código 2 | Uso incorrecto del comando |

## Decisiones técnicas

### DEC-001

- **Decisión:** la autoría de una aprobación se acredita con la localización del commit mediante `git log --no-merges -S`, la confirmación de la ubicación de la línea en el archivo de ese commit, `git verify-commit --raw` y la comparación de la huella `SHA256` con las huellas de `docs/sdd/firmantes_autorizados` obtenidas con `ssh-keygen -lf`.
- **Justificación:** es el único procedimiento determinista que no depende de la red, distingue la línea marcada de una mención de la forma y resuelve el commit de merge. La comparación de huellas ata la firma a la lista que mantiene el propietario y no a la configuración local de Git.
- **Alternativas descartadas:** confiar en `git log --show-signature`, que no ofrece un campo estable para comparar la clave; aceptar el código 0 de `git verify-commit` como prueba suficiente, que depende de la configuración `gpg.ssh.allowedSignersFile` y no de la lista versionada; localizar el commit con la cadena de aprobación sin la casilla marcada, que selecciona el commit que redactó la plantilla de la sección.

### DEC-002

- **Decisión:** la falta de cobertura `RF` o `CB` → `Cubre:` es error cuando la compuerta evaluada es G2 o posterior, y también cuando el estado es `tasked`, `implementing`, `implemented`, `validated` o `released`; antes de esa etapa se conserva la advertencia.
- **Justificación:** `RF-011` fija el error desde G2 y la ejecución sin compuerta debe seguir siendo informativa en `draft`, `clarified` y `planned`, donde la cobertura se está redactando.
- **Alternativas descartadas:** error en cualquier estado, que bloquearía el trabajo de Specify; advertencia permanente con elevación solo en G2, que dejaría el estado `tasked` sin comprobación en `--all`.

### DEC-003

- **Decisión:** la ejecución agregada trata como error cada tarea sin la casilla `Completada` marcada en las specs con estado `implemented`, `validated` o `released`; en `implementing` se reporta como advertencia y en los estados anteriores no se comprueba.
- **Justificación:** `RF-012` limita el error a los estados finales y `AUD-033` exige que el verde agregado no se afirme sobre tareas abiertas.
- **Alternativas descartadas:** error en cualquier estado, que impediría el trabajo normal de Implement; aplicar la comprobación solo con `--gate G3`, que es el comportamiento vigente y deja el verde agregado sin cobertura.

### DEC-004

- **Decisión:** la tabla de transiciones se replica en el validador como constante `TRANSITIONS` con origen, destino e identificador, y una prueba contrasta esa constante con la tabla de §5 del protocolo. El historial se analiza por nombres de columna, no por posición.
- **Justificación:** el validador queda determinista y no depende de que el protocolo se lea en cada ejecución, y la prueba detecta la divergencia en cuanto la base cambie. El análisis por nombre admite una tabla con columnas reordenadas sin falso hallazgo.
- **Alternativas descartadas:** leer la tabla del protocolo en cada ejecución, que acopla la validación al texto y oculta la divergencia hasta que falla; comprobar solo la pertenencia al conjunto de estados, que es el defecto `AUD-051`.

### DEC-005

- **Decisión:** G5 se comprueba con el merge de dos padres del historial local, el registro de validación posterior con la cadena `sin hallazgos` y la ausencia de la rama en las ramas locales y en `refs/remotes/origin/<rama>`. G6 se comprueba con la aprobación en la entrada del release, las tres verificaciones del tag, la coincidencia de `specs/INDEX.md` y `CHANGELOG.md` y, cuando el componente MINOR del tag supere al del tag anterior del listado local, la referencia `AUD-NNN` en la entrada.
- **Justificación:** cubre la condición de cada compuerta con evidencia local y sin red, y distingue la autorización de release de la de implementación, que es el defecto `AUD-035`.
- **Alternativas descartadas:** `git ls-remote` para confirmar la eliminación en el remoto, que incumple `RNF-003`; reutilizar la verificación de G4 para G5 y G6, que es el defecto que la spec corrige.

### DEC-006

- **Decisión:** la sucesión se comprueba en tres pasos: la carpeta declarada en `supersedes` existe, la spec sustituida declara `superseded_by` con el identificador recíproco y el estado de cada una coincide con el campo declarado.
- **Justificación:** `AUD-054` exige simetría y coherencia con el estado; los tres pasos son verificables sobre el frontmatter y sobre el árbol de `specs/`, sin juicio del validador.
- **Alternativas descartadas:** comprobar solo que el campo no está vacío, que admite una relación asimétrica; resolver la cadena completa de sucesiones, que excede el alcance de B2 y corresponde a B4.

### DEC-007

- **Decisión:** las comprobaciones C-01 a C-03, C-06 a C-10 y C-13 degradan a advertencia en `SPEC-001` a `SPEC-009`; C-04 y C-05 se aplican con la severidad de `DEC-002` y `DEC-003`, y en la ventana de legado también degradan a advertencia cuando su incumplimiento derive de una comprobación nueva.
- **Justificación:** `RNF-006` y `CB-014` fijan la ventana, y `DEC-011` exige que la ejecución agregada siga en 0 con el corpus publicado.
- **Alternativas descartadas:** aplicar el mecanismo a las specs publicadas, que devolvería código 1 sobre contratos cerrados y contravendría la cláusula de legado de la base; excluir las specs de legado de la ejecución, que ocultaría su estado.

### DEC-008

- **Decisión:** los comandos se alinean con la compuerta de entrada de su etapa y se elimina la circularidad: `/sdd-implement` exige G2 y escribe `implementing` e `implemented`, y `/sdd-validate` escribe el reporte con el rol `reviewer` sin evaluar G4 ni escribir `validated`; el orquestador evalúa G4 después de la firma y escribe `validated`.
- **Justificación:** resuelve `AUD-011`, `AUD-012`, `AUD-013`, `AUD-014` y `AUD-052` con una sola condición de entrada por etapa y una sola escritura por rol.
- **Alternativas descartadas:** mantener G3 en cada tarea y añadir la comprobación de cierre, que conserva dos momentos para la misma compuerta; dejar que el comando de validación ejecute G4 al final de su propio flujo, que restablece la circularidad porque la evaluación ocurriría en la misma invocación que escribe el reporte antes de la firma del propietario.

### DEC-009

- **Decisión:** cada comprobación nueva entra con una prueba positiva y una negativa; la negativa exige código de salida 1 y el mensaje esperado. Las comprobaciones de autoría se prueban con la función de Git inyectada y texto preparado; la verificación real de firma se registra en el reporte de validación sobre el commit `f38eb6a`.
- **Justificación:** `RF-019` exige ambas pruebas y la inyección evita depender de claves, de configuración local y de red en la suite.
- **Alternativas descartadas:** crear claves y repositorios firmados por prueba, que hace la suite dependiente de `ssh-keygen` y de la configuración del equipo; probar solo el caso positivo, que no acredita el rechazo.

### DEC-010

- **Decisión:** cada ejecución imprime al final dos listas rotuladas, una de comprobaciones ejecutadas y otra de comprobaciones no verificadas; la segunda se construye desde una constante con la lista de §14 del protocolo. Los códigos de salida se mantienen en 0, 1 y 2.
- **Justificación:** `RF-018` y `AUD-094` exigen que el verde declare su alcance y que no se lea como conformidad del régimen.
- **Alternativas descartadas:** imprimir el alcance solo con `--gate`, que deja el verde de `--all` sin declaración; añadir un código de salida nuevo para el resultado parcial, que rompe el contrato de §14.

### DEC-011

- **Decisión:** la ampliación conserva las 47 pruebas vigentes en verde, `--all` en 0, las funciones y constantes actuales y la estructura de fixtures por directorio; los fixtures nuevos se añaden como directorios hermanos y las pruebas nuevas como funciones del mismo módulo.
- **Justificación:** permite implementar por tareas pequeñas sin reescritura del validador y mantiene la comparación con el estado publicado.
- **Alternativas descartadas:** dividir el validador en paquetes, que cambia la ruta que la base cita en sus comandos; reescribir la suite, que impide detectar regresiones contra el comportamiento vigente.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Unitaria de comprobación | Funciones de prueba de `tools/sdd/tests/test_validate.py` sobre funciones puras y sobre `Reporter` | Un hallazgo esperado por caso, con severidad y mensaje esperados |
| Unitaria de autoría | Función de Git inyectada con texto preparado de `git verify-commit` y de `ssh-keygen -lf` | Aprobación acreditada con huella autorizada; rechazo con huella ajena, sin firma o con commit que no confirma la sección |
| Integración de estado | Fixtures temporales de spec completa por estado y por transición | Código 1 en la transición no admitida; código 0 en la admitida |
| Integración de compuerta | `python tools\sdd\validate.py --spec SPEC-NNN --gate Gx` sobre fixtures | Código 1 con el mensaje de la comprobación que falla; código 0 con la evidencia completa |
| Comando | Lectura del texto de `.opencode/commands/` y prueba de integración ligera sobre fixture | El comando nombra G2 y no G4 como entrada de Implement; el de validación no evalúa G4 ni escribe `validated` |
| Regresión | Las 47 pruebas vigentes y `python tools\sdd\validate.py --all` | 47 pruebas en verde y código 0 |
| Cierre | `python tools\sdd\validate.py --spec SPEC-010 --gate G2` y `--all` | Código 0 con las dos listas de alcance impresas |

Reglas de la estrategia:

- TDD en Python: primero la prueba que falla, después el código mínimo y después el refactor, en ese orden por tarea.
- La prueba negativa comprueba el código de salida y el texto del hallazgo; una prueba que solo cuente hallazgos no acredita el rechazo.
- Los fixtures de autoría, G5 y G6 se construyen en directorio temporal y se eliminan al terminar la prueba.
- Ninguna prueba ejecuta consulta de red ni escribe en el repositorio.
- La verificación real de firma de G1 de `SPEC-010` se transcribe en el reporte de validación y no en la suite.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | `.opencode/commands/sdd-implement.md`, precondición; `validate.py`, catálogo de compuertas | Lectura del texto del comando y `test_comando_implement_exige_g2` |
| `RF-002` | `sdd-implement.md`, paso de inicio; `validate.py`, historial | `test_historial_sin_fila_del_estado_falla` y fixture `estado/t4-escrito` con código 0 |
| `RF-003` | `sdd-implement.md`, cierre de etapa | Fixture `estado/t5-escrito` con código 0 y `--gate G3` sin hallazgos |
| `RF-004` | `sdd-implement.md`, cierre de etapa; `validate.py`, `gate == G3` | Comando con una sola evaluación de G3 y `test_tarea_abierta_falla_con_g3` |
| `RF-005` | `.opencode/commands/sdd-validate.md`, orden reporte y evaluación | Lectura del comando y `test_comando_validate_sin_g4` |
| `RF-006` | `sdd-validate.md`; `validate.py`, C-13 | `test_reporte_con_casilla_de_aprobacion_falla` |
| `RF-007` | `validate.py`, C-01 | `test_aprobacion_g1_marcada` y `test_aprobacion_g1_sin_marcar_falla` |
| `RF-008` | `validate.py`, C-01 | `test_aprobacion_g4_requerida_en_validated` y `test_aprobacion_g4_sin_marcar_falla` |
| `RF-009` | `validate.py`, C-02 y C-10 | `test_g6_aprobacion_fuera_de_entrada_falla` y `test_g6_release_menor_sin_auditoria_falla` |
| `RF-010` | `validate.py`, C-03 | `test_commit_de_aprobacion_firmado`, `test_commit_sin_firma_falla` y `test_clave_no_autorizada_falla` |
| `RF-011` | `validate.py`, C-04 | `test_cobertura_error_con_g2` y `test_cobertura_advertencia_en_draft` |
| `RF-012` | `validate.py`, C-05 | `test_tareas_abiertas_error_en_all_released` y `test_tareas_abiertas_advertencia_en_implementing` |
| `RF-013` | `validate.py`, C-09 | `test_g5_merge_dos_padres` y `test_g5_rama_presente_falla` |
| `RF-014` | `validate.py`, C-10 | `test_g6_tag_anotado`, `test_g6_tag_ligero_falla` y `test_g6_index_divergente_falla` |
| `RF-015` | `validate.py`, C-06 | `test_transicion_admitida` y `test_transicion_no_admitida_falla` |
| `RF-016` | `validate.py`, C-07 | `test_historial_ausente_falla` y `test_historial_sin_fila_del_estado_falla` |
| `RF-017` | `validate.py`, C-08 | `test_sucesion_reciproca` y `test_sucesion_asimetrica_falla` |
| `RF-018` | `validate.py`, C-11 | `test_alcance_impreso_en_ejecucion_agregada` |
| `RF-019` | `tools/sdd/tests/`, convención de la suite | Revisión de la suite: cada comprobación nueva con una prueba positiva y una negativa |
| `RF-020` | `validate.py`, C-13 | `test_aprobacion_fuera_de_seccion_falla` |
| `RF-021` | `sdd-validate.md`, paso posterior a la firma; `validate.py`, historial | `test_historial_fila_t6_requerida` y lectura del comando |
| `RNF-001` | `validate.py`, capa de entrada | `test_determinismo_dos_ejecuciones` |
| `RNF-002` | `validate.py`, ejecución agregada | Medición de `--all` en el cierre: 60 segundos o menos |
| `RNF-003` | `validate.py`, capa Git | Revisión de importaciones de la biblioteca estándar y `test_sin_red_en_la_suite` |
| `RNF-004` | `validate.py`, capa de salida | `test_hallazgo_con_severidad_ruta_y_comprobacion` |
| `RNF-005` | `validate.py`, capa de lectura | `test_ejecucion_no_modifica_archivos` |
| `RNF-006` | `validate.py`, C-12 | `test_legado_advertencia_sin_codigo_1` y `test_spec_nueva_error_con_codigo_1` |
| `CB-001` | `validate.py`, C-03 | `test_commit_sin_firma_falla` y `test_clave_no_autorizada_falla` |
| `CB-002` | `validate.py`, C-13 | `test_registro_dual_falla` |
| `CB-003` | `validate.py`, C-13 | `test_reporte_con_casilla_de_aprobacion_falla` |
| `CB-004` | `validate.py`, estado de origen por compuerta | `test_gate_desde_estado_incorrecto_falla` |
| `CB-005` | `validate.py`, C-08 | `test_supersedes_sin_carpeta_falla` |
| `CB-006` | `validate.py`, C-08 | `test_superseded_by_sin_estado_falla` |
| `CB-007` | `validate.py`, C-02 | `test_released_sin_aprobacion_g6_falla` |
| `CB-008` | `validate.py`, C-05 | `test_tareas_abiertas_error_en_all_released` |
| `CB-009` | `sdd-implement.md`, precondición | `test_comando_implement_exige_g2` y fixture `estado/tasked-sin-g2` con código 2 |
| `CB-010` | `validate.py`, dictamen y G4 | `test_no_convergido_deja_implemented` |
| `CB-011` | `validate.py`, C-07 | `test_historial_sin_fila_del_estado_falla` |
| `CB-012` | `validate.py`, C-09 | `test_g5_rama_presente_falla` y `test_g5_rama_remota_seguimiento_falla` |
| `CB-013` | `validate.py`, C-10 | `test_g6_tag_ligero_falla` |
| `CB-014` | `validate.py`, C-12 | `test_legado_advertencia_sin_codigo_1` |
| `CB-015` | `validate.py`, C-03 | `test_commit_merge_selecciona_commit_no_merge` |
