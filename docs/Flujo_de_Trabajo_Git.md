# Flujo de trabajo Git del proyecto LLaMA

Este documento es la **norma de integración y release** del repositorio. Su rango es **4** y su carácter es **normativo**: desarrolla el procedimiento Git que `docs/sdd/PROTOCOLO_OPERATIVO.md` fija en el rango 3 y prevalece sobre las plantillas, las specs y el código. Ante contradicción con la constitución o con `AGENTS.md` prevalece el documento de rango menor y este flujo se corrige.

## Compuertas del flujo

El flujo tiene dos compuertas: **G5** autoriza la integración de una rama de trabajo en `dev` y **G6** autoriza la publicación de un release. G5 la verifica el orquestador y G6 la aprueba el propietario mediante un commit firmado. Ningún agente declara una compuerta.

| Compuerta | Autoriza | Condición | Evidencia exigida |
|---|---|---|---|
| G5 | La integración de la rama de trabajo en `dev` | G4 aprobada, spec en `validated`, check `verify` del flujo `SDD` exigible con `strict: true` en `main` y en `dev`, Pull Request con `merge --no-ff` y validación posterior sin hallazgos | merge con dos padres, check `verify` exigible en las dos reglas de protección, validador posterior sin hallazgos y listado de ramas sin la rama integrada |
| G6 | La publicación del release | G5 cumplida, autorización firmada del propietario, auditoría de conformidad registrada, tag anotado verificado e `specs/INDEX.md` y `CHANGELOG.md` actualizados | línea de aprobación firmada en la entrada del release, informe de auditoría registrado, `git cat-file -t`, `git tag -n` y `git rev-parse` del tag |

Sin G5 no se integra y sin G6 no se publica. Una integración intentada sin la compuerta cumplida se revierte en la rama de trabajo y no se registra.

**Auditoría previa al release.** La secuencia del release es G5, después la auditoría de conformidad sobre el estado integrado en `dev` y después G6. La auditoría se ejecuta sobre el commit de merge integrado, sigue la plantilla de informe de auditoría de rango 5 y declara el veredicto calculado desde el inventario de hallazgos. El release exige el veredicto `CONFORME`; un veredicto distinto de `CONFORME` impide la publicación, conserva la spec en `validated` y transcribe el motivo con el hallazgo que lo sostiene.

## Integración

`merge --no-ff` es la única forma admitida de integración. El merge con `--no-ff` conserva la relación entre la rama de trabajo y la rama destino. Quedan prohibidos `rebase`, `squash merge` y la copia manual de archivos como mecanismo de integración.

Cada rama de trabajo se vincula a una spec: el campo `branch` del frontmatter coincide con la rama real, los commits de implementación incluyen `Spec: SPEC-NNN` en el cuerpo y no se integra una rama cuya spec esté por debajo del estado `validated`.

### Ramas

- `main`: estado estable y listo para producción. No se trabaja directamente sobre ella.
- `dev`: integración del desarrollo. Se mantiene en un estado verificable.
- `feat/<nombre>`: nueva funcionalidad, creada desde `dev`.
- `fix/<nombre>`: corrección detectada en `dev`, creada desde `dev`.
- `hotfix/<nombre>`: corrección detectada en `main`, creada desde `main`.
- `docs/<nombre>`: cambio exclusivamente documental, creado desde `dev`; no altera requisitos, comportamiento ni configuración y se registra con un commit `docs:` o `chore:`.
- `release/vX-Y-Z`: rama de empaquetado y publicación de versiones, creada desde `dev`.

Flujos:

```text
dev  -> feat/<nombre>    -> dev
dev  -> fix/<nombre>     -> dev
dev  -> docs/<nombre>    -> dev
dev  -> release/vX-Y-Z   -> dev & main
main -> hotfix/<nombre>  -> main -> dev
```

`main` y `dev` rechazan commit y push directos. Los únicos commits adicionales admitidos durante una integración son el commit de merge `--no-ff` y los commits de resolución de conflictos. La protección remota y las excepciones se declaran en «Protección y excepciones».

