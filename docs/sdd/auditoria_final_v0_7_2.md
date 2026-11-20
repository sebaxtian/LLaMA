# Informe de auditoría — estado integrado de `dev` para el release v0.7.2

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, implementado en `.opencode/agents/auditor.md`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-20 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), specs `SPEC-001` a `SPEC-016`, inventario de hallazgos, actas de ratificación, validador `tools/sdd`, suite del mecanismo `tools/sdd/tests`, suite de las herramientas de Git `tools/git/tests`, agentes de `.opencode/`, flujo de integración continua, reglas de protección de ramas, registros Git locales y registro de cambios, con corte en el commit `104496d` de `dev`.
- **Objeto:** emitir el veredicto del estado integrado, calcularlo desde `docs/sdd/inventario_hallazgos.md`, contrastarlo con el declarado, verificar el cierre de `H-01` a `H-03` y de `OBS-001` a `OBS-004`, comprobar la aplicación del acta de interpretación y determinar si el release `v0.7.2` queda habilitado con cero hallazgos abiertos.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas, no aprueba compuertas, no emite línea de aprobación y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `104496dfd4aedce9be0d1760b01da1d3cc35a85f` (`.git/refs/heads/dev`) |
| Rama | `docs/auditoria-final-v0-7-2`, creada desde `dev` en `104496d` (`.git/HEAD`; `.git/logs/HEAD:304`) |
| Fecha de corte | 2026-11-20 |
| Releases de referencia | `v0.7.0`: objeto de tag con mensaje `Release v0.7.0` y commit objetivo `5a3af48`. `v0.7.1`: objeto de tag `4d0473b` (`.git/refs/tags/v0.7.1`), mensaje `Release v0.7.1` y commit objetivo `da30c86`, igual a `main` (`CHANGELOG.md:47`) |
| Validador | `python tools\sdd\validate.py --all`: no ejecutado en esta sesión; la evidencia del corte se transcribe de `specs/016-cierre-auditoria-v0-7-1/validation_report.md:20` y `:109` |
| Suites | No ejecutadas en esta sesión; se transcriben «Ran 222 tests» y «OK» para `tools\sdd\tests` y «Ran 48 tests» y «OK» para `tools\git\tests` (`validation_report.md:17-18`) |
| Entorno | Windows 11 (`win32`); permisos del rol: lectura del corpus y escritura limitada a `docs/sdd/auditoria_*.md` (`.opencode/agents/auditor.md:8-52`); la ejecución de shell está denegada en esta sesión |
| Rol ejecutor | `auditor` |

**Procedimiento.** Cuatro pasos. Primero, lectura íntegra de la base normativa de rangos 1 a 5, de los artefactos de `SPEC-016`, del acta de interpretación y de los informes de auditoría previos. Segundo, lectura de las 85 filas del inventario con verificación de la forma de la cita, del vocabulario del estado, del recuento y del contraste entre el veredicto declarado y el calculado. Tercero, contraste de los siete puntos del régimen: inventario completo, regla citada por hallazgo, ausencia de autorreferencia, seis artefactos de empaquetado, destino del tag en la fila T7, ratificaciones firmadas y auditoría previa al release. Cuarto, examen de las once dimensiones con la evidencia transcrita en §10.

## 2. Base normativa e inventario

La jerarquía consta de siete rangos y una categoría sin rango, declarada de forma coincidente en `docs/constitution.md:48-59` y en `docs/sdd/README.md:15-24`. Cada documento de la base declara su rango y su carácter en el encabezado (`docs/sdd/PROTOCOLO_OPERATIVO.md:3`; `docs/Flujo_de_Trabajo_Git.md:3`; `docs/sdd/plantillas/informe_auditoria.md:3`). La categoría sin rango no fija reglas y su contradicción con un documento normativo se corrige en el documento sin rango (`docs/constitution.md:66`; `docs/sdd/PROTOCOLO_OPERATIVO.md:44`).

