## 1. Ficha de reproducibilidad

### 1.1 Fecha y commit de corte

| Campo | Valor |
|---|---|
| Fecha de corte | `2026-11-14` |
| Rama auditada | `feat/auditoria-cumplimiento-sdd` |
| Hash completo del commit de corte | `1d6b2c5a0424eff677d330c478c27628150d7106` |
| Hash abreviado | `1d6b2c5` |
| Asunto del commit | `docs(sdd): contrato de auditoria de cumplimiento SPEC-008` |

El commit de corte se fijó antes de la escritura de este informe y es la referencia temporal de cada cita posterior (`specs/008-auditoria-cumplimiento-sdd/plan.md:50`, `specs/008-auditoria-cumplimiento-sdd/spec.md:251`). El hash abreviado es el prefijo de siete caracteres del hash completo.

La consulta `git show --stat --oneline HEAD` (código de salida `0`) registra cinco archivos y 1326 inserciones:

| Archivo | Inserciones |
|---|---|
| `specs/008-auditoria-cumplimiento-sdd/clarify.md` | 87 |
| `specs/008-auditoria-cumplimiento-sdd/plan.md` | 426 |
| `specs/008-auditoria-cumplimiento-sdd/spec.md` | 387 |
| `specs/008-auditoria-cumplimiento-sdd/tasks.md` | 425 |
| `specs/INDEX.md` | 1 |

### 1.2 Entorno

| Componente | Valor |
|---|---|
| Sistema operativo | Windows 11 (`win32`) |
| Rama de trabajo | `feat/auditoria-cumplimiento-sdd` |
| Intérprete de verificación | Python, invocado como `python` desde la raíz del repositorio |
| Validador del proyecto | `tools\sdd\validate.py`, ejecutado como `python tools\sdd\validate.py` |
| Historial consultado | Repositorio Git de la raíz del proyecto, con `git` como cliente de solo lectura |
| Directorio de ejecución | Raíz del repositorio; las rutas de las tablas son relativas a esa raíz |

Las consultas de esta ficha se ejecutaron sobre el árbol de trabajo y el historial del repositorio, sin escritura y sin consultas remotas.

### 1.3 Consultas ejecutadas

| Consulta | Comando literal | Propósito | Salida | Código de salida | Sección que la emplea |
|---|---|---|---|---|---|
| C1 | `git rev-parse HEAD` | Fijar el identificador del commit de corte | `1d6b2c5a0424eff677d330c478c27628150d7106` | `0` | 1.1 |
| C2 | `git show --stat --oneline HEAD` | Registrar los archivos y las inserciones del commit de corte | `1d6b2c5 docs(sdd): contrato de auditoria de cumplimiento SPEC-008` con cinco archivos y 1326 inserciones | `0` | 1.1 |
| C3 | `git status --short` | Registrar los cambios no incluidos en el commit de corte | Seis entradas, transcritas abajo | `0` | 1.3, D9 y D10 |
| C4 | `python tools\sdd\validate.py --spec SPEC-008 --gate G2` | Comprobar el contrato de la spec frente a la compuerta G2 | `OK: sin hallazgos.` | `0` | 12.2 |
| C5 | `git ls-tree --name-only 1d6b2c5 docs/sdd/` | Fijar el inventario de la raíz de `docs/sdd/` en el commit de corte | 21 archivos Markdown | `0` | 2.3 y 12.1 |
| C6 | `git branch -a` | Registrar las ramas locales y las referencias remotas | Ramas locales y referencias remotas, entre ellas `remotes/origin/release/v0-6-0` | `0` | D9 y 12.3 |
| C7 | `git log --merges --oneline dev` | Registrar las fusiones del historial de integración | 26 merges con dos padres, siete de ellos de spec | `0` | D5, 6, 7 y 12.3 |
| C8 | `git rev-list --left-right --count dev...main` | Medir la divergencia entre `dev` y `main` | `0 1` | `0` | D9 |
| C9 | `git rev-list --left-right --count feat/gemma-4-26b-a4b-it-qat-gguf...dev` | Medir la divergencia de la rama de trabajo local | `2 47` | `0` | D9 |
| C10 | `git tag --list` | Registrar los tags del periodo | Ocho tags anotados, de `v0.1.0` a `v0.6.0` | `0` | 6, D9 y 12.3 |
| C11 | `Select-String -Path .opencode\agents\*.md -Pattern 'mode:'` | Contrastar los permisos declarados por rol | Cinco coincidencias: un `primary`, dos `all` y dos `subagent` | `0` | D7 |
| C12 | `Select-String -Path tools\sdd\validate.py -Pattern 'Approved'` | Comprobar si el validador verifica la aprobación de G1 | Sin coincidencias | `0` | D4 y 6 |
| C13 | `Select-String -Path specs\*\tasks.md -Pattern 'CA-\d{3}'` | Contar las referencias a criterios de aceptación en las tareas | 0 en SPEC-001, SPEC-004 y SPEC-006; 5 en SPEC-002 y SPEC-003; 10 en SPEC-005; 7 en SPEC-007; 38 en SPEC-008 | `0` | D5 y 8 |
| C14 | `Get-ChildItem docs\sdd -Filter *.md -File` | Comparar el árbol de trabajo con el inventario del corte | 23 archivos en la raíz, dos de ellos sin seguimiento y fuera del periodo | `0` | 2.3 |
| C15 | `Test-Path .github\workflows` | Comprobar la existencia de integración continua | `False` | `0` | D8 |
| C16 | `Select-String -Path specs\00*\spec.md -Pattern '^version:'` | Registrar la versión declarada por cada spec | 0.1.0, 0.12.0, 0.6.0, 0.9.0, 0.6.0, 0.6.0 y 0.2.0 | `0` | D6 |
| C17 | `python tools\sdd\validate.py --all` | Validar el conjunto de specs | `[WARN] specs\008-auditoria-cumplimiento-sdd\validation_report.md: validation_report.md no existe` seguido de `OK: sin hallazgos.` | `0` | 12.2 |
| C18 | `Get-ChildItem docs\sdd\plantillas -Filter *.md` | Contar las plantillas normativas | `5` | `0` | 2.3 y 12.1 |
| C19 | `Get-ChildItem .opencode\agents -Filter *.md` | Contar los roles declarados | `5` | `0` | 4 y D7 |
| C20 | `Select-String -Path .opencode\commands\*.md,.opencode\agents\*.md -Pattern 'implementing\|implemented\|validated'` | Comprobar si algún rol escribe los estados intermedios | Sin coincidencias | `0` | 4 y D6 |
| C21 | `Get-ChildItem .git\hooks -File \| Where-Object { $_.Name -notlike '*.sample' }` | Comprobar hooks activos | Sin archivos | `0` | 4 y D8 |
| C22 | `Test-Path main.bat` | Comprobar la existencia del menú principal | `True` | `0` | 4 y D10 |
| C23 | `Select-String -Path docs\sdd\README.md -Pattern 'guia_maestra'` | Comprobar si la guía maestra está indexada | Sin coincidencias | `0` | 4 y D10 |

Transcripción literal de la salida de C3:

```text
 M docs/sdd/PROTOCOLO_OPERATIVO.md
 M docs/sdd/README.md
 M docs/sdd/diagrama_flujo_ciclo_vida_sdd.md
 M docs/sdd/guia_maestra_sdd.md
?? docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md
?? docs/sdd/plan_cierre_brechas_sdd.md
```

Las seis entradas de C3 son cambios previos al corte y quedan fuera del periodo auditado; se consignan como evidencia de las dimensiones D9 y D10 (`specs/008-auditoria-cumplimiento-sdd/spec.md:251`, `specs/008-auditoria-cumplimiento-sdd/tasks.md:50`).

## 2. Base normativa e inventario

### 2.1 Jerarquía aplicada

`docs/constitution.md:43` abre la sección `## 6. Jerarquía normativa` y `docs/constitution.md:45` fija la regla de prevalencia del documento de mayor rango. La tabla reproduce el orden declarado en ese bloque:

| Documento | Rango | Cita |
|---|---|---|
| `docs/constitution.md` | 1 | `docs/constitution.md:48` |
| `AGENTS.md` | 2 | `docs/constitution.md:49` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | `docs/constitution.md:50` |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | `docs/constitution.md:51` |
| Documento maestro técnico | 5 | `docs/constitution.md:52` |
| `specs/NNN-slug/spec.md` | 6 | `docs/constitution.md:53` |
| `clarify.md`, `plan.md` y `tasks.md` | 7 | `docs/constitution.md:54` |
| `validation_report.md` | 8 | `docs/constitution.md:55` |
| Código | 9 | `docs/constitution.md:56` |

`docs/constitution.md` es la norma suprema aplicada por esta auditoría y `AGENTS.md` ocupa el rango inmediatamente inferior. `AGENTS.md:3` declara que la norma suprema es `docs/constitution.md` y que el procedimiento SDD es `docs/sdd/PROTOCOLO_OPERATIVO.md`; `AGENTS.md:17` registra las aprobaciones humanas de G1, G4 y G6. La base documental inventariada en 2.3 se sitúa por debajo de ambos documentos y no los sustituye (`specs/008-auditoria-cumplimiento-sdd/spec.md:40`).

### 2.2 Regla de inclusión

La base normativa se define por regla y no por recuento: es norma cada documento Markdown de la raíz de `docs/sdd/` cuyo nombre no figure en la lista de exclusiones por nombre exacto, más cada documento Markdown de `docs/sdd/plantillas/` (`specs/008-auditoria-cumplimiento-sdd/spec.md:27`, `specs/008-auditoria-cumplimiento-sdd/plan.md:249`). La especificación declara de forma expresa que no fija número de documentos (`specs/008-auditoria-cumplimiento-sdd/spec.md:38`).

| Criterio | Regla aplicada |
|---|---|
| Ubicación | Raíz de `docs/sdd/` y subdirectorio `docs/sdd/plantillas/` |
| Extensión | `.md`, filtrada por nombre de archivo |
| Inclusión | Nombre ausente de la lista de seis exclusiones de `specs/008-auditoria-cumplimiento-sdd/spec.md:31-36` |
| Exclusión | Coincidencia con un elemento de esa lista, aplicada por nombre de archivo |
| Recuento | Calculado en la fecha de corte; la especificación no prefija cifra |

La regla se aplica en el commit de corte de 1.1, de modo que el recuento resulta reproducible por un tercero con el mismo árbol y la misma lista de exclusión.

### 2.3 Inventario calculado

Aplicada la regla de 2.2 sobre el árbol del commit de corte `1d6b2c5` en la fecha `2026-11-14`, el resultado es:

| Magnitud | Valor |
|---|---|
| Archivos Markdown en la raíz de `docs/sdd/` en el corte | 21 |
| Nombres excluidos | 6, de los cuales 4 están presentes en el corte y 2 quedan fuera del periodo |
| Documentos normativos incluidos de la raíz | 17 |
| Plantillas de `docs/sdd/plantillas/` | 5 |
| Total de documentos normativos | 22 |

Documentos normativos del inventario:

| Ruta | Origen |
|---|---|
| `docs/sdd/compendio_sdd.md` | raíz |
| `docs/sdd/diagrama_secuencia_subagentes_sdd.md` | raíz |
| `docs/sdd/evolucion_sdlc_a_sdd.md` | raíz |
| `docs/sdd/guia_agents_md.md` | raíz |
| `docs/sdd/guia_clarify_md.md` | raíz |
| `docs/sdd/guia_constitution_md.md` | raíz |
| `docs/sdd/guia_fase_implement_tdd.md` | raíz |
| `docs/sdd/guia_metodo_ears_sdd.md` | raíz |
| `docs/sdd/guia_plan_md.md` | raíz |
| `docs/sdd/guia_servidores_mcp.md` | raíz |
| `docs/sdd/guia_skills_agentes_sdd.md` | raíz |
| `docs/sdd/guia_spec_md.md` | raíz |
| `docs/sdd/guia_subagentes_opencode_sdd.md` | raíz |
| `docs/sdd/guia_tasks_md.md` | raíz |
| `docs/sdd/mapa_mental_sdd.md` | raíz |
| `docs/sdd/referencia_7_etapas_sdd.md` | raíz |
| `docs/sdd/referencia_ciclo_vida_sdd_puro.md` | raíz |
| `docs/sdd/plantillas/clarify.md` | plantillas |
| `docs/sdd/plantillas/plan.md` | plantillas |
| `docs/sdd/plantillas/spec.md` | plantillas |
| `docs/sdd/plantillas/tasks.md` | plantillas |
| `docs/sdd/plantillas/validation_report.md` | plantillas |

El recuento declarado rige para la fecha de corte de 1.1 y se obtiene del filtro por extensión sobre la raíz de `docs/sdd/`, más el recuento de `docs/sdd/plantillas/`, menos la lista de exclusión por nombre (DEC-001, `specs/008-auditoria-cumplimiento-sdd/plan.md:249`). El recuento se calcula sobre el árbol del commit de corte con `git ls-tree --name-only 1d6b2c5 docs/sdd/`, que lista los 21 archivos; los dos documentos sin seguimiento de 1.3 no forman parte de ese árbol y quedan fuera del periodo.

### 2.4 Documentos excluidos

