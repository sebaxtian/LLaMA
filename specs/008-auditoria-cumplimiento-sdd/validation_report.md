# Reporte de validación — SPEC-008

## Entorno

- Sistema operativo: Windows 11 (`win32`), PowerShell 5.1.26100.9818.
- Rama: `feat/auditoria-cumplimiento-sdd`.
- Commit auditado: `1d6b2c5a0424eff677d330c478c27628150d7106`, fijado antes de la escritura del informe; `git rev-parse HEAD` devuelve el mismo hash al cierre de esta verificación.
- Estado del árbol: el informe `docs/sdd/auditoria_cumplimiento_sdd.md` amplía la tabla 1.3 de dieciséis a veintitrés consultas y sigue sin registrar en el commit de corte; la validación se ejecuta sobre el árbol de trabajo y cada dato se contrasta contra el repositorio o contra el árbol de ese commit.
- Herramientas: Git 2.56.0.windows.3, Python 3.15.2, validador `tools\sdd\validate.py`, `Select-String`, `Get-ChildItem`, `Test-Path` y `git ls-tree` de PowerShell 5.1.
- Entregable auditado: `docs/sdd/auditoria_cumplimiento_sdd.md`, 1069 líneas, doce secciones de nivel 2.
- Artefactos leídos: `spec.md` (v0.4.0), `clarify.md` (AMB-001 a AMB-006), `plan.md` (DEC-001 a DEC-010, V1 a V23) y `tasks.md` (26 de 26).
- Alcance del rol: esta revisión no edita el informe, la spec, el plan ni las tareas; su única escritura es este reporte.
- Naturaleza: tercera revisión independiente. Cierra la brecha B-6 de la segunda revisión tras verificar las consultas C17 a C23 y el recuento de C13.

## Verificación de las correcciones

