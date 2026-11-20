# Acta de ratificación histórica

*Acto del propietario. Ratifica las violaciones históricas del régimen que no admiten reparación retroactiva, con efecto limitado al régimen y sin alterar el contenido publicado.*

## 1. Fecha y autoridad

- Fecha: 2026-11-21 (UTC).
- Autoridad: `Agent Sebaxtian`, propietario del régimen.
- Clave de firma: la declarada en `docs/sdd/firmantes_autorizados`.
- Carácter: acto de ratificación, no de aprobación de compuerta.

## 2. Alcance

El acta ratifica las modificaciones que se introdujeron sobre artefactos ya publicados fuera del procedimiento de firma vigente:

- commit `494db2e`, que añadió la cita de auditoría a la entrada del release `v0.7.0` en `CHANGELOG.md`;
- commit `564bac4`, que modificó la entrada publicada `v0.7.0` de `CHANGELOG.md`, la fila T7 de `specs/014-cierre-observaciones-finales/spec.md` y la nota de cierre de `specs/013-cierre-reauditoria-conformidad/validation_report.md`.

Las tres rutas afectadas son `CHANGELOG.md`, `specs/014-cierre-observaciones-finales/spec.md` y `specs/013-cierre-reauditoria-conformidad/validation_report.md`.

## 3. Exenciones históricas

El acta declara cerradas por ratificación las exenciones que la auditoría de origen había reclasificado:

- `AUD-003`, `AUD-004` y `AUD-005`: regularización por rango normativo.
- `AUD-037`: ventana estructural de legado.
- `AUD-053`: historial de transiciones de las specs anteriores a la base v2.

## 4. Efecto

El efecto es retroactivo y limitado al régimen: regulariza el estado de los artefactos citados y de las exenciones declaradas, y no alcanza contratos, publicaciones ni consumidores externos al repositorio. No reescribe la historia publicada, no mueve tags y no modifica requisitos.

La ratificación no sustituye la firma de ninguna compuerta ni exime del cumplimiento futuro de la regla de firma posterior a la publicación.

## 5. Registro

- Inventario de hallazgos: `docs/sdd/inventario_hallazgos.md`.
- Lista de claves autorizadas: `docs/sdd/firmantes_autorizados`.
- Firma: commit firmado por el propietario que incorpora este acta.
