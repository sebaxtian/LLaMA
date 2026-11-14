# Informe de auditoría — cierre de la hoja de ruta B1 a B4 y conformidad del régimen v2

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-14 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), specs `SPEC-001` a `SPEC-012`, validador `tools/sdd/validate.py`, suite `tools/sdd/tests`, matriz de agentes de `.opencode/`, flujo de integración continua, historial de integración y registro de cambios.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas, no aprueba compuertas y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `5efac03d7532f28bd767c72a74601da76c35b908` (`Merge pull request #10 from sebaxtian/docs/cierre-integracion-spec-012`) |
| Rama | `dev` |
| Fecha de corte | 2026-11-14 |
| Validador ejecutado | `python tools\sdd\validate.py --all` — **no ejecutado en esta auditoría**; el entorno de ejecución denegó la herramienta de shell (§9) |
| Entorno | Windows 11 (`win32`); lectura del árbol de trabajo y de los archivos de `.git`; consulta HTTP a la API de GitHub sobre `sebaxtian/LLaMA`; sin ejecución de comandos |
| Rol ejecutor | `auditor` |

**Método.** La reauditoría se ejecutó en cinco pasos. Primero, lectura íntegra de `docs/sdd/auditoria_cumplimiento_sdd.md` y enumeración de sus cuarenta y un hallazgos `AUD-NNN`. Segundo, contraste de cada hallazgo con la norma aplicable en su rango y con el artefacto que lo cierra. Tercero, lectura de la base v2 completa, de las siete plantillas, de las doce specs y de su frontmatter. Cuarto, contraste del validador y de la suite con el contrato de §14 del protocolo y con el contrato de cada spec. Quinto, verificación del historial: `packed-refs` para ramas y tags, `logs/HEAD` para la secuencia de commits, fusiones y sincronizaciones, y `https://api.github.com/repos/sebaxtian/LLaMA/compare/main...dev` para la divergencia entre ramas.

