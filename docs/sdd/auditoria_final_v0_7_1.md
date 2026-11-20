# Informe de auditoría — conformidad del régimen v2 en el estado publicado posterior al release v0.7.1

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, implementado en `.opencode/agents/auditor.md`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-21 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), specs `SPEC-001` a `SPEC-015`, validador `tools/sdd/validate.py`, suites `tools/sdd/tests` y `tools/git/tests`, matriz de agentes de `.opencode/`, flujo de integración continua, registros Git locales (`.git/logs/HEAD`, `.git/refs/`, `.git/packed-refs`) y registro de cambios.
- **Objeto:** emitir el veredicto de conformidad del régimen en el estado publicado posterior al release `v0.7.1` y determinar si los diez hallazgos de `docs/sdd/auditoria_posterior_v0_7_0.md` quedaron cerrados.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas, no aprueba compuertas, no emite línea de aprobación y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `5ba048dc3da1a4ce5e2fb9516585b5c71a5b2179` (`git rev-parse dev`) |
| Rama | `dev` en `5ba048d`; rama de la sesión `docs/auditoria-final-v0-7-1`, creada desde ese commit (`git branch --list`) |
| Fecha de corte | 2026-11-21 |
| Releases de referencia | `v0.7.0`: objeto de tag `f4a6203`, commit objetivo `5a3af48`. `v0.7.1`: objeto de tag `4d0473b`, commit objetivo `da30c86` (`git rev-parse "vX.Y.Z^{tag}"` y `"vX.Y.Z^{commit}"`) |
| Validador ejecutado | `python tools\sdd\validate.py --all`: punto de corte en el tag anotado `v0.7.1`, sin entradas `[ERROR]` y con advertencias `[WARN]` de la cláusula de legado (`C-07`, `C-13`, `C-14`) sobre `SPEC-001` a `SPEC-009` y sin código de salida distinto de `0`. `python tools\sdd\validate.py --spec SPEC-015 --gate G6`: «OK: sin hallazgos.», sin código de salida distinto de `0` |
| Suites ejecutadas | `python -m unittest discover -s tools\sdd\tests -q`: «Ran 187 tests» y «OK» antes de añadir este informe. `python -m unittest discover -s tools\git\tests -q`: «Ran 48 tests in 20.071s» y «OK» |
| Entorno | Windows 11 (`win32`); shell con la lista blanca del rol: `git status`, `log`, `show`, `diff`, `rev-parse`, `branch`, `merge-base` y `ls-remote`, además del validador y de `unittest`. `git tag`, `git cat-file` y las tuberías quedaron denegados y se sustituyeron por `git rev-parse`, `git show` y la lectura de `.git/` |
| Rol ejecutor | `auditor` |

**Procedimiento.** Cinco pasos. Primero, lectura íntegra de `docs/sdd/auditoria_posterior_v0_7_0.md` y de los diez identificadores que dejó abiertos, con su causa y su destinatario de cierre. Segundo, contraste de cada uno con el artefacto que lo satisface, la norma aplicable y su evidencia por ruta y línea en `5ba048d`. Tercero, reconstrucción del release `v0.7.1` a partir de `.git/logs/HEAD:256-264`, del estatuto de firma de cada commit (`git show --no-patch --format=%G?`) y del diff del commit de empaquetado, contrastada con `docs/Flujo_de_Trabajo_Git.md:256-407`, `docs/sdd/PROTOCOLO_OPERATIVO.md:300-320` y `CHANGELOG.md:13-242`. Cuarto, examen de las once dimensiones. Quinto, ejecución del validador, de la compuerta G6 y de las dos suites, con la salida transcrita.

## 2. Base normativa e inventario

La jerarquía consta de siete rangos y una categoría sin rango, declarada de forma coincidente en `docs/constitution.md:48-59` y `docs/sdd/README.md:15-24`; cada documento declara su rango en su encabezado (`docs/Flujo_de_Trabajo_Git.md:3`; `docs/sdd/plantillas/informe_auditoria.md:3`; `docs/sdd/PROTOCOLO_OPERATIVO.md:3`).

| Documento | Rango | Cita |
|---|---|---|
| `docs/constitution.md` | 1 | `docs/constitution.md:52` |
| `AGENTS.md` | 2 | `docs/constitution.md:53` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | `docs/constitution.md:54` |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | `docs/constitution.md:55`; `docs/Flujo_de_Trabajo_Git.md:3` |
| `docs/sdd/plantillas/*.md` | 5 | `docs/constitution.md:56` |
| `specs/NNN-slug/*.md` | 6 | `docs/constitution.md:57` |
| `src/`, `tools/`, `tests/`, `.opencode/` | 7 | `docs/constitution.md:58` |
| Guías, informes, `README.md`, `MEMORY.md`, índice y `CHANGELOG.md` | Sin rango | `docs/constitution.md:59`; `docs/sdd/README.md:24` |

**Inventario.** La tabla de `docs/sdd/README.md:28-64` declara 35 filas de datos: 34 archivos Markdown del corpus y el archivo de datos `firmantes_autorizados`. El árbol del commit auditado coincide con esa cifra. Este informe añade `docs/sdd/auditoria_final_v0_7_1.md` como archivo 36 sin fila en el corte, hecho que se registra en `AUD-107` y que la regla de inventario de `docs/sdd/README.md:69-70` califica como defecto.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida transcrita. Una afirmación de cierre exige la norma aplicable y el artefacto que la satisface; una afirmación de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento. Ningún resultado favorable del validador se interpreta como conformidad del régimen.

