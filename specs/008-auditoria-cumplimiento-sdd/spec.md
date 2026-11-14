---
id: SPEC-008
title: Auditoría de cumplimiento SDD
status: tasked
version: 0.4.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/auditoria-cumplimiento-sdd
release: ""
supersedes: ""
superseded_by: ""
---

# Auditoría de cumplimiento SDD

## Contexto y objetivo

El proyecto declara un régimen de Desarrollo Basado en Especificaciones (SDD) con siete etapas, compuertas de control con aprobación humana, trazabilidad obligatoria de requisitos a release y verificación determinista mediante un validador propio. Ese régimen se ha aplicado en siete incrementos publicados, de SPEC-001 a SPEC-007, que acumulan spec, clarificación, plan, tareas, implementación y reporte de validación.

La existencia de documentos normativos y de artefactos publicados no demuestra que la práctica real los cumpla. Hasta la fecha no se ha ejecutado una verificación independiente que contraste la norma declarada con lo efectivamente registrado en el repositorio, en su historial de Git y en los artefactos de cada spec. Sin esa verificación, las desviaciones permanecen invisibles, las compuertas pueden declararse superadas sin evidencia reproducible y la trazabilidad puede romperse sin que nadie lo advierta.

El objetivo de esta especificación es definir el contrato de una auditoría de cumplimiento SDD puro, con enfoque estrictamente operativo, que produzca un diagnóstico verificable del régimen declarado frente a la práctica observada. El entregable es un informe único en `docs/sdd/auditoria_cumplimiento_sdd.md`. La auditoría diagnostica y no corrige: no modifica artefactos auditados, no repara hallazgos y no altera el historial de Git.

### Base normativa y exclusiones

La base normativa de la auditoría se define por regla de inclusión y no por un recuento fijado: es norma cada documento Markdown de `docs/sdd/` salvo los seis documentos de referencia excluidos por nombre, a los que se suman los documentos de `docs/sdd/plantillas/`.

Documentos de `docs/sdd/` excluidos de la base normativa:

- `docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md`
- `docs/sdd/diagrama_flujo_ciclo_vida_sdd.md`
- `docs/sdd/guia_maestra_sdd.md`
- `docs/sdd/plan_cierre_brechas_sdd.md`
- `docs/sdd/PROTOCOLO_OPERATIVO.md`
- `docs/sdd/README.md`

La especificación no fija ningún número de documentos. El informe de auditoría DEBE declarar el inventario real de documentos normativos y su recuento en la fecha de corte, obtenidos por aplicación de esta regla.

Por encima de esa base documental rige la jerarquía declarada en `docs/constitution.md`: la constitución es norma suprema y `AGENTS.md` ocupa el rango siguiente. El protocolo operativo, la configuración de agentes, los comandos del ciclo y el validador determinista se emplean únicamente como evidencia de la práctica real, no como criterio normativo.

### Dimensiones evaluadas

| Dimensión | Objeto de evaluación |
|---|---|
| D1 | Autoridad normativa: jerarquía declarada, vigencia y aplicabilidad de cada documento |
| D2 | Ciclo de 7 etapas: secuencia, artefacto de salida y estado resultante por etapa |
| D3 | Contratos de artefactos: campos, secciones y prohibiciones de cada artefacto |
| D4 | Compuertas G1 a G6: condición, evidencia, declarante y verificación |
| D5 | Trazabilidad: cadena RF/CB → CA → T → evidencia → commit → merge → release |
| D6 | Estados y transiciones: modelo declarado frente a estados observados |
| D7 | Roles y menor privilegio: permisos declarados frente a operaciones ejecutadas |
| D8 | Evidencia y verificación: existencia, suficiencia y reproducibilidad de la prueba |
| D9 | Integración Git y release: nomenclatura, fusión, tags y registro de cambios |
| D10 | Consistencia documental operativa: coincidencia entre documentos, índice, agentes y validador |

### Escala de veredicto y severidad

| Veredicto | Definición operativa |
|---|---|
| CONFORME | La práctica satisface la norma y la evidencia permite verificarlo sin excepción |
| PARCIAL | La práctica satisface la norma en una parte de los casos evaluados e incumple en otra, o la evidencia resulta insuficiente en un subconjunto acotado |
| NO CONFORME | La práctica incumple la norma de forma sistemática o en un punto que compromete el control |
| NO VERIFICABLE | No existe evidencia disponible para decidir, o el artefacto requerido no existe |
| NO APLICA | La dimensión carece de objeto evaluable en el periodo auditado |