La reauditoría no reescribe el informe de origen. Los identificadores `AUD-001` a `AUD-094` conservan el significado que les asigna `docs/sdd/auditoria_cumplimiento_sdd.md` y esta versión añade hallazgos nuevos con la continuación inmediata de cada dimensión, conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md:212`.

## 2. Base normativa e inventario

La jerarquía vigente consta de siete rangos y una categoría sin rango, declarada de forma coincidente en tres niveles: `docs/constitution.md:48-59`, `docs/sdd/PROTOCOLO_OPERATIVO.md:29-38` y `docs/sdd/README.md:15-24`. Los siete rangos son constitución, `AGENTS.md`, protocolo operativo, flujo Git, plantillas, contrato de la feature e implementación verificable.

| Documento | Rango | Cita |
|---|---|---|
| `docs/constitution.md` | 1 | `docs/constitution.md:52` |
| `AGENTS.md` | 2 | `docs/constitution.md:53` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | `docs/constitution.md:54` |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | `docs/constitution.md:55` |
| `docs/sdd/plantillas/*.md` | 5 | `docs/constitution.md:56` |
| `specs/NNN-slug/*.md` | 6 | `docs/constitution.md:57` |
| `src/`, `tools/`, `tests/`, `.opencode/` | 7 | `docs/constitution.md:58` |
| Guías, informes, `README.md`, `MEMORY.md`, índice y `CHANGELOG.md` | Sin rango | `docs/constitution.md:59` |

El inventario del corpus se calcula por filas y no por cifra fija (`docs/sdd/README.md:65`). La tabla de inventario de `docs/sdd/README.md:28-61` aporta treinta y dos filas: veinticuatro archivos Markdown de la raíz de `docs/sdd/`, siete plantillas de `docs/sdd/plantillas/` y el archivo de datos `firmantes_autorizados`. La comprobación por nombre contra el árbol del commit auditado no registra archivo sin fila ni fila sin archivo, con la excepción de este informe, que se crea después del corte y se registra en AUD-096.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida de consulta registrada. Una afirmación de cierre exige la norma aplicable y el artefacto que la satisface; una afirmación de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento.

**Escala de veredicto de dimensión.**

| Veredicto | Regla de decisión aplicada |
|---|---|
| `CONFORME` | La dimensión no registra hallazgo vigente ni observación abierta. |
| `CONFORME CON OBSERVACIONES` | La dimensión cumple su objeto con evidencia y registra observaciones de severidad Media o Baja que no rompen la trazabilidad ni anulan una compuerta. |
| `NO CONFORME` | La dimensión registra al menos una observación de severidad Alta, o un hallazgo de la auditoría de origen queda parcialmente abierto. |

**Escala de severidad.** `Crítica` anula una compuerta o permite un cambio sin spec aprobada; `Alta` rompe la trazabilidad o la evidencia de verificación; `Media` produce divergencia entre documentos de distinto rango sin pérdida de trazabilidad; `Baja` produce una inconsistencia editorial o documental menor (`docs/sdd/PROTOCOLO_OPERATIVO.md:211`; `docs/sdd/plantillas/informe_auditoria.md:39-46`).

**Estados de cierre empleados.** `CERRADO` designa el hallazgo cuya causa desapareció y cuenta con artefacto y evidencia. `CERRADO POR EXENCIÓN` designa el hallazgo cuya causa se resolvió por una decisión registrada del propietario o por la cláusula de legado, con la divergencia textual conservada y declarada. `PARCIAL` designa el hallazgo cuya causa persiste en un subconjunto acotado. `VIGENTE` designa el hallazgo sin tratamiento.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Hallazgos y observaciones |
|---|---|---|---|---|
| D1 | Autoridad normativa, vigencia y aplicabilidad de cada documento | `CONFORME CON OBSERVACIONES` | `docs/constitution.md:48-59`; `docs/sdd/PROTOCOLO_OPERATIVO.md:29-47`; `docs/sdd/README.md:15-24`, `:28-61` | AUD-001 a AUD-007 cerrados; AUD-008 |
| D2 | Ciclo de siete etapas y estado resultante | `CONFORME CON OBSERVACIONES` | `docs/sdd/PROTOCOLO_OPERATIVO.md:72-90`; `.opencode/commands/sdd-implement.md:8-14`; `.opencode/commands/sdd-validate.md:8-12` | AUD-011 a AUD-014 cerrados; AUD-015 |
| D3 | Contratos de artefactos | `CONFORME CON OBSERVACIONES` | `docs/sdd/plantillas/spec.md:67-72`; `docs/sdd/plantillas/tasks.md:11-31`; `docs/sdd/plantillas/validation_report.md:5`; `docs/sdd/plantillas/informe_auditoria.md:1-93` | AUD-021 a AUD-023 cerrados; AUD-024 |
| D4 | Compuertas G1 a G6: condición, evidencia y verificación | `CONFORME CON OBSERVACIONES` | `docs/sdd/PROTOCOLO_OPERATIVO.md:134-141`; `tools/sdd/validate.py:420-529`, `:569-588`, `:769-933` | AUD-031 a AUD-035 cerrados; AUD-036 y AUD-037 |
| D5 | Trazabilidad `RF/CB → CA → T → evidencia → commit → merge → release` | `CONFORME CON OBSERVACIONES` | 48 tareas con criterio y evidencia; siete reportes con `Merge:` y `Release:`; `tools/sdd/validate.py:1057-1204` | AUD-041 a AUD-044 cerrados; AUD-045 y AUD-046 |
| D6 | Estados, transiciones e historial | `CONFORME CON OBSERVACIONES` | `docs/sdd/PROTOCOLO_OPERATIVO.md:92-128`; `tools/sdd/validate.py:92-131`, `:594-729`; `specs/012-trazabilidad-profunda-sdd/spec.md:331-341` | AUD-051 a AUD-055 cerrados; AUD-056 |
| D7 | Roles y menor privilegio | `CONFORME CON OBSERVACIONES` | Seis agentes con reglas de shell y precedencia; `docs/sdd/PROTOCOLO_OPERATIVO.md:280-294`; `.opencode/agents/auditor.md:51-91` | AUD-061 a AUD-064 cerrados; AUD-065 |
| D8 | Evidencia y verificación: existencia, suficiencia y reproducibilidad | `NO CONFORME` | `.github/workflows/sdd.yml:14-23`; `tools/sdd/tests` con 131 métodos de prueba; `docs/Flujo_de_Trabajo_Git.md:228` | AUD-071 `PARCIAL`; AUD-073 de severidad Alta y AUD-074 |
| D9 | Integración Git y release | `NO CONFORME` | `packed-refs` con ocho tags anotados; ramas remotas `dev` y `main`; `compare/main...dev` con 48 por delante y 0 por detrás; `docs/sdd/PROTOCOLO_OPERATIVO.md:304` | AUD-081 a AUD-084 cerrados; AUD-085 de severidad Alta y AUD-086 |
| D10 | Consistencia documental operativa | `CONFORME CON OBSERVACIONES` | `MEMORY.md:40`; `docs/sdd/README.md:28-61`; `tools/sdd/validate.py:939-1014`; `specs/INDEX.md:7-18` | AUD-091, AUD-093 y AUD-094 cerrados; AUD-095 a AUD-097 |

## 5. Hallazgos

### 5.1 Cierre de los cuarenta y un hallazgos de origen

| AUD-NNN | Dimensión | Estado | Evidencia del cierre | Nota |
|---|---|---|---|---|
| AUD-001 | D1 | `CERRADO` | `docs/constitution.md:59` sitúa las guías en la categoría sin rango; `docs/sdd/README.md:24` reproduce esa categoría; `docs/sdd/compendio_sdd.md:3` declara carácter no normativo | La autodeclaración de las guías coincide ahora con el rango que la base les atribuye |
| AUD-002 | D1 | `CERRADO` | `docs/constitution.md:54` asigna rango 3 al protocolo; `docs/sdd/PROTOCOLO_OPERATIVO.md:33` lo declara; `docs/sdd/README.md:19` lo indexa | La exclusión del protocolo era una decisión del contrato de SPEC-008 y no una regla de la base v2 |
| AUD-003 | D1 | `CERRADO POR EXENCIÓN` | `specs/009-base-normativa-sdd/plan.md:397-398` resuelve la contradicción por rango sin reescribir la guía; `docs/constitution.md:56` declara la plantilla como rango 5 | La guía conserva la forma «Definition of Done» (`docs/sdd/guia_spec_md.md:148`) y prevalece la plantilla; deuda editorial en AUD-008 |
| AUD-004 | D1 | `CERRADO POR EXENCIÓN` | `docs/sdd/PROTOCOLO_OPERATIVO.md:218` fija tres dígitos; `docs/sdd/plantillas/clarify.md:18-20` usa `CB-001`; la guía conserva `CB-NUEVO-01` en `docs/sdd/guia_clarify_md.md:126` | La precedencia resuelve el identificador; la guía no se reescribió y queda en AUD-008 |
| AUD-005 | D1 | `CERRADO POR EXENCIÓN` | `docs/constitution.md:56` y `docs/sdd/PROTOCOLO_OPERATIVO.md:166` fijan el contenido mínimo en la plantilla; `docs/sdd/referencia_7_etapas_sdd.md:135` conserva el título anterior | El contenido mínimo se decide por rango; deuda editorial en AUD-008 |
| AUD-006 | D1 | `CERRADO` | `docs/sdd/README.md:5-11` declara navegación y precedencia interna; `docs/constitution.md:63` remite el desempate al índice | El índice es documento sin rango y declara el desempate de cada rango |
| AUD-007 | D1 | `CERRADO` | `docs/sdd/README.md:65` sustituye la cifra fija por la regla de contar filas; `docs/sdd/PROTOCOLO_OPERATIVO.md:360-388` no fija recuento de documentos | El inventario se calcula desde la tabla |
| AUD-011 | D2 | `CERRADO` | `.opencode/commands/sdd-implement.md:8` exige `tasked` y G2 registrada; `.opencode/agents/sdd.md:154` declara la misma precondición | Una sola compuerta de entrada a Implement |
| AUD-012 | D2 | `CERRADO` | `.opencode/commands/sdd-implement.md:14` declara «G3 no se evalúa por tarea»; `.opencode/agents/sdd.md:155` la reserva al cierre; `docs/sdd/PROTOCOLO_OPERATIVO.md:79` fija el cierre de la etapa | Un solo momento de G3 |
| AUD-013 | D2 | `CERRADO` | `.opencode/commands/sdd-validate.md:12` ordena no evaluar G4 y escribir el reporte antes; `docs/sdd/PROTOCOLO_OPERATIVO.md:139` exige el reporte convergido y la firma; `tools/sdd/validate.py:105-111` exige el estado `implemented` como origen | El reporte existe antes de la evaluación de G4 |
| AUD-014 | D2 | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:126` asigna la escritura de T4 a T7 al orquestador; `.opencode/commands/sdd-implement.md:9` y `:14` la detallan; `specs/012-trazabilidad-profunda-sdd/spec.md:335-341` registra las filas | Los tres estados intermedios tienen escritor declarado; la atribución de responsable se evalúa en AUD-056 |
| AUD-021 | D3 | `CERRADO` | `docs/sdd/plantillas/spec.md:69-72` admite dos casillas; `docs/sdd/plantillas/validation_report.md:5` retira la casilla del reporte; `tools/sdd/validate.py:1424-1428` marca el defecto | El registro de G4 tiene una sola ubicación; la casilla residual se registra en AUD-024 |
| AUD-022 | D3 | `CERRADO` | `docs/sdd/plantillas/tasks.md:15` declara `Criterio de aceptación`; las 48 tareas de `SPEC-001` a `SPEC-007` lo portan (por ejemplo `specs/001-main-menu/tasks.md:13`) | El contrato de tarea porta el eslabón CA → T |
| AUD-023 | D3 | `CERRADO` | `docs/sdd/plantillas/informe_analitico.md:1-44` y `docs/sdd/plantillas/informe_auditoria.md:1-93` existen; `docs/sdd/PROTOCOLO_OPERATIVO.md:203-214` fija contenido y rol; `.opencode/agents/auditor.md:1-99` implementa el rol | Contrato y rol declarados |
| AUD-031 | D4 | `CERRADO` | `tools/sdd/validate.py:441-465` comprueba forma y ubicación de G1; `:499-529` verifica firma y clave autorizada; `docs/sdd/PROTOCOLO_OPERATIVO.md:136` exige la línea firmada | La comprobación de firma no se ejecuta en `--all`; ventana en AUD-037 y límite en §9 |
| AUD-032 | D4 | `CERRADO` | `tools/sdd/validate.py:569-573` eleva la cobertura a error desde G2 y desde `tasked`; `:1256-1266` aplica la severidad | La cobertura incompleta deja de ser advertencia fuera de la ventana de legado |
| AUD-033 | D4 | `CERRADO` | `tools/sdd/validate.py:576-588` y `:1336-1337` comprueban tareas abiertas en la ejecución agregada | `--all` verifica tareas abiertas |
| AUD-034 | D4 | `CERRADO` | `tools/sdd/validate.py:539-549` exige la casilla de G4 marcada y `:480-529` acredita el commit firmado | G4 exige aprobación y firma, además del dictamen |
| AUD-035 | D4 | `CERRADO` | `tools/sdd/validate.py:858-933` implementa la verificación propia de G5; `:769-852` la de G6, con tag anotado, mensaje, commit objetivo, índice y auditoría | G5 y G6 dejan de compartir la verificación de G4 |
| AUD-041 | D5 | `CERRADO` | Las cuarenta y ocho tareas de las siete specs declaran criterio (4, 10, 5, 5, 9, 5 y 10); `tools/sdd/validate.py:1057-1088` comprueba la reciprocidad | El enlace CA → T consta en las tres specs que lo omitían |
| AUD-042 | D5 | `CERRADO` | `docs/sdd/plantillas/tasks.md:19` declara el campo `Evidencia`; `tools/sdd/validate.py:1091-1115` exige veinte caracteres y rechaza marcas de pendiente | El eslabón T → evidencia tiene formato y comprobación |
| AUD-043 | D5 | `CERRADO` | `tools/sdd/validate.py:1200-1204` registra un error por commit sin `Spec:`; `:1567` la invoca en la ejecución agregada | El defecto de la cadena es error; el alcance se evalúa en AUD-046 |
| AUD-044 | D5 | `CERRADO` | Los reportes de `SPEC-001` a `SPEC-007` declaran `Merge:` y `Release:` (`specs/001-main-menu/validation_report.md:36-37` hasta `specs/007-branch-protection/validation_report.md:66-67`); `tools/sdd/validate.py:1144-1178` lo comprueba | Siete reportes con merge y tag; el registro de `SPEC-008` a `SPEC-011` se evalúa en AUD-045 |
| AUD-051 | D6 | `CERRADO` | `tools/sdd/validate.py:92-103` reproduce la tabla de transiciones; `:594-602` y `:657-659` rechazan una transición no admitida; `tools/sdd/tests/test_validate.py:985` compara la tabla con el protocolo | La tabla de §5 se comprueba |
| AUD-052 | D6 | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:126` asigna escritor a T4 a T7; `.opencode/commands/sdd-implement.md:9` y `:14` y `.opencode/commands/sdd-validate.md:12` lo reflejan | Los tres estados tienen escritor |
| AUD-053 | D6 | `CERRADO POR EXENCIÓN` | `specs/012-trazabilidad-profunda-sdd/spec.md:81-85` conserva la exención del historial anterior a la base v2; `tools/sdd/validate.py:1020-1028` la degrada a advertencia | `SPEC-002` no recibe filas de transición y la exención queda declarada |
| AUD-054 | D6 | `CERRADO` | `tools/sdd/validate.py:691-729` comprueba reciprocidad, existencia y coherencia del estado en `supersedes` y `superseded_by` | La sucesión asimétrica produce error |
| AUD-055 | D6 | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:222-238` fija cinco reglas y su procedimiento; `tools/sdd/validate.py:1118-1141` comprueba el incremento PATCH y la fila de motivo | La versión se deriva del tipo de cambio |
| AUD-061 | D7 | `CERRADO` | Los seis agentes declaran reglas de shell: `.opencode/agents/sdd.md:65-103`, `planner.md:50-73`, `coder.md:50-76`, `reviewer.md:50-85`, `documenter.md:50-55` y `auditor.md:53-88` | La capacidad de ejecución está acotada por rol |
| AUD-062 | D7 | `CERRADO` | `docs/constitution.md:74-77` y `docs/sdd/PROTOCOLO_OPERATIVO.md:262-276` fijan sección protegida, firma y prohibición de autoaprobación; `tools/sdd/validate.py:480-529` la verifica; `docs/sdd/firmantes_autorizados:4-5` registra la clave | La firma histórica no se pudo ejecutar; límite en §9 |
| AUD-063 | D7 | `CERRADO` | `.opencode/agents/auditor.md:1-99` declara el rol con lectura amplia y escritura limitada; `AGENTS.md:45`; `docs/sdd/PROTOCOLO_OPERATIVO.md:287` y `:294` | El rol existe y su alcance está declarado |
| AUD-064 | D7 | `CERRADO` | Los seis agentes cierran con la regla de precedencia; `planner.md:45-49` y `reviewer.md:44-49` declaran la denegación específica después de la concesión general | La ruta más específica prevalece y la denegación explícita también |
| AUD-071 | D8 | `PARCIAL` | `.github/workflows/sdd.yml:1-23` existe y ejecuta validador y suite; el flujo no incluye la preparación del árbol y el contrato de G6 no exige el resultado | El flujo no puede ejecutar el repositorio; causa en AUD-073 |
| AUD-072 | D8 | `CERRADO` | `docs/sdd/plantillas/tasks.md:19` y `tools/sdd/validate.py:1091-1115` condicionan el cierre a la evidencia transcrita | Una tarea cerrada sin evidencia produce error |
| AUD-081 | D9 | `CERRADO` | `compare/main...dev` devuelve 48 por delante y 0 por detrás, con base `5170539`; `main` es ancestro de `dev` | `dev` contiene el commit publicado en `main` |
| AUD-082 | D9 | `CERRADO` | La lista de ramas remotas del repositorio devuelve `dev` y `main`; `release/v0-6-0` no figura | La referencia de empaquetado se eliminó |
| AUD-083 | D9 | `CERRADO` | `CHANGELOG.md:22` registra el archivo de la rama y `docs/sdd/PROTOCOLO_OPERATIVO.md:388` lo declara; `packed-refs:3` conserva la referencia local y el remoto no la publica | La decisión de descarte está registrada |
| AUD-084 | D9 | `CERRADO` | Los dos archivos antes sin seguimiento figuran en `dev` remoto (`docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md` y `docs/sdd/plan_cierre_brechas_sdd.md`); el índice los lista en las filas 29 y 30 | El estado del árbol de trabajo en el corte no se pudo reejecutar; límite en §9 |
| AUD-091 | D10 | `CERRADO` | `MEMORY.md:40` declara `main.bat` implementado; el archivo existe en la raíz | La contradicción señalada desapareció; la vigencia de otras líneas se evalúa en AUD-095 |
| AUD-093 | D10 | `CERRADO` | `docs/sdd/README.md:39` indexa `guia_maestra_sdd.md`; la tabla cubre veinticuatro archivos de la raíz, siete plantillas y el archivo de datos | La navegación alcanza cada archivo del corpus previo al corte; este informe en AUD-096 |
| AUD-094 | D10 | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:318-334` declara comandos, comprobaciones y límite; `tools/sdd/validate.py:977-1014` imprime el alcance con las comprobaciones no verificadas | El verde declara su alcance; la lista de no verificadas se evalúa en AUD-036 |

### 5.2 Observaciones nuevas

| AUD-NNN | Dimensión | Severidad | Evidencia | Efecto observado | Destino |
|---|---|---|---|---|---|
| AUD-008 | D1 | Baja | `docs/sdd/guia_clarify_md.md:126` conserva `CB-NUEVO-01`; `docs/sdd/guia_spec_md.md:53` y `:148` conservan el criterio como «Definition of Done»; `docs/sdd/referencia_7_etapas_sdd.md:135` conserva el título anterior; `docs/sdd/compendio_sdd.md:3` declara carácter sin declarar el rango `Sin rango`; `docs/sdd/PROTOCOLO_OPERATIVO.md:44` y `:352` | La contradicción no alcanza a la norma, pero un redactor que siga la guía produce un artefacto no conforme y el encabezado de las guías no satisface la declaración de rango y carácter de §16 | Corrección editorial de las guías, delegable en `documenter` |
| AUD-015 | D2 | Baja | `.opencode/agents/sdd.md:148-155` numera la tabla desde «2 Specify» hasta «7 Validate», con seis filas y sin Release; `docs/sdd/PROTOCOLO_OPERATIVO.md:72-80` declara siete etapas con Release en la posición 7 | La tabla del orquestador no reproduce el ciclo vigente y omite la etapa que el propietario y el orquestador ejecutan | Corrección editorial de `.opencode/agents/sdd.md` |
| AUD-024 | D3 | Media | `specs/010-mecanismo-control-sdd/spec.md:372` y `specs/011-practica-operativa-sdd/spec.md:334` conservan una tercera casilla `G4` sin marcar con el marcador de plantilla; `docs/sdd/PROTOCOLO_OPERATIVO.md:168` admite dos casillas y ninguna más; `tools/sdd/validate.py:457-458` solo detecta el registro dual marcado | Dos specs validadas portan tres casillas en la sección protegida y el validador no lo detecta; una segunda marca de G4 quedaría fuera del control de duplicidad | Corrección del propietario en la sección protegida y ampliación de C-13 en una spec de base |
| AUD-036 | D4 | Media | `docs/sdd/PROTOCOLO_OPERATIVO.md:330` y `AGENTS.md:76` declaran no verificadas la firma del commit de aprobación y la pertenencia de la clave; `tools/sdd/validate.py:499-529` las verifica y `:1002` las declara ejecutadas | El contrato de rango 3 y la norma de rango 2 describen un alcance menor que el implementado, de modo que la lectura del verde depende de un documento desalineado | Spec de base que alinee §14 y `AGENTS.md` con C-03 |
| AUD-037 | D4 | Media | `tools/sdd/validate.py:90` conserva la ventana de legado de `SPEC-001` a `SPEC-009`; `:375-389` degrada a advertencia las comprobaciones C-01, C-03, C-04, C-05 y C-13 para esas specs; `:571-573` excluye la cobertura de la severidad de error | Las siete specs regularizadas y `SPEC-008` y `SPEC-009` no producen error por aprobación, cobertura ni tarea abierta; el verde agregado no acredita esas comprobaciones sobre nueve specs | Spec de base que unifique la ventana o declare la exención por escrito |
| AUD-045 | D5 | Media | Los reportes de `SPEC-008`, `SPEC-009`, `SPEC-010` y `SPEC-011` no contienen la sección `## Cierre de integración` ni las líneas `Merge:` y `Release:`; `docs/sdd/PROTOCOLO_OPERATIVO.md:310` y `docs/Flujo_de_Trabajo_Git.md:385` exigen el registro en el reporte; `tools/sdd/validate.py:1020-1028` lo degrada a advertencia en la ventana de legado | El release pendiente publicaría cinco specs y solo `SPEC-012` declara su integración en el formato exigido; el registro de G5 de `SPEC-008` a `SPEC-011` no está en el soporte declarado | Preparación del release v0.7.0 y spec de base |
| AUD-046 | D5 | Media | `tools/sdd/validate.py:1184-1191` toma como punto de corte `merge-base(HEAD, dev)`; con `HEAD` en `dev` el rango es vacío y `:1197-1199` informa la comprobación como no aplicable | La comprobación de `Spec:` no examina commit alguno en la rama de integración, de modo que el verde de `--all` sobre `dev` no acredita la cadena en los commits integrados | Spec de base que fije el rango de la comprobación sobre `dev` |
| AUD-056 | D6 | Media | `specs/012-trazabilidad-profunda-sdd/spec.md:339-341` atribuye T4, T5 y T6 a `planner`; `docs/sdd/PROTOCOLO_OPERATIVO.md:126` asigna la escritura de T4 a T7 al orquestador; `specs/012-trazabilidad-profunda-sdd/spec.md:43` declara esa escritura en el orquestador; `docs/sdd/PROTOCOLO_OPERATIVO.md:117-118` atribuye T5 a G3 y T6 a `reviewer` y G4 | El historial de una spec validada contradice la tabla de escritura de estados y su propia declaración de actores, de modo que la transición no acredita el responsable que la norma le asigna | Spec de corrección del historial de `SPEC-012` |
| AUD-065 | D7 | Media | `docs/sdd/PROTOCOLO_OPERATIVO.md:126` obliga al orquestador a escribir T4 a T7 y `:282` le niega escritura sobre documentos; `.opencode/agents/sdd.md:59-61` le concede edición sobre `specs/*/spec.md` y `:175` declara que no escribe artefactos | La matriz de permisos y el cuerpo del rol se contradicen, y la concesión alcanza la sección protegida de aprobaciones | Spec de base que separe la escritura de estado de la sección protegida |
| AUD-073 | D8 | Alta | `.github/workflows/sdd.yml:14-23` ejecuta `actions/setup-python` y después `python tools\sdd\validate.py --all` sin preparar el árbol del repositorio; `docs/Flujo_de_Trabajo_Git.md:435` deja `required_status_checks` en `null` | El flujo declarado como evidencia de verificación no dispone de los archivos que valida y su resultado no condiciona la integración; AUD-071 no se cierra | Spec de corrección del flujo y de su exigibilidad en G5 |
| AUD-074 | D8 | Baja | `docs/Flujo_de_Trabajo_Git.md:228` afirma que no existe suite automatizada para la raíz; `tools/sdd/tests` contiene 131 métodos de prueba y `.github/workflows/sdd.yml:21-23` ejecuta la suite | Una norma de rango 4 declara inexistente el mecanismo que la base v2 exige y que el repositorio contiene | Corrección de `docs/Flujo_de_Trabajo_Git.md` |
| AUD-085 | D9 | Alta | `docs/sdd/PROTOCOLO_OPERATIVO.md:304` y `docs/Flujo_de_Trabajo_Git.md:254-260` exigen la salida `0 0` de `git rev-list --left-right --count dev...main`; `compare/main...dev` devuelve 48 por delante y 0 por detrás en el commit auditado | La comprobación de sincronización no puede cumplirse cuando `dev` contiene trabajo no publicado, de modo que la condición declarada detendría el release v0.7.0 aunque `dev` no esté por detrás de `main` | Spec de corrección de la comprobación de sincronización |
| AUD-086 | D9 | Media | `docs/Flujo_de_Trabajo_Git.md:47` limita la gramática a `feat`, `fix`, `hotfix` y `release`; `AGENTS.md:66` declara las mismas ramas; la solicitud de integración número 10 se integró desde `docs/cierre-integracion-spec-012` | Una rama integrada no pertenece a la gramática vigente y el flujo no contempla el prefijo `docs/` | Corrección del flujo y de la práctica, o ampliación declarada de la gramática |
| AUD-095 | D10 | Baja | `MEMORY.md:13` declara `SPEC-011` en curso; `specs/INDEX.md:17-18` y el frontmatter de `specs/011-practica-operativa-sdd/spec.md:4` la declaran validada, igual que `SPEC-012` | El contexto operativo contradice el estado vigente de dos specs | Corrección editorial de `MEMORY.md` |
| AUD-096 | D10 | Baja | `docs/sdd/README.md:67` declara defecto de conformidad un archivo sin fila; la tabla de inventario de `:28-61` no contiene este informe | El corpus queda con un archivo sin fila hasta que el propietario o `documenter` lo registre; el rol de auditoría no puede editar el índice | Registro de la fila por el propietario o `documenter` |
| AUD-097 | D10 | Baja | `CHANGELOG.md:191-193` limita el historial de releases a `v0.1.0`; `packed-refs:7-22` registra ocho tags anotados de `v0.1.0` a `v0.6.0` | La sección de historial de releases no refleja las versiones publicadas | Corrección editorial de `CHANGELOG.md` |

### 5.3 Recuento

| Clase | Recuento |
|---|---|
| Hallazgos de origen cerrados con evidencia | 36 |
| Hallazgos de origen cerrados por exención registrada | 4 |
| Hallazgos de origen parciales | 1 |
| Hallazgos de origen vigentes | 0 |
| Total de hallazgos de origen | 41 |
| Observaciones nuevas | 16 |
| Observaciones nuevas de severidad Alta | 2 |
| Observaciones nuevas de severidad Media | 8 |
| Observaciones nuevas de severidad Baja | 6 |

Los cuarenta y un hallazgos de origen se distribuyen así: `CERRADO` en AUD-001, AUD-002, AUD-006, AUD-007, AUD-011, AUD-012, AUD-013, AUD-014, AUD-021, AUD-022, AUD-023, AUD-031, AUD-032, AUD-033, AUD-034, AUD-035, AUD-041, AUD-042, AUD-043, AUD-044, AUD-051, AUD-052, AUD-054, AUD-055, AUD-061, AUD-062, AUD-063, AUD-064, AUD-072, AUD-081, AUD-082, AUD-083, AUD-084, AUD-091, AUD-093 y AUD-094; `CERRADO POR EXENCIÓN` en AUD-003, AUD-004, AUD-005 y AUD-053; `PARCIAL` en AUD-071; ningún hallazgo queda `VIGENTE`.

### 5.4 Comprobaciones específicas del encargo

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Ventana de legado de la trazabilidad limitada a `SPEC-008` a `SPEC-011` | Cumple en las comprobaciones C-14 a C-18 | `tools/sdd/validate.py:149-153` acota `TRACE_LEGACY_SPECS` y `TRACE_LEGACY_WINDOW` a ese conjunto; `:1020-1028` aplica la degradación con esa ventana |
| Ventana de legado de las comprobaciones C-01 a C-13 | No está limitada a `SPEC-008` a `SPEC-011` | `tools/sdd/validate.py:90` conserva `SPEC-001` a `SPEC-009`; efecto en AUD-037 |
| Cuarenta y ocho tareas regularizadas | Cumple | `specs/001-main-menu/tasks.md` 4, `002` 10, `003` 5, `004` 5, `005` 9, `006` 5 y `007` 10, con `Criterio de aceptación` y `Evidencia`; suma 48 |
| Siete reportes con merge y tag | Cumple en `SPEC-001` a `SPEC-007` | `Merge:` y `Release:` en los siete reportes, de `specs/001-main-menu/validation_report.md:36-37` a `specs/007-branch-protection/validation_report.md:66-67`; los cuatro reportes restantes en AUD-045 |
| Referencia `Spec:` como error | Cumple con alcance acotado | `tools/sdd/validate.py:1200-1204` emite error; el rango de la comprobación se evalúa en AUD-046 |
| Registro único de G1 y G4 en `spec.md` | Cumple con una desviación | `docs/constitution.md:74`, `docs/sdd/PROTOCOLO_OPERATIVO.md:264` y `tools/sdd/validate.py:1424-1428`; la tercera casilla de `SPEC-010` y `SPEC-011` en AUD-024 |
| Registro único de G6 en `CHANGELOG.md` | Cumple | `docs/constitution.md:74`; `docs/sdd/PROTOCOLO_OPERATIVO.md:264`; `tools/sdd/validate.py:552-563` y `:790-795` rechazan G6 en `spec.md` y G1 o G4 en el release |
| Firmas de `cfb576b`, `6fade8e` y las anteriores | `NO VERIFICABLE` en esta ejecución | Los dos commits existen con los asuntos «docs(sdd): aprobar G1 de SPEC-012» y «docs(sdd): aprobar G4 de SPEC-012», y cada uno modifica una única línea de la sección de aprobaciones de `specs/012-trazabilidad-profunda-sdd/spec.md:316-317` (1 inserción y 1 eliminación); la verificación de firma exige `git verify-commit`, denegado en este entorno (§9) |
| Coherencia de `specs/INDEX.md` con los estados reales | Cumple | `specs/INDEX.md:7-13` declara `released` con release para `SPEC-001` a `SPEC-007`; `:14-18` declara `validated` sin release para `SPEC-008` a `SPEC-012`; el frontmatter de cada `spec.md` coincide en estado, rama y release |
| Release v0.7.0 | Pendiente declarado | `packed-refs:7-22` registra ocho tags hasta `v0.6.0`; `CHANGELOG.md:24-26` declara el registro de G6 del release en curso pendiente de la línea firmada; la ausencia no se registra como hallazgo |

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría.

| Compuerta | Evidencia observada | Límite de esta auditoría |
|---|---|---|
| G1 | Línea marcada en la sección de aprobaciones de las doce specs, con la cadena exacta en `SPEC-008` a `SPEC-012`; `tools/sdd/validate.py:441-465` | La firma del commit no se pudo verificar en esta ejecución; la aprobación corresponde al propietario |
| G2 | `tasked` con cobertura completa en las specs posteriores a la base v2; verificación impresa por el validador | No ejecutada en este entorno |
| G3 | 48 tareas cerradas en las siete specs publicadas y tareas cerradas en `SPEC-008` a `SPEC-012` | Verificación automática no ejecutada en este entorno |
| G4 | Línea marcada en `spec.md` de las doce specs y reporte con dictamen `CONVERGIDO` | Firma y declarante no verificables aquí; la aprobación corresponde al propietario |
| G5 | Fusiones con dos padres en `dev`: `753c3e5`, `ec6a063`, `39b27a2`, `b38ed6c`, `2781db5`, `0afc2ee`, `502c69d` (`docs/sdd/auditoria_cumplimiento_sdd.md:1029-1037`) y `b87e32c` (`specs/012-trazabilidad-profunda-sdd/validation_report.md:85`); la secuencia de integración de las solicitudes 4 a 10 consta en `.git/logs/HEAD:121-185` | El registro de G5 de `SPEC-008` a `SPEC-011` no consta en el soporte exigido (AUD-045) |
| G6 | Ocho tags anotados, con mensaje `Release vX.Y.Z` y commit objetivo en `main`; entrada de release con la línea de aprobación en `CHANGELOG.md` | El release v0.7.0 no existe y su G6 no está declarada; la auditoría no la declara |

## 7. Veredicto global

**Regla aplicada.** Existe al menos una dimensión `NO CONFORME` con una observación de severidad Alta: D8 por AUD-073 y D9 por AUD-085.

| Dimensión | Veredicto | Observación que lo sostiene |
|---|---|---|
| D1 | `CONFORME CON OBSERVACIONES` | AUD-008 |
| D2 | `CONFORME CON OBSERVACIONES` | AUD-015 |
| D3 | `CONFORME CON OBSERVACIONES` | AUD-024 |
| D4 | `CONFORME CON OBSERVACIONES` | AUD-036, AUD-037 |
| D5 | `CONFORME CON OBSERVACIONES` | AUD-045, AUD-046 |
| D6 | `CONFORME CON OBSERVACIONES` | AUD-056 |
| D7 | `CONFORME CON OBSERVACIONES` | AUD-065 |
| D8 | `NO CONFORME` | AUD-073, AUD-074 y AUD-071 `PARCIAL` |
| D9 | `NO CONFORME` | AUD-085, AUD-086 |
| D10 | `CONFORME CON OBSERVACIONES` | AUD-095, AUD-096, AUD-097 |

**Veredicto global:** `NO CONFORME`.

**Recuento de hallazgos vigentes:** 0 de 41. **Recuento de hallazgos parciales:** 1 de 41 (AUD-071). **Observaciones nuevas:** 16, de las cuales 2 son de severidad Alta, 8 de severidad Media y 6 de severidad Baja.

La hoja de ruta B1 a B4 cierra treinta y seis hallazgos con evidencia y cuatro por exención registrada. La conformidad del régimen v2 no se alcanza por dos defectos instrumentales: el flujo de integración continua no puede ejecutar el repositorio que declara verificar (AUD-073) y la comprobación de sincronización de release exige una salida imposible de obtener (AUD-085). Ambos afectan al release v0.7.0 y a la evidencia de sus compuertas, y ninguno se resuelve por la ausencia de hallazgos del validador.

**Declaración expresa.** Este informe no aprueba compuerta alguna, no declara G1, G2, G3, G4, G5 ni G6, y no sustituye la firma del propietario ni su verificación. Registra el resultado de una reauditoría de conformidad y se limita a la evidencia citada. Un resultado favorable de la suite o del validador no acredita la conformidad del régimen ni la autorización de un release.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| Añadir la preparación del árbol al flujo de integración continua y exigir su resultado antes de G5 | AUD-073 | corrección | Spec de la práctica de integración |
| Corregir la comprobación de sincronización de release para exigir que `dev` no esté por detrás de `main` | AUD-085 | corrección | Spec de base sobre §13 y rango 4 |
| Alinear §14 del protocolo y `AGENTS.md` con la verificación de firma de C-03 | AUD-036 | spec de base | Ninguna |
| Unificar la ventana de legado de C-01 a C-13 o declarar por escrito la exención de `SPEC-001` a `SPEC-009` | AUD-037 | spec de base | AUD-036 |
| Retirar la tercera casilla de G4 de `SPEC-010` y `SPEC-011` y ampliar C-13 a la casilla duplicada no marcada | AUD-024 | corrección | Spec de base y commit firmado del propietario |
| Registrar la integración de `SPEC-008` a `SPEC-011` en su reporte antes del release v0.7.0 | AUD-045 | release | Decisión del propietario |
| Corregir la atribución de responsable de T4 a T6 en el historial de `SPEC-012` | AUD-056 | corrección | Spec de corrección |
| Separar en la matriz de permisos la escritura de estado de la sección protegida de aprobaciones | AUD-065 | spec de base | Ninguna |
| Ampliar el rango de la comprobación `Spec:` para cubrir los commits integrados en `dev` | AUD-046 | spec de base | Ninguna |
| Corregir la tabla de etapas de `.opencode/agents/sdd.md` y su referencia a Release | AUD-015 | editorial | Ninguna |
| Alinear las guías con la plantilla y declarar su rango en el encabezado | AUD-008 | editorial | Ninguna |
| Corregir la afirmación sobre la suite en `docs/Flujo_de_Trabajo_Git.md` | AUD-074 | editorial | Ninguna |
| Corregir el estado de las specs en `MEMORY.md` | AUD-095 | editorial | Ninguna |
| Registrar este informe en la tabla de inventario de `docs/sdd/README.md` | AUD-096 | editorial | Escritura del propietario o de `documenter` |
| Actualizar el historial de releases de `CHANGELOG.md` | AUD-097 | editorial | Ninguna |
| Decidir la admisión del prefijo `docs/` en la gramática de ramas o corregir la práctica | AUD-086 | corrección | Spec de base sobre el rango 4 |

## 9. Limitaciones

| Elemento | Causa | Artefacto o comprobación que faltaría |
|---|---|---|
| Ejecución del validador | El entorno de ejecución denegó la herramienta de shell, de modo que `python tools\sdd\validate.py --all` no se ejecutó en esta auditoría | Salida literal del validador con su código de salida sobre `5efac03` |
| Ejecución de la suite | Misma causa; el recuento de 131 métodos se obtuvo por lectura de `tools/sdd/tests` y no por ejecución | Salida literal de `python -m unittest discover -s tools\sdd\tests -q` |
| Verificación de firmas de aprobación | La comprobación exige `git verify-commit` y `ssh-keygen -lf`, denegados en este entorno | Resultado de C-03 para los commits de G1 y G4 de las doce specs y huella contrastada con `docs/sdd/firmantes_autorizados` |
| Estado del árbol de trabajo | `git status --short` no se pudo ejecutar | Listado del árbol en el commit auditado |
| Protección remota de ramas | La configuración remota no forma parte del repositorio y esta auditoría no consultó su API de reglas | Evidencia de la configuración de protección de `main` y `dev` |
| Contenido de `.env` | Fuera del alcance declarado | Procedimiento de gestión de secretos verificable |

Ningún elemento de esta lista se presume cumplido. La falta de la salida del validador y de la verificación de firmas impide acreditar por ejecución lo que los artefactos declaran, y esa ausencia no se sustituye por una suposición.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | Ocho tags anotados con su objeto y su commit pelado, de `v0.1.0` a `v0.6.0`; ramas locales `dev` y `feat/gemma-4-26b-a4b-it-qat-gguf`; ramas remotas `dev` y `main` | `.git/packed-refs:2-22` |
| B | Secuencia de integración: fusiones con dos padres, sincronizaciones y commits de aprobación, hasta `5efac03` | `.git/logs/HEAD:56` a `:185` |
| C | Divergencia entre ramas: 48 commits por delante y 0 por detrás, base `5170539` | `https://api.github.com/repos/sebaxtian/LLaMA/compare/main...dev` |
| D | Solicitudes de integración 1 a 10, con rama de origen y destino | API de GitHub, `list_pull_requests` sobre `sebaxtian/LLaMA` |
| E | Recuento de 131 métodos de prueba y nombres de las clases de la trazabilidad | `tools/sdd/tests/test_validate.py` y `tools/sdd/tests/test_agent_permissions.py` |
| F | Contrato de la auditoría de conformidad previa al release menor | `docs/constitution.md:85-86`; `docs/sdd/PROTOCOLO_OPERATIVO.md:354-356`; `docs/sdd/plantillas/informe_auditoria.md:1-93` |
