# Reporte de validación — SPEC-010

*Auditoría independiente de la Etapa 7 sobre el contrato de `SPEC-010`, cerrada tras las correcciones del commit `f8d6766`. Este documento no registra compuerta alguna: la aprobación de G4 corresponde al propietario y se inscribe en la sección de aprobaciones de `spec.md` mediante un commit firmado.*

## Entorno

- Sistema operativo: Windows 11 (PowerShell 7).
- Rama: `feat/mecanismo-control-sdd`.
- Commit auditado: `f8d676678076f423aca6ae3a9e19b2c654fe3991` (`fix(sdd): cerrar G5 con rama eliminada`); commit de G1: `f38eb6a`; commit de la implementación: `c41b858`; cortes de las auditorías anteriores: `f2ee715` y `3d30098`.
- Herramientas: Python 3.15.2, Git 2.56.0.windows.3, OpenSSH_for_Windows 9.5p2, `unittest` de la biblioteca estándar.
- Artefactos leídos: `specs/010-mecanismo-control-sdd/{spec.md, clarify.md, plan.md, tasks.md}`, `tools/sdd/validate.py`, `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/**`, `.opencode/commands/sdd-implement.md`, `.opencode/commands/sdd-validate.md`, `.opencode/agents/sdd.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` (§5, §6, §11, §13, §14), `docs/sdd/firmantes_autorizados`, `CHANGELOG.md` y `specs/INDEX.md`.
- Suite reejecutada: `python -m unittest discover -s tools\sdd\tests -q` → `Ran 94 tests in 0.689s` y `OK`, código de salida 0. Las siete pruebas de `TestG5Integracion` se ejecutaron además de forma individual y devuelven `ok`.
- Ejecución agregada antes de actualizar este reporte: `python tools\sdd\validate.py --all` → código de salida 1 con 2 hallazgos, ambos emitidos por la versión anterior de este reporte (dictamen `NO CONVERGIDO` y la fila `RF-013`), y 12 advertencias de legado.
- Ejecución agregada después de actualizar este reporte: `--all` devuelve código 0 con las 12 advertencias de legado y sin hallazgos de error; la convergencia del reporte retira los dos hallazgos que emitía la versión anterior.
- Ejecución final de `python tools\sdd\validate.py --spec SPEC-010 --gate G4`: código 1 con un solo hallazgo, `C-01: G4 no está marcada en la sección de aprobaciones`, que queda pendiente de la firma del propietario y no es una brecha del mecanismo.
- Determinismo y tiempo: dos ejecuciones consecutivas de `--all` devuelven salida idéntica (`IGUALES=True`) y 0.324 s sobre el corpus vigente.
- `python tools\sdd\validate.py --spec SPEC-010 --gate G1` → `OK: sin hallazgos`, código 0.
- Estado del árbol: `git status --short` enumera solo este reporte como archivo no rastreado; `git diff --check` sin salida.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | Lectura de `.opencode/commands/sdd-implement.md:8,17` | «la spec debe estar en `tasked` y tener la verificación G2 registrada»; `G4` aparece solo como aprobación del propietario, no como condición de entrada | PASADO |
| `RF-002` | `CA-002` | Lectura de `sdd-implement.md:9`; `validate.py:603-640` | «el orquestador escribe `implementing` en `spec.md` y la fila T4 del historial antes de la primera tarea»; el validador exige que la última fila del historial declare `status` | PASADO |
| `RF-003` | `CA-002` | Lectura de `sdd-implement.md:14` | «Cuando cierres la última tarea, el orquestador escribe `implemented` y la fila T5» | PASADO |
| `RF-004` | `CA-003` | Lectura de `sdd-implement.md:14`; `validate.py:1108-1110` | «G3 no se evalúa por tarea. Se evalúa al cerrar la etapa»; en el validador la comprobación de tareas solo se activa con `gate == "G3"` | PASADO |
| `RF-005` | `CA-004` | Lectura de `.opencode/commands/sdd-validate.md:4,11,12` | `agent: reviewer`; escribe el reporte, «No evalúes G4 ni escribas `validated`» y remite la evaluación al orquestador después de la firma | PASADO |
| `RF-006` | `CA-006` | `test_reporte_con_casilla_de_aprobacion_falla` (:750); `validate.py:1193-1197` | código 1 y hallazgo C-13 que nombra la casilla del reporte; la aprobación de G4 se reconoce solo en la sección de aprobaciones de `spec.md` (`validate.py:432-435`) | PASADO |
| `RF-007` | `CA-007` | `test_aprobacion_g1_marcada` (:712) y `test_aprobacion_g1_sin_marcar_falla` (:720) | positivo código 0 con `verify-commit` invocado; negativo código 1 que nombra `G1`; la forma con cadena exacta y fecha ISO se exige en `validate.py:415-439` | PASADO |
| `RF-008` | `CA-008` | `test_aprobacion_g4_requerida_en_validated` (:724) y `test_aprobacion_g4_sin_marcar_falla` (:734) | dictamen y filas de la matriz en `validate.py:1173-1191`; casilla de G4 en `validate.py:523-530` | PASADO |
| `RF-009` | `CA-009` | `test_g6_aprobacion_fuera_de_entrada_falla` (:854), `test_g6_release_menor_sin_auditoria_falla` (:858), `test_released_sin_aprobacion_g6_falla` (:862) | código 1 con el mensaje de la viñeta ausente y con la ausencia de `AUD-NNN`; `validate.py:770-773,818-827` | PASADO |
| `RF-010` | `CA-007` | `test_autoridad_commit_firmado` (:781), `test_autoridad_sin_firma_falla` (:791), `test_autoridad_clave_ajena_falla` (:795); `validate.py --spec SPEC-010 --gate G1` | `git log --no-merges -S` (`validate.py:442`), `git verify-commit --raw` (:454) y `ssh-keygen -lf docs/sdd/firmantes_autorizados` (:464); la compuerta real devuelve `OK: sin hallazgos` con código 0 | PASADO |
| `RF-011` | `CA-010` | `test_cobertura_error_con_g2` (:904) y `test_cobertura_advertencia_en_draft` (:908) | código 1 en `tasked` con `G2` nombrando `RF-002`; código 0 con advertencia en `draft`; `validate.py:543-547,1038-1048` | PASADO |
| `RF-012` | `CA-011` | `test_tareas_abiertas_error_en_all_released` (:934) | `--all` devuelve código 1 y nombra `T-002`; la fixture con tareas cerradas devuelve 0; `validate.py:550-562,1112-1114` | PASADO |
| `RF-013` | `CA-012` | `test_g5_merge_dos_padres` (:1053), `test_g5_rama_presente_falla` (:1069), `test_g5_rama_remota_seguimiento_falla` (:1073), `test_g5_merge_fuera_de_dev_falla` (:1077), `test_g5_merge_no_integra_la_rama_falla` (:1085), `test_g5_segundo_padre_invalido_falla` (:1098), `test_g5_sin_rama_declarada_falla` (:1103) | resuelve el merge desde `dev` (`validate.py:851`), exige dos padres (`:858-863`) y un segundo padre que sea commit válido (`:864-873`); contrasta el mensaje solo cuando nombra una rama (`:874-880`); exige la rama ausente de `refs/heads` y de `refs/remotes/origin/<rama>` (`:896-907`); no resuelve la referencia de la rama; una spec sin `branch` produce error (`:846-849`) | PASADO |
| `RF-014` | `CA-009` | `test_g6_tag_anotado` (:832), `test_g6_tag_ligero_falla` (:840), `test_g6_mensaje_incorrecto_falla` (:844), `test_g6_index_divergente_falla` (:850) | `cat-file -t` = `tag`, mensaje `Release vX.Y.Z`, `rev-parse ^{commit}`, fila del `INDEX` con estado y release, y comparación del componente MINOR con el tag anterior; `validate.py:775-827` | PASADO |
| `RF-015` | `CA-013` | `test_transicion_admitida` (:963) y `test_transicion_no_admitida_falla` (:970) | código 1 con el par `draft` → `planned`; `TRANSITIONS` contrastada con la tabla de §5 en :985 | PASADO |
| `RF-016` | `CA-014` | `test_historial_coherente_sin_hallazgo` (:974) y `test_historial_sin_fila_del_estado_falla` (:981) | columnas localizadas por nombre y última fila igual a `status`; `validate.py:579-640` | PASADO |
| `RF-017` | `CA-015` | `test_sucesion_reciproca` (:1016), `test_sucesion_asimetrica_falla` (:1023) y `test_sucesion_sin_destino_falla` (:1031) | la recíproca devuelve 0; la asimétrica, la carpeta ausente y el estado ausente devuelven 1; la spec en `superseded` sin `superseded_by` produce C-08 (`validate.py:701-703`) con fixture `sucesion/sin-destino` | PASADO |
| `RF-018` | `CA-016` | `test_alcance_impreso_en_ejecucion_agregada` (:1141); `validate.py --all` | imprime «Comprobaciones ejecutadas» y «Comprobaciones no verificadas», con «la conformidad del régimen completo» en la segunda lista (`validate.py:139-145,913-987,1323`) | PASADO |
| `RF-019` | `CA-017` | Suite de `tools/sdd/tests/` (94 pruebas) y revisión de C-01 a C-13 | doce comprobaciones con positiva y negativa; C-11 incorpora `scope_is_conformant` (`validate.py:941-949`), lo usa `print_scope` (`:951-957`) y la negativa (:1150) induce la ausencia del bloque y la rechaza; C-09 incorpora positiva de rama eliminada y negativas de merge fuera de `dev`, segundo padre inválido, rama sin declarar y mensaje de otra rama | PASADO |
| `RF-020` | `CA-006` | `test_g6_en_spec_falla` (:761), `test_casilla_g1_en_entrada_de_release_falla` (:866), `test_ubicacion_unica_sin_hallazgo` (:875), `test_aprobacion_fuera_de_seccion_falla` (:740), `test_registro_dual_falla` (:744) | la línea de G6 en la sección de aprobaciones de `spec.md` produce C-13 (`validate.py:525-537`); la casilla de G1 o G4 en la entrada del release produce C-13 (`:765-769`); la ubicación correcta no produce hallazgo | PASADO |
| `RF-021` | `CA-005` | Lectura de `sdd-validate.md:12`; `validate.py:603-640` | el comando atribuye al orquestador la evaluación de G4 tras la firma; el estado `validated` exige la casilla de G4 y la fila T6 cuando el orquestador lo escribe | PASADO |
| `RNF-001` | `CA-018` | Dos ejecuciones consecutivas de `python tools\sdd\validate.py --all` | salida idéntica (`IGUALES=True`) y mismo código de salida en ambas | PASADO |
| `RNF-002` | `CA-018` | `Measure-Command` sobre `--all` | 0.324 s sobre el corpus vigente, por debajo de 60 s | PASADO |
| `RNF-003` | `CA-018` | `test_solo_biblioteca_estandar` (:199); revisión de `validate.py` | importaciones de biblioteca estándar (`argparse`, `re`, `subprocess`, `sys`, `datetime`, `pathlib`); las consultas externas son locales a `git` y `ssh-keygen`, sin red | PASADO |
| `RNF-004` | `CA-016` | `test_hallazgo_con_severidad_ruta_y_comprobacion` (:1163) | cada hallazgo ocupa una línea `[WARN]` o `[ERROR]` con la ruta y el mensaje de la comprobación; las comprobaciones nuevas añaden la etiqueta `C-NN` | PASADO |
| `RNF-005` | `CA-019` | `git status --short` antes y después de `--all`; lectura de `validate.py` | sin diferencias atribuibles a la ejecución; el módulo solo abre archivos en lectura | PASADO |
| `RNF-006` | `CA-020` | `--all`; `test_legado_advertencia_sin_codigo_1` (:1184) y `test_legado_spec_nueva_error_con_codigo_1` (:1191) | código 0 con 12 advertencias de legado; la misma falta en `SPEC-010` produce código 1 | PASADO |
| `CB-001` | `CA-007` | `test_autoridad_sin_firma_falla` (:791) y `test_autoridad_clave_ajena_falla` (:795) | firma que no verifica y huella ajena producen código 1 | PASADO |
| `CB-002` | `CA-006` | `test_registro_dual_falla` (:744) | dos casillas de G1 producen código 1 con la palabra «dual»; la detección cubre G1 y G4 | PASADO |
| `CB-003` | `CA-006` | `test_reporte_con_casilla_de_aprobacion_falla` (:750); `validate.py:1193-1197` | casilla de aprobación en el reporte produce código 1 con hallazgo de contrato del reporte | PASADO |
| `CB-004` | `CA-013` | `test_gate_desde_estado_incorrecto_falla` (:993); `validate.py:641-661` | `tasked` con `G4` produce código 1 por estado de origen | PASADO |
| `CB-005` | `CA-015` | `test_sucesion_asimetrica_falla` (:1023, fixture `sin-carpeta`); `validate.py:679-685` | `supersedes: SPEC-099` sin carpeta produce código 1 nombrando el identificador | PASADO |
| `CB-006` | `CA-015` | `test_sucesion_asimetrica_falla` (:1023, fixture `sin-estado`); `validate.py:686-690` | `superseded_by` con estado distinto de `superseded` produce código 1 | PASADO |
| `CB-007` | `CA-009` | `test_released_sin_aprobacion_g6_falla` (:862) | spec en `released` sin la viñeta produce código 1 y G6 no se declara superada | PASADO |
| `CB-008` | `CA-011` | `test_tareas_abiertas_error_en_all_released` (:934) | tarea abierta en `released` produce código 1 con el identificador `T-002` | PASADO |
| `CB-009` | `CA-001` | Lectura de `sdd-implement.md:8` | con `tasked` y sin G2 registrada el comando se detiene sin escribir estado | PASADO |
| `CB-010` | `CA-005` | `test_no_convergido_marcado_es_error` (:153) | dictamen `NO CONVERGIDO` marcado produce código 1 y G4 no se declara superada | PASADO |
| `CB-011` | `CA-014` | `test_historial_sin_fila_del_estado_falla` (:981) | estado sin fila en el historial produce código 1 | PASADO |
| `CB-012` | `CA-012` | `test_g5_rama_presente_falla` (:1069) y `test_g5_rama_remota_seguimiento_falla` (:1073) | rama local y referencia remota de seguimiento producen código 1 | PASADO |
| `CB-013` | `CA-009` | `test_g6_tag_ligero_falla` (:840) y `test_g6_mensaje_incorrecto_falla` (:844) | tag ligero y mensaje incorrecto producen código 1 y G6 no se declara superada | PASADO |
| `CB-014` | `CA-020` | `test_legado_advertencia_sin_codigo_1` (:1184); `--all` | advertencia con cláusula de legado y código 0 | PASADO |
| `CB-015` | `CA-007` | `test_autoridad_commit_merge_verifica_no_merge` (:799); `validate.py:442` | el listado de candidatos excluye los commits de merge y la firma se verifica sobre el commit no merge | PASADO |

