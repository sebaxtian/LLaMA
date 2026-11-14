# Reporte de validación — SPEC-011

*Auditoría independiente de la Etapa 7 sobre el contrato de `SPEC-011`, reauditada sobre el commit de corte `ca9e891`. Este documento no registra compuerta alguna: la aprobación de G4 corresponde al propietario y se inscribe en la sección de aprobaciones de `spec.md` mediante un commit firmado.*

## Entorno

- Sistema operativo: Windows 11 (`win32`), shell PowerShell.
- Rama: `feat/practica-operativa-sdd`.
- Commit auditado: `ca9e891376e38a39f570359109dfd6d100ce5d36` (`fix(sdd): resolver precedencia por ultima entrada coincidente`); auditoría anterior sobre `9da25ed`; implementación en `ae1dd5e`; G1 en `5b0d7f1`.
- Árbol de trabajo antes de este reporte: `git status --short --untracked-files=all` sin salida; `git diff --check` sin salida. Después de escribirlo, el único archivo no rastreado es este reporte.
- Herramientas: Git con los subcomandos `status`, `log`, `diff`, `show`, `rev-parse`, `branch`, `merge-base`, `ls-remote` y `verify-commit`; `python tools\sdd\validate.py`; `python -m unittest`; lectura directa de los artefactos. Las versiones de Git y del intérprete no se capturaron porque la allowlist de `reviewer.md` no incluye `git --version` ni `python --version`.
- Artefactos leídos: `specs/011-practica-operativa-sdd/{spec.md, clarify.md, plan.md, tasks.md}`, los seis archivos de `.opencode/agents/`, `opencode.jsonc`, `.github/workflows/sdd.yml`, `tools/sdd/tests/test_agent_permissions.py`, `tools/sdd/tests/test_validate.py`, `AGENTS.md`, `MEMORY.md`, `specs/INDEX.md`, `CHANGELOG.md`, `docs/sdd/firmantes_autorizados`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `docs/sdd/auditoria_cumplimiento_sdd.md` (B3).
- Suite reejecutada: `python -m unittest discover -s tools\sdd\tests -q` devuelve `Ran 111 tests in 0.820s` y `OK` en la primera ejecución, y `Ran 111 tests in 0.714s` y `OK` en la repetición posterior al escribir este reporte, código de salida 0: 94 pruebas de `test_validate.py` y 17 de `test_agent_permissions.py`.
- Validación agregada: `python tools\sdd\validate.py --all` devuelve código de salida 0 con doce advertencias de legado y la advertencia de este reporte aún ausente, sin hallazgo de error.
- Comprobaciones ejecutadas en esta sesión: `git merge-base --is-ancestor main dev` con código 0; `git ls-remote --heads origin release/v0-6-0` sin salida; `git ls-remote --heads origin feat/gemma-4-26b-a4b-it-qat-gguf` sin salida; `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf` con una referencia; `git verify-commit 5b0d7f1` con firma válida; `git status --short --untracked-files=all -- docs/sdd/` sin salida.
- Concesión de escritura verificada en la práctica: la creación de este reporte se resolvió en `allow`, de modo que el permiso efectivo del rol `reviewer` sobre `specs/011-practica-operativa-sdd/validation_report.md` coincide con la concesión declarada.
- El flujo de integración continua no registra una ejecución remota en este corte: la rama de trabajo no figura en las referencias remotas. La verificación se apoya en su definición y en la ejecución local de los dos pasos con código de salida 0.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | Glob y lectura de `.opencode/agents/*.md` (seis resultados) | Cada rol declara `description`, `mode` y `permissions` con las acciones `edit`, `read`, `shell` y `subagent`; allowlist literal de shell y política de subagentes; `sdd` en `primary`, `planner` y `coder` en `all`, `reviewer`, `documenter` y `auditor` en `subagent` | PASADO |
| `RF-002` | `CA-002` | Lectura de las seis matrices; escritura real del reporte; `test_denegacion_prevalece_en_igual_especificidad` (:790) y `test_cero_conflictos_de_igual_especificidad` (:802) | Las cuatro reglas figuran en los seis cuerpos; el permiso efectivo de `specs/011-practica-operativa-sdd/validation_report.md` resultó `allow` frente a la denegación general `specs/**`, de modo que la ruta más específica prevaleció; las matrices no declaran solapamientos de igual especificidad y ese caso queda resuelto en `deny` por el procedimiento y su prueba | PASADO |
| `RF-003` | `CA-003`, `CA-004` | `auditor.md:14-52` | `edit` deniega `docs/**`, `specs/**`, `src/**`, `tests/**`, `tools/**`, `.opencode/**`, `.github/**`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `CHANGELOG.md` y `.env`, y concede solo `docs/sdd/auditoria_*.md`; `shell *` denegado con seis comandos `git` de lectura, el validador, la suite y tres comprobaciones de integración; `subagent *` denegado | PASADO |
| `RF-004` | `CA-005` | `reviewer.md:14-49`; creación de este reporte | `edit` deniega `specs/**`, `src/**`, `tests/**`, `tools/**`, `docs/**`, `.opencode/**`, `.github/**`, `opencode.jsonc` y `.env`, y concede solo `specs/*/validation_report.md`; la escritura del reporte se ejerció y `subagent *` permanece denegado | PASADO |
| `RF-005` | `CA-006` | `coder.md:14-49`; `test_escritura_del_coder` (:820) | `edit` deniega `docs/**`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `.opencode/**`, `.github/**`, `.env` y `specs/**`, y concede `src/**`, `tests/**`, `tools/**` y `specs/*/tasks.md`, con el cierre de tareas como única escritura fuera de las tres raíces | PASADO |
| `RF-006` | `CA-007`, `CA-015` | `sdd.yml:3-23`; ejecución local de los dos pasos | `on.pull_request.branches: [dev, main]`; pasos «Validación agregada del corpus» (`python tools\sdd\validate.py --all`, salida 0) y «Suite del mecanismo de control» (`python -m unittest discover -s tools\sdd\tests -q`, 111 pruebas `OK`) declarados por separado y sin `continue-on-error`, de modo que el fallo de cualquiera cierra el trabajo | PASADO |
| `RF-007` | `CA-008` | `sdd.yml` completo (23 líneas); `test_flujo_sin_efectos_remotos` (:1002) | Sin disparador `push`, sin `tags`, sin `secrets`, sin `git push`, sin `deploy` y sin `continue-on-error`; `permissions: contents: read` | PASADO |
| `RF-008` | `CA-009`, `CA-010` | Sección «Cierre de la práctica Git» de este reporte | `AUD-081`, `AUD-082`, `AUD-083` y `AUD-084` quedan cerrados con la salida literal de cada comando | PASADO |
| `RF-009` | `CA-011` | `MEMORY.md:13` frente a `specs/INDEX.md:7-17` | La línea declara `SPEC-001` a `SPEC-007` publicadas, `SPEC-008`, `SPEC-009` y `SPEC-010` validadas y `SPEC-011` en curso; coincide con el registro y con el estado `implemented` de esta spec, de modo que `AUD-091` se acredita | PASADO |
| `RF-010` | `CA-012` | `test_agent_permissions.py`: `leer_permisos` (:298), `especificidad` (:302), `resolver` (:336); suite en verde | La resolución devuelve `allow` o `deny` por rol y ruta y las 17 pruebas contrastan las rutas concedidas y las denegadas con un caso negativo por comprobación; `Ran 111 tests` con `OK` | PASADO |
| `RF-011` | `CA-013` | `opencode.jsonc:41-84` | Cuatro reglas en la cabecera; siete entradas de permiso; `ask` solo en `git push *` y `git tag *`; ninguna concesión global de escritura que amplíe una denegación de rol | PASADO |
| `RF-012` | `CA-016` | `AGENTS.md:45`; `validate.py:1200-1207`; sin cambio en `ca9e891` | 67 líneas útiles dentro del límite 30-70 y sin hallazgo del validador; la línea del mapa enumera los seis roles; ninguna regla de la base alterada | PASADO |
| `RF-013` | `CA-017` | `git diff 9da25ed..ca9e891 -- MEMORY.md` | La línea 13 pasa al estado real del registro y la línea 39 enumera los seis agentes y la integración continua; el hecho operativo obsoleto desaparece | PASADO |
| `RNF-001` | `CA-007` | `sdd.yml:13` | `timeout-minutes: 5` en el trabajo `verify`: el flujo no puede exceder 300 s | PASADO |
| `RNF-002` | `CA-008` | `sdd.yml` completo | Sin `secrets`, sin credenciales literales y sin servicios externos en la definición | PASADO |
| `RNF-003` | `CA-012` | `test_prueba_no_destructiva` (:1062-1092); suite en 0.820 s y 0.714 s | Compara huellas `sha256` antes y después de la lectura, exige menos de 60 s y prohíbe la apertura en modo de escritura dentro del módulo; la suite completa queda muy por debajo del umbral | PASADO |
| `RNF-004` | `CA-002` | Inspección de las seis matrices; `test_cero_conflictos_de_igual_especificidad` (:802) | Cero rutas con concesión y denegación de igual especificidad; los solapamientos declarados son de especificidad distinta, como `specs/**` deny frente a `specs/*/validation_report.md` allow en `reviewer` y `docs/**` deny frente a `docs/sdd/auditoria_*.md` allow en `auditor` | PASADO |
| `RNF-005` | `CA-004` | Glob de `.opencode/agents/` | Seis archivos y una única declaración de `auditor` en `auditor.md`; ningún otro rol repite la declaración | PASADO |
| `RNF-006` | `CA-013` | `opencode.jsonc:48-84` y `:86-99` | El bloque `permissions` no contiene credenciales; el encabezado MCP usa `Bearer {env:GITHUB_PERSONAL_ACCESS_TOKEN}` y conserva la referencia al entorno | PASADO |
| `RNF-007` | `CA-007` | `sdd.yml:12,16-18` | `runs-on: windows-latest` y `python-version: '3.12'`; sin servicios externos | PASADO |
| `RNF-008` | `CA-007` | `sdd.yml:21-23`; `Ran 111 tests in 0.714s` | El paso de la suite declara `timeout-minutes: 1` y la ejecución local completa en menos de un segundo | PASADO |
| `CB-001` | `CA-002` | `test_denegacion_prevalece_en_igual_especificidad` (:790) y `test_cero_conflictos_de_igual_especificidad` (:802), en verde | Ninguna matriz declara una ruta a la vez con concesión y denegación de igual especificidad; el caso sintético de igual especificidad se resuelve en `deny` y la prueba de conflictos no encuentra solapamiento | PASADO |
| `CB-002` | `CA-002` | Primera entrada de los seis roles; `test_denegacion_por_defecto` (:752) | Una ruta sin declaración carece de concesión y hereda el `deny` de `edit *`; la lectura se concede sobre `**` salvo `.env` | PASADO |
| `CB-003` | `CA-003` | `auditor.md:14-52`; `test_auditor_solo_informes` (:850) | `docs/**` deny con `docs/sdd/auditoria_*.md` allow al final del bloque; `specs/**` y `src/**` denegados para escritura, de modo que la modificación de un requisito o de una ruta de código queda rechazada | PASADO |
| `CB-004` | `CA-006` | `coder.md:35-49,97`; `test_escritura_del_coder` | `specs/**` deny seguido de `specs/*/tasks.md` allow; el cuerpo detiene la tarea cuando el archivo no figura en su campo `Archivos` | PASADO |
| `CB-005` | `CA-005` | `reviewer.md:14-49,86-88`; escritura del reporte | `subagent *` denegado y `edit` denegado sobre rutas de código, configuración y artefactos de la spec salvo el reporte de validación, que se escribió sin exceder el límite | PASADO |
| `CB-006` | `CA-007` | `sdd.yml:19-23` | Dos pasos con nombre propio y cumplimiento en serie; la ausencia de `continue-on-error` hace fallar el trabajo y el registro del flujo identifica el paso que falló | PASADO |
| `CB-007` | `CA-008` | `sdd.yml` completo; `test_flujo_sin_efectos_remotos` (:1002) | No hay instrucción de push, de tag ni de operación remota; el caso negativo del flujo con `git push origin dev` produce el fallo de la prueba | PASADO |
| `CB-008` | `CA-009` | `git merge-base --is-ancestor main dev` | Código de salida 0: `main` está contenido en `dev` y `AUD-081` se acredita | PASADO |
| `CB-009` | `CA-009` | `git ls-remote --heads origin release/v0-6-0` y `git branch --all --list "*release/v0-6-0*"` | Sin salida en ambos: no figura referencia local ni remota del release anterior y `AUD-082` se acredita | PASADO |
| `CB-010` | `CA-010` | `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf` y `git ls-remote --heads origin feat/gemma-4-26b-a4b-it-qat-gguf` | Una referencia local y ninguna remota; la decisión figura en `PROTOCOLO_OPERATIVO.md:388`, `CHANGELOG.md:22` y `plan_cierre_brechas_sdd.md:35` | PASADO |
| `CB-011` | `CA-010` | `git status --short --untracked-files=all -- docs/sdd/` y `git log --oneline -1 --` sobre los seis documentos | Sin entradas para `docs/sdd/`; los seis documentos del hallazgo quedan versionados en `82b383d` | PASADO |
| `CB-012` | `CA-011` | Contraste de cada hecho de `MEMORY.md` con `specs/INDEX.md`, glob de `src/`, `models/gemma/`, `main.bat`, `tools/sdd/validate.bat` y `docs/sdd/plantillas/` | Ningún hecho operativo contradice el estado del repositorio, de modo que `AUD-091` se registra cerrado | PASADO |
| `CB-013` | `CA-012` | `test_prueba_no_destructiva` (:1090-1092) | Sin lectura de los artefactos el contraste se registra como «no verificada» con su motivo; con lectura, como «verificada» | PASADO |
| `CB-014` | `CA-004` | `auditor.md:96`; `test_auditor_no_aprueba` (:864) | El cuerpo rechaza aprobaciones y compuertas; la matriz no concede escritura sobre `specs/*/spec.md` ni sobre `CHANGELOG.md` | PASADO |
| `CB-015` | `CA-003` | `resolver` sobre `docs/sdd/guia_operativa.md`; `test_auditor_solo_informes` (:855) | La ruta ajena al patrón resuelve en `deny`, porque el patrón de informe no la cubre y la denegación de `docs/**` no se ve desplazada | PASADO |
| `CB-016` | `CA-015` | `sdd.yml:3-5` | El flujo solo se dispara con `pull_request` dirigido a `dev` o a `main`; otra rama de destino no activa el trabajo y la verificación queda a cargo de la ejecución local | PASADO |
| `CB-017` | `CA-014` | Solicitudes reales fuera de la allowlist de `reviewer.md` | Una composición con `echo` y la forma `git -c ... verify-commit` devolvieron `Permission denied: shell`; el rol y el comando quedan identificados en el registro de la sesión | PASADO |

