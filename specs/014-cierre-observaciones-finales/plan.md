# Plan técnico — SPEC-014

*Artefacto de rango 6: diseño de las cinco correcciones de `SPEC-014`, con las decisiones `DEC-NNN`, los contratos de cada corrección, la estrategia de testing y la matriz de cobertura de la spec.*

## Referencias

- `spec.md`: `SPEC-014`, versión 0.2.0, estado `clarified`, con 5 requisitos funcionales, 5 requisitos no funcionales, 7 casos borde y 7 criterios de aceptación; G1 firmada por `Agent Sebaxtian` (2026-11-14).
- `clarify.md`: `SPEC-014`, cerrado con `AMB-001` a `AMB-006` resueltos, los casos borde `CB-006` y `CB-007` añadidos y los valores de la preparación del árbol y de la matriz del orquestador fijados.
- `docs/sdd/auditoria_final_v0_7_0.md`: veredicto global `CONFORME CON OBSERVACIONES`, equivalente a `PARCIAL` en la escala de la plantilla de auditoría, y observaciones abiertas `AUD-066` (Media, D7), `AUD-075` (Media, D8), `AUD-101` (Media, D11) y `AUD-102` (Baja, D11).
- `docs/sdd/auditoria_cierre_v0_7_0.md`: las 16 observaciones previas, 15 cerradas con artefacto y 1 por exención declarada.
- `docs/constitution.md`: rangos de los documentos, prohibición de modificar requisitos para ajustarlos al código y registro de G6 fuera de esta spec.
- `AGENTS.md`: cadena `RF/CB → CA → T → evidencia`, seis roles, matriz del orquestador y prohibición de declarar compuertas.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §5 escritura de estados, §12 roles y permisos del orquestador, §13 registros posteriores a G4 y §14 contrato del validador.
- `docs/Flujo_de_Trabajo_Git.md`: norma de rango 4, con la declaración de la suite en la línea 232 y la del check exigible en la línea 462.
- `docs/sdd/plantillas/plan.md` y `docs/sdd/plantillas/tasks.md`: forma de este artefacto y del de tareas.
- Estado observado del repositorio en el commit `3648341`:
  - `.github/workflows/sdd.yml` declara el job `verify` con `timeout-minutes: 5`, `actions/checkout@v4` sin `fetch-depth` ni `fetch-tags`, dos pasos de ejecución y un solo paso de suite, el de `tools\sdd\tests`.
  - `.opencode/agents/sdd.md` conserva `edit` con efecto `allow` sobre `.opencode/**`, `.github/**`, `opencode.jsonc` y `MEMORY.md` en las líneas 44 a 55, y `specs/**` con efecto `deny` en la línea 57.
  - `opencode.jsonc` no declara matriz de roles: su bloque `permissions` contiene 7 entradas globales, ninguna del orquestador.
  - `tools/sdd/tests/test_agent_permissions.py` declara `problemas_del_flujo` con la exigencia de 2 pasos de ejecución y el fixture `FLUJO_VALIDO` sin parámetros de preparación del árbol; `tools/sdd/tests/test_validate.py` y `tools/git/tests/` completan las 2 suites.
  - `tools/git/tests/` reúne 48 casos de prueba repartidos entre `test_verify_branch_protection.py` y `test_remote_rejection.py`, que ningún job ejecuta en el corte auditado.
  - `specs/013-cierre-reauditoria-conformidad/validation_report.md` declara la matriz de 40 filas en `PASADO`, el dictamen `CONVERGIDO` y la nota 5 de la sección de desviaciones, que difiere la evidencia de `RNF-001` y de `CA-015`.

## Naturaleza del entregable

La spec produce una combinación declarada de configuración, normativa, definición de rol, registro de spec y pruebas:

- Configuración de rango 7: `.github/workflows/sdd.yml`, con la preparación del árbol y el paso de la segunda suite.
- Definición de rol de rango 7: `.opencode/agents/sdd.md`, con la matriz reducida a `.opencode/**`.
- Norma de rango 4: `docs/Flujo_de_Trabajo_Git.md`, con la preparación completa y las 2 suites del check `verify`.
- Registro de spec de rango 6: la nota de cierre append-only del reporte de `SPEC-013`.
- Pruebas de rango 7: las comprobaciones positivas y negativas de `tools/sdd/tests/` sobre el flujo, la matriz y la nota.
- El contrato de esta spec en `specs/014-cierre-observaciones-finales/`.