| Brecha | Corrección esperada | Comprobación ejecutada | Resultado |
|---|---|---|---|
| B-1 | Hallazgo de inventario en D1 como `AUD-007`, sin `AUD-092`, con D1 de siete hallazgos y D10 de tres, reflejado en 12.4 | `Select-String 'AUD-092'` devuelve 0 coincidencias; la fila D1 lista AUD-001 a AUD-007 y la fila D10 lista AUD-091, AUD-093 y AUD-094; 12.4 declara D1 con 7 y D10 con 3, con nota sobre el número 092 vacante | Cerrada |
| B-2 | G3 con 48 tareas cerradas y §8 con 4, 10, 5, 5, 9, 5 y 10 | G3 declara 48 tareas cerradas y 0 abiertas; «56 tareas» no aparece; los siete bloques de §8 coinciden con los encabezados `### T-NNN` y las casillas `- [x] Completada` de cada `tasks.md` | Cerrada |
| B-3 | `AUD-083` con el comando en orden `feat/...` a `dev` y salida `2 47` | `git rev-list --left-right --count feat/gemma-4-26b-a4b-it-qat-gguf...dev` devuelve `2` y `47`, igual a la cita del hallazgo y a la de la fila consolidada | Cerrada |
| B-4 | D5 y `AUD-044` con 26 merges y siete integraciones, conservando los siete hashes | `git log --merges --oneline dev` devuelve 26 líneas; D5 y `AUD-044` declaran 26 merges y los siete hashes de integración | Cerrada |
| B-5 | 2.3 y 12.1 con 21 archivos del corte, 6 nombres con 4 presentes y 2 fuera del periodo, 17 incluidos, 5 plantillas y 22 normativos; `AUD-007` con dos documentos omitidos | `git ls-tree --name-only 1d6b2c5 docs/sdd/` devuelve 21 archivos Markdown en la raíz; los dos nombres sin seguimiento no están en ese árbol; las dos tablas declaran 21, 6 con 4 y 2, 17, 5 y 22; `AUD-007` declara la omisión de dos documentos frente a los 19 del procedimiento | Cerrada |
| B-6 | Tabla 1.3 con las consultas que el cuerpo cita, C17 a C23 incluidas, y C13 con las ocho entradas del glob | La tabla registra 23 consultas de C1 a C23. C17 a C23 existen y se reproducen: `--all` declara la advertencia y `OK` con código `0`; `Get-ChildItem docs\sdd\plantillas -Filter *.md` devuelve 5; `Get-ChildItem .opencode\agents -Filter *.md` devuelve 5; la búsqueda de los tres estados intermedios no devuelve coincidencias; `Get-ChildItem .git\hooks` filtrado devuelve 0 archivos; `Test-Path main.bat` devuelve `True`; la búsqueda de `guia_maestra` no devuelve coincidencias. C13 declara las ocho entradas del glob, con 0, 5, 5, 0, 10, 0, 7 y 38. Cada comando citado en el cuerpo tiene consulta registrada sobre el mismo destino y la misma herramienta; las diferencias de parámetro constan en O-6 | Cerrada |
| B-7 | 12.2 con la línea `[WARN]` y el código 0 | La tabla y el bloque de 12.2 reproducen `[WARN] specs\008-auditoria-cumplimiento-sdd\validation_report.md: validation_report.md no existe` seguido de `OK: sin hallazgos.` con código `0` | Cerrada |
| B-8 | G5 acotada a las siete ramas integradas y con las dos `feat/*` presentes | La fila G5 limita la ausencia a las siete ramas de trabajo integradas y declara las dos ramas `feat/*` presentes; `git branch -a` lo confirma | Cerrada |

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| RF-001 | CA-001 | `git ls-tree --name-only 1d6b2c5 docs/sdd/` + lectura de 2.3 y 12.1 | 2.3 declara 21 archivos en la raíz del corte, 6 nombres excluidos con 4 presentes y 2 fuera del periodo, 17 incluidos, 5 plantillas y 22 normativos, con las 22 rutas enumeradas | PASADO |
| RF-002 | CA-001 | Lectura de 2.1 y del bloque `### AUD-002` | 2.1 sitúa `docs/constitution.md` en rango 1 y `AGENTS.md` en rango 2; AUD-002 registra en D1 la exclusión del documento de rango 3 sin alterar la jerarquía | PASADO |
| RF-003 | CA-002 | Recuento de filas de dimensión en las líneas 237-246 + V7 | Diez filas D1 a D10 en orden, cada una con veredicto de la escala de 3.2 | PASADO |
| RF-004 | CA-003 | V6, V11 y reejecución de la evidencia de G3 y G5 | Seis filas con condición, evidencia, declarante y verificación; G3 declara 48 tareas cerradas y G5 acota la ausencia a las siete ramas integradas | PASADO |
| RF-005 | CA-004 | Recuento de la tabla de §7 + V12 | 71 filas con las nueve columnas sin celdas vacías, `AUSENTE` en la columna `Commit` en las 71 y eslabón faltante con `AUD-NNN` | PASADO |
| RF-006 | CA-005 | `Select-String '^### SPEC-00[1-7]'` = 7 + lectura de §8 | Siete bloques con veredicto individual y recuentos de tareas 4, 10, 5, 5, 9, 5 y 10, coincidentes con cada `tasks.md` | PASADO |
| RF-007 | CA-006 | V8 y comprobación de unicidad y rangos con script sobre §5 | 41 identificadores únicos, 41 filas consolidadas con siete campos, 41 bloques `### AUD-NNN` con siete campos, D1 con 7 y D10 con 3 | PASADO |
| RF-008 | CA-006 | Reejecución de las consultas citadas por los hallazgos | `AUD-083` reproduce `2 47`, `AUD-044` reproduce los 26 merges y las restantes consultas citadas coinciden con el repositorio | PASADO |
| RF-009 | CA-007 | Lectura de 1.1, 1.3 y extracción de los comandos citados en el cuerpo | 1.1 declara fecha, rama y hash; 1.3 registra C1 a C23 y cada comando citado en el cuerpo tiene consulta registrada sobre el mismo destino y la misma herramienta; C13 declara las ocho entradas del glob, con SPEC-008 en 38 | PASADO |
| RF-010 | CA-008 | Lectura de 3.2, 3.3 y 3.4 + V23 | Cinco valores de veredicto, cuatro niveles de severidad y seis reglas de agregación ordenadas | PASADO |
| RF-011 | CA-008 | Lectura de §9 y contraste con la columna de veredicto de §4 | Regla 1 aplicada, ocho dimensiones `NO CONFORME` con hallazgo de severidad Alta o Crítica y veredicto global `NO CONFORME` | PASADO |
| RF-012 | CA-009 | Recuento de las 41 filas de remediación de §10 | Bloques B1 con 10 filas, B2 con 16, B3 con 9 y B4 con 6, sin bloques ajenos | PASADO |
| RF-013 | CA-009 | V14 sobre las 41 filas de remediación | 24 filas `requiere spec`, 9 `editorial` y 8 `proceso`; cada fila referencia un `AUD-NNN` existente | PASADO |
| RF-014 | CA-010 | `git status --short` + V15 | La única creación de la Etapa 6 es el informe; las modificaciones restantes son cuatro documentos previos de `docs/sdd/`, dos documentos previos sin seguimiento y `tasks.md` registrado por el rol planner | PASADO |
| RF-015 | CA-011 | V16 y lectura de §12.2 | No existen apartados dedicados a rendimiento, benchmarks, calidad de código ni revisión interna del validador; su cobertura se evalúa como mecanismo de control | PASADO |
| RF-016 | CA-012 | Contaje de filas de §11 y lectura de las cuatro columnas | Seis limitaciones con causa, artefacto que faltaría y dimensión o compuerta afectada | PASADO |
| RF-017 | CA-013 | AUD-081 a AUD-084 y `git log --merges` | Cuatro desviaciones de Git con referencia observable; el historial permanece sin reescritura y los identificadores citados siguen resolviendo | PASADO |
| RF-018 | CA-014 | Fila D6 y hallazgos AUD-051 a AUD-055 | Estados de las siete specs contrastados con el modelo del validador y cinco transiciones no permitidas registradas | PASADO |
| RF-019 | CA-015 | Fila D7, hallazgos AUD-061 a AUD-064 y §11 | Permisos declarados por rol contrastados con las operaciones observadas; la falta de atribución consta como limitación | PASADO |
| RNF-001 | CA-010 | V3 y V4 | Informe único en `docs/sdd/auditoria_cumplimiento_sdd.md`, en español, en Markdown y con doce secciones | PASADO |
| RNF-002 | CA-006 | V19 y muestreo de DEC-010 con reejecución de consultas | Las afirmaciones antes no sostenidas cuentan con evidencia que las reproduce: 48 tareas, `2 47`, 26 merges, 21 archivos del corte y alcance de G5 | PASADO |
| RNF-003 | CA-007 | V18, V19 y repetición de las consultas citadas | Las 23 consultas de 1.3 reproducen su salida y su código; 12.2 reproduce la salida íntegra de `--all` y el recuento de 2.3 se obtiene del árbol del corte | PASADO |
| RNF-004 | CA-008 | V20 con muestreo de DEC-010 sobre D4 y D5 | La revisión independiente obtiene `NO CONFORME` en D4 y D5 y las mismas severidades por hallazgo | PASADO |
| RNF-005 | CA-006 | Script de orden, unicidad y rangos sobre los 41 identificadores | Identificadores únicos y ascendentes, ordenados por dimensión y dentro del rango reservado de DEC-006; el número 092 queda vacante sin reasignación, declarado en 12.4 | PASADO |
| RNF-006 | CA-009 | V10 | Correspondencia bidireccional 41 a 41 entre hallazgos y remediaciones, sin huérfanos en ninguno de los dos sentidos | PASADO |
| RNF-007 | CA-006 | V9 y recuento por columna sobre la tabla consolidada | La tabla permite el recuento determinista por dimensión, severidad y veredicto: 4 Crítica, 13 Alta, 18 Media y 6 Baja | PASADO |
| CB-001 | CA-005 | Fila D3, §11 y control V15 | Las ausencias se citan como ausencia verificable con el comando que las demuestra y ningún artefacto se creó | PASADO |
| CB-002 | CA-004 | Lectura de §7 y comprobación de la columna de eslabón faltante | Cada eslabón ausente se declara con `AUD-NNN` y la cadena no se completa por inferencia | PASADO |
| CB-003 | CA-003 | Fila G5 de §6 y primera limitación de §11 | El elemento posterior al merge queda `NO VERIFICABLE` y G5 no se presume `CONFORME` | PASADO |
| CB-004 | CA-017 | AUD-003 a AUD-005 y fila D10 | Las contradicciones entre guía y plantilla se registran con el rango de cada documento y la resolución aplicable | PASADO |
| CB-005 | CA-016 | AUD-014 en D2 y AUD-094 en D10 | La divergencia entre el validador y la norma documental consta como hallazgo de D2 y de D10, con el validador tratado como evidencia de práctica | PASADO |
| CB-006 | CA-013 | AUD-081 a AUD-084 | Cada desviación conserva su referencia observable y el historial no se reescribió ni se eliminó evidencia | PASADO |
| CB-007 | CA-001 | Lectura de 2.4 y de las condiciones de §6 | Los seis excluidos se clasifican como referencia y ninguna condición de compuerta se apoya en un documento excluido | PASADO |
| CB-008 | CA-008 | Columna de veredicto de §4 | Ninguna dimensión carece de objeto evaluable, de modo que el valor `NO APLICA` no se activa y su regla consta en 3.2 | PASADO |
| CB-009 | CA-018 | `Select-String 'AUD-092'` = 0 + fila D1 + 12.4 | La diferencia entre inventario declarado y real consta como `AUD-007` en D1, D1 declara siete hallazgos y 12.4 refleja el traslado | PASADO |
| CB-010 | CA-010 | Lectura de 9.1 | Constancia de rechazo de correcciones y remisión a una especificación posterior | PASADO |
| CB-011 | CA-001 | AUD-002 y lectura de 2.4 | La exclusión del documento de rango 3 se registra como hallazgo de D1 y la jerarquía de 2.1 permanece intacta | PASADO |
| CB-012 | CA-007 | Lectura de 1.1, 1.3, 2.3 y AUD-084 | El corte se fijó antes del informe, los dos archivos sin seguimiento quedan fuera del periodo y el inventario de 2.3 se calcula sobre el árbol del corte | PASADO |