| Severidad | Alcance del efecto |
|---|---|
| Crítica | Anula una compuerta o permite un cambio sin spec aprobada |
| Alta | Rompe la trazabilidad de requisitos o la evidencia de verificación |
| Media | Deja un contrato de artefacto incompleto sin pérdida de trazabilidad |
| Baja | Produce una inconsistencia editorial o documental menor |

### Alcance retrospectivo

El periodo auditado comprende las siete specs publicadas, en el estado registrado en `specs/INDEX.md` al momento de la redacción de esta especificación.

| Spec | Título | Estado | Release |
|---|---|---|---|
| SPEC-001 | Menú principal main.bat | released | v0.2.0 |
| SPEC-002 | Orquestación de subagentes SDD | released | v0.3.0 |
| SPEC-003 | Validación estricta de la compuerta G4 | released | v0.3.1 |
| SPEC-004 | Subagente documenter para correcciones normativas | released | v0.4.0 |
| SPEC-005 | Compuertas completas y deuda residual | released | v0.5.0 |
| SPEC-006 | Cierre de observaciones de documentación | released | v0.5.1 |
| SPEC-007 | Protección determinista de ramas GitHub | released | v0.6.0 |

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** fija el alcance de la auditoría, aprueba la compuerta G1 de esta especificación, recibe el informe y decide qué remediaciones se ejecutan y en qué orden.
- **Auditor:** ejecuta la auditoría con independencia del ciclo de desarrollo, verifica cada dimensión y escribe únicamente el informe. No aprueba compuertas y no corrige hallazgos.
- **Orquestador SDD:** invoca y supervisa la auditoría, facilita el acceso a los artefactos y no edita el informe ni los artefactos auditados.
- **Agentes de desarrollo y documentación:** no participan en la auditoría; sus artefactos son objeto de la evaluación.

## Requisitos funcionales (EARS)

### RF-001

La auditoría DEBE declarar en el informe la base normativa empleada, distinguiendo los documentos tomados como norma, los documentos de referencia excluidos y los artefactos usados solo como evidencia de la práctica, y DEBE acompañar el inventario real de documentos normativos con su recuento en la fecha de corte.

### RF-002

La auditoría DEBE aplicar la jerarquía normativa declarada en `docs/constitution.md`, manteniendo `docs/constitution.md` y `AGENTS.md` por encima de la base normativa documental de `docs/sdd/`. La exclusión de un documento que la constitución declara de rango normativo DEBE registrarse como hallazgo de la dimensión D1 y NO DEBE resolverse alterando la jerarquía declarada ni reemplazando el criterio de conformidad con el documento excluido.

### RF-003

La auditoría DEBE evaluar las diez dimensiones D1 a D10 y DEBE emitir un veredicto independiente por dimensión.

### RF-004

CUANDO la auditoría evalúe la dimensión D4, DEBE registrar por cada compuerta G1 a G6 una entrada que declare la condición de superación, la evidencia observada, el declarante de la aprobación y el resultado de la verificación.

### RF-005

CUANDO la auditoría evalúe la dimensión D5, DEBE recorrer la cadena completa RF/CB → CA → T → evidencia → commit → merge → release en cada spec publicada y DEBE registrar cada eslabón ausente o inconsistente.

### RF-006

La auditoría DEBE revisar de forma retrospectiva e individualizada las specs SPEC-001 a SPEC-007 y DEBE emitir un veredicto por spec.

### RF-007

La auditoría DEBE registrar cada hallazgo con un identificador AUD-NNN único, la dimensión asociada, el veredicto, la severidad, la norma incumplida y la evidencia que lo sostiene.

### RF-008

La auditoría DEBE citar la evidencia de cada hallazgo como referencia de archivo con número de línea o como resultado observable de una consulta ejecutada durante la auditoría.

### RF-009

La auditoría DEBE declarar la fecha de corte, el identificador del commit auditado y la relación de comandos o consultas ejecutados, de modo que un tercero pueda reproducir cada verificación.

### RF-010

La auditoría DEBE declarar la escala de veredicto de cinco valores, la escala de severidad de cuatro niveles y la regla de agregación con la que se obtiene el veredicto global.

### RF-011

La auditoría DEBE emitir un veredicto global congruente con los veredictos por dimensión y con la severidad de los hallazgos registrados.

### RF-012

