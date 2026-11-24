# Reporte de validación — SPEC-017

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/gemma-4-26b-a4b-it-qat-gguf`.
- Commit validado: `4336d3c` (`4336d3c3e5e5a9cf22aae4948d010b122f86238d`, `chore(spec-017): renovar la aprobacion G1 sobre el contrato 0.6.0`), con firma verificada `Good "git" signature for sebaxtianrioss@gmail.com with ED25519 key SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc` y firmante presente en `docs/sdd/firmantes_autorizados`.
- Estado del árbol: 29 archivos modificados sin confirmar respecto del commit validado —`spec.md`, `plan.md`, `tasks.md`, `specs/INDEX.md`, `MEMORY.md`, los 4 archivos de `src/gemma/perfiles/`, los 9 módulos de `tools/gemma/` y las 11 suites de `tools/gemma/tests/`; `clarify.md` no figura entre los modificados—; la evidencia de `T-037` a `T-083` se sostiene sobre ese árbol y no sobre `HEAD`. La observación figura como `O-02`.
- Herramientas: intérprete Python resuelto por la vía `LLAMA_PYTHON` (`C:\Users\sebax\AppData\Local\Python\pythoncore-3.15-64\python.exe`), suite `unittest` de la biblioteca estándar, llama.cpp `0.9.0-dev` con commit `0a94a3f28`, GPU dedicada con `16311 MiB` de VRAM total reportada, memoria de expertos en host medida con `--log-verbosity 4`.
- Suites ejecutadas el 2026-11-24 por el `reviewer`: `python -m unittest discover -s tools\gemma\tests -q` → `Ran 140 tests in 8.258s`, `OK`, 0 fallos y 0 pruebas omitidas; `python -m unittest -v tools.gemma.tests.test_lanzador.LanzadorBatTest.test_bat_desde_directorio_ajeno` → `Ran 1 test in 0.970s`, `OK`, con la invocación real del `.bat` y `COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas`.
- Registros de medición leídos de `results/gemma/`: 33 archivos —11 en `rendimiento/` y 22 en `resiliencia/`—; los citados en la matriz se transcriben con sus campos 13, 14, 19 y 22.

Salida de `python tools\sdd\validate.py --spec SPEC-017`:

```
OK: sin hallazgos.

Comprobaciones ejecutadas:
  estructura, frontmatter y secciones de cada artefacto
  notación EARS, léxico vetado e identificadores
  cobertura RF/CB → CA
  historial de transiciones y transiciones admitidas
  sucesión entre specs
  reporte de validación: dictamen y matriz
  INDEX.md y longitud de AGENTS.md
  aprobación de G1 y G4 en su ubicación única
  aprobación de G6 en la entrada del release
  enlace CA → T y evidencia de las tareas
  cierre de integración y versionado de la regularización
  inventario de hallazgos: compleción, regla citada y veredicto
  conjunto de 6 artefactos de empaquetado y destino del tag
  prohibición de autorreferencia y cierre de los dieciséis hallazgos
  historial de releases y constante de estados de la nota de cierre

Comprobaciones no verificadas:
  la veracidad de la evidencia transcrita en los artefactos
  la ejecución real de un script .bat o de una suite de pruebas
  la eliminación de la rama de trabajo en el remoto
  la autosuficiencia del protocolo
  la conformidad del régimen completo
```

Salida de `python tools\sdd\validate.py --spec SPEC-017 --gate G4`:

```
[ERROR] specs\017-configuracion-gemma-4-26b-a4b\spec.md: C-01: G4 no está marcada en la sección de aprobaciones