Escala de veredicto, conforme a `docs/sdd/plantillas/informe_auditoria.md:29-37`: `CONFORME`, `PARCIAL` (equivalente a `CONFORME CON OBSERVACIONES`), `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`.

Escala de severidad, conforme a `docs/sdd/plantillas/informe_auditoria.md:39-46`: `Crítica` afecta la validez de una compuerta o de la base; `Alta` rompe una regla normativa sin invalidar la compuerta; `Media` produce divergencia entre documentos de distinto rango o entre un criterio y su evidencia; `Baja` es un defecto de forma o de redacción.

**Estados de cierre.** `CERRADO` designa la observación cuya causa desapareció y cuenta con artefacto y evidencia en el commit auditado. `PARCIAL` designa la observación cuya causa persiste en un subconjunto acotado. `VIGENTE` designa la observación sin tratamiento.

**Numeración.** Conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md:216`, cada dimensión tiene diez números reservados y la continuación es inmediata al último asignado cuando la dimensión excede su capacidad. Los bloques de D6, D7, D8, D9 y D10 están agotados por las versiones previas (`AUD-051` a `AUD-100`) y el último número asignado de la serie es `AUD-102`, de modo que esta pasada asigna de `AUD-103` en adelante y no reutiliza número alguno.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Observaciones |
|---|---|---|---|---|
| D1 | Autoridad normativa, vigencia y aplicabilidad | `CONFORME` | `docs/constitution.md:48-59`, `:64-66`; `docs/sdd/README.md:15-24`, `:28-64` | `AUD-008` cerrada; la contradicción de alcance entre rangos se computa en D9 (`AUD-103`) |
| D2 | Ciclo de siete etapas y estado resultante | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:92-132`; `specs/015-cierre-auditoria-posterior/spec.md:280-291` | `AUD-015` cerrada; sin observación vigente |
| D3 | Contratos de artefactos y forma de cada uno | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:167-218`; `docs/sdd/plantillas/informe_auditoria.md:9-93`; `specs/015-cierre-auditoria-posterior/validation_report.md:1-91` | `AUD-024` cerrada; sin observación vigente |
| D4 | Compuertas G1 a G6: condición, evidencia y verificación | `CONFORME` | `docs/Flujo_de_Trabajo_Git.md:11-12`, `:456`, `:470`; `docs/sdd/PROTOCOLO_OPERATIVO.md:144-145`, `:302`, `:304` | `AUD-039` cerrada; sin observación vigente |
| D5 | Trazabilidad `RF/CB → CA → T → evidencia → commit → merge → release` | `CONFORME` | `specs/015-cierre-auditoria-posterior/validation_report.md:20-46`, `:86-91`; `specs/015-cierre-auditoria-posterior/spec.md:119-125` | `AUD-045` y `AUD-046` cerradas; sin observación vigente |
| D6 | Estados, transiciones e historial de transiciones | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:109-132`; `specs/014-cierre-observaciones-finales/spec.md:218`, `:231`; `specs/015-cierre-auditoria-posterior/spec.md:291` | `AUD-057` cerrada; `AUD-108` |
| D7 | Roles y menor privilegio | `PARCIAL` | `.opencode/agents/auditor.md:96-99`; `docs/sdd/PROTOCOLO_OPERATIVO.md:284-298`; `git show --stat 89416a7` | `AUD-068` cerrada; `AUD-110` |
| D8 | Evidencia y verificación: existencia, suficiencia e independencia | `NO CONFORME` | `specs/015-cierre-auditoria-posterior/spec.md:121`, `:202`; `specs/015-cierre-auditoria-posterior/tasks.md:286`, `:301`; `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335` | `AUD-076` cerrada; `AUD-109` |
| D9 | Integración Git y release | `NO CONFORME` | `docs/Flujo_de_Trabajo_Git.md:305-407`; `CHANGELOG.md:13-29`; `git show --stat f6f053a`; `git show 564bac4`; `git branch --list` | `AUD-087` cerrada; `AUD-088`, `AUD-089` y `AUD-090` parciales; `AUD-103` a `AUD-106` |
| D10 | Consistencia documental operativa | `PARCIAL` | `docs/sdd/README.md:28-64`; `MEMORY.md:13`; `specs/INDEX.md:21`; `CHANGELOG.md:227-244` | `AUD-099` y `AUD-100` cerradas; `AUD-107` |
| D11 | Integración continua: ejecución, alcance y exigibilidad | `CONFORME` | `.github/workflows/sdd.yml:1-31`; `docs/Flujo_de_Trabajo_Git.md:470`; `tools/git/protection_rules/main.json`, `dev.json` | `AUD-101` y `AUD-102` cerradas; sin observación vigente |

## 5. Hallazgos

### 5.1 Los diez hallazgos del informe anterior

