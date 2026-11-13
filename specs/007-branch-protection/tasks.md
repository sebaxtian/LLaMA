# Tareas — SPEC-007

## Progreso

- [x] 10 de 10 tareas completadas (100% G3 alcanzado).

## Tareas

Orden de ejecución y dependencias:
- Grupo 1 (Normativa): `T-001` sin dependencias; `T-002` depende de `T-001`.
- Grupo 2 (Herramientas y esquemas): `T-003` sin dependencias; `T-004` depende de `T-003`; `T-005` depende de `T-004`.
- Grupo 3 (Configuración remota en GitHub): `T-006` depende de `T-003`, `T-004` y `T-005`; `T-007` y `T-008` dependen de `T-006`.
- Grupo 4 (Validación remota y cierre): `T-009` depende de `T-007` y `T-008`; `T-010` depende de `T-001`, `T-002`, `T-005`, `T-007`, `T-008` y `T-009`.

El grafo de dependencias es estrictamente acíclico (DAG).

### T-001: Actualización normativa en Flujo de Trabajo Git y Protocolo SDD

- **ID:** `T-001`
- **Título:** Actualización normativa en Flujo de Trabajo Git y Protocolo SDD
- **Estado:** [x]
- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `CB-009`, `RNF-001`, `CA-009`.
- **Archivos permitidos:** `docs/Flujo_de_Trabajo_Git.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `Select-String -Path docs/Flujo_de_Trabajo_Git.md -Pattern "release/vX-Y-Z"` confirma la formalización de ramas de empaquetado y la eliminación de la excepción de push directo en `dev`.
  2. `Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern "release/vX-Y-Z"` confirma la exención formal de spec en §8.
  3. `python tools/sdd/validate.py --all` devuelve código de salida `0`.
- [x] Completada.
- **Evidencia:**
  1. `Select-String -Path docs/Flujo_de_Trabajo_Git.md -Pattern "release/vX-Y-Z"` confirmó 8 coincidencias normativas incluyendo la definición formal en §Ramas, la gramática en §Nombres de ramas (`^(feat|fix|hotfix|release)/(?=[a-z0-9-]{3,63}$)[a-z0-9]+(-[a-z0-9]+)*$`), la eliminación del push directo en `dev` y el nuevo flujo de empaquetado e integración por Pull Request.
  2. `Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern "release/vX-Y-Z"` confirmó la exención formal de spec SDD previa para ramas operativas de empaquetado en §8.
  3. `python tools/sdd/validate.py --all` finalizó con código de salida `0` sin errores.

### T-002: Actualización de gobernanza y memoria operativa en AGENTS.md y MEMORY.md

- **ID:** `T-002`
- **Título:** Actualización de gobernanza y memoria operativa en AGENTS.md y MEMORY.md
- **Estado:** [x]
- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RNF-001`, `CB-005`.
- **Archivos permitidos:** `AGENTS.md`, `MEMORY.md`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -c "lines = [l for l in open('AGENTS.md', encoding='utf-8').read().splitlines() if l.strip()]; assert 30 <= len(lines) <= 70, f'Líneas útiles: {len(lines)}'"` devuelve código `0` comprobando que las líneas útiles de `AGENTS.md` están estrictamente dentro del rango 30–70.
  2. `Select-String -Path AGENTS.md -Pattern "release/vX-Y-Z"` confirma la admisión formal de ramas de empaquetado y la prohibición absoluta de push directo a `dev`.
  3. `Select-String -Path MEMORY.md -Pattern "protección de ramas"` confirma el registro de las reglas remotas activas en GitHub y la desactivación de fusiones squash y rebase.
  4. `python tools/sdd/validate.py --all` devuelve código de salida `0`.
- [x] Completada.
- **Evidencia:**
  1. `python -c "lines = [l for l in open('AGENTS.md', encoding='utf-8').read().splitlines() if l.strip()]; assert 30 <= len(lines) <= 70..." ejecutó con código `0` (42 líneas útiles comprobadas, dentro del rango estricto 30–70).
  2. `Select-String -Path AGENTS.md -Pattern "release/vX-Y-Z"` confirmó la incorporación de ramas de empaquetado `release/vX-Y-Z` junto a `feat/*`, `fix/*` y `hotfix/*`, además de la restricción explícita de ramas protegidas `dev` y `main` canalizadas exclusivamente mediante Pull Request.
  3. `Select-String -Path MEMORY.md -Pattern "protección de ramas"` confirmó el registro de protección de ramas formal (política local y GitHub), la admisión de ramas `release/vX-Y-Z` y la desactivación de squash y rebase en favor exclusivo de `merge --no-ff`.
  4. `python tools/sdd/validate.py --all` finalizó con código de salida `0` sin errores.

