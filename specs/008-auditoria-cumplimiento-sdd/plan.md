# Plan técnico — SPEC-008

## Referencias

- `spec.md`: `SPEC-008`, versión 0.3.0, estado `planned`, compuerta G1 aprobada por `Agent Sebaxtian` el 2026-11-14.
- `clarify.md`: `SPEC-008`, cerrado con `AMB-001` a `AMB-006` resueltos y parches aplicados a `spec.md`.
- `docs/constitution.md`: norma suprema de la jerarquía normativa.
- `AGENTS.md`: norma de rango inmediatamente inferior a la constitución.
- Base normativa documental: cada documento Markdown de `docs/sdd/` que no figure entre los seis excluidos por `spec.md`, más los documentos de `docs/sdd/plantillas/`.
- Documentos empleados solo como evidencia de la práctica: `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/sdd/README.md`, las guías de procedimiento de `docs/sdd/`, `tools/sdd/validate.py`, `.opencode/agents/`, `.opencode/commands/`, `specs/`, `CHANGELOG.md` y el historial de Git.
- Plantilla aplicada: `docs/sdd/plantillas/plan.md`.
- Guías de procedimiento consultadas: `docs/sdd/guia_plan_md.md` y `docs/sdd/guia_fase_implement_tdd.md`.
- Entregable de la Etapa 6: `docs/sdd/auditoria_cumplimiento_sdd.md`, documento único.

## Naturaleza del entregable

La especificación no produce código de producción ni componentes ejecutables. El entregable es un informe de auditoría en Markdown. Por esa razón este plan no describe módulos de software: describe la arquitectura del informe, el modelo de evidencia, los contratos de sus tablas, las escalas de decisión y la estrategia de verificación documental.

Consecuencias operativas que el plan fija:

- La Etapa 6 ejecuta el rol `documenter` (DEC-005) con una sola escritura: la creación de `docs/sdd/auditoria_cumplimiento_sdd.md`.
- La auditoría diagnostica y no corrige. Ningún artefacto auditado se edita, renombra, mueve ni elimina (RF-014, CA-010).
- La auditoría no aprueba compuertas. Las columnas de declarante y de resultado registran lo observado; la aprobación G4 de esta especificación corresponde al propietario.
- La auditoría no evalúa calidad de código, rendimiento, benchmarks ni la lógica interna del validador (RF-015, CA-011).
- La verificación del entregable es documental: validador determinista, comprobaciones de contenido sobre el texto del informe, control de alcance con Git y revisión independiente del rol `reviewer`.

## Arquitectura del informe

El informe se compone de doce secciones de nivel 2 en orden fijo, con numeración decimal en las subsecciones (DEC-009). Cada sección tiene una función única, un conjunto declarado de fuentes y una relación explícita con los requisitos de `spec.md`.

### Secciones obligatorias

| # | Sección | Contenido obligatorio | Requisitos cubiertos |
|---|---|---|---|
| 1 | Ficha de reproducibilidad | Fecha de corte, identificador del commit auditado, relación de comandos y consultas con su salida y código de salida, entorno de ejecución y cambios previos al corte | `RF-009`, `CB-012` |
| 2 | Base normativa e inventario | Jerarquía aplicada, regla de inclusión, inventario real de documentos normativos con recuento, lista de documentos excluidos y lista de artefactos usados solo como evidencia | `RF-001`, `RF-002`, `CB-007`, `CB-009`, `CB-011` |
| 3 | Criterio de evaluación y escalas | Regla de evaluación por dimensión, escala de veredicto de cinco valores, escala de severidad de cuatro niveles y regla de agregación del veredicto global | `RF-010` |
| 4 | Matriz de dimensiones D1 a D10 | Una fila por dimensión con veredicto propio y justificación citada | `RF-003`, `RF-017`, `RF-018`, `RF-019`, `CB-005`, `CB-008` |
| 5 | Hallazgos | Tabla consolidada y detalle individual por hallazgo | `RF-007`, `RF-008`, `RNF-002`, `RNF-007` |
| 6 | Evaluación de compuertas G1 a G6 | Una fila por compuerta con condición, evidencia, declarante y verificación | `RF-004`, `CB-003` |
| 7 | Trazabilidad por spec | Recorrido de la cadena completa por spec publicada y registro del eslabón faltante | `RF-005`, `CB-002` |
| 8 | Revisión retrospectiva | Revisión individual de `SPEC-001` a `SPEC-007` con veredicto por spec | `RF-006`, `CB-001` |
| 9 | Veredicto global | Regla de agregación aplicada con su resultado y la constancia de rechazo de correcciones | `RF-011`, `CB-010` |
| 10 | Hoja de ruta B1 a B4 | Remediaciones agrupadas por bloque, clasificadas y vinculadas al hallazgo de origen | `RF-012`, `RF-013` |
| 11 | Limitaciones y elementos no verificables | Cada elemento no verificable con causa y artefacto faltante | `RF-016` |
| 12 | Anexos de evidencia | Salidas completas de las consultas, extractos extensos y mapas auxiliares | `RNF-002`, `RNF-003` |

### Reglas de composición