| `AUD-NNN` | Dimensión | Severidad de origen | Estado | Evidencia en `5ba048d` | Nota |
|---|---|---|---|---|---|
| `AUD-039` | D4 | Baja | `CERRADO` | `docs/Flujo_de_Trabajo_Git.md:11` | La fila G5 incorpora «check `verify` del flujo `SDD` exigible con `strict: true` en `main` y en `dev`» y conserva en `:456` y `:470` la regla de bloqueo; la definición de la compuerta dejó de ser más estrecha que su propia regla |
| `AUD-057` | D6 | Media | `CERRADO` | `specs/014-cierre-observaciones-finales/spec.md:218`, `:231` | La fila T7 declara el release publicado con el tag verificado y la línea de G6 firmada, y la versión 0.8.1 registra el motivo; la precisión de la frase «sobre el commit de empaquetado» se computa en `AUD-108` |
| `AUD-068` | D7 | Baja | `CERRADO` | `docs/sdd/PROTOCOLO_OPERATIVO.md:294` | La remisión al bloque B3 desapareció y el bloque declara ejecutada la formalización de la allowlist con referencia a la matriz vigente de los seis roles |
| `AUD-075` | D8 | Media | `CERRADO` (residuo de `AUD-076`) | `specs/013-cierre-reauditoria-conformidad/validation_report.md:116-126` | La nota append-only declara el valor efectivo `PARCIAL` de las dos filas y el cierre de las siete observaciones del informe final; la causa raíz —un requisito que fija el veredicto de la auditoría— se computa en `AUD-109` |
| `AUD-076` | D8 | Media | `CERRADO` | `specs/013-cierre-reauditoria-conformidad/validation_report.md:120-121`; `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335` | La nota declara el valor efectivo `PARCIAL`, equivalente a `CONFORME CON OBSERVACIONES`, y deja de afirmar que la fila satisfaga `CONFORME`; el criterio publicado no se reescribe, conforme al destino declarado en el informe anterior |
| `AUD-087` | D9 | Alta | `CERRADO` | `docs/Flujo_de_Trabajo_Git.md:305`, `:307`; `CHANGELOG.md:17`; `git rev-parse "v0.7.0^{commit}"` = `5a3af48` | El procedimiento de corrección de un tag publicado existe con tres condiciones simultáneas, el caso `v0.7.0` queda registrado como deuda aceptada entre `ad739a0` y `5a3af48`, y el tag publicado no se movió en `v0.7.1`: el objeto `f4a6203` sigue apuntando a `5a3af48` |
| `AUD-088` | D9 | Alta | `PARCIAL` | `docs/Flujo_de_Trabajo_Git.md:340`, `:375`, `:474`; `tools/sdd/tests/test_agent_permissions.py:1991-2001`, `:2046`; `git log --oneline -S "len(filas), len(encabezados)" -- tools/sdd/tests/test_agent_permissions.py` = solo `5da6df6` | El alcance cerrado de cuatro artefactos y la excepción del empaquetado de `v0.7.0` quedaron declarados. La segunda mitad de la causa persiste: la «regularización de la comprobación afectada» que `specs/015-cierre-auditoria-posterior/spec.md:87` y `:202` afirman no tiene artefacto; `test_historial_de_releases` sigue comparando el número de filas con el de encabezados y la constante que admite `released` sigue igual, sin cambio posterior a `5da6df6` ni fila que lo describa en `CHANGELOG.md` |
| `AUD-089` | D9 | Media | `PARCIAL` | `specs/014-cierre-observaciones-finales/validation_report.md:59-70`; `CHANGELOG.md:31-62` | La nota append-only del reporte existe y transcribe las tres verificaciones de release. El segundo soporte que `docs/sdd/PROTOCOLO_OPERATIVO.md:314` exige —la entrada del release de `CHANGELOG.md`— no registra el resultado de G5 ni el de G6: la entrada `v0.7.0` conserva solo la línea de aprobación en `:62` |
| `AUD-090` | D9 | Alta | `PARCIAL` | `docs/Flujo_de_Trabajo_Git.md:406`; `CHANGELOG.md:19`; `git show --no-patch --format=%G? 564bac4` = `N` | El procedimiento de firma posterior a la publicación quedó declarado y el caso `494db2e` registrado con estado `N`. Falta el registro de la corrección en un commit firmado: la entrada `v0.7.0` conserva el texto introducido sin firma y la modificación del mismo párrafo volvió a ocurrir en un commit sin firma, hecho que se computa en `AUD-104` |
| `AUD-099` | D10 | Media | `CERRADO` | `docs/sdd/README.md:63`, `:64` | La fila 34 del informe anterior existe y el archivo de datos pasó a la fila 35; la recurrencia por este informe se registra en `AUD-107` y el origen de la fila, en `AUD-110` |
| `AUD-100` | D10 | Baja | `CERRADO` | `CHANGELOG.md:244`; `CHANGELOG.md:35` | El párrafo posterior al historial declara en tiempo pasado la línea de G6 registrada y la creación del tag sobre `5a3af48`, y la viñeta enumera los 16 identificadores asignados en lugar del rango que incluía números no asignados |

**Recuento de los diez:** 7 `CERRADO` y 3 `PARCIAL`; 0 `VIGENTE`.

**`AUD-066`.** El informe anterior lo cerró antes de enumerar los diez y esta pasada no lo reexamina como hallazgo propio; se verificó que su causa no reapareció: `docs/sdd/PROTOCOLO_OPERATIVO.md:286` mantiene la escritura del orquestador limitada a la verificación y el registro, y `.opencode/agents/sdd.md:45-55` conserva `.opencode/**` como única concesión con la denegación expresa de `.github/**` y de `MEMORY.md`.

