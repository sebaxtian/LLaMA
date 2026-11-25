# Plan técnico — SPEC-018

*Plantilla de rango 5: norma de forma del artefacto `plan.md`. Cada decisión declara su alternativa descartada y cada fila de la matriz su verificación asociada.*

## Referencias

- `spec.md`: `SPEC-018`, versión 0.7.0, estado `planned`, con 13 requisitos funcionales (`RF-001` a `RF-013`), 5 requisitos no funcionales (`RNF-001` a `RNF-005`), 8 casos borde (`CB-001` a `CB-008`) y 10 criterios de aceptación (`CA-001` a `CA-010`); G1 del contrato reformulado aprobada por el propietario `Agent Sebaxtian` en el commit firmado `d574f58` (2026-11-25), con cuerpo `Spec: SPEC-018` y firma ED25519 verificada por `git verify-commit`.
- `clarify.md`: `SPEC-018`, cerrado sin casillas pendientes con `AMB-001` a `AMB-013` resueltos —`AMB-013` fija lo que conserva el registro de aprobación y la tarea `T-017` que implementa la revocación—, incorporación del caso borde `CB-008`, parches aplicados a requisitos y 3 decisiones de negocio formalizadas.
- `docs/constitution.md`: norma suprema de rango 1; §3 guardrails de carpetas protegidas (`llama.cpp/`, `bin/`, `models/`, `.env`); §5 principio de validación-first y prueba real; §9 prohibición de optimización declarada sin medición empírica.
- `AGENTS.md`: norma operativa de rango 2 para agentes; roles y permisos; guardrails de hardware y de ejecución (.bat con `%~dp0`); mandatos de trazabilidad y validación.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma de rango 3; §5 ciclo de vida y transición T2; §8.3 especificación del artefacto `plan.md`; §9 reglas de versionado; §14 contrato del validador determinista.
- `docs/sdd/plantillas/plan.md`: norma de forma de rango 5 para el diseño técnico.
- `specs/017-configuracion-gemma-4-26b-a4b/plan.md`: diseño previo del orquestador `tools/gemma/lanzador.py`, precheck `tools/gemma/precheck.py`, medición de memoria `tools/gemma/medir.py` y registro de ejecuciones en `tools/gemma/registro.py`.
- `src/gemma/perfiles/`: manifiestos vigentes de los tres perfiles de producción (`rendimiento.json`, `resiliencia.json`, `sin_especulativa.json`) y parámetros iniciales (`parametros_iniciales.json`).
- `docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md`: línea base documental de la arquitectura del modelo Gemma-4-26B-A4B en el hardware objetivo (GEEKOM Mini IT13, RTX 5060 Ti 16 GB VRAM).

## Naturaleza del entregable

La spec produce una combinación declarada de seis componentes de software y configuración:

1. **Datos declarativos del catálogo:** Archivo canónico `src/gemma/escenarios/catalogo.json` que formaliza los 9 escenarios de ejecución del modelo `Gemma-4-26B-A4B-it-qat-GGUF`, cubriendo las 3 × 3 combinaciones (0, 6 y 9 capas MoE en CPU × 4096 tokens, 131 072 tokens y contexto ajustado), con sus 9 identificadores canónicos, presupuestos de VRAM desglosados en 4 componentes, campo informativo de RAM de host y los 7 parámetros de ejecución obligatorios.
2. **Módulo de lógica y dominio de escenarios:** Módulo Python `tools/gemma/escenarios.py` en biblioteca estándar, responsable de cargar el catálogo, validar su integridad, ordenar deterministamente la lista de escenarios, resolver el contexto dinámico ajustado bajo la regla determinista y evaluar la admisibilidad de selección según el ciclo de vida de cuatro estados.
3. **Extensión de comprobaciones previas (Precheck):** Integración en `tools/gemma/precheck.py` de verificaciones específicas para escenarios: detección bloqueante de escenarios `no_ejecutable` (`CB-007`), suficiencia de VRAM disponible frente al presupuesto (`RF-007`, `CB-001`), suficiencia de RAM libre del host (mínimo 8192 MiB libres si MoE CPU > 0 capas; `RF-007`, `CB-008`) y verificación de contexto ajustado resuelto superior a 4096 tokens (`CB-003`).
4. **Integración en orquestador y lanzadores:** Extensión de `tools/gemma/lanzador.py` para admitir `--escenario <id>`, `--listar-escenarios` y menú de selección interactiva; trazabilidad del identificador de escenario en la ejecución y registro; recálculo previo al arranque para contexto ajustado (`CB-005`); evaluación de conformidad `consumo <= presupuesto` (`RF-008`, `CB-002`); y propagación de argumentos CLI desde `src/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat`.
5. **Suite de pruebas de escenarios:** Pruebas unitarias y de integración en `tools/gemma/tests/test_escenarios.py` y extensiones de `test_precheck.py` y `test_lanzador.py`, ejecutables con `python -m unittest` sin dependencia de GPU física ni alteración de binarios ni modelos.
6. **Suite de registro de ejecución:** Pruebas unitarias en `tools/gemma/tests/test_registro.py` que sostienen `RF-008` y `CB-002`: acreditan que el registro declara `escenario_id`, presupuesto declarado, VRAM asignada, VRAM libre, delta y dictamen de conformidad, y que la medición se conserva íntegra cuando el consumo excede el presupuesto declarado.

No produce: binarios en `bin/`, modelos en `models/`, modificaciones en `llama.cpp/`, credenciales en `.env`, ni alteraciones a los 3 manifiestos vigentes en `src/gemma/perfiles/`. Tampoco aprueba compuertas ni declara escenarios en estado `aprobado` sin medición empírica y firma del propietario.

## Arquitectura

### Componentes, responsabilidad y límites