- La sección 1 abre el informe y se escribe antes que cualquier otra sección de contenido, porque su commit de corte es la referencia temporal de cada cita (DEC-004).
- La sección 2 declara primero la jerarquía, después la regla de inclusión, después el inventario con recuento y al final las listas de excluidos y de evidencia de práctica.
- La sección 3 no repite la definición de las dimensiones: solo fija la regla de decisión, las escalas y la agregación.
- El título de la sección 3 evita el término sinónimo que contiene la subcadena vetada por el léxico del validador; su contenido cubre la regla de evaluación, las escalas y la agregación.
- La sección 4 contiene una fila por dimensión, en orden D1 a D10, sin omitir dimensiones y sin fusionar filas.
- La sección 5 contiene la tabla consolidada y, a continuación, un bloque `### AUD-NNN` por hallazgo con siete campos fijos: dimensión, veredicto, severidad, norma incumplida, evidencia, efecto observado y remediación propuesta.
- La sección 6 se ordena por compuerta G1 a G6 y conserva el orden normativo del ciclo.
- La sección 7 se agrupa por spec y, dentro de cada spec, por requisito o caso borde.
- La sección 8 dedica un bloque de nivel 3 a cada spec del periodo, de `SPEC-001` a `SPEC-007`, con veredicto individual y hallazgos asociados.
- La sección 9 aplica la regla de agregación de forma trazable: enuncia la regla, enumera las dimensiones que la activan y declara el resultado.
- La sección 10 usa exclusivamente los bloques B1, B2, B3 y B4 y las tres clasificaciones de remediación.
- La sección 11 lista cada elemento no verificable con tres datos: causa, artefacto que faltaría y dimensión afectada.
- La sección 12 contiene al menos cuatro anexos: inventario calculado, salida del validador, extractos de historial Git y mapa de rangos de hallazgos.

## Modelo de evidencia

### Clases de evidencia

| Clase | Objeto | Formato de cita | Campos obligatorios |
|---|---|---|---|
| E1 | Documento normativo de la base declarada en la sección 2 | `ruta:línea` o `ruta:línea_inicio-línea_fin` | Ruta relativa, línea, extracto literal |
| E2 | Artefacto de spec auditado | `ruta:línea` | Ruta relativa, línea, extracto literal |
| E3 | Artefacto de gobernanza o automatización tratado como práctica | `ruta:línea` | Ruta relativa, línea, extracto literal |
| E4 | Historial o estado de Git | Comando ejecutado con su salida y su código de salida | Comando literal, salida literal, código de salida |
| E5 | Consulta remota de solo lectura | Comando ejecutado con su salida y su código de salida | Comando literal, salida literal, código de salida, disponibilidad de credencial |

### Reglas de suficiencia

- Toda afirmación de conformidad exige al menos una cita de clase E1 o E2 verificable en el commit de corte.
- Toda afirmación de incumplimiento exige una cita de la norma (E1) y una cita de la práctica observada (E2, E3, E4 o E5).
- Toda ausencia se acredita con el comando que la demuestra y su salida, o con la ruta esperada y la evidencia de su inexistencia en el commit de corte.
- El resultado del validador determinista se cita como evidencia de la práctica (E3). Una divergencia entre el validador y la norma documental se registra como hallazgo de D2 o de D10 (`CB-005`).
- Una consulta remota sin credencial disponible no se sustituye por suposición: el punto se califica NO VERIFICABLE y se declara en la sección 11.
- La evidencia insuficiente para decidir produce NO VERIFICABLE, nunca una presunción de cumplimiento (`CB-001`, `CB-003`).
- La auditoría no completa cadenas ni inventarios con inferencias (`CB-002`).

### Registro de evidencia

Cada cita se compone de cinco datos y se repite literal en la sección 12 cuando su extensión lo exige:

1. Clase de evidencia.
2. Ubicación o comando.
3. Extracto o salida.
4. Código de salida, cuando se trate de una consulta.
5. Fecha y hora UTC de la observación.

No se crea un espacio de identificadores nuevo. Las citas se referencian por su ubicación y por el hallazgo `AUD-NNN` que las emplea.

### Ficha de reproducibilidad

La sección 1 se compone de tres tablas:

| Tabla | Campos |
|---|---|
| Corte | Fecha de corte en UTC, rama auditada, hash completo del commit de corte, hash abreviado, mensaje del commit |
| Entorno | Sistema operativo, versión de PowerShell, versión de Git, versión de Python, zona horaria de las marcas |
| Consultas | Orden, comando literal, propósito, salida resumida, código de salida, sección que la emplea |

La tabla de consultas enumera cada comando ejecutado durante la auditoría, incluidos los que no produjeron hallazgos. Un comando que no figure en esa tabla no puede sostener una afirmación del informe.

## Esquemas de tablas

### Tabla de dimensiones

| Dimensión | Objeto | Veredicto | Justificación | Hallazgos asociados |
|---|---|---|---|---|

- `Dimensión`: valor literal de D1 a D10.
- `Objeto`: el objeto de evaluación declarado en `spec.md`, sin reescritura.
- `Veredicto`: uno de los cinco valores de la escala.
- `Justificación`: entre una y tres oraciones, con al menos una cita de evidencia por oración que afirme un hecho.
- `Hallazgos asociados`: lista de identificadores `AUD-NNN` separados por coma, o el literal `Ninguno`.

### Tabla consolidada de hallazgos