| Documento | Rango | Cita |
|---|---|---|
| `docs/constitution.md` | 1 | `docs/constitution.md:52` |
| `AGENTS.md` | 2 | `docs/constitution.md:53` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md` | 3 | `docs/constitution.md:54` |
| `docs/Flujo_de_Trabajo_Git.md` | 4 | `docs/constitution.md:55` |
| `docs/sdd/plantillas/*.md` | 5 | `docs/constitution.md:56` |
| `specs/NNN-slug/*.md` | 6 | `docs/constitution.md:57` |
| `src/`, `tools/`, `tests/`, `.opencode/` | 7 | `docs/constitution.md:58` |
| Guías, informes, `README.md`, `MEMORY.md`, índice y `CHANGELOG.md` | Sin rango | `docs/constitution.md:59`; `docs/sdd/README.md:24` |

**Corpus.** La tabla de inventario de `docs/sdd/README.md:28-69` declara 40 filas de datos y el árbol del corte contiene 40 archivos: 32 en `docs/sdd/`, 7 en `docs/sdd/plantillas/` y `docs/sdd/firmantes_autorizados`. Las filas 39 y 40 registran `docs/sdd/auditoria_previa_v0_7_2.md` y `docs/sdd/ratificacion_interpretacion.md` (`docs/sdd/README.md:68-69`). Este informe añade un archivo 41 que en el corte carece de fila; la fila la escribe el rol `documenter` antes de la integración (`docs/sdd/PROTOCOLO_OPERATIVO.md:300`; `docs/sdd/plantillas/informe_auditoria.md:24`), y mientras falte, `docs/sdd/README.md:75` lo califica como defecto y la prueba `test_inventario_del_corpus` deja el check `verify` en rojo (anexo K).

**Inventario de hallazgos.** `docs/sdd/inventario_hallazgos.md:34-115` porta 82 filas para 82 identificadores `AUD-001` a `AUD-110`, y el registro de `:160-162` añade 3 filas para `AUD-111`, `AUD-112` y `AUD-113`, emitidas por `docs/sdd/auditoria_previa_v0_7_2.md`. El recuento sobre las 85 filas es 79 en `cerrado` y 6 en `cerrado por ratificación` —`AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053` en §4 y `AUD-111` en §8—, con 0 en `parcial`, 0 en `vigente` y 0 en `cerrado por exención`; las 85 filas citan la regla con la forma `ruta §capítulo:línea` y declaran evidencia de cierre. El anexo de `:144-146` declara 0 observaciones y 0 tratamientos, y `:150` declara el veredicto `CONFORME`. La comprobación `C-19` y el cálculo de `C-21` se ejecutan sobre las 82 filas de §4 por el límite de `tools/sdd/hallazgos.py:23-31`, de modo que las 3 filas de §8 quedan fuera del mecanismo y su recuento se hace aquí por lectura directa; los dos recuentos devuelven 0 hallazgos abiertos y el mismo veredicto.

**Actas.** `docs/sdd/ratificacion_historica.md` ratifica las 5 exenciones y las 2 modificaciones sin firma, firmada en el commit `9042ae6` (`:16-31`). `docs/sdd/ratificacion_interpretacion.md` fija la lectura de §16 y consta firmada en el commit `8c8a2a3` (`:5-10` y `:33-36`), cuya creación registra `.git/logs/HEAD:295` con el asunto «docs(sdd): fijar la interpretacion de la regla de autorreferencia».

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida transcrita. Una afirmación de cumplimiento exige el artefacto y su ubicación; una de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento.

**Regla citada.** Cada hallazgo cita la regla que incumple con la forma `ruta §capítulo:línea`, conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md §16:382`. El juicio que no alcanza una regla de los rangos 1 o 3 se registra como observación, queda fuera del recuento y no computa como hallazgo abierto (`docs/sdd/plantillas/informe_auditoria.md:30`).

Escala de veredicto (`docs/sdd/plantillas/informe_auditoria.md:32-40`): `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`.

Escala de severidad (`docs/sdd/plantillas/informe_auditoria.md:42-49`): `Crítica` afecta la validez de una compuerta o de la base; `Alta` rompe una regla normativa sin invalidar la compuerta; `Media` produce divergencia entre documentos de distinto rango; `Baja` es un defecto de forma, de redacción o de registro.

**Numeración.** Este informe no asigna `AUD-NNN` porque no emite hallazgos con regla citada. El espacio se reserva a los hallazgos con fila en el inventario (`docs/sdd/PROTOCOLO_OPERATIVO.md:216`) y el rol de auditoría no escribe filas (`:300`). Si un corte posterior emitiera un hallazgo, el número libre es `AUD-114`, inmediato al último asignado. Las observaciones se numeran `OBS-005` a `OBS-008`, a continuación de las cuatro del informe previo, y no reutilizan número.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Hallazgos y observaciones |
|---|---|---|---|---|
| D1 | Autoridad normativa, vigencia y aplicabilidad | `CONFORME` | `docs/constitution.md:48-59`, `:61-66`; `docs/sdd/README.md:15-24`, `:28-69` | Ninguno |
| D2 | Ciclo de siete etapas y estado resultante | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:72-132`; `specs/016-cierre-auditoria-v0-7-1/spec.md:4-10`, `:445-471` | Ninguno |
| D3 | Contratos de artefactos y forma de cada uno | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:167-218`; `docs/sdd/plantillas/informe_auditoria.md:9-107`; `specs/016-cierre-auditoria-v0-7-1/validation_report.md:23-67` | Ninguno |
| D4 | Compuertas G1 a G6: condición, evidencia y verificación | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:136-145`; `docs/Flujo_de_Trabajo_Git.md:9-16`; `specs/016-cierre-auditoria-v0-7-1/spec.md:438-439` | Ninguno |
| D5 | Trazabilidad `RF/CB → CA → T → evidencia` | `CONFORME` | `specs/016-cierre-auditoria-v0-7-1/spec.md:41-58`, `:312-412`; `validation_report.md:25-67`; `tasks.md:36-37` | Ninguno |
| D6 | Estados, transiciones e historial de transiciones | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:94-132`; `specs/016-cierre-auditoria-v0-7-1/spec.md:460-471` | `OBS-007` |
| D7 | Roles y menor privilegio | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:284-300`; `.opencode/agents/reviewer.md:2`, `:44-49`, `:104-109`; `.opencode/agents/auditor.md:2`, `:51` | `OBS-006` |
| D8 | Evidencia y verificación: existencia, suficiencia e independencia | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:378`; `docs/sdd/ratificacion_interpretacion.md:16-29`; `docs/sdd/inventario_hallazgos.md:160` | `OBS-005` |
| D9 | Integración Git y release | `CONFORME` | `docs/Flujo_de_Trabajo_Git.md:343-352`, `:412`, `:414`; `CHANGELOG.md:25-49`; `.git/refs/heads/main`, `.git/refs/tags/v0.7.1` | Ninguno |
| D10 | Consistencia documental operativa | `CONFORME` | `docs/sdd/README.md:28-69`; `MEMORY.md:13`; `specs/INDEX.md:22`; `CHANGELOG.md:11-23` | `OBS-008` |
| D11 | Integración continua: ejecución, alcance y exigibilidad | `CONFORME` | `.github/workflows/sdd.yml:1-31`; `tools/git/protection_rules/main.json:2-9`; `tools/git/protection_rules/dev.json:2-9` | Ninguno |

El veredicto global se obtiene del cálculo de `RF-013` sobre las filas del inventario y no de esta matriz; la coincidencia entre ambos se declara en §7. Las cuatro observaciones son de severidad `Baja` y ninguna impide `CONFORME` (`docs/sdd/plantillas/informe_auditoria.md:77`).

**Contraste del régimen nuevo.** Los siete puntos que `SPEC-016` introduce se contrastan con el corte `104496d`:

| Punto | Resultado | Evidencia |
|---|---|---|
| Inventario completo | `CONFORME` | 85 filas para 85 identificadores emitidos por los 6 informes presentes; 82 en §4 para los 5 informes del mecanismo y 3 en §8 para el informe previo (`docs/sdd/inventario_hallazgos.md:34-115`, `:160-162`) |
| Hallazgo con regla citada | `CONFORME` | Las 85 filas usan la forma `ruta §capítulo:línea`; `C-20` sin diferencia (`tools/sdd/hallazgos.py:394-405`) |
| Ausencia de autorreferencia | `CONFORME` | `RF-015` y `CA-016` expresan la condición sobre el inventario y no nombran los valores del veredicto (`specs/016-cierre-auditoria-v0-7-1/spec.md:201`, `:412`); el acta de `8c8a2a3` fija la lectura de §16 (`docs/sdd/ratificacion_interpretacion.md:18-22`) |
| Seis artefactos de empaquetado | `CONFORME` | Tabla con claves `A1` a `A6` idéntica en `docs/sdd/PROTOCOLO_OPERATIVO.md:355-362` y en `docs/Flujo_de_Trabajo_Git.md:345-352`; `C-22` sin diferencia |
| Destino del tag en la fila T7 | `CONFORME` | `specs/014-cierre-observaciones-finales/spec.md:232` declara `5a3af48` con `5da6df6` como ancestro; `specs/015-cierre-auditoria-posterior/spec.md:293` declara `da30c86` con `f6f053a` como ancestro; `C-23` sin diferencia |
| Ratificación firmada | `CONFORME` | Actas de `9042ae6` y de `8c8a2a3`; el estado de firma no se re-verificó en esta sesión (anexo L) |
| Auditoría previa al release | Presente | Este informe se ejecuta sobre el estado integrado en `dev` (`docs/Flujo_de_Trabajo_Git.md:16`); el recuento de hallazgos abiertos es 0 |

## 5. Hallazgos

Ninguno. El corte `104496d` no presenta un juicio que cite una regla de los rangos 1 o 3 como incumplida en las once dimensiones. Por esa razón este informe no asigna `AUD-NNN` y no abre fila en el inventario.

### Observaciones

| N.º | Severidad | Observación | Tratamiento |
|---|---|---|---|
| `OBS-005` | `Baja` | `docs/sdd/PROTOCOLO_OPERATIVO.md §16:378` declara que un requisito «no declara un recuento de hallazgos», mientras `RF-015` y `CA-016` exigen que el registro conste con 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento (`specs/016-cierre-auditoria-v0-7-1/spec.md:201`, `:412`). La conciliación depende de la lectura del acta y no del texto del protocolo. | Registrado: acta `docs/sdd/ratificacion_interpretacion.md:18-22`, que califica la condición como estado del inventario y no como predicción del informe, firmada en el commit `8c8a2a3` (2026-11-21); `AUD-111` consta `cerrado por ratificación` en `docs/sdd/inventario_hallazgos.md:160`. |
| `OBS-006` | `Baja` | La concesión mecánica del `reviewer` conserva `specs/*/validation_report.md` y la del `auditor`, `docs/sdd/auditoria_*.md` (`.opencode/agents/reviewer.md:44-49`; `.opencode/agents/auditor.md:51`); el límite a la spec en curso y al informe propio consta en la prosa del rol y en §12:296, no en una regla de permiso más específica. | Registrado: declaración de autoría y de límite en `docs/sdd/PROTOCOLO_OPERATIVO.md:296` y en `.opencode/agents/reviewer.md:104` y `:109`, integrada en el commit `58d67d5` (2026-11-20); no se observa escritura del rol en el reporte de una spec ajena en el corte. |
| `OBS-007` | `Baja` | La fila T6 del ciclo reabierto incluye la integración `6b85789` como evidencia de una transición anterior a ella, y las etiquetas T5 y T6 figuran dos veces (`specs/016-cierre-auditoria-v0-7-1/spec.md:467-471`). La repetición de `OBS-004` es de forma: la fila invoca G4 del ciclo reabierto y las 39 filas en `PASADO`, que `§5` exige como evidencia, y añade un hecho posterior. | Sin tratamiento registrado; severidad `Baja`, que no impide `CONFORME` conforme a `RF-013`. |
| `OBS-008` | `Baja` | El bloque `Unreleased` no porta viñeta propia de la reapertura ni de la cláusula de §12 que esa reapertura introdujo (`CHANGELOG.md:11-23`), y el ciclo reabierto numera la implementación y la validación en PATCH —`0.9.2` y `0.9.3`— donde el ciclo anterior usó MINOR —`0.7.0` y `0.8.0`— (`specs/016-cierre-auditoria-v0-7-1/spec.md:452-456`). La reapertura ya consumió el incremento MINOR en `0.9.0` (`:453`) y el bloque `Unreleased` registra los cambios de base del ciclo. | Sin tratamiento registrado; severidad `Baja`, que no impide `CONFORME` conforme a `RF-013`. |

Las cuatro observaciones son de severidad `Baja`, no computan como hallazgo abierto y no impiden el veredicto `CONFORME` (`docs/sdd/plantillas/informe_auditoria.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:393`).

### Verificación de los hallazgos y observaciones del informe previo

| Identificador | Declaración del informe previo | Estado observado en `104496d` | Evidencia |
|---|---|---|---|
| `H-01` / `AUD-111` | `RF-015` y `CA-016` fijaban el veredicto `CONFORME` | Corregido y cerrado por ratificación: los cuatro bloques expresan la condición sobre el inventario y no nombran valores del veredicto | `specs/016-cierre-auditoria-v0-7-1/spec.md:201`, `:247`, `:297`, `:412`; `docs/sdd/ratificacion_interpretacion.md:18-22`; `docs/sdd/inventario_hallazgos.md:160` |
| `H-02` / `AUD-112` | El rol `reviewer` escribió en reportes publicados y su concesión no tenía límite de spec | Corregido por la vía declarativa: §12 atribuye la nota al `documenter` con firma del propietario y limita al `reviewer` a la spec en curso; el rol declara el mismo límite y la spec atribuye la nota al `documenter` | `docs/sdd/PROTOCOLO_OPERATIVO.md:296`; `.opencode/agents/reviewer.md:2`, `:104`, `:109`; `specs/016-cierre-auditoria-v0-7-1/spec.md:85`, `:87`, `:205`; `docs/sdd/inventario_hallazgos.md:161` |
| `H-03` / `AUD-113` | `MEMORY.md` declaraba `tasked` y lo atribuía al índice | Corregido: declara `validated`, release pendiente y cita el índice; las tres fuentes coinciden | `MEMORY.md:13`; `specs/016-cierre-auditoria-v0-7-1/spec.md:4`, `:10`; `specs/INDEX.md:22` |
| `OBS-001` | La fila `AUD-108` citaba `specs/015…/spec.md:292` | Corregido a `:293`, que porta la fila T7 | `docs/sdd/inventario_hallazgos.md:113`; `specs/015-cierre-auditoria-posterior/spec.md:293` |
| `OBS-002` | El rango 4 describía la suite «con 187 pruebas» | Corregido a 222 pruebas, cifra que coincide con la ejecución transcrita | `docs/Flujo_de_Trabajo_Git.md:235`; `validation_report.md:17` |
| `OBS-003` | Fechas documentales un día posteriores al sello del commit | Tratado por convención declarada: las fechas de las dos tablas son documentales y se declaran en UTC | `specs/016-cierre-auditoria-v0-7-1/spec.md:473` |
| `OBS-004` | La fila T6 incluía una integración posterior a G4 | Corregido en la fila del primer ciclo y reproducido en la del ciclo reabierto, que se registra como `OBS-007` | `specs/016-cierre-auditoria-v0-7-1/spec.md:468`, `:471` |

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría (`docs/constitution.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:278`).

| Compuerta | Evidencia observada | Límite de esta auditoría |
|---|---|---|
| G1 | Casilla G1 marcada en `specs/016-cierre-auditoria-v0-7-1/spec.md:438`, con el nombre del propietario y fecha 2026-11-21; `clarify.md` cerrado sin casillas pendientes | La aprobación corresponde al propietario; este informe no la declara ni reproduce la línea de registro |
| G4 | Casilla G4 en `spec.md:439`; dictamen `CONVERGIDO` con 39 de 39 filas en `PASADO` (`validation_report.md:67`, `:78-81`) | La matriz acredita el commit `58d67d5` para 2 filas y `e2ede7a` para las 37 anteriores; no se re-ejecutó la validación |
| G5 | Merge `6b85789` del Pull Request #32 con dos padres `922ee68` y `0283833`, e integración `104496d` del Pull Request #33 en `dev`; validador posterior sin hallazgos según `validation_report.md:109`; rama de trabajo eliminada | La verificación corresponde al orquestador y no constituye aprobación; los padres de `6b85789` se citan del reporte y la forma de dos padres no se re-verificó en esta sesión |
| G6 | El registro de cambios no porta entrada `v0.7.2` (`CHANGELOG.md:11-23`) y no existe tag del release ni rama `release/v0-7-2` en `.git/refs/heads` ni en `.git/refs/remotes/origin` | No emitido; la condición de publicación se examina en §7 |

## 7. Veredicto global

**Veredicto calculado desde el inventario.** `CONFORME`. Recuento sobre las 85 filas: 0 hallazgos abiertos, 79 en `cerrado`, 6 en `cerrado por ratificación` y 0 en `cerrado por exención`, con 0 filas sin regla citada y 0 filas sin evidencia de cierre. La precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME` se aplica en ese orden y el primer valor que se cumple es `CONFORME` (`docs/sdd/PROTOCOLO_OPERATIVO.md:384-393`). El cálculo sobre las 82 filas que lee el mecanismo devuelve el mismo valor. El valor coincide con el declarado en `docs/sdd/inventario_hallazgos.md:150`, de modo que no hay diferencia que transcribir entre el cálculo y la declaración del inventario.