La especificación enumera seis documentos de `docs/sdd/` excluidos de la base normativa (`specs/008-auditoria-cumplimiento-sdd/spec.md:29-36`). De los seis, cuatro están presentes en el árbol del corte y dos quedan fuera del periodo por carecer de seguimiento (1.3). Cada uno se clasifica como referencia y no se emplea como criterio de conformidad (`specs/008-auditoria-cumplimiento-sdd/spec.md:231`).

| Documento | Clase | Uso admitido en el informe |
|---|---|---|
| `docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md` | Referencia | Contraste descriptivo del estado del proceso; no fija criterio de conformidad |
| `docs/sdd/diagrama_flujo_ciclo_vida_sdd.md` | Referencia | Apoyo gráfico del ciclo; no fija criterio de conformidad |
| `docs/sdd/guia_maestra_sdd.md` | Referencia | Guía de lectura del corpus; no fija criterio de conformidad |
| `docs/sdd/plan_cierre_brechas_sdd.md` | Referencia | Propuesta de cierre de brechas; no fija criterio de conformidad |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | Referencia | Evidencia de la práctica declarada; no fija criterio de conformidad |
| `docs/sdd/README.md` | Referencia | Índice de navegación del corpus; no fija criterio de conformidad |

La exclusión de `docs/sdd/PROTOCOLO_OPERATIVO.md` como norma, pese a su rango 3 declarado en `docs/constitution.md:50`, se registra como hallazgo de la dimensión D1 en la sección 5 (`specs/008-auditoria-cumplimiento-sdd/spec.md:103`) y no modifica la jerarquía expuesta en 2.1.

### 2.5 Artefactos de evidencia de práctica

| Artefacto | Clase de evidencia | Objeto citado |
|---|---|---|
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | E3 | Procedimiento declarado y su contraste con la práctica observada |
| `tools/sdd/validate.py` | E3 | Salida del validador determinista y divergencias frente a la norma documental |
| `.opencode/agents/` | E3 | Permisos y alcance declarados por rol en la configuración de agentes |
| `specs/` | E2 y E3 | E2 para `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`; E3 para `specs/INDEX.md` y para las casillas de evidencia de `tasks.md` |
| Historial de Git | E4 | Comandos con su salida y su código de salida: commits, fusiones, tags y estado del árbol |

Las citas de estas fuentes se registran con el formato de `specs/008-auditoria-cumplimiento-sdd/plan.md:70-74`. La suficiencia se rige por `specs/008-auditoria-cumplimiento-sdd/plan.md:78-81`: cada afirmación de conformidad exige una cita de clase E1 o E2 verificable en el commit de corte, cada afirmación de incumplimiento exige una cita de la norma y una de la práctica observada, y la evidencia insuficiente produce `NO VERIFICABLE` sin presunción de cumplimiento.

## 3. Criterio de evaluación y escalas

### 3.1 Regla de evaluación por dimensión

Cada dimensión de D1 a D10 se evalúa por separado, con su objeto declarado y su veredicto propio; esta sección fija la decisión y las escalas, y no repite la definición de las dimensiones (`specs/008-auditoria-cumplimiento-sdd/plan.md:52`).

1. Se reúne la evidencia del commit de corte correspondiente al objeto de la dimensión.
2. Se contrasta la práctica observada con la disposición normativa citada con `ruta:línea` (`specs/008-auditoria-cumplimiento-sdd/plan.md:78-80`).
3. Se asigna a la dimensión un veredicto de la escala de 3.2, con la precedencia `NO CONFORME`, después `NO VERIFICABLE`, después `PARCIAL`, después `CONFORME` (`specs/008-auditoria-cumplimiento-sdd/plan.md:200`, `specs/008-auditoria-cumplimiento-sdd/plan.md:289`).
4. Cada hallazgo que sostiene el veredicto recibe la severidad de 3.3 y un identificador del rango reservado a su dimensión (`specs/008-auditoria-cumplimiento-sdd/plan.md:171-184`).
5. La falta de evidencia para decidir produce `NO VERIFICABLE` y nunca una presunción de cumplimiento (`specs/008-auditoria-cumplimiento-sdd/plan.md:83`).

### 3.2 Escala de veredicto

| Veredicto | Regla de decisión |
|---|---|
| `CONFORME` | La dimensión no registra hallazgos y cada caso evaluable cuenta con evidencia verificable en el commit de corte |
| `PARCIAL` | La dimensión registra al menos un hallazgo de severidad Media o Baja, o incumple en una parte de los casos evaluables sin superar la mitad, o un subconjunto acotado carece de evidencia |
| `NO CONFORME` | La dimensión registra al menos un hallazgo de severidad Alta o Crítica, o incumple en más de la mitad de los casos evaluables |
| `NO VERIFICABLE` | La dimensión carece de evidencia para decidir el conjunto de sus casos evaluables |
| `NO APLICA` | La dimensión carece de objeto evaluable en el periodo auditado, con justificación de la ausencia de objeto |

Las cinco reglas proceden de `specs/008-auditoria-cumplimiento-sdd/plan.md:192-198`. Cuando dos reglas concurren, se aplica el orden de precedencia de 3.1.

### 3.3 Escala de severidad

| Severidad | Criterio de asignación |
|---|---|
| Crítica | El hallazgo anula una compuerta o permite un cambio sin spec aprobada |
| Alta | El hallazgo rompe la trazabilidad de requisitos o la evidencia de verificación |
| Media | El hallazgo deja un contrato de artefacto incompleto sin pérdida de trazabilidad |
| Baja | El hallazgo produce una inconsistencia editorial o documental menor |

Los cuatro niveles proceden de `specs/008-auditoria-cumplimiento-sdd/plan.md:204-209`. La severidad se asigna por el efecto observado y no por el número de ocurrencias: se elige el nivel más alto cuya definición coincida con el efecto y el efecto se declara en el campo correspondiente del hallazgo (`specs/008-auditoria-cumplimiento-sdd/plan.md:211`, `specs/008-auditoria-cumplimiento-sdd/plan.md:289`).

### 3.4 Regla de agregación

La tabla se evalúa de arriba abajo y se aplica la primera regla que se cumpla; el veredicto de esa fila es el veredicto global del informe (`specs/008-auditoria-cumplimiento-sdd/plan.md:215`, `specs/008-auditoria-cumplimiento-sdd/plan.md:253`).

| Orden | Condición | Veredicto global |
|---|---|---|
| 1 | Existe al menos una dimensión `NO CONFORME` con al menos un hallazgo de severidad Crítica o Alta | `NO CONFORME` |
| 2 | Ninguna dimensión es `CONFORME`, `PARCIAL` ni `NO CONFORME`, y al menos una es `NO VERIFICABLE` | `NO VERIFICABLE` |
| 3 | Existe al menos una dimensión `NO CONFORME` con hallazgos exclusivamente de severidad Media o Baja | `PARCIAL` |
| 4 | Existe al menos una dimensión `PARCIAL` o `NO VERIFICABLE` y ninguna dimensión `NO CONFORME` | `PARCIAL` |
| 5 | Cada dimensión es `CONFORME` o `NO APLICA`, y al menos una es `CONFORME` | `CONFORME` |
| 6 | Cada dimensión es `NO APLICA` | `NO APLICA` |

Las seis reglas proceden de `specs/008-auditoria-cumplimiento-sdd/plan.md:217-224`. La sección 9 enuncia la regla aplicada y enumera las dimensiones que la activan (`specs/008-auditoria-cumplimiento-sdd/plan.md:59`).

## 4. Matriz de dimensiones D1 a D10

La matriz evalúa las diez dimensiones con el objeto declarado en `specs/008-auditoria-cumplimiento-sdd/spec.md:44-55`, el veredicto de la escala de 3.2 y una justificación con cita en cada oración que afirma un hecho. El orden de las filas y el de los identificadores de la sección 5 siguen el rango reservado a cada dimensión (`specs/008-auditoria-cumplimiento-sdd/plan.md:171-184`).

| Dimensión | Objeto | Veredicto | Justificación | Hallazgos asociados |
|---|---|---|---|---|
| D1 | Autoridad normativa: jerarquía declarada, vigencia y aplicabilidad de cada documento | `NO CONFORME` | Diecisiete documentos de la base se autodeclaran «Documento de referencia (no normativo)» en su línea 3 (`docs/sdd/compendio_sdd.md:3`, `docs/sdd/guia_spec_md.md:3`), mientras la sección 2 les atribuye fuerza normativa. La base excluye un documento que la constitución sitúa en rango 3 (`docs/constitution.md:50`; `specs/008-auditoria-cumplimiento-sdd/spec.md:35`) y registra tres contradicciones entre guías y plantillas (`docs/sdd/guia_spec_md.md:148-151` frente a `docs/sdd/plantillas/spec.md:51-57`). | AUD-001, AUD-002, AUD-003, AUD-004, AUD-005, AUD-006, AUD-007 |
| D2 | Ciclo de 7 etapas: secuencia, artefacto de salida y estado resultante por etapa | `NO CONFORME` | El ciclo está declarado con su artefacto y su responsable (`docs/sdd/referencia_ciclo_vida_sdd_puro.md:77-85`), pero los comandos y el agente SDD fijan condiciones de entrada incompatibles (`.opencode/commands/sdd-implement.md:8` frente a `.opencode/agents/sdd.md:88`). G4 se ejecuta antes de existir el reporte que la propia compuerta exige (`specs/003-validacion-g4/validation_report.md:35-39`) y ninguna orden escribe los estados `implementing`, `implemented` ni `validated` (`Select-String -Path .opencode\commands\*.md,.opencode\agents\*.md -Pattern 'implemented'` no devuelve coincidencias). | AUD-011, AUD-012, AUD-013, AUD-014 |
| D3 | Contratos de artefactos: campos, secciones y prohibiciones de cada artefacto | `PARCIAL` | Las siete specs publicadas reúnen los cinco artefactos, pero dos contratos quedan incompletos: la plantilla de tareas no porta el criterio de aceptación (`docs/sdd/plantillas/tasks.md:12`) y el registro de G4 se reparte entre dos plantillas (`docs/sdd/plantillas/spec.md:63`; `docs/sdd/plantillas/validation_report.md:27`). El registro de G4 en los reportes diverge entre specs (`specs/001-main-menu/validation_report.md:36` frente a `specs/005-compuertas-completas/validation_report.md:73`) y no existe contrato para la documentación analítica (`Get-ChildItem docs\sdd\plantillas -Filter *.md` devuelve cinco plantillas). | AUD-021, AUD-022, AUD-023 |
| D4 | Compuertas G1 a G6: condición, evidencia, declarante y verificación | `NO CONFORME` | Las siete specs registran la aprobación de G1 (`specs/001-main-menu/spec.md:95`; `specs/007-branch-protection/spec.md:231`), pero el validador no comprueba la cadena `Approved` (`Select-String -Path tools\sdd\validate.py -Pattern 'Approved'` no devuelve coincidencias). G5 y G6 comparten la verificación de G4 (`tools/sdd/validate.py:78`) y `python tools\sdd\validate.py --all` devuelve `OK: sin hallazgos.` con código `0`. | AUD-031, AUD-032, AUD-033, AUD-034, AUD-035 |
| D5 | Trazabilidad: cadena RF/CB → CA → T → evidencia → commit → merge → release | `NO CONFORME` | Las siete specs declaran líneas `Cubre:` para sus criterios, pero tres no mencionan ningún CA en sus tareas (`Select-String -Path specs\001-main-menu\tasks.md -Pattern 'CA-\d{3}'` no devuelve coincidencias). El eslabón con el commit solo produce advertencia (`tools/sdd/validate.py:517-519`) y ningún artefacto declara el merge que integra cada spec (el historial contiene 26 merges con dos padres; siete integran una spec de SPEC-001 a SPEC-007). | AUD-041, AUD-042, AUD-043, AUD-044 |
| D6 | Estados y transiciones: modelo declarado frente a estados observados | `NO CONFORME` | El validador admite diez estados (`tools/sdd/validate.py:25-36`) y solo comprueba la pertenencia al conjunto (`tools/sdd/validate.py:299-300`). Las siete specs están en `released` y SPEC-002 registra una reapertura ratificada sin historial de transiciones (`specs/002-orquestacion-subagentes-sdd/spec.md:156`). | AUD-051, AUD-052, AUD-053, AUD-054, AUD-055 |
| D7 | Roles y menor privilegio: permisos declarados frente a operaciones ejecutadas | `NO CONFORME` | La matriz declara cinco roles (`.opencode/agents/sdd.md:3`, `.opencode/agents/documenter.md:3`) y tres omiten reglas de shell (`.opencode/agents/coder.md:4-16`, `.opencode/agents/reviewer.md:4-10`). Las aprobaciones son líneas de texto plano (`docs/constitution.md:62`) y no existe rol de auditor (`Get-ChildItem .opencode\agents -Filter *.md` devuelve cinco archivos). | AUD-061, AUD-062, AUD-063, AUD-064 |
| D8 | Evidencia y verificación: existencia, suficiencia y reproducibilidad de la prueba | `NO CONFORME` | Existen 47 casos de prueba en `tools/sdd/tests` y no hay flujo de integración continua ni hook activo (`Test-Path .github\workflows` devuelve `False`). La evidencia por tarea no es obligatoria ni verificada (`tools/sdd/validate.py:421-424` comprueba la cobertura y no el bloque de evidencia). | AUD-071, AUD-072 |
| D9 | Integración Git y release: nomenclatura, fusión, tags y registro de cambios | `PARCIAL` | La nomenclatura de ramas, los ocho tags anotados y las aprobaciones de `CHANGELOG.md` cumplen el flujo (`AGENTS.md:41`; `CHANGELOG.md:25`). `dev` está un commit por detrás de `main` (`git rev-list --left-right --count dev...main` devuelve `0 1`) y la protección de ramas descrita en los documentos de SPEC-007 no es verificable desde el repositorio, subconjunto acotado sin evidencia. | AUD-081, AUD-082, AUD-083, AUD-084 |
| D10 | Consistencia documental operativa: coincidencia entre documentos, índice, agentes y validador | `NO CONFORME` | El índice de specs coincide con el frontmatter de las siete specs publicadas y `AGENTS.md` tiene 61 líneas útiles, dentro del rango de `docs/constitution.md:39`. `MEMORY.md:43` declara pendiente un archivo que existe en la raíz y el validador devuelve `OK: sin hallazgos.` sin comprobar aprobaciones, transiciones, G5 ni G6 (`tools/sdd/validate.py:78`). | AUD-091, AUD-093, AUD-094 |

