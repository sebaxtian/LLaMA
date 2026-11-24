---
id: SPEC-017
title: Configuración ejecutable y medible de Gemma-4-26B-A4B-it-qat-GGUF
status: clarified
version: 0.11.0
created: 2026-11-20
updated: 2026-11-24
owner: Agent Sebaxtian
branch: feat/gemma-4-26b-a4b-it-qat-gguf
release: ""
supersedes: ""
superseded_by: ""
---

# Configuración ejecutable y medible de Gemma-4-26B-A4B-it-qat-GGUF

## Contexto y objetivo

La feature hace ejecutable, verificable y medible la configuración local del modelo `Gemma-4-26B-A4B-it-qat-GGUF`: 25,23 mil millones de parámetros totales, 8 expertos activos de 128 por capa, cuantización UD-Q4_K_XL, proyector multimodal en BF16 y modelo draft de predicción multitoken, sobre una RTX 5060 Ti de 16 GB de VRAM conectada por eGPU USB4, un procesador Intel Core i9 de 13.ª generación, 32 GB de RAM, Windows 11 y llama.cpp build 12235.

La configuración heredada presenta 7 defectos verificados:

1. Resuelve sus rutas de forma relativa al directorio actual, de modo que solo funciona cuando se invoca desde su propia carpeta.
2. No comprueba la existencia del ejecutable, del archivo de pesos principal, del proyector multimodal ni del modelo draft antes de iniciar el servidor.
3. Su cabecera declara «línea base de producción: perfil rendimiento máximo», mientras la norma del proyecto prohíbe declarar una configuración optimizada sin haberla medido.
4. No registra por ejecución la versión ni el commit de llama.cpp utilizados.
5. Presenta un único perfil sin separar la configuración candidata, el resultado medido y la configuración aprobada.
6. La línea base documental de la feature conserva 400 secuencias corruptas por doble codificación, además de marca de orden de bytes.
7. El perfil declara atención rápida activada, descarga total de capas a la GPU, 9 capas de expertos en CPU, micro-lote de 1 120 tokens, contexto de 131 072 tokens y decodificación especulativa con 3 tokens de borrador, sin contraste medido frente a los parámetros iniciales del proyecto, que declaran atención rápida desactivada, descarga total de capas a la GPU y carga de pesos sin mapa de memoria.

Objetivo: fijar el contrato que hace reproducible la configuración desde cualquier directorio de trabajo, que impide iniciar el servidor con dependencias ausentes o con pesos de una cuantización distinta de la declarada, que registra la versión y el commit de llama.cpp en cada ejecución, que separa configuración candidata, resultado medido y configuración aprobada, y que exige la medición de cada desviación frente a los parámetros iniciales del proyecto antes de declarar 1 perfil como medido.

Resultado esperado: 1 configuración invocable desde cualquier directorio, con 0 ejecuciones iniciadas sobre artefactos ausentes, con 1 registro por ejecución que declara la versión y el commit de llama.cpp, con 1 carga del modelo dentro de la VRAM total reportada por la GPU, con al menos 512 MiB de VRAM libre y sin desbordamiento no documentado hacia memoria compartida, con 1 prueba de contexto sostenido de al menos 2 000 tokens sin detención del servidor, con 1 perfil alternativo sin decodificación especulativa, y con 1 línea base documental sin secuencias corruptas.

La feature no declara la configuración aprobada: la aprobación corresponde al propietario. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad de la configuración ni la aprobación de compuerta alguna.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** confirma que la configuración es satisfactoria para su caso de uso, decide qué perfil es el canónico, aprueba G1 y G4 mediante un commit firmado con una clave de la lista de firmantes autorizados y autoriza el cierre documental de la feature; no delega la firma.
- **Agente `planner`:** redacta los artefactos de esta spec dentro de su carpeta en el registro de specs, escribe la fila del registro de specs y las transiciones T1 a T3 del historial; no escribe la sección de aprobaciones y no declara compuertas.
- **Agente `coder`:** escribe la configuración ejecutable y sus pruebas automatizadas, y cierra tareas con la evidencia transcrita; no altera los requisitos ni la línea base documental fuera del alcance declarado por una tarea.
- **Agente `documenter`:** actualiza la línea base documental de la feature y el registro de cambios dentro del alcance que el contrato declare, como delegado explícito del propietario.
- **Agente `reviewer`:** escribe el reporte de validación de esta spec y no altera la matriz ni el dictamen de un reporte ajeno.
- **Orquestador (`sdd`):** verifica G2, G3 y G5, registra el resultado de cada verificación y ejecuta el validador y los commits de control; no redacta artefacto alguno y no declara aprobación.
- **Operador local:** invoca la configuración desde cualquier directorio de trabajo, aporta la medición de cada prueba y transcribe su resultado.

## Requisitos funcionales (EARS)

### RF-001

`CUANDO se invoca la configuración desde un directorio de trabajo distinto del que contiene sus archivos, el sistema DEBE resolver la raíz del repositorio sin depender del directorio actual ni de la variable de ruta del sistema, y DEBE iniciar el servidor con los 4 artefactos locales —ejecutable, archivo de pesos principal, proyector multimodal y modelo draft— resueltos desde esa raíz.`

### RF-002

`CUANDO se inicia una ejecución, el sistema DEBE comprobar antes del lanzamiento del servidor la existencia del ejecutable, del archivo de pesos principal y del proyector multimodal, y DEBE comprobar además la existencia del modelo draft cuando el perfil seleccionado declare decodificación especulativa.`

### RF-003

`SI falta al menos 1 de los artefactos requeridos por el perfil seleccionado, ENTONCES el sistema DEBE abortar sin lanzar el servidor, DEBE emitir 1 mensaje que identifique el artefacto ausente y DEBE devolver 1 código de salida distinto de cero.`

### RF-004

`CUANDO se completa 1 ejecución, el sistema DEBE registrar en 1 archivo de registro propio de esa ejecución la versión del binario y el identificador de commit de llama.cpp utilizados, y NO DEBE sobrescribir el registro de una ejecución anterior.`

### RF-005

`El sistema DEBE mantener en la línea base documental de la feature 3 secciones distintas —configuración candidata, resultado medido y configuración aprobada— y NO DEBE presentar 1 configuración candidata en la sección de configuración aprobada.`

### RF-006

`El sistema DEBE registrar en cada prueba 1 valor conforme a la columna de contenido obligatorio de la tabla de este requisito, o 1 marca de no disponible, en los 22 campos, y DEBE declarar la unidad en los 13 campos de magnitud: 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19 y 22.`

Campos obligatorios de cada prueba:

| N.º | Campo                                   | Contenido obligatorio                                              |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Fecha de la prueba                      | fecha en la forma `YYYY-MM-DD`                                     |
| 2   | Nombre de la prueba                     | nombre declarado por la prueba                                     |
| 3   | Versión del binario                     | versión declarada por el servidor                                  |
| 4   | Commit de llama.cpp                     | identificador del commit del binario en uso                        |
| 5   | Modelo y cuantización                   | nombre del modelo y cuantización declarada                         |
| 6   | Contexto configurado                    | valor en tokens                                                    |
| 7   | Ranuras del servidor                    | número de ranuras                                                  |
| 8   | Capas de expertos en CPU                | número de capas                                                    |
| 9   | Micro-lote                              | valor en tokens                                                    |
| 10  | Atención rápida                         | estado activado o desactivado                                      |
| 11  | Decodificación especulativa             | estado activado o desactivado, con el techo de tokens del borrador |
| 12  | Tiempo de carga                         | valor en segundos                                                  |
| 13  | VRAM asignada                           | valor en MiB                                                       |
| 14  | VRAM libre                              | valor en MiB                                                       |
| 15  | RAM utilizada                           | valor en MiB                                                       |
| 16  | Velocidad de prompt                     | valor en tokens por segundo                                        |
| 17  | Velocidad de generación                 | valor en tokens por segundo                                        |
| 18  | Estabilidad del servidor                | continúa en servicio o se detuvo                                   |
| 19  | Desbordamiento hacia memoria compartida | valor en MiB                                                       |
| 20  | Calidad funcional de la respuesta       | valoración declarada con su criterio                               |
| 21  | Errores y advertencias                  | mensajes registrados o marca de ausencia                           |
| 22  | Memoria de expertos en host             | valor en MiB                                                       |