### 5.2 Observaciones nuevas

| `AUD-NNN` | Dimensión | Severidad | Evidencia | Efecto observado | Destino |
|---|---|---|---|---|---|
| `AUD-103` | D9 | Media | `docs/sdd/PROTOCOLO_OPERATIVO.md:351` frente a `docs/Flujo_de_Trabajo_Git.md:340`, `:474`; `docs/constitution.md:65`; `git show --stat f6f053a` | §15 del rango 3 enumera tres artefactos de la rama `release/vX-Y-Z` y omite la línea `Release:` de los reportes publicados, mientras el rango 4 enumera cuatro. La corrección se aplicó primero en el rango 4 y dejó desalineado el rango 3, en orden inverso al que fija `docs/constitution.md:65`. Además, el empaquetado de `v0.7.1` escribió en `specs/015-cierre-auditoria-posterior/spec.md` la fila del historial de versiones y la fila T7, contenido que la enumeración cerrada de `docs/Flujo_de_Trabajo_Git.md:340` no admite aunque `docs/sdd/PROTOCOLO_OPERATIVO.md:119` y `:239` lo exijan al publicar | Alineación del rango 3 con el rango 4 y admisión expresa de las filas de historial y de transición en el alcance del empaquetado |
| `AUD-104` | D9 | Alta | `git show --no-patch --format=%G? 564bac4` = `N`; `git show 564bac4 -- CHANGELOG.md`; `git show --stat 564bac4`; `docs/constitution.md:76`; `docs/sdd/PROTOCOLO_OPERATIVO.md:270`, `:286` | El commit `564bac4`, sin firma verificable, modificó la entrada publicada `v0.7.0` de `CHANGELOG.md` —sustituyó la viñeta que citaba el rango de identificadores y el párrafo posterior al historial—, la fila T7 de `specs/014-cierre-observaciones-finales/spec.md` y añadió la nota de `specs/013-cierre-reauditoria-conformidad/validation_report.md`, artefactos publicados. Ese mismo commit introdujo en `docs/Flujo_de_Trabajo_Git.md:406` la regla que exige un commit firmado para cada modificación posterior a la publicación, de modo que la práctica del commit contradice la regla que declara | Registro de esas modificaciones en un commit firmado por el propietario, o declaración expresa de su tratamiento, sin reescribir el contenido publicado |
| `AUD-105` | D9 | Media | `CHANGELOG.md:13-29`; `specs/015-cierre-auditoria-posterior/validation_report.md:75-77`, `:86-91`; `docs/sdd/PROTOCOLO_OPERATIVO.md:314` | La entrada del release `v0.7.1` porta la línea de aprobación y el bloque de cambios, y no registra el resultado de G5 ni el de G6. El reporte de la spec registra la viñeta de G5 y anuncia en `:77` que «la transcripción del objeto `v0.7.1`, de su mensaje y de su commit objetivo se añade a este documento en la etapa Release, con el registro de G6»; esa transcripción no existe en el documento publicado, de modo que los dos soportes que §13 exige quedan incompletos y la promesa del propio reporte queda incumplida | Registro append-only del resultado de G6 y del objeto del tag en el reporte publicado y en la entrada del release |
| `AUD-106` | D9 | Media | `git branch --list`; `docs/Flujo_de_Trabajo_Git.md:369-373`, `:254` | El paso 8 del procedimiento obligatorio de release exige eliminar `release/vX-Y-Z` tras confirmar la integración. La rama `release/v0-7-1` sigue existiendo en local y la rama `release/v0-7-0` también; el listado remoto no las conserva (`git branch -r --list origin/release/v0-7-1` sin salida), de modo que la eliminación quedó a medias y la confirmación que la norma exige no se produjo | Eliminación de las dos ramas de empaquetado o declaración de su conservación |
| `AUD-107` | D10 | Media | `docs/sdd/README.md:28-64`; `docs/sdd/README.md:69-70`; `.opencode/agents/auditor.md:96`; `python -m unittest discover -s tools\sdd\tests -q` con «Ran 187 tests» y «FAILED (failures=1)» por `docs/sdd/README.md no registra la fila de docs/sdd/auditoria_final_v0_7_1.md` | Este informe añade `docs/sdd/auditoria_final_v0_7_1.md` y la tabla de inventario no porta su fila: 36 archivos frente a 35 filas. La regla de inventario califica el archivo sin fila como defecto y la prueba `test_inventario_del_corpus` lo detecta con el mensaje transcrito, de modo que el check `verify` del Pull Request que transporte el informe queda en rojo. El rol de auditoría no puede corregirlo: su única concesión alcanza `docs/sdd/auditoria_*.md` | Registro de la fila por el propietario o el `documenter` antes de integrar el informe, con la misma solución estructural que `AUD-099` y `AUD-110` muestran pendiente |
| `AUD-108` | D6 | Baja | `specs/014-cierre-observaciones-finales/spec.md:231`; `specs/015-cierre-auditoria-posterior/spec.md:291`; `git rev-parse "v0.7.0^{commit}"`, `"v0.7.1^{commit}"` | Las dos filas T7 declaran el tag «verificado sobre el commit de empaquetado». Los tags apuntan a los commits de merge publicados en `main` —`5a3af48` y `da30c86`— y no a los commits de empaquetado `5da6df6` y `f6f053a`, que son sus ancestros. La evidencia de la transición nombra un objeto distinto del que `docs/Flujo_de_Trabajo_Git.md:385-389` exige verificar | Corrección de la redacción de las dos filas en una spec posterior, sin renumerar las specs publicadas |
| `AUD-109` | D8 | Alta | `specs/015-cierre-auditoria-posterior/spec.md:121`, `:202`; `specs/015-cierre-auditoria-posterior/tasks.md:286`, `:301`; `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335`; `specs/015-cierre-auditoria-posterior/validation_report.md:69` | `RF-010` y `CA-008` de `SPEC-015` fijan como condición que el informe de auditoría de `v0.7.1` declare «10 de 10 cerradas», y ese recuento figura en el paquete de cierre y en `CHANGELOG.md:21`. Esta pasada acredita 7 cerradas y 3 parciales sobre las mismas diez, de modo que el valor declarado no se sostiene sobre la evidencia. La misma forma aparece en `RNF-001` y `CA-015` de `SPEC-013`, que fijan el veredicto `CONFORME` de la auditoría: un requisito del objeto auditado no puede determinar el recuento ni el veredicto del informe que lo audita, porque la compuerta que se apoya en ese informe deja de tener evidencia independiente | Decisión del propietario sobre la regla que impide fijar el veredicto en un requisito, con regularización por spec posterior de las dos specs afectadas |
| `AUD-110` | D7 | Media | `git show --stat 89416a7`; `git show --no-patch --format=%G? 89416a7` = `N`; `docs/sdd/README.md:63`; `.opencode/agents/auditor.md:96`; `docs/constitution.md:79`; `docs/sdd/PROTOCOLO_OPERATIVO.md:298` | El commit `89416a7`, de la sesión de auditoría anterior, contiene el informe `docs/sdd/auditoria_posterior_v0_7_0.md` y además la fila 34 de `docs/sdd/README.md`. El rol de auditoría tiene escritura limitada a `docs/sdd/auditoria_*.md`, de modo que la fila se escribió fuera de su alcance y sin firma; en el mismo commit, el informe registró `AUD-099` como archivo sin fila, afirmación que su propio commit contradice | Decisión del propietario sobre la autoría de la fila y declaración del cauce para que el inventario se actualice antes de integrar un informe |

