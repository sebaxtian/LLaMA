# Clarificación — SPEC-014

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-014` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `AUD-101` declara que la preparación del árbol es superficial y sin etiquetas, pero no fija el valor de profundidad ni el efecto esperado sobre el alcance de la comprobación de la referencia a la spec. Una profundidad distinta de la completa deja la comprobación en «no aplicable» y el job `verify` no examina commit alguno, de modo que el defecto reaparece con otra redacción.
- **Pregunta:** ¿Con qué profundidad y con qué declaración de etiquetas prepara el árbol el job `verify`, y qué alcance adquiere la comprobación de la referencia a la spec?
- **Respuesta:** la preparación declara `fetch-depth: 0` y `fetch-tags: true`, es decir, historial completo y etiquetas del repositorio. Con esa preparación la comprobación acota el alcance al último tag anotado de release o, en su defecto, a los commits posteriores al ancestro común con `main`, y examina al menos un commit de implementación cuando el rango no está vacío. El repositorio no se recorta y no se sustituye la comprobación por una declaración de no aplicable.
- **Decisión:** corrección de `RF-001` y ajuste de `CB-001`, `CB-002` y `CA-001`, con la tabla de parámetros fijados en el cuerpo del requisito.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `AUD-102` registra que las 48 pruebas de `tools/git/tests` no se ejecutan en job alguno y que la norma de rango 4 describe el check `verify` con el alcance de una sola suite. No estaba fijado si el alcance se amplía, se declara la ausencia de cobertura o se limita el check a la suite existente.
- **Pregunta:** ¿Qué suites ejecuta el job `verify` y qué documento declara ese alcance?
- **Respuesta:** el job `verify` ejecuta también `tools/git/tests`, como paso nombrado y con su propio límite de ejecución, además de `tools/sdd/tests`. `docs/Flujo_de_Trabajo_Git.md` declara que el check `verify` ejecuta las dos suites, de modo que el alcance del check exigible y su descripción normativa coinciden. Ninguna suite queda fuera de job.
- **Decisión:** corrección de `RF-002` y ajuste de `CB-003` y `CA-002`, con la obligación documental en el rango 4.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `AUD-066` señala que el orquestador conserva `edit` con efecto `allow` sobre `.opencode/**`, `.github/**`, `opencode.jsonc` y `MEMORY.md` mientras §12 del protocolo le niega la escritura sobre documentos y código y le atribuye esas rutas a otros roles. El destino de la observación admitía dos sentidos opuestos: ampliar §12 o retirar las concesiones.
- **Pregunta:** ¿Se alinea §12 con la matriz o se retiran las concesiones de la matriz, y qué rol asume cada una de las rutas retiradas?
- **Respuesta:** se retiran las concesiones. El orquestador conserva escritura solo sobre `.opencode/**`. Las rutas `.github/**`, `opencode.jsonc` y `MEMORY.md` quedan en manos del propietario o del rol concesionario: `.github/**` en el `coder`, `MEMORY.md` en el `documenter` y `opencode.jsonc` en el propietario, por ser una ruta sin rol concesionario. §12 del protocolo y `AGENTS.md` no se editan: la corrección es de la matriz.
- **Decisión:** corrección de `RF-003` y ajuste de `CB-004` y `CA-003`, con la tabla de valores fijados en el cuerpo del requisito.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `AUD-075` registra que `RNF-001` y `CA-015` de `SPEC-013` figuran superados con la evidencia diferida al informe final y que esa evidencia no confirma la condición: las dieciséis observaciones están cerradas, pero el veredicto global es `CONFORME CON OBSERVACIONES` porque cinco dimensiones conservan observación vigente. Tampoco estaba fijado si la fila se corrige, se reabre el requisito o se registra la evidencia sin tocar la matriz.
- **Pregunta:** ¿Cómo se resuelve la evidencia diferida de `RNF-001` y `CA-015` sin reabrir un requisito publicado?
- **Respuesta:** `SPEC-013` recibe en su reporte de validación una nota append-only que transcribe el veredicto del informe final, el cierre de las dieciséis observaciones de la reauditoría previa —quince con artefacto y una por exención declarada—, la causa del veredicto `CONFORME CON OBSERVACIONES`, que son las siete observaciones nuevas, y el estado de las cuatro observaciones que esta spec cierra. La matriz de trazabilidad y el dictamen no se alteran, el estado `validated` se conserva y no se reabre requisito alguno. La nota registra el resultado observado y no reescribe el criterio publicado.
- **Decisión:** corrección de `RF-004` y ajuste de `CB-005` y `CA-004`, con el caso borde nuevo `CB-006` sobre el estado transcrito.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** `AUD-075` exige una nota en el reporte de una spec en estado `validated`, y el contrato de roles acota la escritura de `validation_report.md` al reporte de la spec en curso. No estaba fijado qué rol escribe la nota ni con qué permiso, de modo que la corrección podía quedar sin responsable ejecutable.
- **Pregunta:** ¿Qué rol escribe la nota de cierre en el reporte de `SPEC-013` y con qué habilitación?
- **Respuesta:** la escribe el `reviewer`, que es el rol con permiso de escritura sobre `specs/*/validation_report.md` en la matriz vigente, por delegación escrita del propietario y en la modalidad append-only que §13 del protocolo fija para los registros posteriores a G4. La delegación no alcanza la sección de aprobaciones de `spec.md` ni el dictamen, y no se interpreta como permiso para aprobar compuerta alguna.
- **Decisión:** precisión de `## Actores y permisos` y de `RF-004`; sin requisito nuevo.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `RF-005` exige que cada observación quede cerrada con evidencia verificable, pero no fijaba qué se entiende por cierre ni qué ocurre cuando el artefacto de una observación no existe al redactar el informe final. Sin ese límite, la declaración de cierre podía apoyarse en la intención de corregir.
- **Pregunta:** ¿Qué acredita el cierre de cada una de las cuatro observaciones y qué se registra cuando falta el artefacto?
- **Respuesta:** el cierre exige dos elementos por observación: el artefacto que elimina la causa —la preparación del árbol corregida, el paso de la segunda suite, la matriz reducida o la nota de cierre— y la evidencia transcrita de su verificación. El informe final declara cuatro de cuatro cerradas. Una observación sin artefacto de cierre no se declara cerrada: se registra en estado vigente con su causa, y la reauditoría posterior conserva el hallazgo.
- **Decisión:** corrección de `RF-005` y ajuste de `CA-005`, con el caso borde nuevo `CB-007` sobre la observación sin artefacto.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-006