### RF-007

`El sistema DEBE declarar el estado de cada perfil de la configuración como candidato, medido o aprobado, y NO DEBE declarar 1 perfil como línea base de producción, como configuración optimizada ni como perfil canónico mientras su medición no conste registrada y el propietario no lo haya confirmado por escrito.`

### RF-008

`MIENTRAS el servidor carga el modelo, CUANDO se completa la asignación de memoria, el sistema DEBE registrar la VRAM asignada, la VRAM libre y la VRAM total reportada por la GPU en MiB, y NO DEBE declarar el perfil cargado cuando la VRAM asignada exceda la VRAM total reportada por la GPU o cuando exista desbordamiento hacia memoria compartida sin registro.`

### RF-009

`CUANDO se ejecuta la prueba de contexto sostenido, el sistema DEBE generar al menos 2 000 tokens en 1 sola solicitud sin que el servidor se detenga, y DEBE registrar la velocidad de generación de esa prueba en tokens por segundo.`

### RF-010

`SI el archivo de pesos principal no corresponde a la cuantización declarada por el perfil, ENTONCES el sistema DEBE abortar antes de lanzar el servidor, DEBE identificar la cuantización declarada y la cuantización leída y DEBE devolver 1 código de salida distinto de cero.`

### RF-011

`DONDE el modelo draft no está disponible, el sistema DEBE ofrecer 1 perfil sin decodificación especulativa que declare únicamente el ejecutable, el archivo de pesos principal y el proyector multimodal, DEBE permitir iniciar ese perfil sin el modelo draft y NO DEBE iniciar el perfil que declara decodificación especulativa.`

### RF-012

`CUANDO 1 perfil se aparta de los parámetros iniciales del proyecto para el mismo modelo —descarga de capas a la GPU, atención rápida, tamaño de contexto, tamaño de micro-lote, capas de expertos en CPU y carga de pesos—, el sistema DEBE registrar 1 prueba comparativa con el valor inicial, el valor propuesto y la diferencia medida de velocidad y de memoria, DEBE registrar además la alternativa de contexto menor medida cuando el perfil declare 131 072 tokens de contexto, y NO DEBE declarar medido ese perfil sin la prueba comparativa registrada.`

### RF-013

`El sistema DEBE registrar 1 verificación de compatibilidad entre las opciones declaradas por 1 perfil y el binario en uso antes de la primera prueba medida de ese perfil.`

### RF-014

`MIENTRAS no conste 1 prueba comparativa registrada de 1 desviación de los parámetros iniciales del proyecto para el mismo modelo, el sistema DEBE aplicar el parámetro inicial del proyecto y NO DEBE aplicar el valor de la desviación.`

## Requisitos no funcionales

### RNF-001

`La comprobación previa de los artefactos requeridos DEBE completarse en 5 segundos o menos antes del lanzamiento del servidor.`

### RNF-002

`El número de secuencias corruptas por doble codificación en la línea base documental DEBE ser 0 y el archivo NO DEBE contener marca de orden de bytes.`

### RNF-003

`El sistema DEBE declarar y sostener 1 derrame no intencional hacia memoria compartida de como máximo 512 MiB, entendido como la diferencia entre el «Shared Usage» del árbol de procesos del servidor y la memoria de expertos en host declarada en el campo 22 de RF-006, y NO DEBE contar como derrame la descarga intencional de expertos a la CPU.`

### RNF-004

`El 100 % de las ejecuciones DEBE dejar 1 archivo de registro propio y el número de registros de ejecuciones anteriores sobrescritos DEBE ser 0.`

### RNF-005

`El 100 % de los campos de la tabla de RF-006 DEBE declarar 1 valor conforme a la columna de contenido obligatorio o 1 marca de no disponible, el número de campos vacíos DEBE ser 0, y los 13 campos de magnitud DEBEN declarar su unidad.`

### RNF-006

`El 100 % de las configuraciones declaradas aprobadas DEBE declarar 1 umbral mínimo de velocidad de generación en tokens por segundo, fijado por el propietario a partir de 1 medición registrada, y el número de configuraciones aprobadas que carecen de ese umbral DEBE ser 0.`