| Componente | Artefacto | Responsabilidad | Límite | Rol que escribe |
|---|---|---|---|---|
| Manifiesto del catálogo | `src/gemma/escenarios/catalogo.json` | Declarar formalmente los 9 escenarios (3×3), sus identificadores canónicos, sus estados iniciales, presupuestos desglosados de VRAM en 4 componentes, campo informativo de RAM requerida de sistema, valores base de contexto ajustado y los 7 parámetros de ejecución. | No sustituye ni altera los archivos de perfil en `src/gemma/perfiles/`; no contiene rutas absolutas de host; no declara ningún escenario como `aprobado` sin confirmación expresa. | `coder` |
| Dominio del catálogo | `tools/gemma/escenarios.py` | Cargar y validar el esquema del catálogo, aplicar orden determinista jerárquico de enumeración, derivar contexto ajustado en múltiplos de 1024 tokens con suelo > 4096, evaluar admisibilidad de selección y asegurar inmutabilidad de identificadores. | Funciones puras basadas en biblioteca estándar; no realiza llamadas al sistema operativo para invocar procesos ni lee hardware directamente salvo delegación explícita. | `coder` |
| Comprobaciones previas | `tools/gemma/precheck.py` | Validar precondiciones de recursos antes de iniciar el servidor: bloqueo en precheck de `no_ejecutable`, contraste VRAM disponible vs presupuesto, contraste RAM libre host >= 8192 MiB si MoE CPU > 0, y contraste de contexto ajustado resuelto. | No inicia el proceso del servidor; no altera el estado de los escenarios en el catálogo; no inventa ni estima métricas no disponibles. | `coder` |
| Orquestador y CLI | `tools/gemma/lanzador.py` | Gestionar argumentos CLI (`--escenario`, `--listar-escenarios`), activar selector interactivo ante ausencia de parámetros, orquestar recálculo de contexto previo a lanzamiento, inyectar `escenario_id` en logs/registros y calcular conformidad presupuestaria. | No edita `specs/`, `docs/`, `bin/`, `models/` ni `.env`; delega la medición de hardware en `medir.py` y el precheck en `precheck.py`. | `coder` |
| Lanzador por lotes | `src/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat` | Resolver la raíz mediante `%~dp0`, resolver el intérprete de Python mediante las 3 vías conocidas sin depender del `PATH` y propagar argumentos (`%*`) hacia `lanzador.py`. | No contiene lógica de negocio de escenarios ni validación de recursos; no resuelve rutas relativas al directorio actual de ejecución. | `coder` |
| Registro de ejecución | `tools/gemma/registro.py` | Extender el esquema de registro para incluir el identificador del escenario seleccionado, presupuesto declarado, consumo medido y dictamen de conformidad (`consumo <= presupuesto`). | No sobrescribe registros históricos; no altera el estado de aprobación sin mediación del propietario. | `coder` |
| Suite de registro | `tools/gemma/tests/test_registro.py` | Verificar el bloque de conformidad presupuestaria del registro: `escenario_id`, presupuesto declarado, VRAM asignada, VRAM libre, delta y dictamen (`RF-008`), y la conservación íntegra de la medición con exceso declarado (`CB-002`). | Pruebas herméticas sobre directorios temporales; no invocan GPU, no consultan hardware ni alteran registros históricos. | `coder` |
| Suite de pruebas | `tools/gemma/tests/test_escenarios.py` | Verificar la estructura del catálogo (9 combinaciones únicas, 0 ausentes, 0 duplicadas), algoritmos de ordenación, derivación de contexto ajustado, precheck de RAM/VRAM y rechazo de IDs inválidos. | Pruebas herméticas e independientes de hardware; sustituyen puntos de inyección para simular VRAM y RAM sin consultar el sistema host real. | `coder` |

### Flujo de interacción y ciclo de vida de ejecución

```
Operador / CLI
    │
    ▼
[unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat]
    │  (Resuelve raíz %~dp0 e intérprete de Python)
    ▼
[tools/gemma/lanzador.py]
    │
    ├── ¿Solicita listar (--listar-escenarios)?
    │       └── [escenarios.listar_escenarios()] ──> Imprime 9 escenarios en orden jerárquico ──> Exit 0
    │
    ├── ¿Modo interactivo sin argumentos?
    │       └── Menú interactivo jerárquico ──> Operador selecciona ID
    │
    ├── ¿Selecciona escenario (--escenario <ID>)?
    │       │
    │       ├── 1. Validar existencia del ID en catalogo.json
    │       │       └── SI no existe ──> Enumera 9 IDs disponibles y aborta con código 2 (RF-004)
    │       │
    │       ├── 2. Precheck de estado (precheck.verificar_escenario)
    │       │       └── SI estado == 'no_ejecutable' (ESC-M6-C131K) ──> Diagnóstico y aborta con código 3 (CB-007)
    │       │
    │       ├── 3. Resolución de contexto ajustado (si aplica: ESC-*-CADJ)
    │       │       └── Derivar tokens en múltiplos de 1024 a partir de VRAM libre real (RF-009)
    │       │       └── SI tokens <= 4096 ──> Aborta con código 3 sin iniciar (CB-003)
    │       │
    │       ├── 4. Precheck de recursos de hardware
    │       │       ├── Consultar VRAM disponible
    │       │       │    └── SI no medible ──> Aborta con código 3 sin estimar (CB-001)
    │       │       │    └── SI VRAM disponible < presupuesto ──> Aborta con código 3 (RF-007)
    │       │       └── SI capas MoE en CPU > 0 (6 o 9 capas):
    │       │            └── Consultar RAM libre del host
    │       │            └── SI RAM libre < 8192 MiB ──> Aborta con código 3 (CB-008, RF-007)
    │       │
    │       ├── 5. Recálculo dinámico previo al arranque (CB-005)
    │       │       └── Si VRAM libre cambió tras selección, recalcular tokens efectivos de CADJ
    │       │
    │       ├── 6. Lanzamiento del servidor llama.cpp con parámetros del escenario (RF-003, RF-013)
    │       │       └── Registro de ID de escenario en consola y logs
    │       │
    │       ├── 7. Medición y evaluación de conformidad (RF-008, CB-002)
    │       │       ├── Muestreo de VRAM asignada y libre
    │       │       ├── delta = consumo_medido - presupuesto_declarado
    │       │       ├── conforme = (consumo_medido <= presupuesto_declarado)
    │       │       └── Registro en results/gemma/ conservando la medición
    │       │
    │       └── Fin de ejecución ──> Exit 0
```

## Contratos

### C-1: Estructura del archivo canónico `src/gemma/escenarios/catalogo.json`

El archivo declara una estructura JSON estricta con exactamente 9 entradas bajo la clave raíz `escenarios`:

