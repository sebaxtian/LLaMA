# Clarificación — SPEC-018

*Artefacto de rango 6: registro de las doce ambigüedades de SPEC-018 resueltas con el propietario antes de abrir Plan, y de la reapertura de la clarificación del 2026-11-25 con AMB-013. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1. La reapertura no declara G1: la aprobación anterior queda sin efecto sobre el contrato reformulado y la nueva aprobación firmada corresponde al propietario.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** La cifra nominal y la regla de derivación para el contexto ajustado no estaban especificadas numéricamente en `spec.md`, postergando la definición a la etapa Clarify.
- **Pregunta:** ¿Cuál es la cifra nominal base de tokens y la regla determinista de cálculo para cada escenario de contexto ajustado?
- **Respuesta:** Cada escenario ajustado declara un valor nominal base en tokens (múltiplos de 1024 tokens: para 0 capas 8192 tokens; para 6 capas 16384 tokens; para 9 capas 65536 tokens) derivado de la fórmula determinista que reserva el presupuesto de VRAM sin derrame a host. En tiempo de ejecución previo al lanzamiento, el sistema verifica la VRAM libre real y deriva el contexto efectivo aplicando la regla determinista en múltiplos de 1024 tokens con suelo mínimo de 4096 tokens (CB-003).
- **Decisión:** Se actualizan `RF-009` y `CA-007` fijando los valores nominales base (8192, 16384 y 65536 tokens) y la regla determinista en múltiplos de 1024 tokens con suelo mínimo de 4096 tokens.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** La composición y el desglose de recursos del presupuesto de VRAM por escenario no estaban formalizados numéricamente ni en componentes.
- **Pregunta:** ¿Cómo se estructura y desglosa el presupuesto de VRAM de cada escenario?
- **Respuesta:** Cada escenario declara un presupuesto total de VRAM en MiB y el desglose de 4 componentes alineado con SPEC-017 (pesos, cache_kv, computo, reserva/margen). Debe garantizar un margen de VRAM libre mínimo de 512 MiB respecto a la capacidad de la GPU (16384 MiB).
- **Decisión:** Se actualizan `RF-006` y `CA-004` para exigir el desglose de 4 componentes (`pesos`, `cache_kv`, `computo`, `reserva/margen`) y el margen libre mínimo de 512 MiB respecto a 16384 MiB.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** Ambigüedad sobre la relación funcional entre el nuevo catálogo de escenarios y los perfiles vigentes en `src/gemma/perfiles/`.
- **Pregunta:** ¿Cómo interactúa el catálogo de escenarios con los perfiles existentes de Gemma?
- **Respuesta:** El catálogo convive con los perfiles existentes (rendimiento, resiliencia, sin_especulativa) en `src/gemma/perfiles/`. Los perfiles representan perfiles de producción versionados, mientras el catálogo es la matriz de 9 escenarios de ejecución del modelo. La selección de un escenario aplica sus parámetros de forma autónoma.
- **Decisión:** Se actualizan `RF-012` y `CA-004` estableciendo la convivencia y la autonomía de ejecución de los escenarios respecto a los perfiles vigentes.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** No se explicitaba el mecanismo de interfaz para que el operador invoque el selector de escenario.
- **Pregunta:** ¿Por qué vías de interfaz se selecciona un escenario y cómo se comporta ante la ausencia de argumentos?
- **Respuesta:** Doble vía: opción CLI en el lanzador (argumento para seleccionar por identificador y opción para listar) e integración en el flujo interactivo de selección de ejecución. La invocación sin argumento de escenario mantiene el perfil predeterminado o solicita selección.
- **Decisión:** Se actualizan `RF-003`, `RF-005` y `CA-002` explicitando la doble vía CLI e interactiva.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** Ausencia de un modelo formal de ciclo de vida y estados para los escenarios dentro del catálogo.
- **Pregunta:** ¿Cuáles son los estados admitidos para cada escenario y qué condiciones rigen sus transiciones?
- **Respuesta:** Cada escenario declara uno de cuatro estados: `declarado`, `medido`, `aprobado`, `no_ejecutable`. Inicialmente se declaran como `declarado` (salvo el inviable que se marca `no_ejecutable`). Ningún escenario pasa a `aprobado` sin medición registrada y confirmación escrita del propietario (RF-011).
- **Decisión:** Se actualizan `RF-002`, `RF-011` y `CA-008` incorporando formalmente el ciclo de vida de cuatro estados (`declarado`, `medido`, `aprobado`, `no_ejecutable`).
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** No se definía el formato sintáctico exacto de los identificadores de los escenarios.
- **Pregunta:** ¿Cuál es la sintaxis exacta de los 9 identificadores de escenario en el catálogo?
- **Respuesta:** Identificador determinista y semántico con prefijo `ESC-` seguido de capas MoE y contexto: `ESC-M0-C4K`, `ESC-M0-C131K`, `ESC-M0-CADJ`, `ESC-M6-C4K`, `ESC-M6-C131K`, `ESC-M6-CADJ`, `ESC-M9-C4K`, `ESC-M9-C131K`, `ESC-M9-CADJ`. El identificador es permanente e invariable incluso si el contexto ajustado efectivo se recalcula por disponibilidad dinámica.
- **Decisión:** Se actualizan `RF-002` y `CA-001` especificando los 9 identificadores canónicos y su invariabilidad.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `RF-005` exigía "1 orden determinista" de enumeración pero no definía los criterios de ordenación.
- **Pregunta:** ¿Cuál es la regla determinista para ordenar la lista de escenarios del catálogo?
- **Respuesta:** Orden jerárquico determinista: primero por capas de expertos en CPU ascendente (0, 6, 9), y segundo por contexto efectivo en tokens ascendente (4096, ajustado, 131072).
- **Decisión:** Se actualizan `RF-005` y `CA-002` explicitando la regla de ordenación jerárquica por capas MoE en CPU y contexto en tokens.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `RF-013` requería declarar 7 parámetros de ejecución restantes sin fijar los valores canónicos esperados.
- **Pregunta:** ¿Cuáles son los valores y directrices canónicas para los 7 parámetros de ejecución restantes en cada escenario?
- **Respuesta:** Cada escenario declara explícitamente sus 7 parámetros restantes en el catálogo (descarga total a GPU: -ngl 99; atención rápida: flash_attn on; ubatch: 1120; mmap: on/off según perfil base; parallel: 1; cache_type_k: q8_0; cache_type_v: q8_0; y draft de 3 tokens si aplica), garantizando autonomía y reproducibilidad estricta.
- **Decisión:** Se actualizan `RF-013` y `CA-009` especificando los valores canónicos de los 7 parámetros de ejecución restantes.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-009