**Veredicto del estado auditado.** `CONFORME`. Este informe no emite hallazgos con regla citada y sus cuatro observaciones son de severidad `Baja`, de modo que el número de hallazgos abiertos es 0 y el número de observaciones de severidad `Alta` o `Media` sin tratamiento es 0. La trazabilidad `RF/CB → CA → T → evidencia` del ciclo reabierto consta con 39 de 39 filas en `PASADO` y 36 de 36 tareas cerradas (`specs/016-cierre-auditoria-v0-7-1/tasks.md:36-37`).

**Aplicación de la interpretación ratificada.** El acta de `8c8a2a3` fija que la prohibición de §16 alcanza a declarar por anticipado el veredicto y a fijar por anticipado el recuento o el conjunto de dimensiones de un informe no realizado, y que no alcanza a condicionar la publicación a la verificación de un estado del inventario (`docs/sdd/ratificacion_interpretacion.md:18-22`). La lectura se aplica: `RF-015`, `RNF-009`, `CB-012` y `CA-016` no nombran `CONFORME`, `PARCIAL`, `NO CONFORME` ni `NO VERIFICABLE` y expresan la condición como 0 hallazgos abiertos y 0 observaciones sin tratamiento (`spec.md:201`, `:247`, `:297`, `:412`); el umbral de publicación del rango 4 conserva la exigencia de `CONFORME` y queda fuera del alcance de la prohibición de §16, que solo alcanza a las specs (`docs/Flujo_de_Trabajo_Git.md:16`, `:232`). Ninguna spec del corpus fija el veredicto, el recuento ni las dimensiones de un informe concreto posterior a su aprobación; los dos criterios publicados de `SPEC-013` que conservaban esa forma quedan sin efecto por la nota append-only de `specs/013-cierre-reauditoria-conformidad/validation_report.md:128-134`. La única tensión literal entre §16:378 y `RF-015` tiene tratamiento registrado y consta como `OBS-005`; no queda infracción del §16 sin tratamiento.

