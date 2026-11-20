# Informe de auditoría — estado integrado de `dev` previo al release v0.7.2

*Plantilla de rango 5: norma de forma del informe de auditoría. Rol ejecutor: `auditor`, implementado en `.opencode/agents/auditor.md`, con lectura de la base completa y escritura limitada a este informe.*

- **Fecha:** 2026-11-20 (UTC).
- **Alcance:** base normativa v2 (constitución, `AGENTS.md`, protocolo operativo, flujo Git, siete plantillas e índice del corpus), specs `SPEC-001` a `SPEC-016`, validador `tools/sdd/validate.py`, suite del mecanismo `tools/sdd/tests`, suite de las herramientas de Git `tools/git/tests`, agentes de `.opencode/`, flujo de integración continua, reglas de protección de ramas, registros Git locales y registro de cambios, con corte en el commit `c520244` de `dev`.
- **Objeto:** emitir el veredicto del estado integrado en `dev` previo al release `v0.7.2`, calcular el veredicto desde `docs/sdd/inventario_hallazgos.md`, contrastarlo con el declarado y determinar si la condición de `RF-015` de `SPEC-016` se satisface.
- **Carácter:** evidencia de la auditoría de conformidad; no fija reglas, no aprueba compuertas, no emite línea de aprobación y no sustituye la verificación del propietario.

## 1. Ficha de reproducibilidad

| Campo | Valor |
|---|---|
| Commit auditado | `c52024416bdf626467fff35883542b379b6b4946` (`git rev-parse dev`) |
| Rama | `docs/auditoria-previa-v0-7-2`, creada desde `dev` en `c520244` (`git branch --show-current`) |
| Fecha de corte | 2026-11-20 |
| Releases de referencia | `v0.7.0`: objeto de tag con mensaje `Release v0.7.0` y commit objetivo `5a3af48`. `v0.7.1`: objeto de tag con mensaje `Release v0.7.1` y commit objetivo `da30c86`, igual a `main` |
| Validador ejecutado | `python tools\sdd\validate.py --all`: 17 comprobaciones ejecutadas, 0 entradas `[ERROR]`, código de salida 0; las advertencias corresponden a la cláusula de legado de `SPEC-001` a `SPEC-009` |
| Suites ejecutadas | `python -m unittest discover -s tools\sdd\tests -q`: «Ran 222 tests in 1.268s» y «OK» en el corte, antes de añadir este informe; el anexo K transcribe la ejecución posterior. `python -m unittest discover -s tools\git\tests -q`: «Ran 48 tests in 20.420s» y «OK» |
| Entorno | Windows 11 (`win32`); lista blanca del rol: `git status`, `log`, `show`, `diff`, `rev-parse`, `branch`, `merge-base`, `ls-remote` y `verify-commit`, además del validador y de `unittest` |
| Rol ejecutor | `auditor` |

**Procedimiento.** Cuatro pasos. Primero, lectura íntegra de la base normativa de rangos 1 a 5, de los artefactos de `SPEC-016` y de los informes de auditoría previos. Segundo, lectura de las 82 filas de `docs/sdd/inventario_hallazgos.md` con verificación de la forma de la cita, del vocabulario del estado y del recuento, y cálculo del veredicto con la precedencia de `RF-013`. Tercero, contraste de los siete puntos del régimen nuevo: inventario completo, regla citada por hallazgo, ausencia de autorreferencia, seis artefactos de empaquetado, destino del tag en la fila T7, ratificación firmada y auditoría previa al release. Cuarto, examen de las once dimensiones con la evidencia transcrita en §10.

## 2. Base normativa e inventario

La jerarquía consta de siete rangos y una categoría sin rango, declarada de forma coincidente en `docs/constitution.md:48-59` y en `docs/sdd/README.md:15-24`. Cada documento de la base declara su rango y su carácter en el encabezado (`docs/sdd/PROTOCOLO_OPERATIVO.md:3`; `docs/Flujo_de_Trabajo_Git.md:3`; `docs/sdd/plantillas/informe_auditoria.md:3`).

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