Comprobaciones ejecutadas:
  estructura, frontmatter y secciones de cada artefacto
  notación EARS, léxico vetado e identificadores
  cobertura RF/CB → CA
  historial de transiciones y transiciones admitidas
  sucesión entre specs
  reporte de validación: dictamen y matriz
  INDEX.md y longitud de AGENTS.md
  compuerta G4: estado de origen
  aprobación de G1 y G4 en su ubicación única
  firma del commit de aprobación y clave autorizada
  aprobación de G6 en la entrada del release
  enlace CA → T y evidencia de las tareas
  cierre de integración y versionado de la regularización
  inventario de hallazgos: compleción, regla citada y veredicto
  conjunto de 6 artefactos de empaquetado y destino del tag
  prohibición de autorreferencia y cierre de los dieciséis hallazgos
  historial de releases y constante de estados de la nota de cierre

Comprobaciones no verificadas:
  la veracidad de la evidencia transcrita en los artefactos
  la ejecución real de un script .bat o de una suite de pruebas
  la eliminación de la rama de trabajo en el remoto
  la autosuficiencia del protocolo
  la conformidad del régimen completo
```

Salida del código de retorno `1` del comando anterior: el único hallazgo es la casilla `G4` sin marcar.

El hallazgo de la compuerta G4 es el esperado antes de la aprobación del propietario: la casilla `G4` de `specs/017-configuracion-gemma-4-26b-a4b/spec.md:306` permanece sin marcar y sin contenido. Antes de redactar este reporte, la misma compuerta añadía el hallazgo de `validation_report.md` ausente, que este documento resuelve; el código de retorno sigue siendo `1` solo por la casilla de la compuerta. El `reviewer` no declara la compuerta ni escribe línea de aprobación alguna.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | `.bat --perfil rendimiento --modo comprobar` desde `tmp\senuelo`; `python -m unittest discover -s tools\gemma\tests -p "test_lanzador.py"` | `test_bat_desde_directorio_ajeno: Intérprete: C:\Users\sebax\AppData\Local\Python\pythoncore-3.15-64\python.exe (LLAMA_PYTHON)` y `cierre=COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas`, `codigo=0`, 0 rutas impresas bajo el directorio temporal; `T-043` repite la invocación desde `tmp\senuelo` con 0 líneas `REGISTRO:` (`T-018`, `T-043`) | PASADO |
| `RF-002` | `CA-002` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` | `ExistenciasTest.test_existencias_superadas` en verde con los 4 artefactos y `test_perfil_sin_especulativa_sin_draft` en verde con los 3 del perfil alternativo; `Ran 14 tests in 0.124s` y `OK` (`T-011`, `T-075`) | PASADO |
| `RF-003` | `CA-002` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` | `[ERROR] artefacto ausente: mmproj models/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF/mmproj-BF16.gguf` con código `4` y 0 lanzamientos del servidor (`T-011`) | PASADO |
| `RF-004` | `CA-003` | `python -m unittest discover -s tools\gemma\tests -p "test_registro.py"` y recuento de `results/gemma/` | `DosEjecucionesTest` deja `20261121T140307Z-rendimiento-carga.md` y `20261121T140307Z-rendimiento-carga-2.md` con 0 sobrescrituras; los 33 registros declaran `version_binario: 0.9.0-dev` y `commit_llama_cpp: 0a94a3f28` (`T-024`, `T-025`) | PASADO |
| `RF-005` | `CA-004` | `python -m unittest discover -s tools\gemma\tests -p "test_documento.py"` sobre el documento real | `test_documento_tres_secciones: secciones=## Configuración candidata, ## Resultado medido y ## Configuración aprobada; marcas=rendimiento=candidato, resiliencia=candidato, sin_especulativa=candidato; candidatos_en_aprobada=0` (`T-035`, `T-044`, re-ejecutado) | PASADO |
| `RF-006` | `CA-005` | `python -m unittest discover -s tools\gemma\tests -p "test_registro.py"` y lectura de registros | 22 filas en el orden de `RF-006` con la fila 22 «Memoria de expertos en host» en `MiB` y las 13 magnitudes 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19 y 22 con unidad; los registros declaran la fila 22 «Memoria de expertos en host» en `2846.25 MiB` y en `4071.38 MiB` según la corrida (`T-025`, `T-060`) | PASADO |
| `RF-007` | `CA-004` | `python -m unittest discover -s tools\gemma\tests -p "test_estado.py"` y lectura de los 3 manifiestos | Los 3 manifiestos declaran `"estado": "candidato"`, `"aprobacion": null` y `"designacion": null`; `test_aprobado_con_desbordamiento_devuelve_candidato: estado=candidato`; el documento no contiene `línea base de producción`, `perfil rendimiento máximo` ni `optimizado` en `## Configuración aprobada` (`T-029`, `T-030`, `T-044`) | PASADO |
| `RF-008` | `CA-007` | `MEMORIA:` de la ejecución de servicio de `T-043` y campos 13, 14 y `vram_total_mib` de los registros | `MEMORIA: VRAM total 16311, usada 12162, libre 3889, residente 4893, desbordamiento 4346`; los registros declaran `vram_total_mib: 16311` con campo 13 `15715 MiB` y `12162 MiB`, ambos menores o iguales al total reportado (`T-020`, `T-043`, `20261124T192807Z`) | PASADO |
| `RF-009` | `CA-008` | `.bat --perfil resiliencia --modo medir --prueba contexto-sostenido` | `SONDA: 2400 tokens en 24.32 s, 99.35 tokens/s` en 1 sola solicitud, campo 17 `99.35 tokens/s` y campo 18 `continúa en servicio` del registro `20261124T160701Z-resiliencia-contexto-sostenido` (`T-037`, `T-073`) | PASADO |
| `RF-010` | `CA-009` | `python -m unittest discover -s tools\gemma\tests -p "test_gguf.py"` y comprobación 2 de `C-9` | Lectura real `general.name='Gemma-4 26B-A4B IT (smart Q4_0, QAT-lossless)' general.file_type=2 tamano_bytes=14249047104`; ante divergencia, `[ERROR] cuantización declarada UD-Q4_K_XL, nombre interno leído <nombre_gguf>` con código `5` y 0 lanzamientos (`T-045`, `T-011`) | PASADO |
| `RF-011` | `CA-010` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` y lectura de `sin_especulativa.json` | `sin_especulativa.json` declara 3 artefactos, `"draft": null` y `"especulativa": {"tipo": "ninguno", "techo": null}`; la comprobación 1 se supera sin el borrador y el perfil especulativo devuelve código `4` al retirarlo (`T-003`, `T-011`, `T-053`) | PASADO |
| `RF-012` | `CA-011` | 4 comparaciones medidas con `--modo comparar` y `--modo medir --prueba alternativa-contexto-menor` | Bloques de `C-7` con 10 claves: `ubatch` `512`→`1120` (Δprompt `+21,22`, Δgen `−6,39`, ΔVRAM `+220`/`−220`); `ctx_size` `4096`→`131072` (Δgen `+3,94`, Δprompt `−4,58`, ΔVRAM `+2440`/`−2440`) con `alternativa_contexto` `20261124T183107Z-resiliencia-alternativa-contexto-menor` y `38,8`/`83,8` tokens/s; `ncmoe` `0`→`9` en los 2 perfiles (Δgen `−94,10` y `−106,54`, ΔVRAM `−3500`/`+3500`) (`T-039`, `T-041`, `T-042`, `T-082`) | PASADO |
| `RF-013` | `CA-012` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` | `test_comprobacion_3_enumera_los_9_ejes: detalle=9 opciones enumeradas por el binario: cache_type_k --cache-type-k, cache_type_v --cache-type-v, ctx_size --ctx-size, flash_attn --flash-attn, gpu_layers --n-gpu-layers, load_mode --load-mode, ncmoe --n-cpu-moe, parallel --parallel, ubatch --ubatch-size codigo=0`; la opción sintética no enumerada devuelve `[ERROR] opción rechazada por el binario` con código `3` (`T-014`, `T-074`, `T-075`) | PASADO |
| `RF-014` | `CA-014` | `python -m unittest discover -s tools\gemma\tests -p "test_lanzador.py"` | `test_modo_comparar_conserva_ncmoe_adoptado: mediciones=2 ncmoe=['9', '9'] ubatch=['512', '1120'] ctx_size=['4096', '4096'] omitidas=2`: rige el valor propuesto de `ncmoe` porque su comparación consta citada, y el inicial en `ubatch` y `ctx_size` porque no consta cita (`T-009`, `T-079`) | PASADO |
| `RNF-001` | `CA-002` | `.bat --perfil rendimiento --modo comprobar` real, dentro de `test_bat_desde_directorio_ajeno` | `Ran 1 test in 0.970s` y `OK` con `cierre=COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas` en la misma invocación, de modo que las 5 comprobaciones previas —incluidas la lectura del GGUF y la consulta de opciones del binario— se completaron por debajo del límite de 5 s (`T-015`, `T-047`, re-ejecutado) | PASADO |
| `RNF-002` | `CA-006` | `python -m unittest discover -s tools\gemma\tests -p "test_documento.py"` | `test_documento_codificacion: doble_codificacion=0 bom=0` sobre el documento real; `T-034` registra 404 sustituciones de secuencia doblemente codificada, 0 identificadores y 0 valores alterados (`T-034`, `T-044`) | PASADO |
| `RNF-003` | `CA-007` | Campos 19 y 22 de los registros de carga, comparación y contexto sostenido | Derrame = campo 19 − campo 22: `3150 − 2846.25 = 274.62 MiB` (`T-082`), `3176 − 2846.25 = 329.75 MiB` (`T-039`), `3122 − 2846.25 = 275.75 MiB` (`T-041`) y `4346 − 4071.38 = 274.62 MiB` (`T-043`), todos de como máximo `512 MiB`; la descarga intencional de expertos se resta y no cuenta como derrame (`T-062`, `T-082`) | PASADO |
| `RNF-004` | `CA-003` | `python -m unittest discover -s tools\gemma\tests -p "test_registro.py"` y recuento de `results/gemma/` | `DosEjecucionesTest` deja 1 archivo por ejecución con el sufijo `-2` ante colisión y 0 bytes alterados del primero; `test_documento_valores_historicos: ... results/gemma/ declara 33 registro(s)` y 0 sobrescrituras (`T-024`, `T-025`, `T-064`) | PASADO |
| `RNF-005` | `CA-005` | `python -m unittest discover -s tools\gemma\tests -p "test_registro.py"` y `-p "test_comparar.py"` | 0 campos vacíos, 0 magnitudes sin unidad —también en la fila 22— y los registros de 21 filas se leen con la fila 22 en `no disponible` sintetizada en memoria sin escribir el archivo (`T-060`, `T-064`, `DEC-027`) | PASADO |
| `RNF-006` | `CA-015` | `python -m unittest discover -s tools\gemma\tests -p "test_estado.py"` | Con `aprobacion` sin `umbral_tg_tokens_por_segundo` el estado es `candidato` con `aprobacion: falta la clave «umbral_tg_tokens_por_segundo» que exige RNF-006`; los 3 manifiestos declaran `aprobacion: null`, de modo que 0 configuraciones aprobadas carecen del umbral (`T-029`, `T-030`) | PASADO |
| `RNF-007` | `CA-007` | Campo 14 de los registros de la configuración vigente y `python -m unittest discover -s tools\gemma\tests -p "test_estado.py"` | Última carga del perfil vigente con `3889 MiB` libres (`20261124T191126Z-rendimiento-comparacion-ncmoe` y `MEMORIA: ... libre 3889` de `T-043`), por encima de los `512 MiB`; la elegibilidad es negativa con `511 MiB` y positiva con `512 MiB` (`T-030`, `T-043`) | PASADO |
| `CB-001` | `CA-001` | `python -m unittest discover -s tools\gemma\tests -p "test_lanzador.py"` | `test_bat_desde_directorio_ajeno` con 1 señuelo en la ruta relativa de los pesos: 0 rutas resueltas desde el directorio de trabajo y el manifiesto leído bajo la raíz resuelta por `%~dp0` (`T-016`, `T-018`) | PASADO |
| `CB-002` | `CA-012` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` | `[ERROR] opción rechazada por el binario: ncmoe (9)` con código `3` y 0 lanzamientos del servidor (`T-015`) | PASADO |
| `CB-003` | `CA-008` | `python -m unittest discover -s tools\gemma\tests -p "test_probe.py"` y `-p "test_lanzador_modos.py"` | `SONDA: 1200 tokens contados antes del corte: transcripción cortada por la detención del servidor` y `test_registro_de_prueba_fallida_no_promueve: ... estabilidad=se detuvo` con el perfil sin promover (`T-067`, `T-073`) | PASADO |
| `CB-004` | `CA-007` | Registro `results/gemma/rendimiento/20261124T192807Z-rendimiento-comparacion-contexto.md` | Conservado con campo 14 `336 MiB`, campo 19 `4594 MiB`, campo 22 `4071.38 MiB` y derrame `522.62 MiB`, superior al umbral; el perfil sigue `candidato` y la medición no se editó (`T-042`) | PASADO |
| `CB-005` | `CA-006` | `python -m unittest discover -s tools\gemma\tests -p "test_documento.py"` | `test_documento_valores_historicos: valor_alterado=0 identificador_alterado=0; results/gemma/ declara 33 registro(s) y la comparación los contrasta` (`T-044`, `T-064`) | PASADO |
| `CB-006` | `CA-004` | `python -m unittest discover -s tools\gemma\tests -p "test_estado.py"` y `-p "test_perfiles_datos.py"` | `test_huella_cambia_por_los_2_ejes_de_cache: manifiesto=rendimiento.json huella_9=71e631c2… registros_previos=2 estado=candidato`; 1 cambio de `opciones` degrada a `candidato` con el motivo «opciones modificadas» y registrar 1 comparación no degrada (`T-029`, `T-079`) | PASADO |
| `CB-007` | `CA-013` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` | `test_presupuesto_evalua_contexto_efectivo: efectivo='presupuesto de VRAM de 12832 MiB para 4096 tokens de contexto cabe en 13000 MiB disponibles' codigo=0 declarado='[ERROR] presupuesto de VRAM insuficiente: 20768 MiB para 131072 tokens de contexto frente a 13000 MiB disponibles' codigo_declarado=6` (`T-047`, `T-056`) | PASADO |
| `CB-008` | `CA-010` | `python -m unittest discover -s tools\gemma\tests -p "test_precheck.py"` | `test_precheck_perfil_especulativo_sin_borrador`: mensaje que nombra la alternativa sin decodificación especulativa y 0 lanzamientos del servidor (`T-010`, `T-053`) | PASADO |