`SI la nota de cierre transcribe un estado de las 16 observaciones distinto del que declara el informe final, ENTONCES la validación DEBE registrar un error que nombre el valor en conflicto y NO DEBE declarar la nota conforme.`

### CB-007

`SI una de las 4 observaciones no cuenta con artefacto de cierre, ENTONCES el informe final NO DEBE declararla cerrada y DEBE registrar su causa en estado vigente.`

## Parches aplicados a `spec.md`

- [x] `RF-001` y `CA-001`: profundidad completa con valor 0 y descarga de etiquetas, con el alcance de al menos 1 commit de implementación y la tabla de parámetros fijados — afecta a `RF-001`, `CB-001`, `CB-002` y `CA-001`.
- [x] `RF-002` y `CA-002`: ejecución de las 2 suites como pasos nombrados y declaración del alcance en `docs/Flujo_de_Trabajo_Git.md` — afecta a `RF-002`, `CB-003` y `CA-002`.
- [x] `RF-003` y `CA-003`: matriz del orquestador limitada a `.opencode/**`, con `.github/**`, `opencode.jsonc` y `MEMORY.md` denegados y la tabla de roles concesionarios — afecta a `RF-003`, `CB-004` y `CA-003`.
- [x] `RF-004` y `CA-004`: nota de cierre append-only con el veredicto, el cierre de las 16 observaciones y la causa del veredicto, sin alterar matriz ni dictamen — afecta a `RF-004`, `CB-005` y `CA-004`.
- [x] `RF-005` y `CA-005`: cierre con artefacto y evidencia por observación, con la observación sin artefacto en estado vigente — afecta a `RF-005` y `CA-005`.
- [x] `## Actores y permisos`: escritura de la matriz en `.opencode/agents/sdd.md` y `opencode.jsonc` por el propietario, nota de cierre por el `reviewer` por delegación y competencias del `coder` y del `documenter` — afecta a `RF-003` y `RF-004`.
- [x] `## Fuera de alcance`: cierre de `AUD-038`, `AUD-067` y `AUD-098` en el Pull Request #13, conservación de `SPEC-013` y ausencia de declaración de compuertas — afecta a `RF-004` y `RF-005`.
- [x] Caso borde nuevo `CB-006` incorporado al cuerpo de la spec y enlazado en la línea `Cubre:` de `CA-004` — afecta a `CB-006` y `CA-004`.
- [x] Caso borde nuevo `CB-007` incorporado al cuerpo de la spec y enlazado en la línea `Cubre:` de `CA-005` — afecta a `CB-007` y `CA-005`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-14 y `status` `clarified`; fila nueva en `## Historial de cambios` y fila T1 en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- La profundidad del clon es un requisito de verificación y no una optimización: sin historial completo y sin etiquetas, la comprobación de la referencia a la spec no examina commit alguno y el check `verify` acredita menos de lo que declara.
- El check exigible del job `verify` cubre las dos suites del repositorio. La suite de `tools/git/tests` deja de ser cobertura ausente y su resultado forma parte del check que condiciona G5.
- La matriz de permisos es la que se corrige y §12 del protocolo se conserva. El menor privilegio del orquestador se expresa en la matriz, y la única ruta que conserva es `.opencode/**`, que no es documentación, código ni configuración del repositorio.
- `opencode.jsonc` queda en el propietario porque ningún rol de la matriz declara escritura sobre esa ruta: la ruta no declarada está denegada.
- La nota de cierre de `SPEC-013` es append-only y registra el resultado observado. No reescribe el criterio publicado, no cambia el valor `PASADO` de la matriz y no altera el dictamen `CONVERGIDO`; su función es que la evidencia diferida quede transcrita y contrastable.
- El veredicto `CONFORME CON OBSERVACIONES` no se corrige ni se sustituye: se transcribe con su causa, que son las siete observaciones nuevas y no las dieciséis observaciones previas, cerradas en su totalidad.
- El cierre de una observación exige artefacto y evidencia. Una observación sin artefacto permanece vigente y la declaración de cierre del informe final no la absorbe.
- La corrección de una ruta, de un paso del flujo o de una fila de reporte no cambia el rango ni el carácter del documento que la contiene, y no autoriza compuerta alguna.
- El validador acredita estructura, coherencia y trazabilidad declarada; no acredita la ejecución real del flujo en GitHub ni la conformidad del régimen, y no sustituye la firma del propietario en G1 ni en G4.