## Registro de las comprobaciones C-01 a C-13

| # | Comprobación | Implementación | Prueba positiva | Prueba negativa | Causa esperada de la negativa | Resultado |
|---|---|---|---|---|---|---|
| C-01 | Casilla de G1 y de G4 marcada, con cadena exacta y fecha ISO | `validate.py:394-439,506-540` | :712, :724 | :720, :734 | «G1/G4 no está marcada en la sección de aprobaciones» | PASADO |
| C-02 | Viñeta de G6 dentro de la entrada del release | `validate.py:709-717,770-773` | :832 | :854, :862 | «la entrada del release no contiene la viñeta» | PASADO |
| C-03 | Commit localizado, no merge, con firma y clave autorizada | `validate.py:442-504` | :781, :799 | :791, :795 | «la firma no verifica» y «la clave no figura en la lista» | PASADO |
| C-04 | Cobertura `RF`/`CB` → `Cubre:` | `validate.py:305-320,543-547,1038-1048` | :895 | :904 | «RF-002 no aparece en ninguna línea Cubre» con código 1 | PASADO |
| C-05 | Tareas abiertas en la ejecución agregada | `validate.py:283-293,550-562,1112-1114` | :934 (tareas cerradas) | :934 (tareas abiertas) | «la tarea T-002 no está completada y la spec está en released» | PASADO |
| C-06 | Transición admitida y estado de origen de la compuerta | `validate.py:568-577,603-640,641-661` | :963, :993 | :970, :993 | «la transición draft → planned no está admitida» y «estado de origen tasked no habilita G4» | PASADO |
| C-07 | Historial de transiciones y coherencia con `status` | `validate.py:579-640` | :974 | :981 | «el estado implemented no figura como destino de la última fila» | PASADO |
| C-08 | Reciprocidad de sucesión y coherencia de estado | `validate.py:665-707` | :1016 | :1023, :1031 | «no es recíproco», «no existe su carpeta», «se exige superseded» y «está en superseded y no declara superseded_by» | PASADO |
| C-09 | G5: merge en `dev`, segundo padre válido, validación posterior y rama ausente | `validate.py:832-908` | :1053 | :1077, :1085, :1098, :1103, :1069, :1073 | «no hay integración alcanzable desde dev», «no integra la rama», «segundo padre no es un commit válido», «no declara la rama», «sigue presente» y «figura en la referencia remota» | PASADO |
| C-10 | G6: tag anotado, mensaje, commit objetivo, INDEX y auditoría | `validate.py:775-827` | :832 | :840, :844, :850, :858 | «objeto ligero», «el mensaje no es», «INDEX declara otro estado» y «no cita el informe» | PASADO |
| C-11 | Impresión de comprobaciones ejecutadas y no verificadas | `validate.py:913-957,1323` | :1141 | :1150 | la salida inducida carece del bloque de no verificadas y `scope_is_conformant` devuelve `False` | PASADO |
| C-12 | Ventana de legado para `SPEC-001` a `SPEC-009` | `validate.py:90,349-363` | :1184 | :1191 | advertencia con código 0 en `SPEC-001` frente a error con código 1 en `SPEC-010` | PASADO |
| C-13 | Ubicación única de la aprobación y casilla en el reporte | `validate.py:87,415-439,525-537,765-769,1193-1197` | :724, :832, :875 | :740, :744, :750, :761, :866 | «marcada fuera de la sección», «registro dual», «el reporte porta una casilla», «la línea de G6 está en spec.md» y «la casilla de G1 está en la entrada del release» | PASADO |