**Corpus.** La tabla de inventario de `docs/sdd/README.md:28-67` declara 38 filas de datos y el árbol del corte contiene 38 archivos: 31 en `docs/sdd/` y 7 en `docs/sdd/plantillas/`. Las filas 36, 37 y 38 registran `docs/sdd/inventario_hallazgos.md`, `docs/sdd/firmantes_autorizados` y `docs/sdd/ratificacion_historica.md` (`docs/sdd/README.md:65-67`). Este informe añade un archivo 39 que en el corte carece de fila; la fila la escribe el rol `documenter` antes de la integración (`docs/sdd/PROTOCOLO_OPERATIVO.md:300`; `docs/sdd/plantillas/informe_auditoria.md:24`), y mientras falte, `docs/sdd/README.md:72-73` lo califica como defecto y la prueba `test_inventario_del_corpus` deja el check `verify` en rojo con el mensaje «docs/sdd/README.md no registra la fila de docs/sdd/auditoria_previa_v0_7_2.md» (anexo K).

**Inventario de hallazgos.** `docs/sdd/inventario_hallazgos.md:33-114` porta 82 filas para 82 identificadores `AUD-001` a `AUD-110`, con los ocho campos de `RF-011`. El recuento de estados es 77 en `cerrado` y 5 en `cerrado por ratificación` (`AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053`), 0 en `parcial`, 0 en `vigente` y 0 en `cerrado por exención`. El anexo de `docs/sdd/inventario_hallazgos.md:141-145` declara 0 observaciones y 0 tratamientos, y `docs/sdd/inventario_hallazgos.md:149` declara el veredicto `CONFORME`. La comprobación `C-19` del validador contrasta los 82 identificadores de los cinco informes con las 82 filas y no registra diferencia.

## 3. Criterio y escalas

**Criterio.** Cada afirmación se sostiene con evidencia citada por ruta y línea, por identificador de commit o por salida transcrita. Una afirmación de cumplimiento exige el artefacto y su ubicación; una de incumplimiento exige la norma y la práctica observada. La falta de evidencia produce `NO VERIFICABLE` y nunca presunción de cumplimiento.

**Regla citada.** Cada hallazgo cita la regla que incumple con la forma `ruta §capítulo:línea`, conforme a `docs/sdd/PROTOCOLO_OPERATIVO.md §16:382`. El juicio que no alcanza una regla de los rangos 1 o 3 se registra como observación, queda fuera del recuento y no computa como hallazgo abierto.

Escala de veredicto (`docs/sdd/plantillas/informe_auditoria.md:32-40`): `CONFORME`, `PARCIAL`, `NO CONFORME`, `NO VERIFICABLE` y `NO APLICA`.

Escala de severidad (`docs/sdd/plantillas/informe_auditoria.md:42-49`): `Crítica` afecta la validez de una compuerta o de la base; `Alta` rompe una regla normativa sin invalidar la compuerta; `Media` produce divergencia entre documentos de distinto rango; `Baja` es un defecto de forma, de redacción o de cita.

**Numeración.** Este informe no asigna `AUD-NNN`. El espacio se reserva a los hallazgos con fila en el inventario (`docs/sdd/PROTOCOLO_OPERATIVO.md:216`) y el rol de auditoría no escribe filas (`docs/sdd/PROTOCOLO_OPERATIVO.md:300`). Los hallazgos que emite se registran como `H-01` a `H-03`, sin número reservado, y las observaciones como `OBS-NNN`; la fila de cada `H-NN` corresponde al `documenter` antes de la integración.

## 4. Matriz de dimensiones