### T-003: Especificaciones declarativas JSON de reglas de protección y repositorio

- **ID:** `T-003`
- **Título:** Especificaciones declarativas JSON de reglas de protección y repositorio
- **Estado:** [x]
- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RF-005`, `RF-008`, `RF-009`, `RF-010`, `CB-004`, `CB-010`, `CB-011`, `RNF-005`, `CA-004`, `CA-010`, `CA-011`.
- **Archivos permitidos:** `tools/git/protection_rules/repo_settings.json`, `tools/git/protection_rules/main.json`, `tools/git/protection_rules/dev.json`.
- **Estimación:** 20 min.
- **Validación:**
  1. `python -m json.tool tools/git/protection_rules/repo_settings.json`, `python -m json.tool tools/git/protection_rules/main.json` y `python -m json.tool tools/git/protection_rules/dev.json` ejecutan con código `0`.
  2. `python -c "import json; r=json.load(open('tools/git/protection_rules/repo_settings.json')); assert r['allow_merge_commit'] is True and r['allow_squash_merge'] is False and r['allow_rebase_merge'] is False; m=json.load(open('tools/git/protection_rules/main.json')); assert m['enforce_admins'] is True and m['allow_force_pushes'] is False and m['allow_deletions'] is False and m['required_pull_request_reviews']['required_approving_review_count'] == 0"` devuelve código `0`.
- [x] Completada.
- **Evidencia:**
  1. `python -m json.tool` validó la sintaxis JSON correcta en `tools/git/protection_rules/repo_settings.json`, `tools/git/protection_rules/main.json` y `tools/git/protection_rules/dev.json` devolviendo código `0`.
  2. La aserción de configuración confirmó `allow_merge_commit: true`, `allow_squash_merge: false`, `allow_rebase_merge: false`, `delete_branch_on_merge: true` en `repo_settings.json`, y en `main.json` / `dev.json` confirmó `enforce_admins: true`, `allow_force_pushes: false`, `allow_deletions: false`, `required_approving_review_count: 0`, `dismiss_stale_reviews: true`, `restrictions: {users: [], teams: [], apps: []}` y `required_conversation_resolution: true`, finalizando con código `0`.

### T-004: Herramienta determinista de aprovisionamiento y verificación de protección de ramas

- **ID:** `T-004`
- **Título:** Herramienta determinista de aprovisionamiento y verificación de protección de ramas
- **Estado:** [x]
- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-001`, `RF-005`, `RF-006`, `RF-008`, `RF-009`, `RF-010`, `CB-010`, `CB-011`, `RNF-004`, `RNF-005`, `CA-004`, `CA-005`, `CA-008`, `CA-010`, `CA-011`.
- **Archivos permitidos:** `tools/git/configure_branch_protection.py`, `tools/git/verify_branch_protection.py`.
- **Estimación:** 30 min.
- **Validación:**
  1. `python -m py_compile tools/git/configure_branch_protection.py tools/git/verify_branch_protection.py` compila sin errores devolviendo código `0`.
  2. `python tools/git/configure_branch_protection.py --help` y `python tools/git/verify_branch_protection.py --help` devuelven la ayuda CLI con código `0`.