## 5. Hallazgos

### 5.1 Tabla consolidada

La tabla es la fuente del recuento de la sección y su número de filas coincide con el de bloques `### AUD-NNN` de 5.2. El veredicto de cada fila es el de la dimensión afectada y la severidad se asigna por el efecto observado (`specs/008-auditoria-cumplimiento-sdd/plan.md:211`).

| AUD-NNN | Dimensión | Veredicto | Severidad | Norma incumplida | Evidencia | Remediación |
|---|---|---|---|---|---|---|
| AUD-001 | D1 | `NO CONFORME` | Media | `docs/constitution.md:14` | `docs/sdd/compendio_sdd.md:3`; ver AUD-001 | B1 · editorial |
| AUD-002 | D1 | `NO CONFORME` | Alta | `docs/constitution.md:45`, `docs/constitution.md:50` | `specs/008-auditoria-cumplimiento-sdd/spec.md:35`; ver AUD-002 | B1 · requiere spec |
| AUD-003 | D1 | `NO CONFORME` | Media | `docs/constitution.md:45` | `docs/sdd/guia_spec_md.md:148-151`; ver AUD-003 | B1 · editorial |
| AUD-004 | D1 | `NO CONFORME` | Media | `docs/constitution.md:45` | `docs/sdd/guia_clarify_md.md:126-132`; ver AUD-004 | B1 · editorial |
| AUD-005 | D1 | `NO CONFORME` | Media | `docs/constitution.md:45` | `docs/sdd/referencia_7_etapas_sdd.md:135`; ver AUD-005 | B1 · editorial |
| AUD-006 | D1 | `NO CONFORME` | Baja | `docs/constitution.md:45` | `docs/sdd/README.md:7`; ver AUD-006 | B1 · editorial |
| AUD-007 | D1 | `NO CONFORME` | Baja | `docs/constitution.md:14` | inventario de 19 frente a 21 archivos; ver AUD-007 | B1 · editorial |
| AUD-011 | D2 | `NO CONFORME` | Alta | `docs/sdd/referencia_ciclo_vida_sdd_puro.md:77-85` | `.opencode/commands/sdd-implement.md:8`; ver AUD-011 | B2 · requiere spec |
| AUD-012 | D2 | `NO CONFORME` | Media | `docs/sdd/referencia_ciclo_vida_sdd_puro.md:77-85` | `.opencode/agents/sdd.md:89`; ver AUD-012 | B2 · requiere spec |
| AUD-013 | D2 | `NO CONFORME` | Crítica | `docs/constitution.md:18` | `specs/003-validacion-g4/validation_report.md:35-39`; ver AUD-013 | B2 · requiere spec |
| AUD-014 | D2 | `NO CONFORME` | Alta | `docs/constitution.md:14` | búsqueda sin coincidencias en `.opencode`; ver AUD-014 | B2 · requiere spec |
| AUD-021 | D3 | `PARCIAL` | Media | `docs/constitution.md:62` | `docs/sdd/plantillas/validation_report.md:27`; ver AUD-021 | B2 · requiere spec |
| AUD-022 | D3 | `PARCIAL` | Media | `docs/constitution.md:15` | `docs/sdd/plantillas/tasks.md:12`; ver AUD-022 | B4 · requiere spec |
| AUD-023 | D3 | `PARCIAL` | Media | `docs/constitution.md:14` | cinco plantillas en `docs/sdd/plantillas`; ver AUD-023 | B1 · requiere spec |
| AUD-031 | D4 | `NO CONFORME` | Crítica | `docs/constitution.md:16` | `tools/sdd/validate.py` sin la cadena `Approved`; ver AUD-031 | B2 · requiere spec |
| AUD-032 | D4 | `NO CONFORME` | Alta | `docs/constitution.md:15` | `tools/sdd/validate.py:323-325`; ver AUD-032 | B2 · requiere spec |
| AUD-033 | D4 | `NO CONFORME` | Media | `docs/constitution.md:18` | `tools/sdd/validate.py:383-385`; ver AUD-033 | B2 · requiere spec |
| AUD-034 | D4 | `NO CONFORME` | Alta | `docs/constitution.md:16` | `tools/sdd/validate.py:444-462`; ver AUD-034 | B2 · requiere spec |
| AUD-035 | D4 | `NO CONFORME` | Crítica | `docs/constitution.md:16` | `tools/sdd/validate.py:78`; ver AUD-035 | B2 · requiere spec |
| AUD-041 | D5 | `NO CONFORME` | Media | `docs/constitution.md:15` | `specs/001-main-menu/tasks.md` sin `CA-`; ver AUD-041 | B4 · proceso |
| AUD-042 | D5 | `NO CONFORME` | Alta | `docs/constitution.md:15` | `docs/sdd/plantillas/tasks.md:15`; ver AUD-042 | B4 · requiere spec |
| AUD-043 | D5 | `NO CONFORME` | Alta | `docs/constitution.md:15` | `tools/sdd/validate.py:517-519`; ver AUD-043 | B4 · requiere spec |
| AUD-044 | D5 | `NO CONFORME` | Alta | `docs/constitution.md:15` | `git log --merges --oneline`; ver AUD-044 | B4 · requiere spec |
| AUD-051 | D6 | `NO CONFORME` | Alta | `docs/constitution.md:14` | `tools/sdd/validate.py:299-300`; ver AUD-051 | B2 · requiere spec |
| AUD-052 | D6 | `NO CONFORME` | Alta | `docs/constitution.md:14` | búsqueda sin coincidencias en `.opencode`; ver AUD-052 | B2 · requiere spec |
| AUD-053 | D6 | `NO CONFORME` | Media | `docs/constitution.md:15` | `specs/002-orquestacion-subagentes-sdd/spec.md:156`; ver AUD-053 | B2 · proceso |
| AUD-054 | D6 | `NO CONFORME` | Media | `docs/constitution.md:14` | `specs/008-auditoria-cumplimiento-sdd/spec.md:11-12`; ver AUD-054 | B2 · requiere spec |
| AUD-055 | D6 | `NO CONFORME` | Baja | `docs/constitution.md:14` | siete versiones dispares en `specs/00*/spec.md`; ver AUD-055 | B1 · requiere spec |
| AUD-061 | D7 | `NO CONFORME` | Alta | `docs/constitution.md:17` | `.opencode/agents/coder.md:4-16`; ver AUD-061 | B3 · proceso |
| AUD-062 | D7 | `NO CONFORME` | Crítica | `docs/constitution.md:16`, `docs/constitution.md:63` | `docs/constitution.md:62`; ver AUD-062 | B2 · requiere spec |
| AUD-063 | D7 | `NO CONFORME` | Media | `docs/constitution.md:17` | cinco roles en `.opencode/agents`; ver AUD-063 | B3 · requiere spec |
| AUD-064 | D7 | `NO CONFORME` | Media | `docs/constitution.md:17` | `.opencode/agents/coder.md:4-16`; ver AUD-064 | B3 · editorial |
| AUD-071 | D8 | `NO CONFORME` | Media | `docs/constitution.md:18` | `.github/workflows` inexistente; ver AUD-071 | B3 · proceso |
| AUD-072 | D8 | `NO CONFORME` | Alta | `docs/constitution.md:18` | `tools/sdd/validate.py:421-424`; ver AUD-072 | B4 · requiere spec |
| AUD-081 | D9 | `PARCIAL` | Media | `docs/constitution.md:32`, `AGENTS.md:43` | `git rev-list --left-right --count dev...main` devuelve `0 1`; ver AUD-081 | B3 · proceso |
| AUD-082 | D9 | `PARCIAL` | Baja | `docs/constitution.md:32` | `git branch -a` muestra `remotes/origin/release/v0-6-0`; ver AUD-082 | B3 · proceso |
| AUD-083 | D9 | `PARCIAL` | Media | `AGENTS.md:41` | `git rev-list --left-right --count feat/gemma-4-26b-a4b-it-qat-gguf...dev` devuelve `2 47`; ver AUD-083 | B3 · proceso |
| AUD-084 | D9 | `PARCIAL` | Media | `AGENTS.md:43`, `AGENTS.md:45` | `git status --short` con seis entradas; ver AUD-084 | B3 · proceso |
| AUD-091 | D10 | `NO CONFORME` | Baja | `docs/constitution.md:14` | `MEMORY.md:43`; ver AUD-091 | B3 · editorial |
| AUD-093 | D10 | `NO CONFORME` | Baja | `docs/constitution.md:14` | `docs/sdd/README.md` sin `guia_maestra_sdd.md`; ver AUD-093 | B1 · editorial |
| AUD-094 | D10 | `NO CONFORME` | Alta | `docs/constitution.md:18` | `tools/sdd/validate.py:78`; ver AUD-094 | B2 · requiere spec |

### 5.2 Detalle por hallazgo

Cada bloque declara los siete campos del esquema de la sección 5: dimensión, veredicto, severidad, norma incumplida, evidencia, efecto observado y remediación propuesta.

### AUD-001

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `docs/sdd/compendio_sdd.md:3`, `docs/sdd/mapa_mental_sdd.md:3` y `docs/sdd/referencia_ciclo_vida_sdd_puro.md:3` abren con «Documento de referencia (no normativo)» y remiten al PROTOCOLO; la misma línea 3 aparece en los diecisiete documentos de la raíz inventariados en 2.3.
- **Efecto observado:** la base de la sección 2 atribuye rango normativo a documentos que declaran no serlo, de modo que la autoridad de la norma no se puede verificar sin ambigüedad.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: alinear la autodeclaración de los diecisiete documentos con el rango que la sección 2 les asigna.

### AUD-002

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:45`, `docs/constitution.md:50`.
- **Evidencia:** `specs/008-auditoria-cumplimiento-sdd/spec.md:35` excluye `docs/sdd/PROTOCOLO_OPERATIVO.md` de la base normativa, mientras `docs/sdd/README.md:10` lo declara norma ejecutable del corpus y `docs/constitution.md:50` le asigna rango 3. La tensión se reconoce en `specs/008-auditoria-cumplimiento-sdd/spec.md:245-247` (CB-011) y en la subsección 2.4.
- **Efecto observado:** el criterio de conformidad omite el procedimiento que la jerarquía sitúa en rango 3, por lo que la verificación no se ancla al orden normativo declarado y cada dimensión se contrasta contra documentos de rango inferior.
- **Remediación propuesta:** B1 base normativa, clasificación requiere spec: resolver la exclusión con una especificación que fije el criterio sin alterar la jerarquía de `docs/constitution.md:48-50`.

### AUD-003

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:45`.
- **Evidencia:** `docs/sdd/guia_spec_md.md:148-151` exige los criterios de aceptación como checklist «Definition of Done»; `docs/sdd/plantillas/spec.md:51-57` los declara como CA-NNN con línea `Cubre:`.
- **Efecto observado:** el contrato de `spec.md` admite dos formas incompatibles; una spec redactada según la guía no satisface la plantilla y la discrepancia no se resuelve por rango, porque ambos documentos ocupan el mismo nivel de la base.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: unificar la forma de los criterios de aceptación en la guía y en la plantilla.

### AUD-004

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:45`.
- **Evidencia:** `docs/sdd/guia_clarify_md.md:126-132` identifica los casos borde con `CB-NUEVO-01`, de dos dígitos; `docs/sdd/plantillas/clarify.md:20` usa tres dígitos.
- **Efecto observado:** el identificador que produce la guía no encaja en el espacio de nombres de la plantilla, de modo que el contrato de `clarify.md` no es único.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: fijar una sola anchura de identificador para los casos borde.

### AUD-005

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:45`.
- **Evidencia:** `docs/sdd/referencia_7_etapas_sdd.md:135` titula «Casos Límite y Fueras de Alcance» sin exigir requisitos no funcionales ni criterios de aceptación; `docs/sdd/plantillas/spec.md:35-57` exige ambos.
- **Efecto observado:** la guía de etapas admite una spec sin requisitos no funcionales ni criterios de aceptación, en contradicción con el contenido mínimo de la plantilla.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: alinear la sección de casos límite de la guía con el contenido mínimo de la plantilla.

