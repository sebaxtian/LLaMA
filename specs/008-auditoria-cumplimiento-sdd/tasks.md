# Tareas — SPEC-008

## Regla de ejecución

La Etapa 6 de esta especificación la ejecuta el rol `documenter` (DEC-005), único rol con permiso de escritura en `docs/**`. Su escritura se limita a crear `docs/sdd/auditoria_cumplimiento_sdd.md` (RNF-001, RF-014).

Regla de registro que el orquestador aplica sin improvisar:

1. `documenter` redacta el informe y no edita `specs/`; por tanto no marca casillas ni escribe evidencia en este archivo.
2. El rol `planner` registra la casilla `- [x] Completada.` y el bloque de evidencia de cada tarea, después de recibir el reporte del implementador con la salida de la validación en estado correcto.
3. `documenter` tiene `shell *` denegado: los comandos declarados en `**Validación:**` los ejecuta la sesión orquestadora, y su salida literal se adjunta al reporte que recibe el `planner` para el registro.
4. Una casilla se marca solo cuando la validación de la tarea se cumple; una validación fallida obliga a corregir el informe y a repetir la comprobación antes del registro.
5. El recuento de `## Progreso` se actualiza en el mismo acto de registro de cada casilla.
6. La auditoría no corrige artefactos auditados: una solicitud de corrección se rechaza y se remite a una especificación posterior (CB-010, RF-014).
7. El control de alcance de la tarea `T-026` cierra la etapa: entrega al rol `reviewer` el commit de corte, la tabla de consultas y el resultado de la batería V1 a V23.

## Referencias

- `spec.md`: `SPEC-008`, versión 0.4.0, estado `tasked`, compuerta G1 aprobada por `Agent Sebaxtian` el 2026-11-14.
- `clarify.md`: `AMB-001` a `AMB-006` resueltos y caso borde `CB-012` incorporado.
- `plan.md`: arquitectura de doce secciones, modelo de evidencia E1 a E5, esquemas de tablas y decisiones `DEC-001` a `DEC-010`.
- Entregable de la Etapa 6: `docs/sdd/auditoria_cumplimiento_sdd.md` como documento único (RNF-001).
- Plantilla aplicada: `docs/sdd/plantillas/tasks.md`.
- Guías consultadas: `docs/sdd/guia_tasks_md.md` y `docs/sdd/guia_fase_implement_tdd.md`.

## Progreso

- [ ] 0 de 26 tareas completadas.

## Orden de ejecución y dependencias

- Grupo 1 (corte y base normativa): `T-001` sin dependencias; `T-002` depende de `T-001`; `T-003` depende de `T-002`; `T-004` depende de `T-003`; `T-005` depende de `T-002`.
- Grupo 2 (evaluación de dimensiones): `T-006` depende de `T-004` y `T-005`; `T-007` depende de `T-006`; `T-008` depende de `T-007`; `T-009` depende de `T-008`; `T-010` depende de `T-009`; `T-011` depende de `T-010`; `T-012` depende de `T-011`; `T-013` depende de `T-012`; `T-014` depende de `T-013`; `T-015` depende de `T-014`.
- Grupo 3 (consolidación): `T-016` depende de `T-015`; `T-017` depende de `T-016`; `T-018` depende de `T-017`; `T-019` depende de `T-018`; `T-020` depende de `T-019`.
- Grupo 4 (cierre y entrega): `T-021` depende de `T-020`; `T-022` depende de `T-021`; `T-023` depende de `T-022`; `T-024` depende de `T-023`; `T-025` depende de `T-024`; `T-026` depende de `T-025`.

El grafo de dependencias es acíclico y cada arista apunta a una tarea existente de este archivo.

## Tareas

