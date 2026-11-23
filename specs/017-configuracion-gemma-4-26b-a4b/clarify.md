# Clarificación — SPEC-017

*Artefacto de rango 6: registro de las trece ambigüedades de `SPEC-017` resueltas con el propietario antes de abrir Plan, y de la reapertura de la clarificación del 2026-11-23. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1. La reapertura no declara G1: la aprobación anterior queda sin efecto sobre el contrato reformulado y la nueva aprobación firmada corresponde al propietario.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `RF-007` y `CA-004` fijan los estados candidato, medido y aprobado de cada perfil, y el objetivo de la feature nombra 1 configuración canónica, pero el contrato no designa qué perfil es el canónico y la expresión «perfil canónico» admite cualquier candidato de la línea base documental. La promoción queda así sin sujeto declarado y la sección de configuración aprobada podría recibir 1 perfil sin que conste el acto que lo designa.
- **Pregunta:** ¿Qué perfil es el canónico y en qué momento lo fija el contrato?
- **Respuesta:** no se fija en la spec: es el que el propietario confirme por escrito y, hasta entonces, cada perfil es candidato.
- **Decisión:** parche a `RF-007` y a `CA-004` con la prohibición de declarar 1 perfil como canónico sin la confirmación escrita del propietario; la designación se registra como decisión de negocio y no como valor de la spec.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** el perfil declara 131 072 tokens de contexto y el contrato no fija si ese tamaño es requisito del caso de uso o valor candidato sujeto a comparación. `CB-007` impide iniciar el servidor cuando el contexto excede la VRAM disponible y `RF-012` exige comparación de la desviación de tamaño de contexto, pero no consta si la alternativa de contexto menor forma parte de la medición registrada.
- **Pregunta:** ¿Qué carácter tiene el contexto de 131 072 tokens y qué medición acompaña su desviación?
- **Respuesta:** es requisito del caso de uso, sujeto al caso borde que impide iniciar cuando el contexto excede la VRAM disponible; el contexto menor se mide como alternativa comparada.
- **Decisión:** parche a `RF-012` y a `CA-011` con la exigencia de registrar la alternativa de contexto menor medida cuando el perfil declare 131 072 tokens de contexto.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** el perfil declara atención rápida activada mientras los parámetros iniciales del proyecto para el modelo la declaran desactivada. `RF-012` exige 1 prueba comparativa de la desviación, pero el contrato no fija qué parámetro rige en la configuración ejecutable mientras esa prueba no conste registrada, de modo que la desviación podría aplicarse sin contraste medido.
- **Pregunta:** ¿En qué condición se admite la atención rápida activada?
- **Respuesta:** es una excepción admitida solo con 1 prueba comparativa registrada de la opción activada frente a la desactivada; sin esa prueba rige el parámetro inicial del proyecto.
- **Decisión:** requisito funcional nuevo `RF-014` con la primacía del parámetro inicial del proyecto y criterio `CA-014`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** el perfil declara micro-lote de 1 120 tokens sin que conste si el valor es requisito del caso de uso o si hereda del perfil anterior. `RF-012` exige comparación de la desviación de micro-lote, pero el contrato no declara qué rige mientras la comparación no exista, de modo que 1 valor heredado podría quedar fijado como si fuera requisito.
- **Pregunta:** ¿Qué carácter tiene el micro-lote de 1 120 tokens?
- **Respuesta:** es 1 valor heredado sujeto a comparación y no 1 requisito del caso de uso.
- **Decisión:** `RF-014` y `CA-014` con la misma regla de primacía del parámetro inicial.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** la línea base documental conserva 9 capas de expertos en CPU y el análisis de la feature propone 10, sin que el contrato declare el valor de referencia ni si la comparación de ese parámetro es exigible. `RF-012` enumera las desviaciones que exigen prueba comparativa sin incluir las capas de expertos en CPU, de modo que la elección entre 9 y 10 quedaría fuera de la medición registrada.
- **Pregunta:** ¿Cuál de los 2 valores de capas de expertos en CPU es el de referencia y cómo se elige?
- **Respuesta:** ambos son candidatos; la elección corresponde al propietario tras la comparación, con el margen de VRAM libre que fija `RNF-007`.
- **Decisión:** parche a `RF-012` y a `CA-011` con las capas de expertos en CPU en la lista de desviaciones comparadas, sin fijar 9 ni 10 como valor del contrato.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `RF-009` exige registrar la velocidad de generación en tokens por segundo y `RF-007` prohíbe declarar aprobado 1 perfil sin medición registrada, pero el contrato no fija la condición de velocidad que habilita la aprobación. Sin esa condición, 1 configuración se declara aprobada con cualquier velocidad registrada y la aprobación no distingue 1 resultado aceptable de 1 resultado deficiente.
- **Pregunta:** ¿Qué umbral de velocidad de generación habilita la aprobación de 1 configuración?
- **Respuesta:** se decide después de medir. La spec no fija la cifra y debe exigir que ninguna configuración se declare aprobada sin 1 umbral mínimo de velocidad de generación en tokens por segundo, declarado por el propietario a partir de 1 medición registrada.
- **Decisión:** requisito no funcional nuevo `RNF-006` y criterio `CA-015`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `RF-001`, `RF-002` y `RF-011` nombran el proyector multimodal como artefacto requerido y `## Fuera de alcance` excluye la prueba multimodal como condición de aprobación, sin que conste si la cobertura multimodal es obligatoria para declarar medido 1 perfil. La ambigüedad afecta al peso de la prueba multimodal en la promoción del perfil.
- **Pregunta:** ¿La prueba multimodal es condición para declarar medido 1 perfil?
- **Respuesta:** es cobertura opcional y queda fuera de la condición de aprobación.
- **Decisión:** sin cambio en `spec.md`; el punto ya consta en `## Fuera de alcance` y el proyector multimodal permanece exigido como artefacto de existencia en `RF-002` y `RF-011`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `RF-008` y `CA-007` declaran la VRAM libre sin margen mínimo, `RNF-003` fija el desbordamiento hacia memoria compartida en 0 MiB y `CB-004` admite «0 MiB de VRAM libre» como umbral del caso borde. Con esos valores, 1 carga con desbordamiento de 0 MiB y 1 MiB de VRAM libre se declara aprobable, porque el margen que evita el desbordamiento durante el servicio no está fijado.
- **Pregunta:** ¿Qué margen de VRAM libre se exige tras la carga y sobre qué memoria se mide?
- **Respuesta:** 512 MiB libres como mínimo tras la carga, medidos sobre la GPU dedicada.
- **Decisión:** requisito no funcional nuevo `RNF-007`; parche a `CA-007` y a `CB-004` con el margen de 512 MiB y la remisión del umbral del caso borde a ese requisito.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-009

