# Plan técnico — SPEC-007

## Referencias

- `spec.md`: `SPEC-007`, versión 0.2.0 (estado `planned`, compuerta G1 aprobada formalmente el 2026-11-13 por Agent Sebaxtian).
- `clarify.md`: `SPEC-007`, cerrado con AMB-001 a AMB-006 resueltos y parches aplicados a `spec.md`.
- Documentos normativos afectados: `docs/Flujo_de_Trabajo_Git.md`, `AGENTS.md`, `MEMORY.md` y `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- Herramientas y automatización: `tools/git/` (configuración y verificación determinista de protección de ramas).

## Arquitectura de módulos

El sistema de protección determinista de ramas implementa el modelo Opción D mediante una arquitectura desacoplada en tres niveles:

1. **Nivel de Gobernanza y Configuración Remota (GitHub Platform Layer):**
   - Configuración declarativa de reglas de protección clásicas (`Classic Branch Protection Rules`) para las ramas `main` y `dev` mediante la API REST de GitHub.
   - Ajustes globales del repositorio (`Repository Settings`) para restringir de manera absoluta los métodos de integración de Pull Requests, admitiendo exclusivamente commits de fusión sin avance rápido (`merge --no-ff`) y deshabilitando fusiones por squash y rebase.
   - Especificaciones declarativas estructuradas en archivos de configuración JSON versionados (`tools/git/protection_rules/`) para garantizar reproducibilidad e inmutabilidad.

2. **Nivel de Automatización y Verificación (Deterministic Tooling Layer):**
   - Módulo de aprovisionamiento y auditoría remota (`tools/git/configure_branch_protection.py` y `tools/git/verify_branch_protection.py`).
   - Lectura de credenciales gobernadas a través de GitHub CLI (`gh auth token`) o variables de entorno locales protegidas, invocando endpoints deterministas de la API REST v3 de GitHub.
   - Verificador de estado con validación exhaustiva de parámetros booleanos y numéricos, devolviendo código de salida 0 en conformidad y 1 en presencia de desvíos.

3. **Nivel de Alineación Normativa (Governance Documentation Layer):**
   - Actualización armónica y sincronizada de los cuatro documentos rectores del repositorio (`docs/Flujo_de_Trabajo_Git.md`, `AGENTS.md`, `MEMORY.md` y `docs/sdd/PROTOCOLO_OPERATIVO.md`).
   - Erradicación definitiva de cualquier excepción que permita commits directos sobre `dev` o `main`.
   - Formalización del ciclo de vida y nomenclatura estricta de las ramas auxiliares de empaquetado `release/vX-Y-Z` como ramas transitorias exentas de especificación funcional previa.

```text
+-----------------------------------------------------------------------------------+
|                           Nivel de Alineación Normativa                           |
|  - docs/Flujo_de_Trabajo_Git.md (Ramas release/vX-Y-Z, fin de push directo en dev) |
|  - docs/sdd/PROTOCOLO_OPERATIVO.md §8 (Excepción formal para release/vX-Y-Z)     |
|  - AGENTS.md (Restricción de ramas e inmutabilidad)                              |
|  - MEMORY.md (Mapa operativo y directrices de protección remota)                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     Nivel de Automatización y Verificación                        |
|  - tools/git/configure_branch_protection.py (Aprovisionador determinista)        |
|  - tools/git/verify_branch_protection.py (Auditor de reglas activas)             |
|  - tools/git/protection_rules/*.json (Especificaciones declarativas de ramas)    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Nivel de Configuración Remota                              |
|  - GitHub Repository Settings: PATCH /repos/:owner/:repo                          |
|      * allow_merge_commit: true                                                   |
|      * allow_squash_merge: false                                                  |
|      * allow_rebase_merge: false                                                  |
|  - Classic Branch Protection API: PUT /repos/:owner/:repo/branches/:b/protection |
|      * main: enforce_admins, required_reviews(0), no direct push, no force/delete|
|      * dev:  enforce_admins, required_reviews(0), no direct push, no force/delete|
+-----------------------------------------------------------------------------------+
```

## Esquemas, tipos e interfaces

### Contrato de Ajustes de Repositorio (GitHub REST API v3)

- **Endpoint:** `PATCH /repos/{owner}/{repo}`
- **Esquema JSON del Payload:**

```json
{
  "allow_merge_commit": true,
  "allow_squash_merge": false,
  "allow_rebase_merge": false,
  "allow_auto_merge": false,
  "delete_branch_on_merge": false
}
```

### Contrato de Protección Clásica de Ramas (GitHub REST API v3)

- **Endpoint:** `PUT /repos/{owner}/{repo}/branches/{branch}/protection`
- **Cabecera obligatoria:** `Accept: application/vnd.github+json`
- **Esquema JSON del Payload (idéntico para `main` y `dev`):**

```json
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0,
    "require_last_push_approval": false
  },
  "restrictions": {
    "users": [],
    "teams": [],
    "apps": []
  },
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "required_linear_history": false
}
```

### Interfaz del Script Auditor `verify_branch_protection.py`

- **Firma:** `def verify_protection(owner: str, repo: str, branch: str, expected_config: dict) -> list[str]`
  - Recibe el propietario, nombre de repositorio, nombre de la rama auditada (`main` o `dev`) y el diccionario de configuración canónica esperada.
  - Retorna una lista de discrepancias detectadas; si la lista está vacía, la rama cumple con exactitud la especificación.
- **Firma:** `def verify_repo_settings(owner: str, repo: str) -> list[str]`
  - Evalúa que `allow_merge_commit == True`, `allow_squash_merge == False` y `allow_rebase_merge == False`.
- **Códigos de salida del comando CLI:**
  - `0`: Configuración remota plenamente convergida con la especificación.
  - `1`: Desvío detectado en parámetros de protección o ajustes de fusión.
  - `2`: Error de conectividad, autenticación o parámetros de invocación.

## Decisiones técnicas

### DEC-001: Mecanismo de protección en GitHub (Classic Branch Protection vs Rulesets)

- **Decisión:** Implementar las reglas de protección remota utilizando la API clásica de protección de ramas de GitHub (`Classic Branch Protection Rules` mediante el endpoint REST `/branches/{branch}/protection`), complementada con los ajustes de repositorio para los métodos de fusión.
- **Justificación:**
  1. Compatibilidad universal: Classic Branch Protection se encuentra disponible de forma homogénea en repositorios públicos y privados sin distinción de planes (Free, Pro, Team o Enterprise).
  2. Determinismo: la API REST v3 de protección clásica cuenta con un esquema de parámetros directo, exhaustivo y documentado formalmente para `restrictions`, `enforce_admins`, `required_pull_request_reviews`, `allow_force_pushes` y `allow_deletions`.
  3. Soporte en GitHub CLI: permite inspección y actualización inmediata mediante comandos `gh api` sin dependencias de esquemas jerárquicos variables.
- **Alternativas descartadas:**
  - *GitHub Repository Rulesets (v2):* descartado debido a que la granularidad de sus reglas y la aplicación de excepciones de bypass presentan variaciones según el tipo de plan de la cuenta, introduciendo sobrecarga de configuración innecesaria para un repositorio en etapa unipersonal.
  - *Configuración manual exclusiva por interfaz web:* descartada por carecer de trazabilidad determinista y reproducibilidad automatizada, vulnerando el requisito RNF-005.

### DEC-002: Parámetros exactos de protección para las ramas `main` y `dev`

- **Decisión:** Configurar parámetros estrictos e idénticos en ambas ramas (`main` y `dev`):
  1. `required_status_checks: null`: diferido formalmente a la especificación posterior de CI (AMB-004).
  2. `enforce_admins: true`: las reglas de protección aplican por defecto a todos los roles, previniendo fallos accidentales del Propietario. El bypass se restringe a emergencias críticas de infraestructura autorizadas expresamente (RF-008).
  3. `required_pull_request_reviews.required_approving_review_count: 0`: umbral fijado en cero revisiones obligatorias para la etapa unipersonal actual, evitando deadlocks donde el autor del PR no puede autoaprobarse en la plataforma (AMB-003, RF-009, CA-010).
  4. `required_pull_request_reviews.dismiss_stale_reviews: true`: descarte automático de aprobaciones obsoletas ante nuevos envíos.
  5. `restrictions: { "users": [], "teams": [], "apps": [] }`: activación del bloqueo de envíos directos; ningún actor puede realizar `push` directo fuera del mecanismo de Pull Requests (RF-002).
  6. `allow_force_pushes: false`: prohibición irrevocable de envíos forzados bajo cualquier modalidad (`--force`, `--force-with-lease`) (RF-003, CB-001, CA-002).
  7. `allow_deletions: false`: prohibición de eliminación de las ramas protegidas (RF-004, CB-006, CA-003).
  8. `required_linear_history: false`: debe permanecer inactivo (`false`), dado que en GitHub la activación de historial lineal prohíbe de manera forzada los commits de fusión `merge --no-ff`, contradiciendo el principio fundacional de la constitución del proyecto.
  9. `require_signed_commits: false`: desactivado inicialmente para preservar la continuidad de agentes y entornos locales sin infraestructura de llaves criptográficas estandarizadas (AMB-006, RF-010, CB-011, CA-011).
- **Alternativas descartadas:**
  - *Exigir 1 aprobación mínima (`required_approving_review_count: 1`):* descartado porque en desarrollo unipersonal bloquea de manera insalvable la integración de cualquier PR del Propietario.
  - *Activar `required_linear_history: true`:* descartado porque GitHub bloquea los commits generados con `merge --no-ff` al forzar únicamente rebase o squash.

### DEC-003: Desactivación global de squash y rebase en ajustes de repositorio

- **Decisión:** Modificar la configuración general del repositorio remoto (`PATCH /repos/{owner}/{repo}`) fijando `allow_merge_commit: true`, `allow_squash_merge: false` y `allow_rebase_merge: false`.
- **Justificación:**
  1. Hace cumplir a nivel de servidor la regla constitucional de conservar la topología de grafo con commits de fusión reales sin avance rápido (`merge --no-ff`).
  2. Elimina la posibilidad de errores humanos en la interfaz gráfica web de GitHub, suprimiendo los botones de «Squash and merge» y «Rebase and merge».
- **Alternativas descartadas:**
  - *Confiar únicamente en la disciplina procedimental humana:* descartado por no proveer una barrera determinista frente a selecciones erróneas en la interfaz web.

### DEC-004: Erradicación absoluta de la excepción de push directo en `dev`

- **Decisión:** Suprimir de manera integral la cláusula que admitía commits directos de tipo `chore: prepare release vX.Y.Z` en la rama `dev`.
- **Justificación:**
  1. Conforme a la resolución de AMB-002, toda rama protegida debe mantener trazabilidad inmaculada mediante Pull Requests gobernados.
  2. Permitir excepciones debilita la política de seguridad y abre brechas operativas.
  3. El empaquetado de release se canaliza a partir de ahora de forma limpia a través de ramas dedicadas.
- **Alternativas descartadas:**
  - *Mantener push directo exclusivo para el usuario administrador:* descartado porque vulnera el principio de auditoría remota homogénea y el requerimiento RF-002.

### DEC-005: Creación y regulación de ramas auxiliares `release/vX-Y-Z`

- **Decisión:** Incorporar al flujo de trabajo Git y al protocolo SDD la tipología de ramas transitorias de empaquetado con nomenclatura fija `release/vX-Y-Z` (ejemplo: `release/v0-2-0`, `release/v0-6-0`).
- **Propiedades técnicas y operativas:**
  1. Nomenclatura: utiliza guiones en la versión para evitar conflictos con el espacio de nombres de referencias Git (`refs/heads/release/v0.2.0` frente al tag anotado `refs/tags/v0.2.0`).
  2. Exención SDD: exentas de requerir una especificación funcional previa (`spec.md`), formalizado como una excepción explícita en §8 de `docs/sdd/PROTOCOLO_OPERATIVO.md` junto a la Etapa 1 y el cambio editorial (AMB-001, CB-009, CA-009).
  3. Alcance de modificaciones: restringido exclusivamente al empaquetado de versión (`CHANGELOG.md`, `specs/INDEX.md`, frontmatter de la spec publicada).
  4. Flujo de integración: creada desde `dev` actualizado, procesa los cambios de release, abre Pull Request hacia `dev` y posteriormente hacia `main` (o sincronización de release), integrándose siempre con `merge --no-ff` y eliminándose tras la publicación y etiquetado con tag anotado.
- **Alternativas descartadas:**
  - *Nombrar con puntos `release/v0.2.0`:* descartado para prevenir colisiones en el sistema de referencias de Git.
  - *Exigir una spec SDD para cada corte de release:* descartado por introducir burocracia sin aporte de especificación de software, al tratarse de un procedimiento puramente de empaquetado.

### DEC-006: Mapeo y actualización armónica de documentos de gobernanza

- **Decisión:** Actualizar de manera sincrónica y coherente los cuatro documentos de referencia del proyecto durante la implementación de la spec:
  1. `docs/Flujo_de_Trabajo_Git.md`:
     - Modificar §Ramas para listar formalmente `release/vX-Y-Z`.
     - Actualizar §Nombres de ramas para incluir la expresión regular de validación:
       `^(feat|fix|hotfix)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$|^release/v[0-9]+-[0-9]+-[0-9]+$`
     - Modificar §Procedimiento obligatorio de release: sustituir el commit directo en `dev` por la creación de la rama `release/vX-Y-Z` y su integración vía Pull Request.
     - Modificar §Excepciones: registrar la exención de spec para ramas `release/vX-Y-Z`.
  2. `AGENTS.md`:
     - Reflejar la regla de no push directo a `dev` y la admisión de ramas `release/vX-Y-Z`.
     - Mantener la extensión del archivo estrictamente dentro del rango de 30 a 70 líneas útiles conforme a la validación de `validate.py`.
  3. `MEMORY.md`:
     - Registrar en la sección de Git y flujo de trabajo que la protección de ramas en GitHub está formalmente activa, las ramas protegidas son `main` y `dev`, y las fusiones squash y rebase están deshabilitadas en el repositorio remoto.
  4. `docs/sdd/PROTOCOLO_OPERATIVO.md`:
     - Actualizar §8 (Excepciones) para documentar formalmente la excepción de ramas auxiliares de release (`release/vX-Y-Z`) junto a la Etapa 1 y el cambio editorial.
- **Alternativas descartadas:**
  - *Actualizar solo Flujo_de_Trabajo_Git.md:* descartado porque la inconsistencia con AGENTS.md, MEMORY.md y PROTOCOLO_OPERATIVO.md genera contradicciones normativas prohibidas por la constitución.

### DEC-007: Script determinista de aprovisionamiento y verificación

- **Decisión:** Implementar scripts en Python utilizando la biblioteca estándar (`tools/git/configure_branch_protection.py` y `tools/git/verify_branch_protection.py`) que consuman especificaciones JSON declarativas y se comuniquen con la API de GitHub mediante tokens o GitHub CLI (`gh`).
- **Justificación:**
  1. Permite ejecutar la verificación en cualquier momento de manera automatizada.
  2. Facilita la auditoría determinista en compuertas de control o pipelines locales.
  3. Permite la regeneración de reglas si el repositorio sufre alguna modificación accidental.
- **Alternativas descartadas:**
  - *Scripts basados exclusivamente en PowerShell:* descartado para mantener uniformidad con las herramientas SDD del proyecto desarrolladas en Python con biblioteca estándar.

## Estrategia de testing

La validación de la protección de ramas se organiza en dos niveles complementarios: pruebas de verificación de configuración remota mediante API y pruebas operativas de rechazo determinista sobre el repositorio remoto.

### 1. Nivel de Verificación Declarativa de Configuración (API REST GitHub)

Se ejecutan consultas autenticadas mediante GitHub CLI (`gh api`) o el script auditor `tools/git/verify_branch_protection.py`:

- **Verificación de ajustes del repositorio (RF-005, CB-004):**
  - **Comando:** `gh api repos/{owner}/{repo} --jq "{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge}"`
  - **Salida esperada:** `{"merge": true, "squash": false, "rebase": false}`
  - **Código de salida:** `0`
- **Verificación de reglas en `main` (RF-001, RF-003, RF-004, RF-008, RF-009, RF-010):**
  - **Comando:** `gh api repos/{owner}/{repo}/branches/main/protection --jq "{force: .allow_force_pushes.enabled, delete: .allow_deletions.enabled, admins: .enforce_admins.enabled, reviews: .required_pull_request_reviews.required_approving_review_count, restrictions: (.restrictions != null)}"`
  - **Salida esperada:** `{"force": false, "delete": false, "admins": true, "reviews": 0, "restrictions": true}`
  - **Código de salida:** `0`
- **Verificación de reglas en `dev` (RF-001, RF-002, RF-003, RF-004, RF-008, RF-009, RF-010):**
  - **Comando:** `gh api repos/{owner}/{repo}/branches/dev/protection --jq "{force: .allow_force_pushes.enabled, delete: .allow_deletions.enabled, admins: .enforce_admins.enabled, reviews: .required_pull_request_reviews.required_approving_review_count, restrictions: (.restrictions != null)}"`
  - **Salida esperada:** `{"force": false, "delete": false, "admins": true, "reviews": 0, "restrictions": true}`
  - **Código de salida:** `0`

### 2. Nivel de Pruebas Deterministas de Rechazo Remoto (Git Engine Rejection Tests)

Pruebas operativas directas invocadas mediante el cliente Git local apuntando al remoto `origin`:

- **Prueba 1: Rechazo de envío directo sin Pull Request (CA-001, RF-002, CB-005):**
  - **Acción:** Creación de un commit de prueba local sobre `dev` o intento de push de un commit huérfano:
    `git push origin HEAD:dev`
  - **Salida esperada:** Error devuelto por GitHub:
    `remote: error: GH006: Protected branch update failed for refs/heads/dev.` o mensaje indicando que los commits deben canalizarse por Pull Request.
  - **Código de salida:** Distinto de 0 (`!= 0`, fallo controlado).
- **Prueba 2: Rechazo irrevocable de envío forzado (CA-002, RF-003, CB-001):**
  - **Acción:** Intento de envío forzado convencional o con lease hacia `main` o `dev`:
    `git push origin feat/branch-protection:dev --force`
    `git push origin feat/branch-protection:dev --force-with-lease`
  - **Salida esperada:** Error devuelto por GitHub:
    `remote: error: GH003: Protected branch update failed ... cannot force push to protected branch`
  - **Código de salida:** Distinto de 0 (`!= 0`, fallo controlado).
- **Prueba 3: Rechazo de eliminación remota de ramas protegidas (CA-003, RF-004, CB-006):**
  - **Acción:** Intento de supresión de rama remota:
    `git push origin --delete dev`
    `git push origin --delete main`
  - **Salida esperada:** Error devuelto por GitHub:
    `remote: error: GH006: Protected branch update failed ... branch deletion not allowed`
  - **Código de salida:** Distinto de 0 (`!= 0`, fallo controlado).

### 3. Nivel de Pruebas de Validador SDD y Consistencia Global

- **Comando de validación SDD:**
  - `python tools\sdd\validate.py --all`
  - **Salida esperada:** 0 errores.
  - **Código de salida:** `0`.
- **Comprobación de líneas de `AGENTS.md`:**
  - Verificar que las líneas no vacías se encuentren estrictamente entre 30 y 70.

## Matriz de cobertura

| Requisito / Caso Borde | Componente / Regla | Prueba / Comando |
|---|---|---|
| RF-001 | Classic Branch Protection API (`main`, `dev`) | Auditoría remota con `gh api /branches/{main,dev}/protection` validando reglas activas |
| RF-002 | Protección de rama: `restrictions` activa | Prueba Git: intento de `git push origin HEAD:dev` sin PR genera rechazo GH006 con salida `!= 0` |
| RF-003 | Protección de rama: `allow_force_pushes: false` | Prueba Git: intento de `git push origin ... --force` genera rechazo GH003 con salida `!= 0` |
| RF-004 | Protección de rama: `allow_deletions: false` | Prueba Git: intento de `git push origin --delete dev` genera rechazo GH006 con salida `!= 0` |
| RF-005 | Ajustes de repositorio: `allow_merge_commit`, no squash/rebase | Auditoría remota con `gh api repos/:owner/:repo` confirmando `merge=true, squash=false, rebase=false` |
| RF-006 | Protección de rama: `required_status_checks` | Verificación de esquema diferido a spec de CI y validación local con `validate.py` |
| RF-007 | Gestión de Pull Requests en GitHub | Verificación de interfaz remota ante ramas base desactualizadas |
| RF-008 | Bypass gobernado: `enforce_admins: true` (Admin Agent Sebaxtian) | Inspección de auditoría de configuración remota en GitHub |
| RF-009 | Protección de rama: `required_approving_review_count: 0` | Auditoría remota con `gh api` confirmando 0 revisiones obligatorias en fase unipersonal |
| RF-010 | Protección de rama: sin exigencia de firmas criptográficas | Auditoría remota confirmando `required_signatures` inactivo y admisión de commit no firmado |
| CB-001 | Protección de rama: rechazo de `--force-with-lease` | Prueba Git: `git push origin ... --force-with-lease` genera rechazo inmediato con salida `!= 0` |
| CB-002 | Detección de rama base desactualizada en Pull Request | Prueba remota: PR no sincronizado con base actualizada reporta necesidad de actualización |
| CB-003 | Fallo o cancelación en checks de CI requeridos | Condicionado a la futura especificación de flujos de CI |
| CB-004 | Intento de fusión con modalidad squash o rebase | Consulta API: interfaz remota no ofrece opciones squash o rebase |
| CB-005 | Push directo de `chore: prepare release` a `dev` | Prueba Git: push directo con dicho commit en `dev` es rechazado por `restrictions` (`!= 0`) |
| CB-006 | Intento de eliminación remota vía `git push origin --delete` | Prueba Git: eliminación remota de `dev` o `main` es abortada por el servidor (`!= 0`) |
| CB-007 | Reinicio de validación ante nuevos commits en PR | Condicionado a la futura especificación de flujos de CI |
| CB-008 | Sincronización de hotfix con fallos de CI | Condicionado a la futura especificación de flujos de CI |
| CB-009 | Creación y procesamiento de rama `release/vX-Y-Z` sin spec previa | Validación SDD: `tools/sdd/validate.py` no exige spec para ramas `release/vX-Y-Z` |
| CB-010 | Fusión de PR por el autor sin revisores externos | Integración fluida de PR unipersonal sin bloqueo por falta de revisores de terceros |
| CB-011 | Aceptación de commits sin firma digital GPG/SSH | Integración exitosa de commit sin firma criptográfica vía PR gobernado |