### T-001: Verificación del estado de partida y lista de cambios previos

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-009`, `RF-014`, `CB-012`, `RNF-003`.
- **Archivos:** ninguno: consultas de solo lectura sobre el repositorio; el informe no se crea en esta tarea.
- **Estimación:** 25 min.
- **Validación:**
  1. `git rev-parse HEAD` devuelve un hash hexadecimal de 40 caracteres y coincide con el HEAD de la rama `feat/auditoria-cumplimiento-sdd`.
  2. `git show --stat --oneline HEAD` lista `spec.md`, `clarify.md`, `plan.md` y `tasks.md` de `specs/008-auditoria-cumplimiento-sdd/` entre los archivos del commit candidato a corte.
  3. `git status --short` se transcribe literal en el reporte como lista de cambios previos, con el número de entradas contadas y la indicación de que queda fuera del periodo auditado (CB-012).
  4. `python tools\sdd\validate.py --spec SPEC-008 --gate G2` devuelve código de salida `0`.
- [ ] Completada.

### T-002: Fijación del commit de corte y sección 1 de reproducibilidad

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-009`, `CB-012`, `RNF-003`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. Existe `docs/sdd/auditoria_cumplimiento_sdd.md` y su encabezado `## 1. Ficha de reproducibilidad` abre el informe (DEC-009).
  2. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^### 1\.[123] ').Count` devuelve `3`: tabla de corte, tabla de entorno y tabla de consultas.
  3. `git rev-parse HEAD` coincide carácter por carácter con el hash completo escrito en la tabla de corte, y el hash abreviado escrito es su prefijo de siete caracteres (V13).
  4. La tabla de consultas registra al menos `git rev-parse HEAD` y `git status --short` con su salida y su código de salida, y una frase declara que los cambios no registrados quedan fuera del periodo auditado y se consignan en D9 y D10.
  5. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^## ').Count` devuelve `1`: el cuerpo del informe no se inicia en esta tarea.
- [ ] Completada.

### T-003: Sección 2, jerarquía, regla de inclusión e inventario calculado

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `CB-009`, `RNF-003`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. Existe `## 2. Base normativa e inventario` con las subsecciones `2.1 Jerarquía aplicada`, `2.2 Regla de inclusión` y `2.3 Inventario calculado`.
  2. La subsección 2.1 cita con `ruta:línea` el rango de `docs/constitution.md` como norma suprema y el de `AGENTS.md` como rango inmediatamente inferior (DEC-003).
  3. El recuento declarado en 2.3 coincide con el recalculado por la regla de DEC-001: `$x = @('comparacion_operativa_sdd_actual_vs_objetivo.md','diagrama_flujo_ciclo_vida_sdd.md','guia_maestra_sdd.md','plan_cierre_brechas_sdd.md','PROTOCOLO_OPERATIVO.md','README.md'); (Get-ChildItem docs\sdd -Filter *.md -File | Where-Object { $_.Name -notin $x }).Count + (Get-ChildItem docs\sdd\plantillas -Filter *.md -File).Count` devuelve el mismo número.
  4. La subsección 2.3 enumera cada documento incluido con su ruta relativa y declara la fecha de corte del recuento (V22).
- [ ] Completada.

