# Plan técnico — SPEC-009

## Referencias

- `spec.md`: `SPEC-009`, versión 0.2.0, estado `clarified`, compuerta G1 aprobada por `Agent Sebaxtian` en el commit firmado `f6faa3b` (2026-11-14).
- `clarify.md`: `SPEC-009`, cerrado con `AMB-001` a `AMB-008` resueltos y parches aplicados a `spec.md`.
- `docs/constitution.md`: norma suprema vigente; su §6 fija la jerarquía que esta base sustituye.
- `AGENTS.md`: reglas operativas vigentes de rango 2.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma ejecutable vigente de rango 3; se sustituye por redacción nueva (`RF-007`).
- `docs/Flujo_de_Trabajo_Git.md`: procedimiento Git de rango 4; se alinea con G5 y G6.
- `docs/sdd/README.md`: índice del corpus vigente; pasa a declarar el orden de precedencia dentro de cada rango (`RF-003`).
- `docs/sdd/plantillas/`: plantillas vigentes de rango 5, incluidas las dos que se reforman por contrato (`RF-013`, `RF-012`).
- `docs/sdd/auditoria_cumplimiento_sdd.md`: informe de auditoría `SPEC-008`; su bloque B1 origina los requisitos de esta spec y su sección 10 fija la clasificación de remediaciones.
- `MEMORY.md`, `README.md`, `CHANGELOG.md`: documentos de raíz que se alinean con la base v2.
- Plantilla aplicada: `docs/sdd/plantillas/plan.md`.

## Naturaleza del entregable

La especificación no produce código de producción, componentes ejecutables ni suites nuevas. El entregable es un conjunto de documentos normativos en Markdown. Por esa razón este plan no describe módulos de software: describe la arquitectura documental, el contrato de cada documento, el modelo de aprobación, la transición desde la base vigente y la verificación documental.

Consecuencias operativas que el plan fija:

- La Etapa 6 escribe documentos; no crea archivos de prueba, no modifica `tools/` y no modifica `.opencode/` (DEC-013).
- La base v2 se publica por sustitución en la misma ruta. No conviven dos documentos vigentes para la misma materia (DEC-010).
- Cada documento declara su rango y su carácter en su propio encabezado. Un documento que omite esa declaración es un defecto de conformidad (`CB-002`).
- La verificación es documental: validador determinista, comprobaciones de contenido sobre el texto, control de alcance con Git y revisión independiente del rol `reviewer`.
- El plan no implementa los bloques B2, B3 ni B4 del informe de auditoría. Declara el mecanismo de firma y el contrato del validador, y atribuye su automatización a B2.

## Alcance documental de la Etapa 6

| # | Documento | Rango | Operación | Requisitos que impone |
|---|---|---|---|---|
| 1 | `docs/constitution.md` | 1 | Sustitución | `RF-001`, `RF-003`, `RF-008`, `RF-019`, `RF-020`, `RF-022` |
| 2 | `AGENTS.md` | 2 | Sustitución | `RF-009`, `RF-019` |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | Redacción desde cero y anexo de transición | `RF-006`, `RF-007`, `RF-024`, `RF-025`, `RF-026`, `RF-027`, `RF-028` |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | 4 | Sustitución alineada | `RF-010`, `RF-011` |
| 5 | `docs/sdd/plantillas/spec.md` | 5 | Sustitución | `RF-005`, `RF-012` |
| 6 | `docs/sdd/plantillas/clarify.md` | 5 | Sustitución | `RF-005` |
| 7 | `docs/sdd/plantillas/plan.md` | 5 | Sustitución | `RF-005` |
| 8 | `docs/sdd/plantillas/tasks.md` | 5 | Sustitución | `RF-013` |
| 9 | `docs/sdd/plantillas/validation_report.md` | 5 | Sustitución | `RF-012` |
| 10 | `docs/sdd/plantillas/informe_analitico.md` | 5 | Creación | `RF-014` |
| 11 | `docs/sdd/plantillas/informe_auditoria.md` | 5 | Creación | `RF-015` |
| 12 | `docs/sdd/README.md` | 5 como índice de navegación; contenido descriptivo como referencia | Sustitución | `RF-002`, `RF-017`, `RF-018`, `CB-012` |
| 13 | `docs/sdd/firmantes_autorizados` | Sin rango: registro de datos | Creación | `RF-008`, `CB-005` |
| 14 | `README.md` | Sin rango: referencia no normativa | Sustitución | — |
| 15 | `MEMORY.md` | Sin rango: referencia no normativa | Sustitución | — |
| 16 | `CHANGELOG.md` | Sin rango: registro de cambios y de G6 | Sustitución | `RF-012`, `RF-021`, `RF-024`, `RF-028` |

El documento 12 cumple dos funciones y su encabezado las declara: navegación del corpus y orden de precedencia dentro de cada rango. Su contenido descriptivo es referencia no normativa.

## Arquitectura documental

La base se organiza en siete rangos normativos y una categoría sin rango. El contenido del mapa es único y se declara en tres soportes: la constitución fija la jerarquía suprema, el protocolo la desarrolla con la tabla de rangos y carácter, y el índice la reproduce para navegación (DEC-001).

### Mapa de autoridad v2