CUANDO la auditoría concluya la evaluación, DEBE emitir una hoja de ruta priorizada organizada en los bloques B1 base normativa, B2 mecanismo de control, B3 práctica operativa y B4 trazabilidad profunda.

### RF-013

La hoja de ruta DEBE asignar a cada remediación una clasificación entre editorial, requiere spec y proceso, junto con la referencia del hallazgo AUD-NNN que la origina.

### RF-014

La auditoría NO DEBE modificar, corregir, renombrar ni eliminar artefactos auditados, y su única escritura DEBE ser el informe de auditoría.

### RF-015

La auditoría NO DEBE evaluar la calidad técnica del código, el rendimiento, los benchmarks ni la revisión interna del validador determinista.

### RF-016

La auditoría DEBE registrar una sección de limitaciones con cada elemento calificado NO VERIFICABLE, la causa de la imposibilidad y el artefacto que faltaría para verificarlo.

### RF-017

La auditoría DEBE registrar las desviaciones de Git observadas en el periodo auditado con su referencia observable y NO DEBE corregirlas.

### RF-018

MIENTRAS la auditoría evalúe la dimensión D6, DEBE contrastar cada estado observado en las specs con el modelo de estados declarado y DEBE registrar cada transición no permitida.

### RF-019

MIENTRAS la auditoría evalúe la dimensión D7, DEBE contrastar los permisos declarados por rol con las operaciones registradas en la evidencia del periodo auditado.

## Requisitos no funcionales

### RNF-001

El informe DEBE redactarse en español y en formato Markdown dentro de `docs/sdd/auditoria_cumplimiento_sdd.md` como documento único.

### RNF-002

Cada afirmación de conformidad o de incumplimiento DEBE estar sostenida por evidencia citada, y la auditoría NO DEBE emitir veredictos fundados en apreciación sin evidencia.

### RNF-003

La verificación DEBE ser reproducible por un tercero a partir del commit, la fecha de corte y los comandos declarados, sin depender de sesiones previas ni de la memoria de la auditoría.

### RNF-004

Dos auditorías independientes sobre el mismo commit DEBEN obtener el mismo veredicto por dimensión y la misma severidad por hallazgo.

### RNF-005

Los identificadores AUD-NNN DEBEN ser únicos, ordenados por dimensión y no reutilizarse entre versiones del informe.

### RNF-006

El informe DEBE mantener correspondencia completa entre hallazgos y remediaciones: cada hallazgo DEBE tener al menos una remediación asignada y cada remediación DEBE referenciar el hallazgo que la origina.

### RNF-007

El informe DEBE incluir una tabla consolidada de hallazgos con dimensión, severidad y veredicto que permita el recuento determinista de los resultados.

## Casos borde

### CB-001

SI un artefacto exigido por la base normativa no existe o está incompleto en el periodo auditado, ENTONCES la auditoría DEBE calificar el punto como NO VERIFICABLE, citar la ausencia como evidencia y NO DEBE crear el artefacto.

### CB-002

SI una spec publicada no permite reconstruir la cadena de trazabilidad hasta su release, ENTONCES la auditoría DEBE registrar el eslabón faltante como hallazgo de D5 y NO DEBE completar la cadena con inferencias.

### CB-003

SI la evidencia histórica de una compuerta no se conserva en el repositorio, ENTONCES la auditoría DEBE calificar la verificación de esa compuerta como NO VERIFICABLE y NO DEBE presumir su cumplimiento por la existencia del estado liberado.

### CB-004

SI dos documentos de la base normativa se contradicen entre sí, ENTONCES la auditoría DEBE registrar la contradicción como hallazgo, indicar el rango de cada documento y la resolución aplicable según la jerarquía, sin editar documento alguno.

### CB-005

SI el resultado del validador determinista diverge de la norma documental, ENTONCES la auditoría DEBE registrar la divergencia como hallazgo de D2 o de D10 y DEBE tratar el validador como evidencia de la práctica.

### CB-006

SI la auditoría detecta una desviación de Git en el periodo auditado, ENTONCES DEBE registrarla con la referencia observable y NO DEBE reescribir el historial ni eliminar la evidencia.

### CB-007

SI la auditoría encuentra un documento de `docs/sdd/` excluido de la base normativa, ENTONCES DEBE clasificarlo como referencia y NO DEBE emplearlo como criterio de conformidad.

### CB-008

SI una dimensión carece de objeto evaluable en el periodo auditado, ENTONCES la auditoría DEBE calificarla NO APLICA y DEBE justificar la ausencia de objeto.

