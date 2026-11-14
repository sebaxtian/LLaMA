# Plan técnico — SPEC-012

*Artefacto de rango 6: diseño de la trazabilidad profunda verificable de `SPEC-012`, con las decisiones `DEC-NNN` y la matriz de cobertura de la spec.*

## Referencias

- `spec.md`: `SPEC-012`, versión 0.2.0, estado `clarified`, con nueve requisitos funcionales, ocho no funcionales, dieciocho casos borde y diecisiete criterios de aceptación.
- `clarify.md`: `SPEC-012`, cerrado con `AMB-001` a `AMB-008` resueltos, cuatro casos borde nuevos y once parches marcados.
- `docs/constitution.md`: principio de trazabilidad y prohibición de modificar requisitos para ajustarlos al código.
- `AGENTS.md`: cadena `RF/CB → CA → T → evidencia`, roles de escritura y prohibición de declarar compuertas.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §7 trazabilidad obligatoria, §8 contratos de artefactos, §9 versionado, §13 integración Git y §14 contrato del validador.
- `docs/sdd/plantillas/tasks.md` y `docs/sdd/plantillas/validation_report.md`: forma de los dos artefactos que la regularización toca.
- `docs/sdd/auditoria_cumplimiento_sdd.md`: bloque B4 y hallazgos `AUD-022`, `AUD-041`, `AUD-042`, `AUD-043`, `AUD-044` y `AUD-072`; tabla de integración y release de la sección 6.
- Estado observado del repositorio: `tools/sdd/validate.py` con las comprobaciones `C-01` a `C-13`, `tools/sdd/tests/test_validate.py` con 111 pruebas, siete specs publicadas con 48 tareas cerradas y siete reportes de validación sin sección de cierre.

## Naturaleza del entregable

La spec produce código de verificación, pruebas y regularización documental:

- `tools/sdd/validate.py`: cinco comprobaciones nuevas (`C-14` a `C-18`), la ejecución de las comprobaciones de historial dentro de la ejecución agregada y la degradación por ventana de legado.
- `tools/sdd/tests/test_validate.py` y `tools/sdd/tests/fixtures/trazabilidad/`: veinte pruebas nuevas con sus casos positivos y negativos.
- `specs/001-main-menu/tasks.md` a `specs/007-branch-protection/tasks.md`: 48 tareas con criterio de aceptación y evidencia, sin cambio de su contenido funcional.
- `specs/001-main-menu/validation_report.md` a `specs/007-branch-protection/validation_report.md`: sección `## Cierre de integración` con el merge y el tag de cada spec.
- `specs/012-trazabilidad-profunda-sdd/`: los artefactos de esta spec.

No produce scripts `.bat`, no modifica la base normativa, no edita las plantillas de rango 5 ni altera requisitos, casos borde, criterios, estimaciones o estados de las specs publicadas.

## Arquitectura

### Capas y responsabilidades

| Capa | Artefactos | Responsabilidad | Límite |
|---|---|---|---|
| Verificación del corpus | `tools/sdd/validate.py` | Evalúa el enlace `CA → T`, la evidencia, el cierre de integración y el versionado de la regularización | No escribe artefactos ni declara compuertas |
| Verificación del historial | `tools/sdd/validate.py` | Lee el historial local y exige la referencia `Spec:` en el commit de implementación | Solo lectura; no crea commits ni consulta el remoto |
| Pruebas del mecanismo | `tools/sdd/tests/test_validate.py`, `fixtures/trazabilidad/` | Ejercita cada comprobación con un caso positivo y un caso negativo | No modifica archivos versionados |
| Regularización de tareas | `specs/001-main-menu/tasks.md` a `specs/007-branch-protection/tasks.md` | Añade criterio de aceptación y evidencia a cada tarea | No altera campo previo ni estado |
| Regularización de reportes | Los siete `validation_report.md` publicados | Añade la sección de cierre con merge y tag | Append-only: no toca matriz ni dictamen |
| Contrato de la feature | `specs/012-trazabilidad-profunda-sdd/` | Declara requisitos, decisiones, tareas y evidencia | No reescribe las specs publicadas |