- **Descripción:** Tratamiento en el catálogo del escenario de 6 capas y 131 072 tokens que la evidencia previa señala como incapaz de alcanzar servicio.
- **Pregunta:** ¿Debe incluirse en el catálogo la combinación de 6 capas y 131 072 tokens y cómo debe comportarse el sistema ante ella?
- **Respuesta:** Se incluye en el catálogo para preservar la cobertura 3×3 de los 9 escenarios requerida por RF-001, pero su estado inicial se fija como `no_ejecutable` fundamentado en la evidencia de SPEC-017 (arranque no alcanza servicio en 16 GB VRAM). El precheck / lanzador impide el lanzamiento y emite diagnóstico sin intentar cargar el servidor.
- **Decisión:** Se actualizan `RF-001`, `CB-007` y `CA-010` formalizando que `ESC-M6-C131K` pertenece al catálogo en estado `no_ejecutable` y aborta en precheck sin intentar iniciar el servidor.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-010

- **Descripción:** Falta de criterio explícito sobre el sentido del margen entre el consumo medido y el presupuesto declarado para evaluar conformidad.
- **Pregunta:** ¿Qué relación matemática entre consumo medido y presupuesto determina que un escenario es conforme?
- **Respuesta:** El consumo medido de VRAM debe ser menor o igual al presupuesto declarado (consumo <= presupuesto). Se admite que sobre VRAM (reserva libre), pero cualquier derrame por encima del presupuesto declarado genera alerta y descalifica la conformidad del escenario.
- **Decisión:** Se actualizan `RF-008`, `CB-002` y `CA-006` fijando la regla de conformidad `consumo <= presupuesto`.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-011

