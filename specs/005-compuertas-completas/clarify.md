# Clarificación - SPEC-005

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados a `spec.md`).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** RF-002 y CB-001 no fijan qué cuenta como celda superada. «PASADO (con observación)» debe considerarse superada, y «PASADO / FALLADO» no. Una regla de «empieza por PASADO» aceptaría ambas.
- **Pregunta:** ¿Qué estados de celda se consideran superados en la matriz de trazabilidad?
- **Respuesta:** Solo cuenta como superada una celda cuyo estado, tras normalizar mayúsculas y espacios, es PASADO, seguido opcionalmente de una observación entre paréntesis. «PASADO (con observación)» es válida. Las celdas que combinan PASADO con otro estado, como «PASADO / FALLADO», no lo son.
- **Decisión:** Se aplica en CB-001 y CA-002 de `spec.md` y en DEC-003 de `plan.md`. Esta forma exacta concreta la decisión del propietario («empiece por PASADO»): la regla literal de prefijo aceptaría «PASADO / FALLADO», que el propietario no pretende aceptar. **Punto a confirmar por el propietario al revisar G1 de la versión 0.2.0.**
- **Precisión asociada (DEC-002 de `plan.md`):** la decisión del propietario («tabla identificada por su cabecera con Estado») se acota a tablas de trazabilidad, cuya primera cabecera es `Requisito`, `Criterio` o `CA`. Una cabecera «Estado» aparece también en tablas de verificación y brechas de SPEC-002 (con valores «CERRADA» o «Conforme»), que no son trazabilidad; aplicar la regla a todas ellas haría fallar SPEC-002 y rompería CB-003. Se acepta la columna `Resultado` porque los fixtures de G4 la usan. Mismo punto de confirmación.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** RF-004 pide declarar cobertura en SPEC-001, que está en estado `released`. No queda claro si esto autoriza a alterar su texto.
- **Pregunta:** ¿Qué puede cambiarse en el `spec.md` de SPEC-001?
- **Respuesta:** Solo se añaden líneas «Cubre:» a sus criterios de aceptación. No se altera el texto de requisitos, casos borde ni criterios, ni el frontmatter, ni los reportes.
- **Decisión:** Se precisa RF-004 en `spec.md` con esa restricción. En CA-004 se exige que el texto sea idéntico a la versión 0.3.0 salvo las líneas añadidas. El mapeo de cobertura se toma del `validation_report.md` de SPEC-001 (DEC-005).
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** RF-005 pide describir la escritura de `sdd`, pero el protocolo §10 lo presenta como «solo lectura» y la descripción real de permisos (AMB-006 de SPEC-002) incluye `git add` y `git commit`.
- **Pregunta:** ¿Cómo debe describirse `sdd` en §10 de `docs/sdd/PROTOCOLO_OPERATIVO.md`?
- **Respuesta:** `sdd` es orquestador de solo lectura sobre artefactos y código, con permiso de bookkeeping Git (`git add` y `git commit`) para los artefactos de control. No escribe artefactos ni código.
- **Decisión:** Se aplica en RF-005 y CA-005 de `spec.md` y en DEC-006 de `plan.md`. Esta descripción es coherente con AMB-006 y DEC-007 de SPEC-002, que enumeran la allowlist de `shell`.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

No se añaden casos borde nuevos. CB-001 y CB-002 de `spec.md` quedan precisados por AMB-001 y AMB-002. CB-003 no cambia.

## Parches aplicados a `spec.md`

- [x] RF-004: restricción de alcance a líneas «Cubre:» añadidas (AMB-002).
- [x] RF-005: descripción de `sdd` como orquestador de solo lectura con bookkeeping Git (AMB-003).
- [x] CB-001: regla de celda superada y caso de «PASADO / FALLADO» (AMB-001).
- [x] CA-002: ejemplos de «PASADO (con observación)» y de «PASADO / FALLADO» (AMB-001).
- [x] CA-004: texto idéntico a la versión 0.3.0 de SPEC-001 salvo «Cubre:» (AMB-002).
- [x] CA-005: capacidad de escritura de `sdd` descrita como bookkeeping Git (AMB-003).
- [x] Frontmatter `status: clarified`, `version: 0.2.0`; G1 registrada; historial 0.2.0.

## Decisiones de negocio

- SPEC-005 no crea un agente nuevo ni cambia permisos de `.opencode/`. La descripción de `sdd` en §10 se alinea con los permisos ya vigentes.
- La advertencia de cobertura RF/CB sigue siendo advertencia (no error). La conversión a error queda fuera de alcance, como indica `spec.md`.
- Los reportes históricos (SPEC-001 a SPEC-004) no se modifican. Su validez se comprueba con la regla nueva (CB-003).

## Nota de confirmación (SPEC-006)

- **Confirmación de AMB-001:** el propietario confirma que solo cuenta como superada una celda PASADO, con paréntesis de observación opcional. NO PASADO, PENDIENTE, PARCIAL y las celdas compuestas con estado negativo son error.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.