### T-004: Sección 2, documentos excluidos y artefactos de evidencia de práctica

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-002`, `CB-007`, `CB-011`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. `@('comparacion_operativa_sdd_actual_vs_objetivo.md','diagrama_flujo_ciclo_vida_sdd.md','guia_maestra_sdd.md','plan_cierre_brechas_sdd.md','PROTOCOLO_OPERATIVO.md','README.md') | ForEach-Object { (Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern ([regex]::Escape($_))).Count }` devuelve seis valores mayores o iguales que `1` (V22).
  2. La subsección `2.4 Documentos excluidos` clasifica cada uno de los seis documentos como referencia y declara que no se emplea como criterio de conformidad (CB-007).
  3. La subsección `2.5 Artefactos de evidencia de práctica` enumera al menos `docs/sdd/PROTOCOLO_OPERATIVO.md`, `tools/sdd/validate.py`, `.opencode/agents/`, `specs/` y el historial de Git, con la clase E3 o E4 que corresponde (DEC-003).
  4. Una frase registra que la exclusión de `docs/sdd/PROTOCOLO_OPERATIVO.md` como norma, pese a su rango declarado en la constitución, se remite al hallazgo de D1 de la sección 5 (CB-011) y no modifica la jerarquía de 2.1.
- [ ] Completada.

### T-005: Sección 3, criterio de evaluación, escalas y regla de agregación

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-010`, `RNF-004`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. Existe `## 3. Criterio de evaluación y escalas` con las subsecciones `3.1 Regla de evaluación por dimensión`, `3.2 Escala de veredicto`, `3.3 Escala de severidad` y `3.4 Regla de agregación` (V23).
  2. La subsección 3.2 declara los cinco valores `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`; la 3.3 declara los cuatro niveles `Crítica`, `Alta`, `Media` y `Baja`.
  3. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| [1-6] \|').Count` devuelve `6`: la tabla de agregación reproduce las seis reglas ordenadas de DEC-002.
  4. La subsección 3.1 declara la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL`, `CONFORME` de DEC-008 y no evalúa ninguna dimensión.
- [ ] Completada.

### T-006: Sección 4, estructura de la matriz y fila D1 con sus hallazgos

- **Dependencias:** `T-004`, `T-005`.
- **Requisitos cubiertos:** `RF-002`, `RF-003`, `CB-008`, `CB-009`, `CB-011`, `RNF-002`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. Existe `## 4. Matriz de dimensiones D1 a D10` con la cabecera de cinco columnas del esquema de `plan.md`: dimensión, objeto, veredicto, justificación y hallazgos asociados.
  2. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D1 \|').Count` devuelve `1` y el veredicto de la fila pertenece a la escala de 3.2.
  3. La justificación de la fila D1 cita al menos una ubicación con `ruta:línea` y una ausencia acreditada con su comando, y la columna de hallazgos asociados referencia identificadores del rango `AUD-001` a `AUD-010` (DEC-006, RNF-002).
  4. Existe `## 5. Hallazgos` con un bloque `### AUD-NNN` por hallazgo de D1 y siete campos fijos: dimensión, veredicto, severidad, norma incumplida, evidencia, efecto observado y remediación propuesta.
  5. El bloque que registra la exclusión del protocolo operativo pertenece a D1 e indica el rango 3 de la constitución sin alterar la jerarquía (CB-011), y la diferencia entre inventario declarado e inventario real queda registrada como hallazgo de D1 (CB-009).
- [ ] Completada.

### T-007: Fila D2 y hallazgos del ciclo de siete etapas

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `CB-005`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D2 \|').Count` devuelve `1` y la fila se inserta entre D1 y el final de la tabla de la sección 4.
  2. La fila contrasta la etapa declarada, su artefacto de salida y el estado resultante observado, con al menos una cita de clase E1 y una de clase E2 o E3 (DEC-003).
  3. Existe una entrada `### AUD-011` a `AUD-020` por divergencia detectada, con los siete campos fijos.
  4. La salida del validador determinista se cita como evidencia de práctica y cualquier divergencia frente a la norma documental queda registrada como hallazgo de D2 (CB-005).
- [ ] Completada.

### T-008: Fila D3 y hallazgos de contratos de artefactos

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `CB-001`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D3 \|').Count` devuelve `1` y la fila contrasta los campos y secciones obligatorias de cada contrato con los artefactos observados.
  2. Cada ausencia dentro del alcance de D3 se cita como ausencia verificable con el comando que la demuestra, sin crear el artefacto (CB-001).
  3. Los hallazgos de D3 se registran en el rango `AUD-021` a `AUD-030` con los siete campos fijos.
- [ ] Completada.

### T-009: Fila D4 y evidencia de las compuertas G1 a G6

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-004`, `CB-003`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D4 \|').Count` devuelve `1` y la fila resume el resultado de las seis compuertas.
  2. La evidencia de cada compuerta procede de la sección de aprobaciones de cada spec, de su reporte de validación o de `specs/INDEX.md`, con `ruta:línea`, y la falta de evidencia conservada se escribe como `Sin evidencia conservada` (CB-003).
  3. Ninguna compuerta con evidencia ausente queda calificada `CONFORME` por la existencia del estado liberado (CB-003).
  4. Los hallazgos de D4 se registran en el rango `AUD-031` a `AUD-040` con los siete campos fijos y la tabla de la sección 6 queda pendiente para `T-016`.
- [ ] Completada.

### T-010: Fila D5 y hallazgos de la cadena de trazabilidad

