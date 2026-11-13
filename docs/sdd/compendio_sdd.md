# **Compendio Integral: Desarrollo Basado en Especificaciones (SDD)**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)** es una metodología de ingeniería de software en la que una especificación formal, estructurada y legible por máquina actúa como la guía o fuente de verdad del sistema antes de escribir código ejecutable.

Frente a la improvisación de instrucciones no estructuradas (_vibe coding_), el SDD fundamenta el ciclo de vida del software en el rigor de los contratos, eliminando la ambigüedad y garantizando que tanto los desarrolladores humanos como los agentes de Inteligencia Artificial dispongan de un marco determinista de trabajo.

---

## **1\. Fundamentos y Taxonomía del SDD**

Formalizada y referenciada en la industria por publicaciones de entidades y autores como Thoughtworks, Martin Fowler, IBM y la comunidad de ingeniería nativa de IA, la adopción del SDD se clasifica en **tres niveles o enfoques principales**.

La diferencia central entre estos tres enfoques radica en **qué ocurre con la especificación una vez que el código ya ha sido implementado** y cuál de los dos artefactos actúa como la fuente de verdad definitiva:

```
      BAJO COMPROMISO <─────────────────────────────────────────> ALTO COMPROMISO

 ┌────────────────────────┐   ┌─────────────────────────┐   ┌────────────────────────┐
 │       Spec-First       │   │     Spec-Anchored       │   │     Spec-as-Source     │
 ├────────────────────────┤   ├─────────────────────────┤   ├────────────────────────┤
 │ • La spec arranca el   │   │ • La spec y el código   │   │ • La spec es la ÚNICA  │
 │   desarrollo.          │   │   conviven y evolucionan│   │   fuente editada.      │
 │ • La spec puede        │   │   juntos en Git.        │   │ • El código se         │
 │   obsoletearse post-   │   │ • Doble fuente de       │   │   regenera al 100%     │
 │   generación.          │   │   verdad sincronizada.  │   │   vía compiladores/IA. │
 │ • Ideal para PoCs.     │   │ • Ideal para Enterprise │   │ • Ideal para SDKs.     │
 └────────────────────────┘   └─────────────────────────┘   └────────────────────────┘
```

---

## **2\. Los Tres Niveles de Adopción de SDD**

### **2.1. Spec-First (Especificación Primero / Prioridad en Especificaciones)**

#### **Concepto y Funcionamiento**

En el enfoque **Spec-First**, la especificación se redacta detalladamente antes de escribir cualquier línea de código. Sirve como el "punto de entrada" al desarrollo para establecer claridad inicial, guiar la arquitectura o servir de instrucción (_prompt_ estructurado) a desarrolladores o agentes de IA. Sin embargo, **una vez que el código inicial es generado o implementado, la especificación no necesariamente se mantiene activa** ni se actualiza de forma continua.

#### **Diferencias Clave**

- **Fuente de verdad:** El **código fuente** pasa a ser la fuente de verdad definitiva una vez completada la fase inicial de generación.
- **Acoplamiento:** El compromiso o acoplamiento con la especificación es **bajo**.
- **Mantenimiento:** La especificación suele quedar estática o "morir" tras la entrega del código inicial.

#### **Ventajas**

- **Claridad inicial rápida:** Elimina la ambigüedad en la fase de análisis sin imponer la carga administrativa de mantener documentación sincronizada a largo plazo.
- **Baja fricción de entrada:** Es la forma más sencilla de comenzar a utilizar SDD en equipos acostumbrados al desarrollo tradicional.
- **Aceleración inicial con IA:** Permite estructurar la idea inicial para que un agente de IA genere el esqueleto o prototipo sin bloqueos.

#### **Desventajas**

- **Obsolescencia (_Intent Drift_):** A medida que el software evoluciona y se agregan refactorizaciones o correcciones directas en el código, la especificación queda desactualizada rápidamente.
- **Pérdida de trazabilidad:** Futuros desarrolladores o agentes de IA no podrán confiar en la especificación original para entender el comportamiento actual del sistema.

#### **Casos de Uso Típicos**

- Prototipos rápidos o pruebas de concepto (_PoC_).
- Proyectos pequeños con ciclo de vida corto o de una sola entrega.
- Tareas delimitadas donde el objetivo es arrancar la implementación sin requerir gobernanza a largo plazo.

---

### **2.2. Spec-Anchored (Especificación Anclada / Gobernanza Continua)**

#### **Concepto y Funcionamiento**

El paradigma **Spec-Anchored** establece que la especificación **acompaña al código durante todo el ciclo de vida del software**, manteniéndose viva, versionada en Git y sincronizada con las iteraciones del sistema. Si los requisitos cambian, primero se actualiza la especificación y luego el código (o se reflejan bidireccionalmente los cambios) mediante pruebas de contrato y pipelines de CI/CD.

#### **Diferencias Clave**

- **Fuente de verdad:** **Doble fuente de verdad sincronizada** (el código y la especificación coexisten y se validan mutuamente).
- **Acoplamiento:** El compromiso con la especificación es **medio-alto** y de gobernanza continua.
- **Mantenimiento:** Requiere actualizar la especificación en cada nueva funcionalidad o cambio arquitectónico.