### Orden de las comprobaciones nuevas

| Comprobación | Entrada | Condición de error | Artefacto informado |
|---|---|---|---|
| `C-14` | Bloques `### T-NNN` y líneas `Cubre:` de `spec.md` | Tarea sin criterio, criterio inexistente, criterio de otra spec, criterio sin tarea o separación sin coma | `tasks.md` y `spec.md` |
| `C-15` | Campo `Evidencia` de cada tarea cerrada | Campo ausente, marcador sin sustituir, menos de 20 caracteres o marca de pendiente | `tasks.md` |
| `C-16` | Historial de la rama desde el punto de integración o los últimos 50 commits | Commit de implementación sin `Spec: SPEC-NNN` | Salida de la ejecución agregada |
| `C-17` | Sección `## Cierre de integración` del reporte | Sección ausente en `validated` o `released`, valor vacío o tag divergente del frontmatter y del índice | `validation_report.md` |
| `C-18` | Versión e historial de cambios de una spec regularizada | Falta el incremento PATCH o falta la fila de motivo | `spec.md` |

Las comprobaciones se ejecutan después de `C-04` y antes de `C-05`, de modo que una tarea sin criterio no oculte una tarea abierta. La severidad se resuelve con la función de emisión existente, que degrada a advertencia cuando la spec pertenece a la ventana de legado.

### Procedimiento del enlace `CA → T`

1. Se leen los identificadores `CA-NNN` declarados como encabezado en la sección de criterios de aceptación de `spec.md`.
2. Se lee el campo `Criterio de aceptación` de cada bloque `### T-NNN` de `tasks.md` y se separan los identificadores por coma.
3. Una tarea sin identificador produce error con su identificador.
4. Un identificador que no figura en el conjunto de la spec produce error con la tarea y el identificador.
5. Un identificador de la forma `CA-NNN` que pertenece a otro directorio de `specs/` produce error de referencia cruzada e informa la spec de destino.
6. Un identificador que figura en el texto del campo pero no separado por coma produce error de formato.
7. El criterio del conjunto de la spec que no figura en ninguna tarea produce error con su identificador.
8. El conjunto se calcula una vez por spec y el resultado se reutiliza en la comprobación del reporte.

### Procedimiento de la comprobación de evidencia

1. Se lee el bloque `### T-NNN` y se extrae la línea del campo `Evidencia`.
2. La tarea sin la casilla `Completada` marcada no se evalúa: una tarea abierta puede no declarar evidencia.
3. La tarea cerrada sin campo produce error.
4. El texto del campo se normaliza eliminando los espacios en blanco y comparándolo sin distinguir mayúsculas de minúsculas.
5. El texto normalizado con menos de 20 caracteres produce error.
6. El texto normalizado que coincide con la marca de pendiente, con la marca `N/A` o con un término vetado por el protocolo produce error.
7. El texto que supera las dos condiciones no produce hallazgo y su longitud se informa solo en la salida de depuración.

### Procedimiento de la comprobación de historial

1. Se resuelve el punto de integración de la rama actual contra `dev`; si no se resuelve, se usa el punto de integración contra `main`.
2. Se enumeran los commits posteriores a ese punto; si el punto no se resuelve, se enumeran los últimos 50 commits.
3. Se excluyen los commits de merge: no declaran la implementación de una tarea.
4. Se exige la cadena `Spec: SPEC-NNN` con un identificador existente en el cuerpo del commit.
5. El commit sin la cadena produce error con su identificador abreviado y el código de salida es 1.
6. La enumeración vacía se informa como comprobación no aplicable y no produce error.
7. El commit anterior al punto de integración no se examina y queda cubierto por la ventana de legado.