### 5.3 Contraste del release `v0.7.1` con el procedimiento corregido

| Verificación | Resultado | Evidencia |
|---|---|---|
| Alcance del empaquetado limitado a los artefactos declarados | `PARCIAL` | `git show --stat f6f053a` registra cuatro archivos: `CHANGELOG.md`, `specs/INDEX.md`, `specs/015-cierre-auditoria-posterior/spec.md` y `specs/015-cierre-auditoria-posterior/validation_report.md`. El archivo de reporte cambia solo la línea `Release:` (`:89`), conforme. El de la spec cambia el frontmatter, y además la fila de historial de versiones y la fila T7, contenido que la enumeración de `docs/Flujo_de_Trabajo_Git.md:340` no admite. Se computa en `AUD-103` |
| Commit de empaquetado firmado por el propietario | `CONFORME` | `git show --no-patch --format=%G?%n%GS%n%GK f6f053a` devuelve `G`, `sebaxtianrioss@gmail.com` y `SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc`; la identidad figura en `docs/sdd/firmantes_autorizados:4` |
| Línea de aprobación de G6 dentro de la entrada del release | `CONFORME` | `CHANGELOG.md:13` abre `## [v0.7.1]` y `:29` porta `- Approved by: Agent Sebaxtian`, antes de `## [v0.7.0]` en `:31`; `--spec SPEC-015 --gate G6` devuelve «OK: sin hallazgos.» |
| Tag anotado, mensaje exacto y commit publicado | `CONFORME` | `git rev-parse "v0.7.1^{tag}"` = `4d0473b`, luego es objeto de tag; `git show -s --format=%s v0.7.1` muestra `Release v0.7.1`; `git rev-parse "v0.7.1^{commit}"` = `da30c86` = `git rev-parse main`; el tag se creó una sola vez según la evidencia disponible, sin referencia previa ni movimiento posterior (`AUD-087` no reapareció) |
| `main` ancestro de `dev` y tag alcanzable desde `main` | `CONFORME` | `git merge-base main dev` = `da30c86` = `git rev-parse main`, de modo que `main` es ancestro de `dev`; el commit del tag es el de `main`, luego es alcanzable desde ella |
| Vigencia del caso `v0.7.0` como deuda aceptada y admisión de un tercer tag | `CONFORME` | `docs/Flujo_de_Trabajo_Git.md:305-307` admite una sola excepción con tres condiciones simultáneas, desplaza la corrección a un release PATCH cuando existe consumidor y declara que el tag publicado «no se mueve de nuevo». El caso queda registrado con el identificador anterior `ad739a0` y el destino `5a3af48`; un tercer movimiento no está admitido por la norma y `v0.7.1` se publicó con tag propio sin recrear `v0.7.0` |

### 5.4 Recuento

