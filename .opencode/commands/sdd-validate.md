---
description: Audita y emite el reporte de validación (Etapa 7 Validate)
agent: reviewer
---

Audita la convergencia de la spec $ARGUMENTS conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. **Precondición:** G3 completa, con todas las tareas cerradas y su evidencia transcrita.
2. Lee `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y el diff de código.
3. Verifica la matriz `RF/CB → CA → T → evidencia` y la cobertura completa.
4. Escribe `specs/NNN-slug/validation_report.md` con entorno, matriz, brechas y dictamen.
5. **No evalúes G4 ni escribas `validated`.** El orquestador evalúa G4 después de que el reporte exista y de que el propietario firme la línea en `spec.md`.
6. El dictamen `CONVERGIDO` solo se emite al 100 % de requisitos con evidencia `PASADO`.
7. Registra las brechas con referencia al requisito y a la ruta. No corrijas los artefactos auditados.

No declares compuertas. La aprobación de G4 corresponde al propietario y se registra en `spec.md` con commit firmado.