- **Dependencias:** `T-009`.
- **Requisitos cubiertos:** `RF-005`, `CB-002`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D5 \|').Count` devuelve `1` y la fila declara el estado de la cadena RF/CB → CA → T → evidencia → commit → merge → release en cada spec publicada.
  2. Cada eslabón ausente consta como hallazgo del rango `AUD-041` a `AUD-050` y la cadena no se completa por inferencia (CB-002).
  3. La fila cita la línea `Cubre:` del criterio y la matriz de cobertura del plan como fuentes de verificación, con `ruta:línea`.
  4. La tabla de la sección 7 queda pendiente para `T-019` y la fila D5 declara esa remisión.
- [ ] Completada.

### T-011: Fila D6 y contraste del modelo de estados

- **Dependencias:** `T-010`.
- **Requisitos cubiertos:** `RF-018`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D6 \|').Count` devuelve `1` y la fila contrasta cada estado observado en las specs con el modelo de estados declarado.
  2. Cada transición no permitida figura como hallazgo del rango `AUD-051` a `AUD-060`, con el estado de origen, el estado de destino y la referencia observada.
  3. La fila cita el frontmatter de cada spec y `specs/INDEX.md` con `ruta:línea` como evidencia del estado observado.
- [ ] Completada.

### T-012: Fila D7 y contraste de roles y permisos

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RF-019`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D7 \|').Count` devuelve `1` y la fila contrasta el permiso declarado por rol con la operación registrada.
  2. Cada diferencia entre permiso declarado y operación observada figura como hallazgo del rango `AUD-061` a `AUD-070`, incluida la ausencia de un rol de auditoría declarada en AMB-005.
  3. La evidencia de la operación observada se cita con `ruta:línea` o con un comando y su salida; la falta de atribución consta como limitación para la sección 11 (RNF-002).
- [ ] Completada.

### T-013: Fila D8 y suficiencia de la evidencia de verificación

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RNF-002`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D8 \|').Count` devuelve `1` y la fila evalúa existencia, suficiencia y reproducibilidad de la prueba declarada por cada spec.
  2. Cada afirmación de la fila cita evidencia y ninguna queda sostenida por apreciación sin cita (RNF-002).
  3. Los hallazgos de D8 se registran en el rango `AUD-071` a `AUD-080`; los elementos sin prueba disponible se remiten a la sección 11.
- [ ] Completada.

### T-014: Fila D9 y desviaciones de Git del periodo

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-017`, `CB-006`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D9 \|').Count` devuelve `1` y la fila evalúa nomenclatura de ramas, modalidad de fusión, tags y registro de cambios.
  2. Cada desviación aporta el comando de Git ejecutado con su salida y su código de salida, y el historial permanece sin reescritura (CB-006).
  3. Los hallazgos de D9 se registran en el rango `AUD-081` a `AUD-090`; los cambios previos al corte se citan como evidencia de D9 conforme a CB-012.
- [ ] Completada.

### T-015: Fila D10, cierre de la matriz y control de las diez dimensiones

- **Dependencias:** `T-014`.
- **Requisitos cubiertos:** `RF-003`, `CB-004`, `CB-005`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| D(10|[1-9]) \|').Count` devuelve `10` en orden D1 a D10, sin omisiones ni filas fusionadas (V5).
  2. Cada fila contiene uno de los cinco valores de veredicto y una justificación con al menos una cita (V7).
  3. La fila D10 registra las contradicciones entre documentos normativos con el rango de cada documento y la resolución aplicable según la jerarquía, sin editar documento (CB-004), y toda divergencia del validador frente a la norma consta en D2 o en D10 (CB-005).
  4. Los hallazgos de D10 se registran en el rango `AUD-091` a `AUD-099` y la dimensión sin objeto evaluable queda calificada `NO APLICA` con su justificación (CB-008).
- [ ] Completada.

### T-016: Sección 6, evaluación de compuertas G1 a G6

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-004`, `CB-003`, `RNF-002`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. Existe `## 6. Evaluación de compuertas G1 a G6` y `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| G[1-6] \|').Count` devuelve `6` (V6).
  2. Cada fila presenta las seis columnas del esquema de `plan.md` con contenido y un resultado de la escala de 3.2 (V11).
  3. Cada compuerta sin evidencia conservada queda calificada `NO VERIFICABLE` y su fila se remite a la sección 11 (CB-003).
  4. La fila D4 de la sección 4 coincide con el resultado agregado de la tabla; si difiere, se corrige la fila D4 y se anota la corrección en el reporte de la tarea.
