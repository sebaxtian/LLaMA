---
id: SPEC-007
title: Protección determinista de ramas GitHub
status: released
version: 0.2.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/branch-protection
release: v0.6.0
supersedes: ""
superseded_by: ""
---

# Protección determinista de ramas GitHub

## Contexto y objetivo

El flujo de trabajo Git del proyecto y la constitución establecen que las ramas `main` y `dev` son ramas protegidas por política: se prohíben commits directos de trabajo, envíos forzados con reescritura de historial y eliminación de ramas, exigiendo integración exclusiva mediante commits de fusión sin avance rápido (`merge --no-ff`) tras superar validaciones deterministas.

En un entorno remoto alojado en GitHub, estas restricciones operativas locales no se garantizan de manera automática sin la activación de reglas de protección en la plataforma remota. La falta de salvaguardas remotas permite eventuales fallos humanos o desvíos procedimentales, tales como envíos directos no controlados, fusiones con historial aplastado o rebase, o integración de cambios que no han superado las comprobaciones obligatorias.

El objetivo de esta especificación es definir el modelo determinista de protección de ramas en GitHub (denominado Opción D). Dicho modelo implementa reglas de protección remotas para blindar de manera inviolable las ramas `main` y `dev`, asegurando que el flujo de integración respete de forma estricta las directrices de gobernanza, inmutabilidad y calidad del proyecto.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** titular con atribuciones exclusivas para autorizar compuertas de control (G1, G4, G6), publicar releases y gestionar la apertura de ramas `release/vX-Y-Z`. El mecanismo de bypass se reserva exclusivamente a escenarios de contingencia extrema o recuperación autorizada, no utilizándose para la preparación rutinaria de releases.
- **Agentes de desarrollo (`planner`, `coder`, `reviewer`, `documenter`):** operan dentro de ramas de trabajo subordinadas (`feat/*`, `fix/*`, `hotfix/*`). No disponen de permisos para realizar envíos directos ni alterar la configuración de las ramas protegidas.
- **Ramas auxiliares `release/*`:** ramas transitorias bajo la nomenclatura estricta `release/vX-Y-Z` utilizadas exclusivamente para el empaquetado de versiones, exentas de spec previa y canalizadas a través de Pull Request hacia `dev` o `main`.
- **Orquestador (`sdd`):** gestiona el ciclo de vida SDD, ejecuta validaciones locales deterministas y supervisa las compuertas de calidad sin permisos de elusión remota.
- **Servidor remoto (GitHub):** ejecuta la verificación de las reglas de protección, bloqueando operaciones indebidas y validando el estado de las ramas antes de consentir la fusión.

## Requisitos funcionales (EARS)

### RF-001

El sistema DEBE aplicar reglas de protección deterministas independientes y activas a las ramas `main` y `dev` en el repositorio remoto GitHub.

### RF-002

SI un actor intenta realizar un envío directo (`push`) de commits a la rama `main` o a la rama `dev` fuera del mecanismo gobernado de Pull Requests, ENTONCES el sistema DEBE rechazar la operación de envío.

### RF-003

SI un actor intenta realizar un envío forzado (`force push`) hacia la rama `main` o hacia la rama `dev`, ENTONCES el sistema DEBE rechazar la operación de manera irrevocable.

### RF-004

SI un actor intenta eliminar las ramas remotas `main` o `dev`, ENTONCES el sistema DEBE rechazar la solicitud de eliminación.

### RF-005

CUANDO se procesa la integración de una rama hacia `main` o hacia `dev` en GitHub, el sistema DEBE exigir la creación de un commit de fusión sin avance rápido (`merge --no-ff`) mediante Pull Request y NO DEBE permitir fusiones mediante avance rápido, `squash merge` ni `rebase merge`.

### RF-006

DONDE se encuentren formalmente aprovisionados flujos de validación automatizada en el repositorio remoto, el sistema DEBE bloquear la integración hacia `dev` o hacia `main` hasta que las comprobaciones requeridas concluyan satisfactoriamente.

### RF-007

CUANDO se solicita integrar una rama hacia `dev` o hacia `main`, el sistema DEBE exigir que la rama de origen se encuentre sincronizada con el último commit de la rama destino antes de autorizar la fusión.

### RF-008