- **Descripción:** `CB-005` y `CA-006` exigen corregir las secuencias corruptas por doble codificación de la línea base documental sin declarar el límite de la corrección sobre los valores medidos y los identificadores de prueba. Sin ese límite, la corrección de codificación podría reescribir contenido histórico y alterar el sujeto de la comparación de la feature.
- **Pregunta:** ¿Qué alcanza la corrección de la línea base documental?
- **Respuesta:** solo la codificación: no se altera ningún valor medido histórico ni ningún identificador de prueba.
- **Decisión:** sin cambio en `spec.md`; `CB-005` ya limita la corrección a 1 cambio editorial y `CA-006` exige que los valores medidos históricos y los identificadores de prueba conserven su contenido.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-010

- **Descripción:** `RF-004` y `RNF-004` exigen 1 archivo de registro propio por ejecución sin declarar su ubicación ni su relación con el control de versiones. La ambigüedad admite un registro versionado, que incorporaría resultados locales al repositorio, y un registro en 1 ruta que el contrato no puede nombrar sin incumplir la prohibición de rutas técnicas.
- **Pregunta:** ¿Dónde se ubica el registro de cada ejecución y qué exige la spec sobre su ruta?
- **Respuesta:** fuera del control de versiones, en la carpeta de resultados locales del proyecto; la spec solo exige 1 registro propio por ejecución y no nombra rutas.
- **Decisión:** sin cambio en `spec.md`; `RF-004` y `RNF-004` se mantienen sin ruta y la ubicación se registra como decisión de negocio.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-011

- **Descripción:** el frontmatter declara `release: ""` y `## Fuera de alcance` excluye la publicación del release, pero no consta si la feature se cierra en esta rama, si se integra sin release o si se empaqueta en 1 release propio. El destino condiciona la versión del release y el contenido de la entrada del registro de cambios.
- **Pregunta:** ¿Cuál es el destino de la feature y cuándo se decide?
- **Respuesta:** permanece abierto hasta la confirmación del propietario y el release se decide después de esa confirmación.
- **Decisión:** sin cambio en `spec.md`; se registra como decisión de negocio y el campo `release` del frontmatter permanece vacío.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-012

- **Descripción:** `RF-001` exige resolver 4 artefactos locales, entre ellos el modelo draft, y `RF-011` ofrece 1 perfil sin decodificación especulativa cuando ese modelo no está disponible. El contrato no declara si el modelo draft integra el perfil canónico o si su ausencia solo habilita la alternativa, de modo que la obligatoriedad del artefacto queda indeterminada.
- **Pregunta:** ¿El modelo draft es obligatorio en la configuración?
- **Respuesta:** es opcional: es la alternativa del perfil sin decodificación especulativa y no forma parte del perfil canónico.
- **Decisión:** parche a `RF-011` y a `CA-010` con la iniciación del perfil sin decodificación especulativa sin el modelo draft.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-013

