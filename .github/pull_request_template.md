# Pull Request

## Resumen

<Descripción breve del cambio y del problema que resuelve.>

## Spec vinculada

- ID: `SPEC-NNN`
- Rama: `feat/<nombre>`
- Estado de la spec: `validated`

## Checklist SDD

- [ ] Existe una spec aprobada (`specs/NNN-slug/spec.md`) con estado `validated`.
- [ ] `clarify.md` cerrado y parches aplicados.
- [ ] `plan.md` con matriz de cobertura `RF/CB → componente → prueba`.
- [ ] `tasks.md` con todas las tareas `[x]` y evidencia.
- [ ] `validation_report.md` con dictamen `CONVERGIDO` al 100 %.
- [ ] `python tools\sdd\validate.py --spec SPEC-NNN` devuelve `0`.

## Validaciones

- [ ] `git diff --check` sin errores.
- [ ] Sin cambios en `llama.cpp/`, `bin/`, `models/` ni `.env`.
- [ ] `CHANGELOG.md` actualizado bajo `Unreleased`.
- [ ] Los commits de implementación incluyen `Spec: SPEC-NNN`.

## Evidencia

<Enlaces o resumen de las evidencias de validación.>
