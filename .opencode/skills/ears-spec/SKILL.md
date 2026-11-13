---
name: ears-spec
description: Notación EARS para redactar requisitos funcionales no ambiguos en spec.md.
---

# Notación EARS para `spec.md`

Carga esta skill antes de redactar requisitos funcionales.

## Patrones

| Tipo | Patrón |
|---|---|
| Ubiquitous | `El sistema DEBE <respuesta>`. |
| Event-driven | `CUANDO <evento>, el sistema DEBE <respuesta>`. |
| State-driven | `MIENTRAS <estado>, el sistema DEBE <respuesta>`. |
| Unwanted | `SI <condición>, ENTONCES el sistema DEBE <respuesta>`. |
| Optional | `DONDE <característica>, el sistema DEBE <respuesta>`. |

## Reglas

- Cada `RF` contiene una palabra normativa: `DEBE`, `NO DEBE`, `DEBERÍA` o `PUEDE`.
- Cada umbral tiene número y unidad.
- Léxico ambiguo prohibido: `TBD`, `TODO`, `por definir`, `etc.`, `y/o`, `apropiado`, `adecuado`, `óptimo`, `según sea necesario`, `cuando sea posible`.
- Un requisito es atómico: expresa una única obligación verificable.

## Ejemplo

```text
### RF-001
CUANDO el usuario inicia el menú, el sistema DEBE mostrar las opciones disponibles ordenadas alfabéticamente.
```

Cada `RF` debe tener un `CA` que lo verifique.