```json
{
  "version": "1.0.0",
  "modelo": "Gemma-4-26B-A4B-it-qat-GGUF",
  "descripcion": "Catálogo canónico de 9 escenarios de ejecución del modelo Gemma-4-26B-A4B",
  "escenarios": {
    "ESC-M0-C4K": {
      "id": "ESC-M0-C4K",
      "estado": "declarado",
      "capas_cpu_moe": 0,
      "contexto": {
        "tipo": "fijo",
        "declarado_tokens": 4096,
        "efectivo_tokens": 4096,
        "regla_derivacion": null
      },
      "presupuesto_vram": {
        "total_mib": 14200,
        "desglose": {
          "pesos_mib": 11800,
          "cache_kv_mib": 600,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 0,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M0-CADJ": {
      "id": "ESC-M0-CADJ",
      "estado": "declarado",
      "capas_cpu_moe": 0,
      "contexto": {
        "tipo": "ajustado",
        "declarado_tokens": 8192,
        "efectivo_tokens": 8192,
        "regla_derivacion": "multiplos_1024_suelo_4096"
      },
      "presupuesto_vram": {
        "total_mib": 14800,
        "desglose": {
          "pesos_mib": 11800,
          "cache_kv_mib": 1200,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 0,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M0-C131K": {
      "id": "ESC-M0-C131K",
      "estado": "declarado",
      "capas_cpu_moe": 0,
      "contexto": {
        "tipo": "fijo",
        "declarado_tokens": 131072,
        "efectivo_tokens": 131072,
        "regla_derivacion": null
      },
      "presupuesto_vram": {
        "total_mib": 15600,
        "desglose": {
          "pesos_mib": 11800,
          "cache_kv_mib": 2000,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 0,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M6-C4K": {
      "id": "ESC-M6-C4K",
      "estado": "declarado",
      "capas_cpu_moe": 6,
      "contexto": {
        "tipo": "fijo",
        "declarado_tokens": 4096,
        "efectivo_tokens": 4096,
        "regla_derivacion": null
      },
      "presupuesto_vram": {
        "total_mib": 11200,
        "desglose": {
          "pesos_mib": 8800,
          "cache_kv_mib": 600,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 3500,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M6-CADJ": {
      "id": "ESC-M6-CADJ",
      "estado": "declarado",
      "capas_cpu_moe": 6,
      "contexto": {
        "tipo": "ajustado",
        "declarado_tokens": 16384,
        "efectivo_tokens": 16384,
        "regla_derivacion": "multiplos_1024_suelo_4096"
      },
      "presupuesto_vram": {
        "total_mib": 12800,
        "desglose": {
          "pesos_mib": 8800,
          "cache_kv_mib": 2200,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 3500,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M6-C131K": {
      "id": "ESC-M6-C131K",
      "estado": "no_ejecutable",
      "capas_cpu_moe": 6,
      "contexto": {
        "tipo": "fijo",
        "declarado_tokens": 131072,
        "efectivo_tokens": 131072,
        "regla_derivacion": null
      },
      "presupuesto_vram": {
        "total_mib": 15800,
        "desglose": {
          "pesos_mib": 8800,
          "cache_kv_mib": 5200,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 3500,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M9-C4K": {
      "id": "ESC-M9-C4K",
      "estado": "declarado",
      "capas_cpu_moe": 9,
      "contexto": {
        "tipo": "fijo",
        "declarado_tokens": 4096,
        "efectivo_tokens": 4096,
        "regla_derivacion": null
      },
      "presupuesto_vram": {
        "total_mib": 9600,
        "desglose": {
          "pesos_mib": 7200,
          "cache_kv_mib": 600,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 5200,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M9-CADJ": {
      "id": "ESC-M9-CADJ",
      "estado": "declarado",
      "capas_cpu_moe": 9,
      "contexto": {
        "tipo": "ajustado",
        "declarado_tokens": 65536,
        "efectivo_tokens": 65536,
        "regla_derivacion": "multiplos_1024_suelo_4096"
      },
      "presupuesto_vram": {
        "total_mib": 14500,
        "desglose": {
          "pesos_mib": 7200,
          "cache_kv_mib": 5500,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 5200,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    },
    "ESC-M9-C131K": {
      "id": "ESC-M9-C131K",
      "estado": "declarado",
      "capas_cpu_moe": 9,
      "contexto": {
        "tipo": "fijo",
        "declarado_tokens": 131072,
        "efectivo_tokens": 131072,
        "regla_derivacion": null
      },
      "presupuesto_vram": {
        "total_mib": 15500,
        "desglose": {
          "pesos_mib": 7200,
          "cache_kv_mib": 6500,
          "computo_mib": 1000,
          "reserva_mib": 800
        }
      },
      "ram_sistema_requerida_mib": 5200,
      "parametros_ejecucion": {
        "gpu_layers": 99,
        "flash_attn": "on",
        "ubatch": 1120,
        "load_mode": "none",
        "parallel": 1,
        "cache_type_k": "q8_0",
        "cache_type_v": "q8_0",
        "spec_draft_n_max": 3
      },
      "aprobacion": null
    }
  }
}
```

**Bloque `aprobacion`.** Cada escenario declara `null` mientras no conste aprobación. 1 escenario en estado `aprobado` declara 1 objeto con las claves siguientes, y `cargar_catalogo` rechaza el manifiesto con `ValueError` cuando falta alguna de las 4 claves de valores o la referencia de la medición:

```json
"aprobacion": {
  "capas_cpu_moe": 6,
  "contexto_efectivo_tokens": 8192,
  "parametros_ejecucion": {
    "gpu_layers": 99,
    "flash_attn": "on",
    "ubatch": 1120,
    "load_mode": "none",
    "parallel": 1,
    "cache_type_k": "q8_0",
    "cache_type_v": "q8_0",
    "spec_draft_n_max": 3
  },
  "presupuesto_vram_total_mib": 12800,
  "medicion": "results/gemma/<archivo-de-medicion>.md",
  "confirmacion_propietario": "<texto de la confirmación escrita del propietario>"
}
```