### Nombres de ramas

El nombre completo debe cumplir esta gramática de caracteres:

```text
^(feat|fix|hotfix|docs|release)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$
```

Reglas:

- Solo se permiten minúsculas, números y guiones.
- `<nombre>` debe tener entre 3 y 63 caracteres, sin contar el prefijo `feat/`, `fix/`, `hotfix/`, `docs/` o `release/`.
- En ramas de release se utiliza obligatoriamente la convención de guiones `vX-Y-Z` (ej. `release/v0-1-0`), evitando puntos en el nombre de la rama para prevenir colisiones en Git.
- La longitud se mide sobre `<nombre>` y no sobre la cadena completa.
- `docs/` se reserva a los cambios exclusivamente documentales y se valida con las mismas reglas de minúsculas, números y guiones y la misma longitud que los demás prefijos.
- No se permiten espacios, guiones bajos, caracteres especiales ni prefijos alternativos.
- No se permiten nombres duplicados de ramas activas.
- Las ramas se eliminan únicamente después de confirmar su integración.

La expresión valida simultáneamente el patrón de caracteres y que `3 <= longitud(<nombre>) <= 63`.

Ejemplos válidos:

```text
feat/main-menu
feat/phi4-script
fix/model-path
hotfix/server-startup
docs/cierre-integracion-spec-012
release/v0-1-0
```

### Features y fixes

Antes de integrar una rama, se actualiza con la rama destino:

```bash
git switch feat/<nombre>
git merge --no-ff dev
```

Para un fix:

```bash
git switch fix/<nombre>
git merge --no-ff dev
```

Después de validar la rama:

```bash
git switch dev
git merge --no-ff feat/<nombre>
```

o:

```bash
git switch dev
git merge --no-ff fix/<nombre>
```

### Hotfixes

El procedimiento de un hotfix es obligatorio y siempre debe seguir este orden:

1. Crear `hotfix/<nombre>` desde el último `main` estable.
2. Actualizar la rama hotfix con `main` antes de validarla.
3. Resolver cualquier conflicto dentro de `hotfix/<nombre>`.
4. Ejecutar las validaciones.
5. Integrar en `main`.
6. Sincronizar `dev` con el `main` actualizado.
7. Resolver cualquier conflicto dentro de `dev`.
8. Repetir las validaciones.

Actualizar el hotfix con `main`:

```bash
git switch hotfix/<nombre>
git merge --no-ff main
```

Integrar en `main`:

```bash
git switch main
git merge --no-ff hotfix/<nombre>
```

Después sincronizar `dev` con `main`:

```bash
git switch dev
git merge --no-ff main
```

Esto garantiza que el hotfix no desaparezca en el siguiente release.

### Conflictos

Los conflictos se resuelven únicamente en la rama definida para cada caso. Nunca se resuelven mediante cambios manuales directos sobre `main`.

Procedimiento obligatorio:

1. Ejecutar el merge indicado.
2. Si hay conflictos, ejecutar `git status`.
3. Resolver los archivos en la rama definida para ese caso.
4. Marcar los archivos resueltos con `git add <archivo>`.
5. Completar el merge con `git commit`.
6. Repetir las validaciones.
7. Continuar con el merge hacia la rama destino solo si las validaciones pasan.

Para cancelar un merge sin completarlo:

```bash
git merge --abort
```

Casos específicos:

- `feat/*` o `fix/*` hacia `dev`: resolver al actualizar la rama de trabajo con `dev`.
- `dev` hacia `main`: resolver previamente al actualizar `dev` con `main`.
- `hotfix/*` hacia `main`: resolver obligatoriamente en `hotfix/*` durante la actualización previa con `main`.
- `main` hacia `dev` después de un hotfix: resolver obligatoriamente en `dev` y repetir las validaciones.

La resolución en `dev` durante la sincronización de un hotfix es la única excepción permitida a la regla de no crear commits directos de trabajo en `dev`, porque forma parte de la integración obligatoria del hotfix.

Si una validación falla, no se completa el merge.