## Ejecución del validador determinista

- Ejecución al inicio de esta revisión, con el reporte de la segunda revisión en disco: `python tools\sdd\validate.py --spec SPEC-008 --gate G4` devuelve código de salida `1` con dos entradas, una por el dictamen `NO CONVERGIDO` anterior y otra por la fila `RF-009` en `FALLADO`.
- Ejecución de cierre, con este reporte: `python tools\sdd\validate.py --spec SPEC-008 --gate G4` devuelve `OK: sin hallazgos.` con código de salida `0`: las 38 filas de la matriz están en `PASADO` y el dictamen marcado es `CONVERGIDO`.

## Registro de las comprobaciones V1 a V23

| # | Comprobación | Resultado | Observación |
|---|---|---|---|
| V1 | `python tools\sdd\validate.py --spec SPEC-008 --gate G3` | PASADO | `OK: sin hallazgos.` con código de salida `0` |
| V2 | `python tools\sdd\validate.py --all` | PASADO | Código de salida `0`, sin advertencias sobre SPEC-008 |
| V3 | `Test-Path docs/sdd/auditoria_cumplimiento_sdd.md` | PASADO | `True` |
| V4 | `(Select-String -Path ... -Pattern '^## ').Count` | PASADO | `12` |
| V5 | Filas de dimensión | PASADO (con salvedad) | Diez filas D1 a D10 en las líneas 237 a 246; el patrón literal del plan devuelve 28 porque también captura las tablas de §9 y de 12.4 |
| V6 | Recuento de filas de compuerta | PASADO | `6` |
| V7 | Veredicto por dimensión en la escala de 3.2 | PASADO | Diez de diez con `NO CONFORME` o `PARCIAL` |
| V8 | Siete campos por hallazgo | PASADO | 41 filas consolidadas sin celdas vacías y 41 bloques de detalle con siete campos cada uno |
| V9 | Coincidencia de recuentos de §5 | PASADO (con salvedad) | 41 filas de datos y 41 bloques; el patrón literal del plan devuelve 42 porque incluye la fila de cabecera `AUD-NNN` |
| V10 | Cobertura de remediaciones | PASADO | 41 identificadores en la tabla consolidada y 41 en la hoja de ruta, con diferencia simétrica vacía |
| V11 | Compuertas completas | PASADO | Seis filas con seis columnas con contenido y resultado de la escala |
| V12 | Trazabilidad sin celdas vacías | PASADO | 71 filas y 9 columnas sin celdas vacías; el eslabón faltante sigue el esquema de `plan.md:158` |
| V13 | Commit citado | PASADO | `git rev-parse HEAD` devuelve `1d6b2c5a0424eff677d330c478c27628150d7106`, idéntico al hash de 1.1 |
| V14 | Clasificación de remediaciones | PASADO | Bloques B1 a B4 y clasificaciones `editorial`, `requiere spec` y `proceso` sin valores ajenos |
| V15 | Alcance de escritura | PASADO | `git status --short`: `?? docs/sdd/auditoria_cumplimiento_sdd.md` como única creación; las demás entradas coinciden con la lista previa y con `tasks.md` registrado por el rol planner |
| V16 | Sin contenido fuera de alcance | PASADO | No hay apartados de rendimiento, benchmarks, calidad de código ni lógica interna; la constancia de rechazo está en 9.1 |
| V17 | Sin léxico ambiguo | PASADO | Cero coincidencias de los diez términos que `docs/sdd/PROTOCOLO_OPERATIVO.md:112` prohíbe en RF, RNF y CA |
| V18 | Repetición de consultas | PASADO (con salvedad) | C1, C2, C4 a C16 y C18 a C23 reproducen su salida y su código; C3, C14 y C17 son instantáneas tomadas antes de existir el informe, y por eso C17 ya no emite la advertencia |
| V19 | Repetición de citas | PASADO | Se abrieron `docs/constitution.md:48`, `docs/sdd/compendio_sdd.md:3`, `tools/sdd/validate.py:78`, `specs/001-main-menu/spec.md:95` y `CHANGELOG.md:25`, y los extractos existen |
| V20 | Determinismo del veredicto | PASADO | La revisión independiente de D4 y de D5 con el muestreo de DEC-010 obtiene `NO CONFORME` en ambas y las mismas severidades; las ocho brechas de las revisiones anteriores están cerradas y verificadas |
| V21 | Limitaciones completas | PASADO | G5 es la única compuerta con evidencia no conservada y aparece en §11 con causa y artefacto faltante; no hay dimensión `NO VERIFICABLE` |
| V22 | Base normativa declarada | PASADO | Los seis nombres excluidos, la jerarquía y el recuento de 21 archivos del corte con 17 incluidos y 5 plantillas coinciden con la regla de DEC-001 y con `git ls-tree` |
| V23 | Escalas declaradas | PASADO | Cinco veredictos, cuatro severidades y seis reglas de agregación ordenadas |

