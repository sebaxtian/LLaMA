---
description: Muestra el estado de una spec, compuertas y siguiente acción
agent: sdd
---

Muestra el estado de la spec $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Lee `specs/INDEX.md` y los artefactos de `specs/NNN-slug/`.
2. Determina el estado actual a partir del frontmatter de `spec.md`.
3. Indica qué compuerta es la siguiente y qué acción debe ejecutarse.
4. Ejecuta `python tools\sdd\validate.py --spec SPEC-NNN` para un diagnóstico.

No edites archivos. Reporta estado, compuerta pendiente y siguiente comando.