### Validaciones previas a la integración

Antes de cada integración se comprueba, en este orden:

1. Confirmar que los archivos modificados corresponden al alcance de la rama.
2. Ejecutar `git status --short` y confirmar que no hay cambios inesperados.
3. Ejecutar `git diff --check`.
4. Confirmar que no se añadieron modelos, binarios, dependencias ni archivos de `llama.cpp`.
5. Confirmar que los cambios mantienen coherencia con `AGENTS.md`, `README.md` y `MEMORY.md`.
6. Ejecutar `python tools\sdd\validate.py --all` (o `--spec SPEC-NNN` para una rama con spec).
7. Registrar cambios relevantes en `CHANGELOG.md` bajo `Unreleased`.

La validación se clasifica por tipo de cambio:

#### Cambios documentales

Un cambio exclusivamente documental pasa la validación cuando:

- `git diff --check` no reporta errores.
- Las rutas y referencias locales mencionadas existen o están marcadas como futuras.
- No incorpora artefactos externos.
- La documentación mantiene coherencia con las reglas del proyecto.

No requiere ejecutar un modelo.

#### Cambios en scripts `.bat`

Un cambio de script pasa la validación únicamente cuando:

- Utiliza `%~dp0`.
- Usa rutas explícitas al ejecutable y al modelo.
- Valida que el ejecutable y el modelo existan.
- El ejecutable y el modelo requeridos están disponibles localmente.
- El script se ejecuta correctamente con el modelo configurado.
- Se registran, cuando corresponda, VRAM, RAM, tokens por segundo, contexto, slots y versión de llama.cpp.

Si falta el binario o el modelo requerido, la validación queda **BLOQUEADA** y la rama no se integra. No se considera suficiente documentar que la dependencia existe.

#### Cambios de configuración de modelo

Además de las validaciones de script, se debe comprobar que:

- La cuantización corresponde al archivo utilizado.
- Los parámetros son compatibles con la arquitectura del modelo.
- El consumo de VRAM y RAM está dentro de lo esperado.
- No existe desbordamiento no documentado hacia memoria compartida.

Un resultado de `llama-bench` no sustituye la validación de un servidor con contexto largo.

#### Cambios de release

Un release pasa la validación únicamente cuando:

- `dev` contiene los cambios aprobados.
- `CHANGELOG.md` tiene entradas en `Unreleased`.
- El incremento de versión cumple las reglas de «Sincronización y tag».
- El propietario ha autorizado el release.
- La auditoría de conformidad posterior a G5 y previa a G6 declara el veredicto `CONFORME` sobre el estado integrado en `dev`.
- La validación estructural y las validaciones funcionales aplicables han pasado.

La raíz del repositorio cuenta con dos suites de pruebas: la del mecanismo de control en `tools/sdd/tests/`, con 222 pruebas, y la de las herramientas de Git en `tools/git/tests/`, con 48 pruebas. El job `verify` del flujo `SDD` de `.github/workflows/sdd.yml` las ejecuta como pasos nombrados en cada Pull Request dirigido a `main` y a `dev`: `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q`, cada uno con `timeout-minutes: 1`, dentro de un job con `timeout-minutes: 5`. El fallo de cualquiera de las dos suites deja el check `verify` en rojo y bloquea G5, y ninguna de las dos sustituye las validaciones anteriores.

### Condición de cierre de la rama

Una rama de trabajo se cierra cuando se cumplen tres condiciones: el merge en `dev` figura con dos padres, el validador posterior no reporta hallazgos y las validaciones aplicables pasaron. Mientras falte una, la integración no está cerrada y G5 no se registra.

## Eliminación de rama

La rama de trabajo se elimina después de confirmar la integración, nunca antes:

```bash
git switch dev
git branch -d feat/<nombre>
```

La eliminación se verifica sobre el listado de ramas; las dos comprobaciones deben devolver una salida vacía:

```bash
git branch --list feat/<nombre>
git branch -r --list origin/feat/<nombre>
```