- **Descripción:** El presupuesto contemplaba únicamente VRAM, omitiendo el impacto en memoria RAM del host de las capas MoE derivadas a CPU.
- **Pregunta:** ¿Debe el presupuesto por escenario incluir la memoria RAM del sistema además de la VRAM y comprobarse su suficiencia?
- **Respuesta:** El presupuesto principal obligatorio es de VRAM (en MiB). Se añade un campo informativo de memoria RAM de sistema requerida para las capas MoE derivadas a CPU (0 capas = 0 MiB; 6 capas ≈ 3500 MiB; 9 capas ≈ 5200 MiB), con precomprobación de que el host tenga al menos 8192 MiB de RAM libre.
- **Decisión:** Se actualizan `RF-006`, `RF-007`, `CA-004`, `CA-005` y se añade el nuevo caso borde `CB-008` para requerir el campo informativo de RAM de sistema y la comprobación de RAM libre host >= 8192 MiB.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-012

- **Descripción:** Incertidumbre sobre si un escenario requiere que el perfil base correspondiente esté aprobado para poder ser seleccionado o ejecutado.
- **Pregunta:** ¿La selección y ejecución de un escenario depende del estado de aprobación del perfil base?
- **Respuesta:** La selección de un escenario es independiente de si un perfil está aprobado. Cualquier escenario en estado `declarado` o `medido` puede ser seleccionado y ejecutado para validación o comparación técnica.
- **Decisión:** Se actualizan `RF-011`, `RF-012` y `CA-008` estableciendo que la ejecutabilidad depende del estado del escenario (`declarado` o `medido`) y no del estado de los perfiles.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-008

`SI la memoria RAM libre del host es menor a 8192 MiB al seleccionar 1 escenario que deriva capas de expertos a CPU (6 o 9 capas), ENTONCES el sistema NO DEBE iniciar el servidor y DEBE declarar la RAM libre disponible y la RAM requerida en MiB.`

## Parches aplicados a `spec.md`

- [x] Inclusión del identificador canónico `ESC-M6-C131K` en estado `no_ejecutable` para completar la cobertura 3×3 — afecta a `RF-001`, `CB-007` y `CA-010`.
- [x] Especificación de los 9 identificadores canónicos invariables y los 4 estados admitidos (`declarado`, `medido`, `aprobado`, `no_ejecutable`) — afecta a `RF-002` y `CA-001`.
- [x] Especificación de la doble vía (CLI interactivo y argumentos CLI) para el selector de escenario — afecta a `RF-003`, `RF-005` y `CA-002`.
- [x] Definición del orden determinista jerárquico de enumeración (capas MoE CPU ascendente, luego contexto efectivo ascendente) — afecta a `RF-005` y `CA-002`.
- [x] Desglose de 4 componentes del presupuesto de VRAM (pesos, cache_kv, computo, reserva/margen), margen mínimo de 512 MiB libres sobre 16384 MiB y campo informativo de RAM de sistema requerida — afecta a `RF-006` y `CA-004`.
- [x] Precomprobación de VRAM disponible y verificación de RAM libre de host mínima (8192 MiB) — afecta a `RF-007`, `CB-008` y `CA-005`.
- [x] Criterio formal de conformidad del consumo medido frente al presupuesto (`consumo <= presupuesto`) y registro de exceso — afecta a `RF-008`, `CB-002` y `CA-006`.
- [x] Declaración de valores nominales base de contexto ajustado (8192, 16384 y 65536 tokens) y regla determinista en múltiplos de 1024 tokens con suelo mínimo de 4096 tokens — afecta a `RF-009` y `CA-007`.
- [x] Modelo de transición a `aprobado` condicionado a medición registrada y confirmación del propietario, con ejecutabilidad autónoma para estados `declarado` y `medido` independiente de los perfiles — afecta a `RF-011` y `CA-008`.
- [x] Convivencia y autonomía de ejecución de los escenarios frente a los 3 perfiles vigentes — afecta a `RF-012` y `CA-004`.
- [x] Especificación de valores y directrices canónicas para los 7 parámetros de ejecución restantes — afecta a `RF-013` y `CA-009`.
- [x] `RF-011` y `CA-008` con el registro de aprobación que conserva los 4 valores que sostuvieron la aprobación —capas de expertos en CPU, contexto efectivo en tokens, los 7 parámetros de ejecución y el presupuesto de VRAM en MiB— y con la comparación de esos valores frente a los declarados por el escenario, de modo que 1 diferencia en cualquiera de ellos revoca la condición de aprobado y exige 1 medición nueva — afecta a `RF-011` y `CA-008`.

