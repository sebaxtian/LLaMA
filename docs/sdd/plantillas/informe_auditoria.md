# Informe de auditoría — <alcance>

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, implementado en `.opencode/agents/auditor.md`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** YYYY-MM-DD (UTC).
- **Alcance:** <base normativa y documentos auditados>.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas ni sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `<sha>` |
| Rama | `<rama>` |
| Fecha de corte | YYYY-MM-DD |
| Validador ejecutado | `python tools\sdd\validate.py --all` |
| Entorno | Windows 11, <versión de las herramientas> |
| Rol ejecutor | <rol que ejecuta la auditoría> |

## 2. Base normativa e inventario

- <Documentos normativos auditados con rango y versión>.
- <Archivos sin rango declarados en el inventario de `docs/sdd/README.md`>.
- La fila de este informe en la tabla de inventario de `docs/sdd/README.md` la escribe el `documenter` antes de la integración; el rol de auditoría escribe solo el informe y no escribe esa fila.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta, sección y fecha. Un veredicto sin evidencia no se emite.

**Regla citada.** Cada hallazgo cita la regla normativa que se incumple con la forma `ruta §capítulo:línea`, por ejemplo `docs/constitution.md §7:76`. El juicio que no cita una regla se registra como observación; la observación queda fuera del recuento de hallazgos y no computa como hallazgo abierto en el cálculo del veredicto. Un hallazgo sin regla citada no se admite.

Escala de veredicto:

| Veredicto | Significado |
|---|---|
| `CONFORME` | La condición se cumple con evidencia citada. |
| `PARCIAL` | La condición se cumple en parte y la brecha queda declarada. |
| `NO CONFORME` | La condición no se cumple. |
| `NO VERIFICABLE` | La evidencia disponible no permite decidir. |
| `NO APLICA` | La condición no alcanza al objeto auditado. |

Escala de severidad:

| Severidad | Significado |
|---|---|
| `Crítica` | Afecta la validez de una compuerta o de la base normativa. |
| `Alta` | Rompe una regla normativa sin invalidar la compuerta. |
| `Media` | Produce divergencia entre documentos de distinto rango. |
| `Baja` | Defecto de forma o de redacción. |

**Numeración.** Los hallazgos usan `AUD-NNN` correlativo por dimensión, con diez números reservados por dimensión y continuación inmediata al último asignado cuando una dimensión excede su capacidad. Un número asignado no se reutiliza entre versiones del informe.

## 4. Matriz de dimensiones

| Dimensión | Veredicto | Evidencia | Hallazgos |
|---|---|---|---|
| <dimensión> | <veredicto de la escala> | <ruta y sección> | `AUD-NNN` |

## 5. Hallazgos

### AUD-001

- **Dimensión:** <dimensión>.
- **Veredicto:** <veredicto de la escala>.
- **Severidad:** <severidad de la escala>.
- **Regla citada:** `<ruta> §<capítulo>:<línea>`.
- **Evidencia:** <ruta, sección y fecha>.
- **Descripción:** <qué se observa>.
- **Remediación:** <qué condición cierra el hallazgo>.

### Observaciones

| N.º | Severidad | Observación | Tratamiento |
|---|---|---|---|
| 1 | `Alta` | <juicio que no cita una regla normativa> | <decisión registrada del propietario, con fecha e identificador del commit> |

Las observaciones no computan en el recuento de hallazgos ni como hallazgo abierto. Una observación de severidad `Alta` o `Media` sin tratamiento impide el veredicto `CONFORME`.

## 6. Compuertas

| Compuerta | Veredicto | Evidencia |
|---|---|---|
| G1 | <veredicto> | <commit firmado y línea registrada en `spec.md`> |
| G4 | <veredicto> | <reporte convergido y línea registrada en `spec.md`> |
| G6 | <veredicto> | <informe de auditoría, tag verificado y entrada del release> |

## 7. Veredicto global

- <Veredicto del conjunto, con la justificación y los hallazgos que lo sostienen>.

El veredicto se calcula desde el estado de las filas del inventario de hallazgos, con la precedencia `NO CONFORME`, después `NO VERIFICABLE`, después `PARCIAL` y después `CONFORME`; se declara el primero que se cumple y se transcribe la fila que sostiene la diferencia cuando el veredicto declarado contradice el recuento. `CONFORME` exige 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento. La condición de cada veredicto es la de §16 de `docs/sdd/PROTOCOLO_OPERATIVO.md`.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| <acción> | `AUD-NNN` | <bloque> | <dependencia> |

## 9. Limitaciones

- <Qué no se pudo verificar y por qué.>

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | <salida transcrita o extracto> | <ruta o comando> |
