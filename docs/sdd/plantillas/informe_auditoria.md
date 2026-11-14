# Informe de auditoría — <alcance>

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol habilitado: auditoría, con lectura de la base completa y escritura limitada a este informe. Mientras ese rol no exista en `.opencode/`, la escritura la ejecuta `documenter` bajo la declaración del rol.*

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

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta, sección y fecha. Un veredicto sin evidencia no se emite.

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
- **Evidencia:** <ruta, sección y fecha>.
- **Descripción:** <qué se observa>.
- **Remediación:** <qué condición cierra el hallazgo>.

## 6. Compuertas

| Compuerta | Veredicto | Evidencia |
|---|---|---|
| G1 | <veredicto> | <commit firmado y línea registrada en `spec.md`> |
| G4 | <veredicto> | <reporte convergido y línea registrada en `spec.md`> |
| G6 | <veredicto> | <informe de auditoría, tag verificado y entrada del release> |

## 7. Veredicto global

- <Veredicto del conjunto, con la justificación y los identificadores de los hallazgos que lo sostienen>.

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
