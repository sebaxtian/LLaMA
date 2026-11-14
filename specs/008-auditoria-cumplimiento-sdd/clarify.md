# Clarificación — SPEC-008

## Estado

- [x] Cerrado (AMB resueltos y parches aplicados a `spec.md`).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** La sección «Base normativa y exclusiones» de `spec.md` enumeraba los documentos excluidos y dejaba implícita una base normativa con un recuento fijado de antemano. Un recuento cerrado en la especificación envejece con el corpus, no permite verificar por regla qué documento es norma y contradice la exigencia de reproducibilidad de RNF-003 cuando el inventario real de `docs/sdd/` cambia.
- **Pregunta:** ¿Cómo se determina el conjunto de documentos que la auditoría emplea como norma y qué recuento debe declarar el informe?
- **Respuesta:** La base normativa se define por regla de inclusión y no por un número. Es norma cada documento Markdown de `docs/sdd/` salvo los seis documentos excluidos por nombre: `comparacion_operativa_sdd_actual_vs_objetivo.md`, `diagrama_flujo_ciclo_vida_sdd.md`, `guia_maestra_sdd.md`, `plan_cierre_brechas_sdd.md`, `PROTOCOLO_OPERATIVO.md` y `README.md`. A esa base se suman los documentos de `docs/sdd/plantillas/`. El informe de auditoría debe declarar el inventario real y su recuento en la fecha de corte. No se fija ningún número en la especificación. El recuento «19» empleado en la conversación previa queda descartado.
- **Decisión:** Se ajusta la sección «Base normativa y exclusiones» para expresar la regla de inclusión y remitir el recuento al informe, y se amplía RF-001 con la obligación de declarar el inventario real y su recuento en la fecha de corte. Se amplía CA-001 con la misma exigencia.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `docs/constitution.md` asigna rango normativo al `PROTOCOLO_OPERATIVO.md`, mientras que la especificación lo excluye de la base normativa y lo trata como evidencia de la práctica. Sin una regla explícita existía el riesgo de que la auditoría aplicara el protocolo como criterio de conformidad, o de que resolviera la tensión editando la jerarquía declarada, en contradicción con RF-014 y CB-011.
- **Pregunta:** ¿Qué documentos actúan como norma superior, qué corpus actúa como criterio de conformidad y qué tratamiento recibe la exclusión del protocolo operativo?
- **Respuesta:** La auditoría aplica `docs/constitution.md` y `AGENTS.md` como normas superiores y el corpus normativo de `docs/sdd/` como criterio de conformidad. La exclusión del `PROTOCOLO_OPERATIVO.md` como norma, pese a que la constitución le asigna rango 3, se registra como hallazgo de la dimensión D1 conforme a CB-011. La auditoría no edita documentos ni resuelve la tensión.
- **Decisión:** Se amplía RF-002 para declarar que la exclusión de un documento de rango normativo declarado se registra como hallazgo y no se resuelve reemplazando el criterio de conformidad. La cobertura de CB-011 en CA-001 se conserva.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** La verificación de reproducibilidad de RF-009 y CA-007 exigía citar un commit auditado, pero la rama `feat/auditoria-cumplimiento-sdd` aún no registraba commits y el árbol de trabajo arrastraba cambios anteriores ajenos a la auditoría. La especificación no definía en qué punto se fija el corte ni qué tratamiento reciben esos cambios.
- **Pregunta:** ¿Sobre qué commit se ejecuta la auditoría y qué ocurre con los cambios previos que permanecen sin registrar?
- **Respuesta:** El corte se fija en el HEAD de `feat/auditoria-cumplimiento-sdd` inmediatamente después de registrar `spec.md`, `clarify.md`, `plan.md` y `tasks.md`, es decir, en el commit anterior a la escritura del informe de auditoría. El informe debe citar ese identificador de commit. Los cambios previos sin commitear quedan fuera del periodo auditado y se registran como evidencia de las dimensiones D9 y D10.
- **Decisión:** Se amplía CA-007 para exigir que el commit de corte esté fijado antes de escribir el informe y que los cambios no registrados queden fuera del periodo, y se añade el caso borde CB-012 con cobertura en CA-007.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** Dos de los seis documentos excluidos de la base normativa no están versionados en el repositorio. La especificación no indicaba si esa circunstancia los reintegraba a la base, si debía corregirse durante la auditoría o si constituía evidencia de una dimensión concreta.
- **Pregunta:** ¿Qué tratamiento reciben los documentos excluidos que no están bajo seguimiento de Git?
- **Respuesta:** Permanecen excluidos de la base normativa, se registran como evidencia de la dimensión D10 y la auditoría no los incorpora a Git. Su falta de seguimiento tampoco habilita su corrección ni su eliminación durante la auditoría.
- **Decisión:** No se altera la regla de exclusión de la sección «Base normativa y exclusiones». La observación se documenta como decisión de negocio y se cubre con CB-007 y CA-010, que mantienen la prohibición de escribir fuera del informe.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** La matriz de roles vigente no asigna a ningún rol la redacción de documentación analítica. La Etapa 6 del ciclo exige un informe de auditoría y la especificación no identificaba al ejecutor autorizado, lo que dejaba la implementación sin responsable y con riesgo de que un rol sin permiso de escritura en `docs/` intentara redactarlo.
- **Pregunta:** ¿Qué rol ejecuta la Etapa 6 y cuál es el límite exacto de su escritura?
- **Respuesta:** Ningún rol de la matriz actual está autorizado para redactar documentación analítica. La Etapa 6 la ejecutará el rol `documenter`, único con permiso de escritura en `docs/**`, limitado a crear `docs/sdd/auditoria_cumplimiento_sdd.md`. La ausencia de un rol de auditoría se registra como hallazgo de la dimensión D7. El propietario ratifica esta decisión al aprobar G1.
- **Decisión:** Se mantiene RF-014 como límite de escritura del ejecutor y se cubre la observación con CA-010 y CA-015. La ratificación queda supeditada a la aprobación G1, que no se marca en esta etapa.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** RF-002 exigía aplicar la jerarquía de `docs/constitution.md` sin precisar el efecto de excluir un documento que esa jerarquía declara normativo. La redacción admitía dos lecturas: registrar la exclusión como hallazgo, o emplear el documento excluido como criterio de conformidad por su rango declarado.
- **Pregunta:** ¿La exclusión de un documento de rango normativo declarado obliga a usarlo como criterio de conformidad o se limita a registrarse?
- **Respuesta:** Se registra y no se resuelve. La exclusión de un documento de rango 3 se registra como hallazgo de D1 y no se interpreta como obligación de emplear el `PROTOCOLO_OPERATIVO.md` como criterio de conformidad.
- **Decisión:** Se reformula RF-002 para hacer explícito que la exclusión se registra como hallazgo de D1 y que no altera el criterio de conformidad ni la jerarquía declarada.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-012

