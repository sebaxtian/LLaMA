# Flujo de trabajo Git del proyecto LLaMA

Este documento define de forma determinista la estrategia de ramas, integración, conflictos, releases y versionado del proyecto `LLaMA`.

## Ramas

- `main`: estado estable y listo para producción. No se trabaja directamente sobre ella.
- `dev`: integración del desarrollo. Debe mantenerse en un estado verificable.
- `feat/<nombre>`: nueva funcionalidad, creada desde `dev`.
- `fix/<nombre>`: corrección detectada en `dev`, creada desde `dev`.
- `hotfix/<nombre>`: corrección detectada en `main`, creada desde `main`.

Flujos:

```text
dev  -> feat/<nombre>   -> dev
dev  -> fix/<nombre>    -> dev
main -> hotfix/<nombre> -> main -> dev
```

No se utilizarán ramas `release/*` en esta etapa.

`main` y `dev` son ramas protegidas por política del proyecto:

- No se permite crear commits directos de trabajo en `main`.
- No se permite crear commits directos de trabajo en `dev`; los cambios deben llegar mediante `feat/*`, `fix/*` o `hotfix/*`.
- Los únicos commits adicionales permitidos durante una integración son los commits de merge `--no-ff` y los commits de resolución de conflictos definidos en este documento.
- El commit `chore: prepare release vX.Y.Z` está autorizado directamente en `dev` como excepción exclusiva para preparar un release; solo puede modificar `CHANGELOG.md`, debe realizarse después de las validaciones y debe integrarse posteriormente en `main` mediante `merge --no-ff`.
- En un repositorio remoto, estas reglas deben implementarse mediante protección de ramas. En un repositorio local, deben cumplirse mediante este procedimiento operativo.

## Nombres de ramas

El nombre completo debe cumplir esta gramática de caracteres:

```text
^(feat|fix|hotfix)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$
```

Reglas:

- Solo se permiten minúsculas, números y guiones.
- `<nombre>` debe tener entre 3 y 63 caracteres, sin contar el prefijo `feat/`, `fix/` o `hotfix/`.
- La longitud se mide sobre `<nombre>` y no sobre la cadena completa.
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
```

## Estrategia de integración

La única estrategia permitida es `merge --no-ff`.

No se utilizarán:

- `rebase` para integrar ramas compartidas.
- `squash merge`.
- Copia manual de archivos como mecanismo de integración.

El merge con `--no-ff` conserva la relación entre la rama de trabajo y la rama destino.

### Features y fixes

Antes de integrar una rama, actualizarla con la rama destino:

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

## Conflictos

Los conflictos se resuelven únicamente en la rama definida para cada caso. Nunca se deben resolver mediante cambios manuales directos sobre `main`.

Procedimiento obligatorio:

1. Ejecutar el merge indicado.
2. Si hay conflictos, ejecutar `git status`.
3. Resolver los archivos en la rama definida para ese caso.
4. Marcar los archivos resueltos con `git add <archivo>`.
5. Completar el merge con `git commit`.
6. Repetir todas las validaciones.
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

## Validaciones obligatorias

Antes de cada integración:

1. Confirmar que los archivos modificados corresponden al alcance de la rama.
2. Ejecutar `git status --short` y confirmar que no hay cambios inesperados.
3. Ejecutar `git diff --check`.
4. Confirmar que no se añadieron modelos, binarios, dependencias ni archivos de `llama.cpp`.
5. Confirmar que los cambios mantienen coherencia con `AGENTS.md`, `README.md` y `MEMORY.md`.
6. Registrar cambios relevantes en `CHANGELOG.md` bajo `Unreleased`.

La validación se clasifica por tipo de cambio:

### Cambios documentales

Un cambio exclusivamente documental pasa la validación cuando:

- `git diff --check` no reporta errores.
- Las rutas y referencias locales mencionadas existen o están marcadas como futuras.
- No incorpora artefactos externos.
- La documentación mantiene coherencia con las reglas del proyecto.

No requiere ejecutar un modelo.

### Cambios en scripts `.bat`

Un cambio de script pasa la validación únicamente cuando:

- Utiliza `%~dp0`.
- Usa rutas explícitas al ejecutable y al modelo.
- Valida que el ejecutable y el modelo existan.
- El ejecutable y el modelo requeridos están disponibles localmente.
- El script se ejecuta correctamente con el modelo configurado.
- Se registran, cuando corresponda, VRAM, RAM, tokens por segundo, contexto, slots y versión de llama.cpp.

Si falta el binario o el modelo requerido, la validación queda **BLOQUEADA** y la rama no se integra. No se considera suficiente documentar que la dependencia existe.

### Cambios de configuración de modelo

Además de las validaciones de script, se debe comprobar que:

- La cuantización corresponde al archivo utilizado.
- Los parámetros son compatibles con la arquitectura del modelo.
- El consumo de VRAM y RAM está dentro de lo esperado.
- No existe desbordamiento no documentado hacia memoria compartida.

Un resultado de `llama-bench` no sustituye la validación de un servidor con contexto largo.

### Cambios de release

Un release pasa la validación únicamente cuando:

- `dev` contiene todos los cambios aprobados.
- `CHANGELOG.md` tiene entradas en `Unreleased`.
- El incremento SemVer cumple las reglas de este documento.
- El propietario ha autorizado el release.
- La validación estructural y las validaciones funcionales aplicables han pasado.

No existe actualmente una suite automatizada de tests para el proyecto raíz. La ausencia de una suite no elimina las validaciones obligatorias anteriores.

## Bootstrap determinista

Git 2.28 o superior es requisito para utilizar `git init -b main`.

Ejecutar desde la raíz del proyecto:

```bash
git --version
git init -b main
git branch --show-current
```

La última salida debe ser exactamente `main`. Si no lo es, detener el procedimiento y corregir antes de crear commits:

```bash
git branch -M main
git branch --show-current
```

Si `git init -b main` no está disponible, el procedimiento debe detenerse. No se utilizará un comportamiento implícito de la configuración global de Git.

Antes del primer commit, verificar:

```bash
git status --short
git ls-files --others --exclude-standard
```

La lista esperada contiene exactamente:

```text
.gitignore
AGENTS.md
CHANGELOG.md
LICENSE
MEMORY.md
README.md
bin/.gitkeep
docs/Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md
docs/Flujo_de_Trabajo_Git.md
models/.gitkeep
src/.gitkeep
```

Crear el primer commit con mensaje exacto:

```bash
git add .gitignore AGENTS.md CHANGELOG.md LICENSE MEMORY.md README.md
git add bin/.gitkeep models/.gitkeep src/.gitkeep
git add docs/Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md
git add docs/Flujo_de_Trabajo_Git.md
git commit -m "chore: initialize project structure"
```

Verificar el commit:

```bash
git rev-parse --verify HEAD
git status --short
```

El estado debe estar limpio. Crear `dev` desde el primer commit de `main`:

```bash
git switch -c dev main
git rev-parse main
git rev-parse dev
```

Ambos hashes deben ser iguales. Volver a `main`:

```bash
git switch main
git branch --show-current
```

## Semantic Versioning y tags

Solo se permiten tags que cumplan esta expresión exacta:

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

La autorización del propietario se registra en la sección del release de `CHANGELOG.md` mediante una entrada exacta:

```text
- Approved by: Agent Sebaxtian
```

Sin esa entrada no se crea el tag.

Flujo de release:

```text
dev -> sincronizar con main -> validación -> CHANGELOG.md -> main -> tag vX.Y.Z
```

Procedimiento obligatorio de release:

```bash
git switch dev
git merge --no-ff main
```

Resolver conflictos en `dev`, completar el merge y repetir las validaciones. Después:

```bash
git status --short
# Actualizar CHANGELOG.md en dev con la versión y fecha UTC.
git add CHANGELOG.md
git commit -m "chore: prepare release vX.Y.Z"
git switch main
git merge --no-ff dev
git rev-parse main
git rev-parse dev
```

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

## CHANGELOG.md

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

## Resultados locales y artefactos externos

Los resultados permanentes de benchmark revisados y documentados pueden versionarse dentro de `docs/`. Los resultados temporales deben guardarse en `logs/`, `results/` o `tmp/`, que están excluidos por `.gitignore`.

El repositorio no distribuye junto con el proyecto completo:

- Modelos descargados.
- Binarios precompilados o compilados.
- Dependencias instalables.
- Controladores o firmware.
- El repositorio fuente `llama.cpp`.

Estos componentes deben obtenerse desde sus fuentes oficiales y tienen licencias independientes de la licencia MIT del material propio del proyecto.

La titularidad de `LICENSE` está confirmada por el propietario: `Agent Sebaxtian` es la identidad legal definitiva, `agent@sebaxtian.dev` es el correo que se desea publicar y el titular posee los derechos del material propio incluido. La licencia MIT no autoriza redistribuir componentes externos cuyas licencias sean diferentes.

## Estado actual

- El repositorio Git todavía no ha sido inicializado.
- Aún no existen las ramas `main` ni `dev`.
- Aún no existen ramas `feat/*`, `fix/*` ni `hotfix/*`.
- Todavía no se ha publicado ningún release ni tag.
- `src/` y `models/` contienen únicamente sus respectivos `.gitkeep`.
