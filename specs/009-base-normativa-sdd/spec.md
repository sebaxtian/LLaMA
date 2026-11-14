---
id: SPEC-009
title: Nueva base normativa SDD
status: clarified
version: 0.2.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/base-normativa-sdd-v2
release: ""
supersedes: ""
superseded_by: ""
---

# Nueva base normativa SDD

## Contexto y objetivo

El informe `docs/sdd/auditoria_cumplimiento_sdd.md` emite veredicto global `NO CONFORME` y concentra en el bloque B1 los defectos de autoridad normativa: diecisiete documentos del corpus se autodeclaran no normativos mientras la base les atribuye fuerza, el procedimiento ejecutable queda excluido del criterio de conformidad, las guías contradicen a las plantillas en la forma de los criterios de aceptación y en la anchura de los identificadores de casos borde, el índice no cubre el corpus y el recuento declarado no coincide con el árbol, la documentación analítica carece de contrato y la versión de las specs no se deriva de regla alguna.

Objetivo: sustituir la base normativa vigente por una base v2 con un mapa único de autoridad, un protocolo operativo autosuficiente y un conjunto de documentos alineados entre sí, de modo que cualquier lector resuelva una regla sin ambigüedad y sin consultar documentos que declaran no ser norma.

Resultado esperado: siete rangos declarados, plantillas reconocidas como norma, guías e informes reconocidos como referencia, protocolo operativo v2 con las dieciséis secciones de su contenido mínimo, registro único de aprobaciones, contratos de informe analítico y de informe de auditoría, regla de versionado de specs, índice completo del corpus y auditoría de conformidad exigida antes de cada release menor.

El recuento de diecisiete documentos citado en el primer párrafo describe el corte de la auditoría y no fija un recuento para la base v2: el inventario vigente se calcula desde el índice del corpus (RF-018).

La nueva base rige desde su integración. Esta spec se redacta con la base vigente y no implementa los bloques B2, B3 ni B4 del informe de auditoría.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** aprueba G1, G4 y G6 mediante commit firmado con su clave; no delega la firma ni la emisión de compuertas.
- **Agente `planner`:** redacta los artefactos de la spec; no los aprueba ni modifica requisitos para ajustarlos a una implementación.
- **Agente `documenter`:** aplica correcciones editoriales dentro de `docs/`; no aprueba compuertas.
- **Rol de auditoría:** lee la base normativa completa y redacta el informe de auditoría; no modifica requisitos ni aprueba compuertas.
- **Agente `coder`:** implementa tareas de una spec aprobada; no modifica la base normativa.
- **Agente `reviewer`:** verifica conformidad y evidencia; no aprueba compuertas.
- **Validador:** comprueba estructura y devuelve un código de salida; un resultado favorable declara solo el alcance escrito en su contrato.

## Contenido mínimo del protocolo operativo v2

| # | Sección exigida | Materia |
|---|---|---|
| 1 | Objeto, ámbito y rango | A qué obliga el protocolo y sobre qué documentos |
| 2 | Mapa de autoridad y precedencia | Rangos, carácter y regla de resolución de conflictos |
| 3 | Modelo SDD y glosario | Términos con un único significado |
| 4 | Ciclo de siete etapas | Entrada, salida, artefacto, estado, responsable y comando por etapa |
| 5 | Máquina de estados | Tabla de transiciones, propietario y evidencia |
| 6 | Compuertas G1 a G6 | Condición, evidencia, declarante, verificación y acción ante fallo |
| 7 | Trazabilidad obligatoria | Campos exigidos por artefacto |
| 8 | Contratos de artefactos | Spec, clarify, plan, tasks, reporte de validación, informe analítico e informe de auditoría |
| 9 | Identificadores y versionado | Espacio de identificadores y regla de versión de specs |
| 10 | EARS y léxico prohibido | Patrones admitidos y términos vetados |
| 11 | Aprobaciones | Formato, autoría por commit firmado, sección protegida y prohibición de autoaprobación |
| 12 | Roles y permisos | Matriz de capacidades por rol |
| 13 | Integración Git y release | Compuertas del flujo, eliminación de ramas y verificación de tags |
| 14 | Contrato del validador | Alcance verificado y alcance no verificado |
| 15 | Excepciones | Cambio editorial y cláusula de legado |
| 16 | Control de cambios y auditoría de conformidad | Cambios de la propia base y auditoría previa al release menor |

## Requisitos funcionales (EARS)

### RF-001