## Brechas

No hay brechas pendientes: las 38 filas de la matriz están en `PASADO`.

### Brechas cerradas

- **B-1** cerrada: `AUD-092` sin coincidencias, `AUD-007` en D1, D1 con siete hallazgos, D10 con tres y 12.4 con el traslado declarado.
- **B-2** cerrada: G3 declara 48 tareas y §8 declara 4, 10, 5, 5, 9, 5 y 10, sin rastro de «56 tareas».
- **B-3** cerrada: el comando declarado en `AUD-083` devuelve `2 47` con el orden de referentes que el propio hallazgo cita.
- **B-4** cerrada: `git log --merges --oneline dev` devuelve 26 líneas y D5 y `AUD-044` declaran 26 merges con las siete integraciones identificadas.
- **B-5** cerrada: 2.3 y 12.1 declaran 21 archivos del corte, 6 nombres con 4 presentes y 2 fuera del periodo, 17 incluidos, 5 plantillas y 22 normativos, y `AUD-007` declara la omisión de dos documentos.
- **B-6** cerrada: 1.3 registra 23 consultas, C17 a C23 cubren los comandos que faltaban y C13 declara las ocho entradas del glob, con SPEC-008 en 38.
- **B-7** cerrada: 12.2 reproduce la línea `[WARN]` y el código `0` de la ejecución real.
- **B-8** cerrada: G5 acota la ausencia a las siete ramas integradas y reconoce las dos ramas `feat/*` presentes.