| AUD-NNN | Dimensión | Veredicto | Severidad | Norma incumplida | Evidencia | Remediación |
|---|---|---|---|---|---|---|

- `AUD-NNN`: identificador único con el rango asignado a la dimensión (DEC-006).
- `Veredicto`: el veredicto de la dimensión afectada.
- `Severidad`: uno de los cuatro niveles.
- `Norma incumplida`: ruta y línea de la disposición incumplida.
- `Evidencia`: cita de la práctica observada, abreviada, con remisión al bloque de detalle.
- `Remediación`: identificador del bloque y clasificación, con remisión al bloque del hallazgo.

La tabla consolidada es la fuente del recuento. Su número de filas debe coincidir con el número de bloques `### AUD-NNN` de la misma sección y con el número de remediaciones vinculadas de la sección 10.

### Tabla de compuertas

| Compuerta | Condición normativa | Evidencia observada | Declarante | Verificación | Resultado |
|---|---|---|---|---|---|

- `Compuerta`: valor literal de G1 a G6.
- `Condición normativa`: condición de superación según la norma citada con ruta y línea.
- `Evidencia observada`: artefacto, línea o consulta que acredita la superación, o el literal `Sin evidencia conservada`.
- `Declarante`: rol o persona que declaró la aprobación, con la cita de la línea que lo registra.
- `Verificación`: resultado de contrastar la evidencia con la condición.
- `Resultado`: uno de los cinco valores de la escala. La ausencia de evidencia conservada produce NO VERIFICABLE y nunca CONFORME por existencia del estado liberado (`CB-003`).

### Tabla de trazabilidad

| Spec | RF/CB | CA | T | Evidencia | Commit | Merge | Release | Eslabón faltante |
|---|---|---|---|---|---|---|---|---|

- `Spec`: valor literal de `SPEC-001` a `SPEC-007`.
- `RF/CB`: requisito o caso borde de la spec, en una fila por identificador.
- `CA`, `T`, `Commit`, `Merge`, `Release`: identificador o referencia observada.
- `Evidencia`: prueba o comando declarado por la spec para ese requisito.
- `Eslabón faltante`: literal `Ninguno` o el nombre del eslabón ausente con el `AUD-NNN` que lo registra.
- Ninguna celda queda vacía. La ausencia se escribe como `AUSENTE` y se acompaña del `AUD-NNN` correspondiente.

### Tabla de remediaciones

| Bloque | Remediación | Hallazgo AUD-NNN | Clasificación |
|---|---|---|---|

- `Bloque`: valor literal B1, B2, B3 o B4.
- `Remediación`: acción concreta y verificable, redactada en una oración.
- `Hallazgo AUD-NNN`: identificador del hallazgo que la origina. Una remediación puede cubrir varios hallazgos y cada hallazgo exige al menos una fila.
- `Clasificación`: valor literal `editorial`, `requiere spec` o `proceso`.

### Rangos de hallazgos

| Dimensión | Rango reservado |
|---|---|
| D1 | `AUD-001` a `AUD-010` |
| D2 | `AUD-011` a `AUD-020` |
| D3 | `AUD-021` a `AUD-030` |
| D4 | `AUD-031` a `AUD-040` |
| D5 | `AUD-041` a `AUD-050` |
| D6 | `AUD-051` a `AUD-060` |
| D7 | `AUD-061` a `AUD-070` |
| D8 | `AUD-071` a `AUD-080` |
| D9 | `AUD-081` a `AUD-090` |
| D10 | `AUD-091` a `AUD-099` |

Si una dimensión supera su capacidad de diez hallazgos, el excedente continúa en la numeración inmediatamente posterior al último número asignado del informe y el anexo del mapa de rangos registra el rango real empleado (DEC-006).

## Escalas operativas

### Veredicto por dimensión

| Veredicto | Regla de decisión |
|---|---|
| CONFORME | La dimensión no registra hallazgos y cada caso evaluable cuenta con evidencia verificable en el commit de corte |
| PARCIAL | La dimensión registra al menos un hallazgo de severidad Media o Baja, o incumple en una parte de los casos evaluables sin superar la mitad, o un subconjunto acotado carece de evidencia |
| NO CONFORME | La dimensión registra al menos un hallazgo de severidad Alta o Crítica, o incumple en más de la mitad de los casos evaluables |
| NO VERIFICABLE | La dimensión carece de evidencia para decidir el conjunto de sus casos evaluables |
| NO APLICA | La dimensión carece de objeto evaluable en el periodo auditado, con justificación de la ausencia de objeto |

Precedencia cuando dos reglas concurren: NO CONFORME, después NO VERIFICABLE cuando la falta de evidencia impide decidir la dimensión, después PARCIAL, después CONFORME (DEC-008).

### Severidad

| Severidad | Criterio de asignación |
|---|---|
| Crítica | El hallazgo anula una compuerta o permite un cambio sin spec aprobada |
| Alta | El hallazgo rompe la trazabilidad de requisitos o la evidencia de verificación |
| Media | El hallazgo deja un contrato de artefacto incompleto sin pérdida de trazabilidad |
| Baja | El hallazgo produce una inconsistencia editorial o documental menor |