### AUD-006

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Baja.
- **Norma incumplida:** `docs/constitution.md:45`.
- **Evidencia:** el único índice del corpus es `docs/sdd/README.md:7`, `docs/sdd/README.md:10` y `docs/sdd/README.md:14`, documento excluido por `specs/008-auditoria-cumplimiento-sdd/spec.md:36`; la base de 2.3 no incluye índice alguno.
- **Efecto observado:** la base de veintidós documentos no declara su orden interno, por lo que las contradicciones de AUD-003 a AUD-005 no tienen vía de resolución dentro de la base y la precedencia queda en un documento de referencia.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: incorporar a la base un índice con la precedencia interna de los documentos de igual rango.

### AUD-007

- **Dimensión:** D1.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Baja.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** en el commit de corte, `docs/sdd/PROTOCOLO_OPERATIVO.md` declara 19 documentos en `docs/sdd/`; `git ls-tree --name-only 1d6b2c5 docs/sdd/` lista 21 archivos Markdown en la raíz del corte.
- **Efecto observado:** el inventario declarado por el procedimiento no coincide con el árbol del corte, de modo que un tercero que lo siga omite dos documentos del corpus.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: actualizar el recuento declarado por el procedimiento sin alterar la regla de inclusión de la sección 2.

### AUD-011

- **Dimensión:** D2.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/sdd/referencia_ciclo_vida_sdd_puro.md:77-85`.
- **Evidencia:** `.opencode/commands/sdd-implement.md:8` exige G4 al iniciar la etapa Implement; `.opencode/agents/sdd.md:88` exige G2 verificada y la spec en estado `tasked`.
- **Efecto observado:** la condición de entrada de Implement no es unívoca; la conformidad de una implementación no se puede decidir con el ciclo declarado porque dos fuentes del mismo ciclo exigen compuertas distintas.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: fijar una sola compuerta de entrada para Implement y alinear el comando y el agente.

### AUD-012

- **Dimensión:** D2.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/sdd/referencia_ciclo_vida_sdd_puro.md:77-85`.
- **Evidencia:** `.opencode/commands/sdd-implement.md:13` valida G3 por tarea; `.opencode/agents/sdd.md:89` reserva G3 para el cierre de la etapa.
- **Efecto observado:** G3 admite dos momentos de ejecución y su resultado no acredita el mismo estado de las tareas en una y otra lectura.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: declarar el momento único de G3 y su relación con el cierre de la etapa.

### AUD-013

- **Dimensión:** D2.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Crítica.
- **Norma incumplida:** `docs/constitution.md:18`.
- **Evidencia:** `.opencode/commands/sdd-validate.md:9` y `.opencode/agents/reviewer.md:24` ejecutan `--gate G4` antes de escribir el reporte que G4 exige; `specs/003-validacion-g4/validation_report.md:35-39` documenta el error circular.
- **Efecto observado:** la compuerta G4 se ejecuta antes de existir su propia evidencia, por lo que la autorización de implementación queda anulada como control y el reporte se produce después de la verificación que lo requiere.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: separar la verificación de cierre de G4 de la escritura previa del reporte, con orden explícito en el comando y en el agente.

### AUD-014

- **Dimensión:** D2.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `Select-String -Path .opencode\commands\*.md,.opencode\agents\*.md -Pattern 'implementing|implemented|validated'` no devuelve coincidencias; las siete specs publicadas figuran en `released` y conservan los cinco artefactos.
- **Efecto observado:** tres estados del modelo no tienen escritor, de modo que el paso de `tasked` a `released` no queda registrado por ninguna orden y el estado observado no se puede reconstruir.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: asignar a un comando la escritura de los tres estados y su registro en el historial de la spec.

### AUD-021

- **Dimensión:** D3.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:62`.
- **Evidencia:** `docs/sdd/plantillas/spec.md:63` incluye solo la casilla de G1 y `docs/sdd/plantillas/validation_report.md:27` incluye una casilla de G4; el registro diverge en la práctica: marcado en `specs/001-main-menu/validation_report.md:36` y `specs/007-branch-protection/validation_report.md:66`, sin marcar en `specs/002-orquestacion-subagentes-sdd/validation_report.md:180`, `specs/003-validacion-g4/validation_report.md:138`, `specs/004-editor-documentacion/validation_report.md:141`, `specs/005-compuertas-completas/validation_report.md:73` y `specs/006-observaciones-cierre/validation_report.md:51`.
- **Efecto observado:** dos artefactos pueden consignar resultados opuestos de la misma aprobación de G4, mientras las siete specs la registran en `spec.md` (`specs/001-main-menu/spec.md:96`, `specs/007-branch-protection/spec.md:232`); el registro de la aprobación no es unívoco.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: fijar un solo artefacto como titular del registro de G4 y retirar la casilla duplicada de la plantilla restante.

### AUD-022

- **Dimensión:** D3.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** `docs/sdd/plantillas/tasks.md:12` y `docs/sdd/plantillas/tasks.md:21` declaran `Requisitos cubiertos: RF-001` sin identificar el criterio de aceptación.
- **Efecto observado:** el contrato de tarea no porta el eslabón CA → T, por lo que una tarea conforme a la plantilla no permite reconstruir qué criterio de aceptación satisface.
- **Remediación propuesta:** B4 trazabilidad profunda, clasificación requiere spec: añadir el campo de criterio de aceptación al contrato de tarea y a la matriz de cobertura.

### AUD-023

- **Dimensión:** D3.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `Get-ChildItem docs\sdd\plantillas -Filter *.md` devuelve cinco plantillas (spec, clarify, plan, tasks y validation_report) y ninguna cubre la documentación analítica; `specs/008-auditoria-cumplimiento-sdd/clarify.md` registra la ausencia como AMB-005.
- **Efecto observado:** la documentación analítica se produce sin contrato de campos ni secciones y sin rol autorizado; este informe se redactó bajo esa ausencia y su estructura depende de un plan particular.
- **Remediación propuesta:** B1 base normativa, clasificación requiere spec: definir el contrato de la documentación analítica y el rol habilitado para redactarla.

### AUD-031

- **Dimensión:** D4.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Crítica.
- **Norma incumplida:** `docs/constitution.md:16`.
- **Evidencia:** `Select-String -Path tools\sdd\validate.py -Pattern 'Approved'` no devuelve coincidencias, mientras las siete specs registran la línea de aprobación (`specs/001-main-menu/spec.md:95`, `specs/002-orquestacion-subagentes-sdd/spec.md:156`, `specs/003-validacion-g4/spec.md:148`, `specs/004-editor-documentacion/spec.md:151`, `specs/005-compuertas-completas/spec.md:153`, `specs/006-observaciones-cierre/spec.md:131`, `specs/007-branch-protection/spec.md:231`).
- **Efecto observado:** una spec sin aprobación de G1 pasa el validador con código de salida `0`, de modo que la compuerta queda anulada en la verificación automática y el verde no acredita la autorización del propietario.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: incorporar al validador la comprobación de la cadena `Approved` y del declarante en la compuerta G1.

### AUD-032

- **Dimensión:** D4.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** `tools/sdd/validate.py:323-325` emite advertencia cuando falta la línea `Cubre:`; `tools/sdd/validate.py:421-424` emite error cuando falta la cobertura de requisitos de una tarea.
- **Efecto observado:** un requisito sin criterio de aceptación no impide el verde del validador, por lo que la cadena RF/CB → CA se puede romper sin fallo de G2.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: elevar a error la ausencia de `Cubre:` y alinear la compuerta G2 con el criterio de G3.

### AUD-033

- **Dimensión:** D4.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:18`.
- **Evidencia:** `tools/sdd/validate.py:383-385` solo comprueba G3 con `--gate G3`; `python tools\sdd\validate.py --all` no pasa compuerta y no verifica tareas abiertas.
- **Efecto observado:** el verde de `--all` se afirma sobre un conjunto que incluye tareas abiertas, de modo que el éxito se declara sin la evidencia de la compuerta G3.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: incluir la verificación de tareas abiertas en la ejecución agregada o declarar su ausencia como resultado parcial.

### AUD-034

- **Dimensión:** D4.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:16`.
- **Evidencia:** `tools/sdd/validate.py:444-462` comprueba la presencia del reporte, el dictamen y las filas no superadas, sin comprobar la aprobación de G4.
- **Efecto observado:** la compuerta G4 se declara superada sin verificar la autorización del propietario, por lo que la evidencia de la compuerta se reduce a la existencia del reporte.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: exigir en G4 la línea de aprobación y el declarante, además del dictamen del reporte.

### AUD-035

- **Dimensión:** D4.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Crítica.
- **Norma incumplida:** `docs/constitution.md:16`.
- **Evidencia:** `tools/sdd/validate.py:78` define `GATES_REQUIRING_REPORT = {"G4","G5","G6"}` y las tres compuertas ejecutan la misma verificación; no existe lógica propia para G5 ni para G6.
- **Efecto observado:** la autorización de release no se distingue de la de implementación, por lo que G6 queda anulada como control independiente y un release sin aprobación propia pasa con el mismo verde.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: dotar a G5 y G6 de condiciones y verificaciones propias, con la aprobación de release como requisito de G6.

### AUD-041

- **Dimensión:** D5.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** `Select-String -Path specs\001-main-menu\tasks.md -Pattern 'CA-\d{3}'` no devuelve coincidencias, y la misma consulta sobre `specs\004-editor-documentacion\tasks.md` y `specs\006-observaciones-cierre\tasks.md` tampoco; SPEC-002 registra 5 referencias, SPEC-003 5, SPEC-005 10 y SPEC-007 7.
- **Efecto observado:** en tres de las siete specs el enlace CA → T no está registrado de forma explícita en las tareas y solo se reconstruye por tránsito a través del RF/CB, de modo que la correspondencia existe pero no consta como enlace declarado en el artefacto de tareas.
- **Remediación propuesta:** B4 trazabilidad profunda, clasificación proceso: registrar el criterio de aceptación en las tareas de las tres specs y verificar la correspondencia en la revisión de cierre.

### AUD-042

- **Dimensión:** D5.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** `docs/sdd/plantillas/tasks.md:15` define el campo `Validación` y la plantilla no declara un campo de evidencia por tarea; `tools/sdd/validate.py:421-424` comprueba la cobertura de requisitos de la tarea y no un bloque de evidencia.
- **Efecto observado:** el eslabón T → evidencia no tiene formato declarado ni comprobación, por lo que un tercero no puede reconstruirlo con un criterio común y la evidencia queda a juicio de quien redacta.
- **Remediación propuesta:** B4 trazabilidad profunda, clasificación requiere spec: fijar los campos mínimos de la evidencia de tarea y su comprobación en el validador.

### AUD-043

- **Dimensión:** D5.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** `tools/sdd/validate.py:517-519` busca la cadena `Spec:` en los últimos 50 commits y produce una advertencia; `--all` ignora `--git`.
- **Efecto observado:** un commit de implementación sin referencia a la spec no impide el verde, de modo que el eslabón evidencia → commit no se comprueba y la advertencia no bloquea la integración.
- **Remediación propuesta:** B4 trazabilidad profunda, clasificación requiere spec: convertir la ausencia de `Spec:` en error y ejecutar la comprobación Git en la verificación agregada.

### AUD-044

- **Dimensión:** D5.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** el historial contiene 26 merges con dos padres; siete integran una spec de SPEC-001 a SPEC-007 (`753c3e5` en SPEC-001, `ec6a063` en SPEC-002, `39b27a2` en SPEC-003, `b38ed6c` en SPEC-004, `2781db5` en SPEC-005, `0afc2ee` en SPEC-006 y `502c69d` en SPEC-007), y `CHANGELOG.md:25` registra la aprobación de release; ningún artefacto de las siete specs declara el merge que las integra.
- **Efecto observado:** el eslabón commit → merge → release no está declarado ni es verificable de forma determinista: los merges constan en el historial, pero falta la declaración que los vincula con cada spec, su tag y su registro de cambios.
- **Remediación propuesta:** B4 trazabilidad profunda, clasificación requiere spec: registrar en el reporte de validación el hash del merge y el tag de release de cada spec.

### AUD-051

- **Dimensión:** D6.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `tools/sdd/validate.py:25-36` enumera diez estados admitidos; `tools/sdd/validate.py:299-300` solo comprueba la pertenencia al conjunto y no valida ninguna transición.
- **Efecto observado:** una spec puede pasar de `draft` a `released` sin transición registrada y el validador no lo detecta, de modo que el estado observado no acredita el recorrido del ciclo.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: declarar la tabla de transiciones admitidas y comprobarla en el validador.

### AUD-052

- **Dimensión:** D6.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `Select-String -Path .opencode\commands\*.md,.opencode\agents\*.md -Pattern 'implementing|implemented|validated'` no devuelve coincidencias; las siete specs publicadas figuran en `released`.
- **Efecto observado:** tres de los diez estados admitidos no tienen escritor, por lo que el paso entre `tasked` y `released` no queda registrado y los estados intermedios son nominales.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: asignar la escritura de los tres estados a las etapas que los producen o retirarlos del conjunto admitido.

### AUD-053

- **Dimensión:** D6.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:15`.
- **Evidencia:** `specs/002-orquestacion-subagentes-sdd/spec.md:156` registra una spec «ratificada tras la reapertura v0.5.0» sin historial de transiciones; las siete specs figuran en `released`.
- **Efecto observado:** la reapertura y la ratificación no tienen registro de estados, por lo que el vínculo entre la versión publicada y el release v0.5.0 no es reconstruible.
- **Remediación propuesta:** B2 mecanismo de control, clasificación proceso: añadir el historial de transiciones al artefacto de la spec al reabrirla o ratificarla.