- [ ] Completada.

### T-017: Sección 5, tabla consolidada de hallazgos

- **Dependencias:** `T-016`.
- **Requisitos cubiertos:** `RF-007`, `RNF-007`, `CB-004`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. La tabla consolidada abre la sección 5, antes del primer bloque `### AUD-`, con las siete columnas del esquema de `plan.md` y sin celdas vacías (V8).
  2. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| AUD-').Count` coincide con `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^### AUD-').Count` (V9).
  3. La columna de dimensión, la de severidad y la de veredicto permiten el recuento determinista por dimensión y por severidad (RNF-007).
  4. Cada identificador de la tabla es único y pertenece al rango de su dimensión o al excedente declarado por DEC-006.
- [ ] Completada.

### T-018: Detalle de hallazgos, numeración y correspondencia de remediaciones

- **Dependencias:** `T-017`.
- **Requisitos cubiertos:** `RF-008`, `RNF-005`, `RNF-006`, `CB-001`, `CB-006`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. Cada bloque `### AUD-NNN` contiene los siete campos fijos y su campo de evidencia cita `ruta:línea` o un comando con su salida (RF-008).
  2. La secuencia de identificadores es creciente por dimensión, sin repetición y sin reutilización entre versiones del informe (RNF-005).
  3. Cada hallazgo declara al menos una remediación propuesta con bloque B1 a B4 y clasificación, y cada remediación referencia su `AUD-NNN` de origen (RNF-006).
  4. Las ausencias constan como ausencia citada y su bloque indica que el artefacto no se creó (CB-001); las desviaciones de Git conservan la referencia observable sin reescribir historial (CB-006).
- [ ] Completada.

### T-019: Sección 7, trazabilidad por spec publicada

- **Dependencias:** `T-018`.
- **Requisitos cubiertos:** `RF-005`, `CB-002`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. Existe `## 7. Trazabilidad por spec` con la tabla de nueve columnas del esquema de `plan.md` y una fila por requisito de `SPEC-001` a `SPEC-007`.
  2. Ninguna celda queda vacía; la ausencia se escribe como `AUSENTE` acompañada del `AUD-NNN` que la registra (V12).
  3. Cada fila recorre la cadena RF/CB → CA → T → evidencia → commit → merge → release y el eslabón faltante se declara sin completar la cadena por inferencia (CB-002).
  4. Los hallazgos citados en la columna de eslabón faltante existen en la sección 5.
- [ ] Completada.

### T-020: Sección 8, revisión retrospectiva de SPEC-001 a SPEC-007

- **Dependencias:** `T-019`.
- **Requisitos cubiertos:** `RF-006`, `CB-001`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. Existe `## 8. Revisión retrospectiva` con siete bloques de nivel 3, uno por spec de `SPEC-001` a `SPEC-007`, en orden ascendente.
  2. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^### SPEC-00[1-7]').Count` devuelve `7`.
  3. Cada bloque declara un veredicto individual de la escala de 3.2 y los identificadores de hallazgo que lo sostienen.
  4. Cada artefacto inexistente o incompleto se cita como ausencia verificable y el informe no crea el artefacto (CB-001).
- [ ] Completada.

### T-021: Sección 9, veredicto global y constancia de rechazo de correcciones

- **Dependencias:** `T-020`.
- **Requisitos cubiertos:** `RF-011`, `CB-010`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. Existe `## 9. Veredicto global` y el texto enuncia la regla de agregación aplicada por su número de orden de 3.4, enumera las dimensiones que la activan y declara el resultado.
  2. El veredicto global pertenece a la escala de 3.2 y es congruente con las diez filas de la sección 4 (RF-011).
  3. La sección contiene la constancia de rechazo de cualquier solicitud de corrección de un artefacto auditado, remitida a una especificación posterior (CB-010).
  4. Un tercero puede repetir la aplicación de la regla desde la tabla de 3.4 y las filas de la sección 4 sin consultar otra fuente (RNF-003).