## Verificación de la firma de G1

- `git -c gpg.ssh.allowedSignersFile=docs/sdd/firmantes_autorizados verify-commit f38eb6a` → `Good "git" signature for sebaxtianrioss@gmail.com with ED25519 key SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc`, código de salida 0.
- `ssh-keygen -lf docs/sdd/firmantes_autorizados` → `256 SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc agent@sebaxtian.dev (ED25519)`. La huella firmante figura en la lista.
- `git show f38eb6a:specs/010-mecanismo-control-sdd/spec.md` contiene la casilla de G1 marcada con la cadena exacta y la fecha ISO.
- `python tools\sdd\validate.py --spec SPEC-010 --gate G1` → `OK: sin hallazgos`, código 0.

## Verificación de la corrección de G5

- `check_g5` ya no resuelve la referencia de la rama: la única consulta con la rama es `git rev-parse --verify --quiet refs/remotes/origin/<rama>` (`validate.py:903`), que comprueba la referencia remota de seguimiento y no la rama local. La prueba positiva :1053 afirma que no existe una llamada `rev-parse` con la rama sin `refs/remotes`.
- El merge se resuelve con `git log --merges -1 --format=%H dev` (`:851`), exige dos padres (`:858-863`) y comprueba que el segundo padre sea un objeto commit con `git cat-file -e <sha>^{commit}` (`:864-873`). La negativa :1098 induce un segundo padre inválido y devuelve código 1 con «segundo padre».
- La prueba positiva :1053 representa la rama eliminada: `refs/heads` contiene `main` y `dev` sin la rama de trabajo, no hay referencia remota de seguimiento y el validador no intenta resolver la referencia.
- La negativa :1085 usa el mensaje `Merge branch 'feat/otra-rama' into dev`; el validador contrasta el mensaje con la rama declarada (`:874-880`) y devuelve código 1 nombrando `feat/otra-rama` y `feat/mecanismo-control-sdd`, sin resolver la referencia.
- Una spec sin `branch` produce error (`:846-849`) y la prueba :1103 lo verifica, de modo que no elude G5.
- Comprobación sobre el historial real: el merge alcanzable desde `dev` es `09eaf34` (`Merge pull request #6 from sebaxtian/feat/base-normativa-sdd-v2`), con padres `5c98b68` y `d7114a7`; `git cat-file -e d7114a7^{commit}` devuelve 0. El mensaje no nombra una rama con la forma reconocida y la comprobación de mensaje no se aplica. El historial local no contiene merges con la forma `Merge remote-tracking branch`.

