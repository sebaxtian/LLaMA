---
description: Ejecuta el validador SDD y las compuertas aplicables
agent: sdd
---

Ejecuta el validador SDD para $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. Sin argumentos de spec: ejecuta `python tools\sdd\validate.py --all`.
2. Con `SPEC-NNN`: ejecuta `python tools\sdd\validate.py --spec SPEC-NNN` y, si procede, `--gate Gx`.
3. Verifica la longitud de `AGENTS.md`, la consistencia con `specs/INDEX.md` y los códigos de salida (`0` válido, `1` error, `2` uso).
4. Reporta cada hallazgo con archivo y regla infringida.

No edites archivos. El validador es el árbitro determinista.
