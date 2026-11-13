# Clarificación - SPEC-001

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** la spec no definía si el menú se repite después de ejecutar un script o termina.
- **Pregunta:** ¿main.bat vuelve a mostrar el menú tras ejecutar un script?
- **Respuesta:** sí; el menú se repite hasta que el usuario elige la opción de salida.
- **Decisión:** bucle de menú; la ejecución de un script retorna al menú.
- **Fecha:** 2026-11-12 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** la spec no definía el tratamiento de archivos de src/ que no son .bat.
- **Pregunta:** ¿se listan los archivos no-.bat (por ejemplo .gitkeep)?
- **Respuesta:** no; solo se listan los archivos con extensión .bat.
- **Decisión:** filtro por extensión .bat, ignorando el resto.
- **Fecha:** 2026-11-12 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** la spec no definía el comportamiento cuando un script ejecutado falla.
- **Pregunta:** ¿qué ocurre si el script seleccionado termina con código de salida distinto de cero?
- **Respuesta:** se informa del error y se vuelve al menú.
- **Decisión:** propagar el código de salida, informar del error y retornar al menú.
- **Fecha:** 2026-11-12 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-003

SI el script seleccionado termina con un código de salida distinto de cero, ENTONCES el sistema DEBE informar del error y volver al menú.

## Parches aplicados a spec.md

- [x] Incorporado RF-006 (bucle de menú hasta salir).
- [x] Incorporado CB-003 (error del script y retorno al menú).
- [x] Añadido CA-005 (el menú se vuelve a mostrar tras ejecutar un script).

## Decisiones de negocio

- El menú opera en bucle hasta que el usuario elige salir.
- Solo se listan archivos .bat del primer nivel de src/.