## Cierre de la práctica Git

| Hallazgo | Hecho acreditado | Comando literal | Resultado |
|---|---|---|---|
| `AUD-081` | `dev` contiene el commit publicado en `main` | `git merge-base --is-ancestor main dev` | Código de salida 0. CERRADO |
| `AUD-082` | La referencia remota del release anterior no figura en el listado | `git ls-remote --heads origin release/v0-6-0` y `git branch --all --list "*release/v0-6-0*"` | Sin salida en ambos comandos. CERRADO |
| `AUD-083` | La rama Gemma permanece local, no publicada y con decisión registrada | `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf` y `git ls-remote --heads origin feat/gemma-4-26b-a4b-it-qat-gguf` | Una referencia local y ninguna remota; decisión en `PROTOCOLO_OPERATIVO.md:388`, `CHANGELOG.md:22` y `plan_cierre_brechas_sdd.md:35`. CERRADO |
| `AUD-084` | Los seis documentos versionados y sin cambio pendiente | `git status --short --untracked-files=all -- docs/sdd/` y `git log --oneline -1 -- docs/sdd/PROTOCOLO_OPERATIVO.md docs/sdd/README.md docs/sdd/diagrama_flujo_ciclo_vida_sdd.md docs/sdd/guia_maestra_sdd.md docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md docs/sdd/plan_cierre_brechas_sdd.md` | Sin entradas para `docs/sdd/`; los seis documentos en `82b383d`. CERRADO |
| `AUD-091` | `MEMORY.md` sin hechos operativos obsoletos | Contraste de cada hecho con `specs/INDEX.md`, glob de `src/`, `models/gemma/`, `main.bat`, `tools/sdd/validate.bat` y `docs/sdd/plantillas/`; `git diff 9da25ed..ca9e891 -- MEMORY.md` | La línea 13 declara el estado real del registro y el resto de los hechos coincide. CERRADO |