### AUD-054

- **Dimensión:** D6.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `specs/008-auditoria-cumplimiento-sdd/spec.md:11-12` declara los campos `supersedes` y `superseded_by`; el validador no comprueba ninguno de los dos (`tools/sdd/validate.py:299-300` valida la pertenencia del estado).
- **Efecto observado:** la relación de sucesión entre specs puede quedar incompleta o asimétrica sin que la verificación lo advierta.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: comprobar la simetría de `supersedes` y `superseded_by` y la coherencia con el estado.

### AUD-055

- **Dimensión:** D6.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Baja.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `Select-String -Path specs\00*\spec.md -Pattern '^version:'` devuelve 0.1.0, 0.12.0, 0.6.0, 0.9.0, 0.6.0, 0.6.0 y 0.2.0 para las siete specs publicadas.
- **Efecto observado:** la versión no se deriva del alcance del cambio ni de una regla observable, por lo que dos auditorías independientes no reproducen la misma numeración.
- **Remediación propuesta:** B1 base normativa, clasificación requiere spec: declarar la regla de versionado de las specs y aplicarla al historial de cambios.

### AUD-061

- **Dimensión:** D7.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:17`.
- **Evidencia:** `.opencode/agents/coder.md:4-16`, `.opencode/agents/planner.md:4-13` y `.opencode/agents/reviewer.md:4-10` declaran permisos de archivo y no declaran reglas de shell; `.opencode/agents/documenter.md:4-19` sí deniega shell y subagentes.
- **Efecto observado:** tres roles conservan una capacidad de ejecución que la matriz no acota, de modo que el menor privilegio no es verificable para ellos y la comparación entre permiso declarado y operación observada queda incompleta.
- **Remediación propuesta:** B3 práctica operativa, clasificación proceso: declarar en cada rol las reglas de shell y de subagentes y contrastarlas con la operación registrada.

### AUD-062

- **Dimensión:** D7.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Crítica.
- **Norma incumplida:** `docs/constitution.md:16`, `docs/constitution.md:63`.
- **Evidencia:** `docs/constitution.md:62` fija la aprobación como línea explícita de texto plano y `.opencode/agents/planner.md:4-13` permite escribir en `specs/**`.
- **Efecto observado:** la línea de aprobación puede ser escrita por un rol distinto del propietario y no existe mecanismo que atribuya su autoría, de modo que la compuerta descansa en una declaración no verificable y la prohibición de autoaprobación no se puede comprobar.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: registrar la aprobación con un mecanismo de autoría verificable y restringir la escritura de la sección de aprobaciones.

### AUD-063

- **Dimensión:** D7.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:17`.
- **Evidencia:** `Get-ChildItem .opencode\agents -Filter *.md` devuelve cinco archivos (`.opencode/agents/sdd.md:3`, `planner.md:3`, `coder.md:3`, `reviewer.md:3` y `documenter.md:3`); ninguno declara la función de auditoría descrita en `specs/008-auditoria-cumplimiento-sdd/clarify.md` (AMB-005).
- **Efecto observado:** la función de auditoría se ejecutó con los permisos del rol de documentación, de modo que la matriz no declara el rol que produce el informe ni el alcance de su acceso.
- **Remediación propuesta:** B3 práctica operativa, clasificación requiere spec: declarar el rol de auditoría con permisos de solo lectura sobre los artefactos auditados y escritura limitada al informe.

### AUD-064

- **Dimensión:** D7.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:17`.
- **Evidencia:** `.opencode/agents/coder.md:4-16` deniega `specs/**` y `docs/**`, permite `specs/*/tasks.md` y no declara la precedencia entre la denegación y el permiso.
- **Efecto observado:** el permiso efectivo depende del orden de resolución del cliente y no de la matriz declarada, por lo que dos lecturas del mismo archivo admiten alcances distintos.
- **Remediación propuesta:** B3 práctica operativa, clasificación editorial: declarar la regla de precedencia entre permisos solapados y reescribir la matriz sin solapamiento.

### AUD-071

- **Dimensión:** D8.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:18`.
- **Evidencia:** `tools/sdd/tests` contiene 47 casos de prueba; `Test-Path .github\workflows` devuelve `False` y `Get-ChildItem .git\hooks` solo muestra archivos de ejemplo.
- **Efecto observado:** la batería no se ejecuta en la integración ni queda ligada al commit, de modo que su resultado depende de una ejecución manual no registrada y la reproducibilidad descansa en la memoria de quien la ejecutó.
- **Remediación propuesta:** B3 práctica operativa, clasificación proceso: ejecutar la batería en un flujo de integración y registrar su salida en el reporte de validación.

### AUD-072

