---
id: SPEC-018
title: Catálogo de escenarios, selector y presupuesto por escenario
status: tasked
version: 0.4.0
created: 2026-11-24
updated: 2026-11-25
owner: Agent Sebaxtian
branch: feat/catalogo-escenarios
release: ""
supersedes: ""
superseded_by: ""
---

# Catálogo de escenarios, selector y presupuesto por escenario

## Contexto y objetivo

La intención declarada por el propietario es la siguiente: «Cuando quieras abrir el catálogo de escenarios —ncmoe 0/6/9 × ctx_size 4096/131072/ajustado, selector de escenario y presupuesto por escenario—, necesito la rama creada y el identificador.» Esta spec desarrolla esa intención y no la amplía.

La feature publica 1 catálogo de 9 escenarios de ejecución del modelo `Gemma-4-26B-A4B-it-qat-GGUF`: 1 escenario por cada combinación de 3 valores de capas de expertos en CPU —0, 6 y 9 capas— con 3 valores de contexto —4096 tokens, 131 072 tokens y contexto ajustado—. Añade 1 selector que permite elegir 1 escenario del catálogo y 1 presupuesto de recursos declarado por escenario.

La configuración vigente presenta 4 defectos verificados:

1. El repositorio no contiene ningún catálogo de escenarios ni ningún selector de escenario: no existe 1 superficie que enumere combinaciones de ejecución ni 1 vía para elegir 1 combinación declarada.
2. Los 3 manifiestos de perfil vigentes declaran el mismo presupuesto de VRAM, sin distinción por combinación, de modo que el presupuesto no expresa el consumo de 1 escenario concreto.
3. El valor de 6 capas de expertos en CPU no figura en ningún manifiesto vigente: los perfiles declaran 0 y 9 capas, de modo que la combinación intermedia de la intención declarada carece de superficie donde declararse.
4. El contexto de 131 072 tokens consta medido y no adoptado, y ningún perfil declara 1 contexto ajustado; ningún perfil figura como configuración aprobada.

El defecto 2 convierte cada cambio de combinación en 1 edición manual del manifiesto, sin trazabilidad de qué combinación se ejecutó. El defecto 3 impide declarar la combinación de 6 capas sin reutilizar 1 perfil pensado para otro propósito. El defecto 4 impide distinguir el contexto declarado del contexto efectivo de 1 escenario ajustado. El defecto 1 impide seleccionar 1 combinación declarada y exige improvisarla en cada ejecución.

La evidencia medida de la configuración vigente registra que el arranque con 6 capas de expertos en CPU y 131 072 tokens de contexto no alcanza el estado de servicio en la máquina objetivo. El catálogo debe declarar ese resultado como no ejecutable en lugar de presentar la combinación como disponible, y esa constancia es la que sostiene el caso borde del escenario que no llega a servicio.

Objetivo: fijar el contrato que publica el catálogo de 9 escenarios con 1 identificador único por escenario, que hace seleccionable cada escenario con su identificador registrado en la ejecución, que declara 1 presupuesto de VRAM propio por escenario con independencia del presupuesto único del manifiesto de perfil, y que declara de forma reproducible el valor del contexto ajustado.

Resultado esperado: 1 catálogo con 9 escenarios que cubre las 3 × 3 combinaciones, con 9 identificadores distintos y 0 combinaciones duplicadas; 9 presupuestos declarados y 0 escenarios sin presupuesto; 0 selecciones de 1 escenario del catálogo sin el identificador registrado en la ejecución; 0 lanzamientos con el presupuesto declarado por encima de la VRAM disponible; 3 escenarios ajustados con 1 valor numérico de contexto en tokens y su regla de derivación; y 0 escenarios presentados como configuración aprobada sin medición registrada y confirmación escrita del propietario.