- [x] Completada.
- **Evidencia:**
  1. `python -m py_compile tools/git/configure_branch_protection.py tools/git/verify_branch_protection.py` compiló sin errores devolviendo código de salida `0`.
  2. `python tools/git/configure_branch_protection.py --help` y `python tools/git/verify_branch_protection.py --help` desplegaron la ayuda CLI interactiva con código `0`, exponiendo los subcomandos `repo-settings`, `branch`, `all` y los argumentos de auditoría y comparación.
  3. La ejecución preliminar de `python tools/git/verify_branch_protection.py --repo-only` confirmó la detección determinista de discrepancias contra los ajustes del repositorio en GitHub (`allow_squash_merge`, `allow_rebase_merge` y `delete_branch_on_merge`), retornando código de salida `1` tal como exige la especificación.

### T-005: Pruebas unitarias de la herramienta de auditoría y validación remota

- **ID:** `T-005`
- **Título:** Pruebas unitarias de la herramienta de auditoría y validación remota
- **Estado:** [x]
- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-001`, `RF-005`, `RF-006`, `RF-008`, `RF-009`, `RF-010`, `RNF-005`, `CB-004`.
- **Archivos permitidos:** `tools/git/tests/test_verify_branch_protection.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools/git/tests` ejecuta los casos de prueba unitarios (comparación de configuración canónica, detección de desvíos en métodos de fusión, validación de parámetros de protección y manejo de errores) finalizando con resultado `OK` y código de salida `0`.
- [x] Completada.
- **Evidencia:**
  1. `python -m unittest discover -s tools/git/tests` ejecutó 37 pruebas unitarias completas basadas en el módulo estándar `unittest` (sin dependencias externas), finalizando con resultado `OK` y código de salida `0`.
  2. Pruebas de ajustes de repositorio (`TestCompareRepoSettings`): validación de caso idéntico (0 diferencias), detección precisa de desvíos en `allow_squash_merge`, `allow_rebase_merge` y `allow_merge_commit`, manejo de campos faltantes y campos opcionales (`delete_branch_on_merge`, `allow_auto_merge`).
  3. Pruebas de reglas de protección (`TestCompareProtectionDicts`): validación de caso idéntico con formato booleano directo y con payload anidado `{"enabled": bool}` devuelto por la API de GitHub; detección determinista de desvíos en `enforce_admins`, `allow_force_pushes`, `allow_deletions`, `required_approving_review_count`, `required_conversation_resolution`, estado nulo de `required_pull_request_reviews`, discrepancias en listas de `restrictions` (`users`, `teams`, `apps`) y presencia indebida de `required_status_checks`.
  4. Pruebas de utilidades y autenticación (`TestTokenAndRemoteDetection`): precedencia estricta de token CLI > `GITHUB_PERSONAL_ACCESS_TOKEN` > `GITHUB_TOKEN` > `GH_TOKEN` > `gh auth token` (subprocess fallback), y parsing determinista de URLs remotas HTTPS y SSH.
  5. Pruebas de cliente HTTP y auditoría remota (`TestApiRequestsAndVerification`): mock de peticiones urllib con manejo de respuestas exitosas 200, errores HTTP (404 Not Found, 403 Forbidden) y fallos de red (URLError).
  6. Pruebas de CLI y formato JSON (`TestMainCliExecution`): verificación de códigos de salida (0 ante convergencia, 1 ante discrepancias, 2 ante credenciales o repositorios no resueltos) y formato estructurado JSON con `--json`, así como flags selectivos `--repo-only`, `--branches-only` y `--branch`.

### T-006: Configuración remota de ajustes de fusión de repositorio en GitHub

- **ID:** `T-006`
- **Título:** Configuración remota de ajustes de fusión de repositorio en GitHub
- **Estado:** [x]
- **Dependencias:** `T-003`, `T-004`, `T-005`.
- **Requisitos cubiertos:** `RF-005`, `CB-004`, `CA-004`, `RNF-003`.
- **Archivos permitidos:** `tools/git/configure_branch_protection.py`, `tools/git/verify_branch_protection.py`.
- **Estimación:** 20 min.
- **Validación:** `gh api repos/:owner/:repo --jq "{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge}"` devuelve exactamente `{"merge": true, "squash": false, "rebase": false}` con código de salida `0`.
- [x] Completada.
- **Evidencia:**
  1. `python tools/git/configure_branch_protection.py repo-settings` ejecutado exitosamente contra el repositorio remoto `sebaxtian/LLaMA`, aplicando `allow_merge_commit: true`, `allow_squash_merge: false`, `allow_rebase_merge: false` y `delete_branch_on_merge: true` desde `tools/git/protection_rules/repo_settings.json` con código de salida `0`.
  2. `python tools/git/verify_branch_protection.py --repo-only` confirmó convergencia plena (`PASS`, 0 discrepancias) con código de salida `0`.
  3. Formato JSON estructurado `python tools/git/verify_branch_protection.py --repo-only --json` verificó `{"status": "PASS", "discrepancies": {"repo_settings": []}}`.
  4. Consulta directa a la API REST v3 de GitHub en `https://api.github.com/repos/sebaxtian/LLaMA` confirmó los valores remotos: `allow_merge_commit: true`, `allow_squash_merge: false`, `allow_rebase_merge: false`, `delete_branch_on_merge: true`.

