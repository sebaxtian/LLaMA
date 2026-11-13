---
id: SPEC-001
title: Menú principal main.bat
status: released
version: 0.1.0
created: 2026-11-12
updated: 2026-11-12
owner: Agent Sebaxtian
branch: feat/main-menu
release: "v0.2.0"
supersedes: ""
superseded_by: ""
---

# Menú principal `main.bat`

## Contexto y objetivo

El proyecto ejecuta modelos LLM localmente mediante scripts `.bat` almacenados en `src/`. Sin un punto de entrada central, el usuario debe conocer y ejecutar cada script manualmente. `main.bat` será el menú raíz que descubre los scripts disponibles en `src/` y permite seleccionar cuál ejecutar, resolviendo rutas con `%~dp0` y sin depender del directorio de invocación.

## Actores y permisos

- **Usuario local:** inicia `main.bat`, selecciona un script para ejecutar o sale del menú.

## Requisitos funcionales (EARS)

### RF-001
CUANDO el usuario inicia `main.bat`, el sistema DEBE descubrir los archivos `.bat` presentes en el primer nivel de `src/` y mostrarlos como opciones numeradas en orden alfabético.

### RF-002
CUANDO el usuario introduce el número de una opción válida, el sistema DEBE ejecutar el script `.bat` correspondiente mediante su ruta explícita.

### RF-003
El menú DEBE incluir una opción de salida identificada y accesible sin ejecutar ningún script.

### RF-004
SI la entrada del usuario no es un número entero o no corresponde a una opción mostrada, ENTONCES el sistema DEBE mostrar un mensaje de error y volver a solicitar la entrada.

### RF-005
CUANDO no existen archivos `.bat` en `src/`, el sistema DEBE mostrar un mensaje informativo y permitir únicamente la opción de salida.

### RF-006
MIENTRAS el usuario no seleccione la opción de salida, el sistema DEBE volver a mostrar el menú después de ejecutar un script.

## Requisitos no funcionales

### RNF-001
`main.bat` DEBE resolver la raíz del proyecto con `%~dp0` y no debe depender del directorio actual ni del `PATH` del sistema.

### RNF-002
`main.bat` DEBE verificar la existencia del script seleccionado antes de intentar ejecutarlo.

## Casos borde

### CB-001
SI `src/` no contiene archivos `.bat` (solo `.gitkeep` u otros archivos), ENTONCES el sistema DEBE informar que no hay scripts disponibles.

### CB-002
SI el nombre de un script contiene espacios, ENTONCES el sistema DEBE ejecutarlo correctamente citando la ruta.

### CB-003
SI el script seleccionado termina con un código de salida distinto de cero, ENTONCES el sistema DEBE informar del error y volver al menú.

## Fuera de alcance

- Descubrimiento recursivo de subcarpetas de `src/`.
- Descubrimiento de scripts fuera de `src/`.
- Gestión de modelos, binarios o dependencias.
- Menús anidados o configuración persistente.

## Criterios de aceptación

### CA-001
DADO al menos un archivo `.bat` en `src/`, CUANDO se inicia `main.bat`, ENTONCES se muestran las opciones numeradas en orden alfabético junto con la opción de salida.

### CA-002
DADO un menú mostrado, CUANDO el usuario introduce el número de un script válido, ENTONCES el script se ejecuta y se propaga su código de salida.

### CA-003
DADO un menú mostrado, CUANDO el usuario introduce una entrada no numérica o fuera de rango, ENTONCES se muestra un mensaje de error y se vuelve a solicitar la entrada.

### CA-004
DADO `src/` sin archivos `.bat`, CUANDO se inicia `main.bat`, ENTONCES se muestra un mensaje informativo y solo la opción de salida.

### CA-005
DADO un menú mostrado y un script ejecutado, CUANDO el script termina, ENTONCES el menú se vuelve a mostrar salvo que se eligiera salir.

## Aprobaciones

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-12)
- [x] G4: - Approved by: Agent Sebaxtian (2026-11-12)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-12 | Redacción inicial |
| 0.2.0 | 2026-11-12 | Aprobación G1, plan y tareas |
| 0.3.0 | 2026-11-12 | Implementación y validación |