La presente redacción fija como requisito que el valor del contexto ajustado y la composición del presupuesto consten declarados y sean reproducibles; la cifra concreta del contexto ajustado y la composición del presupuesto se fijan en la etapa Clarify, no en esta etapa. La feature no declara ninguna combinación como configuración aprobada: esa confirmación corresponde al propietario. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del catálogo ni la aprobación de compuerta alguna.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** fija la cifra del contexto ajustado y la composición del presupuesto por escenario, confirma por escrito qué escenario, si alguno, se presenta como configuración aprobada, aprueba G1 y G4 mediante un commit firmado con una clave de la lista de firmantes autorizados y no delega la firma.
- **Agente `planner`:** redacta los artefactos de esta spec dentro de su carpeta en el registro de specs, escribe la fila del registro de specs y las transiciones del historial; no escribe la sección de aprobaciones y no declara compuertas.
- **Agente `coder`:** escribe el catálogo, el selector, el presupuesto por escenario y sus pruebas automatizadas, y cierra tareas con la evidencia transcrita; no altera los requisitos ni los manifiestos de perfil fuera del alcance declarado por una tarea.
- **Agente `documenter`:** actualiza la línea base documental del modelo y el registro de cambios dentro del alcance que el contrato declare, como delegado explícito del propietario.
- **Agente `reviewer`:** escribe el reporte de validación de esta spec y no altera la matriz ni el dictamen de un reporte ajeno.
- **Orquestador (`sdd`):** verifica G2, G3 y G5, registra el resultado de cada verificación y ejecuta el validador y los commits de control; no redacta artefacto alguno y no declara aprobación.
- **Operador local:** solicita la lista de escenarios, selecciona 1 escenario del catálogo, aporta la medición de cada prueba y transcribe su resultado.

## Requisitos funcionales (EARS)

### RF-001

`El catálogo DEBE declarar 9 escenarios de ejecución, 1 por cada combinación de los 3 valores de capas de expertos en CPU —0, 6 y 9 capas— con los 3 valores de contexto —4096 tokens, 131 072 tokens y contexto ajustado—, incluyendo el escenario de 6 capas y 131 072 tokens con estado inicial no ejecutable, y el número de combinaciones ausentes DEBE ser 0.`

### RF-002

`Cada escenario DEBE declarar 1 identificador único y estable entre los 9 identificadores canónicos —ESC-M0-C4K, ESC-M0-C131K, ESC-M0-CADJ, ESC-M6-C4K, ESC-M6-C131K, ESC-M6-CADJ, ESC-M9-C4K, ESC-M9-C131K, ESC-M9-CADJ—, 1 estado entre los 4 admitidos —declarado, medido, aprobado, no_ejecutable—, el valor de capas de expertos en CPU en capas, el valor de contexto declarado y el contexto efectivo en tokens, y el número de identificadores repetidos entre los 9 escenarios DEBE ser 0.`

### RF-003

`CUANDO el operador selecciona 1 escenario del catálogo mediante argumento CLI o selección interactiva, el sistema DEBE iniciar el servidor con los valores declarados por ese escenario y DEBE registrar en la ejecución el identificador del escenario seleccionado.`

### RF-004

`SI la selección identifica 1 escenario que no figura en el catálogo, ENTONCES el sistema DEBE abortar sin iniciar el servidor, DEBE enumerar los 9 identificadores disponibles y DEBE devolver 1 código de salida distinto de cero.`

### RF-005

`CUANDO el operador solicita la lista de escenarios mediante CLI o menú interactivo, el sistema DEBE enumerar los 9 en 1 orden determinista jerárquico —primero por capas de expertos en CPU ascendente (0, 6, 9) y segundo por contexto efectivo en tokens ascendente (4096, ajustado, 131 072)— y DEBE declarar por escenario su identificador, su estado, sus capas de expertos en CPU, su contexto efectivo en tokens y su presupuesto de VRAM en MiB.`

### RF-006

`El catálogo DEBE declarar 1 presupuesto de VRAM propio en MiB para cada uno de los 9 escenarios con desglose de sus 4 componentes —pesos, cache_kv, computo y reserva— con 1 margen libre mínimo de 512 MiB respecto a la capacidad de la GPU (16 384 MiB) y 1 campo informativo de memoria RAM de sistema requerida en MiB, y el número de escenarios sin presupuesto declarado DEBE ser 0.`

### RF-007

`SI el presupuesto declarado de 1 escenario excede la VRAM disponible de la GPU dedicada o si la RAM libre del host es menor a 8192 MiB al seleccionar capas derivadas a CPU, ENTONCES el sistema NO DEBE iniciar el servidor y DEBE declarar los recursos disponibles y requeridos en MiB.`

### RF-008

`CUANDO se completa la carga de 1 escenario, el sistema DEBE registrar la VRAM asignada, la VRAM libre y la diferencia en MiB entre el consumo medido y el presupuesto declarado de ese escenario, evaluando la conformidad bajo la regla de consumo medido menor o igual al presupuesto declarado.`