- **Dimensión:** D8.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:18`.
- **Evidencia:** `tools/sdd/validate.py:421-424` comprueba la cobertura de requisitos de cada tarea y no el bloque de evidencia; la casilla de tarea completada se registra sin exigir ese bloque (`specs/008-auditoria-cumplimiento-sdd/tasks.md:52`).
- **Efecto observado:** una tarea puede marcarse completada sin prueba registrada, de modo que la afirmación de éxito no queda respaldada por evidencia y la verificación se reduce a la cobertura.
- **Remediación propuesta:** B4 trazabilidad profunda, clasificación requiere spec: condicionar el cierre de la tarea al bloque de evidencia y comprobar su presencia en el validador.

### AUD-081

- **Dimensión:** D9.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Media.
- **Norma incumplida:** `docs/constitution.md:32`, `AGENTS.md:43`.
- **Evidencia:** `git rev-list --left-right --count dev...main` devuelve `0 1`.
- **Efecto observado:** la rama de integración no contiene el commit publicado en `main`, de modo que un release preparado desde `dev` omitiría ese cambio y el estado de ambas ramas no converge.
- **Remediación propuesta:** B3 práctica operativa, clasificación proceso: sincronizar `dev` con `main` mediante merge `--no-ff` y verificar la convergencia antes de cada release.

### AUD-082

- **Dimensión:** D9.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Baja.
- **Norma incumplida:** `docs/constitution.md:32`.
- **Evidencia:** `git branch -a` conserva la referencia `remotes/origin/release/v0-6-0` después del release.
- **Efecto observado:** una referencia de empaquetado permanece tras el cierre, de modo que el estado remoto no refleja la finalización del release.
- **Remediación propuesta:** B3 práctica operativa, clasificación proceso: eliminar la referencia remota obsoleta al cerrar el release y verificar el listado de ramas.

### AUD-083

- **Dimensión:** D9.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Media.
- **Norma incumplida:** `AGENTS.md:41`.
- **Evidencia:** `git rev-list --left-right --count feat/gemma-4-26b-a4b-it-qat-gguf...dev` devuelve `2 47`.
- **Efecto observado:** una rama de trabajo conserva dos commits sin integrar y un desfase de cuarenta y siete commits, de modo que su contenido permanece fuera de `dev` sin registro de integración ni de descarte.
- **Remediación propuesta:** B3 práctica operativa, clasificación proceso: decidir la integración o el descarte de la rama y registrar la decisión en el release correspondiente.

### AUD-084

- **Dimensión:** D9.
- **Veredicto:** `PARCIAL`.
- **Severidad:** Media.
- **Norma incumplida:** `AGENTS.md:43`, `AGENTS.md:45`.
- **Evidencia:** `git status --short` devuelve seis entradas en `docs/sdd/` (cuatro archivos modificados y dos sin seguimiento), transcritas en 1.3.
- **Efecto observado:** el corpus cambia fuera de cualquier commit y fuera de una solicitud de integración, de modo que el inventario de la sección 2 no es reproducible desde el corte para esos seis archivos y los cambios no constan en el registro de cambios.
- **Remediación propuesta:** B3 práctica operativa, clasificación proceso: registrar los seis cambios por la vía de integración declarada y anotarlos en el registro de cambios.

### AUD-091

- **Dimensión:** D10.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Baja.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `MEMORY.md:43` declara que `main.bat` está pendiente de implementación; `Test-Path main.bat` devuelve `True`.
- **Efecto observado:** el contexto operativo contradice el estado del repositorio, de modo que quien lo consulte como referencia parte de un hecho falso.
- **Remediación propuesta:** B3 práctica operativa, clasificación editorial: actualizar la línea de `MEMORY.md` con el estado real del archivo.

### AUD-093

- **Dimensión:** D10.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Baja.
- **Norma incumplida:** `docs/constitution.md:14`.
- **Evidencia:** `Select-String -Path docs\sdd\README.md -Pattern 'guia_maestra_sdd'` no devuelve coincidencias y la navegación de `docs/sdd/README.md:7`, `docs/sdd/README.md:10` y `docs/sdd/README.md:14` no cubre los 21 documentos de la raíz en el corte.
- **Efecto observado:** el único índice del corpus no enlaza el documento maestro ni la totalidad de los documentos, de modo que la navegación es incompleta y un lector no alcanza cada archivo desde el índice.
- **Remediación propuesta:** B1 base normativa, clasificación editorial: completar la navegación del índice con los documentos ausentes.

### AUD-094

- **Dimensión:** D10.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** Alta.
- **Norma incumplida:** `docs/constitution.md:18`.
- **Evidencia:** `python tools\sdd\validate.py --all` devuelve `OK: sin hallazgos.` con código de salida `0`; el validador no comprueba aprobaciones ni transiciones y aplica la misma verificación a G4, G5 y G6 (`tools/sdd/validate.py:78`).
- **Efecto observado:** el verde del validador se lee como conformidad del régimen sin cubrir las compuertas de aprobación ni el modelo de estados, de modo que la divergencia entre la norma documental y la herramienta permanece oculta.
- **Remediación propuesta:** B2 mecanismo de control, clasificación requiere spec: alinear la verificación automática con las compuertas y transiciones declaradas, o declarar por escrito el alcance parcial del verde.

## 6. Evaluación de compuertas G1 a G6

La tabla evalúa las seis compuertas en el orden del ciclo y con las seis columnas del esquema de `specs/008-auditoria-cumplimiento-sdd/plan.md:139`. La columna de resultado responde a una sola pregunta: si la evidencia conservada acredita la condición de la compuerta en el periodo auditado (`specs/008-auditoria-cumplimiento-sdd/plan.md:147`). Los defectos del mecanismo de verificación —falta de comprobación automática, advertencia en lugar de error, ausencia de lógica propia— se registran en la columna de verificación y sostienen el veredicto de la dimensión D4, sin convertir en incumplida una compuerta cuya evidencia existe. La falta de evidencia conservada impide el `CONFORME` y se declara como ausencia remitida a la sección 11 (CB-003). El valor de cada fila pertenece a la escala de 3.2, aplicada al contraste de la evidencia con la condición y no a la calidad del mecanismo. La auditoría no aprueba compuertas y la columna de resultado registra lo observado (`specs/008-auditoria-cumplimiento-sdd/plan.md:23`).

| Compuerta | Condición normativa | Evidencia observada | Declarante | Verificación | Resultado |
|---|---|---|---|---|---|
| G1 | Spec sin ambigüedades, requisitos en EARS correcto y aprobación del propietario (`docs/constitution.md:16`; `docs/sdd/plantillas/spec.md:63`) | Las siete specs registran la línea de aprobación (`specs/001-main-menu/spec.md:95`, `specs/002-orquestacion-subagentes-sdd/spec.md:156`, `specs/003-validacion-g4/spec.md:148`, `specs/004-editor-documentacion/spec.md:151`, `specs/005-compuertas-completas/spec.md:153`, `specs/006-observaciones-cierre/spec.md:131`, `specs/007-branch-protection/spec.md:231`) y el validador comprueba EARS y secciones | Agent Sebaxtian (`specs/001-main-menu/spec.md:95`; `specs/007-branch-protection/spec.md:231`) | Documental: las siete líneas de aprobación y la comprobación de EARS y secciones acreditan la condición; la cadena de aprobación no tiene comprobación automática y la línea no atribuye autoría (AUD-031, AUD-062), defecto del mecanismo que se registra en D4 y D7 | `CONFORME` |
| G2 | Plan y tareas conformes a su contrato y cobertura completa de requisitos (`docs/sdd/referencia_ciclo_vida_sdd_puro.md:83`; `docs/sdd/plantillas/tasks.md`) | Las siete specs tienen `plan.md` y `tasks.md`; `python tools\sdd\validate.py --spec SPEC-008 --gate G2` devuelve `0`; la cobertura RF/CB → CA está completa en las siete | Validación automatizada del validador (`tools/sdd/validate.py`), sin declarante personal | La cobertura está completa en las siete y `--gate G2` devuelve `0`, de modo que la evidencia acredita la condición; la cobertura incompleta solo produce advertencia (`tools/sdd/validate.py:323-325`), defecto del mecanismo que se registra en D4 (AUD-032) | `CONFORME` |
| G3 | Tareas cerradas con evidencia y pruebas en verde (`docs/sdd/guia_fase_implement_tdd.md:110-114`; `docs/sdd/plantillas/tasks.md:16`) | 48 tareas cerradas y 0 abiertas en las siete specs; 47 casos de prueba en `tools/sdd/tests`; el campo de evidencia no está definido en la plantilla (`docs/sdd/plantillas/tasks.md:15`) ni verificado (`tools/sdd/validate.py:421-424`) | Registro de tareas de las siete specs (`specs/001-main-menu/tasks.md` a `specs/007-branch-protection/tasks.md`), sin declarante personal | Las 48 tareas constan cerradas y las pruebas existen en `tools/sdd/tests`; la evidencia por tarea no está definida ni verificada (AUD-042, AUD-072), de modo que la condición se acredita solo en parte | `PARCIAL` |
| G4 | Reporte de validación con dictamen y aprobación del propietario (`docs/constitution.md:16`; `docs/sdd/plantillas/validation_report.md:27`) | Siete reportes con dictamen CONVERGIDO (`specs/001-main-menu/validation_report.md:32`, `specs/002-orquestacion-subagentes-sdd/validation_report.md:159`, `specs/003-validacion-g4/validation_report.md:118`, `specs/004-editor-documentacion/validation_report.md:135`, `specs/005-compuertas-completas/validation_report.md:68`, `specs/006-observaciones-cierre/validation_report.md:46`, `specs/007-branch-protection/validation_report.md:61`) y siete aprobaciones en `spec.md`; el registro G4 del reporte solo está marcado en `specs/001-main-menu/validation_report.md:36` y `specs/007-branch-protection/validation_report.md:66` | Agent Sebaxtian (`specs/001-main-menu/spec.md:96`; `specs/007-branch-protection/spec.md:232`) | Aprobación documental: siete dictámenes CONVERGIDOS y siete aprobaciones en `spec.md` acreditan la condición; el registro G4 del reporte diverge en cinco de los siete (AUD-021) y el validador no comprueba la aprobación (AUD-034), defectos de contrato y de mecanismo que se registran en D3 y D4 | `CONFORME` |
| G5 | Merge `--no-ff`, validación posterior a la fusión y rama de trabajo eliminada (`docs/constitution.md:15`; `AGENTS.md:41`) | Siete fusiones con dos padres (`753c3e5`, `ec6a063`, `39b27a2`, `b38ed6c`, `2781db5`, `0afc2ee`, `502c69d`); las siete ramas de trabajo integradas no figuran en `git branch -a`, mientras `feat/auditoria-cumplimiento-sdd` y `feat/gemma-4-26b-a4b-it-qat-gguf` permanecen y no forman parte de las siete integradas; `Sin evidencia conservada` de la validación posterior al merge | Historial Git (`git log --merges --oneline`; `git branch -a`), sin declarante personal | Fusión y eliminación evidenciadas en el historial; la validación posterior al merge carece de evidencia conservada, elemento cuya verificación queda `NO VERIFICABLE` (CB-003) y se declara en la sección 11 | `PARCIAL` |
| G6 | Autorización del release, tag anotado y actualización de `specs/INDEX.md` y `CHANGELOG.md` (`AGENTS.md:17`; `docs/constitution.md:16`) | Ocho tags anotados con asunto `Release vX.Y.Z`; ocho aprobaciones en `CHANGELOG.md:25`, `CHANGELOG.md:35`, `CHANGELOG.md:50`, `CHANGELOG.md:64`, `CHANGELOG.md:78`, `CHANGELOG.md:99`, `CHANGELOG.md:128` y `CHANGELOG.md:174`; `specs/INDEX.md` coincide con el frontmatter en estado, rama y release | Agent Sebaxtian (`CHANGELOG.md:25`; `CHANGELOG.md:174`) | Documental y reproducible: el tag, el registro y el índice acreditan la condición; la compuerta comparte la verificación de G4 (`tools/sdd/validate.py:78`, AUD-035) y la autorización consta como texto plano (AUD-062), defectos que se registran en D4 y D7 | `CONFORME` |

El recuento es de cuatro compuertas `CONFORME` (G1, G2, G4 y G6) y dos `PARCIAL` (G3 y G5); ninguna queda `NO CONFORME`. En G5, el elemento de validación posterior al merge queda `NO VERIFICABLE` conforme a CB-003 y se declara en la sección 11. La fila D4 de la sección 4 sigue en `NO CONFORME` porque su objeto es el mecanismo de control de las compuertas, mientras esta tabla evalúa si la evidencia acredita la condición de cada una.

## 7. Trazabilidad por spec

La tabla recorre la cadena RF/CB → CA → T → evidencia → commit → merge → release con una fila por identificador y las nueve columnas del esquema de `specs/008-auditoria-cumplimiento-sdd/plan.md:151`. Los enlaces CA y T proceden de la matriz de cobertura de cada plan y de su `tasks.md`, y la columna de evidencia remite al archivo de tareas que registra el cierre. La columna `Commit` queda en `AUSENTE` en las 71 filas porque ningún artefacto declara el commit de implementación (AUD-043), y la columna de eslabón faltante acompaña cada ausencia con el `AUD-NNN` que la registra (CB-002). La columna `Merge` y la columna `Release` son las del historial de integración, cuyo vínculo no está declarado en los artefactos (AUD-044).

| Spec | RF/CB | CA | T | Evidencia | Commit | Merge | Release | Eslabón faltante |
|---|---|---|---|---|---|---|---|---|
| SPEC-001 | RF-001 | CA-001 | T-002 | tasks.md T-002 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | RF-002 | CA-002 | T-004 | tasks.md T-004 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | RF-003 | CA-001 | T-003 | tasks.md T-003 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | RF-004 | CA-003 | T-003 | tasks.md T-003 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | RF-005 | CA-004 | T-004 | tasks.md T-004 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | RF-006 | CA-005 | T-004 | tasks.md T-004 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | CB-001 | CA-004 | T-004 | tasks.md T-004 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | CB-002 | CA-002 | T-004 | tasks.md T-004 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-001 | CB-003 | CA-005 | T-004 | tasks.md T-004 | AUSENTE | 753c3e5 | v0.2.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-001 | CA-001 | T-003 | tasks.md T-003 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-002 | CA-001, CA-006 | T-001 | tasks.md T-001 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-003 | CA-002, CA-006 | T-002 | tasks.md T-002 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-004 | CA-003 | T-003 | tasks.md T-003 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-005 | CA-004 | T-003 | tasks.md T-003 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-006 | CA-005, CA-007 | T-004, T-007, T-009 | tasks.md T-004, T-007, T-009 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | RF-007 | CA-008 | T-004, T-010 | tasks.md T-004, T-010 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | CB-001 | CA-005, CA-010 | T-004, T-007, T-010 | tasks.md T-004, T-007, T-010 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | CB-002 | CA-008 | T-004 | tasks.md T-004 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-002 | CB-003 | CA-007 | T-004, T-007, T-009 | tasks.md T-004, T-007, T-009 | AUSENTE | ec6a063 | v0.3.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | RF-001 | CA-001 | T-001, T-002, T-004, T-005 | tasks.md T-001, T-002, T-004, T-005 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | RF-002 | CA-002 | T-001, T-002, T-003, T-004 | tasks.md T-001, T-002, T-003, T-004 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | RF-003 | CA-003 | T-001, T-002, T-004 | tasks.md T-001, T-002, T-004 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | RF-004 | CA-004 | T-003, T-004 | tasks.md T-003, T-004 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | RF-005 | CA-005 | T-001, T-002, T-004 | tasks.md T-001, T-002, T-004 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | CB-001 | CA-002 | T-001, T-002, T-004, T-005 | tasks.md T-001, T-002, T-004, T-005 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | CB-002 | CA-005 | T-001, T-002, T-004 | tasks.md T-001, T-002, T-004 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | CB-003 | CA-005 | T-004, T-005 | tasks.md T-004, T-005 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-003 | CB-004 | CA-001 | T-001, T-002 | tasks.md T-001, T-002 | AUSENTE | 39b27a2 | v0.3.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | RF-001 | CA-001 | T-002, T-005 | tasks.md T-002, T-005 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | RF-002 | CA-002 | T-001, T-005 | tasks.md T-001, T-005 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | RF-003 | CA-003 | T-001, T-005 | tasks.md T-001, T-005 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | RF-004 | CA-004 | T-002, T-005 | tasks.md T-002, T-005 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | RF-005 | CA-005 | T-001, T-003 | tasks.md T-001, T-003 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | RF-006 | CA-006 | T-003 | tasks.md T-003 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | CB-001 | CA-005, CA-006 | T-001, T-003 | tasks.md T-001, T-003 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | CB-002 | CA-002 | T-001, T-005 | tasks.md T-001, T-005 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-004 | CB-003 | CA-003 | T-001, T-005 | tasks.md T-001, T-005 | AUSENTE | b38ed6c | v0.4.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | RF-001 | CA-001 | T-001, T-002, T-008 | tasks.md T-001, T-002, T-008 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | RF-002 | CA-002 | T-003, T-004, T-008 | tasks.md T-003, T-004, T-008 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | RF-003 | CA-003 | T-005, T-008 | tasks.md T-005, T-008 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | RF-004 | CA-004, CA-006 | T-006, T-008 | tasks.md T-006, T-008 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | RF-005 | CA-005, CA-006 | T-007, T-008 | tasks.md T-007, T-008 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | CB-001 | CA-002, CA-006 | T-003, T-004 | tasks.md T-003, T-004 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | CB-002 | CA-003 | T-005 | tasks.md T-005 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-005 | CB-003 | CA-006 | T-009 | tasks.md T-009 | AUSENTE | 2781db5 | v0.5.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-006 | RF-001 | CA-001 | T-001 | tasks.md T-001 | AUSENTE | 0afc2ee | v0.5.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-006 | RF-002 | CA-002 | T-002 | tasks.md T-002 | AUSENTE | 0afc2ee | v0.5.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-006 | RF-003 | CA-003, CA-004 | T-003 | tasks.md T-003 | AUSENTE | 0afc2ee | v0.5.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-006 | CB-001 | CA-004 | T-001, T-005 | tasks.md T-001, T-005 | AUSENTE | 0afc2ee | v0.5.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-006 | CB-002 | CA-002 | T-002, T-005 | tasks.md T-002, T-005 | AUSENTE | 0afc2ee | v0.5.1 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-001 | CA-001, CA-009 | T-001, T-002, T-003, T-004, T-005, T-007, T-008 | tasks.md T-001, T-002, T-003, T-004, T-005, T-007, T-008 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-002 | CA-001 | T-002, T-007, T-008, T-009 | tasks.md T-002, T-007, T-008, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-003 | CA-002 | T-007, T-008, T-009 | tasks.md T-007, T-008, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-004 | CA-003 | T-007, T-008, T-009 | tasks.md T-007, T-008, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-005 | CA-004 | T-003, T-004, T-005, T-006 | tasks.md T-003, T-004, T-005, T-006 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-006 | CA-005, CA-007 | T-004, T-005, T-009 | tasks.md T-004, T-005, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-007 | CA-006 | T-008, T-009 | tasks.md T-008, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-008 | CA-008 | T-003, T-004, T-005, T-007, T-008 | tasks.md T-003, T-004, T-005, T-007, T-008 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-009 | CA-010 | T-003, T-004, T-005, T-007, T-008 | tasks.md T-003, T-004, T-005, T-007, T-008 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | RF-010 | CA-011 | T-003, T-004, T-005, T-007, T-008 | tasks.md T-003, T-004, T-005, T-007, T-008 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-001 | CA-002 | T-009 | tasks.md T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-002 | CA-006 | T-008, T-009 | tasks.md T-008, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-003 | CA-005 | T-009 | tasks.md T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-004 | CA-004 | T-003, T-005, T-006 | tasks.md T-003, T-005, T-006 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-005 | CA-001 | T-002, T-008, T-009 | tasks.md T-002, T-008, T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-006 | CA-003 | T-009 | tasks.md T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-007 | CA-005 | T-009 | tasks.md T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-008 | CA-007 | T-009 | tasks.md T-009 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-009 | CA-009 | T-001 | tasks.md T-001 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-010 | CA-010 | T-003, T-004, T-007, T-008 | tasks.md T-003, T-004, T-007, T-008 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |
| SPEC-007 | CB-011 | CA-011 | T-003, T-004, T-007, T-008 | tasks.md T-003, T-004, T-007, T-008 | AUSENTE | 502c69d | v0.6.0 | commit (AUD-043); evidencia de tarea (AUD-042); vínculo merge-release (AUD-044) |

La tabla aporta 71 filas, una por identificador de las siete specs: 9 de SPEC-001, 10 de SPEC-002, 9 de SPEC-003, 9 de SPEC-004, 8 de SPEC-005, 5 de SPEC-006 y 21 de SPEC-007. Ninguna celda queda vacía y el eslabón commit figura como `AUSENTE` en las 71 filas (AUD-043).

## 8. Revisión retrospectiva de SPEC-001 a SPEC-007

Cada bloque revisa una spec publicada en el commit de corte con sus cinco artefactos, sus compuertas registradas, su cobertura y sus tareas, y su integración y release. La revisión es documental y no crea ni corrige artefactos (CB-001). Tres eslabones de severidad Alta afectan a las siete specs: la evidencia de tarea no estandarizada (AUD-042), el commit de implementación no declarado (AUD-043) y el vínculo merge-release no declarado (AUD-044); el veredicto de cada bloque aplica la escala de 3.2 y la precedencia de DEC-008, y no se ajusta para coincidir con el veredicto global de la sección 9.

### SPEC-001

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/001-main-menu/spec.md:95`) y G4 (`specs/001-main-menu/spec.md:96`); dictamen CONVERGIDO (`specs/001-main-menu/validation_report.md:32`) y registro G4 del reporte marcado (`specs/001-main-menu/validation_report.md:36`).
- **Cobertura y tareas:** 4 tareas cerradas; `tasks.md` no referencia ningún `CA-NNN`, de modo que el enlace CA → T solo se reconstruye por tránsito a través del RF/CB (AUD-041, Media).
- **Integración y release:** merge `753c3e5` y release `v0.2.0`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta).
- **Veredicto individual:** `NO CONFORME`. Los tres eslabones de severidad Alta (AUD-042, AUD-043 y AUD-044) concurren con el enlace CA → T ausente (AUD-041, Media), y la regla de 3.2 asigna `NO CONFORME` por el hallazgo de severidad Alta.