| Clase | Recuento |
|---|---|
| Hallazgos del informe anterior examinados | 10 |
| Cerrados con evidencia | 7 |
| Parciales | 3 (`AUD-088`, `AUD-089`, `AUD-090`) |
| Vigentes de los diez | 0 |
| Residuo del informe final examinado | 1 (`AUD-075`, cerrado) |
| Observaciones nuevas | 8 |
| Nuevas de severidad `Crítica` | 0 |
| Nuevas de severidad `Alta` | 2 (`AUD-104`, `AUD-109`) |
| Nuevas de severidad `Media` | 5 (`AUD-103`, `AUD-105`, `AUD-106`, `AUD-107`, `AUD-110`) |
| Nuevas de severidad `Baja` | 1 (`AUD-108`) |
| Hallazgos vigentes del régimen en este corte | 11 |

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría (`docs/constitution.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:278`).

| Compuerta | Evidencia observada | Límite de esta auditoría |
|---|---|---|
| G1 | Quince specs con dos casillas en su sección de aprobaciones, G1 y G4, por ejemplo `specs/015-cierre-auditoria-posterior/spec.md:264-265`; `python tools\sdd\validate.py --all` no registra `[ERROR]` de forma ni de ubicación | Las firmas de los quince commits de G1 no se verificaron una por una; la aprobación corresponde al propietario |
| G4 | Línea de G4 en las quince specs y dictamen `CONVERGIDO` en el reporte de cada una, por ejemplo `specs/015-cierre-auditoria-posterior/validation_report.md:81`; el commit `3a98f2b` devuelve `G` | Las firmas de los quince commits de G4 no se verificaron una por una |
| G6 | Entrada `v0.7.1` con línea de registro firmada en un commit `G`; tag anotado `4d0473b` con mensaje `Release v0.7.1` sobre `da30c86`, igual a `main`; `main` ancestro de `dev`; `--gate G6` sin hallazgos; entrada con la cita de la auditoría que la motiva | El resultado de G6 no consta transcrito en los dos soportes (`AUD-105`); el informe que acredita el cierre de los diez hallazgos se emite después de la publicación y su recuento quedó fijado por un requisito de la spec auditada (`AUD-109`); la verificación favorable del validador no acredita conformidad |

**G2, G3 y G5.** Su verificación corresponde al orquestador y no constituye aprobación (`docs/sdd/PROTOCOLO_OPERATIVO.md:136`). La evidencia disponible es la declaración de las transiciones T4, T5 y T7 en `specs/015-cierre-auditoria-posterior/spec.md:288-291`, la viñeta de G5 en `specs/015-cierre-auditoria-posterior/validation_report.md:91` y el cierre de integración de las specs publicadas.

## 7. Veredicto global

**Recuento de hallazgos vigentes:** 11 —8 observaciones nuevas (0 `Crítica`, 2 `Alta`, 5 `Media` y 1 `Baja`) y 3 residuos parciales de severidad de origen `Alta`, `Media` y `Alta`—. De los diez hallazgos del informe anterior, 7 quedaron cerrados y 3 son parciales; el residuo de `AUD-075` quedó cerrado por `SPEC-015` y no se computa dos veces.

**Regla aplicada.** Una dimensión es `CONFORME` cuando no conserva observación abierta; es `PARCIAL` cuando conserva al menos una observación abierta de severidad `Media` o `Baja` con efecto declarado; es `NO CONFORME` cuando conserva una observación de severidad `Alta` o `Crítica`.

| Dimensión | Veredicto | Observación que lo sostiene |
|---|---|---|
| D1 | `CONFORME` | Ninguna vigente; `AUD-008` cerrada |
| D2 | `CONFORME` | Ninguna vigente; `AUD-015` cerrada |
| D3 | `CONFORME` | Ninguna vigente; `AUD-024` cerrada |
| D4 | `CONFORME` | Ninguna vigente; `AUD-039` cerrada |
| D5 | `CONFORME` | Ninguna vigente; `AUD-045` y `AUD-046` cerradas |
| D6 | `PARCIAL` | `AUD-108` (Baja) |
| D7 | `PARCIAL` | `AUD-110` (Media) |
| D8 | `NO CONFORME` | `AUD-109` (Alta) |
| D9 | `NO CONFORME` | `AUD-104` (Alta); `AUD-103`, `AUD-105` y `AUD-106` (Media); `AUD-088` y `AUD-090` (parciales de origen `Alta`) y `AUD-089` (parcial de origen `Media`) |
| D10 | `PARCIAL` | `AUD-107` (Media) |
| D11 | `CONFORME` | Ninguna vigente; `AUD-101` y `AUD-102` cerradas |

**Veredicto global:** `NO CONFORME`.

**Fundamento.** El régimen mejoró de forma verificable en este corte. Siete de los diez hallazgos anteriores desaparecieron con artefacto y evidencia: la fila G5 del rango 4 incorporó el check exigible, la remisión al bloque B3 se retiró, la fila T7 de `SPEC-014` declara el release publicado, las filas `RNF-001` y `CA-015` de `SPEC-013` tienen nota que declara su valor efectivo, el procedimiento de corrección de un tag publicado existe con su caso registrado, y el párrafo y la viñeta de `CHANGELOG.md` quedaron corregidos. El release `v0.7.1` cumple las verificaciones que se le podían exigir: empaquetado sobre cuatro rutas declaradas, commit firmado con clave de la lista versionada, tag anotado creado una sola vez sobre el commit publicado, línea de G6 dentro de la entrada y `main` ancestro de `dev`.

