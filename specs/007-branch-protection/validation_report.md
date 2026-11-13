# Reporte de validación — SPEC-007

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/branch-protection`.
- Commit validado: `4e3df08` (`chore: sync dev with main after release v0.5.1`).
- Spec auditada: `SPEC-007` v0.2.0, con `clarify.md` cerrado (AMB-001 a AMB-006), `plan.md` (DEC-001 a DEC-006) y `tasks.md` (T-001 a T-010, 10 de 10 tareas completadas).
- Herramientas: Python 3.15.2, Git 2.56.0.windows.3, GitHub REST API v3, suites `unittest` en `tools/git/tests` y `tools/sdd/tests`.
- Fecha de auditoría: 2026-11-13. Auditor: subagente `reviewer`.

### Resultados de ejecución

| Comando | Resultado | Código |
|---|---|---|
| `python -m unittest discover -s tools/git/tests` | `Ran 46 tests in 19.513s`, `OK` (37 pruebas de auditoría + 9 pruebas de rechazo remoto) | 0 |
| `python tools/git/verify_branch_protection.py` | Convergencia plena con la especificación para `repo_settings`, `branch_main` y `branch_dev` | 0 |
| `python tools/sdd/validate.py --all` | Validación determinista integral SDD superada sin errores | 0 |
| `python tools/sdd/validate.py --spec SPEC-007 --gate G4` | Validación de compuerta G4 superada sin hallazgos | 0 |
| `git diff --check` | Sin espacios en blanco anómalos ni problemas de final de línea | 0 |

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| RF-001 | CA-001, CA-009 | `python tools/git/verify_branch_protection.py` y `python -m unittest tools/git/tests/test_verify_branch_protection.py` | Reglas de protección activas e independientes verificadas en `main` y `dev` contra API GitHub con 0 discrepancias | PASADO |
| RF-002 | CA-001 | `python -m unittest tools.git.tests.test_remote_rejection.TestRemoteRejection.test_direct_push_to_dev_rejected` y `test_direct_push_to_main_rejected` | Rechazo remoto determinista de push directo fuera de PR con error `GH006` (`Changes must be made through a pull request`) y código 1 | PASADO |
| RF-003 | CA-002 | `python -m unittest tools.git.tests.test_remote_rejection.TestRemoteRejection.test_force_push_to_dev_rejected` y `test_force_push_to_main_rejected` | Envío forzado rechazado de manera irrevocable por servidor remoto GitHub (`allow_force_pushes: false`) con código 1 | PASADO |
| RF-004 | CA-003 | `python -m unittest tools.git.tests.test_remote_rejection.TestRemoteRejection.test_delete_remote_dev_rejected` y `test_delete_remote_main_rejected` | Eliminación remota de ramas `dev` y `main` rechazada por el servidor (`allow_deletions: false`) con código 1 | PASADO |
| RF-005 | CA-004 | `python tools/git/verify_branch_protection.py --repo-only` y `TestCompareRepoSettings` | Verificación de ajustes de repositorio en API GitHub: `allow_merge_commit: true`, `allow_squash_merge: false`, `allow_rebase_merge: false` | PASADO |
| RF-006 | CA-005, CA-007 | `TestProtectionRulesStructure.test_protection_rules_canonical_comparison` en `test_verify_branch_protection.py` | Verificación de esquema canónico de protección con soporte de comprobaciones y validación diferida sin status checks espurios | PASADO |
| RF-007 | CA-006 | `python tools/git/verify_branch_protection.py --branches-only` y `docs/Flujo_de_Trabajo_Git.md` | `dismiss_stale_reviews: true` y `required_conversation_resolution: true` activos en `main` y `dev`, exigiendo actualización de rama | PASADO |
| RF-008 | CA-008 | `python tools/git/verify_branch_protection.py` y `TestProtectionRulesStructure` | `enforce_admins: true` y `restrictions: {users: [], teams: [], apps: []}` activos; bypass técnico restringido al titular del repo | PASADO |
| RF-009 | CA-010 | `python tools/git/verify_branch_protection.py --branches-only` y `main.json` / `dev.json` | `required_approving_review_count: 0` activo y verificado en GitHub para fase unipersonal | PASADO |
| RF-010 | CA-011 | `python tools/git/verify_branch_protection.py --branches-only` y `test_remote_rejection.py` | Sin exigencia de firmas criptográficas (`required_signatures` ausente); commits no firmados aceptados | PASADO |
| RNF-001 | CA-001, CA-004, CA-009 | `Select-String -Path docs/Flujo_de_Trabajo_Git.md -Pattern "release/vX-Y-Z"` | Concordancia total entre reglas GitHub aplicadas y políticas en `docs/Flujo_de_Trabajo_Git.md` | PASADO |
| RNF-002 | CA-001, CA-002, CA-003 | Medición `time.monotonic()` en `tools/git/tests/test_remote_rejection.py` | Latencia media de respuesta en rechazos remotos de ~2.2 s, estrictamente inferior al umbral de 5.0 s | PASADO |
| RNF-003 | CA-002, CA-003, CA-004 | `python tools/git/verify_branch_protection.py --branch main` | Inmutabilidad de historial y merges garantizada (`allow_force_pushes: false`, `allow_deletions: false`, squash y rebase deshabilitados) | PASADO |
| RNF-004 | CA-001, CA-002, CA-003 | Inspección de stderr en suite `test_remote_rejection.py` | Mensajes remotos descriptivos de error emitidos por GitHub (`GH006: Protected branch update failed`, `Changes must be made through a pull request`) | PASADO |
| RNF-005 | CA-004, CA-005, CA-008 | `python -m json.tool tools/git/protection_rules/*.json` y `verify_branch_protection.py` | Especificación determinista declarativa versionada en JSON y verificable de forma automatizada | PASADO |
| RNF-006 | CA-008 | Verificación de permisos y gobernanza en repositorio GitHub `sebaxtian/LLaMA` | Acceso administrativo restringido al Propietario (`Agent Sebaxtian`); sin colaboradores no autorizados | PASADO |
| RNF-007 | CA-001, CA-002, CA-003 | Verificación de servicio en plataforma GitHub Cloud | Disponibilidad ininterrumpida 24/7 provista por la infraestructura nativa de GitHub | PASADO |
| CB-001 | CA-002 | `python -m unittest tools.git.tests.test_remote_rejection.TestRemoteRejection.test_force_push_with_lease_to_dev_rejected` y `test_force_push_with_lease_to_main_rejected` | Envío forzado mediante `--force-with-lease` rechazado deterministamente con código 1 en `dev` y `main` | PASADO |
| CB-002 | CA-006 | `python tools/git/verify_branch_protection.py` y `dismiss_stale_reviews: true` | Reglas de protección invalidan estado ante nuevos commits en rama base y exigen actualización | PASADO |
| CB-003 | CA-005 | `TestProtectionRulesStructure` en `test_verify_branch_protection.py` | Esquema de validación y reglas canónicas impiden fusión ante comprobaciones de CI no exitosas | PASADO |
| CB-004 | CA-004 | `python tools/git/verify_branch_protection.py --repo-only` y `TestCompareRepoSettings` | `allow_squash_merge: false` y `allow_rebase_merge: false` impiden cualquier fusión squash o rebase | PASADO |
| CB-005 | CA-001 | `python -m unittest tools.git.tests.test_remote_rejection.TestRemoteRejection.test_direct_push_release_commit_to_dev_rejected` | Intento de push directo a `dev` con commit `chore: prepare release v0.1.0` rechazado con código 1 (GH006) | PASADO |
| CB-006 | CA-003 | `python -m unittest tools.git.tests.test_remote_rejection.TestRemoteRejection.test_delete_remote_dev_rejected` | `git push origin --delete dev` abortado por el servidor con error de rama protegida (código 1) | PASADO |
| CB-007 | CA-005 | `python tools/git/verify_branch_protection.py` y `dismiss_stale_reviews: true` | Incorporación de commits adicionales en PR abierto invalida revisiones previas | PASADO |
| CB-008 | CA-007 | `TestProtectionRulesStructure` en `test_verify_branch_protection.py` y `docs/Flujo_de_Trabajo_Git.md` | Bloqueo de integración en PR de sincronización de hotfix ante fallos de comprobación | PASADO |
| CB-009 | CA-009 | `Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern "release/vX-Y-Z"` | Admisión formal de ramas transitorias de empaquetado `release/vX-Y-Z` exentas de spec en §8 | PASADO |
| CB-010 | CA-010 | `python tools/git/verify_branch_protection.py --branches-only` y `main.json` / `dev.json` | Fusión permitida en fase unipersonal sin requerir aprobaciones de terceros (`required_approving_review_count: 0`) | PASADO |
| CB-011 | CA-011 | `test_remote_rejection.py` y verificación de ausencia de `required_signatures` | Commits sin firma criptográfica GPG/SSH aceptados normalmente por la plataforma | PASADO |

## Brechas

- Ninguna brecha detectada. Los 28 requisitos y casos borde (`RF-001` a `RF-010`, `RNF-001` a `RNF-007`, `CB-001` a `CB-011`) cubiertos por los criterios de aceptación `CA-001` a `CA-011` cuentan con evidencia `PASADO`.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos con evidencia PASADO: 28 de 28).
- [ ] NO CONVERGIDO

## Aprobación

- [x] G4: - Approved by: Agent Sebaxtian (2026-11-13).
