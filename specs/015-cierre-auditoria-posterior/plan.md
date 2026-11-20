# Plan técnico — SPEC-015

*Artefacto de rango 6: diseño de las siete correcciones de `SPEC-015`, con las decisiones `DEC-001` a `DEC-007`, los contratos `C-1` a `C-8`, la estrategia de testing y la matriz de cobertura de los 11 requisitos funcionales, los 4 requisitos no funcionales y los 8 casos borde.*

## Referencias

- `spec.md`: `SPEC-015`, versión 0.2.0, estado `clarified`, con 11 requisitos funcionales, 4 requisitos no funcionales, 8 casos borde y 11 criterios de aceptación; G1 firmada por `Agent Sebaxtian` (2026-11-20).
- `clarify.md`: `SPEC-015`, cerrado con `AMB-001` a `AMB-011` resueltos, 13 parches aplicados a `spec.md` y las 10 decisiones de negocio que fijan el alcance de las correcciones.
- `docs/sdd/auditoria_posterior_v0_7_0.md`: veredicto global `NO CONFORME` sobre el commit `13e85e2`, con 10 observaciones vigentes —`AUD-087`, `AUD-088` y `AUD-090` de severidad Alta; `AUD-089`, `AUD-076`, `AUD-057` y `AUD-099` de severidad Media; `AUD-039`, `AUD-068` y `AUD-100` de severidad Baja— y el recuento de 10 de 10 abiertas.
- `docs/constitution.md`: rangos de los documentos, prohibición de modificar requisitos para ajustarlos al código, prohibición de reescribir historia publicada y registro de G6 fuera de `spec.md`.
- `AGENTS.md`: cadena `RF/CB → CA → T → evidencia`, seis roles, matriz del orquestador, línea de registro de aprobación y prohibición de declarar compuertas.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §12 en la línea 294 —bloque de documentos de raíz con la remisión al bloque B3— y §13 en la línea 302 —condición de G5 con el check `verify` exigible en las dos ramas—.
- `docs/Flujo_de_Trabajo_Git.md`: norma de rango 4, con la tabla de compuertas en las líneas 9 a 14, la prohibición de mover el tag publicado en la línea 301, el procedimiento de release en las líneas 319 a 392, las tres verificaciones de release en la línea 394, el registro append-only en la línea 398, el check exigible en las líneas 448 y 462 y la excepción de ramas de release en la línea 466.
- `specs/013-cierre-reauditoria-conformidad/validation_report.md`: matriz de 40 filas en `PASADO`, dictamen `CONVERGIDO`, nota de desviación de la línea 80 sobre `RNF-001` y nota de cierre de las líneas 96 a 114 con la evidencia diferida de `RNF-001` y de `CA-015`.
- `specs/014-cierre-observaciones-finales/validation_report.md`: sección de cierre de integración de las líneas 52 a 57 con `Merge: b018ab8`, `Release: v0.7.0` y la viñeta de G5, sin transcripción del resultado de G6.
- `specs/014-cierre-observaciones-finales/spec.md`: estado `released`, versión 0.8.0, campo `release` con `v0.7.0`, fila `0.8.0` del historial de cambios en la línea 217 y fila T7 de la línea 230 con el tag pendiente de la firma de G6.
- `CHANGELOG.md`: viñeta de la línea 24 con el rango `AUD-038` a `AUD-102`, línea de registro de G6 en la línea 44, historial de releases de las líneas 209 a 223 y párrafo de la línea 225 en tiempo futuro.
- `docs/sdd/README.md`: tabla de inventario de las líneas 28 a 63, con la fila 34 del informe posterior en la línea 63.
- `tools/sdd/validate.py`: `C-02` y `C-10` en las líneas 778 a 861 —entrada del release, tag anotado, `INDEX.md` y cita de auditoría del incremento MINOR—, y `C-18` en las líneas 1182 a 1205 —incremento PATCH con fila de motivo—.
- `tools/sdd/tests/test_agent_permissions.py`: suite del mecanismo de control con 6 clases declaradas y los detectores `problemas_del_flujo`, `problemas_de_documentacion` y `problemas_del_cierre` como antecedente de forma.
- `docs/sdd/plantillas/plan.md` y `docs/sdd/plantillas/tasks.md`: forma de este artefacto y del de tareas.

## Naturaleza del entregable

La spec produce una combinación declarada de normativa, registro documental, registro de spec y pruebas:

- Norma de rango 4: `docs/Flujo_de_Trabajo_Git.md`, con el procedimiento de corrección de un tag publicado, el alcance cerrado de la rama de empaquetado, la firma obligatoria posterior a la publicación y la fila G5 alineada con el check `verify`.
- Norma de rango 3: `docs/sdd/PROTOCOLO_OPERATIVO.md`, con la remisión de §12 sustituida por la referencia a la matriz de permisos vigente.
- Registro de spec de rango 6: la nota append-only del resultado de G6 en el reporte de `SPEC-014`, la nota de cierre corregida en el reporte de `SPEC-013` y la fila T7 con la regularización PATCH de `SPEC-014`.
- Registro de cambios de raíz: `CHANGELOG.md`, con el párrafo en tiempo pasado y la enumeración de los 16 identificadores asignados.
- Pruebas de rango 7: las comprobaciones de `tools/sdd/tests/test_agent_permissions.py` sobre el procedimiento de tag, el alcance del empaquetado, la firma posterior, la alineación de compuertas, las dos notas, la fila T7 y el registro de cambios, con pareja positiva y negativa.
- El contrato de esta spec en `specs/015-cierre-auditoria-posterior/`.

