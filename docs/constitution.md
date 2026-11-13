# Constitución del proyecto LLaMA

La presente constitución es la **norma suprema** del repositorio. Ningún agente, humano o script puede contravenirla. Ante cualquier contradicción entre documentos, esta constitución prevalece sobre el resto de la documentación.

## 1. Identidad y misión

- El proyecto `LLaMA` ejecuta, prueba y compara modelos LLM localmente mediante [llama.cpp](https://github.com/ggml-org/llama.cpp) en Windows 11.
- Caso de uso principal: programación en Python, análisis de datos y arquitectura de software.
- El desarrollo se rige estrictamente por **Desarrollo Basado en Especificaciones (SDD)**, en su variante **Spec-Anchored**: la especificación y el código conviven y se validan mutuamente.

## 2. Principios innegociables

1. **Especificación primero.** Ninguna feature, fix, refactor o cambio de configuración se implementa sin una spec aprobada.
2. **Determinismo.** Cada requisito, tarea y validación debe ser verificable por un agente sin ambigüedad.
3. **Trazabilidad total.** Cada requisito se vincula a criterios de aceptación, tareas, evidencia y release.
4. **Aprobación humana.** La spec, la autorización de implementación y la autorización de release exigen aprobación explícita del propietario.
5. **Menor privilegio.** Cada agente recibe solo los permisos que necesita para su función.
6. **Verificabilidad.** Ninguna afirmación de éxito sin evidencia registrada en `validation_report.md`.

## 3. Guardrails de archivos (reglas no negociables)

- `llama.cpp/`: repositorio oficial clonado. **Prohibido** crear, modificar, eliminar, mover, renombrar o sobrescribir cualquier archivo o carpeta en su interior. Solo lectura de documentación y código de referencia.
- `bin/`: dependencias y versiones precompiladas o compiladas de llama.cpp. Excluido de Git. Prohibido colocar modelos dentro.
- `models/`: modelos descargados. Excluido de Git. Prohibido colocar binarios dentro.
- `.env`: credenciales locales. Excluido, protegido contra lectura y edición. Las plantillas usan `example.env`.
- `.gitkeep`: `bin/.gitkeep`, `models/.gitkeep`, `src/.gitkeep` deben conservarse.

## 4. Stack tecnológico

- Lenguaje de implementación principal para herramientas: **Python** (biblioteca estándar, sin dependencias externas para el validador SDD).
- Scripts de ejecución de modelos: **`.bat`** para Windows.
- Control de versiones: **Git**, con la política definida en `docs/Flujo_de_Trabajo_Git.md`.
- Plataforma: **Windows 11**.

## 5. Estándares de calidad

- **TDD estricto** para todo código Python.
- **Validación-first** para scripts `.bat`: comando, salida esperada, código de salida y métricas antes de implementar.
- `AGENTS.md` se mantiene entre 30 y 70 líneas útiles.
- Todo cambio relevante se registra en `CHANGELOG.md` bajo `Unreleased`.
- Idioma de la documentación: **español**.

## 6. Jerarquía normativa

Cuando dos documentos entren en conflicto, prevalece el de mayor rango. El conflicto **detiene el trabajo** y se corrige el documento superior.

```text
1. docs/constitution.md              (este documento)
2. AGENTS.md                         Reglas operativas para agentes
3. docs/sdd/PROTOCOLO_OPERATIVO.md   Norma SDD ejecutable
4. docs/Flujo_de_Trabajo_Git.md      Procedimiento Git
5. Documento maestro técnico         Hardware y benchmarks
6. specs/NNN-slug/spec.md            Contrato de la feature
7. clarify.md / plan.md / tasks.md   Decisiones y ejecución
8. validation_report.md              Evidencia de convergencia
9. Código
```

## 7. Gobernanza y aprobaciones

- El propietario del proyecto es `Agent Sebaxtian` (`agent@sebaxtian.dev`).
- Las aprobaciones se registran como líneas explícitas `- Approved by: Agent Sebaxtian`.
- Ningún agente puede aprobar su propia spec ni autorizar su propia implementación o release.
- La única excepción al requisito de spec previa es la **Etapa 1 (Constitución/Setup)**, autorizada una sola vez por el propietario, y el cambio **exclusivamente editorial**.

## 8. Prohibiciones

- Código generado sin spec aprobada, fuera de la excepción editorial.
- Rebase, squash merge o copia manual como estrategia de integración.
- Tags que no cumplan `vMAJOR.MINOR.PATCH` o que no sean anotados.
- Incorporar modelos, binarios, dependencias, credenciales, controladores o firmware al repositorio.
- Declarar un modelo "optimizado" sin comprobar carga, VRAM/RAM y velocidad.