## Brechas

Sin entradas: el conjunto de los 38 requisitos y casos borde queda con evidencia `PASADO`.

## Observaciones no bloqueantes

- La resolución efectiva depende del orden de las entradas: cada matriz declara las denegaciones generales y después las concesiones específicas, de modo que la última entrada coincidente concede. El resultado es correcto en el corte, pero una reordenación futura reabriría `AUD-064`; conviene declarar la regla de orden general a específico en los seis cuerpos.
- El `resolver` de `test_agent_permissions.py:336` decide por especificidad con desempate en `deny` y no reproduce el criterio de orden del cliente; las 17 pruebas no detectarían una inversión del orden. La comprobación empírica de esta auditoría cubre ese hueco en el corte.
- `opencode.jsonc:5` declara `"default_agent": "plan"`, que no corresponde a ninguno de los seis roles de `.opencode/agents/`. Ningún requisito de esta spec lo cubre; se consigna como riesgo de configuración del cliente.
- `auditor.md` deniega la escritura fuera del informe, pero su cuerpo no instruye el registro del hallazgo cuando una solicitud se deniega (`CB-003`, `CB-014`, `CB-015`). La capacidad de registro existe en `docs/sdd/plantillas/informe_auditoria.md`; la omisión es de redacción y no de matriz de permisos.
- La firma de G1 se comprobó con `git verify-commit 5b0d7f1` y con `git show --show-signature --no-patch 5b0d7f1`: `Good "git" signature for sebaxtianrioss@gmail.com with ED25519 key SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc`, clave que figura en `docs/sdd/firmantes_autorizados:4`.
- El alcance del corte `ca9e891` se limita a siete rutas —los seis roles de `.opencode/agents/` y `MEMORY.md`—, sin cambio en `spec.md`, `plan.md`, `tasks.md`, `opencode.jsonc`, `.github/workflows/sdd.yml`, `AGENTS.md`, el validador, la suite ni la base normativa.

## Dictamen

- [x] CONVERGIDO.
- [ ] NO CONVERGIDO.

`38` de `38` requisitos y casos borde con evidencia `PASADO`. Queda pendiente el registro de G4 en la sección de aprobaciones de `spec.md` mediante un commit firmado por el propietario; esta auditoría no lo declara.

## Cierre de integración

Merge: 9df8446
Release:
