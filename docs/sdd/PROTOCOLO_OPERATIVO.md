# Protocolo Operativo SDD del proyecto LLaMA

Este documento es la **norma ejecutable** del Desarrollo Basado en Especificaciones (SDD) del proyecto LLaMA. Su rango es **3** y su carácter es **normativo**: desarrolla el proceso que `docs/constitution.md` fija como principio en el rango 1 y que `AGENTS.md` enuncia como obligación operativa en el rango 2, y prevalece sobre el flujo Git (rango 4), las plantillas (rango 5), las specs (rango 6) y el código (rango 7).

La versión v2 es una **redacción nueva desde cero**: sustituye al protocolo anterior en la misma ruta, sin edición incremental y sin remisiones que deleguen una regla en un documento de referencia no normativa. La transición desde la base vigente se registra en el Anexo de transición de este documento y en la entrada `Unreleased` de `CHANGELOG.md`.

Rige desde el commit que lo integra en `dev`; antes de ese commit rige el protocolo anterior, conservado en el historial Git.

## 1. Objeto, ámbito y rango

**Objeto.** Fijar cómo se especifica, clarifica, planifica, descompone, implementa, valida, integra y publica un cambio del repositorio, de modo que dos lectores independientes alcancen la misma decisión.

**Alcance personal.** Obliga a cada rol de agente de §12, al propietario en lo que este documento le atribuye y a cada persona que edite el repositorio.

**Documentos alcanzados.** `docs/Flujo_de_Trabajo_Git.md` (rango 4), las plantillas de `docs/sdd/plantillas/` (rango 5), las specs de `specs/NNN-slug/` (rango 6), la implementación de `src/`, `tools/`, `tests/` y `.opencode/` (rango 7), y los documentos sin rango en lo que este protocolo les atribuye.

**Vigencia.** Rige desde el commit que integra la base v2 en `dev`. Antes de ese commit rige el protocolo anterior, conservado en el historial Git y sin vigencia simultánea.

**Relación con el rango 1.** La constitución fija el principio y la prohibición; este protocolo las desarrolla y no las amplía ni las atenúa. Ante contradicción prevalece la constitución y el trabajo se detiene hasta corregir este documento.

**Relación con el rango 2.** `AGENTS.md` enuncia la obligación en una línea y remite a este documento para el desarrollo. Por rango, `AGENTS.md` prevalece sobre este protocolo: la remisión no transfiere autoridad y una divergencia en la materia desarrollada se corrige en este documento.

**Defecto de conformidad.** Un documento de rango 4 a 7 que contradiga una regla de este protocolo es defecto de conformidad y se corrige en el documento de rango menor, nunca en este protocolo por acomodo al texto inferior.

## 2. Mapa de autoridad y precedencia

La autoridad se ordena en siete rangos y una categoría sin rango. El carácter de cada documento y el desempate dentro de su rango se declaran en la tabla siguiente.