- `capas_cpu_moe`: entero no negativo; conserva las capas de expertos en CPU que sostuvieron la aprobación.
- `contexto_efectivo_tokens`: entero positivo; conserva el contexto efectivo en tokens que sostuvo la aprobación.
- `parametros_ejecucion`: objeto que conserva los 7 parámetros de ejecución obligatorios y el techo de draft, con las mismas claves y los mismos tipos que el bloque `parametros_ejecucion` del escenario.
- `presupuesto_vram_total_mib`: entero positivo; conserva el presupuesto de VRAM en MiB que sostuvo la aprobación.
- `medicion`: texto no vacío que referencia la medición registrada que sostuvo la aprobación.
- `confirmacion_propietario`: texto no vacío de la confirmación escrita del propietario.

El bloque es la referencia de la comparación de `C-3`: `validar_admisibilidad_escenario` contrasta los 4 valores conservados con los declarados por el escenario y 1 diferencia en cualquiera de ellos revoca la condición de aprobado, conforme a `DEC-012`.

### C-2: Interfaz de línea de comandos (CLI) y códigos de salida

La interfaz de comandos de `tools/gemma/lanzador.py` se extiende de forma compatible con la existente:

- `--escenario <ID>`: Selecciona un escenario del catálogo por su identificador exacto.
- `--listar-escenarios`: Muestra por consola la lista de los 9 escenarios formateada en orden determinista jerárquico.
- `--modo <comprobar|servir|medir>`: Aplica el modo de ejecución seleccionado para el escenario especificado.
- Selección interactiva: Si no se provee `--perfil` ni `--escenario`, el sistema presenta el menú interactivo para escoger perfil o escenario del catálogo.

**Códigos de salida:**

| Código | Significado | Causa |
|---|---|---|
| `0` | Éxito | Ejecución completada, precheck superado, o listado de escenarios exitoso. |
| `2` | Error de sintaxis o invocación | Escenario no encontrado en el catálogo (`RF-004`), modo no admitido o argumentos incompatibles. |
| `3` | Fallo de precheck de recursos o inviabilidad | Escenario `no_ejecutable` (`CB-007`), VRAM no medible (`CB-001`), VRAM disponible < presupuesto (`RF-007`), RAM host < 8192 MiB (`CB-008`), contexto resuelto <= 4096 tokens (`CB-003`). |
| `8` | Error de entorno de ejecución | Intérprete Python no disponible o ruta no encontrada (proveniente del `.bat`). |

### C-3: Firmas de interfaz en `tools/gemma/escenarios.py`

```python
def cargar_catalogo(ruta_catalogo: Path | None = None) -> dict[str, Any]:
    """Carga y valida la integridad del catálogo de escenarios.
    Lanza ValueError si faltan claves obligatorias, IDs duplicados o estructura corrupta."""

def listar_escenarios(catalogo: dict[str, Any]) -> list[dict[str, Any]]:
    """Devuelve los 9 escenarios ordenados deterministamente:
    1. capas_cpu_moe ascendente (0, 6, 9)
    2. contexto_efectivo ascendente (4096, ajustado, 131072)"""

def resolver_contexto_ajustado(
    escenario: dict[str, Any],
    vram_libre_mib: int,
    consumo_kv_por_1024_mib: float = 85.0
) -> int:
    """Calcula el contexto efectivo en múltiplos de 1024 tokens.
    Garantiza suelo mínimo de 4096 tokens. Si el cálculo es <= 4096,
    devuelve el valor calculado para que precheck aborte."""

def validar_admisibilidad_escenario(escenario: dict[str, Any]) -> tuple[bool, str]:
    """Verifica si el escenario puede ser lanzado.
    Devuelve (False, motivo) si estado == 'no_ejecutable' o si contexto ajustado no declara valor.
    Si estado == 'aprobado', compara el bloque `aprobacion` con los valores declarados:
    capas_cpu_moe, contexto_efectivo_tokens, parametros_ejecucion y presupuesto_vram_total_mib.
    Devuelve (False, motivo) nombrando el valor que difiere y exigiendo 1 medición nueva
    cuando falta el bloque o cuando 1 de los 4 valores conservados difiere del declarado.
    Devuelve (True, "") en el resto de los casos admitidos."""
```

### C-4: Contrato de comprobaciones previas (Precheck)

`tools/gemma/precheck.py:verificar_recursos_escenario(...)` evalúa secuencialmente las condiciones:

1. **Estado ejecutable:** `estado != 'no_ejecutable'`. Si falla, emite `[FALLO] Escenario no ejecutable: <motivo>` y aborta con código 3 (`CB-007`).
2. **Contexto ajustado numérico:** Si `contexto.tipo == 'ajustado'`, se verifica que `declarado_tokens` y `efectivo_tokens` sean numéricos (`RF-010`). Si resuelto <= 4096 tokens, emite `[FALLO] Contexto ajustado resuelto insuficiente: <tokens> <= 4096` y aborta con código 3 (`CB-003`).
3. **Disponibilidad de VRAM:** Consulta de VRAM libre vía `medir.vram_libre_mib()`. Si es `None`, emite `[FALLO] VRAM disponible no medible` sin estimar y aborta con código 3 (`CB-001`).
4. **Presupuesto de VRAM:** Comparación `vram_libre_mib >= presupuesto.total_mib`. Si es menor, emite `[FALLO] Presupuesto excede VRAM disponible: requerido <req> MiB, disponible <disp> MiB` y aborta con código 3 (`RF-007`).
5. **Memoria RAM de host:** Si `capas_cpu_moe > 0`, consulta memoria RAM libre de host. Si `ram_libre_host_mib < 8192`, emite `[FALLO] RAM libre de host insuficiente: disponible <disp> MiB, requerida 8192 MiB` y aborta con código 3 (`CB-008`, `RF-007`).

### C-5: Registro de ejecución y dictamen de conformidad presupuestaria

Al completarse una ejecución con `--escenario`, `tools/gemma/registro.py` registra los campos:

- `escenario_id`: Identificador canónico del escenario (`ESC-M*-C*`).
- `presupuesto_vram_declarado_mib`: Presupuesto total declarado en catálogo.
- `vram_asignada_medida_mib`: Consumo real medido de la GPU.
- `vram_libre_medida_mib`: VRAM libre restante tras la carga.
- `delta_presupuesto_mib`: `vram_asignada_medida_mib - presupuesto_vram_declarado_mib`.
- `conforme_presupuesto`: Booleano determinista (`delta_presupuesto_mib <= 0`).
- Si `delta_presupuesto_mib > 0`: Registra advertencia de exceso presupuestario en MiB, conserva el archivo de medición y fija `conforme_presupuesto = false` (`RF-008`, `CB-002`).