### CB-009

SI el inventario de documentos declarado en la norma no coincide con el inventario real de `docs/sdd/`, ENTONCES la auditoría DEBE registrar la diferencia como hallazgo de D1 y NO DEBE corregir el inventario declarado.

### CB-010

SI durante la auditoría se solicita corregir un artefacto auditado, ENTONCES la auditoría DEBE rechazar la corrección y DEBE remitirla a una especificación posterior.

### CB-011

SI la base normativa de la auditoría excluye un documento que `docs/constitution.md` declara de rango normativo, ENTONCES la auditoría DEBE registrar la tensión como hallazgo de D1 y NO DEBE resolverla alterando la jerarquía declarada.

### CB-012

SI el árbol de trabajo contiene cambios sin registrar o no existe un commit de corte fijado, ENTONCES la auditoría DEBE fijar el commit de corte antes de escribir el informe, DEBE excluir del periodo auditado los cambios no registrados y DEBE consignarlos como evidencia de las dimensiones D9 y D10.

## Fuera de alcance

- Corregir, remediar o cerrar los hallazgos detectados, que corresponde a una especificación posterior por cada bloque de la hoja de ruta.
- Modificar `docs/sdd/`, `docs/constitution.md`, `AGENTS.md`, `specs/`, `CHANGELOG.md` o cualquier artefacto auditado.
- Evaluar la calidad técnica del código, el rendimiento de los modelos, los benchmarks de hardware o la cobertura de pruebas de los scripts de ejecución.
- Auditar la lógica interna del validador determinista, sus pruebas unitarias o su diseño.
- Auditar el contenido del repositorio oficial de llama.cpp o cualquier artefacto excluido de Git.
- Auditar repositorios ajenos, bifurcaciones personales o configuraciones remotas de terceros.
- Establecer la política de aprobaciones, la jerarquía normativa o el flujo Git, que se limitan a verificar contra la norma vigente.
- Ejecutar la auditoría, que corresponde a la etapa de implementación de esta especificación.

## Criterios de aceptación

### CA-001

`DADO el repositorio con su corpus documental, CUANDO se revisa la sección inicial del informe, ENTONCES el informe enumera los documentos tomados como norma, los seis documentos de referencia excluidos y los artefactos usados como evidencia, declara el inventario real de documentos normativos con su recuento en la fecha de corte, mantiene la constitución y AGENTS.md por encima de la base documental y no emplea documentos excluidos como criterio de conformidad.`

Cubre: `RF-001`, `RF-002`, `CB-007`, `CB-011`.

### CA-002

`DADO el alcance declarado de la auditoría, CUANDO se revisa el cuerpo del informe, ENTONCES aparecen las diez dimensiones D1 a D10, cada una con su veredicto propio tomado de la escala de cinco valores.`

Cubre: `RF-003`.

### CA-003

`DADO el periodo auditado, CUANDO se revisa la dimensión D4, ENTONCES cada compuerta G1 a G6 presenta una entrada con condición, evidencia citada, declarante de la aprobación y resultado de la verificación, y las compuertas sin evidencia conservada quedan calificadas NO VERIFICABLE sin presunción de cumplimiento.`

Cubre: `RF-004`, `CB-003`.

### CA-004

`DADO cada spec publicada, CUANDO se revisa la dimensión D5, ENTONCES la cadena RF/CB → CA → T → evidencia → commit → merge → release se recorre completa y cada eslabón ausente aparece como hallazgo, sin completar la cadena por inferencia.`

Cubre: `RF-005`, `CB-002`.

### CA-005

`DADO el conjunto SPEC-001 a SPEC-007, CUANDO se revisa la revisión retrospectiva, ENTONCES cada spec presenta su veredicto individual y los artefactos inexistentes o incompletos quedan citados como ausencia verificable sin crear el artefacto.`

Cubre: `RF-006`, `CB-001`.

### CA-006

`DADO un hallazgo registrado, CUANDO se revisa su entrada, ENTONCES contiene un identificador AUD-NNN único, la dimensión, el veredicto, la severidad, la norma incumplida y la evidencia citada con referencia de archivo y línea o con resultado observable de una consulta.`

Cubre: `RF-007`, `RF-008`.

### CA-007