DONDE se requiera habilitar permisos de elusión excepcional (bypass) de las reglas de protección frente a contingencias críticas de infraestructura, el sistema DEBE restringir dicha capacidad exclusivamente a la identidad del Propietario (`Agent Sebaxtian`).

### RF-009

DONDE se gestione la revisión de Pull Requests hacia `dev` o `main` en la fase unipersonal del repositorio, el sistema DEBE fijar en cero (0) el mínimo de revisiones aprobatorias requeridas.

### RF-010

El sistema NO DEBE exigir firmas criptográficas en los commits dentro de las reglas de protección remota durante la fase operativa actual.

## Requisitos no funcionales

### RNF-001

La configuración de protección en GitHub DEBE mantener concordancia plena con las políticas de ramas de `docs/Flujo_de_Trabajo_Git.md`.

### RNF-002

El sistema DEBE rechazar cualquier operación no autorizada en un lapso inferior a 5 segundos desde la recepción del comando en el servidor remoto.

### RNF-003

Las reglas de protección DEBEN garantizar la inmutabilidad permanente del historial lineal y de los commits de fusión integrados en `main`.

### RNF-004

CUANDO el sistema rechaza una operación remota por infracción de las reglas, el sistema DEBE generar un mensaje descriptivo que identifique la restricción aplicada.

### RNF-005

La configuración de protección remota DEBE estructurarse como una especificación determinista y verificable.

### RNF-006

El sistema DEBE denegar privilegios de modificación o desactivación de las reglas de protección a cualquier actor distinto del Propietario.

### RNF-007

Las reglas de protección DEBEN operar de forma ininterrumpida las 24 horas del día durante la vigencia del repositorio.

## Casos borde

### CB-001

SI un actor intenta realizar un envío forzado hacia `main` o `dev` utilizando la variante `--force-with-lease`, ENTONCES el sistema DEBE rechazar la operación con la misma restricción aplicada a cualquier envío forzado.

### CB-002

SI la rama destino recibe nuevos commits mientras un Pull Request se encuentra abierto, ENTONCES el sistema DEBE calificar la rama como desactualizada y bloquear su integración.

### CB-003

DONDE existan comprobaciones automatizadas de CI requeridas en un Pull Request hacia `dev` y una de ellas termine con error o sea cancelada, ENTONCES el sistema DEBE mantener el bloqueo de integración impidiendo la fusión.

### CB-004

SI un actor intenta fusionar un Pull Request eligiendo las modalidades de fusión `squash and merge` o `rebase and merge`, ENTONCES el sistema DEBE rechazar la acción por encontrarse deshabilitadas dichas alternativas en los ajustes del repositorio.

### CB-005

SI cualquier actor intenta efectuar un push directo con el commit `chore: prepare release vX.Y.Z` en `dev`, ENTONCES el sistema DEBE rechazar la transferencia, requiriendo canalizar la integración mediante Pull Request desde la rama `release/vX-Y-Z`.

### CB-006

SI un actor intenta suprimir la rama `dev` mediante la instrucción remota `git push origin --delete dev`, ENTONCES el sistema DEBE abortar la operación con un error de rama protegida.

### CB-007

DONDE existan comprobaciones automatizadas de CI requeridas y se incorporen commits adicionales a una rama con un Pull Request abierto, ENTONCES el sistema DEBE cancelar las comprobaciones previas y reiniciar la validación completa sobre el nuevo commit final.

### CB-008

DONDE existan comprobaciones automatizadas de CI requeridas y una sincronización de hotfix hacia `dev` presente fallos en ellas, ENTONCES el sistema DEBE bloquear la integración hasta que el conjunto completo de pruebas alcance un estado satisfactorio.

### CB-009

SI un actor crea una rama auxiliar para empaquetado de versión con nomenclatura `release/vX-Y-Z`, ENTONCES el sistema DEBE admitir la creación y procesamiento de dicha rama sin exigir una especificación funcional previa.

### CB-010

SI el autor de un Pull Request en fase unipersonal solicita la integración del cambio habiendo superado los requisitos estructurales sin contar con aprobaciones de terceros, ENTONCES el sistema DEBE permitir la fusión sin incurrir en bloqueo por falta de aprobadores.

### CB-011

SI un commit incorporado en un Pull Request no cuenta con firma digital GPG o SSH, ENTONCES el sistema DEBE aceptar el commit sin rechazarlo por ausencia de firma criptográfica.

## Fuera de alcance