#### **Ventajas**

- **Prevención de desalineación (_Drift_):** Garantiza que la documentación ejecutadora y la intención del producto coincidan exactamente con lo que ejecuta el código.
- **Excelente para Agentes de IA:** Otorga a los agentes de IA un marco de contexto (_guardrails_) actualizado para refactorizar o añadir _features_ sin romper reglas preexistentes.
- **Equilibrio práctico:** Es considerado el punto más sostenible y escalable entre rigor arquitectónico y flexibilidad de ingeniería.

#### **Desventajas**

- **Disciplina de equipo obligatoria:** Si un desarrollador modifica el código sin actualizar la especificación (o viceversa), el sistema de gobernanza se rompe.
- **Esfuerzo continuo:** Exige integrar herramientas de validación de contratos (como linters o test de contrato automatizados) en el flujo de integración continua.

#### **Casos de Uso Típicos**

- Sistemas empresariales, arquitecturas de microservicios y aplicaciones de producción de mediano y largo plazo.
- Equipos colaborativos que desarrollan junto a agentes de IA (ej. OpenCode, Claude Code, GitHub Copilot).
- APIs y contratos de integración donde múltiples equipos dependen de la misma especificación.

---

### **2.3. Spec-as-Source (Especificación como Código Fuente / Spec como Programa)**

#### **Concepto y Funcionamiento**

En el nivel de abstracción más alto, **Spec-as-Source** posiciona a la especificación abstracta como **el único archivo que el ser humano edita directamente**. En este modelo, los desarrolladores no escriben ni modifican el código de implementación ejecutable; este es generado al 100% de forma automática por compiladores, _emitters_ o agentes de IA a partir de la especificación.

#### **Diferencias Clave**

- **Fuente de verdad:** La **especificación es la única fuente de verdad**; el código es únicamente un producto compilado o derivado.
- **Acoplamiento:** Compromiso **absoluto y total** con la especificación.
- **Intervención humana:** El programador jamás edita el código generado directamente; si hay un fallo o cambio, se modifica la especificación y se recompila todo el sistema.

#### **Ventajas**

- **Cero inconsistencias:** Inexistencia total de divergencia entre la especificación y el código ejecutable.
- **Automatización extrema:** Permite generar SDKs multilenguaje, _stubs_ de servidor, esquemas de bases de datos y suites de prueba de manera instantánea.
- **Sustitución de código:** Facilita migrar de lenguaje o _stack_ tecnológico cambiando únicamente los compiladores/_emitters_ sin tocar la lógica escrita.

#### **Desventajas**

- **Inflexibilidad y rigidez:** Si el generador o agente de IA comete un error en un caso borde, no se puede "parchear" el código a mano sin romper el pipeline de generación.
- **Dependencia de la madurez tecnológica:** Requiere compiladores de especificaciones extremadamente robustos o modelos de IA con bajísima tasa de alucinación.

#### **Casos de Uso Típicos**

- Generación automatizada de SDKs de API en múltiples lenguajes (herramientas como Fern, Stainless o Speakeasy).
- Definición de contratos de API con lenguajes de modelado como TypeSpec para emitir OpenAPI, Protobuf o JSON Schema.
- Sistemas de modelos de datos altamente estandarizados o arquitecturas impulsadas totalmente por compiladores.

---

## **3\. Matriz Comparativa de los Tres Enfoques**

| Dimensión de Análisis       | Spec-First                                            | Spec-Anchored                                   | Spec-as-Source                              |
| :-------------------------- | :---------------------------------------------------- | :---------------------------------------------- | :------------------------------------------ |
| **Fuente de Verdad**        | El código fuente (tras la fase inicial)               | Doble fuente de verdad sincronizada             | La especificación abstracta                 |
| **Rol del Humano**          | Escribe la spec inicial y luego programa/edita código | Mantiene la spec y edita/revisa código e IA     | Solo edita la especificación                |
| **Rol del Código**          | Artefacto principal de trabajo post-inicio            | Artefacto coordinado que evoluciona con la spec | Subproducto automatizado/compilado          |
| **Riesgo de _Drift_**       | **Alto** (la spec queda obsoleta rápido)              | **Bajo** (mitigado por CI/CD y pruebas)         | **Nulo** (el código siempre se regenera)    |
| **Complejidad de Adopción** | **Baja** (ideal para iniciar)                         | **Media** (requiere disciplina de equipo)       | **Alta** (exige madurez de herramientas/IA) |
| **Enfoque Principal**       | Claridad y velocidad al arrancar                      | Mantenibilidad, gobernanza y calidad            | Automatización total e interoperabilidad    |

---

## **4\. Conclusión Práctica para la Ingeniería Moderna**

En la práctica diaria de la ingeniería de software actual, **el nivel Spec-Anchored (o un híbrido entre Spec-First y Spec-Anchored) es la opción más recomendada y extendida**. Ofrece el equilibrio ideal al permitir que los desarrolladores y agentes de IA colaboren sobre un plan claro y verificado, manteniendo el control de calidad sobre el código sin caer en la rigidez extrema de prohibir la edición directa del código fuente.

---