| Dimensión | Objeto evaluado | Veredicto | Evidencia principal | Hallazgos |
|---|---|---|---|---|
| D1 | Autoridad normativa, vigencia y aplicabilidad | `CONFORME` | `docs/constitution.md:48-59`, `:61-66`; `docs/sdd/README.md:15-24`, `:28-67` | Ninguno vigente |
| D2 | Ciclo de siete etapas y estado resultante | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:72-132`; `specs/016-cierre-auditoria-v0-7-1/spec.md:4`, `:438-444` | Ninguno vigente |
| D3 | Contratos de artefactos y forma de cada uno | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:167-218`; `docs/sdd/plantillas/informe_auditoria.md:9-107`; `specs/016-cierre-auditoria-v0-7-1/validation_report.md:23-65` | Ninguno vigente |
| D4 | Compuertas G1 a G6: condición, evidencia y verificación | `CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:136-145`; `docs/Flujo_de_Trabajo_Git.md:11-16`; `specs/016-cierre-auditoria-v0-7-1/spec.md:418-419` | Ninguno vigente |
| D5 | Trazabilidad `RF/CB → CA → T → evidencia` | `CONFORME` | `specs/016-cierre-auditoria-v0-7-1/spec.md:312-412`; `specs/016-cierre-auditoria-v0-7-1/validation_report.md:23-79` | Ninguno vigente |
| D6 | Estados, transiciones e historial de transiciones | `PARCIAL` | `specs/016-cierre-auditoria-v0-7-1/spec.md:436-444`; `specs/014-cierre-observaciones-finales/spec.md:232`; `specs/015-cierre-auditoria-posterior/spec.md:293` | `OBS-004` |
| D7 | Roles y menor privilegio | `PARCIAL` | `docs/sdd/PROTOCOLO_OPERATIVO.md:284-300`; `.opencode/agents/reviewer.md:48`; `.opencode/agents/auditor.md:51` | `H-02` |
| D8 | Evidencia y verificación: existencia, suficiencia e independencia | `NO CONFORME` | `docs/sdd/PROTOCOLO_OPERATIVO.md:378`; `specs/016-cierre-auditoria-v0-7-1/spec.md:201`, `:404` | `H-01` |
| D9 | Integración Git y release | `CONFORME` | `docs/Flujo_de_Trabajo_Git.md:343-352`, `:412`, `:414`; `CHANGELOG.md:11-23`, `:41-49`; tags `v0.7.0` y `v0.7.1` | Ninguno vigente |
| D10 | Consistencia documental operativa | `PARCIAL` | `docs/sdd/README.md:28-67`; `MEMORY.md:13`; `specs/INDEX.md:22`; `CHANGELOG.md:15-23` | `H-03`, `OBS-001`, `OBS-002`, `OBS-003` |
| D11 | Integración continua: ejecución, alcance y exigibilidad | `CONFORME` | `.github/workflows/sdd.yml:1-31`; `tools/git/protection_rules/main.json:3-6`; `tools/git/protection_rules/dev.json:3-6` | Ninguno vigente |

El veredicto global no se obtiene de esta matriz sino del cálculo de `RF-013` sobre las filas del inventario; la diferencia entre ambos se declara en §7.

**Contraste del régimen nuevo.** Los siete puntos del régimen que `SPEC-016` introduce se contrastan con el corte `c520244`:

| Punto | Resultado | Evidencia |
|---|---|---|
| Inventario completo | `CONFORME` | 82 identificadores de los cinco informes frente a 82 filas (`docs/sdd/inventario_hallazgos.md:33-114`); `C-19` sin diferencia |
| Hallazgo con regla citada | `CONFORME` | Las 82 filas usan la forma `ruta §capítulo:línea`; `C-20` sin diferencia |
| Ausencia de autorreferencia en las specs | `NO CONFORME` | `H-01`: `RF-015` y `CA-016` de `SPEC-016` fijan el veredicto `CONFORME` de este informe, contra `docs/sdd/PROTOCOLO_OPERATIVO.md §16:378` |
| Seis artefactos de empaquetado | `CONFORME` | Tabla con claves `A1` a `A6` idéntica en `docs/sdd/PROTOCOLO_OPERATIVO.md:355-362` y en `docs/Flujo_de_Trabajo_Git.md:345-352`; `C-22` sin diferencia |
| Destino del tag en la fila T7 | `CONFORME` | `specs/014-cierre-observaciones-finales/spec.md:232` declara `5a3af48` con `5da6df6` como ancestro; `specs/015-cierre-auditoria-posterior/spec.md:293` declara `da30c86` con `f6f053a` como ancestro; `C-23` sin diferencia |
| Ratificación firmada | `CONFORME` | Acta en `docs/sdd/ratificacion_historica.md:16-31`; el commit `9042ae6` añade 39 líneas y retira 0, y devuelve `G` con la identidad del propietario |
| Auditoría previa al release | Presente, condición no satisfecha | Este informe se ejecuta sobre el estado integrado en `dev` (`docs/Flujo_de_Trabajo_Git.md:16`); el veredicto calculado es `CONFORME` y el estado auditado no satisface `RF-015` por `H-01` |

**Artefactos del último ciclo.** `9042ae6` incorpora el acta y concentra la ratificación; `d0126ce` concentra las correcciones de los artefactos publicados en un solo commit firmado con estado `G`, con 20 rutas, 1965 altas y 104 bajas, y las dos notas de autorreferencia de reportes publicados constan con 11 y 24 altas y 0 bajas; `79bcd83` integra `feat/cierre-auditoria-v0-7-1` en `dev` con dos padres; `c520244` integra la rama de cierre y es el corte de este informe.

## 5. Hallazgos

### H-01 — `SPEC-016` fija el veredicto `CONFORME` de esta auditoría

- **Dimensión:** D8.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Alta`.
- **Regla citada:** `docs/sdd/PROTOCOLO_OPERATIVO.md §16:378`.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:378`; `docs/sdd/plantillas/spec.md:80`; `specs/016-cierre-auditoria-v0-7-1/spec.md:201` (`RF-015`), `:207` (`RNF-001`), `:239` (`RNF-009`), `:404` (`CA-016`), `:410` (`CA-017`); `docs/sdd/inventario_hallazgos.md:113`; `tools/sdd/hallazgos.py:141-147`; `tools/sdd/validate.py:1432-1443`; corte `c520244` del 2026-11-20.
- **Descripción:** `§16` declara que ninguna spec fija el veredicto de una auditoría futura y que un requisito o un criterio no declara `CONFORME`, `PARCIAL`, `NO CONFORME` ni `NO VERIFICABLE`, y que el criterio que invoca una auditoría se limita a exigir la existencia del artefacto y la evidencia transcrita. `RF-015` de `SPEC-016` exige publicar el release `v0.7.2` «solo después de 1 auditoría de conformidad ejecutada sobre el estado integrado en dev que declare el veredicto `CONFORME`», y `CA-016` repite esa condición con el mismo valor. La auditoría que evalúa esa condición es este informe, emitido después de la aprobación G1 del 2026-11-21 y de la aprobación G4 del mismo día, de modo que el requisito fija la salida de un informe posterior a su aprobación. La contradicción es interna además de normativa: `RNF-001` declara que el número de requisitos y criterios de la spec que fijan el veredicto «DEBE ser 0», mientras `RF-015`, `RNF-009` y `CA-016` lo fijan, y `CA-017` acredita ese recuento en 0. La comprobación `C-24` no lo detecta porque `tools/sdd/hallazgos.py:141-147` solo activa el control cuando el bloque nombra un informe concreto por ruta, y `RF-015` no nombra ninguno. La fila `AUD-109` se cerró con la premisa de que ninguna spec fija el veredicto (`docs/sdd/inventario_hallazgos.md:113`); `RF-015` restablece la causa que esa fila declaraba cerrada.
- **Remediación:** sustituir en `RF-015` y en `CA-016` la exigencia del valor `CONFORME` por la exigencia de existencia del informe, de su veredicto calculado y de la evidencia transcrita, y trasladar la condición de publicación al rango 3 o al rango 4, que no están alcanzados por la prohibición de `§16`; ampliar después `C-24` para que detecte la forma sin referencia explícita y registrar el cambio con una spec aprobada.

