---
description: Genera el plan técnico de una spec (Etapa 4 Plan)
agent: planner
---

Genera el plan técnico para la spec $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Lee `spec.md` y `clarify.md` (la spec debe estar en `clarified`).
2. Redacta `plan.md` con la plantilla `docs/sdd/plantillas/plan.md`.
3. Incluye arquitectura de módulos, esquemas/tipos, interfaces, decisiones `DEC-001` y estrategia de testing.
4. Para scripts `.bat`, declara comando, salida esperada, código de salida y métricas (validación-first).
5. Añade la matriz de cobertura `RF/CB → componente → prueba`.
6. El estado pasa a `planned`.

No introduzcas alcance nuevo respecto a `spec.md`.