No produce scripts `.bat`, no modifica `src/`, `tools/` fuera de las pruebas declaradas, `llama.cpp/`, `models/` ni `bin/`, no altera la matriz ni el dictamen de `SPEC-013` y no cambia su estado `validated`. No declara compuerta alguna: G1 y G4 corresponden al propietario y la verificación de G2, G3 y G5 al orquestador.

## Arquitectura

### Componentes, responsabilidad y límite

| Componente | Artefacto | Responsabilidad | Límite | Rol que escribe |
|---|---|---|---|---|
| Preparación del árbol | `.github/workflows/sdd.yml` | Declara la profundidad completa del historial y la descarga de etiquetas en `actions/checkout` | No publica, no etiqueta y no usa secretos | `coder` |
| Alcance del job | `.github/workflows/sdd.yml` | Ejecuta las 2 suites como pasos nombrados, con límite propio por suite y límite total del job | No ejecuta una suite fuera del job ni añade un tercer mecanismo de prueba | `coder` |
| Matriz del orquestador | `.opencode/agents/sdd.md` | Reduce la escritura del orquestador a `.opencode/**` y deniega `.github/**`, `opencode.jsonc` y `MEMORY.md` | Ruta sin rol concesionario para los agentes: la escribe el propietario | propietario |
| Norma de integración | `docs/Flujo_de_Trabajo_Git.md` | Declara la preparación completa y las 2 suites del check `verify` | No fija reglas del ciclo SDD ni de las compuertas | `documenter` |
| Nota de cierre | `specs/013-cierre-reauditoria-conformidad/validation_report.md` | Transcribe el veredicto del informe final y el estado de las 4 observaciones | Append-only: no altera matriz, dictamen ni estado | `reviewer`, por delegación escrita del propietario |
| Suite del mecanismo | `tools/sdd/tests/test_agent_permissions.py` | Ejerce la estructura del flujo, la matriz del orquestador y la nota de cierre con pareja positiva y negativa | Solo lee texto; no escribe archivos versionados ni consulta el remoto | `coder` |
| Contrato de la feature | `specs/014-cierre-observaciones-finales/` | Declara requisitos, decisiones, tareas y evidencia | No reescribe requisitos de `SPEC-013` ni declara compuertas | `planner` |

### Orden de las correcciones

Las correcciones se ejecutan en un orden que evita que una comprobación corregida declare en rojo un artefacto aún sin corregir:

1. Pruebas en rojo de la preparación del árbol, del alcance del job, de la matriz y de la nota de cierre.
2. Preparación completa del árbol y paso de la segunda suite en el flujo, con las pruebas del flujo en verde.
3. Matriz del orquestador reducida a `.opencode/**`, con la prueba de la matriz en verde.
4. Declaración documental del alcance del job en la norma de rango 4.
5. Nota de cierre append-only en el reporte de `SPEC-013`, con la prueba de la nota en verde.
6. Paquete de cierre de las 4 observaciones, regresión agregada de las 2 suites y contraste de conservación de `SPEC-013`.

La matriz se corrige después de la prueba y antes de la nota porque `CB-004` atribuye el artefacto al rol que `tasks.md` declara, y la nota se escribe al final porque transcribe el estado de las 4 observaciones, que depende de los artefactos anteriores.

### Procedimiento de trabajo

- Las pruebas se escriben en rojo antes de la corrección que las satisface y declaran su pareja positiva y su pareja negativa, según `RNF-003`.
- El flujo y la matriz siguen TDD: prueba negativa sobre el texto sintético, comprobación en rojo, corrección mínima y comprobación en verde.
- Los documentos y la nota de cierre siguen validación-first: se transcribe la afirmación vigente, se contrasta el valor nuevo con el informe final y solo después se escribe.
- Cada ejecución de prueba o de validador se transcribe en el campo `Evidencia` de su tarea al cerrarla; ninguna tarea declara un resultado supuesto.

## Contratos

### C-1. Preparación del árbol

