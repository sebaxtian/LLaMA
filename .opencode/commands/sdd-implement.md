---
description: Implementa una única tarea pendiente con TDD (Etapa 6 Implement)
agent: coder
---

Implementa UNA única tarea pendiente de la spec $ARGUMENTS siguiendo `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. La spec debe estar en `tasked` y autorizada (G4). Si no, detente y repórtalo.
2. Localiza la primera tarea `[ ]` de `tasks.md` y lee sus dependencias y archivos.
3. Python: escribe el test que falle, luego el código mínimo y refactoriza.
4. `.bat`: declara comando, salida esperada, código de salida y métricas; implementa y verifica.
5. Marca la tarea `[x]` con evidencia y actualiza `tasks.md`.
6. Valida con `python tools\sdd\validate.py --spec SPEC-NNN --gate G3`.

Si una tarea exige un archivo no declarado, o aparece una ambigüedad, detente y pide actualizar `tasks.md` o registrar una `CLR`.