- Configuración de servidores de integración continua en plataformas externas fuera de GitHub Actions o del validador determinista del repositorio.
- Creación de flujos de trabajo `.github/workflows/` y designación activa de status checks obligatorios en GitHub, lo cual queda diferido a una especificación posterior de CI.
- Reglas de protección sobre repositorios ajenos o bifurcaciones personales no gestionadas por el titular.
- Automatización de despliegues a entornos de producción o infraestructura de nube.
- Creación de ramas auxiliares no contempladas en `docs/Flujo_de_Trabajo_Git.md` (exceptuando las ramas `release/vX-Y-Z` admitidas formalmente).

## Criterios de aceptación

### CA-001

`DADO un repositorio remoto con protección activa, CUANDO un actor intenta realizar un envío directo de commits a main o dev (incluyendo commits de empaquetado de release), ENTONCES el servidor remoto rechaza el envío notificando que los cambios requieren un Pull Request.`

Cubre: `RF-001`, `RF-002`, `CB-005`.

### CA-002

`DADO un intento de reescritura de historial en main o dev, CUANDO un actor ejecuta git push --force o git push --force-with-lease, ENTONCES el servidor remoto rechaza la operación e indica que el envío forzado está prohibido.`

Cubre: `RF-003`, `CB-001`.

### CA-003

`DADO un repositorio remoto con ramas protegidas, CUANDO un actor solicita la eliminación remota de main o dev, ENTONCES el sistema bloquea la acción y preserva intactas las ramas.`

Cubre: `RF-004`, `CB-006`.

### CA-004

`DADO un Pull Request listo para su integración hacia main o dev, CUANDO se consulta la interfaz de fusión, ENTONCES el sistema únicamente ofrece la opción de commit de merge sin avance rápido, manteniendo deshabilitadas las opciones de squash y rebase en los ajustes del repositorio.`

Cubre: `RF-005`, `CB-004`.

### CA-005

`DADO un repositorio donde se implementen flujos de CI en una etapa posterior, CUANDO se evalúen comprobaciones automáticas requeridas en un Pull Request hacia dev, ENTONCES el sistema bloqueará la integración ante fallos o ejecuciones en curso hasta su conclusión satisfactoria.`

Cubre: `RF-006`, `CB-003`, `CB-007`.

### CA-006

`DADO un Pull Request cuya rama base recibe commits adicionales tras su apertura, CUANDO se verifica el estado de integración, ENTONCES el sistema señala que la rama requiere actualización y prohíbe la fusión hasta incorporar los cambios recientes.`

Cubre: `RF-007`, `CB-002`.

### CA-007

`DADO un procedimiento de sincronización de hotfix hacia dev en presencia de flujos de comprobación requeridos, CUANDO se evalúa la solicitud de integración, ENTONCES el sistema exige el cumplimiento estricto de dichas comprobaciones antes de permitir la fusión.`

Cubre: `RF-006`, `CB-008`.

### CA-008

`DADO un escenario de excepción operativa crítica no rutinaria, CUANDO el Propietario (Agent Sebaxtian) ejecuta una acción de contingencia mediante la política de bypass autorizada, ENTONCES el sistema permite la operación y registra la identidad en la auditoría remota, mientras deniega el acceso a cualquier otro actor.`

Cubre: `RF-008`.

### CA-009

`DADO el empaquetado de una versión para release, CUANDO se crea una rama auxiliar release/vX-Y-Z e integra su contenido mediante Pull Request, ENTONCES el sistema acepta el flujo de empaquetado sin requerir una especificación SDD previa.`

Cubre: `RF-001`, `CB-009`.

### CA-010

`DADO un Pull Request en la fase unipersonal de desarrollo, CUANDO el autor solicita fusionar la rama habiendo satisfecho los controles de integración sin contar con revisiones de otros usuarios, ENTONCES el sistema procesa la fusión de manera determinista sin exigir un umbral de 1 o más aprobaciones.`

Cubre: `RF-009`, `CB-010`.

### CA-011

`DADO el envío de commits para su integración remota, CUANDO los commits no poseen firma criptográfica GPG o SSH, ENTONCES el servidor remoto acepta la contribución sin rechazarla por falta de firma.`

Cubre: `RF-010`, `CB-011`.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-13)
- [x] G4: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial |
| 0.2.0 | 2026-11-13 | Parches tras clarificación AMB-001 a AMB-006 |