**Condición de publicación.** Se satisface con 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento. El release `v0.7.2` queda habilitado en cuanto al veredicto y sujeta su publicación a cuatro condiciones que este informe no ejecuta: la fila 41 de este informe en la tabla de inventario, escrita por el `documenter` antes de la integración (`docs/sdd/PROTOCOLO_OPERATIVO.md:300`); la integración de la rama de empaquetado por Pull Request con `merge --no-ff` sobre los seis artefactos de `§15`; la verificación de G5 por el orquestador; y la aprobación de G6 por el propietario con la transcripción del identificador de este informe y del recuento de hallazgos abiertos en la entrada del release (`spec.md:201`, `:412`; `docs/Flujo_de_Trabajo_Git.md:16`).

**Declaración expresa.** Este informe no aprueba compuerta alguna: no declara G1, G2, G3, G4, G5 ni G6, no emite línea de aprobación y no sustituye la firma del propietario. Un resultado favorable del validador o de las suites no acredita la conformidad del régimen ni autoriza por sí solo un release.

## 8. Hoja de ruta

| Acción | Cierra | Bloque | Dependencia |
|---|---|---|---|
| Registrar la fila 41 de `docs/sdd/auditoria_final_v0_7_2.md` en la tabla de inventario del corpus antes de la integración | Requisito del corpus (`docs/sdd/README.md:75`) | corrección del `documenter` | Escritura del `documenter`; desbloquea el check `verify` |
| Crear la rama `release/v0-7-2`, empaquetar los seis artefactos de `§15` y transcribir el identificador de este informe y el recuento de hallazgos abiertos en la entrada del release | Condición de `RF-015` y de `CA-016` | empaquetado | G5 verificada y decisión del propietario |
| Verificar G5 sobre el merge de la rama de empaquetado y eliminar la rama | Requisito de G5 | orquestador | Integración por Pull Request con `merge --no-ff` |
| Declarar G6 en la entrada del release y crear el tag anotado `v0.7.2` sobre el commit de merge publicado en `main` | Requisito de G6 | propietario y orquestador | G5 cumplida y este informe registrado |
| Retirar la integración `6b85789` de la fila T6 del ciclo reabierto y unificar las etiquetas T5 y T6 | `OBS-007` | corrección editorial del `planner` | Autorización del propietario |
| Añadir la viñeta de la reapertura al bloque `Unreleased` y declarar la lectura de la versión `0.9.3` | `OBS-008` | corrección editorial del `documenter` | Autorización del propietario |
| Estrechar la concesión mecánica del `reviewer` y del `auditor` o declarar su alcance en el propio archivo de rol | `OBS-006` | spec posterior | Decisión del propietario |