## Contratos

### Contrato del campo de criterio de aceptación

El campo ocupa una línea del bloque de tarea, entre `Requisitos cubiertos` y `Archivos`, con la forma `- **Criterio de aceptación:** ` seguida de uno o más identificadores entre comillas invertidas separados por `, `. La regularización conserva el orden del bloque y no reescribe las líneas existentes.

| Elemento | Forma | Regla |
|---|---|---|
| Etiqueta | `- **Criterio de aceptación:**` | Literal y con dos asteriscos a cada lado |
| Valor | `CA-001` | Identificador de tres dígitos entre comillas invertidas |
| Varios valores | `` `CA-001`, `CA-002` `` | Separados por coma y un espacio |
| Posición | Después de `Requisitos cubiertos` | El campo de evidencia va después de `Validación` |

### Contrato del campo de evidencia

| Elemento | Forma | Regla |
|---|---|---|
| Etiqueta | `- **Evidencia:**` | Literal, con dos asteriscos a cada lado |
| Valor | Texto transcrito de una línea | 20 caracteres o más tras eliminar espacios |
| Marca nula | `pendiente`, `N/A` o término vetado | Produce error en una tarea cerrada |
| Posición | Después de `Validación` y antes de la casilla | Conserva el orden de los ocho campos de la plantilla |

### Contrato de la sección de cierre de integración

El reporte de validación incorpora una sección de nivel 2 titulada `Cierre de integración` con dos líneas obligatorias y ninguna otra obligatoria:

| Línea | Forma | Obligatoriedad |
|---|---|---|
| `Merge:` | `Merge: <sha de 7 a 40 caracteres hexadecimales>` | Obligatoria en `validated` y en `released` |
| `Release:` | `Release: vMAJOR.MINOR.PATCH` | Obligatoria en `released`; en `validated` se admite vacía o con el tag previsto |

La sección se escribe al final del reporte, después del dictamen, y es append-only: no altera la matriz de trazabilidad ni el dictamen. El tag declarado se contrasta con el campo `release` del frontmatter y con la columna `Release` de la fila de la spec en `specs/INDEX.md`; una divergencia produce error con los dos valores.

### Contrato de la regularización histórica

| Spec | Versión actual | Versión regularizada | Commit de integración | Tag de release |
|---|---|---|---|---|
| `SPEC-001` | 0.1.0 | 0.1.1 | `753c3e5` | `v0.2.0` |
| `SPEC-002` | 0.12.0 | 0.12.1 | `ec6a063` | `v0.3.0` |
| `SPEC-003` | 0.6.0 | 0.6.1 | `39b27a2` | `v0.3.1` |
| `SPEC-004` | 0.9.0 | 0.9.1 | `b38ed6c` | `v0.4.0` |
| `SPEC-005` | 0.6.0 | 0.6.1 | `2781db5` | `v0.5.0` |
| `SPEC-006` | 0.6.0 | 0.6.1 | `0afc2ee` | `v0.5.1` |
| `SPEC-007` | 0.2.0 | 0.2.1 | `502c69d` | `v0.6.0` |

Cada spec regularizada recibe cinco cambios y ningún otro:

1. El campo `Criterio de aceptación` en cada tarea, con los criterios que la matriz de cobertura de su plan ya vincula al requisito de la tarea.
2. El campo `Evidencia` en cada tarea cerrada, con la referencia de la fila del reporte o de la línea del informe que la acredita.
3. La sección `## Cierre de integración` en el reporte, con el par de la tabla.
4. La fila de motivo en el historial de cambios, con la versión de la columna correspondiente.
5. El campo `version`, `updated` y el estado sin cambio.

La tarea publicada que no encuentra fuente verificable para su evidencia se registra como brecha en el reporte de esta spec y conserva el campo con la referencia disponible; no se redacta evidencia sin fuente.

## Decisiones técnicas

### DEC-001

- **Decisión:** el enlace `CA → T` se comprueba en las dos direcciones dentro de una sola comprobación (`C-14`): cada tarea declara al menos un criterio existente de su propia spec y cada criterio figura en al menos una tarea. La lista se separa por coma y el conjunto de criterios se calcula una vez desde `spec.md`.
- **Justificación:** `RF-001`, `RF-002`, `RF-003` y `CB-015` exigen la doble dirección y la forma de la lista; `AUD-022` y `AUD-041` registran que el eslabón no consta en el artefacto de tareas. Un cálculo único evita dos recorridos divergentes del mismo par de archivos.
- **Alternativas descartadas:** comprobar solo la dirección tarea a criterio, porque deja un criterio sin tarea sin detectar y `RF-003` quedaría sin verificación; y derivar el enlace por tránsito a través del requisito, porque reproduce el defecto de `AUD-041` y no acredita la declaración expresa.

### DEC-002

- **Decisión:** la evidencia se evalúa con tres condiciones acumulativas: campo presente, 20 caracteres o más tras eliminar los espacios en blanco y texto distinto de una marca de pendiente. Las marcas son `pendiente`, `N/A` y la lista de términos vetados que el validador ya declara. Una tarea sin la casilla marcada no se evalúa.
- **Justificación:** `RF-004`, `RNF-008` y `AMB-001` fijan el umbral y las marcas; `AUD-042` y `AUD-072` registran que el eslabón no tenía formato ni comprobación. Un umbral numérico es determinista y contrastable sin interpretar el contenido.
- **Alternativas descartadas:** exigir una salida de comando con formato reconocible, porque la evidencia histórica no siempre procede de una ejecución y la comprobación rechazaría registros válidos; y aceptar cualquier texto no vacío, porque un marcador sin sustituir pasaría como evidencia.

### DEC-003

- **Decisión:** la comprobación de `Spec:` se ejecuta dentro de `--all` y produce error, no advertencia. El alcance es el conjunto de commits posteriores al punto de integración de la rama contra `dev`, con retroceso a `main` y, en su defecto, a los últimos 50 commits. Los commits de merge se excluyen y la enumeración vacía se informa como no aplicable.
- **Justificación:** `RF-005`, `CB-005`, `CB-006` y `CB-018` fijan el error, el alcance y las dos exenciones; `AUD-043` registra que la comprobación era una advertencia y que `--all` ignoraba `--git`. El alcance por punto de integración evita convertir en error el historial anterior a la base v2.
- **Alternativas descartadas:** mantener la advertencia, porque no bloquea la integración y conserva el hallazgo; examinar los 50 commits recientes sin punto de integración, porque en una rama larga deja fuera los primeros commits del cambio; y exigir la cadena en cada commit del repositorio, porque el historial previo a la regla no la declara.

### DEC-004

- **Decisión:** el cierre de integración se declara en una sección de nivel 2 titulada `Cierre de integración` con las líneas `Merge:` y `Release:`, escrita después del dictamen y sin alterar la matriz. La sección es obligatoria en `validated` y en `released`; en `validated` la línea `Release:` se admite vacía. El tag se contrasta con el frontmatter y con el índice.
- **Justificación:** `RF-006`, `CB-007`, `CB-008`, `CB-009` y `CB-016` fijan la sección y las obligaciones; `AUD-044` registra que ningún artefacto declaraba el merge ni el tag. Una sección propia conserva la forma del reporte y permite comprobar la presencia sin analizar la prosa.
- **Alternativas descartadas:** declarar el merge y el tag en la sección de entorno, porque mezcla el entorno de validación con el cierre de integración; y declararlos en el historial de cambios de `spec.md`, porque el registro de versiones no es el registro de integración y la spec publicada no se reescribe.

### DEC-005