### SPEC-002

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/002-orquestacion-subagentes-sdd/spec.md:156`) y G4 en la misma sección de aprobaciones; dictamen CONVERGIDO (`specs/002-orquestacion-subagentes-sdd/validation_report.md:159`) y registro G4 del reporte sin marcar (`specs/002-orquestacion-subagentes-sdd/validation_report.md:180`), en desacuerdo con el registro de `spec.md` (AUD-021, Media).
- **Cobertura y tareas:** 10 tareas cerradas; `tasks.md` registra 5 referencias a `CA-NNN` y el enlace CA → T consta; la reapertura ratificada de `specs/002-orquestacion-subagentes-sdd/spec.md:156` carece de historial de transiciones (AUD-053, Media).
- **Integración y release:** merge `ec6a063` y release `v0.3.0`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta).
- **Veredicto individual:** `NO CONFORME`. La evidencia de tarea y los dos eslabones de integración aportan hallazgos de severidad Alta (AUD-042, AUD-043 y AUD-044), a los que se suman el registro dual divergente (AUD-021) y la reapertura sin historial (AUD-053); la regla de 3.2 conduce a `NO CONFORME`.

### SPEC-003

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/003-validacion-g4/spec.md:148`) y G4 en la misma sección de aprobaciones; dictamen CONVERGIDO (`specs/003-validacion-g4/validation_report.md:118`) y registro G4 del reporte sin marcar (`specs/003-validacion-g4/validation_report.md:138`), en desacuerdo con el registro de `spec.md` (AUD-021, Media).
- **Cobertura y tareas:** 5 tareas cerradas; `tasks.md` registra 5 referencias a `CA-NNN` y el enlace CA → T consta.
- **Integración y release:** merge `39b27a2` y release `v0.3.1`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta).
- **Veredicto individual:** `NO CONFORME`. El cierre de tareas consta, pero la evidencia de tarea y los dos eslabones de integración aportan hallazgos de severidad Alta (AUD-042, AUD-043 y AUD-044), y el registro G4 del reporte diverge del de `spec.md` (AUD-021, Media); la regla de 3.2 conduce a `NO CONFORME`.

### SPEC-004

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/004-editor-documentacion/spec.md:151`) y G4 en la misma sección de aprobaciones; dictamen CONVERGIDO (`specs/004-editor-documentacion/validation_report.md:135`) y registro G4 del reporte sin marcar (`specs/004-editor-documentacion/validation_report.md:141`), en desacuerdo con el registro de `spec.md` (AUD-021, Media).
- **Cobertura y tareas:** 5 tareas cerradas; `tasks.md` no referencia ningún `CA-NNN`, de modo que el enlace CA → T solo se reconstruye por tránsito a través del RF/CB (AUD-041, Media).
- **Integración y release:** merge `b38ed6c` y release `v0.4.0`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta).
- **Veredicto individual:** `NO CONFORME`. La evidencia de tarea y los dos eslabones de integración aportan hallazgos de severidad Alta (AUD-042, AUD-043 y AUD-044), junto con el enlace CA → T ausente (AUD-041) y el registro G4 divergente (AUD-021); la regla de 3.2 conduce a `NO CONFORME`.

### SPEC-005

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/005-compuertas-completas/spec.md:153`) y G4 en la misma sección de aprobaciones; dictamen CONVERGIDO (`specs/005-compuertas-completas/validation_report.md:68`) y registro G4 del reporte sin marcar (`specs/005-compuertas-completas/validation_report.md:73`), en desacuerdo con el registro de `spec.md` (AUD-021, Media).
- **Cobertura y tareas:** 9 tareas cerradas; `tasks.md` registra 10 referencias a `CA-NNN` y el enlace CA → T consta.
- **Integración y release:** merge `2781db5` y release `v0.5.0`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta).
- **Veredicto individual:** `NO CONFORME`. La cobertura CA → T consta y las tareas están cerradas, pero la evidencia de tarea y los dos eslabones de integración aportan hallazgos de severidad Alta (AUD-042, AUD-043 y AUD-044), a los que se suma el registro G4 divergente (AUD-021, Media); la regla de 3.2 conduce a `NO CONFORME`.

### SPEC-006

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/006-observaciones-cierre/spec.md:131`) y G4 en la misma sección de aprobaciones; dictamen CONVERGIDO (`specs/006-observaciones-cierre/validation_report.md:46`) y registro G4 del reporte sin marcar (`specs/006-observaciones-cierre/validation_report.md:51`), en desacuerdo con el registro de `spec.md` (AUD-021, Media).
- **Cobertura y tareas:** 5 tareas cerradas; `tasks.md` no referencia ningún `CA-NNN`, de modo que el enlace CA → T solo se reconstruye por tránsito a través del RF/CB (AUD-041, Media).
- **Integración y release:** merge `0afc2ee` y release `v0.5.1`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta).
- **Veredicto individual:** `NO CONFORME`. La evidencia de tarea y los dos eslabones de integración aportan hallazgos de severidad Alta (AUD-042, AUD-043 y AUD-044), junto con el enlace CA → T ausente (AUD-041) y el registro G4 divergente (AUD-021); la regla de 3.2 conduce a `NO CONFORME`.

### SPEC-007

- **Artefactos presentes:** `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`.
- **Estado:** `released` en el frontmatter, coincidente con `specs/INDEX.md`.
- **Compuertas registradas:** G1 (`specs/007-branch-protection/spec.md:231`) y G4 (`specs/007-branch-protection/spec.md:232`); dictamen CONVERGIDO (`specs/007-branch-protection/validation_report.md:61`) y registro G4 del reporte marcado (`specs/007-branch-protection/validation_report.md:66`).
- **Cobertura y tareas:** 10 tareas cerradas; `tasks.md` registra 7 referencias a `CA-NNN` y el enlace CA → T consta.
- **Integración y release:** merge `502c69d` y release `v0.6.0`; la spec no declara el commit de implementación (AUD-043, Alta) ni el vínculo entre el merge y el release (AUD-044, Alta), y la referencia remota `remotes/origin/release/v0-6-0` permanece tras el cierre (AUD-082, Baja).
- **Veredicto individual:** `NO CONFORME`. Es la spec con el registro documental más completo, pues el registro G4 del reporte está marcado y la cobertura CA → T consta, pero la evidencia de tarea y los dos eslabones de integración aportan hallazgos de severidad Alta (AUD-042, AUD-043 y AUD-044), y la referencia remota del release persiste (AUD-082, Baja); la regla de 3.2 conduce a `NO CONFORME`.

## 9. Veredicto global

La tabla de agregación de 3.4 se recorre de arriba abajo y se declara la primera regla que se cumple; el veredicto de esa fila es el veredicto global del informe (`specs/008-auditoria-cumplimiento-sdd/plan.md:215`, `specs/008-auditoria-cumplimiento-sdd/plan.md:253`).

**Regla aplicada:** regla 1, porque existe al menos una dimensión `NO CONFORME` con al menos un hallazgo de severidad Crítica o Alta (`specs/008-auditoria-cumplimiento-sdd/plan.md:217`).

| Dimensión | Veredicto | Hallazgos que la activan | Severidad que la activa |
|---|---|---|---|
| D1 | `NO CONFORME` | AUD-002 | Alta |
| D2 | `NO CONFORME` | AUD-013 | Crítica |
| D4 | `NO CONFORME` | AUD-031, AUD-035 | Crítica |
| D5 | `NO CONFORME` | AUD-042, AUD-043, AUD-044 | Alta |
| D6 | `NO CONFORME` | AUD-051, AUD-052 | Alta |
| D7 | `NO CONFORME` | AUD-062 | Crítica |
| D8 | `NO CONFORME` | AUD-072 | Alta |
| D10 | `NO CONFORME` | AUD-094 | Alta |

D3 y D9 quedan en `PARCIAL` y no activan la regla por sí solas; su veredicto y su justificación constan en la matriz de la sección 4. Las reglas 2 a 6 no se evalúan, porque la precedencia se detiene en la primera fila cumplida.

**Veredicto global:** `NO CONFORME`.

El recuento de compuertas de la sección 6, con cuatro `CONFORME` y dos `PARCIAL`, no altera el resultado: la regla de 3.4 opera sobre los veredictos de dimensión y el objeto de D4 es el mecanismo de control de las compuertas, no la evidencia de cada una.

### 9.1 Constancia de rechazo de correcciones

La auditoría no modificó, corrigió, renombró ni eliminó ningún artefacto auditado, y su única escritura fue este informe (`specs/008-auditoria-cumplimiento-sdd/spec.md:151`, RF-014). Una solicitud de corrección sobre un artefacto auditado se rechaza y se remite a una especificación posterior (CB-010, `specs/008-auditoria-cumplimiento-sdd/spec.md:243`). Ningún hallazgo de la sección 5 fue reparado en el curso de la auditoría: cada uno conserva su remediación propuesta y su fila en la hoja de ruta de la sección 10, que registra correcciones pendientes y no correcciones aplicadas.

## 10. Hoja de ruta B1 a B4

La tabla asigna cada hallazgo de 5.2 a un bloque de remediación y a una de las tres clasificaciones de RF-013 (`specs/008-auditoria-cumplimiento-sdd/plan.md:161-169`, `specs/008-auditoria-cumplimiento-sdd/spec.md:147`). Hay una fila por hallazgo y el orden es ascendente por `AUD-NNN`; la columna `Remediación` describe la acción en una frase y remite al bloque de detalle del hallazgo.

| Bloque | Remediación | Hallazgo | Clasificación |
|---|---|---|---|
| B1 | Alinear la autodeclaración de los diecisiete documentos de la base con el rango que les asigna la sección 2; ver AUD-001. | `AUD-001` | editorial |
| B1 | Resolver por especificación la exclusión de `docs/sdd/PROTOCOLO_OPERATIVO.md` de la base normativa, sin alterar la jerarquía de la constitución; ver AUD-002. | `AUD-002` | requiere spec |
| B1 | Unificar la forma de los criterios de aceptación entre la guía de `spec.md` y la plantilla; ver AUD-003. | `AUD-003` | editorial |
| B1 | Fijar una sola anchura de identificador para los casos borde en la guía y en la plantilla; ver AUD-004. | `AUD-004` | editorial |
| B1 | Alinear la sección de casos límite de la guía de etapas con el contenido mínimo de la plantilla; ver AUD-005. | `AUD-005` | editorial |
| B1 | Incorporar a la base un índice con la precedencia interna de los documentos de igual rango; ver AUD-006. | `AUD-006` | editorial |
| B1 | Actualizar el recuento declarado por el procedimiento sin alterar la regla de inclusión; ver AUD-007. | `AUD-007` | editorial |
| B2 | Fijar una sola compuerta de entrada a Implement y alinear el comando y el agente; ver AUD-011. | `AUD-011` | requiere spec |
| B2 | Declarar el momento único de G3 y su relación con el cierre de la etapa; ver AUD-012. | `AUD-012` | requiere spec |
| B2 | Separar la verificación de cierre de G4 de la escritura previa del reporte, con orden explícito en el comando y en el agente; ver AUD-013. | `AUD-013` | requiere spec |
| B2 | Asignar a un comando la escritura de los tres estados intermedios y su registro en el historial de la spec; ver AUD-014. | `AUD-014` | requiere spec |
| B2 | Fijar un solo artefacto como titular del registro de G4 y retirar la casilla duplicada; ver AUD-021. | `AUD-021` | requiere spec |
| B4 | Añadir el campo de criterio de aceptación al contrato de tarea y a la matriz de cobertura; ver AUD-022. | `AUD-022` | requiere spec |
| B1 | Definir el contrato de la documentación analítica y el rol habilitado para redactarla; ver AUD-023. | `AUD-023` | requiere spec |
| B2 | Incorporar al validador la comprobación de la cadena `Approved` y del declarante en la compuerta G1; ver AUD-031. | `AUD-031` | requiere spec |
| B2 | Elevar a error la ausencia de la línea `Cubre:` y alinear la compuerta G2 con el criterio de G3; ver AUD-032. | `AUD-032` | requiere spec |
| B2 | Incluir la verificación de tareas abiertas en la ejecución agregada o declarar su ausencia como resultado parcial; ver AUD-033. | `AUD-033` | requiere spec |
| B2 | Exigir en G4 la línea de aprobación y el declarante, además del dictamen del reporte; ver AUD-034. | `AUD-034` | requiere spec |
| B2 | Dotar a G5 y G6 de condiciones y verificaciones propias, con la aprobación de release como requisito de G6; ver AUD-035. | `AUD-035` | requiere spec |
| B4 | Registrar el criterio de aceptación en las tareas de las tres specs y verificar la correspondencia en la revisión de cierre; ver AUD-041. | `AUD-041` | proceso |
| B4 | Fijar los campos mínimos de la evidencia de tarea y su comprobación en el validador; ver AUD-042. | `AUD-042` | requiere spec |
| B4 | Convertir la ausencia de `Spec:` en error y ejecutar la comprobación Git en la verificación agregada; ver AUD-043. | `AUD-043` | requiere spec |
| B4 | Registrar en el reporte de validación el hash del merge y el tag de release de cada spec; ver AUD-044. | `AUD-044` | requiere spec |
| B2 | Declarar la tabla de transiciones admitidas y comprobarla en el validador; ver AUD-051. | `AUD-051` | requiere spec |
| B2 | Asignar la escritura de los tres estados a las etapas que los producen o retirarlos del conjunto admitido; ver AUD-052. | `AUD-052` | requiere spec |
| B2 | Añadir el historial de transiciones al artefacto de la spec al reabrirla o ratificarla; ver AUD-053. | `AUD-053` | proceso |
| B2 | Comprobar la simetría de `supersedes` y `superseded_by` y la coherencia con el estado; ver AUD-054. | `AUD-054` | requiere spec |
| B1 | Declarar la regla de versionado de las specs y aplicarla al historial de cambios; ver AUD-055. | `AUD-055` | requiere spec |
| B3 | Declarar en cada rol las reglas de shell y de subagentes y contrastarlas con la operación registrada; ver AUD-061. | `AUD-061` | proceso |
| B2 | Registrar la aprobación con un mecanismo de autoría verificable y restringir la escritura de la sección de aprobaciones; ver AUD-062. | `AUD-062` | requiere spec |
| B3 | Declarar el rol de auditoría con solo lectura sobre los artefactos auditados y escritura limitada al informe; ver AUD-063. | `AUD-063` | requiere spec |
| B3 | Declarar la precedencia entre permisos solapados y reescribir la matriz sin solapamiento; ver AUD-064. | `AUD-064` | editorial |
| B3 | Ejecutar la batería de pruebas en un flujo de integración y registrar su salida en el reporte de validación; ver AUD-071. | `AUD-071` | proceso |
| B4 | Condicionar el cierre de la tarea al bloque de evidencia y comprobar su presencia en el validador; ver AUD-072. | `AUD-072` | requiere spec |
| B3 | Sincronizar `dev` con `main` mediante merge `--no-ff` y verificar la convergencia antes de cada release; ver AUD-081. | `AUD-081` | proceso |
| B3 | Eliminar la referencia remota obsoleta al cerrar el release y verificar el listado de ramas; ver AUD-082. | `AUD-082` | proceso |
| B3 | Decidir la integración o el descarte de la rama y registrar la decisión en el release correspondiente; ver AUD-083. | `AUD-083` | proceso |
| B3 | Registrar los seis cambios por la vía de integración declarada y anotarlos en el registro de cambios; ver AUD-084. | `AUD-084` | proceso |
| B3 | Actualizar la línea de `MEMORY.md` con el estado real del archivo; ver AUD-091. | `AUD-091` | editorial |
| B1 | Completar la navegación del índice del corpus con los documentos ausentes; ver AUD-093. | `AUD-093` | editorial |
| B2 | Alinear la verificación automática con las compuertas y transiciones declaradas o declarar por escrito el alcance parcial del verde; ver AUD-094. | `AUD-094` | requiere spec |

El recuento por bloque es B1 10, B2 16, B3 9 y B4 6, y por clasificación editorial 9, requiere spec 24 y proceso 8; las 41 filas coinciden con los 41 bloques `### AUD-NNN` de 5.2.