| Elemento | Valor exigido | Regla |
|---|---|---|
| Acción de preparación | `actions/checkout@v4` como primera de los pasos | Sin preparación no existen los archivos que el job valida |
| Profundidad del historial | `fetch-depth: 0` | Historial completo: una profundidad distinta deja el alcance de `C-16` sin commits que examinar |
| Descarga de etiquetas | `fetch-tags: true` | Sin etiquetas, `annotated_release_tags()` no devuelve tag y el alcance se informa como no aplicable |
| Alcance de la comprobación de la referencia | Último tag anotado de release o, en su defecto, los commits posteriores al ancestro común con `main` | Con el rango no vacío examina al menos 1 commit de implementación |
| Profundidad superficial | Prohibida | Sustituye la verificación por una declaración de no aplicable |
| Efectos remotos | 0 | Sin `push`, `tag`, `fetch`, `release` ni despliegue |

### C-2. Alcance del job `verify`

| Paso | Nombre declarado | Ejecución | Límite |
|---|---|---|---|
| 1 | Prepara el árbol del repositorio | `actions/checkout@v4` con `fetch-depth: 0` y `fetch-tags: true` | Sin límite propio |
| 2 | Prepara Python 3.12 | `actions/setup-python@v5` con `python-version: '3.12'` | Sin límite propio |
| 3 | Validación agregada del corpus | `python tools\sdd\validate.py --all` | Sin límite propio |
| 4 | Suite del mecanismo de control | `python -m unittest discover -s tools\sdd\tests -q` | `timeout-minutes: 1` |
| 5 | Suite de la protección de ramas | `python -m unittest discover -s tools\git\tests -q` | `timeout-minutes: 1` |
| Job | `verify` | Los 5 pasos anteriores sobre `windows-latest` | `timeout-minutes: 5` |

El disparador se conserva en `pull_request` sobre `dev` y `main`, los permisos en `contents: read` y el número de efectos remotos en 0. Un fallo de cualquiera de las 2 suites deja el check `verify` en rojo y bloquea G5. Ninguna de las 2 suites queda fuera del job.

### C-3. Matriz del orquestador

| Ruta | Efecto exigido | Rol concesionario tras la corrección |
|---|---|---|
| `.opencode/**` | `allow` de `edit` | orquestador |
| `.github/**` | `deny` de `edit` | `coder` |
| `opencode.jsonc` | `deny` de `edit` | propietario, por ser ruta sin rol concesionario |
| `MEMORY.md` | `deny` de `edit` | `documenter` |
| `specs/**`, `src/**`, `tests/**`, `tools/**`, `docs/**`, `AGENTS.md`, `CHANGELOG.md`, `llama.cpp/**`, `bin/**`, `models/**` y `.env` | `deny` de `edit` | 0 atribuciones |

- El número de rutas con efecto `allow` de escritura del orquestador es 1 y corresponde a `.opencode/**`.
- El número de atribuciones de escritura del orquestador sobre documentos, código y configuración fuera de `.opencode/**` es 0.
- El número de contradicciones entre esta matriz y §12 del protocolo sobre las rutas de escritura es 0, y el protocolo no se edita.
- Una escritura intentada fuera de `.opencode/**` queda denegada y el artefacto queda atribuido al rol declarado en `tasks.md`.

### C-4. Nota de cierre del reporte de `SPEC-013`

| Elemento | Forma | Obligatoriedad |
|---|---|---|
| Ubicación | A continuación de la sección de cierre del reporte | Obligatoria |
| Encabezado | Título de tercer nivel con la referencia a `SPEC-014` | Obligatorio |
| Veredicto transcrito | `CONFORME CON OBSERVACIONES`, con su equivalencia a `PARCIAL` | Obligatorio |
| Cierre previo | Las 16 observaciones de la reauditoría previa: 15 con artefacto y 1 por exención declarada | Obligatorio |
| Causa del veredicto | Las 7 observaciones nuevas del informe final, no las 16 previas | Obligatorio |
| Estado de las 4 observaciones | `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` con su artefacto de cierre | Obligatorio |
| Matriz y dictamen | Sin alteración: 40 filas en `PASADO` y dictamen `CONVERGIDO` | Prohibida la modificación |
| Estado de `SPEC-013` | `validated`, sin cambio | Prohibida la modificación |
| Nota precedente | Se conserva y la nota nueva se añade a continuación | Obligatorio |
| Recuento transcrito distinto del del informe final | Error con el valor en conflicto y la nota no se declara conforme | Error |