Cobertura de la matriz: 14 de 14 requisitos funcionales, 7 de 7 requisitos no funcionales y 8 de 8 casos borde, con 29 de 29 filas en `PASADO`, y 0 marcadores pendientes en `tasks.md` (`81 de 81` tareas cerradas y la única casilla sin marcar es `G4` de `spec.md`, cuya aprobación no corresponde a un agente).

## Brechas

Sin brechas de requisito: los 14 requisitos funcionales, los 7 no funcionales y los 8 casos borde presentan evidencia `PASADO` y ninguna tarea queda abierta. Se registran las observaciones siguientes, que no abren brecha de requisito y que se declaran para que consten.

**Observaciones mayores**

- `O-01` — `RNF-007` (`specs/017-configuracion-gemma-4-26b-a4b/spec.md:158-160`). El requisito enuncia que «el número de cargas registradas con menos de 512 MiB de VRAM libre DEBE ser 0», y `results/gemma/` conserva 4 cargas registradas por debajo de ese umbral: campo 14 `56 MiB` en `20261122T203814Z-resiliencia-carga-inicial`, `389 MiB` en `20261124T174952Z-rendimiento-comparacion-micro-lote`, `53 MiB` en `20261124T175021Z-rendimiento-comparacion-micro-lote` y `336 MiB` en `20261124T192807Z-rendimiento-comparacion-contexto`. El corpus resuelve la tensión como condición de promoción —`CA-007`, `CB-004` y `test_promocion_vram_libre` exigen ≥512 MiB para promover y ordenan conservar la medición que lo incumple, y `RNF-004` prohíbe sobrescribirla—, de modo que el recuento literal no puede ser 0 sin destruir evidencia exigida por la misma spec. La configuración vigente cumple el umbral (`3889 MiB`). Se recomienda que el propietario reformule el recuento de `RNF-007` en una clarificación posterior, con el mismo tratamiento que `AMB-013` dio a `RNF-003`; el `reviewer` no modifica el requisito.
- `O-02` — Estado validado sin confirmar (`specs/017-configuracion-gemma-4-26b-a4b/`, `tools/gemma/`, `src/gemma/perfiles/`). `git status --short` devuelve 29 archivos modificados respecto de `4336d3c`, entre ellos `spec.md`, `plan.md`, `tasks.md`, `specs/INDEX.md`, `MEMORY.md`, los 4 perfiles, los 9 módulos de `tools/gemma/` y 11 suites de pruebas. El árbol es el que sostiene la evidencia de `T-037` a `T-083` y el que se ha validado; el commit firmado de G4 debe contenerlo, porque `--gate G4 --git` verifica el alcance declarado y la firma sobre el commit y no sobre el árbol de trabajo.
- `O-03` — `RNF-002` y la traza de la corrección editorial (`tasks.md:519`, `tasks.md:856`). `T-034` declara que la marca de orden de bytes «no existía; la línea 1 ya empezaba por `# `», mientras `T-044` transcribe `AssertionError: True is not false : RNF-002 exige 0 marcas de orden de bytes y el documento real empieza por b'\xef\xbb\xbf'`. Las dos transcripciones no pueden ser ciertas a la vez. La conformidad final se acredita por la re-ejecución del 2026-11-24 (`doble_codificacion=0 bom=0`) y no por una transcripción de la retirada: la corrección no consta atribuida a ninguna tarea —`T-044` declara como archivos `tools/gemma/tests/test_documento.py` y `tools/gemma/documento.py`, y ninguna tarea posterior a `T-035` declara escritura en `docs/gemma/`—, de modo que la autoría del cambio editorial queda sin traza en `tasks.md`.