### Observaciones no bloqueantes

- **O-1.** La justificación de D7 cita `.opencode/agents/sdd.md:3` y `.opencode/agents/documenter.md:3` (`docs/sdd/auditoria_cumplimiento_sdd.md:243`) para sostener que la matriz declara cinco roles; esas líneas solo registran el campo `mode`. La matriz con cinco filas está en `docs/sdd/PROTOCOLO_OPERATIVO.md:164-170` del commit de corte.
- **O-2.** La justificación de D10 atribuye 61 líneas útiles a `AGENTS.md` (`docs/sdd/auditoria_cumplimiento_sdd.md:246`); el archivo tiene 61 líneas y 42 no vacías, de modo que el rango de `docs/constitution.md:39` se cumple en ambas lecturas.
- **O-3.** La evidencia de `T-017` en `specs/008-auditoria-cumplimiento-sdd/tasks.md:274` mantiene la distribución 4 Crítica, 14 Alta, 17 Media y 6 Baja; la tabla consolidada arroja 4, 13, 18 y 6. El dato no figura en el informe y el recuento determinista de `RNF-007` se cumple sobre la tabla.
- **O-4.** Los patrones literales de V5 y V9 en `plan.md` siguen sin acotarse a la sección que pretenden medir: V5 cuenta además las tablas de §9 y 12.4 y V9 incluye la fila de cabecera.
- **O-5.** La salida declarada de C14 corresponde al árbol previo a la escritura del informe; una vez creado, `Get-ChildItem docs\sdd -Filter *.md -File` devuelve 24 archivos en la raíz. Conviene declarar C3, C14 y C17 como instantáneas, del mismo modo que C3 ya se declara como cambio previo al corte.
- **O-6.** Cuatro citas del cuerpo usan un parámetro más estrecho que su consulta registrada: D2 cita el patrón `'implemented'` frente a C20 con `'implementing|implemented|validated'`; `AUD-093` cita `'guia_maestra_sdd'` frente a C23 con `'guia_maestra'`; D5 y `AUD-044` citan `git log --merges --oneline` sin referente frente a C7 con `dev`, y ambas formas devuelven 26; y `AUD-041` cita la instancia `specs\001-main-menu\tasks.md` del glob de C13. La consulta registrada reproduce el resultado en los cuatro casos y ninguna afirmación cambia.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos con evidencia PASADO).
- [ ] NO CONVERGIDO.

Requisitos en estado PASADO: 38 de 38. Requisitos en estado FALLADO: ninguno. Requisitos en estado NO VERIFICABLE: ninguno. Las ocho brechas de las revisiones anteriores están cerradas y verificadas contra el repositorio, y la última corrección, la relación de consultas de 1.3, permite reproducir cada verificación declarada en el informe.

El veredicto global del informe auditado se mantiene en `NO CONFORME`: esta convergencia es la de la especificación de auditoría, no un cambio del diagnóstico que el informe emite sobre el periodo auditado.

## Aprobación

- [x] G4: `- Approved by: Agent Sebaxtian` (2026-11-14)