El repositorio DEBE declarar un único mapa de autoridad con los siete rangos siguientes: constitución, reglas operativas de agentes, protocolo operativo, flujo Git, plantillas, contrato de la feature y código.

### RF-002

El repositorio DEBE declarar, para cada documento de la base normativa, su rango y su carácter de norma o de referencia, sin excepción.

### RF-003

El mapa de autoridad DEBE declararse en tres niveles: `docs/constitution.md` §6 fija la jerarquía suprema, `docs/sdd/PROTOCOLO_OPERATIVO.md` §2 la desarrolla con la tabla de rangos y carácter, y `docs/sdd/README.md` la reproduce como índice de navegación. SI dos documentos del mismo rango se contradicen, ENTONCES el índice DEBE declarar el orden de precedencia dentro de ese rango, ese orden DEBE actuar como desempate y el trabajo DEBE detenerse hasta corregir el documento superior.

### RF-004

El corpus de guías, los informes de análisis y los informes de auditoría DEBEN declarar su carácter de referencia no normativa y NO DEBEN establecer reglas de obligado cumplimiento.

### RF-005

Las plantillas de `docs/sdd/plantillas/` DEBEN prevalecer sobre las guías y NO DEBEN admitir dos formas incompatibles para un mismo campo.

### RF-006

El protocolo operativo DEBE definir por sí mismo cada regla de obligado cumplimiento y NO DEBE remitir a una guía ni a un informe para fijar esa regla.

### RF-007

CUANDO se publique la base v2, el repositorio DEBE contener un protocolo operativo nuevo, redactado desde cero, y NO DEBE obtenerlo por edición incremental del protocolo vigente.

### RF-008

El repositorio DEBE conservar `docs/constitution.md` como norma suprema, DEBE declarar el mecanismo de aprobación de sus cambios y DEBE exigir que esa aprobación se verifique por commit firmado con la clave del propietario.

### RF-009

`AGENTS.md` DEBE contener entre 30 y 70 líneas útiles, DEBE limitarse a reglas operativas de agentes y NO DEBE reproducir el contenido del protocolo operativo.

### RF-010

El flujo Git DEBE declarar la compuerta que autoriza la integración y la compuerta que autoriza el release, DEBE fijar la eliminación de la rama de trabajo después de la integración y NO DEBE admitir una integración sin compuerta cumplida.

### RF-011

CUANDO se publique un release, el flujo Git DEBE exigir la sincronización de `dev` con `main`, DEBE exigir la verificación del tag anotado con el formato `vMAJOR.MINOR.PATCH` y DEBE registrar el resultado de esa verificación.

### RF-012

El repositorio DEBE registrar G1 y G4 en `spec.md` y G6 en `CHANGELOG.md`, DEBE verificar la autoría de esas tres compuertas por commit firmado y NO DEBE admitir casilla de aprobación en el reporte de validación.

### RF-013

Las plantillas de tareas DEBEN incluir, por cada tarea, el criterio de aceptación que la origina y un campo de evidencia de ejecución.

### RF-014

El repositorio DEBE declarar el contrato del informe analítico con sus secciones obligatorias y el rol habilitado para redactarlo.

### RF-015

El repositorio DEBE declarar el contrato del informe de auditoría con sus secciones obligatorias, la escala de veredicto y la regla de numeración de hallazgos.

### RF-016

El repositorio DEBE declarar una única regla de versionado de specs derivada del alcance del cambio y DEBE aplicarla al historial de cambios de cada spec. La regla DEBE fijar la versión 0.1.0 para la redacción inicial, un incremento MINOR por cada etapa que cambie el contrato (clarify, plan, tasks y validación), un incremento PATCH para correcciones editoriales que no cambien requisitos, un incremento MINOR con motivo registrado para la reapertura de una spec en estado `validated`, y la prohibición de renumerar una spec en estado `released`, cuyos cambios posteriores se tramitan por reapertura o por spec nueva.

### RF-017

El repositorio DEBE ofrecer un índice del corpus que liste cada documento de `docs/sdd/` con su carácter y su orden de lectura, y que cubra la totalidad de archivos presentes: los de la raíz de `docs/sdd/`, los de `docs/sdd/plantillas/`, los informes de análisis y el informe de auditoría.

### RF-018

El repositorio DEBE declarar la regla de inclusión de documentos en la base normativa y NO DEBE fijar un recuento de documentos; el inventario DEBE calcularse en el índice.

### RF-019