El valor `NO CONFORME` proviene de dos dimensiones. En D9, la regla de firma posterior a la publicación que `SPEC-015` introdujo fue contradicha por su propio commit de implementación: `564bac4`, sin firma, modificó la entrada publicada `v0.7.0` y dos artefactos publicados (`AUD-104`). Junto a ello, el empaquetado sigue escribiendo filas que su alcance declarado no admite y el rango 3 quedó desalineado del rango 4 en orden inverso al de precedencia (`AUD-103`), el release no transcribe el resultado de G6 en los dos soportes ni cumple la transcripción que su propio reporte anuncia (`AUD-105`), y la rama de empaquetado no se eliminó (`AUD-106`). En D8, un requisito de la spec auditada fija el recuento del informe que la audita y ese recuento —«10 de 10»— no se sostiene: esta pasada acredita 7 cerradas y 3 parciales (`AUD-109`). Las tres observaciones parciales de D9 y las de D6, D7 y D10 son de registro y de forma, y ninguna invalida una compuerta por sí sola; la de D8 afecta la independencia de la evidencia en que G6 se apoya, y por eso se registra, sin declarar compuerta.

**Alcance del veredicto.** El veredicto califica el régimen en `5ba048d`, no la calidad del release como entrega ni el acierto de su contenido. Un tag publicado no se repara moviéndolo: la corrección de `AUD-104` es declarativa y firmada, y la de `AUD-103` es de alineación normativa.

**Declaración expresa.** Este informe no aprueba compuerta alguna: no declara G1, G2, G3, G4, G5 ni G6, no emite línea de aprobación y no sustituye la firma del propietario ni su verificación. Registra el resultado de una auditoría de conformidad y se limita a la evidencia citada. Un resultado favorable del validador o de una suite no acredita la conformidad del régimen ni autoriza un release.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| Registrar las modificaciones de `564bac4` en un commit firmado por el propietario o declarar su tratamiento sin reescribir el contenido publicado | `AUD-104` y la parte pendiente de `AUD-090` | registro del propietario | Decisión del propietario |
| Alinear §15 del rango 3 con el rango 4 y admitir en el alcance del empaquetado las filas de historial y de transición | `AUD-103` | corrección de alineación | Ninguna |
| Registrar de forma append-only el resultado de G6 y el objeto del tag en el reporte de `SPEC-015` y en la entrada `v0.7.1` | `AUD-105` y la parte pendiente de `AUD-089` | registro del propietario | `AUD-104` resuelto |
| Eliminar las ramas `release/v0-7-1` y `release/v0-7-0` o declarar su conservación | `AUD-106` | corrección | Ninguna |
| Registrar la fila de `docs/sdd/auditoria_final_v0_7_1.md` en la tabla de inventario | `AUD-107` | corrección | Escritura del propietario o de `documenter`; desbloquea la integración del informe |
| Regularizar el criterio de `test_historial_de_releases` y la constante que admite `released`, con fila en el registro de cambios | Parte pendiente de `AUD-088` | spec posterior | `AUD-103` resuelto en su parte normativa |
| Fijar la regla que impide a un requisito determinar el recuento y el veredicto de la auditoría, y regularizar `SPEC-013` y `SPEC-015` | `AUD-109` | spec posterior | Decisión del propietario |
| Declarar el cauce para que el inventario se actualice antes de integrar un informe y atribuir la fila de `89416a7` | `AUD-110` | decisión del propietario | `AUD-107` |
| Corregir la redacción de las dos filas T7 que nombran el commit de empaquetado como destino del tag | `AUD-108` | spec posterior | Ninguna |

## 9. Limitaciones

| Elemento | Causa | Evidencia o comprobación que faltaría |
|---|---|---|
| Creación única del tag `v0.7.1` | Las etiquetas no llevan reflog en esta configuración; el objeto de tag no conserva su historia. Se acreditó la ausencia de una referencia previa y de un movimiento posterior, no el número de operaciones de creación | Bitácora de la operación de etiquetado o registro del remoto (`git ls-remote`) con el instante de publicación |
| Orden exacto entre la publicación del tag y el avance local de `main` | La fecha del tagger es `2026-11-20 11:16:05 -0500` y el reflog registra el avance local de `main` a las `11:16:09`; el commit objetivo ya existía en el remoto por el Pull Request #25. La diferencia de segundos no altera el destino verificado | Bitácora del remoto con la hora de creación del tag |
| Firmas de los commits de G1 y G4 de las quince specs | La sesión verificó la firma del commit de G6 y de los commits de aprobación citados, y no recorrió los treinta commits de G1 y de G4 uno por uno | Resultado de la comprobación de firma para cada commit de G1 y de G4, con la huella contrastada contra `docs/sdd/firmantes_autorizados` |
| Correspondencia entre la clave firmante y la lista versionada | `.git/config:25-26` declara el archivo de firmantes admitidos fuera del repositorio; la verificación se sostiene en que la identidad del commit figura en `docs/sdd/firmantes_autorizados:4` y en la comprobación por contenido registrada en el informe anterior | Configuración que apunte la verificación a la lista versionada |
| Estado remoto de la protección de ramas | La configuración remota no forma parte del repositorio y la sesión no consultó la API de reglas | Salida de `python tools/git/verify_branch_protection.py` con token válido |
| Ejecución efectiva del job `verify` en GitHub | Se acreditó por lectura del flujo y por la ejecución local de las dos suites; no se observó una ejecución del job | Registro de una ejecución con el punto de corte y el número de commits examinados |
| Efecto de este informe sobre la suite | `test_inventario_del_corpus` recorre el archivo nuevo sin fila y la ejecución posterior a la escritura de este documento devuelve «Ran 187 tests» y «FAILED (failures=1)», con el mensaje `docs/sdd/README.md no registra la fila de docs/sdd/auditoria_final_v0_7_1.md`; el hecho se registra en `AUD-107` y no se corrige desde el rol de auditoría | Fila de inventario registrada por el propietario o el `documenter` |