### H-02 — El rol `reviewer` escribió en reportes de validación de specs publicadas

- **Dimensión:** D7.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Media`.
- **Regla citada:** `docs/sdd/PROTOCOLO_OPERATIVO.md §12:290`.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:290`, `:296`; `.opencode/agents/reviewer.md:48`; `specs/016-cierre-auditoria-v0-7-1/spec.md:87`; `specs/013-cierre-reauditoria-conformidad/validation_report.md:118`, `:128-137`; `specs/015-cierre-auditoria-posterior/validation_report.md:108`, `:106-115`; `git show --stat d0126ce`.
- **Descripción:** la matriz de `§12` concede al `reviewer` escritura sobre `validation_report.md` «de la spec en curso» y `§12:296` declara que un permiso no se extiende por analogía y que la ruta no declarada está denegada. La configuración del rol concede `specs/*/validation_report.md` sin límite de spec (`reviewer.md:48`), y las dos notas de autorreferencia de los reportes de `SPEC-013` y de `SPEC-015` se atribuyen a ese rol en documentos publicados y ya validados (`specs/016-cierre-auditoria-v0-7-1/spec.md:87` declara la delegación del propietario). La firma del commit `d0126ce` con estado `G` acredita la autoría del propietario sobre el acto, no la habilitación del rol para escribir una ruta que la matriz no le concede. La misma forma, sin uso observado, alcanza la concesión de `auditor.md:51`, que admite cualquier `docs/sdd/auditoria_*.md` y no solo el informe que el rol produce.
- **Remediación:** estrechar la concesión de `reviewer.md` a la spec en curso o declarar en `§12` del rango 3 que el propietario escribe esas notas en los reportes publicados y que el `reviewer` solo redacta el reporte de su propia spec; corregir la delegación de `specs/016-cierre-auditoria-v0-7-1/spec.md:87` en la spec que regularice el régimen.

### H-03 — `MEMORY.md` declara `SPEC-016` en `tasked` y atribuye ese estado al índice

- **Dimensión:** D10.
- **Veredicto:** `NO CONFORME`.
- **Severidad:** `Baja`.
- **Regla citada:** `docs/constitution.md §6:66`.
- **Evidencia:** `MEMORY.md:13`; `specs/016-cierre-auditoria-v0-7-1/spec.md:4`; `specs/INDEX.md:22`; `docs/sdd/README.md:24`.
- **Descripción:** `MEMORY.md:13` afirma que `SPEC-016` «consta en estado `tasked` … conforme a `specs/INDEX.md`», mientras el frontmatter de la spec declara `status: validated` y la fila 22 del índice declara `validated`. La categoría sin rango no fija reglas y su contradicción con un documento normativo se resuelve a favor del documento normativo, con la corrección aplicada en el documento sin rango; la frase citada agrava el defecto porque invoca como fuente un índice que declara el valor contrario.
- **Remediación:** actualizar `MEMORY.md:13` al estado `validated` y al release pendiente cuando el `documenter` cierre el ciclo, sin alterar el frontmatter de la spec ni la fila del índice.

### Observaciones