## 9. Limitaciones

- La ejecución de shell está denegada en esta sesión: no se ejecutaron `python tools\sdd\validate.py --all`, las dos suites, `git merge-base --is-ancestor`, `git cat-file`, `git tag -n`, `git rev-parse` ni `git verify-commit`. La evidencia de ejecución se transcribe de `specs/016-cierre-auditoria-v0-7-1/validation_report.md:17-21` y `:109`, y del reflog de `.git/logs/HEAD`.
- La ancestría de `main` en `dev` se sostiene con cuatro hechos verificados: `main` vale `da30c86` y no se movió después (`.git/logs/refs/heads/main:13`), `dev` vale `104496d`, `dev` integró `main` por `merge` en un commit anterior (`.git/logs/refs/heads/dev:28`) y el corte anterior acreditó la misma relación (`docs/sdd/auditoria_previa_v0_7_2.md:180`). No se re-ejecutó la comprobación de ancestría.
- Los padres del merge `6b85789` se citan de `validation_report.md:88` y los de la integración `104496d` no constan en el corpus; no se leyeron los objetos de commit, de modo que la forma de dos padres no se re-verificó en esta sesión.
- El estado de firma de los commits `8c8a2a3`, `58d67d5`, `9042ae6` y `d0126ce` no se re-verificó contra `docs/sdd/firmantes_autorizados`; se transcribe la verificación que declaran el inventario, el reporte y el acta (`docs/sdd/inventario_hallazgos.md:160-162`; `validation_report.md:21`).
- La verificación de la evidencia transcrita por los artefactos no forma parte de las comprobaciones del validador (`docs/sdd/PROTOCOLO_OPERATIVO.md:343`); este informe contrasta la cita con el archivo y la línea y no acredita la ejecución histórica que cada fila declara.
- Las 79 filas en `cerrado` se examinaron por forma, estado, cita y evidencia de cierre, sin reconstruir la ejecución de los seis informes de origen ni verificar una por una las firmas de los commits que las cerraron.
- Al añadirse este informe, el corpus pasa de 40 a 41 archivos y la tabla de inventario conserva 40 filas; mientras el `documenter` no escriba la fila 41, `test_inventario_del_corpus` devuelve el mensaje «docs/sdd/README.md no registra la fila de docs/sdd/auditoria_final_v0_7_2.md» y el check `verify` queda en rojo. El efecto es el declarado por `docs/sdd/README.md:75` y no altera el corte auditado.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | «17 comprobaciones ejecutadas, 0 entradas `[ERROR]` y código de salida 0» en el corte, y código 0 después de la integración `6b85789` | `specs/016-cierre-auditoria-v0-7-1/validation_report.md:20`, `:109` |
| B | «Ran 222 tests in 1.269s» y «OK»; «Ran 48 tests in 21.088s» y «OK» | `specs/016-cierre-auditoria-v0-7-1/validation_report.md:17-18` |
| C | `dev` = `104496d`; `main` = `da30c86`; `refs/tags/v0.7.1` = `4d0473b`; sin `release/*` en `.git/refs/heads` ni en `.git/refs/remotes/origin` | `.git/refs/heads/dev`, `.git/refs/heads/main`, `.git/refs/tags/v0.7.1`, `.git/refs/heads`, `.git/refs/remotes/origin` |
| D | `8c8a2a3` «docs(sdd): fijar la interpretacion de la regla de autorreferencia»; `58d67d5` «fix(sdd): corregir la autorreferencia y el alcance del inventario»; `6b85789` y `104496d` por avance rápido desde `origin/dev`; creación de la rama `docs/auditoria-final-v0-7-2` desde `dev` en `104496d` | `.git/logs/HEAD:295-304` |
| E | 85 filas: 82 en §4 y 3 en §8; 79 en `cerrado`, 6 en `cerrado por ratificación`, 0 abiertas | Lectura de `docs/sdd/inventario_hallazgos.md:34-115`, `:160-162` |
| F | §16 declara la prohibición de autorreferencia en `:378`, la regla citada en `:382`, el cálculo del veredicto en `:384-393` y la prohibición de G6 sin informe en `:395` | `docs/sdd/PROTOCOLO_OPERATIVO.md` |
| G | Acta de interpretación: prohibición acotada al veredicto y al recuento anticipados; la condición de estado no se alcanza; `AUD-111` cerrado por ratificación | `docs/sdd/ratificacion_interpretacion.md:16-36` |
| H | Los cuatro bloques de `SPEC-016` no nombran valores del veredicto y expresan 0 hallazgos abiertos y 0 observaciones sin tratamiento | `specs/016-cierre-auditoria-v0-7-1/spec.md:201`, `:247`, `:297`, `:412` |
| I | `MEMORY.md` en `validated`, `spec.md` en `validated` con `release: ""`, `specs/INDEX.md:22` en `validated` con guion en la columna del release | Lectura contrastada de las tres rutas |
| J | 40 filas de inventario frente a 40 archivos del corpus antes de este informe: 32 en `docs/sdd/`, 7 en `docs/sdd/plantillas/` y `docs/sdd/firmantes_autorizados` | Lectura de `docs/sdd/README.md:28-69` |
| K | «FAILED» esperado de `test_inventario_del_corpus` con este informe presente: «docs/sdd/README.md no registra la fila de docs/sdd/auditoria_final_v0_7_2.md»; se cierra con la fila 41 que escribe el `documenter` | `tools/sdd/tests/test_agent_permissions.py:1768-1777`; `python -m unittest discover -s tools\sdd\tests -q` |
| L | Estado de firma no re-verificado: `8c8a2a3`, `58d67d5`, `9042ae6` y `d0126ce`; se transcribe la verificación declarada por el inventario y el reporte | `git show --no-patch --format='%G?'` (no ejecutado); `docs/sdd/inventario_hallazgos.md:160-162`; `validation_report.md:21` |