El repositorio DEBE declarar un rol de auditoría con permiso de lectura sobre la base normativa completa, sin permiso de modificar requisitos y sin permiso de aprobar compuertas. El rol DEBE declararse en la base v2, en el protocolo operativo v2 y en `AGENTS.md`; su implementación en `.opencode/` corresponde al bloque B3 y queda fuera del alcance de esta spec.

### RF-020

El repositorio DEBE declarar el procedimiento de control de cambios aplicable a la propia base normativa, con spec previa, versión del documento y registro en `CHANGELOG.md`.

### RF-021

CUANDO se prepare un release menor, el repositorio DEBE ejecutar una auditoría de conformidad, DEBE conservar su informe y NO DEBE otorgar G6 sin ese informe.

### RF-022

El repositorio DEBE declarar una cláusula de legado para las specs publicadas `SPEC-001` a `SPEC-007` y DEBE remitir su regularización a una spec posterior.

### RF-023

Los documentos de la base DEBEN declarar el mismo conjunto de compuertas, estados, roles y rutas, y una divergencia entre ellos NO DEBE quedar sin resolución por rango.

### RF-024

CUANDO la base v2 se integre, el repositorio DEBE registrar la transición desde la base vigente con la fecha, el alcance y el estado de cada documento sustituido. Los documentos de la base v2 sustituyen a los vigentes en las mismas rutas: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md`, `README.md`, `MEMORY.md`, `docs/sdd/README.md` y `docs/sdd/plantillas/`. El registro DEBE declararse en un anexo del protocolo operativo v2 y en `CHANGELOG.md` bajo `Unreleased`, y las versiones anteriores DEBEN permanecer en el historial Git.

### RF-025

El protocolo operativo v2 DEBE contener las dieciséis secciones del contenido mínimo declarado en esta spec.

### RF-026

El protocolo operativo v2 DEBE fijar la notación EARS, el espacio de identificadores con tres dígitos y la lista de léxico prohibido en los requisitos.

### RF-027

El protocolo operativo v2 DEBE declarar la máquina de estados con la tabla de transiciones, el propietario de cada transición y la evidencia que la habilita.

### RF-028

El repositorio DEBE registrar la decisión de archivar la rama `feat/gemma-4-26b-a4b-it-qat-gguf` sin integrarla, DEBE excluir esa rama de la integración y DEBE declarar que permanece local sin publicarse. La decisión DEBE inscribirse en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición del protocolo operativo v2.

## Requisitos no funcionales

### RNF-001

El repositorio DEBE redactar cada regla de la base con una condición observable y una respuesta única, de modo que dos lectores independientes alcancen la misma decisión.

### RNF-002

Mientras un lector consulte la base normativa, el repositorio DEBE permitir resolver una regla sin abrir un documento de referencia no normativa.

### RNF-003

El repositorio DEBE redactar la base normativa en español y DEBE mantener el formato de cada documento legible en texto plano.

### RNF-004

El repositorio DEBE mantener estable el espacio de identificadores: NO DEBE reutilizar un identificador `SPEC-NNN` ni renumerar un requisito ya publicado.

### RNF-005

El repositorio DEBE declarar en el protocolo el alcance exacto del validador y NO DEBE presentar un resultado favorable del validador como conformidad del régimen completo.

### RNF-006

CUANDO se sustituya la base vigente, el repositorio NO DEBE perder ninguna regla de la constitución, de `AGENTS.md` ni del flujo Git que permanezca aplicable.

## Casos borde

### CB-001

SI dos documentos del mismo rango se contradicen y el índice no declara su orden, ENTONCES el repositorio DEBE detener el trabajo y DEBE registrar la contradicción como defecto de la base.

### CB-002

SI un documento de `docs/sdd/` no declara rango ni carácter, ENTONCES el repositorio DEBE tratarlo como defecto de conformidad y NO DEBE usarlo para decidir una regla.

### CB-003

SI una spec publicada no satisface la base v2, ENTONCES el repositorio DEBE aplicar la cláusula de legado, DEBE conservar su contenido y NO DEBE reescribirla retroactivamente.

### CB-004

SI la aprobación de G1, G4 o G6 carece de commit firmado con la clave del propietario, ENTONCES el repositorio DEBE considerar la compuerta no aprobada.

### CB-005

SI el commit que introduce la línea de aprobación de una compuerta no está firmado por una clave de la lista de firmantes autorizados del propietario, o la firma no verifica, ENTONCES el repositorio DEBE considerar la compuerta no aprobada y DEBE registrar la aprobación como incumplimiento.

### CB-006

SI el recuento de documentos citado en un documento de la base no coincide con el inventario del índice, ENTONCES el repositorio DEBE aplicar el inventario del índice y DEBE corregir el recuento citado.

### CB-007

SI una guía contradice una plantilla, ENTONCES el repositorio DEBE aplicar la plantilla y DEBE corregir la guía.

### CB-008

SI el protocolo remite a una guía para fijar una regla, ENTONCES el repositorio DEBE registrar el defecto de autosuficiencia y DEBE corregirlo en la revisión siguiente de la base.

### CB-009

SI un release menor se prepara sin informe de auditoría de conformidad registrado, ENTONCES el repositorio NO DEBE emitir G6.

### CB-010

SI un cambio de la base normativa se propone sin spec aprobada, ENTONCES el repositorio NO DEBE integrarlo y DEBE tratar el cambio como incumplimiento.

### CB-011

SI una rama archivada conserva commits no integrados, ENTONCES el repositorio DEBE registrar la decisión de archivo en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición del protocolo operativo v2, DEBE mantener la rama local sin publicar, DEBE conservar la referencia y NO DEBE integrar esos commits.

### CB-012

SI se incorpora un documento nuevo a `docs/sdd/` sin entrada en el índice, ENTONCES el repositorio DEBE registrar la navegación incompleta y DEBE actualizar el índice antes de aprobar la compuerta en curso.

### CB-013

SI el historial de una spec publicada contiene versiones no derivadas de una regla, ENTONCES el repositorio DEBE conservar esas versiones y DEBE regularizarlas en la spec posterior de legado.

## Fuera de alcance

- La implementación de los bloques B2 (mecanismo de control), B3 (práctica operativa) y B4 (trazabilidad profunda) del informe de auditoría.
- La implementación del rol de auditoría en `.opencode/`: la base v2, el protocolo operativo y `AGENTS.md` lo declaran, y su materialización corresponde a B3.
- La reforma del validador: su contrato se declara en esta spec y su cambio corresponde a B2.
- La reescritura de las specs publicadas `SPEC-001` a `SPEC-007`: su regularización corresponde a la spec de legado.
- La modificación de la configuración de agentes, comandos y habilidades del proyecto.
- Los parámetros de hardware, las cuantizaciones y los benchmarks de modelos.

## Criterios de aceptación

### CA-001

DADO el mapa de autoridad de la base v2, CUANDO un lector consulta el rango de un documento, ENTONCES encuentra el documento, su rango y su carácter en una sola tabla y sin documento adicional.

Cubre: `RF-001`, `RF-002`, `CB-002`.

### CA-002

DADO un conflicto entre dos documentos del mismo rango, CUANDO se aplica el orden de precedencia que el índice declara dentro de ese rango, ENTONCES la resolución queda determinada por ese orden y el trabajo se detiene hasta corregir el documento superior.

Cubre: `RF-003`, `CB-001`.

### CA-003

DADO un documento de referencia que contradice a una plantilla, CUANDO se decide la regla aplicable, ENTONCES prevalece la plantilla y la contradicción queda registrada como defecto corregible.

Cubre: `RF-004`, `RF-005`, `CB-007`.

### CA-004

DADO el protocolo operativo v2, CUANDO se busca la definición de una regla de obligado cumplimiento, ENTONCES la regla aparece definida en el protocolo sin remisión a una guía y el documento se reconoce como redacción nueva.

Cubre: `RF-006`, `RF-007`, `CB-008`.

### CA-005

DADO el índice de secciones del protocolo v2, CUANDO se contrasta con el contenido mínimo declarado, ENTONCES las dieciséis secciones están presentes, con la notación EARS, el espacio de identificadores y la máquina de estados declarados.

Cubre: `RF-025`, `RF-026`, `RF-027`.

### CA-006

DADO un cambio en `docs/constitution.md`, CUANDO se verifica su aprobación, ENTONCES el commit que introduce la línea de aprobación está firmado por una clave de la lista de firmantes autorizados del propietario, la firma verifica y, en su ausencia, la compuerta no se considera aprobada.

Cubre: `RF-008`, `CB-004`, `CB-005`.

### CA-007

DADO `AGENTS.md`, CUANDO se cuentan sus líneas útiles, ENTONCES el resultado está entre 30 y 70 y el contenido se limita a reglas operativas sin reproducir el protocolo.

Cubre: `RF-009`.

### CA-008

DADO el flujo Git descrito en `docs/Flujo_de_Trabajo_Git.md`, CUANDO se publica un release, ENTONCES la integración y el release remiten a su compuerta, la rama de trabajo queda eliminada y el tag anotado queda verificado con `dev` sincronizada con `main`.

Cubre: `RF-010`, `RF-011`.

### CA-009

DADO el registro de aprobaciones de una spec, CUANDO se busca la compuerta G4, ENTONCES aparece en `spec.md` y no en el reporte de validación, y G6 aparece en `CHANGELOG.md`.

Cubre: `RF-012`.

### CA-010

DADO el contrato de tareas de una plantilla, CUANDO se revisa una tarea, ENTONCES incluye su criterio de aceptación y un campo de evidencia.

Cubre: `RF-013`.

### CA-011

DADO un informe analítico y un informe de auditoría, CUANDO se contrastan con su contrato, ENTONCES cada uno declara sus secciones obligatorias y el informe de auditoría declara la escala de veredicto y la regla de numeración de hallazgos.

Cubre: `RF-014`, `RF-015`.

### CA-012

DADO el rol de auditoría, CUANDO se contrasta con sus permisos declarados, ENTONCES conserva lectura sobre la base, carece de permiso de edición de requisitos, carece de permiso de aprobación, figura declarado en la base v2, en el protocolo operativo v2 y en `AGENTS.md`, y su implementación en `.opencode/` queda asignada al bloque B3.

Cubre: `RF-019`.

### CA-013

DADO el historial de cambios de una spec, CUANDO se aplica la regla de versionado, ENTONCES la redacción inicial figura como 0.1.0, cada etapa que cambió el contrato figura con incremento MINOR, cada corrección editorial figura con incremento PATCH y dos revisiones independientes obtienen el mismo número de versión.

Cubre: `RF-016`, `CB-013`.

### CA-014

DADO el índice de `docs/sdd/`, CUANDO se contrasta con el árbol de archivos, ENTONCES cada archivo de la raíz de `docs/sdd/`, de `docs/sdd/plantillas/` y cada informe de análisis y de auditoría aparece con su carácter y su orden de lectura, y el recuento se obtiene del índice.

Cubre: `RF-017`, `RF-018`, `CB-006`, `CB-012`.

### CA-015

DADO un release menor, CUANDO se revisa la evidencia de G6, ENTONCES existe informe de auditoría de conformidad registrado y el cambio de la base tiene spec aprobada.

Cubre: `RF-020`, `RF-021`, `CB-009`, `CB-010`.

### CA-016

DADA una spec publicada con anterioridad a la base v2, CUANDO se evalúa su conformidad, ENTONCES la cláusula de legado la ampara, su contenido se conserva y su regularización queda remitida a la spec posterior.

Cubre: `RF-022`, `CB-003`.

### CA-017

DADOS dos documentos de la base v2, CUANDO se comparan sus compuertas, estados, roles y rutas, ENTONCES los cuatro conjuntos coinciden.

Cubre: `RF-023`.

### CA-018

DADA la integración de la base v2, CUANDO se consulta el anexo de transición del protocolo v2 y la entrada de `CHANGELOG.md` bajo `Unreleased`, ENTONCES el registro declara la fecha, el alcance y el estado de cada documento sustituido, y las versiones anteriores permanecen en el historial Git.

Cubre: `RF-024`.

### CA-019

DADA la rama `feat/gemma-4-26b-a4b-it-qat-gguf`, CUANDO se consulta su estado, ENTONCES aparece archivada sin integrar, con la decisión registrada en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición, permanece local sin publicarse y no hay commits de esa rama en `dev`.

Cubre: `RF-028`, `CB-011`.

## Trazabilidad con el informe de auditoría

| Hallazgo | Requisitos que lo resuelven |
|---|---|
| `AUD-001` | `RF-002`, `RF-004` |
| `AUD-002` | `RF-001`, `RF-006`, `RF-023` |
| `AUD-003` | `RF-005`, `RF-013` |
| `AUD-004` | `RF-026` |
| `AUD-005` | `RF-013`, `RF-025` |
| `AUD-006` | `RF-003`, `RF-017` |
| `AUD-007` | `RF-018` |
| `AUD-023` | `RF-014`, `RF-019` |
| `AUD-055` | `RF-016` |
| `AUD-093` | `RF-017` |

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [ ] G1: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-14 | Clarificación: mapa de autoridad en tres niveles, autoría frente a propiedad, sustitución y transición, rol de auditoría, alcance del índice, versionado de specs, archivo de la rama Gemma y recuento histórico |