| N.º | Severidad | Observación | Tratamiento |
|---|---|---|---|
| `OBS-001` | `Baja` | La fila `AUD-108` de `docs/sdd/inventario_hallazgos.md:112` cita `specs/015-cierre-auditoria-posterior/spec.md:292` como evidencia de la fila T7 corregida; la línea 292 porta la transición T6 y la fila T7 corregida está en la línea 293. El cierre no cambia porque el artefacto existe una línea después, y la cita señala una línea que no porta el artefacto que declara. | Propuesta: corregir la cita a `:293` en la próxima edición del inventario, con registro de la corrección en `CHANGELOG.md`. Sin decisión del propietario en el corte. |
| `OBS-002` | `Baja` | `docs/Flujo_de_Trabajo_Git.md:235` describe la suite del mecanismo «con 187 pruebas», mientras la ejecución del corte devuelve «Ran 222 tests» y el propio reporte de `SPEC-016` transcribe 222. La cifra es descriptiva y no fija una regla, de modo que el defecto es de redacción y no de alineación normativa. | Propuesta: sustituir la cifra por una remisión a la ejecución de la suite o actualizarla a 222 en la corrección editorial siguiente. Sin decisión del propietario en el corte. |
| `OBS-003` | `Baja` | Las filas del historial de cambios y de transiciones de `SPEC-016` y la entrada del ciclo registran 2026-11-21 (`specs/016-cierre-auditoria-v0-7-1/spec.md:425-432`), mientras los commits que las introducen están sellados el 2026-11-20 entre las 11:48 y las 13:02 en la zona `-0500`. La fecha documental es un día posterior al sello del commit y no altera el corte. | Propuesta: declarar la zona horaria de las fechas documentales o alinearlas con el sello del commit en la corrección editorial siguiente. Sin decisión del propietario en el corte. |
| `OBS-004` | `Baja` | La fila T6 de `specs/016-cierre-auditoria-v0-7-1/spec.md:444` incluye la integración `79bcd83` como evidencia de la transición `implemented` a `validated`, y esa integración es posterior a la aprobación G4 del commit `3704b33`, que es uno de sus dos padres. La transición queda acreditada por el dictamen y por G4; la mención de un hecho posterior en su evidencia es un defecto de forma. | Propuesta: retirar la mención de la integración de la fila T6 y conservarla en la fila T7 al empaquetar el release, o dejarla con nota de orden temporal. Sin decisión del propietario en el corte. |

Las cuatro observaciones son de severidad `Baja` y no computan como hallazgo abierto ni impiden el veredicto calculado; su tratamiento queda propuesto y no registrado por el propietario.

## 6. Compuertas

Esta sección no emite veredicto de compuerta. Registra la evidencia observada y su límite, conforme a la prohibición de aprobar del rol de auditoría (`docs/constitution.md:77`; `docs/sdd/PROTOCOLO_OPERATIVO.md:278`).

| Compuerta | Evidencia observada | Límite de esta auditoría |
|---|---|---|
| G1 | Casilla G1 marcada en `specs/016-cierre-auditoria-v0-7-1/spec.md:418`, con el nombre del propietario y fecha 2026-11-21; el commit `b2edcfc` devuelve `G` con la identidad del propietario | La aprobación corresponde al propietario; este informe no la declara ni reproduce la línea de registro. `H-01` registra que el contrato aprobado incorporó después la forma que `§16:378` prohíbe |
| G4 | Línea de G4 en `specs/016-cierre-auditoria-v0-7-1/spec.md:419`; el commit `3704b33` devuelve `G`; dictamen `CONVERGIDO` con 37 de 37 filas en `specs/016-cierre-auditoria-v0-7-1/validation_report.md:76-79` | La aprobación corresponde al propietario; la matriz del reporte acredita el commit `e2ede7a` y no el estado integrado |
| G5 | Merge `79bcd83` con dos padres (`7992173` y `3704b33`); rama `feat/cierre-auditoria-v0-7-1` sin resultado en `git branch --list`; validador posterior sin `[ERROR]`; check `verify` exigible con `strict: true` en `main.json` y en `dev.json` | La verificación corresponde al orquestador y no constituye aprobación |
| G6 | El registro de cambios no porta entrada `v0.7.2` (`CHANGELOG.md:11-23`) y no existe tag del release en el corte | No emitido; la condición de `RF-015` se examina en §7 |

