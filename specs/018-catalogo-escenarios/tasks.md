# Tareas — SPEC-018

*Plantilla de rango 5: norma de forma del artefacto `tasks.md`. Cada tarea declara los ocho campos en el orden indicado y se cierra solo con la evidencia transcrita.*

## Progreso

- Cerradas: 2 de 16 tareas.

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
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-005`, `RF-011`, `CB-004`, `CB-006`, `RNF-001`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-008`, `CA-009`.
- **Archivos:** `tools/gemma/escenarios.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestOrdenamientoEscenarios tools.gemma.tests.test_escenarios.TestAdmisibilidadEscenarios` en verde con `OK`: valida carga, orden jerárquico determinista (MoE CPU asc, contexto efectivo asc), detección y rechazo de duplicados (`CB-004`) y revocación de estado aprobado ante modificaciones (`CB-006`).
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-005

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-009`, `RF-010`, `RNF-005`, `CB-003`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/gemma/tests/test_escenarios.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` en rojo por ausencia de las funciones de derivación y validación de contexto ajustado en `tools/gemma/escenarios.py`.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

### T-006

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-009`, `RF-010`, `RNF-005`, `CB-003`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `tools/gemma/escenarios.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` en verde con `OK`: valida derivación en múltiplos de 1024 tokens con valores base (8192, 16 384, 65 536 tokens), detección de contexto resuelto <= 4096 tokens e inadmisibilidad de selección para escenarios ajustados sin valor numérico.
- **Evidencia:** Pendiente de ejecución de la tarea.
- [ ] Completada.

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