| Rango | Documento | Carácter | Precedencia dentro del rango |
|---|---|---|---|
| 1 | `docs/constitution.md` | Norma suprema | Único documento del rango |
| 2 | `AGENTS.md` | Norma operativa para agentes | Único documento del rango |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | Norma ejecutable del proceso | Único documento del rango |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | Norma de integración y release | Único documento del rango |
| 5 | `docs/sdd/plantillas/*.md` | Norma de forma de cada artefacto | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md`, este sobre `validation_report.md`, este sobre `informe_analitico.md` y este sobre `informe_auditoria.md` |
| 6 | `specs/NNN-slug/*.md` | Contrato de la feature | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md` y este sobre `validation_report.md` |
| 7 | `src/`, `tools/`, `tests/`, `.opencode/` | Implementación verificable | El código no prevalece sobre norma alguna; su divergencia se corrige en el código |
| Sin rango | Guías de `docs/sdd/`, informes de análisis, informes de auditoría | Referencia no normativa | Sin precedencia: no fijan reglas (`RF-004`) |
| Sin rango | `README.md`, `MEMORY.md` | Descripción del estado | Sin precedencia: una divergencia se corrige en el documento descriptivo |
| Sin rango | `docs/sdd/README.md` | Navegación con función de desempate | Declara el orden de precedencia de cada rango (`RF-003`) |
| Sin rango | `CHANGELOG.md` | Registro de cambios y de G6 | Su función de registro de G6 es la única norma que porta (`RF-012`) |

Reglas de resolución que el mapa fija:

- Entre rangos distintos prevalece el de número menor.
- Dentro de un rango prevalece el documento que el índice sitúa antes (DEC-007).
- Una contradicción entre rangos, o dentro de un rango sin orden declarado, detiene el trabajo y se registra como defecto de la base (`CB-001`).
- La corrección se aplica siempre en el soporte de mayor rango y, después, en el de menor rango que quedó desalineado.

### Diagrama de dependencia normativa

```text
constitution.md (1)
  └─ AGENTS.md (2)
       └─ PROTOCOLO_OPERATIVO.md (3)
            ├─ Flujo_de_Trabajo_Git.md (4)
            ├─ plantillas/ (5)
            └─ specs/NNN-slug/ (6) ── código (7)
Índice: docs/sdd/README.md  → declara carácter y precedencia de cada rango
Registro: CHANGELOG.md      → transición y G6
Referencia: guías e informes → no fijan reglas
```

## Contratos de los documentos

Cada contrato fija secciones obligatorias, prohibiciones y la comprobación que lo verifica. El redactor no crea secciones fuera del contrato; el contenido auxiliar se ubica como subsección de la sección que lo emplea.

### `docs/constitution.md` (rango 1)

Diez secciones de nivel 2, en este orden:

| § | Sección | Contenido obligatorio | Requisitos |
|---|---|---|---|
| 1 | Identidad y misión | Qué es el proyecto, plataforma y caso de uso principal, adopción de SDD Spec-Anchored | `RF-001` |
| 2 | Principios innegociables | Especificación previa, determinismo, trazabilidad, aprobación por commit firmado, menor privilegio, verificabilidad | `RF-008` |
| 3 | Guardrails de archivos | `llama.cpp/` de solo lectura, `bin/` y `models/` sin contenido cruzado, `.env` protegido, `.gitkeep` conservados | — |
| 4 | Stack | Python para herramientas, `.bat` para ejecución, Git y Windows 11 | — |
| 5 | Estándares de calidad | TDD para Python, validación-first para `.bat`, longitud de `AGENTS.md` entre 30 y 70 líneas útiles, registro en `CHANGELOG.md`, idioma español | `RF-009` |
| 6 | Jerarquía normativa | Tabla de siete rangos con carácter, categoría sin rango, regla de desempate y regla de conflicto | `RF-001`, `RF-002`, `RF-003` |
| 7 | Gobernanza y aprobaciones | Propietario, lista de firmantes autorizados versionada, sección de aprobaciones protegida, mecanismo de firma, prohibición de autoaprobación | `RF-008`, `CB-004`, `CB-005` |
| 8 | Control de cambios de la base | Spec previa, versión del documento, registro en `CHANGELOG.md`, auditoría de conformidad previa al release menor | `RF-020`, `RF-021`, `CB-010` |
| 9 | Prohibiciones | Integración sin compuerta, tag no anotado, contenido prohibido en el repositorio, declaración de optimización sin medición | — |
| 10 | Legado y transición | Cláusula de legado para `SPEC-001` a `SPEC-007`, sustitución en la misma ruta y remisión a la spec de regularización | `RF-022`, `RF-024`, `CB-003` |

Prohibiciones del documento: fijar un recuento de documentos del corpus (`RF-018`); delegar una regla ejecutable al protocolo con una remisión que sustituya su contenido (la constitución define el principio y el protocolo lo desarrolla); contener rutas de procedimiento que cambien por etapa.

La sección 7 declara que la línea de aprobación de una compuerta solo queda válida dentro del commit firmado por una clave de la lista de firmantes autorizados. La sección 8 declara que un cambio de la constitución exige spec aprobada, incremento de versión del documento y entrada en `CHANGELOG.md`.

### `AGENTS.md` (rango 2)

Reglas operativas de agentes en 30 a 70 líneas útiles. Presupuesto por bloque, con total máximo de 68 líneas:

| Bloque | Contenido | Líneas máximas |
|---|---|---|
| Encabezado | Título y orden de precedencia en una frase | 3 |
| Misión y stack | Alcance del repositorio y tecnologías | 6 |
| Comandos | Validación, siguiente identificador, consulta de agentes | 6 |
| Mapa del repositorio | Una línea por ruta con su función | 12 |
| Entrada SDD | Ciclo de siete etapas, estados y compuertas como remisión de una línea cada uno | 10 |
| Aprobaciones | G1, G4 y G6, ubicación del registro, firma y prohibición de autoaprobación | 5 |
| Guardrails | Reglas de archivos y de contenido del repositorio | 8 |
| Git | Ramas, integración, tags y protección | 6 |
| Validación | Qué se comprueba antes de integrar y qué no acredita el validador | 5 |
| MCP y secretos | Convención de nombres y uso de `example.env` | 3 |
| Referencias | Constitución, protocolo, índice y flujo Git | 4 |

Prohibiciones del documento: reproducir el contenido del protocolo (`RF-009`); superar 70 líneas útiles; incorporar procedimiento por etapa; omitir el rol de auditoría (`RF-019`).

La remisión al protocolo se redacta como referencia de lectura, no como definición: `AGENTS.md` enuncia la obligación en una línea y remite al protocolo para el desarrollo. La autosuficiencia exigida por `RF-006` recae en el protocolo, no en `AGENTS.md`.

### `docs/sdd/PROTOCOLO_OPERATIVO.md` v2 (rango 3)

Redacción nueva desde cero (DEC-003). Dieciséis secciones de nivel 2, más un anexo de transición. Cada sección porta contenido normativo propio: una remisión a una guía para fijar una regla es un defecto de autosuficiencia (`CB-008`).

| # | Sección | Contenido normativo mínimo | Requisitos |
|---|---|---|---|
| 1 | Objeto, ámbito y rango | A qué obliga el protocolo, documentos alcanzados, vigencia desde la integración, relación con los rangos 1 y 2 | `RF-006` |
| 2 | Mapa de autoridad y precedencia | Tabla de siete rangos con carácter, categoría sin rango, desempate dentro del rango, regla de conflicto y acción ante contradicción | `RF-001`, `RF-002`, `RF-003`, `CB-001`, `CB-002` |
| 3 | Modelo SDD y glosario | Adopción Spec-Anchored y un significado único para spec, artefacto, compuerta, estado, propietario, autor, firmante, evidencia, rango, carácter, inventario y legado | `RNF-001` |
| 4 | Ciclo de siete etapas | Entrada, salida, artefacto, estado resultante, responsable y comando por etapa | `RF-025` |
| 5 | Máquina de estados | Conjunto de estados admitidos, tabla de transiciones con origen, destino, propietario y evidencia, reapertura y sustitución | `RF-027` |
| 6 | Compuertas G1 a G6 | Condición, evidencia exigida, declarante, verificación y acción ante fallo por compuerta | `RF-012`, `RF-025` |
| 7 | Trazabilidad obligatoria | Campos exigidos por artefacto y cadena `RF/CB → CA → T → evidencia`; prohibición de requisito sin criterio y de criterio sin tarea | `RNF-004` |
| 8 | Contratos de artefactos | Secciones obligatorias y prohibiciones de `spec.md`, `clarify.md`, `plan.md`, `tasks.md`, `validation_report.md`, informe analítico e informe de auditoría | `RF-013`, `RF-014`, `RF-015` |
| 9 | Identificadores y versionado | Espacios de identificadores con tres dígitos, no reutilización, regla de versión de specs con 0.1.0, MINOR, PATCH, reapertura y prohibición de renumerar una spec publicada | `RF-016`, `RNF-004`, `CB-013` |
| 10 | EARS y léxico | Cinco patrones admitidos, exigencia de número y unidad en cada umbral, lista de términos vetados y regla de detección por subcadena | `RF-026` |
| 11 | Aprobaciones | Formato de la línea, ubicación de G1, G4 y G6, sección protegida, firma exigida, lista de firmantes autorizados y prohibición de autoaprobación | `RF-012`, `RF-008`, `CB-004`, `CB-005` |
| 12 | Roles y permisos | Matriz de seis roles con permiso de lectura y de escritura por ruta, incluido el rol de auditoría, y precedencia entre permisos solapados | `RF-019` |
| 13 | Integración Git y release | G5 y G6 como compuertas del flujo, `merge --no-ff`, eliminación de la rama tras la integración, sincronización de `dev` con `main`, verificación del tag anotado, registro del resultado, protección remota y excepciones | `RF-010`, `RF-011` |
| 14 | Contrato del validador | Comandos, comprobaciones verificadas, comprobaciones no verificadas, códigos de salida y límite de lo que un resultado favorable acredita | `RNF-005` |
| 15 | Excepciones y legado | Cambio editorial, ramas de release, cláusula de legado para `SPEC-001` a `SPEC-007`, archivo de rama sin integración | `RF-022`, `CB-003`, `CB-011` |
| 16 | Control de cambios y auditoría de conformidad | Spec previa para cambiar la base, versión del documento, registro en `CHANGELOG.md`, auditoría de conformidad antes de cada release menor y prohibición de G6 sin informe | `RF-020`, `RF-021`, `CB-009`, `CB-010` |

El anexo de transición se rotula como anexo y no como sección, para no alterar el recuento de dieciséis secciones. Contiene: fecha de corte, tabla de documentos sustituidos con ruta, rango, operación y estado, cláusula de legado y registro del archivo de la rama Gemma (DEC-010, DEC-012).

Prohibiciones del documento: remitir a una guía para fijar una regla (`RF-006`, `CB-008`); fijar recuentos del corpus (`RF-018`); declarar un resultado favorable del validador como conformidad del régimen (DEC-004 de `SPEC-008`, `RNF-005`); admitir una integración sin compuerta cumplida.

### `docs/Flujo_de_Trabajo_Git.md` (rango 4)

Sustitución con seis bloques alineados:

| Bloque | Contenido obligatorio | Requisitos |
|---|---|---|
| Compuertas del flujo | G5 como autorización de integración y G6 como autorización de release, con condición y evidencia | `RF-010` |
| Integración | `merge --no-ff` exclusivo, prohibición de rebase, squash y copia manual, condición de cierre de la rama | `RF-010` |
| Eliminación de rama | Eliminación de la rama de trabajo tras confirmar la integración, con el comando de verificación del listado | `RF-010` |
| Sincronización y tag | Sincronización de `dev` con `main` antes del empaquetado, tag anotado `vMAJOR.MINOR.PATCH`, comprobación de tipo, mensaje y commit objetivo | `RF-011` |
| Registro de la verificación | Registro del resultado de G5 y de G6 en `validation_report.md` de la spec publicada y en la entrada del release de `CHANGELOG.md` | `RF-011`, `RF-012` |
| Protección y excepciones | Mapeo de protección remota de `main` y `dev`, excepción editorial y excepción de ramas de release | `RF-010` |

Prohibiciones del documento: admitir una integración sin compuerta cumplida; declarar un release sin tag verificado; fijar un procedimiento de release que contradiga el capítulo 13 del protocolo (la coherencia se comprueba en V11).

### `README.md` y `MEMORY.md` (sin rango, referencia no normativa)

Ambos declaran en su encabezado el carácter de referencia no normativa y su función descriptiva. Secciones de `README.md`:

| Sección | Contenido obligatorio |
|---|---|
| Descripción | Qué hace el repositorio y para qué caso de uso |
| Enfoque | SDD Spec-Anchored y remisión de una línea a la constitución y al protocolo |
| Estructura | Árbol de rutas con la función de cada una |
| Inicio rápido | Requisitos previos y comando de ejecución disponible |
| Estado real | `main.bat` existente, modelos locales presentes, referencia cruzada vigente |

`MEMORY.md` conserva diez bloques: identidad y estado, hardware, mapa operativo, enfoque SDD, regla crítica sobre `llama.cpp/`, reglas de ejecución, parámetros, criterios de validación, Git y MCP, referencias (`RF-018`, `CB-006` del informe de auditoría).

Prohibición de ambos: declarar un hecho que el árbol no respalde; fijar un recuento de documentos del corpus; presentar una guía como norma.

### `CHANGELOG.md` (sin rango, registro)

Tres entradas bajo `Unreleased` en este orden:

| Entrada | Contenido obligatorio | Requisitos |
|---|---|---|
| Base normativa v2 | Alcance, documentos sustituidos, fecha de corte y remisión al anexo de transición del protocolo | `RF-024` |
| Archivo de la rama Gemma | Nombre de la rama, decisión de archivo sin integración, carácter local y no publicado, commits no integrados | `RF-028`, `CB-011` |
| Registro de compuertas | Línea de G6 del release en curso con `- Approved by: Agent Sebaxtian` cuando el propietario la introduzca en un commit firmado | `RF-012` |

Prohibición: mover o reescribir entradas de releases publicados; declarar G6 sin informe de auditoría de conformidad registrado (`CB-009`).

### `docs/sdd/README.md` (índice del corpus)

Cuatro bloques:

| Bloque | Contenido obligatorio | Requisitos |
|---|---|---|
| Carácter del índice | Declaración de función: navegación del corpus y orden de precedencia dentro de cada rango | `RF-002`, `RF-003` |
| Tabla de autoridad | Reproducción del mapa de siete rangos con carácter y precedencia interna | `RF-001`, `RF-003` |
| Tabla de inventario | Una fila por archivo con ruta, carácter, orden de lectura y rango; incluye la raíz de `docs/sdd/`, `plantillas/`, los informes de análisis, el informe de auditoría y el registro `firmantes_autorizados` | `RF-017`, `CB-012` |
| Regla de inventario | Cómo se calcula el recuento desde la tabla y qué hacer cuando aparece un archivo sin fila | `RF-018`, `CB-006`, `CB-012` |

La tabla de inventario usa cinco columnas: `Archivo`, `Ruta`, `Carácter`, `Orden de lectura`, `Rango`. El recuento se obtiene contando filas de datos y nunca se escribe como cifra fija (DEC-007). Un archivo nuevo exige fila antes de aprobar la compuerta en curso.

## Contratos de las plantillas

Las plantillas son norma de rango 5. Prevalecen sobre las guías y no admiten dos formas incompatibles para un mismo campo (`RF-005`, `CB-007`).

### `spec.md`

- Frontmatter con once campos: `id`, `title`, `status`, `version`, `created`, `updated`, `owner`, `branch`, `release`, `supersedes`, `superseded_by`.
- Secciones: contexto y objetivo, actores y permisos, requisitos funcionales en EARS, requisitos no funcionales, casos borde, fuera de alcance, criterios de aceptación, aprobaciones, historial de cambios.
- Cada criterio de aceptación cierra con una línea `Cubre:` que enumera los identificadores `RF` y `CB` que satisface.
- Sección de aprobaciones con dos casillas y ninguna más: G1 y G4.
- Historial de cambios con columnas `Versión`, `Fecha` y `Cambio`, gobernado por la regla de versionado (DEC-006).

Prohibiciones: rutas de código, clases, SQL y comandos técnicos; casilla de G6; dos formas para un mismo campo.

### `clarify.md`

- Bloque por `AMB-NNN` con descripción, pregunta, respuesta, decisión, fecha UTC y responsable.
- Sección de casos borde nuevos, con la constancia de ausencia cuando no los haya.
- Sección de parches aplicados con casilla marcada por cada parche y la referencia del requisito o criterio afectado.
- Decisiones de negocio.
- Prohibición: dejar una casilla `[ ]` pendiente al cerrar (lo comprueba el validador).

### `plan.md`

- Secciones: referencias, naturaleza del entregable, arquitectura, contratos, decisiones `DEC-NNN`, estrategia de testing y matriz de cobertura con filas `RF-NNN` y `CB-NNN`.
- Prohibición: matriz sin verificación asociada o decisión sin alternativa descartada.

### `tasks.md`

Campos obligatorios por tarea, en este orden:

| Campo | Contenido | Requisitos |
|---|---|---|
| `Dependencias` | Identificadores de tareas previas o `ninguna` | — |
| `Requisitos cubiertos` | Identificadores `RF`, `RNF` y `CB` que la tarea satisface | `RF-013` |
| `Criterio de aceptación` | Identificador `CA-NNN` que la tarea materializa | `RF-013`, `CA-010` |
| `Archivos` | Rutas permitidas de la tarea | — |
| `Estimación` | Minutos entre 15 y 30 | — |
| `Validación` | Comando o comprobación que debe pasar | — |
| `Evidencia` | Salida, extracto o comprobación registrada al completar | `RF-013` |
| `Completada` | Casilla que el validador exige con G3 | — |

Prohibición: tarea sin criterio de aceptación o sin campo de evidencia; tarea que toque rutas fuera de su campo `Archivos`.

### `validation_report.md`

- Secciones: entorno, matriz de trazabilidad, brechas y dictamen.
- Matriz con cinco columnas: `Requisito`, `CA`, `Prueba / comando`, `Evidencia`, `Estado`, con `PASADO` como único valor convergente.
- Dictamen con la casilla `CONVERGIDO`.
- Prohibición explícita: casilla o sección de aprobación; el registro de G4 vive en `spec.md` (`RF-012`).

### `informe_analitico.md` (contrato nuevo)

| Sección | Contenido obligatorio |
|---|---|
| Encabezado | Título, fecha, autor y declaración de carácter de referencia no normativa |
| Objeto y alcance | Qué se analiza y qué queda excluido |
| Fuentes | Documentos, comandos y datos empleados, con ruta y fecha de consulta |
| Procedimiento | Cómo se obtiene cada afirmación y qué la haría falsa |
| Análisis | Cuerpo del análisis, con una subsección por materia |
| Conclusiones | Afirmaciones sostenidas por el análisis, separadas de las recomendaciones |
| Límites | Qué no se pudo verificar y por qué |

Rol habilitado para redactarlo: `documenter`. No crea espacio de identificadores propio; sus afirmaciones se citan por sección y fecha. Prohibición: fijar reglas de obligado cumplimiento (`RF-004`).

### `informe_auditoria.md` (contrato nuevo)

Diez secciones: ficha de reproducibilidad, base normativa e inventario, criterio y escalas, matriz de dimensiones, hallazgos, compuertas, veredicto global, hoja de ruta, limitaciones y anexos de evidencia.

Escala de veredicto de cinco valores: `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE`, `NO APLICA`. Escala de severidad de cuatro niveles: `Crítica`, `Alta`, `Media`, `Baja`.

Regla de numeración: `AUD-NNN` correlativo por dimensión, con diez números reservados por dimensión y continuación inmediata al último asignado cuando una dimensión excede su capacidad. Un número asignado no se reutiliza entre versiones del informe.

Rol habilitado: rol de auditoría, con lectura sobre la base y escritura limitada al informe. Mientras la implementación de ese rol en `.opencode/` corresponda a B3, la escritura la ejecuta `documenter` bajo la declaración del rol (`RF-019`).

## Modelo de aprobación

### Ubicación del registro

| Compuerta | Artefacto | Momento | Condición |
|---|---|---|---|
| G1 | `spec.md`, sección de aprobaciones | Cierre de Clarify | Spec sin ambigüedades, `Cubre:` completo y firma del propietario |
| G4 | `spec.md`, sección de aprobaciones | Cierre de Validate | Reporte de validación convergido y firma del propietario |
| G6 | `CHANGELOG.md`, entrada del release | Release | Auditoría de conformidad registrada, tag verificado y firma del propietario |

Una sola ubicación por compuerta. El reporte de validación no porta casilla de aprobación (`RF-012`).

### Mecanismo de firma

1. El propietario firma sus commits con una clave SSH registrada en Git local (`gpg.format` en `ssh` y `user.signingkey` con la clave privada del propietario).
2. La clave pública correspondiente figura en `docs/sdd/firmantes_autorizados`, archivo versionado que solo contiene claves públicas y que el propietario mantiene.
3. El archivo usa el formato de lista de firmantes admitidos de Git: una línea por firmante, con identidad y clave pública, y comentarios con `#`.
4. La verificación de una compuerta consiste en tomar el commit que introduce la línea de aprobación y comprobar que su firma verifica contra esa lista.
5. Si la firma falta, no verifica o la clave no figura en la lista, la compuerta no está aprobada y el caso se registra como incumplimiento (`CB-004`, `CB-005`).

Procedimiento de verificación que el protocolo declara y que el validador automatizará en B2:

| Paso | Comprobación |
|---|---|
| 1 | Localizar el commit que introdujo la línea de aprobación del artefacto |
| 2 | Comprobar que el commit está firmado |
| 3 | Verificar la firma contra la lista de firmantes autorizados |
| 4 | Registrar el resultado en la evidencia de la compuerta |

Esta spec deja el archivo de firmantes creado y el mecanismo declarado. La comprobación automática de firma en el validador corresponde a B2 y se declara como alcance no verificado en el capítulo 14 del protocolo (`RNF-005`).

### Autoría frente a aprobación

- Autor es el rol o agente que redacta un artefacto.
- Propietario es la persona que aprueba.
- La coincidencia entre autor y propietario no invalida la aprobación; lo que la valida es la firma del commit (`AMB-002`).
- Ningún agente declara una compuerta. Un agente que redacta la línea de aprobación produce un registro sin valor y el caso se trata como incumplimiento.

## Trazabilidad de la base v2

La cadena de cada requisito de esta spec se materializa así:

```text
RF/CB de SPEC-009 → documento y sección que lo implementa → comprobación V-NN → evidencia en validation_report.md
```

Reglas de trazabilidad que la base v2 declara y que esta spec aplica:

- Ningún requisito sin criterio de aceptación; ningún criterio sin tarea; ninguna tarea sin evidencia.
- Cada documento de la base cita el requisito que implementa en su propio encabezado de sección.
- Un requisito que cambia después de G1 devuelve la spec a `draft` y exige nueva clarificación.

## Transición y legado

### Sustitución

Los documentos se sustituyen en la misma ruta y conservan su nombre. Las versiones anteriores permanecen en el historial Git y no se copian a rutas paralelas (DEC-010).

| Ruta | Estado tras la Etapa 6 |
|---|---|
| `docs/constitution.md` | Sustituido, versión v2 |
| `AGENTS.md` | Sustituido, versión v2 |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | Sustituido por redacción nueva, versión v2 |
| `docs/Flujo_de_Trabajo_Git.md` | Sustituido, versión alineada |
| `docs/sdd/plantillas/spec.md` | Sustituido |
| `docs/sdd/plantillas/clarify.md` | Sustituido |
| `docs/sdd/plantillas/plan.md` | Sustituido |
| `docs/sdd/plantillas/tasks.md` | Sustituido con criterio de aceptación y evidencia |
| `docs/sdd/plantillas/validation_report.md` | Sustituido sin casilla de aprobación |
| `docs/sdd/plantillas/informe_analitico.md` | Creado |
| `docs/sdd/plantillas/informe_auditoria.md` | Creado |
| `docs/sdd/README.md` | Sustituido como índice con precedencia |
| `README.md` | Sustituido con el estado real del repositorio |
| `MEMORY.md` | Sustituido sin hechos obsoletos |
| `CHANGELOG.md` | Sustituido con las tres entradas de `Unreleased` |

### Registro

El registro de transición se declara en dos soportes que declaran el mismo contenido: el anexo del protocolo v2 y la entrada `Unreleased` de `CHANGELOG.md`. Cada fila declara fecha, alcance y estado. Una divergencia entre ambos registros se corrige en `CHANGELOG.md` (DEC-012).

### Cláusula de legado

Las specs publicadas `SPEC-001` a `SPEC-007` conservan su contenido y quedan amparadas por la cláusula de legado. Su regularización corresponde a una spec posterior. `SPEC-008` se rige por la base v2 desde su publicación. Un historial de versiones no derivado de regla se conserva y se regulariza en la misma spec de legado (`CB-013`).

### Archivo de la rama Gemma

La rama `feat/gemma-4-26b-a4b-it-qat-gguf` permanece local, no se publica y no se integra. Su decisión se registra en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición, con el número de commits no integrados y la declaración de que la referencia se conserva sin fusionar (DEC-012).

## Decisiones técnicas

### DEC-001: mapa de autoridad en tres soportes

- **Decisión:** el mismo contenido de jerarquía se declara en la constitución §6 como tabla suprema, en el protocolo §2 como desarrollo operativo y en `docs/sdd/README.md` como reproducción de navegación. La constitución es la fuente; una divergencia se corrige en el soporte de rango menor.
- **Justificación:** `RF-003` exige tres niveles y un lector puede entrar por cualquiera de ellos; una sola fuente sin reproducción obligaría a abrir la constitución para navegar el corpus, y dos fuentes sin regla de corrección producirían divergencia permanente.
- **Alternativas descartadas:** (a) mapa solo en la constitución: deja el índice sin función de desempate y el protocolo sin tabla de rangos; (b) mapa solo en el protocolo: contradice la primacía de la constitución y `RF-003`; (c) mapa en un archivo nuevo de gobernanza: añade un rango no previsto y un documento que el índice tendría que declarar sin norma que lo respalde.

### DEC-002: guías como referencia y plantillas como norma

- **Decisión:** el corpus de guías, los informes de análisis y los informes de auditoría se declaran referencia no normativa en su encabezado. Las plantillas de `docs/sdd/plantillas/` son norma de rango 5 y prevalecen sobre cualquier guía.
- **Justificación:** `RF-004` y `RF-005` separan explicación de obligación; la contradicción documentada entre una guía y una plantilla sobre la forma de los criterios de aceptación (`AUD-003`) queda resuelta por rango sin reescribir las guías en esta spec.
- **Alternativas descartadas:** (a) convertir las guías en norma: crearía diecisiete fuentes normativas con reglas solapadas y sin orden interno; (b) eliminar las guías: pierde el material explicativo y la trazabilidad con el corpus de origen; (c) mantener la situación vigente: es la causa directa de `AUD-001`, `AUD-003` y `AUD-004`.

### DEC-003: protocolo v2 autosuficiente

- **Decisión:** redactar el protocolo desde cero con las dieciséis secciones del contenido mínimo, cada una con regla propia. La remisión a una guía se admite solo como lectura complementaria y nunca como definición de la regla.
- **Justificación:** `RF-006` y `RF-007` exigen autosuficiencia y redacción nueva; una edición incremental del documento vigente conservaría la estructura de diez secciones y las remisiones que `CB-008` califica como defecto.
- **Alternativas descartadas:** (a) edición incremental del protocolo vigente: no alcanza las dieciséis secciones sin reescritura completa y arrastra la dependencia del corpus; (b) protocolo que remite a las guías por sección: reproduce el defecto que la spec corrige; (c) protocolo dividido en varios archivos: multiplica los rangos y rompe la regla de una sola norma ejecutable.

### DEC-004: registro único de aprobaciones

- **Decisión:** G1 y G4 se registran solo en `spec.md`; G6 se registra solo en `CHANGELOG.md`. El reporte de validación no porta casilla de aprobación.
- **Justificación:** `RF-012` fija un titular por compuerta; dos titulares para la misma compuerta permiten un estado aprobado en un artefacto y no aprobado en el otro (`AUD-021`).
- **Alternativas descartadas:** (a) registro en el reporte de validación: el reporte lo escribe el rol de verificación y la aprobación corresponde al propietario, con lo que se mezclan autoría y aprobación; (b) registro en `INDEX.md`: el registro se actualiza en cada etapa y el historial de aprobación quedaría fuera del artefacto que se aprueba; (c) registro doble con validación cruzada: exige coherencia entre dos artefactos sin aportar información nueva.

### DEC-005: firma SSH y lista de firmantes versionada

- **Decisión:** la aprobación se acredita con la firma SSH del commit que introduce la línea de aprobación, verificada contra `docs/sdd/firmantes_autorizados`. El archivo contiene solo claves públicas, se versiona y lo mantiene el propietario.
- **Justificación:** `RF-008`, `CB-004` y `CB-005` exigen autoría verificable y acotan la confianza a una lista explícita; la firma SSH reutiliza la configuración de Git disponible y no requiere una infraestructura de confianza nueva.
- **Alternativas descartadas:** (a) firma GPG: añade gestión de anillos de claves sin ventaja verificable para el objetivo; (b) aprobación por identidad declarada en el texto: es la situación que `AMB-002` invalidó, porque equivale una cadena escrita con una firma; (c) lista de firmantes fuera del repositorio: impide auditar el alcance de la confianza desde el propio commit.

### DEC-006: regla de versionado de specs

- **Decisión:** 0.1.0 en la redacción inicial; incremento MINOR por cada etapa que cambie el contrato, es decir clarify, plan, tasks y validación; incremento PATCH por corrección editorial sin cambio de requisitos; reapertura de una spec `validated` con incremento MINOR y motivo registrado; prohibición de renumerar una spec `released`, cuyos cambios se tramitan por reapertura o por spec nueva.
- **Justificación:** `RF-016` y `CA-013` exigen que dos revisiones independientes obtengan el mismo número; una regla por tipo de cambio elimina la apreciación y el historial de esta spec ya la aplica con 0.1.0 y 0.2.0.
- **Alternativas descartadas:** (a) versionado libre por criterio del redactor: es la causa de `AUD-055`; (b) SemVer completo con MAJOR en cada cambio de requisito: eleva la versión antes del primer release y rompe la convención del proyecto; (c) versión derivada del recuento de cambios: no distingue un cambio de contrato de una errata.

### DEC-007: índice con orden de precedencia por rango

- **Decisión:** `docs/sdd/README.md` declara, por cada rango, el orden de precedencia interno y el carácter de cada archivo. El orden es el desempate verificable entre documentos del mismo rango. El recuento se calcula contando filas y no se escribe como cifra.
- **Justificación:** `RF-003` y `CA-002` exigen un desempate declarado; `RF-018` prohíbe fijar recuentos y `CA-014` exige cobertura del árbol, de modo que el índice es el único soporte que satisface ambas condiciones.
- **Alternativas descartadas:** (a) desempate por fecha de modificación: depende del historial y no del contenido, y un cambio editorial invertiría la precedencia; (b) desempate por orden alfabético: no guarda relación con la autoridad del documento; (c) ausencia de desempate: `CB-001` detendría el trabajo sin salida.

### DEC-008: contrato de informe analítico y de informe de auditoría

- **Decisión:** se crean dos plantillas con contrato propio. El informe analítico declara objeto, fuentes, procedimiento, análisis, conclusiones y límites, y no crea espacio de identificadores. El informe de auditoría declara diez secciones, escala de veredicto de cinco valores, severidad de cuatro niveles y numeración `AUD-NNN` por dimensión.
- **Justificación:** `RF-014` y `RF-015` exigen contrato declarado; el corpus vigente carece de él (`AUD-023`) y el informe de `SPEC-008` fijó de facto una estructura que la base debe reconocer para no invalidar su propia evidencia.
- **Alternativas descartadas:** (a) un contrato único para ambos informes: mezcla análisis y auditoría y obliga al análisis a portar escala de veredicto que no necesita; (b) contrato declarado solo en el protocolo sin plantilla: deja el formato en la práctica y reproduce `AUD-023`; (c) reutilizar el contrato del informe de `SPEC-008` como texto normativo: convierte un entregable en norma y contradice la separación de rangos.

### DEC-009: rol de auditoría declarado e implementación en B3

- **Decisión:** el rol de auditoría se declara en la constitución, en el protocolo y en `AGENTS.md`, con lectura sobre la base completa, sin permiso de modificar requisitos y sin permiso de aprobar compuertas. Su materialización en `.opencode/` queda en B3.
- **Justificación:** `RF-019` y `CA-012` exigen la declaración en tres documentos y acotan el alcance; crear el agente en esta spec modificaría la configuración de agentes, que la propia spec excluye.
- **Alternativas descartadas:** (a) crear el agente de auditoría en la Etapa 6: excede el alcance y altera un artefacto que la base v2 no rige todavía; (b) asignar la auditoría al rol `reviewer`: mezcla verificación de conformidad con auditoría de la base y concentra dos funciones incompatibles en un rol; (c) atribuir la auditoría al propietario: elimina la independencia que el rol aporta.

### DEC-010: transición en la misma ruta y cláusula de legado

- **Decisión:** cada documento se sustituye en su ruta y con su nombre. Las versiones anteriores quedan en el historial Git. El registro se declara en el anexo del protocolo v2 y en `CHANGELOG.md`. Las specs `SPEC-001` a `SPEC-007` se amparan con una cláusula de legado que conserva su contenido.
- **Justificación:** `RF-024` y `CA-018` exigen sustitución registrada; rutas paralelas producirían dos documentos vigentes para la misma materia, y reescribir las specs publicadas violaría `CB-003`.
- **Alternativas descartadas:** (a) convivencia con sufijo `_v2`: deja la base anterior vigente en la ruta original y crea ambigüedad de autoridad; (b) archivo de la base anterior en `docs/legacy/`: duplica documentos que el historial Git ya conserva y añade superficie de divergencia; (c) reescritura retroactiva de las specs publicadas: destruye la evidencia histórica de las compuertas ya emitidas.

### DEC-011: auditoría de conformidad antes de cada release menor

- **Decisión:** antes de preparar un release menor se ejecuta una auditoría de conformidad, se conserva su informe y se registra su identificador en la entrada del release. Sin ese informe no se emite G6.
- **Justificación:** `RF-021` y `CB-009` ligan la auditoría a la compuerta; conservar el informe permite repetir la verificación y comparar dos releases consecutivos.
- **Alternativas descartadas:** (a) auditoría solo anual: el intervalo puede contener varios releases sin control y rompe la relación con G6; (b) auditoría sin conservación del informe: impide acreditar la compuerta y reproduce la ausencia de evidencia que `SPEC-008` registró en D4; (c) auditoría por cada cambio de la base: excede la capacidad del proceso y desincentiva el cambio normativo.

### DEC-012: archivo de la rama Gemma y su registro

- **Decisión:** la rama `feat/gemma-4-26b-a4b-it-qat-gguf` se archiva sin integrar, permanece local y no se publica. La decisión se registra en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición, con el recuento de commits no integrados y el estado de la referencia.
- **Justificación:** `RF-028` y `CB-011` exigen registrar el archivo y excluir la integración; publicar la rama contradiría la decisión y `CA-019` quedaría sin verificar.
- **Alternativas descartadas:** (a) integrar la rama: introduce parámetros de un modelo no validado y excede el alcance de esta spec; (b) eliminar la rama: pierde el trabajo y la referencia histórica sin dejar decisión registrada; (c) publicar la rama en el remoto: crea un artefacto remoto que el archivo excluye y obliga a mantener protección adicional.

### DEC-013: ejecución de la Etapa 6 y alcance de escritura

- **Decisión:** la Etapa 6 se ejecuta con dos escritores. El rol `documenter` escribe `docs/**` y `AGENTS.md`. Los tres archivos de raíz `README.md`, `MEMORY.md` y `CHANGELOG.md` los escribe el propietario en la misma rama, con el contenido fijado por `tasks.md`, porque la allowlist vigente de agentes no alcanza la raíz del repositorio. Ampliar esa allowlist corresponde a B3 y queda fuera de esta spec.
- **Justificación:** la allowlist vigente concede a `documenter` escritura en `docs/**` y `AGENTS.md` y niega el resto; asignar la escritura de raíz a un rol sin permiso produciría una operación fuera de la declaración de permisos, que es exactamente el defecto de D7 registrado por `SPEC-008`.
- **Alternativas descartadas:** (a) ampliar la allowlist de `documenter` en esta spec: modifica la configuración de agentes, excluida por «Fuera de alcance»; (b) escribir la raíz con `coder`: no tiene permiso sobre documentación y su alcance es el código; (c) dejar los tres archivos fuera del alcance: incumple `RF-024`, que exige la entrada de `CHANGELOG.md` y el estado real de `README.md` y `MEMORY.md`.

## Estrategia de testing

La verificación es documental. No se crean archivos de prueba ni suites nuevas. Cada comprobación declara comando o procedimiento, resultado esperado y acción ante fallo. Las etiquetas `V1` a `V16` identifican comprobaciones de esta estrategia y no pertenecen a los espacios de identificadores del protocolo.

### Momento de ejecución

| Etapa | Comprobaciones aplicables |
|---|---|
| Cierre de Plan (esta etapa) | `V1` |
| Cierre de Tasks | `V1` y `V15` |
| Cierre de Implement | `V1` a `V15` |
| Antes de G4 | `V1` a `V16` |

Una comprobación que no aplica a la etapa en curso se declara `no aplicable` con la etapa en que se ejecutará, y no se marca como superada.

### Comprobaciones

| # | Comprobación | Comando o procedimiento | Resultado esperado |
|---|---|---|---|
| V1 | Conformidad estructural de la spec y sus artefactos | `python tools\sdd\validate.py --spec SPEC-009 --gate G2` | Código de salida `0`, sin errores |
| V2 | Longitud de `AGENTS.md` | `(Get-Content AGENTS.md \| Where-Object { $_.Trim() -ne '' }).Count` | Valor entre 30 y 70 inclusive |
| V3 | Dieciséis secciones del protocolo | `(Select-String -Path docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern '^## [0-9]+\.').Count`; revisar que los números sean 1 a 16 sin repetición ni salto | `16` |
| V4 | Cobertura del índice | Listar `docs\sdd\*.md`, `docs\sdd\plantillas\*.md` y `docs\sdd\firmantes_autorizados`; comparar cada ruta con la tabla de inventario de `docs\sdd\README.md` | Diferencia vacía en ambos sentidos |
| V5 | Ausencia de recuentos fijos | `Select-String -Path docs\constitution.md,AGENTS.md,docs\sdd\PROTOCOLO_OPERATIVO.md,docs\sdd\README.md,docs\Flujo_de_Trabajo_Git.md -Pattern '\b\d+ documentos?\b'` | Sin coincidencias |
| V6 | Autosuficiencia del protocolo | `Select-String -Path docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern 'guia_'` | Sin coincidencias |
| V7 | Contrato de tareas | `Select-String -Path docs\sdd\plantillas\tasks.md -Pattern 'Criterio de aceptación\|Evidencia'` | Dos o más coincidencias, una por campo |
| V8 | Reporte sin casilla de aprobación | `Select-String -Path docs\sdd\plantillas\validation_report.md -Pattern 'Approved by\|Aprobación'` | Sin coincidencias |
| V9 | Plantillas de informe | `Test-Path docs\sdd\plantillas\informe_analitico.md`; `Test-Path docs\sdd\plantillas\informe_auditoria.md` | `True` en ambos comandos |
| V10 | Tabla de jerarquía completa | `Select-String -Path docs\constitution.md,docs\sdd\PROTOCOLO_OPERATIVO.md,docs\sdd\README.md -Pattern '^\|\s*[1-7]\s*\|'`; revisar la fila de categoría sin rango en cada tabla | Siete filas de rango por documento, más la categoría sin rango declarada |
| V11 | Coherencia entre documentos | Extraer de los cuatro documentos normativos el conjunto de compuertas, el conjunto de estados, el conjunto de roles, el conjunto de rutas sustituidas y las verificaciones de release; comparar los cinco conjuntos por pares | Conjuntos idénticos: seis compuertas, diez estados, seis roles, quince rutas y tres verificaciones de release |
| V12 | Registro de transición | `Select-String -Path docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern 'Anexo de transición'`; `Select-String -Path CHANGELOG.md -Pattern 'SPEC-009'` | Dos coincidencias; la entrada de `CHANGELOG.md` bajo `Unreleased` |
| V13 | Archivo de la rama Gemma | `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf`; `git branch -r --list origin/feat/gemma-4-26b-a4b-it-qat-gguf`; `Select-String -Path CHANGELOG.md,docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern 'gemma-4-26b-a4b-it-qat-gguf'` | Rama local presente, rama remota vacía y dos o más coincidencias documentales |
| V14 | Integridad del árbol | `git diff --check` | Salida vacía, código de salida `0` |
| V15 | Alcance de archivos modificados | `git status --short` comparado con la tabla de alcance documental de este plan | Solo las dieciséis rutas declaradas |
| V16 | Revisión independiente | El rol `reviewer` reejecuta `V1` a `V15`, revisa las dieciséis rutas y registra discrepancias en `validation_report.md` | Sin discrepancias abiertas antes de G4 |

### Registro de la verificación

- El resultado de `V1` a `V16` se registra en `validation_report.md` de esta spec durante la Etapa 7.
- Una comprobación fallida obliga a corregir el documento y a repetir la batería completa.
- `V1` se ejecuta también al cierre de Tasks, para confirmar que el plan y las tareas son conformes antes de escribir la base.
- El resultado favorable de `V1` acredita estructura y cobertura documental. No acredita la firma del commit de aprobación ni la conformidad del régimen completo, que se declaran como alcance no verificado en el capítulo 14 del protocolo (`RNF-005`).

## Matriz de cobertura

| Requisito | Documento y sección | Verificación |
|---|---|---|
| `RF-001` | `docs/constitution.md` §6; protocolo §2; índice, tabla de autoridad | `V10`, `V11` |
| `RF-002` | Encabezado de cada documento; índice, columna de carácter | `V4`, `V10` |
| `RF-003` | Constitución §6; protocolo §2; índice, orden de precedencia por rango | `V10`, `V11` |
| `RF-004` | Encabezado de guías e informes; protocolo §2 | `V4`, `V6` |
| `RF-005` | Plantillas de rango 5; protocolo §2 y §8 | `V7`, `V8`, `V9` |
| `RF-006` | Protocolo §1 a §16 sin remisión normativa | `V6` |
| `RF-007` | Protocolo completo; anexo de transición declara la redacción nueva | `V3`, `V12` |
| `RF-008` | Constitución §2 y §7; protocolo §11 | `V11`, `V16` |
| `RF-009` | `AGENTS.md` con once bloques y presupuesto de 68 líneas | `V2` |
| `RF-010` | Flujo Git, compuertas del flujo e integración; protocolo §13 | `V11` |
| `RF-011` | Flujo Git, sincronización, tag y registro; protocolo §13 | `V11` |
| `RF-012` | Plantilla `spec.md` con G1 y G4; `CHANGELOG.md` con G6; plantilla de validación sin casilla | `V8`, `V11` |
| `RF-013` | Plantilla `tasks.md` con criterio de aceptación y evidencia; protocolo §8 | `V7` |
| `RF-014` | Plantilla `informe_analitico.md`; protocolo §8 | `V9` |
| `RF-015` | Plantilla `informe_auditoria.md`; protocolo §8 | `V9` |
| `RF-016` | Protocolo §9; `spec.md` de esta spec, historial de cambios | `V11`, `V16` |
| `RF-017` | `docs/sdd/README.md`, tabla de inventario | `V4` |
| `RF-018` | `docs/sdd/README.md`, regla de inventario; ausencia de cifras en la base | `V5` |
| `RF-019` | Constitución §7; protocolo §12; `AGENTS.md`, bloque de aprobaciones | `V11` |
| `RF-020` | Constitución §8; protocolo §16 | `V11`, `V16` |
| `RF-021` | Protocolo §16; `CHANGELOG.md`, entrada de release | `V11`, `V12` |
| `RF-022` | Constitución §10; protocolo §15 y anexo | `V11` |
| `RF-023` | Los cuatro documentos normativos y sus cinco conjuntos | `V11` |
| `RF-024` | Anexo de transición; `CHANGELOG.md` bajo `Unreleased`; control de alcance | `V12`, `V14`, `V15` |
| `RF-025` | Protocolo, dieciséis secciones | `V3` |
| `RF-026` | Protocolo §10 | `V3`, `V11` |
| `RF-027` | Protocolo §5 | `V3` |
| `RF-028` | `CHANGELOG.md` y anexo de transición | `V13` |
| `RNF-001` | Redacción de cada contrato y de cada regla | `V16` |
| `RNF-002` | Protocolo autosuficiente; ausencia de remisión normativa | `V6` |
| `RNF-003` | Idioma y formato de los dieciséis documentos | `V16` |
| `RNF-004` | Protocolo §9; matriz de cobertura y contrato de tareas | `V11` |
| `RNF-005` | Protocolo §14; registro de la verificación de este plan | `V1`, `V6` |
| `RNF-006` | Constitución §10; anexo de transición con las trece rutas | `V11`, `V16` |
| `CB-001` | Protocolo §2, regla de desempate; índice, orden por rango | `V10` |
| `CB-002` | Encabezado de cada documento; índice, columna de carácter | `V4` |
| `CB-003` | Constitución §10; protocolo §15, cláusula de legado | `V11` |
| `CB-004` | Protocolo §11; constitución §7 | `V11`, `V16` |
| `CB-005` | Protocolo §11; `docs/sdd/firmantes_autorizados` | `V11`, `V16` |
| `CB-006` | `docs/sdd/README.md`, regla de inventario | `V5` |
| `CB-007` | Plantillas de rango 5; protocolo §2 | `V7`, `V8` |
| `CB-008` | Protocolo §1 a §16 sin remisión normativa | `V6` |
| `CB-009` | Protocolo §16; `CHANGELOG.md`, entrada de release | `V11`, `V12` |
| `CB-010` | Constitución §8; protocolo §16 | `V11`, `V12` |
| `CB-011` | `CHANGELOG.md`; anexo de transición; estado de la rama | `V13` |
| `CB-012` | `docs/sdd/README.md`, tabla de inventario y regla de archivo nuevo | `V4` |
| `CB-013` | Protocolo §15; cláusula de legado sobre historiales no derivados de regla | `V16` |

## Riesgos y mitigaciones

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Divergencia entre los tres soportes del mapa de autoridad | Regla sin resolución única | Declarar el contenido una sola vez y reproducirlo con la misma tabla; corregir en el rango menor (DEC-001, `V10`) |
| Longitud de `AGENTS.md` fuera del margen | Incumplimiento de `RF-009` y del validador global | Presupuesto por bloque con total máximo de 68 líneas y comprobación `V2` |
| Protocolo que remite a una guía para fijar una regla | Defecto de autosuficiencia | Redacción desde cero y comprobación `V6` antes de G4 (`CB-008`) |
| Índice que no cubre un archivo nuevo | Navegación incompleta | Regla de archivo nuevo con fila previa a la compuerta en curso (`CB-012`, `V4`) |
| Recuento fijo heredado del corte de auditoría | Contradicción con `RF-018` | Comprobación `V5` y remisión del inventario al índice (`CB-006`) |
| Firmantes sin clave pública disponible | Compuerta no verificable | Lista versionada con solo claves públicas, mantenida por el propietario (`CB-005`) |
| Escritura de raíz sin rol habilitado | Operación fuera de la allowlist | Dos escritores declarados en DEC-013 y control de alcance `V15` |
| Rama Gemma publicada por descuido | Contradicción con `CB-011` | Verificación del remoto en `V13` antes de G4 |
| Transición declarada solo en `CHANGELOG.md` | Registro sin respaldo normativo | Doble soporte con el anexo del protocolo y comprobación `V12` |
| Deriva de alcance hacia B2, B3 o B4 | Cambio fuera de la spec aprobada | Declarar el mecanismo sin automatizarlo; revisión `V16` y control `V15` |

## Criterios de cierre del plan

- La matriz de cobertura alcanza `RF-001` a `RF-028`, `RNF-001` a `RNF-006` y `CB-001` a `CB-013`, sin identificador sin fila.
- Cada comprobación `V1` a `V16` declara comando o procedimiento y resultado esperado.
- Cada decisión `DEC-001` a `DEC-013` declara alternativa descartada.
- `python tools\sdd\validate.py --spec SPEC-009 --gate G2` devuelve código `0`.
- La spec pasa a `planned` y el registro `specs/INDEX.md` coincide con el frontmatter.
- La compuerta G2 se declara en la Etapa 5, al cerrar Tasks, y no en esta etapa.