## Decisiones técnicas

### DEC-001: Ubicación, formato y esquema canónico del catálogo

- **Decisión:** Publicar el catálogo en un archivo JSON único versionado en `src/gemma/escenarios/catalogo.json`, estructurado como un diccionario cuyas claves maestras son exactamente los 9 identificadores canónicos invariables.
- **Justificación:** Centraliza la verdad de los 9 escenarios en un único artefacto declarativo y versionable, desacoplado de los perfiles existentes (`src/gemma/perfiles/`). Permite validación estricta de esquema y comprobación determinista de ausencia de duplicados (`CB-004`) o campos vacíos (`RNF-002`).
- **Alternativas descartadas:**
  - *Fragmentar en 9 archivos JSON independientes:* Generaría dispersión de archivos y complicaría la validación de unicidad de la matriz 3×3.
  - *Incrustar los escenarios en los perfiles vigentes (`rendimiento.json`, `resiliencia.json`, `sin_especulativa.json`):* Violación flagrante de la autonomía declarada en `RF-012` y `CA-004`.

### DEC-002: Identificadores canónicos e invariabilidad ante contexto dinámico

- **Decisión:** Adoptar los 9 identificadores canónicos fijos prefijados con `ESC-` (`ESC-M0-C4K`, `ESC-M0-C131K`, `ESC-M0-CADJ`, `ESC-M6-C4K`, `ESC-M6-C131K`, `ESC-M6-CADJ`, `ESC-M9-C4K`, `ESC-M9-C131K`, `ESC-M9-CADJ`). El identificador `ESC-*-CADJ` permanece constante e invariable en CLI, catálogo y registros, independientemente del número exacto de tokens resueltos en ejecución.
- **Justificación:** Resuelve `AMB-006` y `RF-002`. Un identificador mutable provocaría fallos de trazabilidad, rompería referencias en scripts automáticos y complicaría la búsqueda histórica de pruebas.
- **Alternativas descartadas:**
  - *Modificar el ID dinámicamente según el contexto calculado (ej. `ESC-M0-C8K`):* Produce identificadores volátiles y no deterministas que impiden la selección consistente por CLI.

### DEC-003: Inclusión explícita de `ESC-M6-C131K` como `no_ejecutable`

- **Decisión:** Declarar formalmente el escenario `ESC-M6-C131K` en el catálogo con estado `no_ejecutable` y configurar el precheck para abortar de inmediato con código 3 y diagnóstico informativo ante cualquier intento de lanzamiento.
- **Justificación:** Resuelve `AMB-009`, `RF-001`, `CB-007` y `CA-010`. La evidencia empírica previa demuestra que esta combinación colapsa en la máquina objetivo con 16 GB de VRAM. Incluirlo preserva la completitud matemática de la matriz 3×3 y advertir operativamente previene bloqueos del sistema o falsos diagnósticos.
- **Alternativas descartadas:**
  - *Omitir la combinación del catálogo:* Viola el requisito de 9 escenarios 3×3 de `RF-001`.
  - *Permitir el intento de arranque hasta que falle el binario:* Provoca esperas innecesarias y degrada la experiencia operativa, violando `CB-007`.

### DEC-004: Orden determinista jerárquico de enumeración

- **Decisión:** Implementar la ordenación de los escenarios en CLI y menús bajo la regla jerárquica estricta: primer criterio por `capas_cpu_moe` ascendente (0, 6, 9); segundo criterio por `contexto_efectivo` en tokens ascendente (4096, nominal/ajustado, 131 072).
- **Justificación:** Resuelve `AMB-007`, `RF-005` y `CA-002`. Ofrece una salida predecible y lógica para el operador técnico al comparar configuraciones.
- **Alternativas descartadas:**
  - *Orden alfabético por ID:* Situaría `C131K` antes de `C4K`, resultando antinatural desde la perspectiva de recursos.
  - *Orden de inserción en el archivo JSON:* Frágil ante modificaciones accidentales de edición.

### DEC-005: Presupuesto desglosado en 4 componentes y margen libre de 512 MiB

- **Decisión:** Cada escenario declara su presupuesto de VRAM en MiB con desglose explícito en 4 claves: `pesos_mib`, `cache_kv_mib`, `computo_mib` y `reserva_mib`. La suma de los componentes debe asegurar un margen libre residual de al menos 512 MiB respecto a la capacidad de la GPU (16 384 MiB), además de incluir el campo informativo `ram_sistema_requerida_mib`.
- **Justificación:** Resuelve `AMB-002`, `AMB-011`, `RF-006` y `CA-004`. La interfaz USB4 de la eGPU penaliza severamente el desbordamiento hacia memoria compartida; declarar el desglose permite auditar qué componente causa la saturación.
- **Alternativas descartadas:**
  - *Presupuesto como un único escalar total:* Impide conocer el origen del consumo y reproduce el defecto histórico 2 de la configuración previa.

### DEC-006: Precheck de memoria RAM del host para derivación a CPU

- **Decisión:** Extender `precheck.py` para que, cuando el escenario seleccionado declare `capas_cpu_moe > 0` (6 o 9 capas), consulte la memoria RAM física libre del sistema operativo Windows y aborte con código 3 si es inferior a 8192 MiB.
- **Justificación:** Resuelve `AMB-011`, `RF-007`, `CB-008` y `CA-005`. Al desviar capas de expertos a CPU, el host aloja tensores pesados (~3500 MiB para 6 capas, ~5200 MiB para 9 capas); la ausencia de RAM libre provoca paginación a disco y colapso de rendimiento.
- **Alternativas descartadas:**
  - *Comprobar únicamente la VRAM de la GPU:* Ignora la carga impuesta al sistema host en arquitecturas híbridas CPU/GPU.

### DEC-007: Regla estricta de conformidad presupuestaria y conservación de evidencia

- **Decisión:** La conformidad se evalúa deterministamente como `consumo_medido_mib <= presupuesto_declarado_mib`. Si el consumo excede el presupuesto, se emite advertencia con la diferencia exacta en MiB, se asigna `conforme_presupuesto = false`, pero el registro de ejecución se conserva íntegramente sin invalidar la prueba.
- **Justificación:** Resuelve `AMB-010`, `RF-008`, `CB-002` y `CA-006`. Preserva la trazabilidad forense para que el equipo de arquitectura pueda ajustar el presupuesto o corregir parámetros en iteraciones posteriores.
- **Alternativas descartadas:**
  - *Descartar o eliminar la medición si no es conforme:* Destruiría la evidencia empírica necesaria para el análisis técnico.