### RF-009

`El catálogo DEBE declarar 1 valor nominal base de contexto en tokens para cada escenario de contexto ajustado —8192 tokens para 0 capas, 16 384 tokens para 6 capas y 65 536 tokens para 9 capas— y DEBE registrar la regla determinista que deriva el contexto efectivo en múltiplos de 1024 tokens con suelo mínimo de 4096 tokens a partir del presupuesto y de la VRAM libre real, y el número de escenarios ajustados sin valor nominal o sin regla registrada DEBE ser 0.`

### RF-010

`MIENTRAS 1 escenario de contexto ajustado no declare su valor numérico de contexto en tokens, el sistema NO DEBE permitir su selección y DEBE informar que el escenario no está disponible.`

### RF-011

`El sistema NO DEBE presentar 1 escenario del catálogo como configuración aprobada mientras no conste 1 medición registrada que lo sostenga y el propietario no lo haya confirmado por escrito, pero DEBE permitir la selección y ejecución de cualquier escenario en estado declarado o medido con independencia del estado de aprobación de los perfiles.`

### RF-012

`El catálogo de escenarios DEBE convivir de forma autónoma con los perfiles vigentes en src/gemma/perfiles/, y la modificación o el estado de aprobación de 1 perfil NO DEBE alterar el catálogo, los presupuestos ni los valores declarados por 1 escenario.`

### RF-013

`Cada escenario DEBE declarar explícitamente el valor de los 7 parámetros de ejecución restantes —descarga de capas a GPU (-ngl 99), atención rápida (flash_attn on), micro-lote (ubatch 1120), carga de pesos (mmap según perfil base), ranuras de servidor (parallel 1), tipo de caché clave (cache_type_k q8_0) y tipo de caché valor (cache_type_v q8_0), con draft de 3 tokens si aplica—, y el número de parámetros declarados sin valor DEBE ser 0.`

## Requisitos no funcionales

### RNF-001

`La resolución y la validación de 1 escenario seleccionado DEBEN completarse en 5 segundos o menos antes del lanzamiento del servidor.`

### RNF-002

`El 100 % de los 9 escenarios DEBE declarar identificador, capas de expertos en CPU en capas, contexto efectivo en tokens y presupuesto de VRAM en MiB, y el número de campos vacíos DEBE ser 0.`

### RNF-003

`El número de escenarios del catálogo DEBE ser 9, el número de identificadores distintos DEBE ser 9 y el número de combinaciones duplicadas DEBE ser 0.`

### RNF-004

`El número de escenarios cuyo presupuesto declarado en MiB exceda la VRAM total reportada por la GPU dedicada DEBE ser 0.`

### RNF-005

`El 100 % de los escenarios de contexto ajustado DEBE declarar 1 valor numérico de contexto en tokens y 1 regla de derivación registrada, y el número de escenarios ajustados que carecen de esa regla DEBE ser 0.`

## Casos borde

### CB-001

`SI la VRAM disponible de la GPU dedicada no puede medirse, ENTONCES el sistema NO DEBE iniciar el servidor, DEBE declarar el escenario seleccionado y DEBE declarar la ausencia de la medición sin estimar 1 valor.`

### CB-002

`SI el consumo medido de 1 escenario excede su presupuesto declarado (consumo > presupuesto), ENTONCES el sistema DEBE registrar el exceso en MiB, DEBE conservar la medición y NO DEBE declarar el escenario conforme a su presupuesto.`

### CB-003

`SI el valor numérico resuelto para 1 escenario de contexto ajustado es menor o igual a 4096 tokens, ENTONCES el sistema NO DEBE iniciar el servidor y DEBE declarar el valor resuelto en tokens y el escenario afectado.`

### CB-004

`SI 1 declaración de escenario repite el par de valores de capas de expertos en CPU y contexto de 1 escenario ya declarado, ENTONCES el catálogo DEBE rechazar la declaración y DEBE identificar el identificador duplicado.`

### CB-005

`SI la VRAM disponible cambia entre la selección y el lanzamiento de 1 escenario de contexto ajustado, ENTONCES el sistema DEBE recalcular el valor de contexto antes del lanzamiento y NO DEBE aplicar el valor de la selección anterior.`

### CB-006