La publicación del release `v0.7.1` es el acto de cierre de la spec y corresponde al propietario: el tag, la línea de G6 y el informe de la auditoría de conformidad se registran con su firma y no con la de un agente.

No produce scripts `.bat`, no modifica `src/`, `models/`, `bin/`, `llama.cpp/` ni `.github/`, no altera la matriz ni el dictamen de `SPEC-013` y de `SPEC-014`, no modifica `docs/sdd/auditoria_posterior_v0_7_0.md` y no declara compuerta alguna. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen ni la autorización de un release.

## Arquitectura

### Componentes, responsabilidad y límite

| Componente | Artefacto | Responsabilidad | Límite | Rol que escribe |
|---|---|---|---|---|
| Procedimiento de tag | `docs/Flujo_de_Trabajo_Git.md`, sección «Sincronización y tag» | Declara las 3 condiciones habilitantes, el registro del identificador anterior y la excepción del caso `v0.7.0` con el tag anterior `ad739a0` y el destino `5a3af48` | No mueve, elimina ni recrea un tag; no reescribe la regla de la línea 301 | `documenter`, como delegado explícito del propietario |
| Alcance del empaquetado | `docs/Flujo_de_Trabajo_Git.md`, paso 3 del procedimiento de release y excepción de ramas de release | Declara los 4 artefactos admitidos, la exigencia de spec previa o fix previo para cualquier otra ruta y la excepción del commit `5da6df6` | No habilita código, pruebas, configuración ni documentación operativa en la rama de empaquetado | `documenter`, como delegado explícito del propietario |
| Firma posterior a la publicación | `docs/Flujo_de_Trabajo_Git.md`, sección de registro de la verificación | Declara 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados` por cada modificación posterior a la publicación y la transcripción del estado de firma | No declara aprobada una modificación sin firma verificable; no sustituye la firma del propietario | `documenter`, como delegado explícito del propietario |
| Alineación de compuertas | `docs/Flujo_de_Trabajo_Git.md`, fila G5 de la tabla de compuertas | Incorpora el check `verify` exigible con `strict: true` en `main` y en `dev` a la condición de G5 | No altera la regla de bloqueo de la línea 462 ni la evidencia exigida | `documenter`, como delegado explícito del propietario |
| Remisión de §12 | `docs/sdd/PROTOCOLO_OPERATIVO.md`, bloque de documentos de raíz | Sustituye la remisión al bloque B3 por la referencia a la matriz de permisos vigente y a su formalización ejecutada | No reescribe la tabla de roles ni el rango del documento | `documenter`, como delegado explícito del propietario |
| Nota de G6 | `specs/014-cierre-observaciones-finales/validation_report.md` | Transcribe las 3 verificaciones de release del release publicado | Append-only: no altera matriz, dictamen, estado ni sección de cierre | `reviewer`, por delegación escrita del propietario |
| Nota de cierre corregida | `specs/013-cierre-reauditoria-conformidad/validation_report.md` | Declara el valor efectivo de `RNF-001` y de `CA-015` y el cierre de las 7 observaciones del informe final | Append-only: no reescribe la fila, la matriz, el dictamen ni la nota precedente | `reviewer`, por delegación escrita del propietario |
| Regularización de `SPEC-014` | `specs/014-cierre-observaciones-finales/spec.md` | Sustituye la evidencia de la fila T7 e incrementa la versión a 0.8.1 con 1 fila de motivo | No renumera la spec, no reescribe requisitos ni criterios y no altera `status` ni `release` | `planner` |
| Registro de cambios | `CHANGELOG.md`, viñeta del release `v0.7.0` y párrafo posterior al historial | Declara en tiempo pasado la línea de G6 y la creación del tag y enumera los 16 identificadores asignados | No modifica la entrada protegida del release sin commit firmado del propietario; la corrección se registra en la entrada del release `v0.7.1` | `documenter`, como delegado explícito del propietario |
| Suite de comprobaciones | `tools/sdd/tests/test_agent_permissions.py` | Ejerce la estructura del procedimiento de tag, el alcance del empaquetado, la firma posterior, la alineación de compuertas, las dos notas, la fila T7 y el registro de cambios con pareja positiva y negativa | Solo lee texto del repositorio; no crea tags, no consulta el remoto y no escribe archivos versionados | `coder` |
| Contrato de la feature | `specs/015-cierre-auditoria-posterior/` | Declara requisitos, decisiones, tareas y evidencia | No reabre el contenido funcional de `SPEC-013` ni de `SPEC-014` | `planner` |
| Release de cierre | `CHANGELOG.md`, `specs/INDEX.md`, `specs/015-cierre-auditoria-posterior/spec.md` y el tag `v0.7.1` | Publica el release PATCH con la verificación de G5 registrada, el tag anotado, la línea de G6 firmada y el informe de auditoría registrado | No mueve el tag `v0.7.0`; no publica sin la auditoría registrada | propietario, con la verificación del orquestador |

### Orden de las correcciones

El orden evita que una comprobación nueva declare en rojo un artefacto que aún no se corrigió y deja la publicación al final, porque su condición incluye el cierre anterior:

1. Pruebas en rojo de las 7 comprobaciones —tag, alcance, firma, alineación de compuertas, notas, fila T7 y registro de cambios— y del cierre de las 10 observaciones.
2. Procedimiento de corrección de tag en el rango 4, con su prueba en verde.
3. Alcance cerrado de la rama de empaquetado en el rango 4.
4. Firma obligatoria posterior a la publicación en el rango 4.
5. Fila G5 con el check `verify` y remisión de §12 sustituida.
6. Correcciones de `CHANGELOG.md`.
7. Nota append-only del resultado de G6 en el reporte de `SPEC-014`.
8. Nota de cierre corregida en el reporte de `SPEC-013`.
9. Fila T7 y regularización PATCH de `SPEC-014`.
10. Paquete de cierre de las 10 observaciones con artefacto y evidencia por observación.
11. Regresión agregada, límite de 300 segundos y conservación de las specs publicadas.
12. Publicación del release `v0.7.1` con la verificación de G5 registrada y el informe de auditoría registrado.

La nota de cierre de `SPEC-013` se escribe después de las correcciones de `CHANGELOG.md` y del reporte de `SPEC-014` porque declara el cierre de las 7 observaciones del informe final, que depende de esos artefactos. La fila T7 se corrige antes del paquete de cierre porque su evidencia cita el release publicado y la línea de G6 firmada.

### Procedimiento de trabajo

- Las pruebas se escriben en rojo antes de la corrección que las satisface y declaran su pareja positiva y su pareja negativa, según `DEC-006`.
- Los documentos de rango 3 y 4 y el registro de cambios siguen validación-first: se transcribe la afirmación vigente, se contrasta con el informe posterior y solo después se escribe el texto de reemplazo.
- Las notas de los dos reportes y la fila T7 siguen la regla append-only de `DEC-004` y `DEC-005`: se verifica la ausencia de consumidores del tag `v0.7.0` y la conservación de matriz y dictamen antes de escribir.
- Cada ejecución de prueba, de validador o de comando Git se transcribe en el campo `Evidencia` de su tarea al cerrarla; ninguna tarea declara un resultado supuesto.

## Contratos

### C-1. Procedimiento de corrección de un tag publicado

| Condición habilitante | Evidencia exigida | Efecto de su ausencia |
|---|---|---|
| Autorización escrita del propietario | registro escrito con la fecha y el alcance de la corrección | la corrección no se ejecuta y la observación queda como deuda aceptada |
| Registro del identificador anterior | identificador completo del tag anterior y del destino nuevo en el informe de cierre | la corrección no se registra y la observación permanece vigente |
| Ausencia de consumidores del tag | declaración del propietario de que ningún consumidor depende del tag | la corrección se tramita por un release PATCH nuevo con su propio tag |

- Las 3 condiciones se exigen de forma simultánea y la corrección se ejecuta antes de que un consumidor dependa del tag.
- El número de tags publicados que se mueven, eliminan o reutilizan sin las 3 condiciones es 0.
- La excepción registrada del release `v0.7.0` declara el tag anterior `ad739a0` y el destino vigente `5a3af48`, la deuda aceptada y la prohibición de moverlo de nuevo.
- Una corrección intentada sin autorización escrita no produce movimiento de tag y deja la observación como deuda aceptada del release publicado.

### C-2. Alcance cerrado de la rama de empaquetado

| Artefacto | Modificación admitida |
|---|---|
| `CHANGELOG.md` | entrada del release e historial de releases |
| `specs/INDEX.md` | fila de la spec publicada |
| Frontmatter de una spec publicada | campos `status`, `version`, `updated` y `release` |
| Línea `Release:` de un reporte de validación publicado | tag del release |

- El número de artefactos admitidos es 4 y el de rutas fuera del alcance admitidas sin spec previa o fix previo es 0.
- La modificación de una ruta distinta de las 4 exige una spec previa o un fix previo con su tarea declarada, y la verificación registra un error que nombra la ruta.
- El alcance se declara en el paso 3 del procedimiento de release y en la excepción de ramas de release de la norma de rango 4.
- La excepción del empaquetado de `v0.7.0` declara el commit `5da6df6` con 18 archivos, la regularización de la comprobación afectada y su fila en el registro de cambios.

### C-3. Firma obligatoria posterior a la publicación

| Elemento | Regla |
|---|---|
| Sujeto | cada modificación de una entrada publicada de `CHANGELOG.md` o de un artefacto de una spec publicada |
| Medio | 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados` |
| Evidencia | estado de firma del commit transcrito en la evidencia del cierre |
| Modificación sin firma verificable | el estado de firma se registra y la modificación no se declara válida |
| Alcance de la firma del empaquetado | no se extiende a las correcciones posteriores a la publicación |