Ningún elemento de esta lista se presume cumplido.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | Identificación del commit auditado, de la rama y de la rama de la sesión | `5ba048dc3da1a4ce5e2fb9516585b5c71a5b2179`; `git rev-parse dev`; `git rev-parse main`; `git branch --list` |
| B | Tags de los dos releases: objeto, mensaje y destino | `git rev-parse "v0.7.0^{tag}"` = `f4a6203` y `"v0.7.0^{commit}"` = `5a3af48`; `git rev-parse "v0.7.1^{tag}"` = `4d0473b` y `"v0.7.1^{commit}"` = `da30c86`; `git show -s --format=%s v0.7.1` = `Release v0.7.1`; `git show -s --format=%ci v0.7.1` = `2026-11-20 11:16:05 -0500` |
| C | Ancestría de las ramas base y del tag | `git merge-base main dev` = `da30c86` = `git rev-parse main`; `git rev-parse "v0.7.1^{commit}"` = `git rev-parse main` |
| D | Secuencia del release `v0.7.1` | `.git/logs/HEAD:256-264`: creación de `release/v0-7-1` desde `ad2cbc2`, empaquetado `f6f053a`, PR #24 `de6fefd`, PR #25 `da30c86`, sincronización `5c723d5` |
| E | Padres de los merges del release | `git show --no-patch --format=%P de6fefd` = `ad2cbc2 f6f053a`; `da30c86` = `5a3af48 de6fefd`; `5c723d5` = `de6fefd da30c86`; `f6f053a` = `ad2cbc2` |
| F | Estado de firma de los commits citados | `f6f053a` = `G`; `3a98f2b` = `G`; `4dd07f5`, `da30c86` y `5ba048d` = `E`; `564bac4`, `9750fed`, `2b38aaf`, `ab6ab09` y `89416a7` = `N` |
| G | Alcance del commit de empaquetado | `git show --stat f6f053a`: `CHANGELOG.md`, `specs/015-cierre-auditoria-posterior/spec.md`, `specs/015-cierre-auditoria-posterior/validation_report.md`, `specs/INDEX.md`; `git show f6f053a -- specs/015-cierre-auditoria-posterior/validation_report.md` muestra solo la línea `Release: v0.7.1` |
| H | Modificación sin firma de artefactos publicados | `git show --stat 564bac4`; `git show 564bac4 -- CHANGELOG.md`; `git show --no-patch --format=%G? 564bac4` = `N` |
| I | Entrada del release y línea de registro de G6 | `CHANGELOG.md:13-29`; historial en `:227-242`; párrafo en `:244` |
| J | Denominador del cierre declarado y su base | `specs/015-cierre-auditoria-posterior/spec.md:121`; `specs/015-cierre-auditoria-posterior/tasks.md:286`, `:301`; `specs/015-cierre-auditoria-posterior/validation_report.md:54-69` |
| K | Requisitos que fijan el veredicto de la auditoría | `specs/013-cierre-reauditoria-conformidad/spec.md:139`, `:335`; `specs/015-cierre-auditoria-posterior/spec.md:121`, `:202` |
| L | Notas append-only de los reportes publicados | `specs/014-cierre-observaciones-finales/validation_report.md:59-70`; `specs/013-cierre-reauditoria-conformidad/validation_report.md:116-126` |
| M | Criterio generalizado que `AUD-088` dejó pendiente | `tools/sdd/tests/test_agent_permissions.py:1991-2001`, `:2046`; `git log --oneline -S "len(filas), len(encabezados)" -- tools/sdd/tests/test_agent_permissions.py` = `5da6df6` |
| N | Inventario del corpus y archivo sin fila | `docs/sdd/README.md:28-64`, `:69-70`; recuento de 35 filas frente a 36 archivos con este informe |
| O | Ramas de empaquetado conservadas | `git branch --list`: `release/v0-7-0` y `release/v0-7-1`; `git branch -r --list origin/release/v0-7-1` sin salida |
| P | Procedimiento de corrección de tag y de firma posterior | `docs/Flujo_de_Trabajo_Git.md:305`, `:307`, `:400`, `:406`; `docs/sdd/PROTOCOLO_OPERATIVO.md:312`, `:314` |
| Q | Salidas del validador y de las suites | `--all` sin `[ERROR]` y con `[WARN]` de legado; `--spec SPEC-015 --gate G6` = «OK: sin hallazgos.»; `tools\sdd\tests` = «Ran 187 tests» y «OK» antes del informe y «FAILED (failures=1)» por el archivo sin fila después de su escritura; `tools\git\tests` = «Ran 48 tests in 20.071s» y «OK» |
| R | Flujo de integración continua | `.github/workflows/sdd.yml:15-31`; `docs/Flujo_de_Trabajo_Git.md:470` |
