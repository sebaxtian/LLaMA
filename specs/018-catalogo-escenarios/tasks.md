# Tareas — SPEC-018

*Plantilla de rango 5: norma de forma del artefacto `tasks.md`. Cada tarea declara los ocho campos en el orden indicado y se cierra solo con la evidencia transcrita.*

## Progreso

- Cerradas: 6 de 16 tareas.

## Tareas

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-006`, `RF-013`, `RNF-002`, `RNF-003`, `RNF-004`.
- **Criterio de aceptación:** `CA-001`, `CA-004`, `CA-009`.
- **Archivos:** `tools/gemma/tests/test_escenarios.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestCatalogoEstructura` en rojo con fallo por ausencia de `src/gemma/escenarios/catalogo.json`.
- **Evidencia:** `python -m unittest tools.gemma.tests.test_escenarios.TestCatalogoEstructura` imprimió `FFFFFFF` y 7 fallos, 1 por prueba de `TestCatalogoEstructura` —`test_campos_obligatorios_sin_vacios`, `test_conteo_exacto_nueve_escenarios`, `test_identificadores_canonicos_y_estados`, `test_nueve_escenarios_cobertura_completa`, `test_presupuestos_no_exceden_capacidad_gpu`, `test_presupuestos_vram_desglose_y_ram_sistema` y `test_siete_parametros_ejecucion_declarados`—, cada uno con `AssertionError: False is not true : falta el catálogo de escenarios: C:\Users\sebax\Documents\Workspaces\LLaMA\src\gemma\escenarios\catalogo.json` en `_catalogo`; el cierre fue `Ran 7 tests in 0.013s` y `FAILED (failures=7)` con código de salida `1`. El rojo acredita que `src/gemma/escenarios/catalogo.json` todavía no existe, cuya escritura corresponde a `T-002`, y que la suite declara el contrato `C-1` en rojo: 9 escenarios de la matriz 3 × 3 (0, 6 y 9 capas de expertos en CPU × 4096, ajustado y 131 072 tokens), los 9 identificadores canónicos con `ESC-M6-C131K` en `no_ejecutable` y el resto en `declarado`, presupuesto de VRAM en los 4 componentes `pesos_mib`, `cache_kv_mib`, `computo_mib` y `reserva_mib` con suma igual al total y margen libre mínimo de 512 MiB sobre 16 384 MiB, `ram_sistema_requerida_mib`, los 7 parámetros de ejecución obligatorios con su valor fijo y 0 campos vacíos. No se escribió `src/gemma/escenarios/catalogo.json` ni se ejecutó `git add` ni `git commit`.
- [x] Completada.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-006`, `RF-012`, `RF-013`, `RNF-002`, `RNF-003`, `RNF-004`.
- **Criterio de aceptación:** `CA-001`, `CA-004`, `CA-009`.
- **Archivos:** `src/gemma/escenarios/catalogo.json`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestCatalogoEstructura` en verde con `OK`: verifica 9 escenarios únicos (3×3), 9 IDs canónicos invariables, presupuestos desglosados en 4 componentes con margen libre >= 512 MiB sobre 16 384 MiB, RAM de host, los 7 parámetros de ejecución obligatorios y `ESC-M6-C131K` en `no_ejecutable`.
- **Evidencia:** `python -m unittest tools.gemma.tests.test_escenarios.TestCatalogoEstructura` imprimió `.......`, 1 punto por prueba en verde de `TestCatalogoEstructura` —`test_campos_obligatorios_sin_vacios`, `test_conteo_exacto_nueve_escenarios`, `test_identificadores_canonicos_y_estados`, `test_nueve_escenarios_cobertura_completa`, `test_presupuestos_no_exceden_capacidad_gpu`, `test_presupuestos_vram_desglose_y_ram_sistema` y `test_siete_parametros_ejecucion_declarados`—, con el cierre `Ran 7 tests in 0.004s` y `OK`, sin fallos ni errores, y código de salida `0`. Se creó `src/gemma/escenarios/catalogo.json` en UTF-8 sin BOM y sin comentarios, con las claves raíz `version`, `modelo`, `descripcion` y `escenarios`; declara los 9 escenarios de la matriz 3 × 3 —`ESC-M0-C4K`, `ESC-M0-CADJ` y `ESC-M0-C131K` con 0 capas de expertos en CPU, `ESC-M6-C4K`, `ESC-M6-CADJ` y `ESC-M6-C131K` con 6 capas, y `ESC-M9-C4K`, `ESC-M9-CADJ` y `ESC-M9-C131K` con 9 capas—, con `ESC-M6-C131K` en estado `no_ejecutable` y los otros 8 en estado `declarado`; los contextos fijos de 4096 y 131 072 tokens declaran el efectivo igual al declarado y los ajustados declaran 8192, 16 384 y 65 536 tokens con la regla `multiplos_1024_suelo_4096`; cada presupuesto desglosa `pesos_mib`, `cache_kv_mib`, `computo_mib` y `reserva_mib` con suma igual a `total_mib` y margen libre sobre 16 384 MiB de 2184, 1584, 784, 5184, 3584, 584, 6784, 1884 y 884 MiB respectivamente; `ram_sistema_requerida_mib` declara `0` en los 3 escenarios de 0 capas, `3500` en los 3 de 6 capas y `5200` en los 3 de 9 capas; y los 9 escenarios declaran los 7 parámetros obligatorios —`gpu_layers` 99, `flash_attn` `on`, `ubatch` 1120, `load_mode` `none`, `parallel` 1, `cache_type_k` `q8_0` y `cache_type_v` `q8_0`— más `spec_draft_n_max` 3, conforme a `DEC-011`. `git status --short` informó `?? src/gemma/escenarios/` como única variación de la implementación; no se modificó `tools/gemma/tests/test_escenarios.py` ni artefacto alguno fuera de `src/gemma/escenarios/catalogo.json` y `tasks.md`, y no se ejecutó `git add` ni `git commit`.
- [x] Completada.

### T-003

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-005`, `RF-011`, `CB-004`, `CB-006`, `RNF-001`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-008`, `CA-009`.
- **Archivos:** `tools/gemma/tests/test_escenarios.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestOrdenamientoEscenarios tools.gemma.tests.test_escenarios.TestAdmisibilidadEscenarios` en rojo por ausencia del módulo `tools/gemma/escenarios.py`.
- **Evidencia:** `python -m unittest tools.gemma.tests.test_escenarios` imprimió `EEEEE.......EEEEEEE` y el cierre `Ran 19 tests in 0.532s` y `FAILED (errors=12)` con código de salida `1`. Los 12 errores son 1 por prueba de las 2 clases nuevas —5 de `TestAdmisibilidadEscenarios` (`test_aprobado_sin_aprobacion_no_es_seleccionable`, `test_catalogo_real_declara_la_admisibilidad_por_estado`, `test_escenario_declarado_es_seleccionable`, `test_escenario_medido_es_seleccionable` y `test_escenario_no_ejecutable_no_es_seleccionable`) y 7 de `TestOrdenamientoEscenarios` (`test_carga_del_catalogo_canonico`, `test_carga_rechaza_json_invalido`, `test_carga_rechaza_manifiesto_ausente`, `test_declaracion_duplicada_del_par_se_rechaza`, `test_identificador_ausente_no_se_resuelve_y_enumera_los_nueve`, `test_orden_independe_del_orden_de_declaracion` y `test_orden_jerarquico_determinista`)—, los 12 con `ModuleNotFoundError: No module named 'escenarios'` en `_cargar_modulo` (`tools/gemma/tests/test_escenarios.py:593`, instrucción `import escenarios`) invocado desde `setUp` (`test_escenarios.py:843` en `TestAdmisibilidadEscenarios` y `test_escenarios.py:627` en `TestOrdenamientoEscenarios`). Los 7 puntos corresponden a las 7 pruebas de `TestCatalogoEstructura`, que siguen en verde porque no importan el módulo. El rojo acredita que `tools/gemma/escenarios.py` todavía no existe, cuya escritura corresponde a `T-004`, y que las 12 pruebas nuevas declaran en rojo el contrato `C-3` del plan: `cargar_catalogo(ruta_catalogo: Path | None = None) -> dict` desde la ruta canónica con error explícito ante manifiesto ausente y ante JSON inválido, `listar_escenarios(catalogo: dict) -> list[dict]` con orden jerárquico determinista —capas de expertos en CPU ascendente 0, 6 y 9 y, dentro de cada valor, contexto efectivo ascendente 4096, ajustado y 131 072 tokens— independiente del orden de declaración, rechazo de la declaración duplicada del par de capas y contexto identificando el identificador duplicado (`CB-004`), no resolución del identificador ausente con los 9 identificadores disponibles (`RF-004`) y `validar_admisibilidad_escenario(escenario) -> tuple[bool, str]` con `declarado` y `medido` seleccionables, `no_ejecutable` rechazado con motivo declarado y `aprobado` sin bloque `aprobacion` rechazado (`RF-011`, `CB-006`, `CA-008`). Se añadieron las 2 clases al final de `tools/gemma/tests/test_escenarios.py`, con `sys` y `tempfile` en los imports, las constantes `DIRECTORIO_HERRAMIENTAS`, `DIRECTORIO_TMP`, `ORDEN_CANONICO`, `CAMPOS_LISTADO` e `IDENTIFICADOR_AUSENTE` y los auxiliares `_cargar_modulo` y `_escenario_con_estado`; no se escribió `tools/gemma/escenarios.py`, no se modificó `src/gemma/escenarios/catalogo.json` ni artefacto alguno fuera de `tools/gemma/tests/test_escenarios.py` y `specs/018-catalogo-escenarios/tasks.md`, y no se ejecutó `git add` ni `git commit`.
- [x] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-005`, `RF-011`, `CB-004`, `CB-006`, `RNF-001`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-008`, `CA-009`.
- **Archivos:** `tools/gemma/escenarios.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestOrdenamientoEscenarios tools.gemma.tests.test_escenarios.TestAdmisibilidadEscenarios` en verde con `OK`: valida carga, orden jerárquico determinista (MoE CPU asc, contexto efectivo asc), detección y rechazo de duplicados (`CB-004`) y revocación de estado aprobado ante modificaciones (`CB-006`).
- **Evidencia:** `python -m unittest tools.gemma.tests.test_escenarios` imprimió `...................`, 1 punto por cada una de las 19 pruebas de la suite —las 7 de `TestCatalogoEstructura`, las 7 de `TestOrdenamientoEscenarios` y las 5 de `TestAdmisibilidadEscenarios`—, con el cierre `Ran 19 tests in 0.041s` y `OK`, sin fallos ni errores, y código de salida `0`. Se creó `tools/gemma/escenarios.py` con el contrato `C-3`: `cargar_catalogo(ruta_catalogo=None)` resuelve la ruta canónica `src/gemma/escenarios/catalogo.json` con `Path(__file__).resolve().parents[2]`, lee el manifiesto en UTF-8 y devuelve su objeto raíz tras validar las claves raíz `version`, `modelo` y `escenarios`, los campos obligatorios de cada escenario —`id` coincidente con su clave, `estado` entre los 4 admitidos, `capas_cpu_moe` entero no negativo, `contexto` con `tipo` `fijo` o `ajustado` y `declarado_tokens` y `efectivo_tokens` enteros positivos, `presupuesto_vram` con `total_mib` positivo y los 4 componentes `pesos_mib`, `cache_kv_mib`, `computo_mib` y `reserva_mib` enteros no negativos cuya suma iguala el total, `ram_sistema_requerida_mib` entero no negativo y `parametros_ejecucion` no vacío— y el par (capas de expertos en CPU, contexto efectivo) de los 9 escenarios, de modo que la declaración repetida del par aborta con `ValueError` que nombra los identificadores implicados (`CB-004`); el manifiesto ausente, ilegible o no UTF-8 y el JSON inválido abortan con `ValueError` que nombra el archivo. `listar_escenarios(catalogo)` devuelve exactamente `ESC-M0-C4K`, `ESC-M0-CADJ`, `ESC-M0-C131K`, `ESC-M6-C4K`, `ESC-M6-CADJ`, `ESC-M6-C131K`, `ESC-M9-C4K`, `ESC-M9-CADJ` y `ESC-M9-C131K` por orden de `capas_cpu_moe` ascendente y, dentro de cada valor, de `contexto.efectivo_tokens` ascendente con el identificador como desempate, independiente del orden de declaración del JSON (`DEC-004`), y cada entrada declara `id`, `estado`, `capas_cpu_moe`, `contexto` y `presupuesto_vram` (`RF-005`). `validar_admisibilidad_escenario(escenario)` devuelve `(True, "")` para los estados `declarado` y `medido`, `(False, motivo)` con motivo no vacío para `no_ejecutable` y `(False, motivo)` para `aprobado` cuyo bloque `aprobacion` es nulo, al que exige 1 medición nueva y la confirmación escrita del propietario (`RF-011`, `CB-006`). La suite no se modificó y no se ejecutó `git add` ni `git commit`.
- [x] Completada.

### T-005

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-009`, `RF-010`, `RNF-005`, `CB-003`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/gemma/tests/test_escenarios.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` en rojo por ausencia de las funciones de derivación y validación de contexto ajustado en `tools/gemma/escenarios.py`.
- **Evidencia:** `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` imprimió `.EFEEEEEEEEEEEEEEEEEEEEE` y el cierre `Ran 6 tests in 0.019s` y `FAILED (failures=1, errors=22)` con código de salida `1`. Los 22 errores son 1 por cada subprueba que invoca `resolver_contexto_ajustado`: 1 de `test_contexto_resuelto_menor_o_igual_4096_aborta`, 3 de `test_menos_vram_decrece_sin_superar_la_base` —1 por `ESC-M0-CADJ`, `ESC-M6-CADJ` y `ESC-M9-CADJ`—, 15 de `test_resultado_siempre_multiplo_de_1024` —5 por escenario con 13 600, 13 855, 14 450, 12 000 y 16 384 MiB libre en `ESC-M0-CADJ`, 10 600, 10 855, 11 450, 12 000 y 16 384 MiB en `ESC-M6-CADJ` y 9000, 9255, 9850, 12 000 y 16 384 MiB en `ESC-M9-CADJ`— y 3 de `test_valores_nominales_y_regla_derivacion` —1 por escenario ajustado—, los 22 con `AttributeError: module 'escenarios' has no attribute 'resolver_contexto_ajustado'` en `_resolver` (`tools/gemma/tests/test_escenarios.py:1065`), invocado desde `test_escenarios.py:1288`, `test_escenarios.py:1243`, `test_escenarios.py:1210` y `test_escenarios.py:1142`. El fallo restante es `test_escenario_ajustado_sin_valor_no_seleccionable`, con `AssertionError: True is not false : 1 escenario ajustado sin valor numérico resuelto figura como seleccionable` en `test_escenarios.py:1369`, porque `validar_admisibilidad_escenario` todavía no rechaza el escenario ajustado cuyo `contexto.efectivo_tokens` no declara valor numérico (`RF-010`). El punto restante corresponde a `test_cien_por_ciento_ajustados_con_regla` (`RNF-005`), que contrasta el catálogo real sin invocar las funciones nuevas. La suite completa, `python -m unittest tools.gemma.tests.test_escenarios`, imprimió `.............EFEEEEEEEEEEEEEEEEEEEEE.......` con `Ran 25 tests in 0.035s` y `FAILED (failures=1, errors=22)`; la ejecución de las 3 clases previas, `python -m unittest tools.gemma.tests.test_escenarios.TestCatalogoEstructura tools.gemma.tests.test_escenarios.TestOrdenamientoEscenarios tools.gemma.tests.test_escenarios.TestAdmisibilidadEscenarios`, imprimió `...................` con `Ran 19 tests in 0.023s` y `OK`, de modo que las 19 pruebas anteriores siguen en verde. Se añadió `TestContextoAjustado` a `tools/gemma/tests/test_escenarios.py` con 6 pruebas que declaran el contrato `C-3` y `DEC-008`: `resolver_contexto_ajustado(escenario, vram_libre_mib, consumo_kv_por_1024_mib=85.0) -> int` deriva en múltiplos de 1024 tokens la VRAM disponible para la caché KV —VRAM libre menos `total_mib - cache_kv_mib` del presupuesto—, acotada por el valor nominal base de 8192, 16 384 y 65 536 tokens según 0, 6 y 9 capas de expertos en CPU, sin aplicar suelo; `validar_contexto_ajustado(escenario, tokens_resueltos) -> tuple[bool, str]` devuelve `(True, "")` por encima de 4096 tokens y `(False, motivo)` cuando el valor resuelto es menor o igual a 4096 tokens, con el valor en tokens y el identificador del escenario en el motivo (`CB-003`); y `validar_admisibilidad_escenario(escenario)` debe devolver `(False, motivo)` para el escenario ajustado sin valor numérico resuelto (`RF-010`). Las 6 pruebas son `test_valores_nominales_y_regla_derivacion`, `test_cien_por_ciento_ajustados_con_regla`, `test_resultado_siempre_multiplo_de_1024`, `test_menos_vram_decrece_sin_superar_la_base`, `test_contexto_resuelto_menor_o_igual_4096_aborta` y `test_escenario_ajustado_sin_valor_no_seleccionable`, nombres que figuran en la matriz de trazabilidad de `plan.md`. No se modificó `tools/gemma/escenarios.py` ni artefacto alguno fuera de `tools/gemma/tests/test_escenarios.py` y de este `tasks.md`; no se ejecutó `git add` ni `git commit`.
- [x] Completada.

### T-006

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-009`, `RF-010`, `RNF-005`, `CB-003`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/gemma/escenarios.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` en verde con `OK`: valida derivación en múltiplos de 1024 tokens con valores base (8192, 16 384, 65 536 tokens), detección de contexto resuelto <= 4096 tokens e inadmisibilidad de selección para escenarios ajustados sin valor numérico.
- **Evidencia:** `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` imprimió `......`, 1 punto por cada una de las 6 pruebas de `TestContextoAjustado` —`test_valores_nominales_y_regla_derivacion`, `test_cien_por_ciento_ajustados_con_regla`, `test_resultado_siempre_multiplo_de_1024`, `test_menos_vram_decrece_sin_superar_la_base`, `test_contexto_resuelto_menor_o_igual_4096_aborta` y `test_escenario_ajustado_sin_valor_no_seleccionable`—, con el cierre literal `Ran 6 tests in 0.007s` y `OK`, sin fallos ni errores, y código de salida `0`. `python -m unittest tools.gemma.tests.test_escenarios` imprimió `.........................`, 1 punto por cada una de las 25 pruebas de la suite —las 7 de `TestCatalogoEstructura`, las 7 de `TestOrdenamientoEscenarios`, las 5 de `TestAdmisibilidadEscenarios` y las 6 de `TestContextoAjustado`—, con el cierre literal `Ran 25 tests in 0.020s` y `OK`, sin fallos ni errores, y código de salida `0`. Se completó `tools/gemma/escenarios.py` con el contrato `C-3` del contexto ajustado: `resolver_contexto_ajustado(escenario, vram_libre_mib, consumo_kv_por_1024_mib=85.0)` calcula la VRAM de la caché KV como `vram_libre_mib - (presupuesto_vram.total_mib - desglose.cache_kv_mib)`, deriva `bloques = floor(vram_kv / consumo_kv_por_1024_mib)`, devuelve `min(contexto.declarado_tokens, max(bloques, 0) * 1024)` y no aplica suelo, de modo que con 16 384 MiB libres alcanza los valores nominales de 8192, 16 384 y 65 536 tokens de `ESC-M0-CADJ`, `ESC-M6-CADJ` y `ESC-M9-CADJ`, decrece en múltiplos de 1024 al reducir la VRAM libre, nunca supera la base ni produce negativos y declara 0 tokens con la VRAM justa; `validar_contexto_ajustado(escenario, tokens_resueltos)` devuelve `(True, "")` por encima de 4096 tokens y `(False, motivo)` en 1024, 3072 y 4096 tokens, con el valor resuelto y el identificador del escenario en el motivo (`CB-003`); y `validar_admisibilidad_escenario` devuelve `(False, motivo)` cuando 1 escenario de contexto ajustado no declara valor numérico positivo en `declarado_tokens` o `efectivo_tokens`, con el término `contexto` en el motivo, sin alterar la admisibilidad de los 8 escenarios ejecutables del catálogo real (`RF-010`). Los únicos archivos modificados fueron `tools/gemma/escenarios.py` y `specs/018-catalogo-escenarios/tasks.md`; no se modificaron las pruebas, `catalogo.json` ni artefacto de contrato alguno, y no se ejecutó `git add` ni `git commit`.
- [x] Completada.

### T-007

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-007`, `CB-001`, `CB-003`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-005`, `CA-007`, `CA-010`.
- **Archivos:** `tools/gemma/tests/test_precheck.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_precheck.TestPrecheckEscenarios` en rojo por ausencia de la función `verificar_recursos_escenario` en `tools/gemma/precheck.py`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-008

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-007`, `CB-001`, `CB-003`, `CB-007`, `CB-008`.
- **Criterio de aceptación:** `CA-005`, `CA-007`, `CA-010`.
- **Archivos:** `tools/gemma/precheck.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_precheck.TestPrecheckEscenarios` en verde con `OK`: aborto en precheck con código 3 para `ESC-M6-C131K` (`CB-007`), aborto si VRAM disponible < presupuesto (`RF-007`), aborto sin estimar si VRAM no es medible (`CB-001`), aborto si RAM libre de host < 8192 MiB en MoE CPU (`CB-008`), y aborto si contexto resuelto <= 4096 tokens (`CB-003`).
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-009

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-008`, `CB-002`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `tools/gemma/tests/test_registro.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_registro.TestRegistroEscenarios` en rojo por ausencia de campos de escenario y evaluación presupuestaria en `tools/gemma/registro.py`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-010

- **Dependencias:** `T-009`.
- **Requisitos cubiertos:** `RF-008`, `CB-002`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `tools/gemma/registro.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_registro.TestRegistroEscenarios` en verde con `OK`: verifica registro de `escenario_id`, `presupuesto_vram_declarado_mib`, VRAM asignada, libre, delta y conformidad (`consumo <= presupuesto`); si consumo > presupuesto, verifica registro del exceso y conservación íntegra de la medición con `conforme_presupuesto = false`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-011

- **Dependencias:** `T-010`.
- **Requisitos cubiertos:** `RF-003`, `RF-004`, `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-002`, `CA-003`, `CA-007`.
- **Archivos:** `tools/gemma/tests/test_lanzador.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_lanzador.TestLanzadorEscenarios` en rojo por falta de soporte de argumentos `--escenario` y `--listar-escenarios` en `tools/gemma/lanzador.py`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-012

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RF-003`, `RF-004`, `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-002`, `CA-003`, `CA-007`.
- **Archivos:** `tools/gemma/lanzador.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_lanzador.TestLanzadorEscenarios` en verde con `OK`: `--listar-escenarios` devuelve los 9 escenarios con código 0; ID inexistente aborta con código 2 listando los 9 IDs canónicos (`RF-004`); `--escenario` válido inyecta el ID en la ejecución y recalcula el contexto ajustado ante cambio de VRAM libre antes de arrancar (`CB-005`).
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-013

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-003`, `RF-005`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `tools/gemma/tests/test_lanzador.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_lanzador.TestMenuInteractivoEscenarios` en rojo por falta de integración del selector de escenarios en el flujo interactivo de `tools/gemma/lanzador.py`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-014

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-003`, `RF-005`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `tools/gemma/lanzador.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_lanzador.TestMenuInteractivoEscenarios` en verde con `OK`: simula selección interactiva con entrada por consola y verifica resolución e invocación con los parámetros del escenario elegido.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-015

- **Dependencias:** `T-014`.
- **Requisitos cubiertos:** `RF-003`, `RF-005`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `src/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat`, `tools/gemma/tests/test_lanzador.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_lanzador.TestLanzadorBatPropagacion` en verde con `OK`: verifica que el script `.bat` conserve la resolución de raíz mediante `%~dp0`, las 3 vías de resolución de Python y la propagación íntegra de `%*` hacia `lanzador.py`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-016

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-012`, `RNF-001`.
- **Criterio de aceptación:** `CA-004`, `CA-009`.
- **Archivos:** `tools/gemma/tests/test_escenarios.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestRendimientoResolucion` en verde con `OK`: comprueba que la resolución y validación de escenarios se completa en menos de 5 segundos (`RNF-001`) y verifica que los perfiles en `src/gemma/perfiles/` no se alteran ni interfieren con el catálogo (`RF-012`).
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.