- El número de modificaciones posteriores a la publicación admitidas sin firma verificable es 0.
- El estado de firma se transcribe con el resultado de la comprobación de firma del commit y la huella de la clave.
- Las tareas `T-013`, `T-014`, `T-015` y `T-016` tocan una entrada publicada o un artefacto de una spec publicada, de modo que su contenido se registra en 1 commit firmado por el propietario sobre el texto que prepara el rol declarado.

### C-4. Notas append-only de los dos reportes

| Soporte | Contenido obligatorio | Prohibición |
|---|---|---|
| Reporte de `SPEC-014` | Tag anotado verificado con su commit objetivo, `specs/INDEX.md` y `CHANGELOG.md` actualizados, y línea de G6 firmada | No declara compuerta, no altera matriz ni dictamen, no cambia el estado `released` y no elimina la nota precedente |
| Reporte de `SPEC-013` | Valor efectivo de `RNF-001` y de `CA-015` que la evidencia sostiene, cierre de las 7 observaciones del informe final con 6 cerradas con artefacto y la séptima cerrada por esta spec | No reescribe la fila publicada, no altera las 40 filas de la matriz ni el dictamen `CONVERGIDO` y no declara superado un criterio sin evidencia |

- La nota nueva se añade a continuación de las secciones precedentes y el número de líneas retiradas del reporte es 0.
- El recuento de filas de matriz y de dictámenes alterados por esta spec es 0, según `RNF-001`.