La severidad se asigna por el efecto observado, no por el número de ocurrencias. Se elige el nivel más alto cuya definición coincida con el efecto y se declara el efecto en el campo correspondiente del hallazgo (DEC-008).

### Regla de agregación

Se evalúa en orden y se aplica la primera regla que se cumpla:

| Orden | Condición | Veredicto global |
|---|---|---|
| 1 | Existe al menos una dimensión NO CONFORME con al menos un hallazgo de severidad Crítica o Alta | NO CONFORME |
| 2 | Ninguna dimensión alcanza CONFORME, PARCIAL ni NO CONFORME, y al menos una es NO VERIFICABLE | NO VERIFICABLE |
| 3 | Existe al menos una dimensión NO CONFORME con hallazgos exclusivamente de severidad Media o Baja | PARCIAL |
| 4 | Existe al menos una dimensión PARCIAL o NO VERIFICABLE y ninguna dimensión NO CONFORME | PARCIAL |
| 5 | Cada dimensión es CONFORME o NO APLICA, y al menos una es CONFORME | CONFORME |
| 6 | Cada dimensión es NO APLICA | NO APLICA |

Justificación: la regla 1 conserva la escalada por severidad; la regla 2 evita declarar conformidad parcial cuando no existe base para decidir; la regla 3 cubre el caso de una dimensión NO CONFORME cuyos hallazgos no comprometen compuertas ni trazabilidad, caso no previsto en la propuesta inicial de agregación; las reglas 4 a 6 completan el espacio de estados sin solapamiento.

## Fuentes de evidencia por dimensión

| Dimensión | Fuentes primarias | Evidencia exigida | Producto en el informe |
|---|---|---|---|
| D1 | `docs/constitution.md`, `AGENTS.md`, corpus normativo de `docs/sdd/`, `docs/sdd/plantillas/` | Jerarquía declarada con `ruta:línea`, inventario calculado por regla, tensión de rango del documento excluido | Sección 2 y fila D1 de la sección 4 |
| D2 | Documentos normativos que describen el ciclo, artefactos de cada spec, salida del validador | Etapas declaradas, artefacto de salida por etapa, estado resultante observado | Filas D2 y hallazgos de divergencia |
| D3 | Guías de contrato de cada artefacto y plantillas | Campos y secciones obligatorias frente a artefactos reales | Fila D3 y hallazgos por artefacto |
| D4 | Norma de compuertas, secciones de aprobaciones de cada spec, reportes de validación, `specs/INDEX.md` | Condición, evidencia, declarante y verificación por compuerta | Sección 6 y fila D4 |
| D5 | `Cubre:` de cada criterio, matriz de cobertura de cada plan, requisitos cubiertos de cada tarea, reportes de validación, historial Git | Cadena completa por requisito, con commit, fusión y release | Sección 7 y fila D5 |
| D6 | Modelo de estados declarado, frontmatter de cada spec, `specs/INDEX.md`, historial de cambios | Estado observado por spec y transición registrada | Fila D6 y hallazgos de transición |
| D7 | Matriz de roles y permisos declarada, archivos de agentes y comandos, artefactos que registran operaciones | Permiso declarado frente a operación observada | Fila D7 y hallazgos de exceso o carencia de permiso |
| D8 | Reportes de validación, tareas con evidencia, comandos y salidas citadas, salida del validador | Existencia, suficiencia y reproducibilidad de la prueba | Fila D8 y hallazgos de evidencia insuficiente |
| D9 | Historial Git, tags anotados, fusiones, `CHANGELOG.md`, `specs/INDEX.md` | Nomenclatura, modalidad de fusión, tag y registro de cambios | Fila D9 y sección de desviaciones |
| D10 | Coincidencia entre documentos normativos, índice, configuración de agentes y validador | Contradicción, documento excluido sin seguimiento, divergencia del validador | Fila D10 y hallazgos de consistencia |

Las fuentes de las dimensiones D2, D4 y D6 se toman de los documentos normativos incluidos por la regla de DEC-001. El protocolo operativo y las guías de procedimiento se citan como evidencia de la práctica declarada, nunca como criterio de conformidad.

## Decisiones técnicas

### DEC-001: base normativa por regla de inclusión

- **Decisión:** considerar norma cada documento Markdown de `docs/sdd/` que no figure entre los seis excluidos por nombre en `spec.md`, más los documentos de `docs/sdd/plantillas/`. El inventario se calcula en el commit de corte listando el directorio, filtrando por extensión `.md` y aplicando la lista de exclusión por nombre exacto. El informe declara el inventario resultante y su recuento.
- **Justificación:** la regla se mantiene verificable cuando el corpus cambia, permite reproducir el recuento desde el commit de corte y evita que la especificación envejezca con cada documento nuevo.
- **Alternativas descartadas:** (a) fijar un recuento en la especificación: contradice `RNF-003` y obliga a editar la norma por cada alta documental; (b) enumerar una lista blanca de documentos incluidos: traslada al plan el mantenimiento del corpus y produce omisiones silenciosas; (c) incorporar `docs/sdd/PROTOCOLO_OPERATIVO.md` como norma: contradice `spec.md` y duplicaría el rango 3 ya declarado en la constitución.

### DEC-002: regla de agregación del veredicto global

