---
description: Crea o reanuda la especificación de una feature (Etapa 2 Specify)
agent: planner
---

Crea o reanuda la especificación para $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Determina el ID `SPEC-NNN` (usa `python tools\sdd\validate.py --next-id` si es nueva).
2. Crea la carpeta `specs/NNN-slug/` y redacta `spec.md` con la plantilla `docs/sdd/plantillas/spec.md`.
3. Requisitos funcionales en notación EARS; casos borde `CB-001`; criterios de aceptación `CA-001`.
4. Rellena el frontmatter (id, título, estado `draft`, rama `feat/<nombre>`).
5. Actualiza `specs/INDEX.md`.
6. Valida con `python tools\sdd\validate.py --spec SPEC-NNN --gate G1`.

No escribas código ni detalles técnicos en `spec.md`.