| Rango | Documento | Carácter | Desempate dentro del rango |
|---|---|---|---|
| 1 | `docs/constitution.md` | Norma suprema | Documento único del rango |
| 2 | `AGENTS.md` | Norma operativa para agentes | Documento único del rango |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | Norma ejecutable del proceso | Documento único del rango |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | Norma de integración y release | Documento único del rango |
| 5 | `docs/sdd/plantillas/*.md` | Norma de forma de cada artefacto | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md`, este sobre `validation_report.md`, este sobre `informe_analitico.md` y este sobre `informe_auditoria.md` |
| 6 | `specs/NNN-slug/*.md` | Contrato de la feature | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md` y este sobre `validation_report.md` |
| 7 | `src/`, `tools/`, `tests/`, `.opencode/` | Implementación verificable | El código no prevalece sobre norma alguna; su divergencia se corrige en el código |
| Sin rango | Guías de `docs/sdd/`, informes de análisis, informes de auditoría, `README.md`, `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md` | Referencia no normativa; el índice `docs/sdd/README.md` declara el desempate del rango y `CHANGELOG.md` registra G6 | Sin precedencia: no fija reglas |

Reglas de resolución:

1. Entre rangos distintos prevalece el de número menor.
2. Dentro de un rango, el desempate es el orden de precedencia que `docs/sdd/README.md` declara para ese rango.
3. La categoría sin rango no fija reglas: una contradicción con un documento normativo se resuelve a favor del documento normativo y la corrección se aplica en el documento sin rango.
4. Un documento de `docs/sdd/` que no declara rango ni carácter en su encabezado es defecto de conformidad y no sirve para decidir una regla.
5. **Regla de conflicto:** una contradicción entre rangos, o dentro de un rango sin orden declarado, detiene el trabajo y se registra como defecto de la base con documento, sección y valores en conflicto.
6. **Acción ante contradicción:** se corrige primero el soporte de mayor rango y después el de menor rango que quedó desalineado; no se corrige el documento de menor rango para preservar el texto contradictorio.

## 3. Modelo SDD y glosario

El proyecto adopta **SDD Spec-Anchored**: la especificación es el contrato vigente y convive con el código, validándose mutuamente. No se adopta Spec-as-Source ni Spec-First. Cada término del glosario tiene un único significado en la base y se usa con ese significado.

| Término | Significado único |
|---|---|
| spec | Unidad de contrato identificada `SPEC-NNN` que reside en `specs/NNN-slug/` y agrupa sus artefactos. |
| artefacto | Documento de `specs/NNN-slug/` con contrato propio: `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y `validation_report.md`. |
| compuerta | Condición identificada de `G1` a `G6` que habilita el paso a la etapa siguiente; G1, G4 y G6 son aprobaciones humanas. |
| estado | Valor del campo `status` de una spec, tomado del conjunto admitido de §5. |
| propietario | Persona que declara G1, G4 y G6, mantiene la lista de firmantes y escribe la sección protegida; no es un rol de agente. |
| autor | Rol de agente que redacta un artefacto; su coincidencia con el propietario no invalida una aprobación. |
| firmante | Identidad cuya clave pública figura en `docs/sdd/firmantes_autorizados` y cuyo commit firmado acredita una aprobación. |
| evidencia | Salida literal de un comando, extracto o registro verificable que sostiene una afirmación de cumplimiento. |
| rango | Número de 1 a 7 que ordena la autoridad de un documento; el número menor tiene mayor autoridad. |
| carácter | Condición de un documento como norma suprema, norma operativa, norma ejecutable, norma de integración, norma de forma, contrato, implementación verificable o referencia no normativa. |
| inventario | Conjunto de filas de la tabla de `docs/sdd/README.md` que enumera cada archivo del corpus con su carácter, su orden de lectura y su rango. |
| legado | Condición de una spec publicada que conserva su contenido bajo la cláusula de §15 y no se reescribe retroactivamente. |

## 4. Ciclo de siete etapas

El ciclo encadena siete etapas. Una etapa no se abre hasta que la anterior declara su salida y el estado resultante quedó escrito.

| Etapa | Entrada | Salida | Artefacto | Estado resultante | Responsable | Comando |
|---|---|---|---|---|---|---|
| 1. Specify | rama `feat/*` creada e identificador `SPEC-NNN` asignado | contrato de la feature redactado | `spec.md` | `draft` | `planner` | `/sdd-spec` |
| 2. Clarify | `spec.md` en `draft` | ambigüedades resueltas y parches aplicados | `clarify.md` y `spec.md` | `clarified` | `planner` | `/sdd-clarify` |
| 3. Plan | G1 aprobada y spec en `clarified` | arquitectura, contratos y decisiones | `plan.md` | `planned` | `planner` | `/sdd-plan` |
| 4. Tasks | spec en `planned` | tareas atómicas con cobertura completa | `tasks.md` | `tasked` | `planner` | `/sdd-tasks` |
| 5. Implement | G2 verificada y spec en `tasked` | tareas cerradas con evidencia | código de `src/`, `tools/` y `tests/`, y `tasks.md` | `implementing` y después `implemented` | `coder` | `/sdd-implement` |
| 6. Validate | G3 completa y spec en `implemented` | veredicto de convergencia | `validation_report.md` | `validated` | `reviewer` | `/sdd-validate` |
| 7. Release | G4 aprobada y base integrada en `dev` con G5 cumplida | release publicado con tag verificado | `CHANGELOG.md` y `specs/INDEX.md` | `released` | propietario y orquestador | procedimiento de release de `docs/Flujo_de_Trabajo_Git.md` (G5 y G6) |

Reglas de la etapa de implementación:

- Implement aplica TDD estricto en Python y validación-first en scripts `.bat`, conforme al rango 1.
- Cada invocación de implementación ejecuta una tarea pendiente, salvo autorización expresa del propietario.
- Si una tarea exige una ruta fuera de su campo `Archivos`, se detiene y se corrige `tasks.md` antes de continuar.
- Una ambigüedad no registrada detiene la implementación y exige un `AMB-NNN` en `clarify.md`.
- Un cambio de requisito posterior a G1 devuelve la spec a `draft` y exige nueva clarificación.

Las transiciones hacia `cancelled` y hacia `superseded` no son etapas del ciclo: el propietario las declara y §5 fija su evidencia.

## 5. Máquina de estados

**Estados admitidos.** El campo `status` de una spec toma uno de diez valores y ningún otro:

| Estado | Significado |
|---|---|
| `draft` | La spec está redactada y la clarificación no está cerrada. |
| `clarified` | Las ambigüedades están resueltas y los parches aplicados; la aprobación G1 se registra antes de abrir Plan. |
| `planned` | El plan técnico está escrito y G1 sigue vigente. |
| `tasked` | Las tareas están descompuestas con cobertura completa; la verificación G2 se realiza antes de abrir Implement. |
| `implementing` | Al menos una tarea de la spec está en ejecución. |
| `implemented` | Las tareas están cerradas con evidencia y las pruebas en verde; G3 completa. |
| `validated` | El reporte de validación converge al 100 % y G4 está aprobada. |
| `released` | El release está publicado, con G5 y G6 cumplidas y el tag verificado. |
| `cancelled` | La spec quedó abandonada con motivo escrito por el propietario. |
| `superseded` | La spec quedó sustituida por otra, con el destino declarado. |

**Transiciones.** La tabla fija el origen, el destino, el propietario de la transición y la evidencia que la habilita.

| Transición | Origen | Destino | Propietario de la transición | Evidencia habilitante |
|---|---|---|---|---|
| T1 | `draft` | `clarified` | `planner` | `clarify.md` sin casillas pendientes y parches aplicados |
| T2 | `clarified` | `planned` | G1 y `planner` | línea de G1 firmada en `spec.md` y `plan.md` escrito con sus decisiones |
| T3 | `planned` | `tasked` | `planner` | `tasks.md` con los campos obligatorios y cobertura completa de requisitos y casos borde |
| T4 | `tasked` | `implementing` | G2 | verificación de G2 registrada sin hallazgos |
| T5 | `implementing` | `implemented` | G3 | G3 con cada tarea cerrada, su evidencia transcrita y las pruebas en verde |
| T6 | `implemented` | `validated` | `reviewer` y G4 | `validation_report.md` con dictamen `CONVERGIDO` y línea de G4 firmada en `spec.md` |
| T7 | `validated` | `released` | G5 y G6 | integración con `merge --no-ff` en `dev`, tag anotado verificado y línea de G6 firmada en `CHANGELOG.md` |
| T8 | `draft`, `clarified`, `planned` o `tasked` | `cancelled` | propietario | motivo escrito por el propietario y registrado en el historial de la spec |
| T9 | `validated` | `implementing` | propietario | motivo de reapertura escrito y incremento MINOR de la versión |
| T10 | `validated` o `released` | `superseded` | propietario | identificador `SPEC-NNN` de la spec que sustituye y destino declarado |

Una compuerta no es un estado: la aprobación o verificación se registra entre dos etapas y no forma parte de la definición del estado.

**Escritura de estados.** El `planner` escribe la creación de la spec en `draft` y las transiciones T1, T2 y T3. El orquestador escribe las transiciones T4, T5, T6 y T7. El propietario escribe la cancelación, la reapertura y la sustitución, y el orquestador solo las registra cuando el propietario las autoriza por escrito.

**Reglas.** Las transiciones avanzan solo por la tabla; una transición no listada es defecto de conformidad. La reapertura exige motivo, incremento de versión y revalidación completa. Una spec en `cancelled` no se reabre: se redacta una spec nueva.

## 6. Compuertas G1 a G6

G1, G4 y G6 son aprobaciones humanas y su único declarante es el propietario. G2, G3 y G5 son condiciones verificables: el orquestador las verifica y registra el resultado, sin que esa verificación constituya aprobación. Ningún agente declara una aprobación.

| Compuerta | Condición | Evidencia exigida | Declarante | Verificación | Acción ante fallo |
|---|---|---|---|---|---|
| G1 | Clarify cerrado con `spec.md` sin ambigüedades, requisitos en EARS correcto y cada requisito con criterio de aceptación | `clarify.md` cerrado sin casillas pendientes, parches aplicados, línea `Cubre:` completa en cada criterio y línea de aprobación firmada | propietario | `python tools\sdd\validate.py --spec SPEC-NNN --gate G1`, lectura de `clarify.md` y verificación de la firma del commit | la spec permanece en `draft`, no se abre Plan y no se escribe `plan.md` |
| G2 | Tasks cerrado con `plan.md` y `tasks.md` conformes y cobertura del 100 % | `plan.md` con matriz de cobertura y `tasks.md` con requisitos cubiertos, criterio de aceptación y campo de evidencia por tarea | orquestador | `--gate G2` y contraste de la matriz con la lista de requisitos y casos borde | no se abre Implement y no se invoca a `coder` |
| G3 | Implement cerrado con cada tarea completada con evidencia y las pruebas en verde | casillas de tarea marcadas con la evidencia transcrita y salida de la suite en verde | orquestador | `--gate G3` y ejecución de las pruebas declaradas en `tasks.md` | no se abre Validate y no se invoca a `reviewer` |
| G4 | Validate cerrado con reporte convergido al 100 % | `validation_report.md` con matriz completa en `PASADO`, dictamen `CONVERGIDO` y línea de aprobación firmada en `spec.md` | propietario | `--gate G4 --git` y verificación de la firma del commit | la spec permanece en `implemented` y no se integra |
| G5 | Integración en `dev` con `merge --no-ff`, validación posterior y rama de trabajo eliminada | merge con dos padres, validador posterior sin hallazgos y listado de ramas sin la rama integrada | orquestador | `git log --merges -1`, validador posterior y `git branch --list` | la integración se revierte en la rama de trabajo y G5 no se registra |
| G6 | Release autorizado con auditoría de conformidad, tag anotado e `INDEX` y `CHANGELOG` actualizados | línea de aprobación firmada en la entrada del release, informe de auditoría registrado, tag verificado y documentos actualizados | propietario | verificación de la firma, `git cat-file -t`, `git tag -n` y `git rev-parse` del tag | no se crea el tag, no se publica el release y la entrada permanece en `Unreleased` |

## 7. Trazabilidad obligatoria

**Cadena.** La trazabilidad sigue `RF/CB → CA → T → evidencia`. Cada eslabón se materializa en un artefacto y se comprueba con la verificación que declara el plan de la spec.

| Artefacto | Campo obligatorio que sostiene la cadena |
|---|---|
| `spec.md` | cada `RF` y cada `CB` referenciado por al menos un `CA`, y cada `CA` cierra con la línea `Cubre:` |
| `clarify.md` | cada parche declara el requisito o el criterio que modifica |
| `plan.md` | una fila de matriz por requisito y por caso borde, con la verificación asociada |
| `tasks.md` | `Requisitos cubiertos` y `Criterio de aceptación` en cada tarea |
| `validation_report.md` | una fila por requisito con `CA`, prueba o comando, evidencia y estado |

**Prohibiciones.** Requisito sin criterio de aceptación; criterio sin tarea; tarea sin evidencia; fila de matriz sin verificación; criterio que no se materializa en ninguna tarea.

**Cambio de requisito.** Un requisito que cambia después de G1 devuelve la spec a `draft` y exige nueva clarificación. No se ajusta el criterio para acomodar el código implementado.

## 8. Contratos de artefactos

Cada artefacto de una spec declara rango 6. La plantilla de rango 5 fija la forma; este capítulo fija el contenido mínimo. Una plantilla que contradiga este capítulo se corrige en la plantilla.

### 8.1 `spec.md`

- Frontmatter de once campos: `id`, `title`, `status`, `version`, `created`, `updated`, `owner`, `branch`, `release`, `supersedes` y `superseded_by`.
- Secciones obligatorias en este orden: contexto y objetivo, actores y permisos, requisitos funcionales en EARS, requisitos no funcionales, casos borde, fuera de alcance, criterios de aceptación, aprobaciones e historial de cambios.
- Cada criterio de aceptación cierra con una línea `Cubre:` que enumera los identificadores `RF` y `CB` que satisface.
- La sección de aprobaciones contiene dos casillas y ninguna más: G1 y G4.
- El historial de cambios usa las columnas `Versión`, `Fecha` y `Cambio`, y aplica la regla de §9.
- Prohibiciones: rutas de código, clases, SQL y comandos técnicos; casilla de G6; dos formas para un mismo campo.

### 8.2 `clarify.md`

- Un bloque por `AMB-NNN` con descripción, pregunta, respuesta, decisión, fecha UTC y responsable.
- Sección de casos borde nuevos, con constancia expresa de ausencia cuando no los haya.
- Sección de parches aplicados, con casilla por parche y referencia del requisito o criterio afectado.
- Sección de decisiones de negocio.
- Prohibición: dejar una casilla pendiente al cerrar; el cierre de `clarify.md` es condición de G1.

### 8.3 `plan.md`

- Secciones: referencias, naturaleza del entregable, arquitectura, contratos, decisiones `DEC-NNN`, estrategia de testing y matriz de cobertura.
- Cada decisión declara la alternativa descartada y su justificación.
- La matriz de cobertura tiene una fila por `RF` y por `CB`, con el documento o sección que lo implementa y la verificación asociada.
- Prohibiciones: fila de matriz sin verificación; decisión sin alternativa descartada.

### 8.4 `tasks.md`

- Ocho campos por tarea, en este orden: `Dependencias`, `Requisitos cubiertos`, `Criterio de aceptación`, `Archivos`, `Estimación`, `Validación`, `Evidencia` y `Completada`.
- `Estimación` declara un valor entre 15 y 30 minutos.
- `Evidencia` transcribe la salida de la validación al cerrar la tarea.
- Prohibiciones: tarea sin criterio de aceptación; tarea sin campo de evidencia; tarea que toque rutas fuera de su campo `Archivos`.

### 8.5 `validation_report.md`

- Secciones: entorno, matriz de trazabilidad, brechas y dictamen.
- La matriz usa las columnas `Requisito`, `CA`, `Prueba / comando`, `Evidencia` y `Estado`, con `PASADO` como único valor convergente.
- El dictamen usa la casilla `CONVERGIDO` y su pareja `NO CONVERGIDO`.
- Prohibición: casilla, sección o línea de aprobación. El registro de G4 vive en la sección de aprobaciones de `spec.md`.

### 8.6 Informe analítico

- Secciones: encabezado con título, fecha, autor y carácter de referencia no normativa; objeto y alcance; fuentes; procedimiento; análisis; conclusiones; límites.
- Rol habilitado: `documenter`. No crea espacio de identificadores; sus afirmaciones se citan por sección y fecha.
- Prohibición: fijar reglas de obligado cumplimiento.

### 8.7 Informe de auditoría

- Diez secciones: ficha de reproducibilidad, base normativa e inventario, criterio y escalas, matriz de dimensiones, hallazgos, compuertas, veredicto global, hoja de ruta, limitaciones y anexos de evidencia.
- Escala de veredicto de cinco valores: `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`.
- Escala de severidad de cuatro niveles: `Crítica`, `Alta`, `Media` y `Baja`.
- Numeración `AUD-NNN` correlativa por dimensión, con diez números reservados por dimensión y continuación inmediata al último asignado; un número asignado no se reutiliza entre versiones del informe.
- Rol habilitado: auditoría, con lectura de la base y escritura limitada al informe.
- Prohibición: emitir un veredicto sin evidencia citada por sección.

## 9. Identificadores y versionado

**Espacios.** Los espacios son `SPEC-NNN`, `RF-NNN`, `RNF-NNN`, `CB-NNN`, `AMB-NNN`, `CA-NNN`, `T-NNN`, `DEC-NNN` y `AUD-NNN`. Cada identificador usa tres dígitos con ceros a la izquierda, es único dentro de su espacio y no se reutiliza aunque el elemento se cancele. Las compuertas usan `G1` a `G6` y no forman espacio numérico.

**Referencia.** La forma completa es `<SPEC-NNN>/<espacio>-<NNN>`, por ejemplo `SPEC-009/RF-001`. Dentro de la spec se admite la forma corta del espacio.

**Regla de versionado.** Cinco reglas:

1. La redacción inicial de una spec es `0.1.0`.
2. Cada etapa que cambia el contrato incrementa MINOR: clarify, plan, tasks y validación. Con el incremento MINOR, la posición PATCH vuelve a cero.
3. Una corrección editorial sin cambio de requisitos incrementa PATCH.
4. La reapertura de una spec en `validated` incrementa MINOR y registra el motivo en el historial de cambios.
5. Una spec en `released` no se renumera: sus cambios se tramitan por reapertura o por una spec nueva que declara el campo `supersedes`.

**Procedimiento de aplicación.** Se ejecuta en este orden y no admite apreciación del redactor:

1. Identificar el artefacto que cambia y el tipo de cambio: redacción inicial, cambio de contrato, corrección editorial o reapertura.
2. Leer la versión vigente en el frontmatter del artefacto.
3. Aplicar la regla que corresponde al tipo de cambio identificado.
4. Escribir la fila del historial de cambios con versión, fecha y descripción del cambio.
5. Repetir la lectura de la versión escrita: dos revisiones independientes obtienen el mismo número porque el tipo de cambio determina la posición y no el criterio del redactor.

**Prohibiciones.** Renumerar una spec publicada; reutilizar un identificador; declarar una versión que no corresponda al tipo de cambio registrado en el historial.

## 10. EARS y léxico

**Patrones admitidos.** Cada requisito funcional se redacta con uno de cinco patrones:

| Tipo | Patrón |
|---|---|
| Ubicuo | `El sistema DEBE <respuesta>.` |
| Dirigido por evento | `CUANDO <evento>, el sistema DEBE <respuesta>.` |
| Dirigido por estado | `MIENTRAS <estado>, el sistema DEBE <respuesta>.` |
| No deseado | `SI <condición>, ENTONCES el sistema DEBE <respuesta>.` |
| Opcional | `DONDE <característica>, el sistema DEBE <respuesta>.` |

**Requisito complejo.** Se admite una sola combinación de dos disparadores: `MIENTRAS <estado>, CUANDO <evento>, el sistema DEBE <respuesta>.` Cualquier otra combinación se descompone en dos requisitos.

**Umbral.** Cada umbral declara número y unidad, por ejemplo `15 minutos`, `16 GB` o `100 %`. Un requisito con umbral sin unidad es defecto y no se aprueba en G1.

**Términos vetados.** Se veta el uso de los términos siguientes en requisitos, requisitos no funcionales y criterios de aceptación: `TBD`, `TODO`, `por definir`, `etc.`, `y/o`, `apropiado`, `adecuado`, `óptimo`, `según sea necesario` y `cuando sea posible`.

**Detección.** La comprobación busca cada término como subcadena del texto, sin distinguir mayúsculas de minúsculas y sin exigir límite de palabra, de modo que una variante como `apropiadamente` u `óptimos` también se detecta. La detección produce un hallazgo y no una sustitución automática: la corrección la escribe el autor del artefacto.

## 11. Aprobaciones

**Formato.** La línea de registro contiene la cadena exacta `- Approved by: Agent Sebaxtian`. En `spec.md` se escribe como casilla con el identificador de la compuerta, por ejemplo ``- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)``. En `CHANGELOG.md` se escribe como viñeta `- Approved by: Agent Sebaxtian` dentro de la entrada del release. No se admiten variantes del nombre ni de la fecha.

**Ubicación.** G1 y G4 se registran solo en la sección de aprobaciones de `spec.md` de la spec afectada. G6 se registra solo en la entrada del release de `CHANGELOG.md`. Cada compuerta tiene una sola ubicación y `validation_report.md` no porta casilla de aprobación.

**Sección protegida.** La sección de aprobaciones de `spec.md` y la entrada del release de `CHANGELOG.md` solo las modifica el propietario mediante un commit firmado. Ningún agente las escribe, las completa ni las corrige.

**Firma.** El commit que introduce la línea debe estar firmado con una clave cuya clave pública figure en `docs/sdd/firmantes_autorizados`. El archivo usa el formato de lista de firmantes admitidos de Git, con una línea por firmante, identidad y clave pública, comentarios introducidos por `#`, y solo claves públicas; lo mantiene el propietario.

**Verificación.** Se ejecuta en cuatro pasos: localizar el commit que introdujo la línea de aprobación; comprobar que el commit está firmado; verificar la firma contra la lista de firmantes; registrar el resultado en la evidencia de la compuerta.

**Autoría frente a aprobación.** El autor es el rol que redacta y el propietario es quien aprueba. La coincidencia entre ambos no invalida la aprobación: lo que la acredita es la firma del commit.

**Prohibición de autoaprobación.** Ningún agente aprueba su propia spec, su propia implementación ni su propio release, y ningún agente declara una compuerta. Un agente que redacta una línea de aprobación produce un registro sin valor y el caso se trata como incumplimiento.

**Firma ausente.** Si la firma falta, no verifica o la clave no figura en la lista, la compuerta no está aprobada y el caso se registra como incumplimiento.

## 12. Roles y permisos

| Rol | Lectura | Escritura |
|---|---|---|
| Orquestador (`sdd`) | base normativa, specs, código y estado Git | ninguna sobre documentos y código; ejecuta el validador, `git add` y `git commit` de artefactos de control, y lanza subagentes |
| `planner` | base normativa, specs y código | `specs/**` |
| `documenter` | base normativa, specs y código | `docs/**` y `AGENTS.md` |
| `coder` | base normativa, specs, `src/`, `tests/` y `tools/` | `src/`, `tests/`, `tools/` y el cierre de tareas en `tasks.md` |
| `reviewer` | base normativa, specs, código y estado Git | `validation_report.md` de la spec en curso |
| `auditor` | base normativa completa y specs, sin edición de requisitos | el informe de auditoría que produce, conforme a la plantilla de rango 5 |
| Propietario | base normativa completa | sección de aprobaciones de `spec.md`, entrada del release de `CHANGELOG.md` y `docs/sdd/firmantes_autorizados` |

**Documentos de raíz.** `README.md`, `MEMORY.md` y `CHANGELOG.md` los escribe el propietario o su delegado explícito. El orquestador puede redactarlos como delegado con revisión y aprobación del propietario antes de G4. La formalización de la allowlist de agentes para la raíz corresponde al bloque B3.

**Reglas de la matriz.** La denegación explícita prevalece sobre cualquier concesión. La ruta más específica prevalece sobre la más general. Un permiso no se extiende por analogía: la ruta no declarada está denegada. Si dos roles necesitan escribir la misma ruta en una etapa, escribe el rol que `tasks.md` declara para esa tarea y el otro reporta el hallazgo. Ninguna concesión de escritura autoriza a declarar una compuerta.

**Rol de auditoría.** Se declara en este capítulo, en el rango 1 y en `AGENTS.md`, con lectura sobre la base completa, sin permiso de modificar requisitos y sin permiso de aprobar compuertas. Su implementación en `.opencode/` corresponde al bloque B3; mientras no exista, la escritura del informe de auditoría la ejecuta `documenter` bajo la declaración de este rol.

## 13. Integración Git y release

**G5, integración.** Condición: G4 aprobada, spec en `validated` y rama de trabajo integrada en `dev` por Pull Request con `merge --no-ff`. Evidencia: merge con dos padres, validador posterior a la integración y listado de ramas sin la rama. Sin G5 no se integra.

**G6, release.** Condición: G5 cumplida, autorización firmada del propietario, informe de auditoría de conformidad registrado, tag anotado verificado e `specs/INDEX.md` y `CHANGELOG.md` actualizados. Sin G6 no se publica.

**Integración.** `merge --no-ff` es la única forma admitida. Rebase, squash y copia manual están prohibidos. La rama de trabajo se elimina tras confirmar la integración y la eliminación se verifica con `git branch --list <rama>` sin resultado.

**Sincronización.** Antes del empaquetado, `dev` se sincroniza con `main`. La comprobación es `git rev-list --left-right --count dev...main` con salida `0 0`.

**Tag anotado.** Formato `vMAJOR.MINOR.PATCH` y mensaje `Release vX.Y.Z`. Se crea con `git tag -a vX.Y.Z -m "Release vX.Y.Z" <commit>`. Tres verificaciones: `git cat-file -t vX.Y.Z` devuelve `tag`; `git tag -n vX.Y.Z` muestra el mensaje esperado; `git rev-parse vX.Y.Z^{commit}` devuelve el commit objetivo.

**Verificaciones de release.** Son tres y se declaran con el mismo contenido en este capítulo y en el rango 4: `dev` sincronizada con `main`; tag anotado `vMAJOR.MINOR.PATCH` con mensaje `Release vX.Y.Z` y commit objetivo verificado; `specs/INDEX.md` y `CHANGELOG.md` actualizados con la aprobación de G6.

**Registro.** El resultado de G5 y de G6 se registra en `validation_report.md` de la spec publicada y en la entrada del release de `CHANGELOG.md`.

El reporte de validación es append-only después de G4: el registro de G5 y G6 se añade sin alterar la matriz ni el dictamen.

**Protección remota.** `main` y `dev` rechazan commit y push directos; la integración exige Pull Request con `merge --no-ff` y las opciones de squash y rebase están desactivadas en el repositorio remoto.

**Excepciones.** El cambio exclusivamente editorial y las ramas `release/vX-Y-Z` se rigen por §15.

## 14. Contrato del validador

**Comandos.**

- `python tools\sdd\validate.py --all`: valida el corpus de specs y la longitud de `AGENTS.md`.
- `python tools\sdd\validate.py --spec SPEC-NNN`: valida una spec y sus artefactos.
- `python tools\sdd\validate.py --spec SPEC-NNN --gate Gx`: valida la compuerta indicada.
- `python tools\sdd\validate.py --spec SPEC-NNN --gate G4 --git`: añade las comprobaciones de rama, alcance y cuerpo del commit.
- `python tools\sdd\validate.py --next-id`: devuelve el siguiente identificador libre.

**Comprobaciones verificadas.** Frontmatter y campos obligatorios; pertenencia del estado al conjunto de §5; secciones obligatorias de cada artefacto; notación EARS y léxico vetado; unicidad de identificadores; cobertura `RF/CB → CA → T`; dependencias acíclicas; estimaciones entre 15 y 30 minutos; ausencia de rutas técnicas en `spec.md`; `clarify.md` cerrado; reporte convergido al 100 %; consistencia con `specs/INDEX.md`; longitud de `AGENTS.md`; y con `--git`, rama de trabajo, cambios dentro del alcance declarado y cuerpo `Spec: SPEC-NNN` en cada commit de implementación.

**Comprobaciones no verificadas.** La firma del commit de aprobación y la pertenencia de la clave a `docs/sdd/firmantes_autorizados`; la veracidad de la evidencia transcrita; la ejecución real de un script `.bat` o de una suite de pruebas; las tres verificaciones de release de §13; la autosuficiencia del protocolo; la conformidad del régimen completo.

**Códigos de salida.** `0` sin hallazgos; `1` error de validación; `2` error de uso del comando.

**Límite.** Un resultado favorable acredita estructura, coherencia interna, trazabilidad declarada y alcance del cambio. No acredita la aprobación de compuerta alguna, la firma del commit ni la conformidad del régimen, y no sustituye la verificación del propietario.

## 15. Excepciones y legado

**Cambio editorial.** Sin spec se admite solo un cambio exclusivamente editorial: erratas, formato y enlaces, sin alterar reglas, requisitos, comportamiento, configuración ni scripts. Se registra con commit `docs:` o `chore:`.

**Rama de release.** `release/vX-Y-Z` se dedica al empaquetado de `CHANGELOG.md`, `specs/INDEX.md` y el frontmatter de las specs publicadas; no introduce código funcional ni cambios de requisito y se integra por Pull Request con `merge --no-ff`.

**Hotfix.** Exige spec, aunque sea mínima.

**Cláusula de legado.** Las specs publicadas `SPEC-001` a `SPEC-007` conservan su contenido y no se reescriben retroactivamente; su regularización corresponde a una spec posterior y no se ejecuta por edición directa. La base v2 rige para cada spec posterior a `SPEC-007` desde su publicación. Un historial de versiones no derivado de la regla de §9 se conserva y se regulariza en la misma spec de legado.

**Archivo de rama sin integración.** Una rama con commits no integrados puede archivarse. El archivo exige decisión del propietario, registro en `CHANGELOG.md` bajo `Unreleased` y en el Anexo de transición, permanencia local sin publicación, conservación de la referencia y prohibición de integrar sus commits.

## 16. Control de cambios y auditoría de conformidad

**Cambio de la base.** Un cambio de la base normativa exige spec aprobada previa, incremento de la versión del documento afectado y entrada en `CHANGELOG.md` bajo `Unreleased`. Se prohíbe integrar un cambio de la base sin spec aprobada; la única excepción es el cambio exclusivamente editorial de §15.

**Declaración del documento.** Cada documento de la base declara en su encabezado el rango y el carácter, y su versión se registra en la entrada de `CHANGELOG.md` que lo sustituye. Un documento sin declaración de rango y carácter es defecto de conformidad.

**Auditoría de conformidad.** Antes de cada release menor se ejecuta una auditoría de conformidad sobre la base vigente. La ejecuta el rol de auditoría, sigue la plantilla de informe de auditoría de rango 5, se conserva en `docs/sdd/` y su identificador `AUD-NNN` se registra en la entrada del release.

**Prohibición de G6.** No se emite G6 sin informe de auditoría de conformidad registrado. Un release preparado sin ese informe es incumplimiento y se detiene.

**Corrección de significado.** Una corrección que altere el significado de una regla no es editorial: exige spec aprobada y revisión de conformidad.

## Anexo de transición

**Fecha de corte:** `2026-11-14`.

**Regla de sustitución.** Cada documento de la base se sustituye en su ruta y con su nombre. Las versiones anteriores permanecen en el historial Git y no se copian a rutas paralelas. Este Anexo de transición y la entrada `Unreleased` de `CHANGELOG.md` declaran el mismo registro; una divergencia entre ambos se corrige en `CHANGELOG.md`.

| Ruta | Rango | Operación | Estado |
|---|---|---|---|
| `docs/constitution.md` | 1 | Sustitución | Sustituido, versión v2 |
| `AGENTS.md` | 2 | Sustitución | Sustituido, versión v2 |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | Redacción nueva desde cero | Sustituido, versión v2 |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | Sustitución alineada con G5 y G6 | Sustituido |
| `docs/sdd/plantillas/spec.md` | 5 | Sustitución | Sustituido |
| `docs/sdd/plantillas/clarify.md` | 5 | Sustitución | Sustituido |
| `docs/sdd/plantillas/plan.md` | 5 | Sustitución | Sustituido |
| `docs/sdd/plantillas/tasks.md` | 5 | Sustitución con criterio de aceptación y evidencia | Sustituido |
| `docs/sdd/plantillas/validation_report.md` | 5 | Sustitución sin casilla de aprobación | Sustituido |
| `docs/sdd/plantillas/informe_analitico.md` | 5 | Creación | Creado |
| `docs/sdd/plantillas/informe_auditoria.md` | 5 | Creación | Creado |
| `docs/sdd/README.md` | 5 como índice; referencia no normativa en su contenido | Sustitución | Sustituido con tabla de autoridad e inventario |
| `README.md` | Sin rango | Sustitución | Sustituido con el estado real del repositorio |
| `MEMORY.md` | Sin rango | Sustitución | Sustituido sin hechos obsoletos |
| `CHANGELOG.md` | Sin rango | Sustitución | Sustituido con las entradas de `Unreleased` |

**Archivo de datos declarado aparte.** `docs/sdd/firmantes_autorizados` no figura en la tabla: es un archivo de datos nuevo, sin rango y sin carácter normativo propio, que contiene solo las claves públicas de los firmantes autorizados y lo mantiene el propietario.

**Cláusula de legado.** Las specs publicadas `SPEC-001` a `SPEC-007` conservan su contenido y quedan amparadas por la cláusula de §15. Su regularización corresponde a una spec posterior y no se ejecuta por edición directa de los artefactos publicados.

**Archivo de rama.** La rama `feat/gemma-4-26b-a4b-it-qat-gguf` se archiva sin integrar, con dos commits no integrados. Permanece local, no se publica en el remoto y no se integra; la referencia se conserva y su decisión queda registrada en `CHANGELOG.md` bajo `Unreleased` y en este Anexo de transición.