`DADO el informe entregado, CUANDO un tercero consulta la cabecera de reproducibilidad, ENTONCES encuentra la fecha de corte, el identificador del commit auditado fijado antes de la escritura del informe y la relación de comandos o consultas ejecutados, suficientes para repetir cada verificación, y los cambios no registrados en ese commit quedan fuera del periodo auditado y consignados como evidencia de las dimensiones D9 y D10.`

Cubre: `RF-009`, `CB-012`.

### CA-008

`DADO el informe entregado, CUANDO se revisa la escala y el cierre, ENTONCES declara los cinco valores de veredicto, los cuatro niveles de severidad y la regla de agregación aplicada, y el veredicto global resulta congruente con los veredictos por dimensión, incluida la calificación NO APLICA de las dimensiones sin objeto evaluable.`

Cubre: `RF-010`, `RF-011`, `CB-008`.

### CA-009

`DADO el cierre de la auditoría, CUANDO se revisa la hoja de ruta, ENTONCES aparece organizada en los bloques B1 base normativa, B2 mecanismo de control, B3 práctica operativa y B4 trazabilidad profunda, con cada remediación clasificada como editorial, requiere spec o proceso y vinculada al hallazgo que la origina.`

Cubre: `RF-012`, `RF-013`.

### CA-010

`DADO el repositorio antes y después de la auditoría, CUANDO se compara el estado con la fecha de corte, ENTONCES el único archivo creado o modificado es el informe de auditoría y toda solicitud de corrección de un artefacto auditado queda rechazada y remitida a una especificación posterior.`

Cubre: `RF-014`, `CB-010`.

### CA-011

`DADO el informe entregado, CUANDO se revisa su contenido, ENTONCES no contiene evaluación de calidad técnica del código, de rendimiento, de benchmarks ni de la lógica interna del validador determinista.`

Cubre: `RF-015`.

### CA-012

`DADO el informe entregado, CUANDO se revisa la sección de limitaciones, ENTONCES cada elemento NO VERIFICABLE aparece con la causa de la imposibilidad y el artefacto que faltaría para verificarlo.`

Cubre: `RF-016`.

### CA-013

`DADO el historial de Git del periodo auditado, CUANDO se revisa la dimensión D9, ENTONCES cada desviación observada aparece registrada con su referencia observable y el historial permanece sin reescritura ni eliminación de evidencia.`

Cubre: `RF-017`, `CB-006`.

### CA-014

`DADO el modelo de estados declarado, CUANDO se revisa la dimensión D6, ENTONCES cada estado observado en las specs se contrasta con el modelo y cada transición no permitida figura como hallazgo.`

Cubre: `RF-018`.

### CA-015

`DADO el cuadro de roles y permisos declarado, CUANDO se revisa la dimensión D7, ENTONCES los permisos de cada rol se contrastan con las operaciones registradas y las diferencias figuran como hallazgo.`

Cubre: `RF-019`.

### CA-016

`DADO un resultado del validador determinista contrario a la norma documental, CUANDO se revisa el informe, ENTONCES la divergencia aparece como hallazgo de D2 o de D10 y el validador queda tratado como evidencia de la práctica.`

Cubre: `CB-005`.

### CA-017

`DADO dos documentos de la base normativa con disposiciones contradictorias, CUANDO se revisa el informe, ENTONCES la contradicción aparece como hallazgo con el rango de cada documento y la resolución aplicable según la jerarquía, sin edición de los documentos.`

Cubre: `CB-004`.

### CA-018

`DADO el inventario declarado de documentos normativos, CUANDO se contrasta con el contenido real de docs/sdd/, ENTONCES cualquier diferencia de recuento aparece como hallazgo de D1 y el inventario declarado permanece sin corrección.`

Cubre: `CB-009`.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial |
| 0.2.0 | 2026-11-14 | Clarificación: base normativa por regla de inclusión con recuento delegado al informe (AMB-001), exclusión de rango normativo registrada y no resuelta (AMB-002, AMB-006), commit de corte fijado antes del informe (AMB-003), nuevo caso borde CB-012 y cobertura ampliada en CA-001 y CA-007 |
| 0.3.0 | 2026-11-14 | Plan técnico: arquitectura del informe en doce secciones, modelo de evidencia, esquemas de tablas, regla de agregación y estrategia de verificación documental (DEC-001 a DEC-010); estado `planned` |
| 0.4.0 | 2026-11-14 | Tareas: descomposición en 26 tareas atómicas con dependencias acíclicas, archivos, estimación y validación; regla de ejecución con `documenter` como implementador y `planner` como registrador de casillas y evidencia; estado `tasked` |