### C-5. Fila T7 y regularización de `SPEC-014`

| Elemento | Valor exigido |
|---|---|
| Evidencia de la fila T7 | release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada |
| Transiciones nuevas en el historial | 0: se sustituye la evidencia de la fila existente |
| Versión | 0.8.1, con 1 incremento PATCH sobre 0.8.0 |
| Fila de motivo | fila nueva en el historial de cambios con la versión 0.8.1 y el motivo de regularización |
| Campos conservados | `status: released`, `release: "v0.7.0"`, requisitos y criterios de aceptación |
| Corrección que altere el destino o el identificador del release | se rechaza y el conflicto se registra en el reporte de esa spec |

### C-6. Correcciones de alineación

| Ubicación | Afirmación vigente | Texto exigido | Verificación |
|---|---|---|---|
| `docs/Flujo_de_Trabajo_Git.md:11` | condición de G5 sin el check `verify` | condición con el check `verify` exigible con `strict: true` en `main` y en `dev` | `test_fila_g5_incorpora_el_check_verify` |
| `docs/Flujo_de_Trabajo_Git.md:466` y paso 3 de la línea 336 | 3 artefactos de empaquetado | los 4 artefactos de `C-2` y la exigencia de spec previa o fix previo | `test_alcance_cerrado_de_cuatro_artefactos` |
| `docs/sdd/PROTOCOLO_OPERATIVO.md:294` | «La formalización de la allowlist de agentes para la raíz corresponde al bloque B3» | referencia a la matriz de permisos vigente y a su formalización ejecutada | `test_remision_b3_retirada` |
| `CHANGELOG.md:225` | línea de G6 y tag en tiempo futuro | línea de G6 registrada y tag `v0.7.0` creado, en tiempo pasado | `test_vineta_enumera_los_dieciseis_identificadores` |
| `CHANGELOG.md:24` | rango `AUD-038` a `AUD-102` | los 16 identificadores asignados que la entrada cita | `test_rango_con_numero_no_asignado_es_error` |

- El número de afirmaciones que dejan la definición de G5 más estrecha que la regla de la línea 462 es 0.
- El número de rangos que incluyen un identificador no asignado es 0.
- La regla de bloqueo de la línea 462 se conserva sin cambio.

### C-7. Pareja de pruebas por comprobación

| Comprobación | Prueba positiva | Prueba negativa |
|---|---|---|
| Procedimiento de corrección de tag | `test_procedimiento_de_correccion_completo` | `test_correccion_sin_autorizacion_es_error` |
| Alcance cerrado del empaquetado | `test_alcance_cerrado_de_cuatro_artefactos` | `test_ruta_fuera_del_alcance_es_error` |
| Firma posterior a la publicación | `test_modificacion_publicada_firmada` | `test_modificacion_sin_firma_es_error` |
| Fila G5 con el check `verify` | `test_fila_g5_incorpora_el_check_verify` | `test_fila_g5_sin_check_es_error` |
| Remisión de §12 | `test_remision_b3_retirada` | `test_remision_b3_conservada_es_error` |
| Nota de G6 en el reporte de `SPEC-014` | `test_nota_de_g6_en_reporte_publicado` | `test_nota_sin_verificaciones_de_release_es_error` |
| Nota de cierre del reporte de `SPEC-013` | `test_nota_de_cierre_corregida_en_spec_013` | `test_nota_con_siete_observaciones_sin_cierre_es_error` |
| Fila T7 y regularización | `test_fila_t7_declara_el_release_publicado` | `test_fila_t7_con_tag_pendiente_es_error` |
| Registro de cambios | `test_vineta_enumera_los_dieciseis_identificadores` | `test_rango_con_numero_no_asignado_es_error` |
| Cierre de las 10 observaciones | `test_cierre_de_las_diez_observaciones` | `test_observacion_sin_artefacto_sigue_vigente` |

Cada comprobación declara 1 prueba positiva y 1 prueba negativa, y la negativa demuestra que el detector discrimina sobre texto sintético que conserva el defecto.

### C-8. Cierre por observación

