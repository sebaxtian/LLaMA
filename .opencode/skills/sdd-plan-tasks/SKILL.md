---
name: sdd-plan-tasks
description: Descomposición del plan técnico en tareas atómicas con trazabilidad RF/CB → CA → T.
---

# Plan y tareas

Carga esta skill para generar `plan.md` y `tasks.md`.

## `plan.md`

- Referencias a `spec.md` y `clarify.md`.
- Arquitectura de módulos, esquemas/tipos e interfaces.
- Decisiones `DEC-001` con alternativas descartadas.
- Estrategia de testing. Para `.bat`: comando, salida esperada, código de salida y métricas.
- Matriz de cobertura `RF/CB → componente → prueba`.

## `tasks.md`

Cada tarea `T-001` debe ser:

- **Atómica**: una unidad discreta de trabajo.
- **Acotada**: 15–30 minutos.
- **Trazable**: lista los requisitos cubiertos.
- **Limitada**: solo toca los archivos de su campo `Archivos`.
- **Verificable**: declara el comando o prueba que la valida.

## Reglas

- Cobertura total: todo `RF`/`CB` con `CA` queda cubierto por al menos una tarea.
- Dependencias acíclicas.
- Una tarea no puede tocar archivos fuera de su campo `Archivos`.