### C-5. Cierre por observación

| Observación | Severidad | Artefacto que la cierra | Evidencia de la verificación | Requisito |
|---|---|---|---|---|
| `AUD-101` | Media | Preparación del árbol con `fetch-depth: 0` y `fetch-tags: true` en `.github/workflows/sdd.yml` | Alcance de `C-16` con al menos 1 commit examinado y salida del job con el punto de corte informado | `RF-001` |
| `AUD-102` | Baja | Paso nombrado de `tools/git/tests` en el job `verify` y declaración en `docs/Flujo_de_Trabajo_Git.md` | Ejecución de las 48 pruebas de la suite en el job y ausencia de suites fuera del job | `RF-002` |
| `AUD-066` | Media | Matriz del orquestador con `.opencode/**` como única concesión de escritura | 0 atribuciones fuera de `.opencode/**` y 0 contradicciones con §12 | `RF-003` |
| `AUD-075` | Media | Nota de cierre append-only en el reporte de `SPEC-013` | Nota transcrita sin alteración de matriz, dictamen ni estado | `RF-004` |

Una observación sin artefacto de cierre no se declara cerrada: se registra en estado vigente con su causa y la reauditoría posterior conserva el hallazgo. El informe final declara 4 de 4 cerradas.

### C-6. Pareja de pruebas por comprobación

| Comprobación | Prueba positiva | Prueba negativa |
|---|---|---|
| Preparación completa del árbol | `test_preparacion_completa_del_arbol` | `test_flujo_sin_etiquetas_es_error` |
| Alcance de la referencia a la spec | `test_alcance_de_la_referencia_examina_commit` | `test_alcance_sin_tag_usa_merge_base` |
| Alcance del job con 2 suites | `test_job_ejecuta_las_dos_suites` | `test_flujo_con_una_suite_es_error` |
| Matriz del orquestador | `test_escritura_unica_del_orquestador` | `test_concesion_fuera_de_opencode_es_error` |
| Nota de cierre | `test_nota_de_cierre_append_only` | `test_nota_con_recuento_divergente_es_error` |
| Cierre de las 4 observaciones | `test_cierre_de_las_cuatro_observaciones` | `test_observacion_sin_artefacto_sigue_vigente` |

Cada comprobación declara al menos 1 prueba positiva y 1 prueba negativa en la suite del mecanismo de control, y la prueba negativa demuestra que el detector discrimina sobre texto o fixture sintético.

## Decisiones técnicas

### DEC-001

- **Decisión:** el job `verify` prepara el árbol con `actions/checkout@v4` y declara `fetch-depth: 0` y `fetch-tags: true`. Con esa preparación la comprobación de la referencia a la spec acota el alcance al último tag anotado de release o, en su defecto, a los commits posteriores al ancestro común con `main`, y examina al menos 1 commit de implementación cuando el rango no está vacío.
- **Justificación:** `RF-001`, `CB-001`, `CB-002`, `CA-001` y `AUD-101` fijan la profundidad, las etiquetas y el alcance. La copia superficial y sin etiquetas deja `annotated_release_tags()` sin tag, `scope_point()` sin punto de corte y la comprobación `C-16` informada como no aplicable, de modo que el check acredita la verificación sin examinar commit alguno y el defecto reaparece con cualquier redacción que conserve la preparación superficial.
- **Alternativas descartadas:** conservar la preparación predeterminada y declarar el alcance como no aplicable, porque sustituye la verificación por una declaración de ausencia y `CA-001` exige al menos 1 commit examinado; usar una profundidad acotada distinta de 0, porque el punto de corte por tag queda fuera del historial recortado y el alcance depende del número de commits descargados; descargar las etiquetas en un paso posterior con `git fetch --tags`, porque añade un efecto remoto al job y `C-2` fija 0 efectos remotos.

### DEC-002