| Observación | Severidad | Artefacto que la cierra | Evidencia de la verificación | Requisito |
|---|---|---|---|---|
| `AUD-087` | Alta | Procedimiento de corrección de tag de `docs/Flujo_de_Trabajo_Git.md` con la excepción `ad739a0` → `5a3af48` | `test_procedimiento_de_correccion_completo` en verde, 3 condiciones exigidas y 2 identificadores transcritos | `RF-001` |
| `AUD-088` | Alta | Alcance cerrado de 4 artefactos en `docs/Flujo_de_Trabajo_Git.md` con la excepción del commit `5da6df6` | `test_alcance_cerrado_de_cuatro_artefactos` en verde y 0 rutas fuera del alcance admitidas sin spec previa | `RF-002` |
| `AUD-090` | Alta | Firma obligatoria posterior a la publicación en `docs/Flujo_de_Trabajo_Git.md` | `test_modificacion_publicada_firmada` en verde y 0 modificaciones publicadas admitidas sin firma | `RF-003` |
| `AUD-089` | Media | Nota append-only de las 3 verificaciones de release en el reporte de `SPEC-014` | `test_nota_de_g6_en_reporte_publicado` en verde y 0 líneas retiradas del reporte | `RF-004` |
| `AUD-076` | Media | Nota de cierre corregida en el reporte de `SPEC-013` con el valor efectivo de las 2 filas | `test_nota_de_cierre_corregida_en_spec_013` en verde, 40 filas en `PASADO` y dictamen `CONVERGIDO` conservados | `RF-005` |
| `AUD-057` | Media | Fila T7 de `SPEC-014` con el release publicado y versión 0.8.1 | `test_fila_t7_declara_el_release_publicado` en verde y `python tools\sdd\validate.py --spec SPEC-014` con código 0 | `RF-006` |
| `AUD-039` | Baja | Fila G5 de `docs/Flujo_de_Trabajo_Git.md` con el check `verify` | `test_fila_g5_incorpora_el_check_verify` en verde y contraste con la línea 462 | `RF-007` |
| `AUD-068` | Baja | §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md` sin la remisión al bloque B3 | `test_remision_b3_retirada` en verde y 0 remisiones al bloque B3 en el documento | `RF-008` |
| `AUD-100` | Baja | Párrafo y viñeta de `CHANGELOG.md` corregidos | `test_vineta_enumera_los_dieciseis_identificadores` en verde y 16 identificadores enumerados | `RF-009` |
| `AUD-099` | Media | Fila 34 del informe en la tabla de inventario de `docs/sdd/README.md:63`, ya existente | `test_inventario_del_corpus` en verde sobre el corpus y ausencia de modificación de `docs/sdd/README.md` | `RF-010` |

El recuento de cierre es 10 de 10, sin doble cómputo. Una observación sin artefacto de cierre no se declara cerrada: se registra en estado vigente con su causa.

## Decisiones técnicas

### DEC-001

- **Decisión:** la norma de rango 4 declara 1 procedimiento de corrección de un tag publicado con 3 condiciones habilitantes simultáneas —autorización escrita del propietario, registro del identificador anterior y ausencia de consumidores—, exige el registro del identificador completo del tag anterior y del destino nuevo, fija que la corrección se ejecuta antes de que un consumidor dependa del tag y cierra el caso `v0.7.0` como excepción con el tag anterior `ad739a0` y el destino vigente `5a3af48`.
- **Justificación:** `RF-001`, `CB-001`, `CB-002` y `CA-001` fijan las 3 condiciones y el registro, y `AUD-087` acredita que el artefacto publicado cambió después de la publicación por el desplazamiento de su etiqueta. La línea 301 del rango 4 prohíbe mover, eliminar o reutilizar un tag publicado y las líneas 274 a 278 exigen verificar su ausencia antes de crearlo; sin procedimiento escrito, la prohibición deja la corrección de un defecto de publicación sin cauce y la práctica observada contradice la norma.
- **Alternativas descartadas:** declarar el tag intocable sin procedimiento, porque deja `AUD-087` sin artefacto de cierre y prohíbe cualquier corrección futura sin declarar el cauce que la admitiría; admitir el movimiento con la sola autorización del propietario, porque reproduce el defecto auditado con otra redacción y `CB-002` exige desplazar la corrección a un release PATCH cuando existe un consumidor; sustituir el procedimiento por una nota de errata en el registro de cambios, porque la nota no fija cómo se ejecuta una corrección ni registra el identificador anterior que `CA-001` exige.

### DEC-002

- **Decisión:** la rama `release/vX-Y-Z` se limita a 4 artefactos —`CHANGELOG.md`, `specs/INDEX.md`, el frontmatter de las specs publicadas y la línea `Release:` de un reporte de validación publicado—, y cualquier ruta distinta exige una spec previa o un fix previo con su tarea declarada. El alcance se declara en el paso 3 del procedimiento de release y en la excepción de ramas de release, y la verificación registra un error que nombra la ruta fuera del alcance.
- **Justificación:** `RF-002`, `CB-003` y `CA-002` fijan la lista cerrada y el error, y `AUD-088` acredita que el commit `5da6df6` modificó 18 archivos, entre ellos `MEMORY.md` y una suite de pruebas, sin tarea que lo declarara. La lista vigente de la línea 466 enumera 3 artefactos y omite la línea `Release:` que el propio procedimiento escribe en el reporte de la spec publicada, de modo que el empaquetado conforme quedaría fuera de su alcance declarado.
- **Alternativas descartadas:** conservar los 3 artefactos, porque la línea `Release:` del reporte publicado quedaría prohibida en la rama que el procedimiento obliga a escribirla y la norma se contradiría a sí misma; admitir «documentación autorizada por el propietario», porque abre el alcance que `AUD-088` registró como defecto y `CB-003` exige un error que nombre la ruta; confiar la restricción a la revisión del Pull Request sin comprobación, porque `CA-002` exige que la ruta fuera del alcance produzca un error verificable y no una recomendación.

### DEC-003

- **Decisión:** cada modificación posterior a la publicación de una entrada de release o de un artefacto de una spec publicada consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`, y el estado de firma del commit se transcribe en la evidencia del cierre. Una modificación sin firma verificable registra su estado de firma y no se declara válida. La regla se declara en la norma de rango 4 y no se satisface con la firma del commit de empaquetado.
- **Justificación:** `RF-003`, `CB-004` y `CA-003` fijan la firma por modificación y la transcripción del estado, y `AUD-090` acredita que la cita de auditoría de la entrada protegida fue introducida por el commit `494db2e`, cuyo estado de firma es `N`, después de la publicación. La tabla de protección de la línea 447 declara `require_signed_commits: false`, de modo que la firma exigida por §11 para la sección protegida no se acredita en el remoto y la norma debe declararla en el procedimiento.
- **Alternativas descartadas:** exigir firma solo en el commit de empaquetado original, porque es exactamente la condición que permitió `AUD-090` y deja sin firma cada corrección posterior; activar `require_signed_commits: true` en las dos ramas, porque amplía la exigencia a cada commit de implementación, contradice la fila 447 y no es el objeto de la observación; aceptar la firma del release en lugar de la firma del commit de la modificación, porque la firma del propietario sobre el tag no acredita la autoría del cambio posterior.