- **Descripción:** `RNF-003` fijaba el desbordamiento hacia memoria compartida del perfil aprobado en `0 MiB`, y `CB-004` y `CA-007` repetían ese umbral. Con el proyector multimodal y el modelo draft obligatorios, los 16 GB de VRAM de la GPU objetivo no permiten cargar el modelo sin descargar capas de expertos a la CPU: la medición de la máquina objetivo con `ncmoe` `0` deja `56 MiB` de VRAM libre y `1016 MiB` de «Shared Usage», y con `ncmoe` `9` deja `3175 MiB` de VRAM libre y `4374 MiB` de «Shared Usage», de los cuales `4071 MiB` son `CUDA_Host model buffer` de expertos descargados intencionalmente. Como el «Shared Usage» incluye la descarga intencional, el umbral de `0 MiB` es inalcanzable con el requisito de proyector y la capacidad de la GPU, y el registro no distingue la memoria de expertos en host del derrame no intencional.
- **Pregunta:** ¿Cómo se distingue el derrame no intencional hacia memoria compartida de la descarga intencional de expertos a la CPU y qué umbral se exige al perfil aprobado?
- **Respuesta:** el derrame no intencional es la diferencia entre el «Shared Usage» del árbol de procesos del servidor y la memoria de expertos en host declarada; su umbral es `512 MiB` como máximo y la descarga intencional de expertos a la CPU no cuenta como derrame. Esa memoria de expertos en host se registra en un campo propio del registro de cada prueba.
- **Decisión:** reformulación de `RNF-003` con el derrame no intencional de como máximo `512 MiB` y su definición operativa; ampliación de `RF-006` de 21 a 22 campos con el campo 22 «Memoria de expertos en host» en `MiB`; parches a `RNF-005`, `CB-004`, `CA-005` y `CA-007` para retirar el umbral de `0 MiB` y contar los 22 campos y los 13 campos de magnitud. Aprobada por el propietario el 2026-11-23. La spec vuelve a `draft`, la clarificación se reabre y G1 queda pendiente de nueva aprobación firmada.
- **Fecha:** 2026-11-23 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

Sin casos borde nuevos en esta clarificación. `CB-004` conserva su número y su efecto sobre la promoción del perfil, y su umbral de derrame no intencional se alinea con `RNF-003` conforme a `AMB-013`.

## Parches aplicados a `spec.md`