- **Decisión:** la regularización añade los campos de criterio y de evidencia y la sección de cierre, y conserva sin cambio el requisito, el caso borde, el criterio, el texto de la tarea, la estimación y el estado. La evidencia histórica se transcribe desde el reporte de validación o desde el informe de auditoría con su referencia; la tarea sin fuente verificable se declara como brecha y no se inventa evidencia.
- **Justificación:** `RF-007`, `CB-011`, `CB-013` y `AMB-008` fijan la frontera de la regularización; `RNF-004` exige el 100 % de los requisitos y criterios sin cambios. La prohibición de inventar evidencia evita convertir la regularización en una afirmación no respaldada.
- **Alternativas descartadas:** reescribir las tareas con un texto nuevo, porque altera el contrato publicado y vulnera la cláusula de legado; y declarar la evidencia con una referencia genérica al reporte, porque no permite reconstruir qué fila la acredita.

### DEC-006

- **Decisión:** la regularización incrementa la posición PATCH de cada spec y escribe una fila de motivo en su historial de cambios. La comprobación `C-18` verifica el incremento y la fila. Un cambio que alterara un requisito se tramita como MINOR en una spec nueva y no se aplica aquí.
- **Justificación:** `RF-007`, `CB-017` y `AMB-003` fijan el incremento y la fila; la regla de versionado del protocolo asigna PATCH a la corrección sin cambio de requisitos. La comprobación impide que la regularización quede sin registro de versión.
- **Alternativas descartadas:** conservar la versión, porque la spec publicada quedaría modificada sin registro; e incrementar MINOR, porque declara un cambio de contrato que no existe y habilita una revalidación que la regularización no requiere.

### DEC-007

- **Decisión:** la ventana de legado se limita a las cuatro specs `SPEC-008` a `SPEC-011` y se declara como constante del validador. Las comprobaciones nuevas degradan a advertencia en esas specs y son error desde `SPEC-012`. La ventana no se amplía sin spec posterior.
- **Justificación:** `RF-009`, `RNF-006`, `CB-010` y `AMB-002` fijan el conjunto y el límite; las cuatro specs están validadas sin release y sus reportes no declaran cierre de integración, de modo que exigirles el campo produciría un error sin objeto.
- **Alternativas descartadas:** mantener la ventana de legado existente sobre nueve specs, porque deja sin error las tres specs posteriores a la auditoría y reabre el defecto; y aplicar las comprobaciones nuevas a las cuatro specs, porque obligaría a regularizar specs fuera del alcance declarado.

### DEC-008

- **Decisión:** los siete pares de merge y tag de la regularización se toman de la tabla del contrato, que procede del informe de auditoría y del historial Git. La verificación previa de esa tabla se ejecuta con tres consultas de solo lectura sobre el historial local antes de escribir los reportes.
- **Justificación:** `RF-007`, `AMB-004` y la tabla de cobertura de la auditoría fijan los valores; una verificación previa evita transcribir un identificador que no exista en el historial.
- **Alternativas descartadas:** calcular el merge en el momento de la regularización, porque el merge de una spec publicada ya ocurrió y su búsqueda automática puede devolver otro merge de la misma rama; y dejar el campo sin valor hasta el release, porque la spec ya está publicada y el dato existe.

### DEC-009

- **Decisión:** cada comprobación nueva declara al menos una prueba positiva y una prueba negativa en `tools/sdd/tests/test_validate.py`, con fixtures nuevas bajo `tools/sdd/tests/fixtures/trazabilidad/`. Las pruebas usan solo la biblioteca estándar y el ejecutor del validador como proceso, sin red.
- **Justificación:** `RNF-005` y `CA-017` exigen la pareja por comprobación; la auditoría de `SPEC-010` y `SPEC-011` mostró que una comprobación sin caso negativo no acredita el rechazo. La ejecución como proceso comprueba además el código de salida.
- **Alternativas descartadas:** probar solo el caso positivo, porque no demuestra que la comprobación rechace la falta; e importar las funciones internas, porque acopla la prueba a la implementación y no verifica el contrato de salida.

