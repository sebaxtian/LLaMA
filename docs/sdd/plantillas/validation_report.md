# Reporte de validación — SPEC-XXX

*Plantilla de rango 5: norma de forma del artefacto `validation_report.md`. Después de G4 el documento es append-only: el registro de G5 y de G6 se añade sin alterar la matriz ni el dictamen.*

<!-- Este reporte no porta casilla ni sección de firma del propietario: el registro de G4 vive en la sección de aprobaciones de `spec.md`. -->

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/<nombre>`.
- Commit validado: `<sha>`.
- Herramientas: `<versiones relevantes>`.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | <comando> | <salida o extracto> | `PASADO` |
| `CB-001` | `CA-001` | <comando> | <salida o extracto> | `PASADO` |

El único valor que converge es `PASADO`; cualquier otro valor abre una brecha en la sección siguiente.

## Brechas

- <Requisito sin evidencia o evidencia pendiente. La sección se deja sin entradas para converger.>

## Dictamen

- [ ] `CONVERGIDO` (100 % de requisitos y casos borde con evidencia `PASADO`).
- [ ] `NO CONVERGIDO`.
