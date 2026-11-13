---
description: Descompone el plan en tareas atómicas (Etapa 5 Tasks)
agent: planner
---

Descompone el plan de la spec $ARGUMENTS en tareas siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Lee `plan.md` (la spec debe estar en `planned`).
2. Redacta `tasks.md` con la plantilla `docs/sdd/plantillas/tasks.md`.
3. Cada tarea `T-001` debe ser atómica y contener: dependencias, requisitos cubiertos, archivos permitidos, estimación 15–30 min, comando de validación y checkbox.
4. Verifica cobertura total: todo `RF`/`CB` con `CA` queda cubierto por al menos una tarea.
5. Verifica que las dependencias sean acíclicas.
6. El estado pasa a `tasked`; valida con `python tools\sdd\validate.py --spec SPEC-NNN --gate G2`.

Una tarea no puede tocar archivos fuera de su campo `Archivos`.