SI el árbol de trabajo contiene cambios sin registrar o no existe un commit de corte fijado, ENTONCES la auditoría DEBE fijar el commit de corte antes de escribir el informe, DEBE excluir del periodo auditado los cambios no registrados y DEBE consignarlos como evidencia de las dimensiones D9 y D10.

## Parches aplicados a `spec.md`

- [x] Frontmatter: `status` actualizado a `clarified`, `version` incrementada a `0.2.0` y `updated` sincronizado a 2026-11-14 (AMB-001 a AMB-006).
- [x] «Base normativa y exclusiones»: sustitución del recuento implícito por la regla de inclusión del corpus, con remisión del inventario y del recuento al informe de auditoría (AMB-001).
- [x] RF-001: obligación de acompañar el inventario real de documentos normativos y su recuento en la fecha de corte (AMB-001).
- [x] RF-002: explicitación de que la exclusión de un documento de rango normativo declarado se registra como hallazgo de D1 y no se resuelve, sin reemplazar el criterio de conformidad (AMB-002, AMB-006).
- [x] CB-012: incorporación del caso borde de corte de auditoría con árbol de trabajo sucio o commit no fijado, con cambios no registrados fuera del periodo auditado (AMB-003).
- [x] CA-001: ampliación para exigir el inventario real y su recuento en la fecha de corte, conservando la línea `Cubre:` con `RF-001`, `RF-002`, `CB-007` y `CB-011` (AMB-001, AMB-002).
- [x] CA-007: ampliación para exigir el commit de corte fijado antes de la escritura del informe y la exclusión de los cambios no registrados, con `Cubre:` ampliada a `RF-009` y `CB-012` (AMB-003).
- [x] Historial de cambios: registro de la versión 0.2.0 tras la etapa de clarificación (AMB-001 a AMB-006).

## Decisiones de negocio

- La base normativa se determina por regla de inclusión y nunca por un recuento fijado en la especificación; el recuento es un dato del informe y se declara en la fecha de corte para que un tercero pueda reproducirlo.
- El commit de corte es el único punto de referencia temporal de la auditoría: los cambios que no estén registrados en él quedan fuera del periodo auditado y solo pueden citarse como evidencia de desviación en D9 y D10.
- La auditoría no resuelve tensiones normativas: registra la exclusión de documentos de rango declarado como hallazgo de D1 y mantiene intacta la jerarquía de `docs/constitution.md`.
- Los documentos excluidos sin seguimiento de Git permanecen excluidos y sin incorporación al repositorio; su estado se registra como evidencia de D10.
- La ejecución de la Etapa 6 corresponde al rol `documenter`, con escritura limitada a `docs/sdd/auditoria_cumplimiento_sdd.md`, y la ausencia de un rol de auditoría se registra como hallazgo de D7. La ratificación formal queda en la aprobación G1 del propietario.
- El estado `clarified` se refleja de forma simultánea en `spec.md` y en `specs/INDEX.md`; la aprobación G1 permanece pendiente y no se marca en esta etapa.