Si el listado local o remoto conserva la rama, la eliminación no está confirmada y G5 no se registra. La misma regla se aplica a `fix/*`, `hotfix/*`, `docs/*` y `release/vX-Y-Z`.

## Sincronización y tag

**Sincronización previa.** Antes del empaquetado se verifica la relación de ancestría entre las dos ramas: `main` debe ser ancestro de `dev`, de modo que cada commit de `main` esté contenido en `dev`:

```bash
git merge-base --is-ancestor main dev
```

Un resultado distinto de `0` detiene el empaquetado e informa la relación de ancestría incumplida. El conteo de commits entre las dos ramas no se exige: `dev` puede estar por delante de `main` con trabajo no publicado sin que ese estado bloquee el release. La sincronización se registra como primera verificación de release.

**Tag anotado.** Solo se admiten tags anotados que cumplan esta expresión exacta:

```text
^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$
```

Esto corresponde al formato `vMAJOR.MINOR.PATCH`, con `v` minúscula, enteros sin ceros iniciales y sin componentes adicionales. No se permiten prereleases ni build metadata en esta etapa.

Antes de crear un tag, verificar que no exista:

```bash
git rev-parse --verify --quiet refs/tags/vX.Y.Z
```

El comando debe terminar sin encontrar una referencia. Los tags deben ser anotados y utilizar el mensaje exacto:

```text
Release vX.Y.Z
```