- **Decisión:** el job `verify` ejecuta las 2 suites del repositorio como pasos nombrados: la suite de `tools/sdd/tests` con el nombre actual y una suite nueva de `tools/git/tests`, cada una con `timeout-minutes: 1`, dentro del límite total de 5 minutos del job. `docs/Flujo_de_Trabajo_Git.md` declara que el check `verify` ejecuta las 2 suites.
- **Justificación:** `RF-002`, `CB-003`, `CA-002`, `RNF-002` y `AUD-102` fijan el alcance del check y su declaración normativa. Las 48 pruebas de `tools/git/tests` cubren el rechazo de push directo y de fuerza sobre las ramas protegidas y hoy no las ejecuta job alguno, de modo que su resultado no condiciona la integración mientras la norma de rango 4 describe el check con el alcance de una sola suite.
- **Alternativas descartadas:** ampliar la suite de `tools/sdd/tests` para que descubra también `tools/git/tests`, porque mezcla 2 mecanismos con rutas y dependencias distintas y oculta cuál falla; declarar la cobertura ausente y limitar el check a la suite existente, porque `CA-002` exige que ninguna de las 2 suites quede fuera del job; añadir el descubrimiento de las 2 suites en un paso único, porque el fallo no queda atribuido a una suite y `CA-002` exige pasos nombrados.

### DEC-003

- **Decisión:** la matriz del orquestador en `.opencode/agents/sdd.md` se reduce a `.opencode/**` como única concesión de escritura. Las entradas `edit` con efecto `allow` sobre `.github/**`, `opencode.jsonc` y `MEMORY.md` se retiran y esas 3 rutas quedan con efecto `deny` explícito. §12 del protocolo y `AGENTS.md` no se editan.
- **Justificación:** `RF-003`, `CB-004`, `CA-003`, `RNF-005` y `AUD-066` fijan la ruta única y la ausencia de contradicción. §12 niega al orquestador la escritura sobre documentos y código y atribuye `.github/` al `coder` y `MEMORY.md` al `documenter`, mientras la matriz le concede las 3 rutas y `opencode.jsonc`, de modo que la contradicción está declarada y no resuelta. La ruta no declarada está denegada, y `opencode.jsonc` no tiene rol concesionario: queda en el propietario.
- **Alternativas descartadas:** ampliar §12 para admitir las 3 concesiones, porque eleva el privilegio del orquestador en lugar de reducirlo y contradice el menor privilegio de la base v2; retirar también la concesión sobre `.opencode/**`, porque es la ruta declarada del rol y su retirada dejaría el orquestador sin escritura sobre su propia definición; conservar las concesiones y confiar en la prohibición del cuerpo del rol, porque la concesión efectiva prevalece sobre la prosa y `CA-003` cuenta 0 atribuciones fuera de `.opencode/**`.

### DEC-004

- **Decisión:** el reporte de `SPEC-013` recibe una nota de cierre append-only, escrita por el `reviewer` por delegación escrita del propietario, que transcribe el veredicto `CONFORME CON OBSERVACIONES` con su equivalencia a `PARCIAL`, el cierre de las 16 observaciones previas con sus 15 artefactos y su exención declarada, la causa del veredicto —las 7 observaciones nuevas— y el estado de las 4 observaciones de esta spec. La matriz de 40 filas, el dictamen `CONVERGIDO` y el estado `validated` no se alteran y no se reabre requisito alguno.
- **Justificación:** `RF-004`, `CB-005`, `CB-006`, `CA-004`, `RNF-004` y `AUD-075` fijan la nota y la conservación del documento. La fila de `RNF-001` y la de `CA-015` figuran en `PASADO` con la evidencia diferida a un informe que no confirma el veredicto anticipado, y §13 del protocolo admite registros posteriores a G4 en modalidad append-only, de modo que la evidencia queda transcrita y contrastable sin reescribir el criterio publicado.
- **Alternativas descartadas:** corregir la fila de `RNF-001` y la de `CA-015` a un valor distinto de `PASADO`, porque altera la matriz publicada y `RNF-004` exige su conservación íntegra; reabrir `SPEC-013` para declarar el cambio como nuevo requisito, porque `RNF-004` prohíbe modificar requisitos y criterios y la reapertura devolvería la spec a `draft`; atribuir la nota al `planner`, porque su matriz deniega de forma explícita `specs/*/validation_report.md` y la atribución sería inejecutable.

### DEC-005