## Brechas

Sin brechas abiertas. Las cuatro brechas de las auditorías anteriores quedan cerradas:

- `RF-017`: la spec en `superseded` sin `superseded_by` produce C-08 (`validate.py:701-703`) y su prueba negativa :1031 la ejerce con la fixture `sucesion/sin-destino`.
- `RF-019`: C-11 dispone de la negativa :1150, que induce la ausencia del bloque y comprueba que `scope_is_conformant` lo rechaza.
- `RF-020`: la línea de G6 en `spec.md` y la casilla de G1 o G4 en la entrada del release producen C-13 (`:525-537` y `:765-769`), con las negativas :761 y :866, y la positiva :875 confirma que la ubicación correcta no produce hallazgo.
- `RF-013`: la compuerta se satisface con la rama eliminada porque la integración se acredita con el segundo padre del merge de `dev` y el mensaje cuando nombra una rama, no con la referencia de la rama.

## Observaciones

- `RF-013` · `tools/sdd/validate.py:137,874-880`: la expresión del mensaje admite la forma `Merge remote-tracking branch '...'`, pero captura el valor completo entre comillas; un mensaje `Merge remote-tracking branch 'origin/feat/mecanismo-control-sdd'` se contrastaría con la rama declarada `feat/mecanismo-control-sdd` y produciría un error aunque la integración fuera correcta. El historial del repositorio no contiene merges de esa forma y el flujo documentado usa el merge de Pull Request, cuyo mensaje no se contrasta. Conviene normalizar el prefijo del remoto antes de comparar.
- `RF-013` · `tools/sdd/validate.py:874-880`: la correspondencia entre el merge y la rama declarada solo se comprueba cuando el mensaje nombra una rama; los merges de Pull Request (`Merge pull request #N from ...`) y los mensajes libres omiten esa comprobación. Las condiciones literales de `RF-013` se cumplen con los dos padres y la ausencia de la rama; la comprobación del mensaje es una garantía adicional.
- `RF-020` · `tools/sdd/validate.py:525-537,765-769`: C-13 inspecciona la sección de aprobaciones de `spec.md` y la entrada del release de `CHANGELOG.md`; una línea de G6 escrita en otra sección de `spec.md`, o una casilla de G1 o G4 escrita en otra sección de `CHANGELOG.md`, no produce hallazgo. Los casos registrados quedan cerrados; el alcance restante es una esquina que conviene documentar.
- `RF-001`, `RF-004`, `RF-005`, `RF-021` · `specs/010-mecanismo-control-sdd/plan.md:284-304`: la matriz del plan mantiene la cita de pruebas que no existen en la suite (`test_comando_implement_exige_g2`, `test_comando_validate_sin_g4`, `test_tarea_abierta_falla_con_g3`, `test_historial_fila_t6_requerida`) y de la fixture `estado/tasked-sin-g2`; `tasks.md:255` registra la omisión de las pruebas de texto de `T-013`. La evidencia de estos requisitos es la lectura de los comandos, que se verificó.
- `RF-002`, `RF-003`, `RF-021` · `.opencode/agents/sdd.md:109`: la definición del orquestador declara que no escribe artefactos, mientras que `sdd-implement.md:9,14` y `sdd-validate.md:12` le atribuyen la escritura de `implementing`, `implemented` y `validated`, en línea con §5 del protocolo y en contradicción con §12. La formalización de permisos corresponde al bloque B3 y queda como dependencia declarada.
- `RF-014`, `RNF-001`, `RNF-003`, `RNF-005`, `CB-010` · `plan.md:305-325`: la matriz del plan cita `test_determinismo_dos_ejecuciones`, `test_sin_red_en_la_suite`, `test_ejecucion_no_modifica_archivos` y `test_no_convergido_deja_implemented`, que no existen; estas evidencias se obtuvieron por medición directa y lectura del código.
- `CB-002`, `CB-015` · `tools/sdd/tests/test_validate.py:744-748,799-808`: la prueba de registro dual cubre G1 y G4; la prueba del commit de merge depende de la respuesta preparada de la función inyectada y no afirma que el listado de candidatos excluya los merges. La implementación usa `--no-merges` (`validate.py:442`), de modo que el comportamiento existe; conviene reforzar ambas pruebas.
- `RNF-004` · `tools/sdd/validate.py:1002-1012,1173-1197`: los hallazgos de comprobaciones anteriores a esta spec no llevan la etiqueta `C-NN`; el formato de una línea con severidad, ruta y mensaje se conserva.
- `CB-004` · `tools/sdd/validate.py:641-661` · `tasks.md:207,239`: la comprobación rechaza los estados anteriores al que habilita la compuerta y admite los posteriores como reauditoría; la desviación está declarada en `T-010` y `T-012`.
- `docs/sdd/PROTOCOLO_OPERATIVO.md:330`: la lista de comprobaciones no verificadas aún incluye la firma del commit de aprobación, que el validador ya verifica. La base v2 se cerró en el bloque B1 y la alineación queda fuera del alcance de esta spec.
- Alcance del commit `f8d6766`: dos archivos (`tools/sdd/validate.py` y `tools/sdd/tests/test_validate.py`), con 72 inserciones y 21 supresiones. No modifica la spec, el plan, las tareas ni los comandos, de modo que el estado `implemented` y las transiciones T4 y T5 permanecen sin cambio.

## Dictamen

- [x] CONVERGIDO (42 de 42 requisitos en `PASADO`).
- [ ] NO CONVERGIDO.

Los 42 requisitos quedan en `PASADO`: `RF-001` a `RF-021`, `RNF-001` a `RNF-006` y `CB-001` a `CB-015`. No queda brecha abierta. Las observaciones no bloquean la convergencia y se registran para las etapas posteriores; la dependencia de permisos del bloque B3 y la alineación de `plan.md` con las pruebas reales corresponden a specs posteriores.

La compuerta G4 no se declara superada en este documento. Su aprobación corresponde al propietario y se registra en la sección de aprobaciones de `spec.md` dentro de un commit firmado con una clave de `docs/sdd/firmantes_autorizados`; la línea de G4 permanece sin marcar y su verificación queda pendiente de esa firma.