### DEC-008: Regla determinista de derivación y recálculo en tiempo de lanzamiento para contexto ajustado

- **Decisión:** Los escenarios ajustados declaran un valor nominal base en tokens (8192 para 0 capas, 16 384 para 6 capas y 65 536 para 9 capas). En tiempo de ejecución previo al lanzamiento, el sistema calcula el contexto efectivo dividiendo la VRAM disponible para KV entre el consumo por bloque de 1024 tokens, redondeando hacia abajo a múltiplos de 1024 tokens. Si la VRAM libre cambia entre la selección y el lanzamiento, se recalcula inmediatamente. Si el valor final resuelto es menor o igual a 4096 tokens, se cancela el lanzamiento con código 3.
- **Justificación:** Resuelve `AMB-001`, `RF-009`, `RF-010`, `CB-003`, `CB-005` y `CA-007`. Garantiza máxima utilización de VRAM sin riesgo de rebasamiento y protege el sistema ante condiciones de carrera en el uso de memoria.
- **Alternativas descartadas:**
  - *Permitir contextos menores a 4096 tokens:* Produciría una degradación extrema de la utilidad analítica del modelo y violaría `CB-003`.

### DEC-009: Autonomía operativa del catálogo y desacoplamiento de perfiles

- **Decisión:** El catálogo de escenarios se almacena en `src/gemma/escenarios/` y opera con independencia total de los archivos en `src/gemma/perfiles/`. Cualquier escenario en estado `declarado` o `medido` puede ser seleccionado y ejecutado sin requerir que un perfil de producción esté en estado `aprobado`. La promoción de un escenario a `aprobado` exige medición registrada y confirmación expresa del propietario.
- **Justificación:** Resuelve `AMB-003`, `AMB-005`, `AMB-012`, `RF-011`, `RF-012` y `CA-008`. Permite usar el catálogo como banco de experimentación y evaluación comparativa sin alterar los perfiles congelados de producción.
- **Alternativas descartadas:**
  - *Exigir que el perfil base esté aprobado para poder correr un escenario:* Paralizaría la experimentación comparativa de nuevas configuraciones.

### DEC-010: Doble vía de selección (CLI e Interactiva) con delegación transparente desde `.bat`

- **Decisión:** Extender `tools/gemma/lanzador.py` para procesar `--escenario <id>` y `--listar-escenarios`, integrando un menú interactivo jerárquico cuando no se especifiquen parámetros. El script `src/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat` propaga íntegramente sus argumentos (`%*`) hacia `lanzador.py`.
- **Justificación:** Resuelve `AMB-004`, `RF-003`, `RF-005` y `CA-002`. Satisface tanto la automatización por scripts como la usabilidad directa del operador local.
- **Alternativas descartadas:**
  - *Crear un script `.bat` separado para escenarios:* Generaría duplicación innecesaria de la lógica de resolución de entorno e intérprete Python.

### DEC-011: Declaración explícita de los 7 parámetros de ejecución restantes

- **Decisión:** Cada uno de los 9 escenarios declara de forma obligatoria y explícita sus 7 parámetros de ejecución restantes: descarga de capas a GPU (`-ngl 99`), atención rápida (`flash_attn on`), micro-lote (`ubatch 1120`), carga de pesos (`load_mode none`), ranuras de servidor (`parallel 1`), tipo de caché clave (`cache_type_k q8_0`) y tipo de caché valor (`cache_type_v q8_0`), además de `spec_draft_n_max 3`.
- **Justificación:** Resuelve `AMB-008`, `RF-013` y `CA-009`. Elimina comportamientos indeterminados o dependientes de valores por defecto implícitos en el binario de llama.cpp.
- **Alternativas descartadas:**
  - *Omitir parámetros y confiar en defaults de llama.cpp:* Viola la reproducibilidad estricta exigida en `constitution.md`.

### DEC-012: Bloque de aprobación con los 4 valores conservados y su comparación en la admisibilidad

- **Decisión:** El bloque `aprobacion` de cada escenario pasa de `null` a 1 objeto que conserva los 4 valores aprobados —`capas_cpu_moe`, `contexto_efectivo_tokens`, `parametros_ejecucion` y `presupuesto_vram_total_mib`—, más la referencia de la medición que sostuvo la aprobación y la confirmación escrita del propietario. `validar_admisibilidad_escenario` compara ese objeto con los valores declarados por el escenario y devuelve `(False, motivo)` nombrando el valor que difiere cuando alguno cambia, de modo que 1 diferencia exige 1 medición nueva y revoca la condición de aprobado.
- **Justificación:** Resuelve `AMB-013`, `RF-011`, `CA-008` y `CB-006`. Sin los valores conservados, la admisibilidad se resolvía por la veracidad del campo `aprobacion` y 1 escenario aprobado que recibía 1 modificación en capas de expertos en CPU, contexto efectivo, parámetros de ejecución o presupuesto conservaba la condición de aprobado; conservar y comparar los 4 valores convierte `CB-006` en 1 comprobación determinista, reproducible y auditable, y nombra el valor que difiere para que el operador sepa qué medición debe repetir.
- **Alternativas descartadas:**
  - *Confiar en la veracidad de `aprobacion`:* es la brecha que motiva `DEC-012`, porque 1 bloque presente sin valores conservados no distingue 1 escenario aprobado de 1 escenario modificado.
  - *Recalcular la aprobación por fecha de modificación del archivo:* no distingue qué valor cambió ni es reproducible, porque la fecha del manifiesto depende de la copia, del sistema de archivos y del empaquetado.
  - *Duplicar los valores aprobados en otro archivo:* rompe la unicidad del catálogo y crea 2 fuentes de verdad que pueden divergir sin que la admisibilidad lo detecte.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| **Estructura y Catálogo** (Unitario) | `python -m unittest tools.gemma.tests.test_escenarios.TestCatalogoEstructura` | Carga de `catalogo.json` sin errores; validación de exactamente 9 escenarios únicos (3×3); verificación de los 9 IDs canónicos invariables; verificación de los 4 estados admitidos; verificación de que ningún campo obligatorio está vacío (`RNF-002`, `RNF-003`, `CA-001`). |