- **Decisión:** cada comprobación nueva se implementa con pareja positiva y negativa en `tools/sdd/tests/test_agent_permissions.py`, con fixtures sintéticos para el flujo y textos sintéticos para la matriz y la nota. La prueba positiva se ejecuta sobre el artefacto del repositorio y la negativa sobre una copia que conserva el defecto, y la negativa declara el valor en conflicto o la etiqueta ausente.
- **Justificación:** `RNF-003` y `CA-006` excluyen acreditar una comprobación por su sola presencia en el artefacto. Una prueba que únicamente lee el artefacto real no demuestra que el detector discrimine, y las 6 comprobaciones de `C-6` corrigen defectos que hoy pasan inadvertidos: preparación superficial, suite fuera del job, concesión fuera de `.opencode/**`, nota con recuento divergente y observación declarada cerrada sin artefacto.
- **Alternativas descartadas:** una sola prueba por comprobación sobre el artefacto real, porque no distingue una comprobación correcta de una que acepta cualquier entrada y `RNF-003` exige la pareja; pruebas que consulten el servicio remoto de integración continua, porque introducen red y credencial en la suite y la base prohíbe depender de servicios externos; pruebas que escriban archivos versionados, porque la suite se declara no destructiva y el fixture sintético basta para ejercer la discriminación.

### DEC-006

- **Decisión:** el cierre de cada una de las 4 observaciones exige 2 elementos: el artefacto que elimina la causa y la evidencia transcrita de su verificación. El paquete de cierre de `tasks.md` declara 4 de 4 cerradas con esa pareja por observación, y una observación sin artefacto se registra en estado vigente con su causa en lugar de declararse cerrada.
- **Justificación:** `RF-005`, `CB-007`, `CA-005` y `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` fijan el cierre con evidencia y la observación sin artefacto. La declaración de cierre de un informe de auditoría no absorbe un hallazgo cuya causa permanece, y la reauditoría posterior contrasta el artefacto, de modo que la declaración sin evidencia reabriría el mismo hallazgo con otra redacción.
- **Alternativas descartadas:** declarar el cierre por la intención de corregir, porque `CA-005` exige artefacto y evidencia transcrita y la intención no es contrastable; cerrar las 4 observaciones en la nota de `SPEC-013`, porque la nota registra el estado y no sustituye el artefacto de cada corrección; ampliar el cierre a las 7 observaciones del informe final, porque `AUD-038`, `AUD-067` y `AUD-098` quedaron cerradas en el Pull Request #13 y esta spec declara 4 de 4 sobre las restantes.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Preparación del árbol | `test_preparacion_completa_del_arbol` y `test_flujo_sin_etiquetas_es_error` | La preparación declara `fetch-depth: 0` y `fetch-tags: true`; la omisión de las etiquetas produce un error que nombra la etiqueta ausente y no declara verificado el alcance |
| Alcance de la referencia | `test_alcance_de_la_referencia_examina_commit` y `test_alcance_sin_tag_usa_merge_base` | El alcance enumera al menos 1 commit de implementación con el rango no vacío; sin tag anotado se acota por el ancestro común con `main` sin informar un defecto del repositorio |
| Alcance del job | `test_job_ejecuta_las_dos_suites` y `test_flujo_con_una_suite_es_error` | El job declara 2 pasos de suite nombrados con su límite de 1 minuto; un flujo con una sola suite produce error y nombra la suite ausente |
| Matriz del orquestador | `test_escritura_unica_del_orquestador` y `test_concesion_fuera_de_opencode_es_error` | `.opencode/**` es la única ruta con `allow` de escritura; una concesión sintética sobre `.github/**` produce fallo con la ruta concedida |
| Nota de cierre | `test_nota_de_cierre_append_only` y `test_nota_con_recuento_divergente_es_error` | La nota figura a continuación de las precedentes y transcribe el veredicto, el cierre de las 16 observaciones, la causa y el estado de las 4; un recuento distinto produce error con el valor en conflicto |
| Cierre de observaciones | `test_cierre_de_las_cuatro_observaciones` y `test_observacion_sin_artefacto_sigue_vigente` | Las 4 cuentan con artefacto y evidencia y el paquete declara 4 de 4; una observación sin artefacto se registra vigente y no se declara cerrada |
| Regresión de suites | `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q` | Las 2 suites devuelven código 0, con la suite del mecanismo ampliada y las 48 pruebas de `tools/git/tests` en verde |
| Validador agregado | `python tools\sdd\validate.py --all` | Código 0, sin entradas `[ERROR]`, con las advertencias de legado declaradas y sin advertencia de reporte en `SPEC-014` |
| Conservación de `SPEC-013` | `git diff` del reporte contra el commit anterior y lectura de la matriz y del dictamen | Diferencia limitada a la nota añadida; 40 filas en `PASADO`, dictamen `CONVERGIDO` y estado `validated` sin cambio |
| Límites de tiempo | Lectura de `timeout-minutes` de los pasos y del job, y tiempo medido de la ejecución agregada | Límite total del job de 5 minutos, límite de 1 minuto por paso de suite y 300 segundos o menos en la ejecución agregada |
| Contradicciones de la matriz | Contraste de `.opencode/agents/sdd.md` con §12 del protocolo sobre las rutas de escritura | 0 contradicciones y 0 atribuciones del orquestador fuera de `.opencode/**` |

