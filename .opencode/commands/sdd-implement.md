---
description: Implementa una única tarea pendiente con TDD (Etapa 6 Implement)
agent: coder
---

Implementa UNA tarea pendiente de la spec $ARGUMENTS conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md`.

1. **Precondición:** la spec debe estar en `tasked` y tener la verificación G2 registrada. Si no se cumple, detente y repórtalo.
2. **Estado:** el orquestador escribe `implementing` en `spec.md` y la fila T4 del historial antes de la primera tarea. Tú no editas `spec.md`.
3. Localiza la primera tarea `[ ]` de `tasks.md` y lee sus dependencias y su campo `Archivos`.
4. **Python:** escribe primero el test que falle, después el código mínimo y refactoriza.
5. **`.bat`:** declara comando, salida esperada, código de salida y métricas antes de implementar.
6. Marca la tarea `[x]` y transcribe su evidencia en `tasks.md`.
7. **G3 no se evalúa por tarea.** Se evalúa al cerrar la etapa. Cuando cierres la última tarea, el orquestador escribe `implemented` y la fila T5.
8. Si una tarea exige un archivo no declarado o aparece una ambigüedad, detente y pide actualizar `tasks.md` o registrar la ambigüedad.

No declares compuertas. La aprobación de G4 corresponde al propietario.