- [x] `RF-007` y `CA-004` con la prohibición de declarar 1 perfil como canónico sin la confirmación escrita del propietario, y con la conservación de los estados candidato, medido y aprobado — afecta a `RF-007` y `CA-004`.
- [x] `RF-012` y `CA-011` con la alternativa de contexto menor medida cuando el perfil declara 131 072 tokens de contexto y con las capas de expertos en CPU en la lista de desviaciones comparadas, sin fijar 9 ni 10 como valor del contrato — afecta a `RF-012` y `CA-011`.
- [x] `RF-014` nuevo con la primacía del parámetro inicial del proyecto mientras no conste 1 prueba comparativa registrada de la desviación — afecta a `RF-014` y `CA-014`.
- [x] `RNF-006` nuevo con la prohibición de declarar aprobada 1 configuración sin 1 umbral mínimo de velocidad de generación en tokens por segundo, fijado por el propietario a partir de 1 medición registrada, sin cifra en la spec — afecta a `RNF-006` y `CA-015`.
- [x] `RNF-007` nuevo con al menos 512 MiB de VRAM libre tras la carga, medidos sobre la GPU dedicada — afecta a `RNF-007` y `CA-007`.
- [x] `RF-006`, `RNF-005` y `CA-005` con 1 valor conforme a la columna de contenido obligatorio o 1 marca de no disponible en los 21 campos, y con la unidad exigida solo en los 12 campos de magnitud 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17 y 19 — afecta a `RF-006`, `RNF-005` y `CA-005`.
- [x] `RF-008` y `CA-007` con la VRAM total reportada por la GPU en MiB como base de comparación de la VRAM asignada, en lugar de 16 GB, y con la conservación de la VRAM libre y del desbordamiento en MiB — afecta a `RF-008` y `CA-007`.
- [x] `CB-004` con el margen de 512 MiB de VRAM libre en lugar de 0 MiB, con la remisión del umbral a `RNF-007` y con la conservación del caso de desbordamiento distinto de 0 MiB — afecta a `CB-004` y `CA-007`.
- [x] `RF-011` y `CA-010` con la iniciación del perfil sin decodificación especulativa sin el modelo draft — afecta a `RF-011` y `CA-010`.
- [x] `CA-014` y `CA-015` al final de `## Criterios de aceptación`, con la numeración existente conservada — afecta a `CA-014` y `CA-015`.
- [x] Resultado esperado de `## Contexto y objetivo` con la carga dentro de la VRAM total reportada por la GPU y con al menos 512 MiB de VRAM libre, alineado con `RF-008` y `RNF-007` — afecta a `RF-008` y `RNF-007`.
- [x] Frontmatter con `status` `clarified`, `version` `0.2.0` y `updated` 2026-11-20; fila 0.2.0 en `## Historial de cambios`; fila T1 en `### Historial de transiciones` con la evidencia del cierre de esta clarificación — afecta a la estructura de `spec.md`.
- [x] `RNF-003` reformulado con el derrame no intencional de como máximo 512 MiB, medido como la diferencia entre el «Shared Usage» del árbol de procesos del servidor y la memoria de expertos en host declarada, y con la descarga intencional de expertos a la CPU fuera del cómputo del derrame — afecta a `RNF-003` y a `CA-007`.
- [x] `RF-006` ampliado de 21 a 22 campos con el campo 22 «Memoria de expertos en host» en MiB y con los 13 campos de magnitud 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19 y 22; `RNF-005` y `CA-005` alineados con los 22 campos y los 13 campos de magnitud — afecta a `RF-006`, `RNF-005` y `CA-005`.
- [x] `CB-004` y `CA-007` con el umbral de derrame no intencional de como máximo 512 MiB en lugar de 0 MiB de desbordamiento, con la conservación de la medición registrada y de los 512 MiB de VRAM libre de `RNF-007` — afecta a `CB-004` y `CA-007`.
- [x] Frontmatter con `status` `draft`, `version` `0.5.0` y `updated` 2026-11-23; fila 0.5.0 en `## Historial de cambios`; fila de reversión `tasked` → `draft` en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- Ningún perfil es canónico mientras el propietario no lo confirme por escrito; hasta entonces cada perfil de la línea base documental es candidato y la designación no se escribe como valor de la spec. La promoción exige medición registrada y confirmación escrita, y ningún agente designa el perfil canónico.
- El contexto de 131 072 tokens es requisito del caso de uso y no parámetro inicial: `CB-007` mantiene la prohibición de iniciar cuando el contexto excede la VRAM disponible y la medición registra además la alternativa de contexto menor como comparación.
- El umbral mínimo de velocidad de generación se fija después de medir y no se escribe en la spec: la cifra la declara el propietario a partir de 1 medición registrada, y la aprobación no se declara sin ese umbral.
- La aprobación de 1 configuración exige al menos 512 MiB de VRAM libre sobre la GPU dedicada tras la carga y 1 derrame no intencional hacia memoria compartida de como máximo 512 MiB. El derrame se mide como la diferencia entre el «Shared Usage» del árbol de procesos del servidor y la memoria de expertos en host declarada en el campo 22 del registro; la descarga intencional de expertos a la CPU no cuenta como derrame.
- Los parámetros heredados de la línea base documental —atención rápida activada, micro-lote de 1 120 tokens y capas de expertos en CPU— son candidatos sujetos a comparación y no requisitos. Mientras la comparación no conste registrada rige el parámetro inicial del proyecto.
- La prueba multimodal es cobertura opcional y no condiciona la aprobación; el proyector multimodal permanece exigido como artefacto cuya existencia se comprueba antes de iniciar.
- La corrección de la línea base documental se limita a la codificación: no se altera ningún valor medido histórico ni ningún identificador de prueba, y la corrección se registra como 1 cambio editorial.
- El registro de cada ejecución queda fuera del control de versiones, en la carpeta de resultados locales del proyecto. La spec exige 1 registro propio por ejecución y no nombra rutas ni comandos.
- El destino de la feature permanece abierto hasta la confirmación del propietario y el release se decide después de esa confirmación; el campo `release` del frontmatter permanece vacío y la publicación queda fuera de alcance.
- El modelo draft es opcional: habilita la alternativa sin decodificación especulativa y no integra el perfil canónico. Su ausencia no impide iniciar el perfil alternativo.
- La reformulación de `RNF-003` y la ampliación de `RF-006` a 22 campos reabren la clarificación y devuelven la spec a `draft`: la aprobación de G1 registrada el 2026-11-20 no cubre el contrato reformulado y la nueva aprobación firmada queda pendiente del propietario.
- Esta clarificación no declara compuerta alguna ni la aprobación de la configuración. El cierre de `clarify.md` habilita la lectura de G1 por el propietario y no sustituye su firma.