### DEC-004

- **Decisión:** las dos correcciones de reportes publicados se hacen mediante 1 nota append-only por reporte. La del reporte de `SPEC-014` transcribe las 3 verificaciones de release. La del reporte de `SPEC-013` declara el valor efectivo de `RNF-001` y de `CA-015` y el cierre de las 7 observaciones del informe final, con 6 cerradas con artefacto y la séptima cerrada por esta spec. Las dos conservan matriz, dictamen, estado y nota precedente y no declaran compuerta.
- **Justificación:** `RF-004`, `RF-005`, `CB-005`, `CA-004` y `CA-005` fijan la forma y la conservación, y `RNF-001` fija en 0 el número de filas de matriz y de dictámenes alterados. `AUD-089` acredita que el reporte de `SPEC-014` no transcribe el resultado de G6 y `AUD-076` que las filas `RNF-001` y `CA-015` de `SPEC-013` figuran en `PASADO` mientras la nota de cierre transcribe que su evidencia no acredita el valor literal del criterio. La línea 398 del rango 4 y §13 del protocolo admiten el registro posterior a G4 en modalidad append-only, de modo que la evidencia queda transcrita y contrastable sin reescribir el criterio publicado.
- **Alternativas descartadas:** corregir las filas de `RNF-001` y de `CA-015` a un valor distinto de `PASADO`, porque altera la matriz publicada y `RNF-001` exige 0 filas alteradas; reabrir `SPEC-013` para declarar el cambio como requisito nuevo, porque devuelve la spec a `draft` y contradice el fuera de alcance de esta spec; registrar el resultado de G6 solo en la entrada del release de `CHANGELOG.md`, porque esa entrada es la sección protegida y el soporte declarado de la verificación es el reporte de la spec publicada.

### DEC-005

- **Decisión:** la fila T7 de `SPEC-014` conserva su posición y su destino `released`, y su evidencia se sustituye por el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada. La spec incrementa su versión de 0.8.0 a 0.8.1 con 1 fila de motivo de regularización en el historial de cambios, sin transición nueva, sin renumeración y sin cambio de requisitos, criterios ni campo `release`. Una corrección que altere el destino o el identificador del release se rechaza y el conflicto se registra en el reporte.
- **Justificación:** `RF-006`, `CB-006` y `CA-006` fijan la evidencia, el incremento PATCH y la conservación, y `AUD-057` acredita que la fila declara el tag pendiente de la firma de G6 mientras el release está publicado y la línea de registro existe. La regla de versionado admite PATCH para una corrección editorial que no cambia requisitos y `C-18` del validador exige que la fila de regularización declare la misma versión del frontmatter.
- **Alternativas descartadas:** añadir una transición T8 nueva, porque el destino `released` ya está registrado y una fila adicional declararía 2 transiciones donde el protocolo admite 1; incrementar MINOR a 0.9.0, porque no hay etapa de contrato nueva y el cambio es de evidencia; corregir la fila sin incrementar la versión, porque la modificación de un artefacto de una spec publicada quedaría sin rastro de versión y `CA-006` exige la fila de motivo.

### DEC-006

- **Decisión:** las 10 comprobaciones nuevas se implementan en `tools/sdd/tests/test_agent_permissions.py` como detectores puros sobre el texto de los artefactos, con 1 prueba positiva sobre el artefacto del repositorio y 1 prueba negativa sobre un texto sintético que conserva el defecto. La prueba negativa nombra el valor en conflicto, la condición ausente o la ruta fuera del alcance.
- **Justificación:** `CA-001` a `CA-008` excluyen acreditar una comprobación por su sola presencia en el artefacto, y `DEC-006` de la clarificación fija la pareja. Una prueba que solo lee el texto real no demuestra que el detector discrimina, y las 10 comprobaciones corrigen defectos que hoy pasan inadvertidos: ausencia de las 3 condiciones, ruta fuera del alcance, modificación sin firma, fila G5 incompleta, remisión a un bloque cerrado, nota sin las 3 verificaciones, nota con recuento de 7 observaciones en conflicto, fila T7 con tag pendiente, rango con número no asignado y observación declarada cerrada sin artefacto.
- **Alternativas descartadas:** 1 sola prueba por comprobación sobre el artefacto real, porque no distingue un detector correcto de uno que acepta cualquier entrada; pruebas que creen un tag o consulten el remoto, porque añaden efectos remotos y credenciales a una suite que se declara no destructiva; pruebas que escriban archivos versionados, porque el texto sintético basta para ejercer la discriminación y la suite no debe modificar el árbol.

### DEC-007