- [ ] Completada.

### T-022: Sección 10, hoja de ruta B1 a B4

- **Dependencias:** `T-021`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `RNF-006`, `CB-010`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. Existe `## 10. Hoja de ruta` organizada exclusivamente en los bloques `B1 base normativa`, `B2 mecanismo de control`, `B3 práctica operativa` y `B4 trazabilidad profunda`.
  2. `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^\| B[1-4] \|').Count` es mayor o igual que el número de hallazgos registrados en la tabla consolidada (V14).
  3. Cada fila de remediación declara bloque, acción, `AUD-NNN` de origen y una clasificación igual a `editorial`, `requiere spec` o `proceso` (RF-013).
  4. Cada `AUD-NNN` de la sección 5 aparece al menos una vez en la tabla de remediaciones (RNF-006, V10).
- [ ] Completada.

### T-023: Sección 11, limitaciones y elementos no verificables

- **Dependencias:** `T-022`.
- **Requisitos cubiertos:** `RF-016`, `CB-001`, `CB-008`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. Existe `## 11. Limitaciones y elementos no verificables` con una entrada por cada dimensión `NO VERIFICABLE` y por cada compuerta marcada `Sin evidencia conservada` (V21).
  2. Cada entrada declara la causa de la imposibilidad, el artefacto que faltaría para verificar y la dimensión afectada (RF-016).
  3. Cada dimensión `NO APLICA` conserva la justificación de ausencia de objeto evaluable (CB-008) y cada ausencia citada en la sección 5 figura en esta sección (CB-001).
- [ ] Completada.

### T-024: Sección 12, anexos de evidencia

- **Dependencias:** `T-023`.
- **Requisitos cubiertos:** `RF-008`, `CB-005`, `RNF-003`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. Existe `## 12. Anexos de evidencia` con al menos `12.1 Inventario calculado`, `12.2 Salida del validador determinista`, `12.3 Extractos de historial Git` y `12.4 Mapa de rangos de hallazgos`.
  2. Cada cita extensa reproduce la ruta con línea y el extracto literal, y cada consulta reproduce su comando con la salida y el código de salida (RF-008, V19).
  3. La salida del validador se reproduce íntegra y su tratamiento es el de evidencia de práctica (CB-005).
  4. `12.4` registra el rango real empleado por dimensión, incluido el excedente que DEC-006 autoriza.
- [ ] Completada.

### T-025: Batería de verificación V1 a V23 sobre el informe

- **Dependencias:** `T-024`.
- **Requisitos cubiertos:** `RF-014`, `RF-015`, `RNF-001`, `RNF-003`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python tools\sdd\validate.py --spec SPEC-008 --gate G2` devuelve código `0` (V1, ejecución estructural; la ejecución con `--gate G3` se realiza en `T-026` cuando la totalidad de las casillas quede registrada).
  2. `python tools\sdd\validate.py --all` devuelve código `0` (V2).
  3. `Test-Path docs\sdd\auditoria_cumplimiento_sdd.md` devuelve `True` (V3) y `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^## ').Count` devuelve `12` (V4).
  4. Se ejecuta la batería completa V5 a V23 del apartado «Estrategia de testing» de `plan.md` y el reporte enumera las 23 comprobaciones con su estado, su comando y su salida.
  5. `git status --short` no muestra archivos distintos del informe respecto de la lista de cambios previos de `T-001` (V15), y la búsqueda de léxico ambiguo no devuelve coincidencias (V17).
  6. El informe no contiene apartados dedicados a rendimiento, benchmarks, calidad de código ni lógica interna del validador (V16), y `(Select-String -Path docs\sdd\auditoria_cumplimiento_sdd.md -Pattern '^## ').Count` sigue siendo `12` tras las correcciones (RNF-001).
- [ ] Completada.

### T-026: Cierre de alcance y traspaso al rol reviewer

