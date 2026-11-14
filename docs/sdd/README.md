# Corpus SDD — índice del proyecto LLaMA

Este documento es el **índice del corpus** de `docs/sdd/`. Su función es la navegación del corpus y la declaración del orden de precedencia dentro de cada rango; su contenido descriptivo es referencia no normativa.

## Carácter del índice

- **Navegación.** Enumera cada archivo del corpus con su ruta, su carácter y su orden de lectura.
- **Precedencia entre rangos.** Prevalece el rango de número menor, conforme a la tabla de autoridad.
- **Precedencia dentro de un rango.** Prevalece el documento que este índice sitúa antes en la columna `Orden de lectura`.
- **Desempate.** Una contradicción entre dos documentos del mismo rango se resuelve a favor del que este índice declara antes. Si el rango no tiene orden declarado, el trabajo se detiene y el caso se registra como defecto de la base.
- **Alcance.** El índice no fija reglas de proceso. Las reglas vigentes residen en la constitución, en `AGENTS.md`, en `PROTOCOLO_OPERATIVO.md` y en el flujo Git.

## Tabla de autoridad

| Rango | Documento | Carácter | Precedencia dentro del rango |
|---|---|---|---|
| 1 | `docs/constitution.md` | Norma suprema | Documento único del rango |
| 2 | `AGENTS.md` | Norma operativa para agentes | Documento único del rango |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | Norma ejecutable del proceso | Documento único del rango |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | Norma de integración y release | Documento único del rango |
| 5 | `docs/sdd/plantillas/*.md` | Norma de forma de cada artefacto | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md`, este sobre `validation_report.md`, este sobre `informe_analitico.md` y este sobre `informe_auditoria.md` |
| 6 | `specs/NNN-slug/*.md` | Contrato de la feature | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md` y este sobre `validation_report.md` |
| 7 | `src/`, `tools/`, `tests/`, `.opencode/` | Implementación verificable | El código no prevalece sobre norma alguna; su divergencia se corrige en el código |
| Sin rango | Guías de `docs/sdd/`, informes de análisis, informes de auditoría, `README.md`, `MEMORY.md`, este índice y `CHANGELOG.md` | Referencia no normativa; este índice declara el desempate del rango y `CHANGELOG.md` registra G6 | Sin precedencia: no fija reglas |

## Tabla de inventario

| Archivo | Ruta | Carácter | Orden de lectura | Rango |
|---|---|---|---|---|
| `README.md` | `docs/sdd/README.md` | Índice del corpus; declara la precedencia de cada rango | 1 | Sin rango |
| `PROTOCOLO_OPERATIVO.md` | `docs/sdd/PROTOCOLO_OPERATIVO.md` | Norma ejecutable del proceso | 2 | 3 |
| `spec.md` | `docs/sdd/plantillas/spec.md` | Norma de forma del contrato de la feature | 3 | 5 |
| `clarify.md` | `docs/sdd/plantillas/clarify.md` | Norma de forma de la clarificación | 4 | 5 |
| `plan.md` | `docs/sdd/plantillas/plan.md` | Norma de forma del plan técnico | 5 | 5 |
| `tasks.md` | `docs/sdd/plantillas/tasks.md` | Norma de forma de las tareas | 6 | 5 |
| `validation_report.md` | `docs/sdd/plantillas/validation_report.md` | Norma de forma del reporte de validación | 7 | 5 |
| `informe_analitico.md` | `docs/sdd/plantillas/informe_analitico.md` | Norma de forma del informe analítico | 8 | 5 |
| `informe_auditoria.md` | `docs/sdd/plantillas/informe_auditoria.md` | Norma de forma del informe de auditoría | 9 | 5 |
| `guia_maestra_sdd.md` | `docs/sdd/guia_maestra_sdd.md` | Guía de referencia | 10 | Sin rango |
| `compendio_sdd.md` | `docs/sdd/compendio_sdd.md` | Referencia de fundamentos y taxonomía | 11 | Sin rango |
| `referencia_7_etapas_sdd.md` | `docs/sdd/referencia_7_etapas_sdd.md` | Referencia del ciclo de vida | 12 | Sin rango |
| `referencia_ciclo_vida_sdd_puro.md` | `docs/sdd/referencia_ciclo_vida_sdd_puro.md` | Referencia extendida del ciclo de vida | 13 | Sin rango |
| `evolucion_sdlc_a_sdd.md` | `docs/sdd/evolucion_sdlc_a_sdd.md` | Referencia de evolución metodológica | 14 | Sin rango |
| `guia_constitution_md.md` | `docs/sdd/guia_constitution_md.md` | Guía de referencia | 15 | Sin rango |
| `guia_agents_md.md` | `docs/sdd/guia_agents_md.md` | Guía de referencia | 16 | Sin rango |
| `guia_metodo_ears_sdd.md` | `docs/sdd/guia_metodo_ears_sdd.md` | Guía de referencia de notación EARS | 17 | Sin rango |
| `guia_spec_md.md` | `docs/sdd/guia_spec_md.md` | Guía de referencia del contrato de la feature | 18 | Sin rango |
| `guia_clarify_md.md` | `docs/sdd/guia_clarify_md.md` | Guía de referencia de la clarificación | 19 | Sin rango |
| `guia_plan_md.md` | `docs/sdd/guia_plan_md.md` | Guía de referencia del plan técnico | 20 | Sin rango |
| `guia_tasks_md.md` | `docs/sdd/guia_tasks_md.md` | Guía de referencia de las tareas | 21 | Sin rango |
| `guia_fase_implement_tdd.md` | `docs/sdd/guia_fase_implement_tdd.md` | Guía de referencia de la implementación | 22 | Sin rango |
| `guia_subagentes_opencode_sdd.md` | `docs/sdd/guia_subagentes_opencode_sdd.md` | Guía de referencia de subagentes | 23 | Sin rango |
| `guia_skills_agentes_sdd.md` | `docs/sdd/guia_skills_agentes_sdd.md` | Guía de referencia de skills | 24 | Sin rango |
| `guia_servidores_mcp.md` | `docs/sdd/guia_servidores_mcp.md` | Guía de referencia de servidores MCP | 25 | Sin rango |
| `mapa_mental_sdd.md` | `docs/sdd/mapa_mental_sdd.md` | Referencia gráfica | 26 | Sin rango |
| `diagrama_flujo_ciclo_vida_sdd.md` | `docs/sdd/diagrama_flujo_ciclo_vida_sdd.md` | Referencia gráfica del ciclo de vida | 27 | Sin rango |
| `diagrama_secuencia_subagentes_sdd.md` | `docs/sdd/diagrama_secuencia_subagentes_sdd.md` | Referencia gráfica de subagentes | 28 | Sin rango |
| `comparacion_operativa_sdd_actual_vs_objetivo.md` | `docs/sdd/comparacion_operativa_sdd_actual_vs_objetivo.md` | Informe de análisis | 29 | Sin rango |
| `plan_cierre_brechas_sdd.md` | `docs/sdd/plan_cierre_brechas_sdd.md` | Informe de análisis | 30 | Sin rango |
| `auditoria_cumplimiento_sdd.md` | `docs/sdd/auditoria_cumplimiento_sdd.md` | Informe de auditoría | 31 | Sin rango |
| `firmantes_autorizados` | `docs/sdd/firmantes_autorizados` | Registro de datos con las claves públicas de los firmantes autorizados | 32 | Sin rango |

## Regla de inventario

- El recuento de archivos del corpus se obtiene contando las filas de datos de la tabla de inventario y nunca se escribe como cifra fija.
- Un archivo nuevo de `docs/sdd/` o de `docs/sdd/plantillas/` exige su fila en la tabla antes de aprobar la compuerta en curso.
- Una fila sin archivo o un archivo sin fila es defecto de conformidad y se corrige en este índice.
- La columna `Orden de lectura` es única por archivo y fija el desempate dentro de su rango.
- La columna `Rango` usa un número de 1 a 7 o el valor `Sin rango` de la tabla de autoridad.