`SI 1 escenario medido recibe 1 modificación en sus capas de expertos en CPU, su contexto, sus parámetros de ejecución o su presupuesto, ENTONCES el escenario NO DEBE conservarse como configuración aprobada y DEBE exigirse 1 medición nueva.`

### CB-007

`SI 1 escenario se encuentra en estado no_ejecutable o no alcanza el estado de servicio con su contexto declarado, ENTONCES el sistema DEBE abortar en precheck emitiendo diagnóstico sin intentar iniciar el servidor, DEBE registrar el escenario seleccionado y el contexto solicitado en tokens, NO DEBE declarar el escenario ejecutable y NO DEBE conservar ese intento como medición válida.`

### CB-008

`SI la memoria RAM libre del host es menor a 8192 MiB al seleccionar 1 escenario que deriva capas de expertos a CPU (6 o 9 capas), ENTONCES el sistema NO DEBE iniciar el servidor y DEBE declarar la RAM libre disponible y la RAM requerida en MiB.`

## Fuera de alcance

- Declarar aprobada, medida o canónica 1 combinación del catálogo: la confirmación corresponde al propietario.
- Sustituir, renombrar o retirar los 3 perfiles vigentes de la configuración del modelo.
- Exigir la medición de los 9 escenarios para publicar el catálogo: la medición se exige solo para presentar 1 escenario como configuración aprobada.
- Modificar los valores medidos históricos, los registros de ejecución o la línea base documental fuera del alcance que declare una tarea.
- Declarar compuertas: esta spec no aprueba G1, G4 ni G6.
- Modificar requisitos de una spec publicada para ajustarlos al catálogo implementado.
- Contenido del directorio del repositorio oficial de llama.cpp, que es de solo lectura.
- Versionar modelos, binarios, dependencias, controladores, firmware o credenciales.
- Hardware distinto de la plataforma objetivo declarada.
- La publicación del release de la feature y el cierre de la fase posterior a la confirmación del propietario.

## Criterios de aceptación

### CA-001

`DADO el catálogo de escenarios, CUANDO se contrasta su contenido, ENTONCES declara 9 escenarios que cubren las 3 × 3 combinaciones de 0, 6 y 9 capas de expertos en CPU con 4096 tokens, 131 072 tokens y contexto ajustado, los 9 identificadores corresponden a los identificadores canónicos invariables (ESC-M0-C4K a ESC-M9-CADJ), ninguna combinación está duplicada, cada escenario declara identificador, estado (declarado, medido, aprobado o no_ejecutable), capas, contexto efectivo en tokens y presupuesto en MiB, y el número de campos vacíos y de duplicados es 0.`

Cubre: `RF-001`, `RF-002`, `RNF-002`, `RNF-003`, `CB-004`.

### CA-002

`DADO el catálogo de 9 escenarios, CUANDO el operador solicita la lista o selecciona 1 escenario mediante CLI o menú interactivo, ENTONCES la lista enumera los 9 en el orden determinista jerárquico fijado con identificador, estado, capas de expertos en CPU, contexto efectivo en tokens y presupuesto en MiB, y la selección inicia el servidor con los valores de ese escenario y registra su identificador en la ejecución.`

Cubre: `RF-003`, `RF-005`.

### CA-003

`DADO 1 identificador que no figura en el catálogo, CUANDO se intenta seleccionar, ENTONCES el servidor no se inicia, la salida enumera los 9 identificadores disponibles y el código de salida es distinto de cero.`

Cubre: `RF-004`.

### CA-004

`DADOS el catálogo y los 3 perfiles vigentes, CUANDO se contrastan sus presupuestos y ejecución, ENTONCES cada uno de los 9 escenarios declara su propio presupuesto en MiB con desglose de 4 componentes (pesos, cache_kv, computo, reserva), margen libre mínimo de 512 MiB sobre 16 384 MiB y campo informativo de RAM requerida de sistema, el número de escenarios sin presupuesto es 0, el catálogo convive de forma autónoma con los perfiles, 1 modificación de perfil no altera el escenario, y el número de escenarios cuyo presupuesto excede la VRAM total reportada es 0.`

Cubre: `RF-006`, `RF-012`, `RNF-004`.

### CA-005

`DADO 1 escenario con su presupuesto declarado, CUANDO se lanza y el presupuesto excede la VRAM disponible, la VRAM no puede medirse o la RAM libre del host es menor a 8192 MiB para capas en CPU, ENTONCES el servidor no se inicia, constan los recursos disponibles y requeridos en MiB o la ausencia de la medición, el escenario seleccionado queda declarado y no se estima valor alguno.`