- **Dependencias:** `T-025`.
- **Requisitos cubiertos:** `RF-014`, `CB-010`, `RNF-003`.
- **Archivos:** `docs/sdd/auditoria_cumplimiento_sdd.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. `git status --short` muestra como única creación de esta etapa `docs/sdd/auditoria_cumplimiento_sdd.md`, y las modificaciones restantes coinciden con la lista de cambios previos de `T-001` (V15).
  2. El paquete de traspaso enumera el hash del commit de corte, la tabla de consultas de la sección 1 y el resultado de V1 a V23, con el muestreo de DEC-010 pendiente para el rol `reviewer`.
  3. Tras el registro de las casillas por el rol `planner`, `python tools\sdd\validate.py --spec SPEC-008 --gate G3` devuelve código `0` y `python tools\sdd\validate.py --all` devuelve código `0`.
  4. El informe no corrige ningún artefacto auditado y la constancia de rechazo de correcciones permanece en las secciones 9 o 10 (RF-014, CB-010).
  5. `git rev-parse HEAD` conserva el hash citado en la sección 1 y ninguna consulta del informe se apoya en un commit posterior al corte (RNF-003).
- [ ] Completada.

## Matriz de cobertura RF/CB → CA → T

| Requisito | Criterio de aceptación | Tareas |
|---|---|---|
| `RF-001` | `CA-001` | `T-003` |
| `RF-002` | `CA-001` | `T-003`, `T-004`, `T-006` |
| `RF-003` | `CA-002` | `T-006`, `T-015` |
| `RF-004` | `CA-003` | `T-009`, `T-016` |
| `RF-005` | `CA-004` | `T-010`, `T-019` |
| `RF-006` | `CA-005` | `T-020` |
| `RF-007` | `CA-006` | `T-017` |
| `RF-008` | `CA-006` | `T-018`, `T-024` |
| `RF-009` | `CA-007` | `T-001`, `T-002` |
| `RF-010` | `CA-008` | `T-005` |
| `RF-011` | `CA-008` | `T-021` |
| `RF-012` | `CA-009` | `T-022` |
| `RF-013` | `CA-009` | `T-022` |
| `RF-014` | `CA-010` | `T-001`, `T-025`, `T-026` |
| `RF-015` | `CA-011` | `T-025` |
| `RF-016` | `CA-012` | `T-023` |
| `RF-017` | `CA-013` | `T-014` |
| `RF-018` | `CA-014` | `T-011` |
| `RF-019` | `CA-015` | `T-012` |
| `CB-001` | `CA-005` | `T-008`, `T-018`, `T-020`, `T-023` |
| `CB-002` | `CA-004` | `T-010`, `T-019` |
| `CB-003` | `CA-003` | `T-009`, `T-016` |
| `CB-004` | `CA-017` | `T-015`, `T-017` |
| `CB-005` | `CA-016` | `T-007`, `T-024` |
| `CB-006` | `CA-013` | `T-014`, `T-018` |
| `CB-007` | `CA-001` | `T-004` |
| `CB-008` | `CA-008` | `T-006`, `T-023` |
| `CB-009` | `CA-018` | `T-003`, `T-006` |
| `CB-010` | `CA-010` | `T-021`, `T-022`, `T-026` |
| `CB-011` | `CA-001` | `T-004`, `T-006` |
| `CB-012` | `CA-007` | `T-001`, `T-002` |
| `RNF-001` | `CA-010` | `T-025` |
| `RNF-002` | `CA-006` | `T-006`, `T-013`, `T-016` |
| `RNF-003` | `CA-007` | `T-001`, `T-002`, `T-003`, `T-021`, `T-025`, `T-026` |
| `RNF-004` | `CA-008` | `T-005`, `T-021` |
| `RNF-005` | `CA-006` | `T-018` |
| `RNF-006` | `CA-009` | `T-018`, `T-022` |
| `RNF-007` | `CA-006` | `T-017` |

## Estimaciones

- Estimación mínima: 20 min. Estimación máxima: 30 min. Estimación media: 25,6 min.
- Tiempo total de la Etapa 6: 665 min, equivalentes a 11 h 5 min de trabajo efectivo.
- Tarea más extensa: `T-006`, `T-009`, `T-010`, `T-015`, `T-016`, `T-018`, `T-019` y `T-025`, con 30 min cada una.