Ejemplo:

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
```

Reglas:

- `MAJOR`: cambios incompatibles.
- `MINOR`: nuevas funcionalidades compatibles.
- `PATCH`: correcciones compatibles.
- La prioridad para cambios mixtos es `MAJOR > MINOR > PATCH`.
- Antes de `v1.0.0`, un cambio incompatible incrementa `MINOR` y mantiene `MAJOR` en `0`.
- La primera versión funcional será `v0.1.0`.
- Un hotfix incrementa `PATCH`.
- Un tag publicado no se mueve, elimina ni reutiliza.
- El propietario autoriza el release y el incremento de versión.
- Cuando un release combine correcciones con adiciones derivadas de ellas, el incremento se decide por la naturaleza dominante del cambio y lo autoriza el propietario.

**Corrección de un tag publicado.** La prohibición de mover, eliminar o reutilizar un tag publicado admite una sola excepción: la corrección de una consecuencia de un release publicado, que se ejecuta antes de que un consumidor dependa del tag y que cumple tres condiciones habilitantes de forma simultánea: autorización escrita del propietario, registro del identificador del tag anterior y del destino nuevo, y ausencia de consumidores que dependan del tag. El registro del identificador anterior y del destino se transcribe en la entrada del release y en el informe de la auditoría que la motiva. Si existe un consumidor que depende del tag, la corrección no se admite y se desplaza a un release PATCH nuevo, que publica el estado corregido sin mover el tag publicado.

**Caso `v0.7.0`.** El identificador anterior del tag `v0.7.0` era `ad739a0`, que contenía el empaquetado `5da6df6` sin la cita de auditoría que la condición del incremento MINOR exige, y el destino vigente es `5a3af48`, que incorpora esa cita. La corrección quedó registrada como deuda aceptada del release publicado: el tag publicado no se mueve de nuevo y la corrección del contenido se publica como incremento PATCH en `v0.7.1`. La deuda aceptada se satisface con el procedimiento anterior y con el registro del identificador anterior y del destino en la entrada del release.

La autorización del propietario se registra en la sección del release de `CHANGELOG.md` mediante una entrada exacta:

```text
- Approved by: Agent Sebaxtian
```

Sin esa entrada no se crea el tag.

Flujo de release:

```text
dev -> sincronizar con main -> release/vX-Y-Z (empaquetado) -> PR hacia dev -> PR hacia main -> tag vX.Y.Z
```

Procedimiento obligatorio de release:

1. Sincronizar `dev` con `main`:

```bash
git switch dev
git merge --no-ff main
```

Resolver conflictos en `dev` si los hubiera, completar el merge y repetir las validaciones.

2. Crear la rama auxiliar de empaquetado `release/vX-Y-Z` desde `dev` (ej. `release/v0-1-0`):

```bash
git switch -c release/vX-Y-Z dev
```

3. Actualizar los artefactos de release exclusivamente en `release/vX-Y-Z`: los 6 artefactos de la tabla siguiente, con las claves `A1` a `A6` y el mismo límite que §15 del protocolo de rango 3. Las rutas admitidas son `CHANGELOG.md`, `specs/INDEX.md`, el frontmatter de las specs publicadas, la fila del historial de cambios de la versión de release, la fila T7 del historial de transiciones y la línea `Release:` del reporte publicado. Cualquier otra ruta exige una spec previa o un fix previo: la rama de empaquetado no incorpora código, pruebas, configuración ni documentación operativa, y una ruta fuera de los 6 artefactos detiene el empaquetado y se registra como hallazgo.

| Clave | Artefacto | Modificación admitida |
|---|---|---|
| `A1` | `CHANGELOG.md` | entrada del release e historial de releases |
| `A2` | `specs/INDEX.md` | fila de la spec publicada |
| `A3` | `spec.md` de una spec publicada | campos del frontmatter `status`, `version`, `updated` y `release` |
| `A4` | `spec.md` de una spec publicada | fila del historial de cambios de la versión de release |
| `A5` | `spec.md` de una spec publicada | fila T7 del historial de transiciones |
| `A6` | `validation_report.md` de una spec publicada | línea `Release:` con el tag del release |

4. Crear el commit de empaquetado:

```bash
git add CHANGELOG.md specs/INDEX.md specs/NNN-slug/spec.md specs/NNN-slug/validation_report.md
git commit -m "chore: prepare release vX.Y.Z"
```

5. Ejecutar las validaciones completas:

```bash
python tools/sdd/validate.py --all
```

6. Integrar `release/vX-Y-Z` en `dev` mediante Pull Request con `merge --no-ff` (o localmente con `merge --no-ff`):

```bash
git switch dev
git merge --no-ff release/vX-Y-Z
```

7. Integrar en `main` mediante Pull Request con `merge --no-ff` (o localmente con `merge --no-ff`):

```bash
git switch main
git merge --no-ff release/vX-Y-Z
```

8. Eliminar la rama auxiliar `release/vX-Y-Z` tras confirmar la integración:

```bash
git branch -d release/vX-Y-Z
```

**Excepción registrada del empaquetado de `v0.7.0`.** El commit de empaquetado `5da6df6` modificó 18 archivos en lugar de los 6 artefactos del paso 3: además de `CHANGELOG.md` y de `specs/INDEX.md`, incorporó el registro operativo de `MEMORY.md` y cambios en la suite de pruebas del mecanismo de control. La excepción queda registrada como deuda cerrada por `SPEC-015`: el alcance del paso 3 rige para el empaquetado siguiente y cualquier ruta fuera de esos 6 artefactos exige una spec previa o un fix previo.

El commit de `main` debe contener el changelog actualizado. Antes de crear el tag, verificar que no exista y después comprobar su tipo, mensaje y commit objetivo:

```bash
git rev-parse --verify --quiet refs/tags/vX.Y.Z
# El comando anterior no debe encontrar una referencia.
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git cat-file -t vX.Y.Z
git show -s --format=%s vX.Y.Z
git rev-parse vX.Y.Z^{}
git rev-parse main
```

Las dos últimas salidas deben ser iguales, `git cat-file -t vX.Y.Z` debe devolver `tag` y el asunto debe ser exactamente `Release vX.Y.Z`.

Después se verifica que el tag apunte a un commit alcanzable desde `main`:

```bash
git switch main
git merge-base --is-ancestor vX.Y.Z^{commit} main
```

Un resultado distinto de `0` detiene el release y la sincronización no se declara cumplida.

**Destino del tag.** El tag anotado apunta al commit de merge publicado en `main` y no al commit de empaquetado. La fila T7 del historial de transiciones de la spec publicada declara el identificador de ese commit de merge, la rama `main` como rama del commit y su relación de ancestría con el commit de empaquetado, con el destino `released` y el campo `release` conservados. Una fila T7 que nombra el commit de empaquetado como destino del tag se corrige y no se admite.

**Tres verificaciones de release.** Se ejecutan en este orden y las tres deben pasar: `main` ancestro de `dev` y tag del release alcanzable desde `main`; tag anotado `vX.Y.Z` con mensaje `Release vX.Y.Z` y commit objetivo verificado; `specs/INDEX.md` y `CHANGELOG.md` actualizados con la autorización de G6. Una verificación fallida detiene el release y la entrada permanece en `Unreleased`.

## Registro de la verificación

El resultado de G5 y de G6 se registra en dos soportes: en `validation_report.md` de la spec publicada y en la entrada del release de `CHANGELOG.md`. El reporte de validación es append-only después de G4: el registro de G5 y de G6 se añade sin alterar la matriz ni el dictamen.

**Modificación posterior a la publicación.** Una modificación posterior a la publicación de una entrada de release de `CHANGELOG.md` o de un artefacto de una spec publicada consta en 1 commit firmado por el propietario con una clave de `docs/sdd/firmantes_autorizados`, y el estado de firma de ese commit se transcribe en la evidencia del cierre con la notación de Git. La firma del empaquetado no se extiende a las correcciones posteriores: cada corrección se firma en su propio commit. El caso registrado es el commit `494db2e`, que modificó la entrada del release `v0.7.0` con estado de firma `N`, sin firma verificable; la modificación no se admite y su corrección se registra en un commit firmado por el propietario.

`CHANGELOG.md` mantiene `## [Unreleased]` al inicio. Las fechas utilizan ISO 8601 en UTC:

```text
YYYY-MM-DD
```

Al publicar una versión:

1. Confirmar que `Unreleased` contiene al menos una entrada `- `.
2. Convertir `Unreleased` en `vX.Y.Z`.
3. Añadir la fecha UTC, por ejemplo `## [v0.1.0] - 2026-11-10`.
4. Crear una nueva sección vacía `Unreleased`.
5. Añadir `- Approved by: Agent Sebaxtian` en la sección del release.
6. Actualizar `CHANGELOG.md` en `dev` con la versión, fecha UTC y autorización.
7. Integrar en `main` mediante `merge --no-ff`.
8. Crear el tag anotado sobre el commit publicado.

`Unreleased` se considera vacío únicamente cuando no contiene ninguna entrada `- ` debajo de sus categorías. Las categorías sin entradas deben eliminarse antes de publicar; no se deben conservar encabezados vacíos.

No crear versiones ni tags si `Unreleased` está vacío.

### Consulta del estado Git

Este documento no mantiene un registro histórico de commits, merges ni ramas temporales. El estado real del repositorio se consulta con Git:

```bash
git status --short --branch
git branch --all --verbose --no-abbrev
git log --oneline --decorate --graph --all
git tag --list
```

Los cambios históricos se conservan en el historial Git y los cambios relevantes se resumen en `CHANGELOG.md` bajo `Unreleased` hasta que se publique un release.

## Protección y excepciones

**Protección remota.** En el repositorio remoto, `main` y `dev` aplican las reglas siguientes:

| Parámetro GitHub API | main | dev | Función |
|---|---|---|---|
| `enforce_admins` | `true` | `true` | Aplica las reglas a cada rol; el bypass queda reservado al propietario en contingencias críticas. |
| `required_pull_request_reviews` | Activo (`count: 0`) | Activo (`count: 0`) | Exige Pull Request para cada integración, sin aprobaciones obligatorias en etapa unipersonal. |
| `dismiss_stale_reviews` | `true` | `true` | Invalida las revisiones previas cuando se envían commits nuevos a la rama origen. |
| `restrictions` | `users: [], teams: [], apps: []` | `users: [], teams: [], apps: []` | Bloquea el push directo a cualquier usuario, equipo o aplicación. |
| `allow_force_pushes` | `false` | `false` | Prohíbe los envíos forzados, incluidos `--force` y `--force-with-lease`. |
| `allow_deletions` | `false` | `false` | Impide el borrado de las ramas base. |
| `required_linear_history` | `false` | `false` | Admite el commit de merge `--no-ff`. |
| `require_signed_commits` | `false` | `false` | No exige firma en cada commit; la firma se exige en el commit que introduce la línea de aprobación. |
| `required_status_checks` | `verify` (`strict: true`) | `verify` (`strict: true`) | Exige el check `verify` del flujo `SDD` antes de integrar; su ausencia bloquea G5. |

