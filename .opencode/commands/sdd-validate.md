---
description: Audita y emite el reporte de validación (Etapa 7 Validate)
agent: reviewer
---

Audita la convergencia de la spec $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Lee `spec.md`, `clarify.md`, `plan.md`, `tasks.md` y el diff de código.
2. Ejecuta las validaciones declaradas y `python tools\sdd\validate.py --spec SPEC-NNN --gate G4`.
3. Verifica la matriz `RF/CB → CA → T → evidencia`.
4. Escribe `specs/NNN-slug/validation_report.md` con entorno, matriz, brechas y dictamen.
5. Dictamen `CONVERGIDO` solo al 100 % con evidencia `PASADO`.

Solo editas `validation_report.md`; no tocas código ni otros artefactos.