El orden de ejecución es B1 antes de B2, B2 antes de B3, y B4 como fase posterior. El fundamento es que B1 fija la autoridad normativa y B2 el mecanismo de control: una compuerta no se puede automatizar sobre una base cuya precedencia interna no está resuelta (AUD-002, AUD-006), y la práctica de B3 se contrasta contra las reglas que B2 deja verificables (AUD-061, AUD-062). B4 amplía la cadena de trazabilidad sobre los contratos y las comprobaciones ya fijados, y por eso se ejecuta al final (AUD-022, AUD-072).

## 11. Limitaciones y elementos no verificables

Cada elemento se declara con tres datos: causa de la imposibilidad, artefacto que faltaría y dimensión o compuerta afectada (RF-016, `specs/008-auditoria-cumplimiento-sdd/spec.md:159`; `specs/008-auditoria-cumplimiento-sdd/plan.md:61`).

| Elemento | Causa de la imposibilidad | Artefacto que faltaría | Dimensión o compuerta afectada |
|---|---|---|---|
| Validación posterior al merge | La validación posterior a la fusión no dejó registro conservado en el periodo auditado. | Un artefacto de validación post-integración con fecha, commit y resultado. | G5 y D8. |
| Protección de ramas de SPEC-007 | La configuración remota de GitHub no forma parte del repositorio y la auditoría no ejecutó consultas remotas (`specs/008-auditoria-cumplimiento-sdd/plan.md:82`). | La evidencia de la configuración remota o una verificación reproducible de la protección. | D9. |
| Autoría de las aprobaciones | La aprobación consta como línea de texto plano y esa línea no acredita autoría (`docs/constitution.md:62`). | Un mecanismo de aprobación con autoría verificable. | D7 y las compuertas G1, G4 y G6. |
| Historial de transiciones de estado | El recorrido entre estados no se conserva en ningún artefacto; la spec solo expone el estado vigente. | Un registro de transiciones con estado de origen, estado de destino y fecha. | D6. |
| Integración continua y hooks | No existe flujo de integración continua ni hook activo en el periodo auditado. | Un flujo de verificación automática ligado a la integración. | D8. |
| Estado remoto y credenciales | La auditoría no examina configuraciones remotas ni secretos, y el contenido de `.env` queda fuera de su alcance. | La evidencia del estado remoto y del procedimiento de gestión de secretos. | D9 y D10. |

Ningún elemento de esta lista se presume cumplido: cada uno queda como `NO VERIFICABLE` en su ámbito y se remite a la compuerta o dimensión indicada, conforme a la regla de suficiencia que impide sustituir la evidencia ausente por una suposición (`specs/008-auditoria-cumplimiento-sdd/plan.md:83`).

## 12. Anexos de evidencia

Los anexos reproducen las salidas y los mapas auxiliares que las secciones anteriores citan de forma abreviada (`specs/008-auditoria-cumplimiento-sdd/plan.md:62`, `specs/008-auditoria-cumplimiento-sdd/plan.md:320`).

### 12.1 Inventario calculado

El cálculo aplica la regla de inclusión de 2.2 al árbol del commit de corte `1d6b2c5`; la relación nominal de los 22 documentos figura en 2.3.

| Magnitud | Valor |
|---|---|
| Archivos Markdown en la raíz de `docs/sdd/` en el corte | 21 |
| Nombres excluidos | 6, de los cuales 4 están presentes en el corte y 2 quedan fuera del periodo |
| Documentos normativos incluidos de la raíz | 17 |
| Plantillas de `docs/sdd/plantillas/` | 5 |
| Total de documentos normativos | 22 |

El desglose es 21 archivos Markdown en la raíz del corte, 4 de ellos con nombre excluido, de modo que quedan 17 documentos incluidos; sumados a 5 plantillas dan los 22 documentos de la base normativa.

### 12.2 Salida del validador

| Consulta | Salida | Código de salida |
|---|---|---|
| `python tools\sdd\validate.py --all` | `[WARN] specs\008-auditoria-cumplimiento-sdd\validation_report.md: validation_report.md no existe` y `OK: sin hallazgos.` | `0` |
| `python tools\sdd\validate.py --spec SPEC-008 --gate G2` | `OK: sin hallazgos.` | `0` |

```text
> python tools\sdd\validate.py --all
[WARN] specs\008-auditoria-cumplimiento-sdd\validation_report.md: validation_report.md no existe
OK: sin hallazgos.

> python tools\sdd\validate.py --spec SPEC-008 --gate G2
OK: sin hallazgos.
```

La salida se reproduce literal con el código de salida de cada ejecución, registrada en la ficha de 1.3 (C4). La línea `[WARN]` de la ejecución `--all` es no bloqueante: registra que el `validation_report.md` de esta spec aún no existe en el momento de la ejecución y no altera el resultado, cuyo código de salida es `0`. Su alcance respecto de las compuertas se analiza en las dimensiones D4, D6 y D10 y no se amplía en este anexo (RF-015, `specs/008-auditoria-cumplimiento-sdd/spec.md:155`).

### 12.3 Extractos de historial Git

El commit de corte es `1d6b2c5a0424eff677d330c478c27628150d7106`, con el asunto `docs(sdd): contrato de auditoria de cumplimiento SPEC-008`; `git show --stat --oneline HEAD` registra cinco archivos y 1326 inserciones.

| Archivo | Inserciones |
|---|---|
| `specs/008-auditoria-cumplimiento-sdd/clarify.md` | 87 |
| `specs/008-auditoria-cumplimiento-sdd/plan.md` | 426 |
| `specs/008-auditoria-cumplimiento-sdd/spec.md` | 387 |
| `specs/008-auditoria-cumplimiento-sdd/tasks.md` | 425 |
| `specs/INDEX.md` | 1 |

Las seis entradas de `git status --short`, transcritas de 1.3, son:

```text
 M docs/sdd/PROTOCOLO_OPERATIVO.md
 M docs/sdd/README.md
 M docs/sdd/diagrama_flujo_ciclo_vida_sdd.md
 M docs/sdd/guia_maestra_sdd.md
?? docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md
?? docs/sdd/plan_cierre_brechas_sdd.md
```

Los siete merges con dos padres que registra la sección 6 (G5) y su correspondencia con la spec y el release de la sección 7 son:

| Merge | Spec | Release |
|---|---|---|
| `753c3e5` | SPEC-001 | `v0.2.0` |
| `ec6a063` | SPEC-002 | `v0.3.0` |
| `39b27a2` | SPEC-003 | `v0.3.1` |
| `b38ed6c` | SPEC-004 | `v0.4.0` |
| `2781db5` | SPEC-005 | `v0.5.0` |
| `0afc2ee` | SPEC-006 | `v0.5.1` |
| `502c69d` | SPEC-007 | `v0.6.0` |

Los ocho tags anotados llevan el mensaje `Release vX.Y.Z` (`AGENTS.md:42`) y su aprobación consta en `CHANGELOG.md`:

| Tag | Mensaje | Registro de cambios | Aprobación |
|---|---|---|---|
| `v0.1.0` | `Release v0.1.0` | `CHANGELOG.md:130` | `CHANGELOG.md:174` |
| `v0.2.0` | `Release v0.2.0` | `CHANGELOG.md:101` | `CHANGELOG.md:128` |
| `v0.3.0` | `Release v0.3.0` | `CHANGELOG.md:80` | `CHANGELOG.md:99` |
| `v0.3.1` | `Release v0.3.1` | `CHANGELOG.md:66` | `CHANGELOG.md:78` |
| `v0.4.0` | `Release v0.4.0` | `CHANGELOG.md:52` | `CHANGELOG.md:64` |
| `v0.5.0` | `Release v0.5.0` | `CHANGELOG.md:37` | `CHANGELOG.md:50` |
| `v0.5.1` | `Release v0.5.1` | `CHANGELOG.md:27` | `CHANGELOG.md:35` |
| `v0.6.0` | `Release v0.6.0` | `CHANGELOG.md:13` | `CHANGELOG.md:25` |

El historial se cita como evidencia de clase E4, con la salida del comando y su código de salida (`specs/008-auditoria-cumplimiento-sdd/plan.md:73`).

### 12.4 Mapa de rangos de hallazgos

| Dimensión | Rango reservado | Rango real | Hallazgos |
|---|---|---|---|
| D1 | `AUD-001` a `AUD-010` | `AUD-001` a `AUD-007` | 7 |
| D2 | `AUD-011` a `AUD-020` | `AUD-011` a `AUD-014` | 4 |
| D3 | `AUD-021` a `AUD-030` | `AUD-021` a `AUD-023` | 3 |
| D4 | `AUD-031` a `AUD-040` | `AUD-031` a `AUD-035` | 5 |
| D5 | `AUD-041` a `AUD-050` | `AUD-041` a `AUD-044` | 4 |
| D6 | `AUD-051` a `AUD-060` | `AUD-051` a `AUD-055` | 5 |
| D7 | `AUD-061` a `AUD-070` | `AUD-061` a `AUD-064` | 4 |
| D8 | `AUD-071` a `AUD-080` | `AUD-071` a `AUD-072` | 2 |
| D9 | `AUD-081` a `AUD-090` | `AUD-081` a `AUD-084` | 4 |
| D10 | `AUD-091` a `AUD-099` | `AUD-091` a `AUD-094` | 3 |

El rango reservado procede de la tabla de rangos de `specs/008-auditoria-cumplimiento-sdd/plan.md:173-184` y el rango real del informe. Ninguna dimensión supera su capacidad de diez hallazgos, de modo que no se aplica la extensión prevista en DEC-006 (`specs/008-auditoria-cumplimiento-sdd/plan.md:186`). La numeración es creciente dentro del rango real de cada dimensión y las diez filas suman 41 hallazgos, cifra que coincide con la tabla consolidada de 5.1; el traslado del hallazgo de inventario a D1, numerado `AUD-007`, deja el número 092 sin uso en D10, sin reasignarlo.