### RNF-007

`El sistema NO DEBE promover 1 perfil al estado aprobado cuya última carga registrada declare menos de 512 MiB de VRAM libre sobre la GPU dedicada, y las cargas registradas que no alcanzan ese umbral DEBEN conservarse como evidencia conforme a RNF-004 sin constituir promoción.`

## Casos borde

### CB-001

`SI el directorio de trabajo contiene 1 archivo con la misma ruta relativa que 1 artefacto de la configuración, ENTONCES el sistema DEBE resolver el artefacto desde la raíz del repositorio y NO DEBE usar el archivo del directorio de trabajo.`

### CB-002

`SI el binario en uso rechaza 1 de las opciones declaradas por el perfil, ENTONCES el sistema DEBE abortar, DEBE identificar la opción rechazada y DEBE devolver 1 código de salida distinto de cero.`

### CB-003

`SI el servidor se detiene durante la prueba de contexto sostenido, ENTONCES la prueba DEBE registrarse como fallida, el perfil NO DEBE promoverse a aprobado y DEBE constar el número de tokens generados antes de la detención.`

### CB-004

`SI la última carga registrada de 1 perfil declara menos de 512 MiB de VRAM libre sobre la GPU dedicada o 1 derrame no intencional hacia memoria compartida superior a 512 MiB, ENTONCES el perfil NO DEBE promoverse al estado aprobado, la medición DEBE conservarse con el valor registrado y cada carga registrada por debajo del umbral DEBE permanecer como evidencia conforme a RNF-004 sin constituir promoción.`

### CB-005

`SI la línea base documental conserva secuencias corruptas al iniciar la feature, ENTONCES su corrección DEBE registrarse como 1 cambio editorial y NO DEBE alterar los valores medidos históricos ni los identificadores de prueba.`

### CB-006

`SI 1 perfil aprobado recibe 1 modificación de sus opciones, ENTONCES su estado DEBE volver a candidato y DEBE exigirse 1 medición nueva antes de declararlo aprobado.`

### CB-007

`SI el tamaño de contexto declarado por 1 perfil excede la VRAM disponible antes de la carga, ENTONCES el servidor NO DEBE iniciarse y DEBEN constar el tamaño de contexto solicitado en tokens y la VRAM disponible en MiB.`

### CB-008

`SI el perfil que declara decodificación especulativa se selecciona sin el modelo draft disponible, ENTONCES el sistema DEBE informar que la alternativa es el perfil sin decodificación especulativa y NO DEBE iniciar el servidor con el perfil especulativo.`

## Fuera de alcance

- Modificar contenido del directorio del repositorio oficial de llama.cpp, que es de solo lectura.
- Versionar modelos, binarios, dependencias, controladores, firmware o credenciales.
- Actualizar el registro de cambios, la descripción del repositorio o el documento maestro de benchmarks antes de la confirmación del propietario.
- Declarar el modelo optimizado o la configuración definitiva.
- Declarar compuertas: esta spec no aprueba G1, G4 ni G6.
- Modificar requisitos de una spec publicada para ajustarlos a la configuración implementada.
- Convertir en configuración aprobada los perfiles históricos de la línea base documental.
- La prueba multimodal como condición de aprobación de la configuración.
- La publicación del release de la feature y el cierre de la fase posterior a la confirmación del propietario.
- Hardware distinto de la plataforma objetivo declarada.

## Criterios de aceptación

### CA-001

`DADO un directorio de trabajo distinto del que contiene los archivos de la configuración, CUANDO se invoca la configuración, ENTONCES el servidor se inicia con los 4 artefactos resueltos desde la raíz del repositorio, la invocación no depende del directorio actual ni de la variable de ruta del sistema, y un archivo del directorio de trabajo con la misma ruta relativa que 1 artefacto no se usa.`

Cubre: `RF-001`, `CB-001`.

### CA-002