- **Decisión:** aplicar la tabla ordenada de seis reglas de la sección «Escalas operativas». La primera regla que se cumpla determina el veredicto global. El informe enuncia la regla aplicada y enumera las dimensiones que la activan.
- **Justificación:** la agregación debe ser determinista (`RNF-004`), congruente con los veredictos por dimensión (`RF-011`) y sensible a la severidad. La propuesta inicial no cubría una dimensión NO CONFORME con hallazgos exclusivamente Media o Baja; la regla 3 cierra ese hueco sin elevar el veredicto global por encima de lo que la evidencia sostiene.
- **Alternativas descartadas:** (a) mayoría simple de dimensiones conformes: ignora la severidad y permitiría un global CONFORME con una compuerta anulada; (b) criterio del caso más grave sin umbral: convierte la escala de severidad en un adorno y produce global NO CONFORME por un hallazgo Baja; (c) puntuación ponderada: introduce pesos sin respaldo normativo y rompe la reproducibilidad por terceros.

### DEC-003: formato de evidencia

- **Decisión:** citar los archivos con ruta relativa y número de línea, o rango de líneas cuando la disposición ocupe varias. Citar las consultas con el comando literal, su salida literal y su código de salida. Toda cita extensa se reproduce en la sección 12 y se referencia desde la sección que la emplea.
- **Justificación:** la ruta con línea permite a un tercero abrir el artefacto en el commit de corte; el comando con salida permite repetir la consulta y comparar el resultado.
- **Alternativas descartadas:** (a) citar solo el archivo sin línea: obliga a revisar el documento completo y hace inviable la verificación por muestreo; (b) citar solo extractos sin ruta: impide localizar la fuente y facilita la cita descontextualizada; (c) citar solo comandos sin salida: no permite distinguir el resultado observado del esperado.

### DEC-004: commit de corte

- **Decisión:** fijar el commit de corte en el `HEAD` de la rama `feat/auditoria-cumplimiento-sdd` inmediatamente después de registrar `spec.md`, `clarify.md`, `plan.md` y `tasks.md`, y antes de escribir el informe. El hash completo y el abreviado se declaran en la sección 1. Los cambios presentes en el árbol de trabajo y no registrados en ese commit quedan fuera del periodo auditado y se consignan como evidencia de D9 y D10.
- **Justificación:** el corte debe incluir los artefactos de la propia especificación, porque la auditoría evalúa también su propio proceso; y debe ser anterior a la escritura del informe, porque el informe no puede citarse a sí mismo en el commit que lo contiene.
- **Alternativas descartadas:** (a) cortar en la creación de la rama: excluiría `spec.md`, `clarify.md`, `plan.md` y `tasks.md` del periodo y rompería `CA-007`; (b) cortar después de escribir el informe: el informe quedaría fuera del commit citado y su propia evidencia sería inestable; (c) usar `HEAD` sin verificación: un commit posterior durante la auditoría invalidaría cada cita.

### DEC-005: ejecutor de la etapa 6

- **Decisión:** la Etapa 6 la ejecuta el rol `documenter`, con escritura limitada a la creación de `docs/sdd/auditoria_cumplimiento_sdd.md`. La ausencia de un rol de auditoría en la matriz vigente se registra como hallazgo de D7.
- **Justificación:** `documenter` es el único rol con permiso de escritura en `docs/**`; usar un rol sin ese permiso llevaría a una operación fuera de la allowlist declarada y a un hallazgo de D7 provocado por la propia auditoría.
- **Alternativas descartadas:** (a) ejecutar con `coder`: no tiene permiso de escritura en `docs/`; (b) ejecutar con `sdd`: su alcance es la orquestación de solo lectura y el registro Git de artefactos de control; (c) crear un rol de auditor durante la auditoría: modificaría la configuración auditada y violaría `RF-014`.

### DEC-006: numeración de hallazgos

- **Decisión:** numerar los hallazgos de forma correlativa y agrupada por dimensión, con diez números reservados por dimensión según la tabla de rangos. Dentro de cada dimensión, el orden es el de aparición en la sección 4. Un número asignado no se reutiliza entre versiones del informe. El excedente de una dimensión sigue la regla declarada en la sección de rangos y se documenta en el anexo del mapa de rangos.
- **Justificación:** el rango por dimensión permite auditar la coherencia entre la tabla consolidada, el detalle y la hoja de ruta sin ambigüedad; la no reutilización preserva el historial entre versiones (`RNF-005`).
- **Alternativas descartadas:** (a) numeración global por orden de aparición: impide detectar un hallazgo asignado a una dimensión distinta de la que le corresponde; (b) numeración por severidad: obliga a renumerar al cambiar una severidad y rompe las referencias ya publicadas; (c) reutilizar números liberados: impide comparar dos versiones del informe.

### DEC-007: adaptación de validación-first a la documentación

- **Decisión:** antes de escribir cada sección se declara en `tasks.md` el resultado esperado: títulos, cabeceras de tabla, número mínimo de filas, valores admitidos en cada columna y comprobación asociada. Después de escribirla se ejecuta la comprobación declarada. La declaración vive en `tasks.md`, no en el informe.
- **Justificación:** reproduce el principio de validación-first aplicado a los scripts `.bat`: el criterio de éxito se fija antes de producir el artefacto y no se ajusta después para que coincida con lo escrito.
- **Alternativas descartadas:** (a) TDD con pruebas automatizadas: no existe código que probar y el validador no inspecciona el contenido del informe; (b) verificación solo al final: permite redactar el informe adaptando el criterio a lo observado y elimina la independencia del control.