**Observaciones menores y constancias de proceso**

- `O-04` — Reapertura por `T11` y orden de las transiciones (`spec.md:330-335`). La spec reabrió la clarificación el 2026-11-23 y las transiciones `T2`, `T3`, `T4` y `T5` se registran el 2026-11-24, después de que `T-060` a `T-083` estuvieran implementadas; las filas declaran esa causa y no se reescribieron las tareas ya cerradas. Consta, y la reapertura explica por qué la implementación precede a la transición. `clarify.md` incorpora `AMB-013` y sus parches con fecha del 2026-11-23.
- `O-05` — Tareas retiradas (`plan.md`, `DEC-029`; `tasks.md:23`). `T-038` y `T-040` se retiraron sin reutilizar identificador: `tasks.md` conserva 81 tareas de `T-001` a `T-083` con esos 2 huecos y `T-040` consta como retirada por duplicada; `T-038` consta en `DEC-029` y no en `tasks.md`.
- `O-06` — Registros de 21 filas (`DEC-027`). Los 5 registros escritos antes de la ampliación a 22 campos —`20261122T203814Z-resiliencia-carga-inicial` y las 4 comparaciones `20261123T144036Z`, `20261123T144108Z`, `20261123T144150Z` y `20261123T144232Z`— se conservan intactos y se leen con el campo 22 sintetizado en `no disponible`, sin escribir el archivo; es el tratamiento que exigen `RNF-004` y `CB-005` y consta en `C-6` y en `T-064`.
- `O-07` — Mediciones con configuraciones superadas. Se conservan y se citan como superadas, no como vigentes: las comparaciones de `ncmoe` `0`→`6` de `20261124T113511Z`/`113550Z` (rendimiento) y `20261123T171245Z`/`171321Z` (resiliencia), los presupuestos medidos con `ncmoe` `0` de `T-036` y con `ncmoe` `6` de `T-059` y `T-071`, los 2 registros defectuosos de micro-lote `20261124T174952Z`/`175021Z` (53-389 MiB libres) y el registro `20261124T182029Z-resiliencia-alternativa-contexto-menor` con los campos 16 y 17 en `no disponible`. `DEC-026`, `DEC-029` y `DEC-030` sustituyen sus valores sin reescribir los registros.
- `O-08` — Cláusula contradictoria en `T-043` (`tasks.md:845`). La evidencia declara «0 comprobaciones en estado `PENDIENTE`, que es el estado que la comprobación 4 reporta mientras 1 de los 3 manifiestos … conserva la clave `pendiente`»; la primera mitad es la correcta —`5 de 5`, sin `PENDIENTE`, como confirma la re-ejecución— y la subordinada describe el estado anterior a `T-083`.
- `O-09` — Sección «Resultado medido» del documento (`docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md:320-322`). Declara «Ningún perfil cuenta todavía con un registro de medición que sostenga este estado», mientras `results/gemma/` conserva 33 registros y 2 de ellos declaran la huella de opciones vigente del manifiesto (`71e631c2…` y `960ce0e9…`). `C-4` no obliga a promover a `medido` y los 3 perfiles declaran `candidato`, de modo que no se incumple `RF-005` ni `RF-007`; la frase, sin embargo, no describe el contenido de `results/gemma/`.
- `O-10` — Matriz del plan y suite (`plan.md`, fila de `RNF-001`). La matriz de cobertura cita `test_precheck_duracion` como verificación de `RNF-001`; esa prueba no existe en `tools/gemma/tests/`. La cobertura real es `SalidaTest.test_salida_formateada` —forma de la línea `TIEMPO: <n> ms`— más la ejecución real que este reporte mide (`Ran 1 test in 0.970s`).
- `O-11` — `RF-009` medido sobre la configuración anterior a `DEC-028` y `DEC-029`. El registro `20261124T160701Z-resiliencia-contexto-sostenido` declara 7 ejes, `flash_attn` `off` y `ncmoe` `6`, es decir la configuración previa a la declaración de los 2 ejes de caché y al cambio del valor inicial de la atención rápida; no se repitió la prueba de contexto sostenido con los 9 ejes vigentes. `RF-009` no fija las opciones y el registro se conserva por `RNF-004`, pero la cifra no describe la configuración que sirve el perfil.
- `O-12` — Alcance de `RNF-004` (`spec.md:148`). El requisito enuncia «el 100 % de las ejecuciones» con 1 archivo de registro propio; el modo `servir` no crea registro por diseño, y `T-043` lo verifica así (`0 líneas REGISTRO:`). La lectura aplicada es 1 registro por ejecución de medición (`C-5`), que es la que sostienen `T-024` y `T-025`. Es la misma clase de tensión que `O-01` y conviene alinearla al reformular el contrato.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos y casos borde con evidencia PASADO).
- [ ] NO CONVERGIDO.