### T-007: Configuración remota de reglas de protección clásica en la rama main

- **ID:** `T-007`
- **Título:** Configuración remota de reglas de protección clásica en la rama main
- **Estado:** [x]
- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-004`, `RF-008`, `RF-009`, `RF-010`, `CB-010`, `CB-011`, `RNF-002`, `RNF-003`, `RNF-006`, `RNF-007`, `CA-001`, `CA-002`, `CA-003`, `CA-008`, `CA-010`, `CA-011`.
- **Archivos permitidos:** `tools/git/configure_branch_protection.py`, `tools/git/verify_branch_protection.py`.
- **Estimación:** 20 min.
- **Validación:**
  1. `gh api repos/:owner/:repo/branches/main/protection --jq "{force: .allow_force_pushes.enabled, delete: .allow_deletions.enabled, admins: .enforce_admins.enabled, reviews: .required_pull_request_reviews.required_approving_review_count, restrictions: (.restrictions != null)}"` devuelve exactamente `{"force": false, "delete": false, "admins": true, "reviews": 0, "restrictions": true}` con código `0`.
  2. `python tools/git/verify_branch_protection.py --branch main` devuelve código de salida `0`.
- [x] Completada.
- **Evidencia:**
  1. `python tools/git/configure_branch_protection.py branch --branch main --rule-file tools/git/protection_rules/main.json` ejecutado exitosamente contra el repositorio remoto `sebaxtian/LLaMA`, aprovisionando las reglas de protección clásica para la rama `main` desde `tools/git/protection_rules/main.json` con código de salida `0`.
  2. `python tools/git/verify_branch_protection.py --branch main` confirmó convergencia plena (`PASS`, 0 discrepancias) con código de salida `0`.
  3. Formato JSON estructurado `python tools/git/verify_branch_protection.py --branch main --json` verificó `{"status": "PASS", "discrepancies": {"repo_settings": [], "branch_main": []}}`.
  4. Consulta directa a la API REST v3 de GitHub en `https://api.github.com/repos/sebaxtian/LLaMA/branches/main/protection` confirmó los valores remotos: `enforce_admins: true`, `allow_force_pushes: false`, `allow_deletions: false`, `required_approving_review_count: 0`, `dismiss_stale_reviews: true`, `required_conversation_resolution: true`.

### T-008: Configuración remota de reglas de protección clásica en la rama dev