- **Decisión:** el cierre de las 10 observaciones se declara en 2 soportes: el paquete de cierre de `tasks.md`, con 1 fila por observación con su artefacto, su evidencia y el requisito que la cubre, y el informe de la auditoría de conformidad del release `v0.7.1`, que declara 10 de 10 cerradas. `AUD-099` se declara cerrada por la fila 34 del inventario de `docs/sdd/README.md`, que esta spec no modifica. El release `v0.7.1` se publica como incremento PATCH por el procedimiento de la norma de rango 4, con la verificación de G5 registrada, el tag anotado de mensaje `Release v0.7.1`, la línea de G6 firmada, `specs/INDEX.md` y `CHANGELOG.md` actualizados y el informe de auditoría registrado, sin mover el tag `v0.7.0`.
- **Justificación:** `RF-010`, `RF-011`, `CB-007`, `CB-008`, `CA-008`, `CA-009` y `RNF-002` fijan el recuento, los 2 soportes y la forma del tag. `AMB-010` fija que `AUD-099` ya está cerrada por la fila del inventario y que no se computa dos veces, y `AMB-011` fija el release PATCH como cauce del cierre. El contenido de la spec no añade funcionalidad: corrige procedimiento, registro y documentación, de modo que el incremento corresponde a PATCH.
- **Alternativas descartadas:** declarar el cierre de las 10 observaciones solo en `tasks.md`, porque el informe de la auditoría de `v0.7.1` es el soporte que `RF-010` exige y el recuento quedaría sin el contraste posterior; publicar `v0.8.0`, porque no hay funcionalidad nueva que justifique el incremento MINOR y la norma lo reserva para funcionalidades compatibles; mover el tag `v0.7.0` para corregir su contenido, porque `RF-001` lo prohíbe, el fuera de alcance lo excluye y su registro como deuda aceptada es el cierre de `AUD-087`.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Procedimiento de tag | `test_procedimiento_de_correccion_completo` y `test_correccion_sin_autorizacion_es_error` | El procedimiento declara las 3 condiciones, los 2 identificadores de la excepción y la ejecución previa al consumidor; un texto sin autorización escrita produce error con la condición ausente y no declara la corrección admitida |
| Alcance del empaquetado | `test_alcance_cerrado_de_cuatro_artefactos` y `test_ruta_fuera_del_alcance_es_error` | El alcance declara 4 artefactos y 0 rutas fuera del alcance admitidas; un texto que admite `MEMORY.md` produce error que nombra la ruta |
| Firma posterior | `test_modificacion_publicada_firmada` y `test_modificacion_sin_firma_es_error` | La regla exige 1 commit firmado por modificación publicada y la transcripción del estado de firma; un texto que acepta una modificación sin firma produce error con el estado registrado |
| Alineación de compuertas | `test_fila_g5_incorpora_el_check_verify`, `test_fila_g5_sin_check_es_error`, `test_remision_b3_retirada` y `test_remision_b3_conservada_es_error` | La fila G5 nombra el check `verify` con `strict: true` en las 2 ramas y la regla de bloqueo se conserva; §12 no remite al bloque B3; los textos sintéticos que conservan la omisión producen error con la fila o la remisión nombrada |
| Notas append-only | `test_nota_de_g6_en_reporte_publicado`, `test_nota_de_cierre_corregida_en_spec_013` y `test_nota_con_siete_observaciones_sin_cierre_es_error` | La primera nota transcribe las 3 verificaciones de release; la segunda declara el valor efectivo de las 2 filas y el cierre de las 7 observaciones; una nota con 6 de 7 cerradas produce error con el recuento en conflicto; las 40 filas, el dictamen y el estado de `SPEC-013` conservan su contenido |
| Fila T7 y registro | `test_fila_t7_declara_el_release_publicado`, `test_fila_t7_con_tag_pendiente_es_error`, `test_vineta_enumera_los_dieciseis_identificadores` y `test_rango_con_numero_no_asignado_es_error` | La fila T7 declara el release publicado y la versión 0.8.1 con su fila de motivo; un texto con el tag pendiente produce error; la viñeta enumera 16 identificadores y un rango con número no asignado produce error con el identificador nombrado |
| Cierre de observaciones | `test_cierre_de_las_diez_observaciones` y `test_observacion_sin_artefacto_sigue_vigente` | Las 10 observaciones cuentan con artefacto y evidencia y el recuento declarado es 10 de 10; una observación sin artefacto se registra vigente con su causa y no se cuenta como cerrada |
| Regresión de la suite | `python -m unittest discover -s tools\sdd\tests -q` | Código 0, sin fallos, con las 10 comprobaciones nuevas y sus parejas en verde |
| Regresión de Git | `python -m unittest discover -s tools\git\tests -q` | Código 0 con las 48 pruebas en verde |
| Validador agregado | `python tools\sdd\validate.py --all` | Código 0 en 300 segundos o menos, sin entradas `[ERROR]`, con las advertencias de legado declaradas |
| Validador por spec | `python tools\sdd\validate.py --spec SPEC-013` y `python tools\sdd\validate.py --spec SPEC-014` | Código 0 en las dos ejecuciones, con las 40 filas de matriz y el dictamen de `SPEC-013` conservados y el estado `released` de `SPEC-014` sin cambio |
| Conservación documental | `git diff --numstat` de los dos reportes y de `docs/sdd/README.md` | 0 líneas retiradas en las notas nuevas y 0 líneas modificadas en `docs/sdd/README.md` |
| Tag del release | `git cat-file -t v0.7.1`, `git tag -n`, `git rev-parse v0.7.1^{commit}`, `git merge-base --is-ancestor main dev` y `git rev-parse v0.7.0^{commit}` | `tag` como tipo, mensaje `Release v0.7.1`, commit objetivo de `main` ancestro de `dev`, y `v0.7.0` con su commit objetivo en `5a3af48` |
| Firma de la modificación publicada | `git log -1 --format=%G?` y la verificación de la clave contra `docs/sdd/firmantes_autorizados` | Estado de firma verificable y huella de una clave autorizada en el commit de la corrección |

