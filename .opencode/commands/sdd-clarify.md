---
description: Resuelve ambigüedades de una spec (Etapa 3 Clarify)
agent: planner
---

Resuelve las ambigüedades de la spec $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Audita `spec.md` en busca de vacíos de lógica, requisitos imprecisos, casos límite y contradicciones.
2. Registra cada hallazgo como `AMB-001` en `clarify.md` con pregunta, respuesta, fecha UTC y responsable.
3. Convierte las decisiones en nuevos `RF`/`CB` o en correcciones a `spec.md`.
4. Aplica los parches y marca el apartado "Parches aplicados" como completado.
5. Al cerrar, el estado pasa a `clarified` y se valida con `python tools\sdd\validate.py --spec SPEC-NNN --gate G1`.

No autorices `plan.md` hasta que `clarify.md` esté cerrado y los parches aplicados.