| **Orden determinista** (Unitario) | `python -m unittest tools.gemma.tests.test_escenarios.TestOrdenamientoEscenarios` | `listar_escenarios()` devuelve la secuencia exacta ordenada primero por capas MoE en CPU ascendente (0, 6, 9) y luego por contexto efectivo ascendente (4096, nominal/ajustado, 131 072) (`RF-005`, `CA-002`); `test_declaracion_duplicada_del_par_se_rechaza` verifica que la declaración repetida del par de capas y contexto se rechaza nombrando el identificador duplicado (`CB-004`). |
| **Admisibilidad y aprobación** (Unitario) | `python -m unittest tools.gemma.tests.test_escenarios.TestAdmisibilidadEscenarios` | `test_catalogo_real_declara_la_admisibilidad_por_estado` acredita que ningún escenario figura como aprobado sin medición y confirmación escrita, y que `declarado` y `medido` son seleccionables con independencia de los perfiles (`RF-011`, `CA-008`); `test_modificacion_de_escenario_aprobado_revoca_la_aprobacion`, que implementa `T-017`, verifica que 1 diferencia en capas de expertos en CPU, contexto efectivo, parámetros de ejecución o presupuesto revoca la condición de aprobado, nombra el valor que difiere y exige 1 medición nueva (`CB-006`, `CA-008`). |
| **Contexto ajustado** (Unitario) | `python -m unittest tools.gemma.tests.test_escenarios.TestContextoAjustado` | Derivación matemática exacta en múltiplos de 1024 tokens con valores base (8192, 16 384, 65 536); detección y rechazo de contexto calculado <= 4096 tokens (`CB-003`, `RF-009`, `CA-007`). |
| **Precheck y Casos Borde** (Integración con mocks) | `python -m unittest tools.gemma.tests.test_precheck.TestPrecheckEscenarios` | Aborto con código 3 y diagnóstico al seleccionar `ESC-M6-C131K` (`CB-007`); aborto si VRAM disponible < presupuesto (`RF-007`); aborto si VRAM no medible (`CB-001`); aborto si RAM libre host < 8192 MiB en MoE CPU (`CB-008`); aborto si contexto resuelto <= 4096 tokens (`CB-003`). |
| **Lanzador y CLI** (Integración) | `python -m unittest tools.gemma.tests.test_lanzador.TestLanzadorEscenarios` | Invocación con `--listar-escenarios` muestra los 9 escenarios y devuelve código 0; invocación con ID inexistente aborta listando los 9 IDs con código 2 (`RF-004`, `CA-003`); invocación con `--escenario` válido inyecta el ID en la ejecución (`RF-003`, `CA-002`); `test_contexto_ajustado_se_recalcula_con_la_vram_del_lanzamiento` verifica que ante 1 cambio de VRAM libre entre la selección y el lanzamiento, el contexto se recalcula con la VRAM del lanzamiento (`CB-005`, `CA-007`). |
| **Registro de ejecución** (Unitario) | `python -m unittest tools.gemma.tests.test_registro.TestRegistroEscenarios` | `test_registro_declara_escenario_y_conformidad` verifica el registro de `escenario_id`, presupuesto declarado, VRAM asignada, VRAM libre, delta y dictamen bajo `consumo <= presupuesto` (`RF-008`, `CA-006`); `test_consumo_excede_presupuesto_conserva_medicion` verifica que el exceso se registra en MiB, la medición se conserva íntegra y el dictamen declara no conformidad (`CB-002`, `CA-006`). |
| **Lanzador `.bat`** (Verificación estática y de comandos) | Ejecución de `src\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat --listar-escenarios` y pruebas de paso de argumentos | Salida esperada: resolución correcta de raíz con `%~dp0`, detección de Python vía las 3 vías de `DEC-015`, propagación de `--listar-escenarios`, código de salida `0`. |
| **Rendimiento de resolución** (No funcional) | `python -m unittest tools.gemma.tests.test_escenarios.TestRendimientoResolucion` | La validación del catálogo y resolución de cualquier escenario seleccionado se completa en menos de 1 segundo (ampliamente inferior al umbral de 5 s de `RNF-001`); `test_perfiles_vigentes_no_se_alteran` verifica que los 3 manifiestos de `src/gemma/perfiles/` quedan intactos tras leer y resolver el catálogo (`RF-012`, `CA-004`). |

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | `src/gemma/escenarios/catalogo.json`, `tools/gemma/escenarios.py` | `TestCatalogoEstructura.test_nueve_escenarios_cobertura_completa`: valida que existan exactamente 9 escenarios que cubran las 3×3 combinaciones y que `ESC-M6-C131K` figure con estado inicial `no_ejecutable`. |
| `RF-002` | `src/gemma/escenarios/catalogo.json`, `tools/gemma/escenarios.py` | `TestCatalogoEstructura.test_identificadores_canonicos_y_estados`: comprueba los 9 identificadores canónicos invariables, 0 duplicados y estados válidos (`declarado`, `medido`, `aprobado`, `no_ejecutable`). |
| `RF-003` | `tools/gemma/lanzador.py` | `TestLanzadorEscenarios.test_seleccion_escenario_registra_id`: comprueba que el servidor se configure con los valores del escenario y registre su ID en la ejecución. |
| `RF-004` | `tools/gemma/lanzador.py`, `tools/gemma/escenarios.py` | `TestLanzadorEscenarios.test_escenario_inexistente_aborta_y_lista_ids`: verifica código de salida 2, rechazo del ID y listado de los 9 identificadores disponibles. |
| `RF-005` | `tools/gemma/escenarios.py`, `tools/gemma/lanzador.py` | `TestOrdenamientoEscenarios.test_orden_jerarquico_determinista`: comprueba la enumeración ordenada por capas MoE en CPU ascendente y luego por contexto efectivo ascendente. |
| `RF-006` | `src/gemma/escenarios/catalogo.json` | `TestCatalogoEstructura.test_presupuestos_vram_desglose_y_ram_sistema`: verifica que cada escenario tenga presupuesto desglosado en pesos, cache_kv, computo y reserva, margen libre >= 512 MiB y campo de RAM requerida de host. |
| `RF-007` | `tools/gemma/precheck.py` | `TestPrecheckEscenarios.test_recursos_insuficientes_aborta`: comprueba que no se inicie el servidor si el presupuesto excede la VRAM o si la RAM libre del host es menor a 8192 MiB en MoE CPU, emitiendo diagnóstico de recursos. |
| `RF-008` | `tools/gemma/registro.py`, `tools/gemma/lanzador.py`, `tools/gemma/tests/test_registro.py` | `TestRegistroEscenarios.test_registro_declara_escenario_y_conformidad`: verifica registro de VRAM asignada, libre y diferencia, evaluando conformidad bajo `consumo <= presupuesto`. |
| `RF-009` | `src/gemma/escenarios/catalogo.json`, `tools/gemma/escenarios.py` | `TestContextoAjustado.test_valores_nominales_y_regla_derivacion`: comprueba valores base (8192, 16 384, 65 536) y la derivación en múltiplos de 1024 tokens. |
| `RF-010` | `tools/gemma/escenarios.py`, `tools/gemma/precheck.py` | `TestContextoAjustado.test_escenario_ajustado_sin_valor_no_seleccionable`: comprueba que un escenario ajustado sin valor numérico no pueda seleccionarse y reporte no disponible. |
| `RF-011` | `tools/gemma/escenarios.py`, `tools/gemma/lanzador.py`, `tools/gemma/tests/test_escenarios.py` | `TestAdmisibilidadEscenarios.test_catalogo_real_declara_la_admisibilidad_por_estado` comprueba que ningún escenario figura como aprobado sin medición y confirmación escrita del propietario, y permite ejecución en `declarado` o `medido`; `TestAdmisibilidadEscenarios.test_modificacion_de_escenario_aprobado_revoca_la_aprobacion`, que implementa `T-017`, comprueba que 1 diferencia en los 4 valores conservados revoca la condición de aprobado y exige 1 medición nueva. |
| `RF-012` | `src/gemma/escenarios/catalogo.json`, `src/gemma/perfiles/` | `TestRendimientoResolucion.test_perfiles_vigentes_no_se_alteran`: verifica que la lectura y ejecución del catálogo no altere ni dependa de los manifiestos en `src/gemma/perfiles/`. |
| `RF-013` | `src/gemma/escenarios/catalogo.json` | `TestCatalogoEstructura.test_siete_parametros_ejecucion_declarados`: comprueba que cada escenario declare explícitamente los 7 parámetros canónicos fijados sin valores nulos. |
| `RNF-001` | `tools/gemma/escenarios.py` | `TestRendimientoResolucion.test_tiempo_resolucion_menor_cinco_segundos`: verifica resolución y validación de escenario en menos de 5 segundos. |
| `RNF-002` | `src/gemma/escenarios/catalogo.json` | `TestCatalogoEstructura.test_campos_obligatorios_sin_vacios`: comprueba que el 100 % de los escenarios declare ID, capas MoE, contexto y presupuesto sin campos vacíos. |
| `RNF-003` | `src/gemma/escenarios/catalogo.json` | `TestCatalogoEstructura.test_conteo_exacto_nueve_escenarios`: comprueba exactamente 9 escenarios, 9 identificadores distintos y 0 combinaciones repetidas. |
| `RNF-004` | `src/gemma/escenarios/catalogo.json` | `TestCatalogoEstructura.test_presupuestos_no_exceden_capacidad_gpu`: valida que ningún presupuesto total supere la capacidad física de la GPU (16 384 MiB). |
| `RNF-005` | `src/gemma/escenarios/catalogo.json` | `TestContextoAjustado.test_cien_por_ciento_ajustados_con_regla`: valida que el 100 % de los escenarios ajustados declare valor numérico y regla determinista registrada. |
| `CB-001` | `tools/gemma/precheck.py` | `TestPrecheckEscenarios.test_vram_no_medible_aborta_sin_estimar`: comprueba aborto con código 3 cuando la VRAM no puede medirse, declarando la ausencia de medición. |
| `CB-002` | `tools/gemma/registro.py`, `tools/gemma/tests/test_registro.py` | `TestRegistroEscenarios.test_consumo_excede_presupuesto_conserva_medicion`: verifica que si consumo > presupuesto, se registre el exceso, se marque no conforme y se preserve la medición. |
| `CB-003` | `tools/gemma/escenarios.py`, `tools/gemma/precheck.py` | `TestContextoAjustado.test_contexto_resuelto_menor_o_igual_4096_aborta`: comprueba que si el contexto resuelto es <= 4096 tokens, el servidor no inicie y emita diagnóstico con código 3. |
| `CB-004` | `tools/gemma/escenarios.py` | `TestOrdenamientoEscenarios.test_declaracion_duplicada_del_par_se_rechaza`: comprueba que el catálogo rechace combinaciones repetidas de capas y contexto e identifique el duplicado. |
| `CB-005` | `tools/gemma/lanzador.py` | `TestLanzadorEscenarios.test_contexto_ajustado_se_recalcula_con_la_vram_del_lanzamiento`: verifica que ante fluctuación de VRAM libre tras la selección, el contexto se recalcula inmediatamente antes de lanzar. |
| `CB-006` | `tools/gemma/escenarios.py`, `tools/gemma/tests/test_escenarios.py` | `TestAdmisibilidadEscenarios.test_modificacion_de_escenario_aprobado_revoca_la_aprobacion`, que implementa `T-017` conforme a `DEC-012`: verifica que modificar capas de expertos en CPU, contexto efectivo, parámetros de ejecución o presupuesto en 1 escenario aprobado revoca la condición de aprobado, nombra el valor que difiere y exige 1 medición nueva. |
| `CB-007` | `tools/gemma/precheck.py` | `TestPrecheckEscenarios.test_escenario_no_ejecutable_aborta_en_precheck`: comprueba que `ESC-M6-C131K` aborte en precheck con código 3 y diagnóstico sin intentar iniciar el servidor. |
| `CB-008` | `tools/gemma/precheck.py` | `TestPrecheckEscenarios.test_ram_host_insuficiente_moe_cpu_aborta`: comprueba que si la RAM libre del host es menor a 8192 MiB al seleccionar capas derivadas a CPU, el precheck aborta con código 3. |