- El fallo de una comprobación se atribuye a su prueba por clase, y la ejecución de las 2 suites se transcribe por separado antes de la ejecución agregada.
- No se produce script `.bat`, de modo que no aplica la declaración previa de comando, salida y métricas de la validación-first de scripts.
- La ejecución real del flujo en GitHub y la creación del tag quedan fuera de la suite: las pruebas leen texto del repositorio y el tag se verifica con comandos Git en la evidencia de su tarea.
- La salida de cada ejecución se transcribe en el campo `Evidencia` de la tarea que la ejecuta y en el reporte de validación de esta spec.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | `C-1` y `docs/Flujo_de_Trabajo_Git.md`, sección «Sincronización y tag» | `test_procedimiento_de_correccion_completo` y `test_correccion_sin_autorizacion_es_error` |
| `RF-002` | `C-2`, paso 3 del procedimiento de release y excepción de ramas de release | `test_alcance_cerrado_de_cuatro_artefactos` y `test_ruta_fuera_del_alcance_es_error` |
| `RF-003` | `C-3` y sección de registro de la verificación del rango 4 | `test_modificacion_publicada_firmada` y `test_modificacion_sin_firma_es_error` |
| `RF-004` | `C-4` y reporte de `SPEC-014` | `test_nota_de_g6_en_reporte_publicado` y `test_nota_sin_verificaciones_de_release_es_error` |
| `RF-005` | `C-4` y reporte de `SPEC-013` | `test_nota_de_cierre_corregida_en_spec_013` y `test_nota_con_siete_observaciones_sin_cierre_es_error` |
| `RF-006` | `C-5` y `specs/014-cierre-observaciones-finales/spec.md` | `test_fila_t7_declara_el_release_publicado`, `test_fila_t7_con_tag_pendiente_es_error` y `python tools\sdd\validate.py --spec SPEC-014` |
| `RF-007` | `C-6` y fila G5 de la tabla de compuertas | `test_fila_g5_incorpora_el_check_verify` y `test_fila_g5_sin_check_es_error` |
| `RF-008` | `C-6` y §12 del protocolo | `test_remision_b3_retirada` y `test_remision_b3_conservada_es_error` |
| `RF-009` | `C-6` y `CHANGELOG.md` | `test_vineta_enumera_los_dieciseis_identificadores` y `test_rango_con_numero_no_asignado_es_error` |
| `RF-010` | `C-8` y el paquete de cierre de `tasks.md` | `test_cierre_de_las_diez_observaciones`, `test_observacion_sin_artefacto_sigue_vigente` y contraste de la tabla de `T-017` |
| `RF-011` | Procedimiento de release del rango 4 y la entrada de `CHANGELOG.md` del release | `git cat-file -t v0.7.1`, `git tag -n`, `git rev-parse v0.7.1^{commit}` y `python tools\sdd\validate.py --spec SPEC-015 --gate G6` |
| `RNF-001` | `C-4`, `C-5` y los dos reportes | `git diff --numstat` de ambos reportes: 0 líneas retiradas y 0 filas de matriz alteradas |
| `RNF-002` | Tag `v0.7.1` del release de cierre | `git cat-file -t`, mensaje del tag, `git rev-parse v0.7.1^{commit}` y `git merge-base --is-ancestor main dev` |
| `RNF-003` | Validador agregado | Tiempo medido de `python tools\sdd\validate.py --all`, con umbral de 300 segundos |
| `RNF-004` | Specs publicadas no corregidas | `git diff --numstat` por spec y recuento de requisitos renumerados igual a 0 |
| `CB-001` | `C-1` y la primera condición habilitante | `test_correccion_sin_autorizacion_es_error` con la deuda aceptada declarada |
| `CB-002` | `C-1` y la tercera condición habilitante | `test_procedimiento_de_correccion_completo` con la remisión al release PATCH nuevo |
| `CB-003` | `C-2` y el error de ruta fuera del alcance | `test_ruta_fuera_del_alcance_es_error` con la ruta nombrada |
| `CB-004` | `C-3` y la transcripción del estado de firma | `test_modificacion_sin_firma_es_error` con el estado de firma registrado |
| `CB-005` | `C-4` y la nota precedente del reporte de `SPEC-014` | `test_nota_de_g6_en_reporte_publicado` con 2 notas consecutivas |
| `CB-006` | `C-5` y el destino `released` de la fila T7 | `test_fila_t7_declara_el_release_publicado` con el destino y el campo `release` conservados |
| `CB-007` | `RF-011` y la comprobación de existencia del tag | Lectura de la salida de `git rev-parse --verify --quiet refs/tags/v0.7.1` en la evidencia de `T-019` |
| `CB-008` | `C-8` y el recuento de cierre | `test_observacion_sin_artefacto_sigue_vigente` con la causa vigente registrada |

Las 11 filas de requisitos funcionales, las 4 de requisitos no funcionales y las 8 de casos borde declaran 1 verificación o más, y ninguna fila queda sin instrumento asociado.