`DADO el conjunto de artefactos requeridos por el perfil seleccionado, CUANDO se inicia una ejecución, ENTONCES la existencia de cada artefacto requerido se comprueba en 5 segundos o menos antes del lanzamiento del servidor, y ante 1 artefacto ausente la ejecución se aborta con 1 mensaje que lo identifica y con 1 código de salida distinto de cero.`

Cubre: `RF-002`, `RF-003`, `RNF-001`.

### CA-003

`DADOS la versión del binario y el commit de llama.cpp de una ejecución, CUANDO la ejecución termina, ENTONCES su archivo de registro propio declara la versión y el commit, 2 ejecuciones consecutivas conservan 2 registros con el 100 % de sus datos, y el número de registros anteriores sobrescritos es 0.`

Cubre: `RF-004`, `RNF-004`.

### CA-004

`DADA la línea base documental de la feature, CUANDO se contrasta su estructura, ENTONCES declara 3 secciones distintas —configuración candidata, resultado medido y configuración aprobada—, cada perfil declara su estado como candidato, medido o aprobado, ningún perfil candidato figura en la sección de configuración aprobada ni como línea base de producción, ningún perfil figura como canónico sin la confirmación escrita del propietario, y 1 perfil modificado después de su aprobación vuelve al estado candidato con 1 medición nueva exigida.`

Cubre: `RF-005`, `RF-007`, `CB-006`.

### CA-005

`DADA 1 prueba ejecutada, CUANDO se registra su resultado, ENTONCES consta 1 valor conforme a la columna de contenido obligatorio de la tabla de RF-006, o 1 marca de no disponible, en el 100 % de los 22 campos, los 13 campos de magnitud declaran su unidad, el número de campos vacíos es 0, y la prueba declara su fecha y su nombre.`

Cubre: `RF-006`, `RNF-005`.

### CA-006

`DADA la línea base documental de la feature, CUANDO se inspeccionan su codificación y su texto, ENTONCES el número de secuencias corruptas por doble codificación es 0, el archivo no contiene marca de orden de bytes, y los valores medidos históricos y los identificadores de prueba conservan su contenido.`

Cubre: `RNF-002`, `CB-005`.

### CA-007

`DADO el perfil propuesto para aprobación, CUANDO el servidor completa la carga del modelo, ENTONCES la VRAM asignada, la VRAM libre y la VRAM total reportada por la GPU constan en MiB, la VRAM asignada es menor o igual a la VRAM total reportada por la GPU, la VRAM libre de la última carga registrada es de al menos 512 MiB, 1 derrame no intencional del perfil aprobado es de como máximo 512 MiB, y 1 perfil cuya última carga registrada declare menos de 512 MiB de VRAM libre o 1 derrame no intencional superior a 512 MiB no se promueve al estado aprobado, conserva el valor registrado y mantiene sus cargas registradas por debajo del umbral como evidencia sin que constituyan promoción.`

Cubre: `RF-008`, `RNF-003`, `RNF-007`, `CB-004`.

### CA-008

`DADO el perfil cargado y en servicio, CUANDO se ejecuta la prueba de contexto sostenido, ENTONCES 1 sola solicitud produce al menos 2 000 tokens, el servidor continúa en servicio al finalizar y la velocidad de generación consta en tokens por segundo; si el servidor se detiene, la prueba figura como fallida con el número de tokens generados antes de la detención y el perfil no se promueve a aprobado.`

Cubre: `RF-009`, `CB-003`.

### CA-009

`DADO el archivo de pesos principal, CUANDO su cuantización difiere de la declarada por el perfil, ENTONCES la ejecución se aborta antes del lanzamiento del servidor, se identifican la cuantización declarada y la cuantización leída, y el código de salida es distinto de cero.`

Cubre: `RF-010`.

### CA-010

`DADO un entorno donde el modelo draft no está disponible, CUANDO se inicia la configuración, ENTONCES consta 1 perfil sin decodificación especulativa que declara solo el ejecutable, el archivo de pesos principal y el proyector multimodal, ese perfil se inicia sin el modelo draft, el perfil que declara decodificación especulativa no se inicia, y su selección informa que la alternativa es el perfil sin decodificación especulativa.`

Cubre: `RF-011`, `CB-008`.

### CA-011