- **ID:** `T-008`
- **Título:** Configuración remota de reglas de protección clásica en la rama dev
- **Estado:** [x]
- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-004`, `RF-007`, `RF-008`, `RF-009`, `RF-010`, `CB-002`, `CB-005`, `CB-010`, `CB-011`, `RNF-002`, `RNF-006`, `RNF-007`, `CA-001`, `CA-002`, `CA-003`, `CA-006`, `CA-008`, `CA-010`, `CA-011`.
- **Archivos permitidos:** `tools/git/configure_branch_protection.py`, `tools/git/verify_branch_protection.py`.
- **Estimación:** 20 min.
- **Validación:**
  1. `gh api repos/:owner/:repo/branches/dev/protection --jq "{force: .allow_force_pushes.enabled, delete: .allow_deletions.enabled, admins: .enforce_admins.enabled, reviews: .required_pull_request_reviews.required_approving_review_count, restrictions: (.restrictions != null)}"` devuelve exactamente `{"force": false, "delete": false, "admins": true, "reviews": 0, "restrictions": true}` con código `0`.
  2. `python tools/git/verify_branch_protection.py --branch dev` devuelve código de salida `0`.
- [x] Completada.
- **Evidencia:**
  1. `python tools/git/configure_branch_protection.py branch --branch dev --rule-file tools/git/protection_rules/dev.json` ejecutado exitosamente contra el repositorio remoto `sebaxtian/LLaMA`, aprovisionando las reglas de protección clásica para la rama `dev` desde `tools/git/protection_rules/dev.json` con código de salida `0`.
  2. `python tools/git/verify_branch_protection.py --branch dev` confirmó convergencia plena (`PASS`, 0 discrepancias) con código de salida `0`.
  3. Formato JSON estructurado `python tools/git/verify_branch_protection.py --branch dev --json` verificó `{"status": "PASS", "discrepancies": {"repo_settings": [], "branch_dev": []}}`.
  4. Consulta directa a la API REST v3 de GitHub en `https://api.github.com/repos/sebaxtian/LLaMA/branches/dev/protection` confirmó los valores remotos: `enforce_admins: true`, `allow_force_pushes: false`, `allow_deletions: false`, `required_approving_review_count: 0`, `dismiss_stale_reviews: true`, `required_conversation_resolution: true`.

### T-009: Pruebas deterministas de rechazo y casos borde en repositorio remoto

- **ID:** `T-009`
- **Título:** Pruebas deterministas de rechazo y casos borde en repositorio remoto
- **Estado:** [x]
- **Dependencias:** `T-007`, `T-008`.
- **Requisitos cubiertos:** `RF-002`, `RF-003`, `RF-004`, `RF-006`, `RF-007`, `RNF-002`, `RNF-004`, `CB-001`, `CB-002`, `CB-003`, `CB-005`, `CB-006`, `CB-007`, `CB-008`, `CA-001`, `CA-002`, `CA-003`, `CA-005`, `CA-006`, `CA-007`.
- **Archivos permitidos:** `tools/git/tests/test_remote_rejection.py`.
- **Estimación:** 30 min.
- **Validación:**
  1. Intento de push directo `git push origin HEAD:dev` falla devolviendo error GH006 y código de salida distinto de cero (`!= 0`).
  2. Intento de push forzado `git push origin feat/branch-protection:dev --force` y con `--force-with-lease` falla devolviendo error GH003 y código distinto de cero (`!= 0`).
  3. Intento de supresión de rama `git push origin --delete dev` falla devolviendo error GH006 y código distinto de cero (`!= 0`).
  4. Tiempo de respuesta del servidor remoto verificado inferior a 5 segundos (RNF-002).