## 7. Veredicto global

**Veredicto calculado desde el inventario.** `CONFORME`. Recuento sobre las 82 filas: 0 hallazgos abiertos, 77 en `cerrado`, 5 en `cerrado por ratificación` y 0 en `cerrado por exención`, con 0 filas sin regla citada y 0 filas sin evidencia de cierre. La precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME` se aplica en ese orden y el primer valor que se cumple es `CONFORME`. El valor coincide con el declarado en `docs/sdd/inventario_hallazgos.md:149`, de modo que no hay diferencia que registrar entre el cálculo y la declaración del inventario.

**Veredicto del estado auditado.** `NO CONFORME` en el fondo. Este informe emite tres hallazgos abiertos —`H-01` de severidad `Alta`, `H-02` de severidad `Media` y `H-03` de severidad `Baja`— y ninguno consta en el inventario. La causa de la diferencia es estructural: `RF-011` limita el inventario a los 5 informes de auditoría de `docs/sdd/` y el rol de auditoría no escribe filas, de modo que el cálculo de `RF-013` solo alcanza las 82 filas heredadas y no puede computar los hallazgos de un sexto informe. La fila que sostiene la diferencia no existe; la sostiene la ausencia de fila para `H-01`, `H-02` y `H-03`, y se transcribe esa ausencia en lugar de una fila.

**Condición de `RF-015`.** No se satisface. `RF-015` prohíbe publicar el release con 1 hallazgo abierto de severidad `Crítica` o `Alta`; `H-01` es un hallazgo abierto de severidad `Alta`, emitido y sin artefacto de cierre, y `H-02` y `H-03` permanecen abiertos con severidad `Media` y `Baja`. El cálculo mecánico del inventario devuelve `CONFORME` porque no alcanza esos tres hallazgos, y ese resultado no se invoca como certificado de conformidad: la conjunción de `RF-013` y `RF-015` deja pasar una violación de `§16:378` sin registro, y esa es la brecha que este informe declara.

**Declaración expresa.** Este informe no aprueba compuerta alguna: no declara G1, G2, G3, G4, G5 ni G6, no emite línea de aprobación y no sustituye la firma del propietario. Un resultado favorable del validador o de las suites no acredita la conformidad del régimen ni autoriza un release.

## 8. Hoja de ruta

| Acción | Hallazgo que cierra | Bloque | Dependencia |
|---|---|---|---|
| Registrar la fila de `docs/sdd/auditoria_previa_v0_7_2.md` en la tabla de inventario del corpus antes de la integración | Requisito del corpus (`docs/sdd/README.md:72-73`) | corrección del `documenter` | Escritura del `documenter`; desbloquea el check `verify` |
| Regularizar `RF-015`, `RNF-009` y `CA-016` de `SPEC-016` para que no fijen el veredicto, y trasladar la condición de publicación al rango 3 o al rango 4 | `H-01` | spec posterior | Decisión del propietario y nueva aprobación G1 |
| Ampliar `C-24` para detectar la forma prohibida sin referencia explícita a un informe | `H-01` | corrección del mecanismo | Spec de la regularización de `H-01` |
| Estrechar la concesión de `.opencode/agents/reviewer.md:48` o declarar en `§12` la autoría del propietario sobre las notas de reportes publicados | `H-02` | spec posterior | Decisión del propietario |
| Actualizar `MEMORY.md:13` al estado `validated` y al release pendiente | `H-03` | corrección del `documenter` | Cierre del ciclo |
| Corregir la cita de la fila `AUD-108`, la cifra de pruebas del rango 4, la zona de las fechas documentales y la fila T6 de `SPEC-016` | `OBS-001` a `OBS-004` | corrección editorial o spec posterior | Autorización del propietario |

## 9. Limitaciones

- El inventario de hallazgos no admite filas de este informe: `RF-011` lo limita a los 5 informes de `docs/sdd/` y la escritura de filas corresponde al `documenter`, de modo que los tres hallazgos emitidos no computan en el cálculo de `RF-013` hasta que se registren.
- La verificación de la evidencia transcrita por los artefactos no forma parte de las comprobaciones del validador (`docs/sdd/PROTOCOLO_OPERATIVO.md:343`); este informe contrasta la cita con el archivo y la línea, y no acredita la ejecución histórica que cada fila declara.
- Las 82 filas cerradas se examinaron por forma, estado, cita y evidencia de cierre, sin reconstruir la ejecución de los cinco informes de origen ni verificar una por una las firmas de los commits que las cerraron.
- Las firmas de los commits `9042ae6`, `b2edcfc`, `3704b33` y `d0126ce` se verificaron con estado `G`; el commit de merge `79bcd83` devuelve `E`, que señala una firma que no se puede comprobar con las claves disponibles en el repositorio, y la firma no es exigible para un merge.
- No se ejecutó la comprobación de rama contra el remoto: la lista blanca del rol no incluye la consulta de referencias remotas, y la evidencia de eliminación se limita al listado local.

## 10. Anexos de evidencia

| Anexo | Contenido | Ruta o comando |
|---|---|---|
| A | «Comprobación de historial: punto de corte el tag anotado v0.7.1, 13 commits examinados»; 17 comprobaciones; 0 `[ERROR]`; código 0 | `python tools\sdd\validate.py --all` |
| B | «Ran 222 tests in 1.268s» y «OK» en el corte `c520244`, antes de añadir este informe | `python -m unittest discover -s tools\sdd\tests -q` |
| C | «Ran 48 tests in 20.420s» y «OK» | `python -m unittest discover -s tools\git\tests -q` |
| D | `9042ae6` → `G`, `sebaxtianrioss@gmail.com`; `b2edcfc` → `G`; `3704b33` → `G`; `d0126ce` → `G` | `git show --no-patch --format='%H%n%G?%n%GS'` sobre cada commit |
| E | `79bcd83` con padres `7992173` y `3704b33`; `c520244` como merge de la rama de cierre | `git show --no-patch --format='%H%n%P'` |
| F | `v0.7.1` es objeto de tipo `tag`, mensaje `Release v0.7.1`, commit objetivo `da30c86`; `v0.7.0` apunta a `5a3af48`; `git rev-parse main` = `da30c86` = `git merge-base main dev` | `git show --stat v0.7.1`; `git show --stat v0.7.0`; `git rev-parse main`; `git merge-base main dev` |
| G | Sin resultado en `git branch --list "release/*"` ni en `git branch --list "feat/cierre-auditoria-v0-7-1"` | `git branch --list` |
| H | 38 filas de inventario frente a 38 archivos en el corte; 82 filas de hallazgos, 77 `cerrado` y 5 `cerrado por ratificación`; 0 abiertos | Lectura de `docs/sdd/README.md:28-67` y de `docs/sdd/inventario_hallazgos.md:33-114` |
| I | `specs/016-cierre-auditoria-v0-7-1/spec.md:4` en `validated` y `specs/INDEX.md:22` en `validated` frente a `MEMORY.md:13` en `tasked` | Lectura contrastada de las tres rutas |
| J | Tabla de 6 artefactos con claves `A1` a `A6` en `docs/sdd/PROTOCOLO_OPERATIVO.md:355-362` y en `docs/Flujo_de_Trabajo_Git.md:345-352`; comprobación `C-22` sin hallazgo | Lectura contrastada y validador |
| K | «Ran 222 tests in 1.334s» y «FAILED (failures=1)»: `test_inventario_del_corpus` devuelve «docs/sdd/README.md no registra la fila de docs/sdd/auditoria_previa_v0_7_2.md». El fallo es el efecto declarado de este informe y se cierra con la fila 39 que escribe el `documenter` | `python -m unittest discover -s tools\sdd\tests -q` con este informe presente |