- La verificación de las 2 suites se ejecuta por separado antes de la ejecución conjunta del job, de modo que el fallo quede atribuido a una suite concreta.
- No se produce script `.bat`, de modo que no aplica la declaración previa de comando, salida y métricas de la validación-first de scripts.
- La salida de cada ejecución se transcribe en la evidencia de su tarea y en el reporte de validación de esta spec.
- La ejecución del flujo en GitHub no forma parte de esta estrategia: `CB-002` y `CB-003` se ejercen sobre fixtures sintéticos y la ejecución remota queda fuera del alcance declarado.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | `C-1` y `.github/workflows/sdd.yml` | `test_preparacion_completa_del_arbol` y lectura de los parámetros de `actions/checkout` |
| `RF-002` | `C-2` y `docs/Flujo_de_Trabajo_Git.md` | `test_job_ejecuta_las_dos_suites` y contraste de la declaración de la norma de rango 4 |
| `RF-003` | `C-3` y `.opencode/agents/sdd.md` | `test_escritura_unica_del_orquestador` y contraste con §12 del protocolo |
| `RF-004` | `C-4` y el reporte de `SPEC-013` | `test_nota_de_cierre_append_only` y `git diff` del reporte |
| `RF-005` | `C-5` y el paquete de cierre de `tasks.md` | `test_cierre_de_las_cuatro_observaciones` y contraste de la tabla de `T-011` |
| `RNF-001` | Ejecución agregada del validador | Tiempo medido de `python tools\sdd\validate.py --all` en la evidencia de `T-012` |
| `RNF-002` | `C-2` y el job `verify` | Lectura de los 3 límites de tiempo y contraste con el límite total del job |
| `RNF-003` | `C-6` y `tools/sdd/tests/test_agent_permissions.py` | Recuento de las 6 comprobaciones con pareja positiva y negativa |
| `RNF-004` | Reporte de `SPEC-013` | `git diff` del reporte y contraste de las 40 filas, el dictamen y el estado |
| `RNF-005` | `C-3` y §12 del protocolo | Contraste de las rutas de escritura del orquestador con la tabla de §12 |
| `CB-001` | `C-1` y el paso de preparación del árbol | `test_flujo_sin_etiquetas_es_error` sobre el fixture sin `fetch-tags` |
| `CB-002` | `C-1` y la comprobación de la referencia a la spec | `test_alcance_sin_tag_usa_merge_base` sobre un historial sin tag anotado |
| `CB-003` | `C-2` y el check `verify` | `test_flujo_con_una_suite_es_error` y lectura del límite del paso de suite |
| `CB-004` | `C-3` y la matriz del orquestador | `test_concesion_fuera_de_opencode_es_error` con el rol declarado para la tarea |
| `CB-005` | `C-4` y el reporte de `SPEC-013` | `test_nota_de_cierre_append_only` con 2 notas consecutivas y el dictamen conservado |
| `CB-006` | `C-4` y la nota de cierre | `test_nota_con_recuento_divergente_es_error` con el valor en conflicto en el mensaje |
| `CB-007` | `C-5` y el paquete de cierre | `test_observacion_sin_artefacto_sigue_vigente` y contraste del estado vigente |