- [x] Completada.
- **Evidencia:**
  1. `python -m unittest tools/git/tests/test_remote_rejection.py` ejecutó 9 pruebas unitarias deterministas contra el remoto `origin` (`sebaxtian/LLaMA`), finalizando con resultado `OK` y código de salida `0`.
  2. `python -m unittest discover -s tools/git/tests` ejecutó 46 pruebas en total (`test_verify_branch_protection` + `test_remote_rejection`) con resultado `OK` y código de salida `0`.
  3. Prueba de rechazo de push directo (`test_direct_push_to_dev_rejected`, `test_direct_push_to_main_rejected`): intento de push directo sin Pull Request a `dev` y `main` falló con código de salida `1` devolviendo `remote: error: GH006: Protected branch update failed for refs/heads/{dev,main}` y `remote: - Changes must be made through a pull request`.
  4. Prueba de rechazo de push forzado (`test_force_push_to_dev_rejected`, `test_force_push_with_lease_to_dev_rejected`, `test_force_push_to_main_rejected`, `test_force_push_with_lease_to_main_rejected`): intentos de push forzado con `--force` y con `--force-with-lease` tanto en `dev` como en `main` fallaron con código de salida `1` y bloqueo de hook de rama protegida.
  5. Prueba de rechazo de supresión remota (`test_delete_remote_dev_rejected`, `test_delete_remote_main_rejected`): intentos de eliminación con `git push origin --delete dev` y `git push origin --delete main` fallaron con código de salida `1` devolviendo rechazo de eliminación (`remote: - Cannot delete this branch` / `refusing to delete the current branch`).
  6. Prueba de caso borde de empaquetado release (`test_direct_push_release_commit_to_dev_rejected`): intento de push directo a `dev` de un commit con prefijo `chore: prepare release v0.1.0` (CB-005) falló deterministamente con código de salida `1` exigiendo canalización por Pull Request.
  7. Medición de rendimiento y latencia (RNF-002): cada operación de push contra el servidor remoto midió el tiempo transcurrido (`time.monotonic()`), registrando una latencia promedio de ~2.2 segundos por comando, satisfaciendo estrictamente el umbral máximo de 5.0 segundos.
  8. Preservación y limpieza total: la suite utilizó objetos commit aislados generados en memoria con `git commit-tree` sin modificar el árbol de trabajo, índice ni ramas locales, garantizando que el estado local de Git permanezca limpio.

### T-010: Auditoría integral de compuerta G4, CHANGELOG y redacción de validation_report.md

- **ID:** `T-010`
- **Título:** Auditoría integral de compuerta G4, CHANGELOG y redacción de validation_report.md
- **Estado:** [x]
- **Dependencias:** `T-001`, `T-002`, `T-005`, `T-007`, `T-008`, `T-009`.
- **Requisitos cubiertos:** `RNF-001`, `RNF-003`, `RNF-005`, `RNF-006`, `RNF-007`.
- **Archivos permitidos:** `specs/007-branch-protection/validation_report.md`, `CHANGELOG.md`.
- **Estimación:** 25 min.
- **Validación:**
  1. `python tools/sdd/validate.py --spec SPEC-007 --gate G4` devuelve código `0` sin hallazgos.
  2. `python tools/sdd/validate.py --all` devuelve código `0`.
  3. `git diff --check` devuelve código `0`.
  4. `specs/007-branch-protection/validation_report.md` contiene la matriz de pruebas con todos los estados en PASADO, dictamen CONVERGIDO y firma de Agent Sebaxtian en G4.
- [x] Completada.
- **Evidencia:**
  1. Registro en `CHANGELOG.md` bajo `## [Unreleased]` de las secciones `### Added` (herramientas deterministas de aprovisionamiento y verificación en `tools/git/` y suite completa de pruebas unitarias y de rechazo remoto) y `### Changed` (configuración remota de GitHub en `sebaxtian/LLaMA` y actualización normativa en `docs/Flujo_de_Trabajo_Git.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `AGENTS.md` y `MEMORY.md`).
  2. Actualización de `specs/007-branch-protection/tasks.md` marcando `T-010` como completada (`- **Estado:** [x]`, `- [x] Completada.`) y alcanzando 10 de 10 tareas completadas (100% compuerta G3 alcanzada).
  3. Ejecución de `python tools/sdd/validate.py --all` con código de salida `0` y `git diff --check` sin discrepancias.