Cubre: `RF-007`, `CB-001`, `CB-008`.

### CA-006

`DADO 1 escenario cargado, CUANDO se completa la carga, ENTONCES constan la VRAM asignada, la VRAM libre y la diferencia en MiB entre el consumo medido y el presupuesto del escenario bajo la regla de consumo menor o igual al presupuesto; si el consumo excede el presupuesto, consta el exceso en MiB, la medición se conserva y el escenario no figura conforme a su presupuesto.`

Cubre: `RF-008`, `CB-002`.

### CA-007

`DADOS los 3 escenarios de contexto ajustado, CUANDO se contrasta el catálogo, ENTONCES cada uno declara su valor nominal base de contexto en tokens (8192, 16 384 o 65 536 tokens) y su regla de derivación en múltiplos de 1024 tokens a partir del presupuesto y de la VRAM libre real, ningún escenario ajustado sin ese valor admite selección, el valor se recalcula antes del lanzamiento si la VRAM disponible cambió, y 1 valor resuelto menor o igual a 4096 tokens impide el lanzamiento con el valor declarado en tokens.`

Cubre: `RF-009`, `RF-010`, `RNF-005`, `CB-003`, `CB-005`.

### CA-008

`DADO 1 escenario del catálogo, CUANDO se contrasta su presentación, ENTONCES no figura como configuración aprobada sin 1 medición registrada y la confirmación escrita del propietario, pero permite la selección y ejecución en estado declarado o medido con independencia de los perfiles; y 1 escenario medido que recibe 1 modificación de sus capas, contexto, parámetros o presupuesto no conserva la condición de aprobado y exige 1 medición nueva.`

Cubre: `RF-011`, `CB-006`.

### CA-009

`DADO 1 escenario del catálogo, CUANDO se resuelve y se contrasta su declaración, ENTONCES declara el valor explícito de los 7 parámetros de ejecución restantes fijados, el número de parámetros sin valor es 0 y la resolución y la validación del escenario se completan en 5 segundos o menos antes del lanzamiento.`

Cubre: `RF-013`, `RNF-001`.

### CA-010

`DADO 1 escenario en estado no_ejecutable o que no alcanza el estado de servicio con su contexto declarado (como ESC-M6-C131K), CUANDO se intenta lanzar, ENTONCES el sistema aborta en precheck con diagnóstico sin iniciar el servidor, constan el escenario seleccionado y el contexto solicitado en tokens, el escenario no figura como ejecutable y ese intento no se conserva como medición válida.`

Cubre: `CB-007`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-25)
- [ ] G4: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha      | Cambio                                                                                                             |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| 0.1.0   | 2026-11-24 | Redacción inicial del contrato del catálogo de escenarios, el selector de escenario y el presupuesto por escenario |
| 0.2.0   | 2026-11-25 | Clarificación de ambigüedades AMB-001 a AMB-012, incorporación de CB-008 y parches aplicados a requisitos          |
| 0.3.0   | 2026-11-25 | Redacción del plan técnico (plan.md) con arquitectura, contratos, decisiones DEC-NNN y matriz de cobertura |
| 0.4.0   | 2026-11-25 | Descomposición en tareas atómicas (tasks.md) con dependencias, estimaciones y cobertura completa |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen      | Destino     | Responsable | Evidencia                                                                                                                             |
| ----------- | ---------- | ----------- | ----------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-11-24  | creación   | —           | `draft`     | `planner`   | redacción inicial de `spec.md` con 13 requisitos funcionales, 5 requisitos no funcionales, 7 casos borde y 10 criterios de aceptación |
| 2026-11-25  | T1         | `draft`     | `clarified` | `planner`   | `clarify.md` cerrado sin casillas abiertas y parches aplicados                                                                        |
| 2026-11-25  | T2         | `clarified` | `planned`   | `planner`   | G1 aprobada y plan.md redactado con arquitectura, contratos y decisiones DEC-NNN |
| 2026-11-25  | T3         | `planned`   | `tasked`    | `planner`   | tasks.md con los campos obligatorios y cobertura completa de requisitos y casos borde |

Las fechas de la tabla del historial de cambios y de la tabla del historial de transiciones se declaran en UTC con la forma `YYYY-MM-DD`.
