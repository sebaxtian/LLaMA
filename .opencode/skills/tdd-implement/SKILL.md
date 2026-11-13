---
name: tdd-implement
description: Protocolo TDD (Red → Green → Refactor) para implementar tareas, con adaptación validación-first para scripts .bat.
---

# Protocolo de implementación

Carga esta skill al ejecutar la Etapa 6 (Implement).

## TDD estricto (Python)

1. **Red**: escribe un test que falle y que exprese el comportamiento esperado.
2. **Green**: escribe el código mínimo para que el test pase.
3. **Refactor**: mejora el código sin cambiar comportamiento; los tests siguen en verde.

Reglas:

- No se escribe código de producción sin un test que falle primero.
- Una tarea por invocación, salvo instrucción explícita del propietario.
- Los tests usan `unittest` de la biblioteca estándar.

## Validación-first (`.bat`)

Para scripts `.bat`, antes de implementar declara:

- Comando a ejecutar.
- Salida esperada.
- Código de salida.
- Métricas relevantes (VRAM, RAM, tokens/s, contexto).

Después implementa y verifica que la salida real coincide con la esperada.

## Detenerse

- Si la tarea exige un archivo no declarado en `tasks.md`, detente.
- Si aparece una ambigüedad no registrada, detente y pide una `CLR`.
- No modifiques `RF`/`RNF`/`CA` para ajustarlos al código.