Ajustes a nivel de repositorio:

| Opción de repositorio | Valor | Función |
|---|---|---|
| `allow_merge_commit` | `true` | Habilita el merge con commit explícito y sin avance rápido. |
| `allow_squash_merge` | `false` | Prohíbe el squash en el servidor remoto. |
| `allow_rebase_merge` | `false` | Prohíbe el rebase en el servidor remoto. |
| `delete_branch_on_merge` | `false` | Conserva el control manual de la eliminación de ramas después de verificar la integración. |
| `allow_auto_merge` | `false` | Desactiva las fusiones automáticas desatendidas. |

En el repositorio local, las mismas restricciones se respetan mediante el procedimiento de este documento.

**Check exigible.** El check exigible de las dos ramas es el job `verify` del flujo `SDD` de `.github/workflows/sdd.yml`, con `strict: true`: prepara el árbol con `actions/checkout@v4`, `fetch-depth: 0` y `fetch-tags: true`, instala Python 3.12 con `actions/setup-python@v5` y ejecuta `python tools/sdd/validate.py --all` y las 2 suites —`tools/sdd/tests`, con 222 pruebas, y `tools/git/tests`, con 48 pruebas— en cada Pull Request dirigido a `main` y a `dev`. La preparación con profundidad completa y descarga de etiquetas es la condición del alcance real de la comprobación `Spec:`: sin el historial completo el rango se reduce al último commit descargado y sin las etiquetas el corte del último release no se resuelve, de modo que la comprobación no examinaría commit de implementación alguno. La exigibilidad se declara en `tools/git/protection_rules/main.json` y `tools/git/protection_rules/dev.json`, se aplica con `python tools/git/configure_branch_protection.py` y se verifica con `python tools/git/verify_branch_protection.py`. Si una de las dos ramas no declara exigible el check `verify`, la verificación de G5 queda bloqueada y el caso se registra como ausencia del check exigible.

**Excepción editorial.** Un cambio exclusivamente editorial —erratas, formato y enlaces— se integra sin spec, siempre que no altere reglas, requisitos, comportamiento, configuración ni scripts, y se registra en un commit `docs:` o `chore:`.

**Excepción de ramas de release.** `release/vX-Y-Z` se dedica al empaquetado de los 6 artefactos de las claves `A1` a `A6` de la tabla del paso 3; no introduce código funcional ni cambios de requisito, cualquier otra ruta exige una spec previa o un fix previo y se integra por Pull Request con `merge --no-ff`.

### Contenido excluido del repositorio

Los resultados permanentes de benchmark revisados y documentados pueden versionarse dentro de `docs/`. Los resultados temporales deben guardarse en `logs/`, `results/` o `tmp/`, que están excluidos por `.gitignore`.

El repositorio no distribuye junto con el proyecto completo:

- Modelos descargados.
- Binarios precompilados o compilados.
- Dependencias instalables.
- Controladores o firmware.
- El repositorio fuente `llama.cpp`.

Estos componentes deben obtenerse desde sus fuentes oficiales y tienen licencias independientes de la licencia MIT del material propio del proyecto.

La titularidad de `LICENSE` está confirmada por el propietario: `Agent Sebaxtian` es la identidad legal definitiva, `agent@sebaxtian.dev` es el correo que se desea publicar y el titular posee los derechos del material propio incluido. La licencia MIT no autoriza redistribuir componentes externos cuyas licencias sean diferentes.