### DEC-010

- **Decisión:** el `coder` escribe `tools/sdd/validate.py` y `tools/sdd/tests/`; el `planner` escribe la regularización de `specs/001-main-menu/` a `specs/007-branch-protection/` y los artefactos de esta spec; el orquestador verifica G2, G3 y G5 y no escribe artefactos de la regularización. La no regresión se acredita con la suite completa, el validador agregado y el contraste de contenido de las specs publicadas.
- **Justificación:** la matriz de roles del protocolo atribuye `specs/**` al `planner` y `tools/` al `coder`; `AMB-008` y `RNF-004` exigen que la regularización no altere el contenido funcional, y el contraste por artefacto lo demuestra.
- **Alternativas descartadas:** asignar la regularización al `coder`, porque la matriz limita su escritura en `specs/` al cierre de tareas y la regularización no cierra tarea alguna; y ejecutar la regularización con el orquestador, porque la escritura de artefactos de spec no figura en su permiso.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Enlace `CA → T` | `test_enlace_ca_tarea`, `test_ca_inexistente_en_tarea`, `test_ca_sin_tarea`, `test_ca_de_otra_spec`, `test_formato_de_varios_ca` | el caso positivo devuelve código 0 y cada caso negativo devuelve 1 con el identificador |
| Evidencia | `test_evidencia_valida`, `test_evidencia_corta`, `test_evidencia_con_marcador`, `test_tarea_abierta_sin_evidencia` | la evidencia de 20 caracteres o más no produce hallazgo; la corta, la marcada y la ausente producen error |
| Referencia del commit | `test_commit_con_spec`, `test_commit_sin_spec`, `test_alcance_de_commits`, `test_sin_commit_de_implementacion` | el commit sin la cadena produce error y código 1; el histórico y la enumeración vacía no producen error |
| Cierre de integración | `test_cierre_completo`, `test_cierre_ausente`, `test_cierre_sin_release`, `test_tag_divergente` | la sección completa no produce hallazgo; la ausencia y la divergencia producen error |
| Versionado de la regularización | `test_regularizacion_patch`, `test_regularizacion_sin_patch`, `test_legado_de_008_a_011` | el incremento con fila no produce hallazgo; la falta produce error; el legado produce advertencia |
| Regularización de las siete specs | Validador sobre cada spec de `SPEC-001` a `SPEC-007` | cero hallazgos de `C-14` a `C-18` en las siete |
| Contraste de contenido | Comparación de cada artefacto regularizado con su versión anterior | diferencia limitada a los campos añadidos, la sección de cierre, la versión y la fila de motivo |
| Tabla histórica | Tres consultas de solo lectura al historial local | siete merges existen y siete tags apuntan a su commit |
| Validador del corpus | `python tools\sdd\validate.py --all` | código de salida 0 y cero errores |
| Suite completa | `python -m unittest discover -s tools\sdd\tests -q` | 131 pruebas en verde: 111 vigentes y 20 nuevas |