### DEC-008: asignación determinista de severidad y veredicto de dimensión

- **Decisión:** asignar la severidad por el efecto observado, eligiendo el nivel más alto cuya definición coincida, y declarar el efecto en el hallazgo. Asignar el veredicto de dimensión con la precedencia NO CONFORME, NO VERIFICABLE, PARCIAL, CONFORME, aplicando las reglas de la sección «Escalas operativas».
- **Justificación:** `RNF-004` exige que dos auditorías independientes obtengan la misma severidad por hallazgo y el mismo veredicto por dimensión. Una regla por efecto y precedencia fija elimina la apreciación personal.
- **Alternativas descartadas:** (a) severidad por frecuencia de ocurrencia: no corresponde a las definiciones de `spec.md`; (b) veredicto por mayoría de casos: permite un CONFORME con una compuerta anulada; (c) dejar la precedencia a criterio del auditor: rompe el determinismo.

### DEC-009: estructura fija de doce secciones

- **Decisión:** el informe mantiene las doce secciones de nivel 2 en el orden declarado, con títulos literales y numeración decimal en las subsecciones. No se añaden secciones de nivel 2 fuera de las doce. El contenido auxiliar se ubica como subsección de la sección que lo emplea o como anexo en la sección 12.
- **Justificación:** una estructura fija hace mecánica la comprobación de cobertura por criterio de aceptación y evita que el informe derive hacia secciones no previstas.
- **Alternativas descartadas:** (a) estructura libre: impide verificar la cobertura con comprobaciones de contenido; (b) anexo en archivo separado: incumple `RNF-001`, que exige documento único; (c) secciones adicionales para escalas y para cierre: duplican contenido y abren la puerta a contradicciones internas.

### DEC-010: muestreo para la revisión independiente

- **Decisión:** la revisión independiente del rol `reviewer` reejecuta un conjunto fijo de verificaciones: las seis entradas de compuerta de la sección 6, una fila de trazabilidad por cada spec del periodo y la primera cita de evidencia de cada dimensión. Cualquier discrepancia entre la cita y el artefacto del commit de corte se registra y se corrige antes de la compuerta G4.
- **Justificación:** un muestreo fijo es reproducible y comparable entre revisiones; un muestreo aleatorio no permite afirmar que dos revisiones cubrieron el mismo conjunto.
- **Alternativas descartadas:** (a) revisar el informe completo cita por cita: supera el tiempo disponible y no aporta cobertura diferencial; (b) revisar solo la sección de veredicto global: no valida la evidencia que lo sostiene; (c) muestreo aleatorio declarado: no es reproducible entre revisiones independientes.

## Secuencia de producción del informe

La Etapa 6 se ejecuta en bloques ordenados. Cada bloque termina con la comprobación declarada y con la constancia de la tarea correspondiente en `tasks.md`.

1. **Corte y ficha.** Verificar que el árbol de trabajo coincide con el estado declarado, fijar el commit de corte, capturar el entorno y la lista de cambios previos. Escribir la sección 1.
2. **Base normativa.** Calcular el inventario por regla en el commit de corte, ordenar los documentos, registrar el recuento, la lista de excluidos y la lista de evidencia de práctica. Escribir la sección 2.
3. **Criterio y escalas.** Escribir la sección 3 con las escalas y la regla de agregación, sin evaluar todavía ninguna dimensión.
4. **Dimensiones.** Evaluar D1 a D10 en orden, recogiendo evidencia por dimensión, asignando hallazgos con su rango y redactando la sección 4.
5. **Hallazgos.** Consolidar la tabla de la sección 5, escribir el detalle de cada `AUD-NNN` y verificar la coincidencia de recuentos con la sección 4.
6. **Compuertas.** Recorrer G1 a G6, contrastar condición y evidencia y escribir la sección 6.
7. **Trazabilidad.** Recorrer la cadena completa por cada spec publicada y escribir la sección 7 con el eslabón faltante declarado.
8. **Revisión retrospectiva.** Escribir la sección 8 con un bloque por spec y su veredicto individual.
9. **Cierre.** Aplicar la regla de agregación, escribir la sección 9, redactar la hoja de ruta en la sección 10 y las limitaciones en la sección 11.
10. **Anexos.** Reproducir las salidas completas y el mapa de rangos en la sección 12.
11. **Verificación.** Ejecutar la batería de la estrategia de testing y corregir el informe hasta que cada comprobación se cumpla.
12. **Revisión independiente.** Entregar el informe al rol `reviewer` con el commit de corte y la tabla de consultas.

## Estrategia de testing

La verificación es documental. No se crean archivos de prueba ni suites nuevas. Cada comprobación tiene comando, salida esperada y acción ante fallo. Las etiquetas V1 a V23 identifican comprobaciones de esta estrategia y no pertenecen a los espacios de identificadores del protocolo.

### Comprobaciones estructurales