`DADOS los parámetros iniciales del proyecto para el modelo, CUANDO 1 perfil se aparta de ellos en descarga de capas a la GPU, atención rápida, tamaño de contexto, tamaño de micro-lote, capas de expertos en CPU o carga de pesos, ENTONCES consta 1 prueba comparativa con el valor inicial, el valor propuesto y la diferencia medida de velocidad y de memoria, consta la alternativa de contexto menor medida cuando el perfil declara 131 072 tokens de contexto, y el perfil no figura como medido sin esa prueba.`

Cubre: `RF-012`.

### CA-012

`DADO el binario en uso, CUANDO se declara 1 perfil como medido, ENTONCES consta 1 verificación de compatibilidad de sus opciones con ese binario antes de la primera prueba medida, y ante 1 opción rechazada la ejecución se aborta con la opción identificada y con 1 código de salida distinto de cero.`

Cubre: `RF-013`, `CB-002`.

### CA-013

`DADO el tamaño de contexto declarado por 1 perfil, CUANDO ese tamaño excede la VRAM disponible antes de la carga, ENTONCES el servidor no se inicia y constan el tamaño de contexto solicitado en tokens y la VRAM disponible en MiB.`

Cubre: `CB-007`.

### CA-014

`DADOS los parámetros iniciales del proyecto para el modelo y 1 perfil que se aparta de ellos, CUANDO 1 desviación carece de prueba comparativa registrada, ENTONCES la configuración ejecutable aplica el parámetro inicial del proyecto, el valor de la desviación no se aplica y el perfil no figura como medido.`

Cubre: `RF-014`, `RF-012`.

### CA-015

`DADA 1 configuración declarada aprobada, CUANDO se contrasta su registro, ENTONCES consta 1 umbral mínimo de velocidad de generación en tokens por segundo fijado por el propietario a partir de 1 medición registrada, y el número de configuraciones aprobadas que carecen de ese umbral es 0.`

Cubre: `RNF-006`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-24)
- [ ] G4: `- Approved by: Agent Sebaxtian` ()

## Historial de cambios

| Versión | Fecha      | Cambio                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1.0   | 2026-11-20 | Redacción inicial de la spec                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 0.2.0   | 2026-11-20 | Clarificación cerrada: doce ambigüedades resueltas y parches aplicados a los requisitos y criterios afectados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 0.3.0   | 2026-11-20 | Plan técnico redactado: catorce decisiones, diez contratos, estrategia de testing y matriz de cobertura de los veintinueve requisitos y casos borde                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0.4.0   | 2026-11-20 | Tareas redactadas: cuarenta y dos tareas atómicas con dependencias acíclicas, reparto de roles y cobertura de los catorce requisitos funcionales, los siete no funcionales, los ocho casos borde y los quince criterios de aceptación                                                                                                                                                                                                                                                                                                                                                                                                             |
| 0.5.0   | 2026-11-23 | Reformulación de `RNF-003` como derrame no intencional de como máximo 512 MiB y ampliación de `RF-006` a 22 campos con la memoria de expertos en host en MiB, aprobadas por el propietario; la spec vuelve a `draft` y exige nueva clarificación y nueva aprobación de G1                                                                                                                                                                                                                                                                                                                                                                         |
| 0.6.0   | 2026-11-23 | Cierre de la clarificación reabierta por `T11`: `RNF-003` reformulado como derrame no intencional de 512 MiB y `RF-006` ampliado a 22 campos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 0.8.0   | 2026-11-24 | Plan y tareas actualizados: tabla de 22 campos en `C-6`, decisión `DEC-026` que fija `ncmoe` `6` y correcciones de `T-060` a `T-073`; se registra que la implementación de esas tareas precedió a la transición porque la reapertura por `T11` devolvió la spec a `draft` y las etapas Plan y Tasks se recorren después, sin alterar las tareas ya cerradas                                                                                                                                                                                                                                                                                       |
| 0.9.0   | 2026-11-24 | Transición `tasked` → `implementing` por `T4`: `T-043` cerrada con la evidencia del operador y las 81 tareas completadas; la etapa Implement se registra al cierre de la implementación porque la reapertura por `T11` devolvió la spec a `draft` y las etapas posteriores se recorrieron después, sin reescribir las tareas ya cerradas; G3 no se declara y su verificación corresponde al orquestador                                                                                                                                                                                                                                           |
| 0.9.1   | 2026-11-24 | Transición `implementing` → `implemented` por `T5`: 81 de 81 tareas cerradas con su evidencia transcrita y G3 verificada por el orquestador con `OK: sin hallazgos`; la versión incrementa PATCH y no MINOR porque la etapa Implement no cambia el contrato —la regla de versionado reserva el incremento MINOR a clarify, plan, tasks y validación— y esta fila solo registra el cierre de la etapa y su evidencia, sin modificar requisitos, casos borde ni criterios de aceptación; G4 no se declara y su aprobación corresponde al propietario                                                                                                |
| 0.10.0  | 2026-11-24 | Reapertura por `T11`: reformulación de `RNF-007` aprobada por el propietario, que sustituye el recuento histórico de cargas con menos de 512 MiB de VRAM libre por una condición de promoción —ningún perfil se promueve al estado aprobado si su última carga registrada declara menos de 512 MiB de VRAM libre— y conserva las cargas por debajo del umbral como evidencia conforme a `RNF-004`; parches a `CA-007` y a `CB-004`; la spec vuelve a `draft` y exige nueva clarificación y nueva aprobación de G1, de modo que la aprobación G1 registrada, la verificación G3 y el informe de validación dejan de cubrir el contrato reformulado |
| 0.11.0  | 2026-11-24 | Cierre de la clarificación reabierta por `T11`: `RNF-007` reformulado como condición de promoción —ningún perfil se promueve al estado aprobado si su última carga registrada declara menos de 512 MiB de VRAM libre sobre la GPU dedicada, y las cargas por debajo del umbral se conservan como evidencia conforme a `RNF-004`— y parches a `CA-007` y a `CB-004` para leer ese umbral sobre la última carga registrada del perfil; `AMB-014` queda cerrada con las 13 cargas por debajo del umbral enumeradas en `clarify.md`; la spec pasa a `clarified` y la nueva aprobación firmada de G1 queda pendiente del propietario                   |