- El validador se implementa con TDD: cada comprobación nace con su prueba negativa en rojo, se implementa el mínimo que la satisface y se cierra con la suite en verde.
- La regularización sigue validación-first: antes de escribir se ejecuta el validador sobre la spec publicada, se anota el hallazgo que la comprobación nueva produce y se verifica que desaparece tras añadir los campos.
- La tabla de merge y tag se verifica antes de transcribirla; un par que no se acredite contra el historial se registra como brecha y no se escribe.
- No se produce script `.bat`, de modo que no aplica la declaración previa de comando, salida y métricas de la validación-first de scripts.
- La salida de cada ejecución se transcribe en la evidencia de su tarea y en el reporte de validación de esta spec.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | `C-14` en `tools/sdd/validate.py` | `test_enlace_ca_tarea` y `test_formato_de_varios_ca` |
| `RF-002` | `C-14` en `tools/sdd/validate.py` | `test_ca_inexistente_en_tarea` y `test_ca_de_otra_spec` |
| `RF-003` | `C-14` en `tools/sdd/validate.py` | `test_ca_sin_tarea` |
| `RF-004` | `C-15` en `tools/sdd/validate.py` | `test_evidencia_valida`, `test_evidencia_corta` y `test_evidencia_con_marcador` |
| `RF-005` | `C-16` y ejecución agregada | `test_commit_con_spec`, `test_commit_sin_spec`, `test_alcance_de_commits` y `python tools\sdd\validate.py --all` |
| `RF-006` | `C-17` en `tools/sdd/validate.py` | `test_cierre_completo`, `test_cierre_ausente` y `test_cierre_sin_release` |
| `RF-007` | Regularización de `specs/001-main-menu/` a `specs/007-branch-protection/` | Validador sobre las siete specs y contraste de contenido por artefacto |
| `RF-008` | Exención de historial en `tools/sdd/validate.py` | `test_legado_de_008_a_011` y validador sobre `SPEC-001` a `SPEC-007` |
| `RF-009` | Constante de la ventana de legado | `test_legado_de_008_a_011` y validador sobre `SPEC-012` |
| `RNF-001` | Ejecución agregada | `python tools\sdd\validate.py --all` con tiempo medido en el reporte |
| `RNF-002` | `C-14` a `C-18` sin red | Ejecución en un entorno sin acceso a red y revisión de las llamadas del validador |
| `RNF-003` | Códigos de salida del validador | Pruebas positivas con código 0, negativas con código 1 y error de uso con código 2 |
| `RNF-004` | Contraste de contenido de las siete specs | Comparación con la versión anterior: solo campos añadidos, versión y fila de motivo |
| `RNF-005` | `tools/sdd/tests/test_validate.py` | Recuento de 20 pruebas nuevas con su pareja positiva y negativa |
| `RNF-006` | Constante de la ventana de legado | `test_legado_de_008_a_011` sobre las cuatro specs |
| `RNF-007` | Determinismo del validador | Dos ejecuciones sobre el mismo commit con salida idéntica |
| `RNF-008` | `C-15` en `tools/sdd/validate.py` | `test_evidencia_corta` y `test_evidencia_valida` |
| `CB-001` | `C-14` | `test_ca_inexistente_en_tarea` |
| `CB-002` | `C-14` | `test_ca_sin_tarea` |
| `CB-003` | `C-14` | `test_ca_de_otra_spec` |
| `CB-004` | `C-15` | `test_evidencia_con_marcador` y `test_evidencia_corta` |
| `CB-005` | `C-16` | `test_commit_sin_spec` con código de salida 1 |
| `CB-006` | `C-16` | `test_sin_commit_de_implementacion` |
| `CB-007` | `C-17` | `test_cierre_ausente` |
| `CB-008` | `C-17` | `test_cierre_sin_release` |
| `CB-009` | `C-17` | `test_tag_divergente` |
| `CB-010` | Constante de la ventana de legado | `test_legado_de_008_a_011` |
| `CB-011` | Contrato de la regularización | Contraste de contenido por artefacto y revisión del planner en G2 |
| `CB-012` | Sección de cierre append-only | `test_cierre_completo` sobre un reporte con dictamen no convergido |
| `CB-013` | Contrato de la regularización | Contraste de contenido por tarea en las siete specs |
| `CB-014` | Exención de historial | `test_legado_de_008_a_011` y validador sobre `SPEC-001` a `SPEC-007` |
| `CB-015` | `C-14` | `test_formato_de_varios_ca` |
| `CB-016` | `C-17` | `test_cierre_ausente` |
| `CB-017` | `C-18` | `test_regularizacion_patch` y `test_regularizacion_sin_patch` |
| `CB-018` | `C-16` | `test_alcance_de_commits` |