| # | Comprobación | Comando | Salida esperada |
|---|---|---|---|
| V1 | Conformidad estructural de la spec y sus artefactos | `python tools\sdd\validate.py --spec SPEC-008 --gate G3` | Código de salida `0`; sin errores |
| V2 | Sin errores en el conjunto de specs | `python tools\sdd\validate.py --all` | Código de salida `0` |
| V3 | Informe presente y único | `Test-Path docs/sdd/auditoria_cumplimiento_sdd.md` | `True` |
| V4 | Doce secciones de nivel 2 | `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^## ').Count` | `12` |
| V5 | Diez filas de dimensión | `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D(10|[1-9]) \|').Count` | `10` |
| V6 | Seis filas de compuerta | `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| G[1-6] \|').Count` | `6` |

### Comprobaciones de contenido

| # | Comprobación | Regla |
|---|---|---|
| V7 | Veredicto por dimensión | Cada fila D1 a D10 contiene uno de los cinco valores admitidos en la columna de veredicto |
| V8 | Hallazgo con evidencia y remediación | Cada fila de la tabla consolidada tiene los siete campos no vacíos y cada bloque `### AUD-NNN` contiene los siete campos fijados |
| V9 | Recuento coherente | El número de filas `^\| AUD-` de la tabla consolidada coincide con el número de encabezados `^### AUD-` de la sección 5 |
| V10 | Cobertura de remediaciones | Cada `AUD-NNN` aparece al menos una vez en la tabla de remediaciones y cada fila de remediación referencia un `AUD-NNN` existente |
| V11 | Compuertas completas | Cada fila G1 a G6 presenta las seis columnas con contenido y un resultado de la escala |
| V12 | Trazabilidad sin celdas vacías | Ninguna celda de la tabla de trazabilidad queda vacía ni contiene un literal distinto de `AUSENTE` o `Ninguno` para una ausencia |
| V13 | Commit citado | La salida de `git rev-parse HEAD` coincide con el hash declarado en la sección 1 |
| V14 | Clasificación de remediaciones | Cada valor de la columna de clasificación es `editorial`, `requiere spec` o `proceso`; cada bloque es B1, B2, B3 o B4 |
| V15 | Alcance de escritura | `git status --short` no muestra archivos distintos del informe respecto de la lista de cambios previos capturada en la sección 1 |
| V16 | Sin contenido fuera de alcance | El informe no contiene secciones ni apartados dedicados a rendimiento, benchmarks, calidad de código ni lógica interna del validador; la constancia de rechazo de correcciones figura en las secciones 9 o 10 |
| V21 | Limitaciones completas | Cada dimensión NO VERIFICABLE y cada compuerta con `Sin evidencia conservada` aparece en la sección 11 con causa y artefacto faltante |
| V22 | Base normativa declarada | La sección 2 contiene los seis nombres excluidos, el recuento coincide con el listado calculado por DEC-001 y la jerarquía sitúa la constitución y `AGENTS.md` por encima de la base documental |
| V23 | Escalas declaradas | La sección 3 contiene los cinco valores de veredicto, los cuatro niveles de severidad y la tabla de agregación con seis reglas ordenadas |
| V17 | Sin léxico ambiguo | Búsqueda de los términos prohibidos del protocolo en el informe sin coincidencias |

### Comprobaciones de reproducibilidad

| # | Comprobación | Procedimiento |
|---|---|---|
| V18 | Repetición de consultas | Un tercero ejecuta la tabla de consultas de la sección 1 y obtiene la salida declarada con el mismo código de salida |
| V19 | Repetición de citas | Un tercero abre cinco citas de archivo con línea en el commit de corte y encuentra el extracto declarado |
| V20 | Determinismo del veredicto | La revisión independiente de D4 y D5 con el muestreo de DEC-010 obtiene los mismos veredictos y las mismas severidades |

### Registro de la verificación

- El resultado de V1 a V23 se registra en `validation_report.md` de esta spec durante la Etapa 7, no en el informe de auditoría.
- Una comprobación fallida obliga a corregir el informe y a repetir la batería completa.
- Las comprobaciones V1 y V2 se ejecutan también al cierre de la Etapa 5, para confirmar que el plan y las tareas son conformes antes de escribir el informe.
- El control de alcance V15 se ejecuta antes de la revisión independiente y después de cualquier corrección posterior.

## Matriz de cobertura