### Historial de transiciones

| Fecha (UTC) | Transición             | Origen         | Destino        | Responsable   | Evidencia                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------- | ---------------------- | -------------- | -------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-11-20  | creación               | —              | `draft`        | `planner`     | redacción inicial de `spec.md` con trece requisitos funcionales, cinco requisitos no funcionales, ocho casos borde y trece criterios de aceptación                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 2026-11-20  | T1                     | `draft`        | `clarified`    | `planner`     | `clarify.md` cerrado sin casillas pendientes, doce ambigüedades resueltas y parches aplicados a `spec.md`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 2026-11-20  | T2                     | `clarified`    | `planned`      | `planner`     | G1 firmada en la sección de aprobaciones de `spec.md` y verificada en el commit `eccae87`; `plan.md` redactado con catorce decisiones, diez contratos, estrategia de testing y matriz de cobertura de los catorce requisitos funcionales, los siete requisitos no funcionales y los ocho casos borde                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 2026-11-20  | T3                     | `planned`      | `tasked`       | `planner`     | `tasks.md` redactado con cuarenta y dos tareas atómicas, los ocho campos por tarea, dependencias acíclicas, reparto de roles y cobertura de los catorce requisitos funcionales, los siete requisitos no funcionales, los ocho casos borde y los quince criterios de aceptación                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 2026-11-23  | reversión de requisito | `tasked`       | `draft`        | `planner`     | reformulación de `RNF-003` y ampliación de `RF-006` a 22 campos aprobadas por el propietario; la spec reabre la clarificación y G1 queda pendiente de nueva aprobación firmada                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 2026-11-23  | T1                     | `draft`        | `clarified`    | `propietario` | cierre de la clarificación con la reformulación aprobada; G1 pendiente de firma en el commit de aprobación                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 2026-11-24  | T2                     | `clarified`    | `planned`      | `planner`     | `plan.md` actualizado con la tabla de 22 campos de `C-6` y con `DEC-026`, que fija `ncmoe` `6` en el perfil `resiliencia`; la transición se registra después de que `T-060` a `T-073` se implementaran, porque la reapertura por `T11` devolvió la spec a `draft` y las etapas Plan y Tasks se recorren a continuación sin reescribir las tareas ya cerradas; G2 no se declara y su verificación corresponde al orquestador                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 2026-11-24  | T3                     | `planned`      | `tasked`       | `planner`     | `tasks.md` actualizado con las correcciones de `T-060` a `T-073` y con la evidencia de `T-037` transcrita de la ejecución del operador; la transición se registra después de esa implementación por la reapertura de la spec, no antes; G2 no se declara y la verificación de la compuerta corresponde al orquestador                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 2026-11-24  | T4                     | `tasked`       | `implementing` | `propietario` | implementación completada y registrada al cierre, porque la reapertura por `T11` devolvió la spec a `draft` y las etapas Plan y Tasks se recorrieron después de implementadas las tareas; 81 de 81 tareas cerradas, `T-043` incluida con la evidencia del operador del 2026-11-24 —`5 de 5` comprobaciones superadas sin `PENDIENTE` y servicio desde `tmp\senuelo` con derrame de `274.62 MiB` y VRAM libre de `3889 MiB`—; G3 no se declara y su verificación corresponde al orquestador                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 2026-11-24  | T5                     | `implementing` | `implemented`  | `propietario` | G3 verificada por el orquestador con `python tools\sdd\validate.py --spec SPEC-017 --gate G3`, que devolvió `OK: sin hallazgos`; 81 de 81 tareas cerradas con su evidencia transcrita; suite de pruebas en verde en la última ejecución registrada; G4 no se declara y su aprobación corresponde al propietario                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 2026-11-24  | T11                    | `implemented`  | `draft`        | `propietario` | reformulación de `RNF-007` aprobada por el propietario: el requisito pasa de exigir 0 cargas registradas con menos de 512 MiB de VRAM libre a prohibir la promoción de 1 perfil cuya última carga registrada declare menos de 512 MiB de VRAM libre, con las cargas por debajo del umbral conservadas como evidencia conforme a `RNF-004`; parches a `CA-007` y a `CB-004`; la aprobación G1 registrada, la verificación G3 y el informe de validación dejan de cubrir el contrato reformulado y la nueva aprobación firmada de G1 queda pendiente del propietario                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 2026-11-24  | T1                     | `draft`        | `clarified`    | `propietario` | cierre de la clarificación reabierta por `T11`: `AMB-014` cerrada con las 13 cargas por debajo del umbral de 512 MiB enumeradas —`20261122T203814Z-resiliencia-carga-inicial` con `56 MiB`, `20261124T174952Z-rendimiento-comparacion-micro-lote` con `389 MiB`, `20261124T175021Z-rendimiento-comparacion-micro-lote` con `53 MiB`, `20261124T192807Z-rendimiento-comparacion-contexto` con `336 MiB`, `20261123T144036Z-resiliencia-comparacion-ncmoe` y `20261123T144150Z-resiliencia-comparacion-ncmoe` con `133 MiB` cada una, `20261123T164756Z`, `20261123T164947Z`, `20261123T171120Z` y `20261123T171245Z` de la serie `resiliencia-comparacion-ncmoe` con `25 MiB` cada una, `20261124T113511Z-rendimiento-comparacion-ncmoe` con `25 MiB`, y `20261124T190815Z-resiliencia-comparacion-ncmoe` y `20261124T191036Z-rendimiento-comparacion-ncmoe` con `389 MiB` cada una—; texto vigente de `RNF-007`: «el sistema NO DEBE promover 1 perfil al estado aprobado cuya última carga registrada declare menos de 512 MiB de VRAM libre sobre la GPU dedicada, y las cargas registradas que no alcanzan ese umbral DEBEN conservarse como evidencia conforme a `RNF-004` sin constituir promoción»; la aprobación G1 registrada y la verificación G3 dejan de cubrir el contrato reformulado y G1 queda pendiente de firma en el commit de aprobación |

Las fechas de la tabla del historial de cambios y de la tabla del historial de transiciones se declaran en UTC con la forma `YYYY-MM-DD`.