## Decisiones de negocio

- Se preserva la matriz 3×3 íntegra de 9 escenarios para propósitos de análisis comparativo y catalogación exhaustiva, catalogando el escenario técnicamente inviable (`ESC-M6-C131K`) como `no_ejecutable` desde el diseño.
- El presupuesto de VRAM se rige estrictamente por la regla `consumo <= presupuesto` con margen de seguridad mínimo de 512 MiB para salvaguardar la eGPU USB4 contra transferencias lentas a memoria compartida.
- La memoria RAM de sistema se controla como salvaguarda operativa mediante precheck (mínimo 8192 MiB libres) sin alterar la centralidad del presupuesto de VRAM de la GPU dedicada.

## Reapertura de la clarificación (v0.6.0)

- **Motivo:** brecha de implementación de `CB-006` detectada en la validación con dictamen `NO CONVERGIDO`: `plan.md` designa 1 instrumento de prueba inexistente para la modificación inválida del estado aprobado y `escenarios.py` resuelve la admisibilidad solo por la veracidad del campo `aprobacion`, sin conservar ni comparar los valores que sostuvieron la aprobación.
- **Alcance:** se cierra AMB-013, se parchean `RF-011` y `CA-008` con la conservación y comparación del registro de aprobación, y se fija la tarea `T-017` que implementa la revocación y su prueba. La corrección de los 7 instrumentos de `plan.md` con nombre inexistente corresponde a la etapa Plan. No se añaden casos borde nuevos y `CB-006` conserva su redacción.
- **Constancia:** no se altera ningún otro `AMB`: `AMB-001` a `AMB-012` conservan su descripción, pregunta, respuesta, decisión, fecha y responsable, y el alcance de esta reapertura se limita a `AMB-013`.

### AMB-013

- **Descripción:** `CB-006` exige que 1 escenario aprobado que recibe 1 modificación en capas de expertos en CPU, contexto, parámetros de ejecución o presupuesto pierda la condición de aprobado y exija 1 medición nueva, y la implementación resuelve la admisibilidad solo por la veracidad del campo `aprobacion`, sin conservar ni comparar los valores aprobados; el instrumento que `plan.md` designa no existe.
- **Pregunta:** ¿qué debe conservar el registro de aprobación para que la modificación de 1 valor revoque el estado aprobado?
- **Respuesta:** el registro de aprobación conserva los 4 valores que sostuvieron la aprobación —capas de expertos en CPU, contexto efectivo en tokens, los 7 parámetros de ejecución y el presupuesto de VRAM—, y la admisibilidad compara esos valores con los declarados; 1 diferencia en cualquiera de ellos revoca la condición de aprobado y exige 1 medición nueva.
- **Decisión:** parche a `RF-011` y a `CA-008` con la exigencia de conservar y comparar el registro de aprobación, tarea `T-017` para implementar la revocación y su prueba, y corrección de los 7 instrumentos inexistentes en `plan.md` en la etapa Plan.
- **Fecha:** 2026-11-25 (UTC).
- **Responsable:** Agent Sebaxtian.