| Requisito | Componente | Prueba / comando |
|---|---|---|
| RF-001 | Sección 2, base normativa e inventario | Inventario calculado por la regla de DEC-001 en el commit de corte; recuento declarado y comprobado con el listado del directorio (V22, V18) |
| RF-002 | Secciones 2 y 4, jerarquía y hallazgo de rango | Tabla de jerarquía con constitución y `AGENTS.md` por encima de la base documental; hallazgo de D1 por la exclusión del documento de rango 3 (V22, V7) |
| RF-003 | Sección 4, matriz de dimensiones | Diez filas D1 a D10 con veredicto independiente (V5, V7) |
| RF-004 | Sección 6, compuertas | Seis filas G1 a G6 con condición, evidencia, declarante y verificación (V6, V11) |
| RF-005 | Sección 7, trazabilidad | Una fila por requisito con la cadena completa y el eslabón faltante declarado (V12) |
| RF-006 | Sección 8, revisión retrospectiva | Siete bloques de spec con veredicto individual (V4, V7) |
| RF-007 | Sección 5, hallazgos | Identificador único por rango de dimensión y siete campos por hallazgo (V8, V9) |
| RF-008 | Secciones 5 y 12, evidencia | Cada hallazgo cita ruta con línea o comando con salida (V8, V19) |
| RF-009 | Sección 1, ficha de reproducibilidad | Fecha, commit y relación de consultas con salida y código de salida (V13, V18) |
| RF-010 | Sección 3, escalas | Cinco valores de veredicto, cuatro niveles de severidad y regla de agregación explícita (V23) |
| RF-011 | Sección 9, veredicto global | Aplicación trazable de la regla de agregación de DEC-002 (V23, V9) |
| RF-012 | Sección 10, hoja de ruta | Bloques B1 a B4 con remediaciones agrupadas (V14) |
| RF-013 | Sección 10, clasificación | Cada remediación con clasificación y hallazgo de origen (V10, V14) |
| RF-014 | Informe completo y control de alcance | Escritura única del informe y comparación del árbol de trabajo con el corte (V15) |
| RF-015 | Informe completo | Ausencia de apartados de rendimiento, benchmarks, calidad de código y lógica del validador (V16) |
| RF-016 | Sección 11, limitaciones | Cada elemento no verificable con causa y artefacto faltante (V21) |
| RF-017 | Sección 4, fila D9, y sección 5 | Desviaciones de Git registradas con referencia observable y sin corrección (V12) |
| RF-018 | Sección 4, D6 | Cada estado observado contrastado con el modelo y cada transición no permitida registrada (V7, V9) |
| RF-019 | Sección 4, D7 | Permisos declarados por rol contrastados con las operaciones observadas (V7) |
| RNF-001 | Archivo único | Informe en español, Markdown, en la ruta declarada y sin documento auxiliar (V3) |
| RNF-002 | Secciones 4, 5 y 6 | Toda afirmación con evidencia citada y sin veredictos sin cita (V8, V19) |
| RNF-003 | Sección 1 y sección 12 | Reproducción por un tercero desde el commit y la tabla de consultas (V18, V19) |
| RNF-004 | Escalas y muestreo de DEC-010 | Dos revisiones independientes obtienen el mismo veredicto y la misma severidad (V20) |
| RNF-005 | Rangos de hallazgos | Numeración única, ordenada por dimensión y sin reutilización (V9) |
| RNF-006 | Secciones 5 y 10 | Correspondencia bidireccional entre hallazgos y remediaciones (V10) |
| RNF-007 | Sección 5, tabla consolidada | Dimensión, severidad y veredicto por hallazgo con recuento determinista (V9) |
| CB-001 | Secciones 5 y 11 | Ausencia citada como evidencia y verificación de que el artefacto no se creó (V8, V15) |
| CB-002 | Sección 7 | Eslabón faltante declarado sin completar la cadena por inferencia (V12) |
| CB-003 | Sección 6 | Compuerta sin evidencia conservada calificada NO VERIFICABLE sin presunción (V11) |
| CB-004 | Sección 5 | Contradicción registrada con el rango de cada documento y la resolución aplicable (V8, V9) |
| CB-005 | Secciones 4 y 12 | Divergencia del validador registrada como hallazgo de D2 o D10 (V7, V9) |
| CB-006 | Sección 4, fila D9, y sección 5 | Desviación con referencia observable y sin reescritura del historial (V12) |
| CB-007 | Sección 2 | Documento excluido clasificado como referencia y no empleado como criterio (V22, V16) |
| CB-008 | Sección 4 | Dimensión sin objeto calificada NO APLICA con justificación (V7) |
| CB-009 | Sección 2 | Diferencia de inventario registrada como hallazgo de D1 sin corregir el declarado (V22, V9) |
| CB-010 | Secciones 9 y 10 | Constancia de rechazo de correcciones y remisión a especificación posterior (V16) |
| CB-011 | Sección 2 | Tensión de rango registrada como hallazgo de D1 sin alterar la jerarquía (V22, V9) |
| CB-012 | Sección 1 | Cambios previos al corte listados, fuera del periodo y consignados en D9 y D10 (V13, V15) |

## Riesgos y mitigaciones

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Evidencia histórica de compuertas no conservada en el repositorio | Verificación imposible de decidir | Calificar NO VERIFICABLE conforme a `CB-003` y declarar el artefacto faltante en la sección 11 |
| Atribución de operaciones a agentes no registrada en el historial | D7 sin evidencia suficiente | Declarar la limitación con el artefacto que faltaría y no presumir cumplimiento |
| Corpus documental modificado durante la auditoría | Citas inestables | Fijar el commit de corte antes de escribir y citar siempre contra ese commit |
| Deriva de alcance hacia correcciones | Violación de `RF-014` | Rechazar la corrección y remitirla a especificación posterior; control V15 |
| Ambigüedad en la asignación de severidad | Veredictos no reproducibles | Aplicar la regla de efecto de DEC-008 y declarar el efecto en cada hallazgo |
| Notación de comandos dependiente del shell | Consultas no repetibles | Declarar el shell, la versión de Git y la versión de Python en la sección 1 |
| Reescritura accidental del historial | Pérdida de evidencia | Prohibición explícita en el informe y verificación del historial tras la Etapa 6 |
