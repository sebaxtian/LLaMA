# **Guía Integral: Método EARS (_Easy Approach to Requirements Syntax_) en el Desarrollo Basado en Especificaciones (SDD)**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El método **EARS (_Easy Approach to Requirements Syntax_)** es un marco estructurado de ingeniería de requisitos diseñado para redactar especificaciones en lenguaje natural mediante un conjunto reducido de palabras clave y patrones sintácticos estandarizados deterministas.

En el marco del **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)** puro y los entornos agénticos de desarrollo asistidos por Inteligencia Artificial (como **OpenCode**, Amazon Kiro y GitHub Spec Kit), **EARS** se posiciona como el estándar de redacción funcional por excelencia. Al imponer un orden temporal estricto en las cláusulas, elimina la ambigüedad inherente al texto libre y ofrece directrices operativas inequívocas (_guardrails_) que impiden alucinaciones o interpretaciones erróneas por parte de los modelos de lenguaje.

---

## **1\. Origen y Fundamentos Conceptuales**

**EARS** fue desarrollado originalmente por **Alistair Mavin** y su equipo de ingeniería en **Rolls-Royce plc** durante el análisis de las normativas de aeronavegabilidad aplicadas a los sistemas de control de motores a reacción, siendo publicado oficialmente en 2009\.

El problema central que resuelve EARS es la fragilidad del lenguaje natural libre. En las especificaciones tradicionales, los requisitos suelen redactarse con estructuras desordenadas, mezclando causas, efectos, precondiciones y excepciones en oraciones confusas. EARS introduce una **restricción suave (_gentle constraint_)**: no exige aprender un lenguaje formal matemático o simbólico, sino que disciplina el lenguaje natural estableciendo un orden temporal fijo que obliga a explicitar precondiciones, disparadores y respuestas observables.

Organizaciones de sectores críticos como **Airbus, Bosch, Dyson, Honeywell, Intel, NASA, Rolls-Royce y Siemens** han adoptado EARS para garantizar la máxima precisión en sus sistemas de ingeniería.

---

## **2\. Reglas Generales de Sintaxis EARS**

La estructura universal de una declaración en **EARS** exige que todo requisito contenga de forma estricta los siguientes elementos:

1. **Exactamente un nombre de sistema:** El sujeto ejecutor debe ser explícito e invariable (evitando pronombres o nombres genéricos).
2. **Cero o muchas precondiciones:** Los estados o modos en los que debe encontrarse el sistema antes de actuar.
3. **Cero o un desencadenante (_trigger_):** El evento puntual que activa la acción.
4. **Una o más respuestas del sistema:** La conducta observable obligatoria que el sistema debe ejecutar.

Las cláusulas respetan rigurosamente el **orden temporal de los acontecimientos**: primero se definen los estados previos, luego el evento desencadenante y, por último, la respuesta del sistema.

---

## **3\. Los 5 Patrones Principales y Requisitos Complejos**

**EARS** clasifica los comportamientos de un sistema en **5 patrones sintácticos fundamentales** y una estructura combinatoria para escenarios complejos:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                       PATRONES SINTÁCTICOS EARS                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │ 1. Ubicuo (Sin palabra clave):                                          │
 │    • El/La <nombre del sistema> debe <respuesta del sistema>            │
 │                                                                         │
 │ 2. Dirigido por Eventos (WHEN):                                         │
 │    • Cuando <evento desencadenante>, el/la <sistema> debe <respuesta>   │
 │                                                                         │
 │ 3. Dirigido por Estados (WHILE):                                        │
 │    • Mientras <condición/estado>, el/la <sistema> debe <respuesta>      │
 │                                                                         │
 │ 4. Característica Opcional (WHERE):                                     │
 │    • Donde <opción habilitada>, el/la <sistema> debe <respuesta>        │
 │                                                                         │
 │ 5. Comportamiento No Deseado / Excepción (IF / THEN):                   │
 │    • Si <error/excepción>, entonces el/la <sistema> debe <respuesta>    │
 ├─────────────────────────────────────────────────────────────────────────┤
 │ 6. Requisito Complejo (Combinación):                                    │
 │    • Mientras <estado>, cuando <evento>, el/la <sistema> debe...        │
 └─────────────────────────────────────────────────────────────────────────┘
```

&nbsp;

### **3.1. Patrón Ubicuo (Ubiquitous)**

Aplica a propiedades o comportamientos continuos que el sistema debe satisfacer en todo momento, sin requerir un desencadenante externo ni condiciones previas.

- **Fórmula Sintáctica:** `El/La <nombre del sistema> debe <respuesta del sistema>`
- **Palabra Clave:** Ninguna (declaración directa).
- **Ejemplo del Cuaderno:** _"El teléfono móvil debe tener una masa menor a 150 gramos."_

### **3.2. Patrón Dirigido por Eventos (_Event-Driven_)**

Define cómo responde el sistema inmediatamente después de que ocurre un estímulo o evento puntual.

- **Fórmula Sintáctica:** `Cuando <evento desencadenante>, el/la <nombre del sistema> debe <respuesta del sistema>`
- **Palabra Clave:** **WHEN (Cuando)**.
- **Ejemplo del Cuaderno:** _"Cuando se seleccione 'silenciar', la computadora portátil debe suprimir toda salida de audio."_

### **3.3. Patrón Dirigido por Estados (_State-Driven_)**

Aplica mientras el sistema se encuentre activo en un estado, modo o condición previa prolongada.

- **Fórmula Sintáctica:** `Mientras <condición o estado activo>, el/la <nombre del sistema> debe <respuesta del sistema>`
- **Palabra Clave:** **WHILE (Mientras)**.
- **Ejemplo del Cuaderno:** _"Mientras no haya tarjeta en el cajero automático, el cajero automático debe mostrar 'inserte tarjeta para comenzar'."_

### **3.4. Patrón de Característica Opcional (_Optional Feature_)**

Aplica exclusivamente a variantes de producto, módulos o versiones de software que incorporan una capacidad opcional específica.

- **Fórmula Sintáctica:** `Donde <característica opcional habilitada>, el/la <nombre del sistema> debe <respuesta del sistema>`
- **Palabra Clave:** **WHERE (Donde / Si el sistema incluye)**.
- **Ejemplo del Cuaderno:** _"Donde el vehículo incluya techo solar, el vehículo debe tener un panel de control del techo solar en la puerta del conductor."_

### **3.5. Patrón de Comportamiento No Deseado / Excepción (_Unwanted Behaviour_)**

Especifica la reacción formal del sistema ante situaciones anormales, fallos de entrada, caídas de conectividad o errores de usuario.

- **Fórmula Sintáctica:** `Si <condición no deseada o error>, entonces el/la <nombre del sistema> debe <respuesta del sistema>`
- **Palabra Clave:** **IF / THEN (Si / Entonces)**.
- **Ejemplo del Cuaderno:** _"Si se ingresa un número de tarjeta de crédito no válido, entonces el sitio web debe mostrar 'por favor reingrese los detalles de la tarjeta de crédito'."_

### **3.6. Requisitos Complejos (_Complex Requirements_)**

Cuando la lógica de negocio requiere modelar múltiples dimensiones operativas simultáneas, los patrones simples se combinan respetando estrictamente el orden: estados primero, eventos después y excepciones finales.

- **Fórmula Sintáctica Combinada:** `Mientras <estado>, cuando <evento>, el/la <nombre del sistema> debe <respuesta del sistema>`
- **Ejemplo del Cuaderno:** _"Mientras la aeronave esté en tierra, cuando se ordene empuje inverso, el sistema de control del motor debe habilitar el empuje inverso."_

---

## **4\. Rol e Integración en el Ciclo de Vida SDD**

En la metodología de Desarrollo Basado en Especificaciones, **EARS** constituye el lenguaje vehicular de los requisitos funcionales dentro del artefacto **`specs/NNN-slug/spec.md`**, operando como el puente de precisión a lo largo del flujo:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 2: ESPECIFICACIÓN (Specify)                     │
 │  • Redacción de requisitos en spec.md usando la notación EARS           │
 │  • Asignación de identificadores unívocos (RF-001, RF-002, etc.)        │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                    ETAPA 3: CLARIFICACIÓN (Clarify)                     │
 │  • Auditoría QA: inspección de patrones incompletos (falta de "THEN")   │
 │  • Detección y cierre de casos borde con cláusulas IF / THEN            │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │               ETAPAS 5 Y 6: TAREAS (Tasks) E IMPLEMENTACIÓN (TDD)       │
 │  • Cada requisito EARS se vincula a una prueba unitaria / de contrato   │
 │  • La cláusula del evento define el test; la respuesta define el assert │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 7: VALIDACIÓN (Validate)                      │
 │  • Matriz de trazabilidad: comprobación 1 a 1 de requisitos EARS        │
 └─────────────────────────────────────────────────────────────────────────┘
```

&nbsp;

1. **En la Etapa 2 (Especificación):** Garantiza que los requisitos no se redacten como ideas difusas, sino como contratos funcionales verificables.
2. **En la Etapa 3 (Clarificación):** El equipo o un subagente de IA inspecciona la especificación buscando requisitos que carezcan del patrón de comportamiento no deseado (`IF / THEN`), forzando a definir los casos de borde antes del diseño técnico.
3. **En las Etapas 5 y 6 (Tareas e Implementación TDD):** La estructura `CUANDO -> DEBE` se traduce de forma natural en el paradigma de testing `Given-When-Then` o en pruebas automatizadas directas (el desencadenante se convierte en la acción de prueba y la respuesta esperada en la aserción o _assert_).
4. **En la Etapa 7 (Validación):** Permite construir una matriz de trazabilidad inequívoca, donde cada identificador EARS (`RF-xxx`) se evalúa contra una suite de pruebas para certificar la convergencia del software.

---

## **5\. Ventajas y Limitaciones Técnicas**

### **5.1. Ventajas Clave**

- **Eliminación Drástica de la Ambigüedad:** Obliga al redactor a explicitar siempre quién actúa, en qué momento y bajo qué precondiciones.
- **Baja Curva de Aprendizaje:** Al utilizar lenguaje natural disciplinado, cualquier ingeniero, analista de negocio o líder de producto puede redactar requisitos sin necesidad de software costoso ni capacitación formal compleja.
- **Efectividad para Hablantes No Nativos:** Al contar con estructuras y palabras clave fijas, nivela la calidad de redacción técnica entre equipos distribuidos globalmente.
- **Traducción Directa a Pruebas Automatizadas:** La separación funcional nítida facilita que desarrolladores humanos y agentes deriven de inmediato pruebas unitarias, de integración o contratos OpenAPI.
- **Optimización para Agentes de IA:** Los modelos de lenguaje procesan los patrones **EARS** sin margen para la suposición, eliminando la invención de reglas de negocio en el código (_intent drift_).
- **Compatibilidad Universal:** Se integra de forma limpia en archivos Markdown versionados en repositorios Git (`spec.md`).

### **5.2. Desventajas y Limitaciones**

- **Complejidad ante Múltiples Precondiciones:** Si una regla de negocio depende de más de tres o cuatro condiciones simultáneas, la sintaxis **EARS** genera oraciones excesivamente largas y difíciles de procesar.
- **Inadecuado para Modelado Matemático Avanzado:** No está diseñado para representar cálculos matriciales complejos, fórmulas estadísticas continuas o grafos de transición de estados.
- **Limitado para Restricciones Arquitectónicas Globales:** Los requisitos no funcionales cualitativos (por ejemplo, directrices de diseño de software o políticas de gobernanza que deben ir en `constitution.md`) no siempre pueden formularse con un patrón condicional.

---

## **6\. Plantilla Estándar y Ejemplo de Integración en `spec.md`**

### **6.1. Plantilla Markdown de Sección de Requisitos EARS**

```
# spec.md (Ejemplo base)

## Requisitos Funcionales (Notación EARS)

### Requisitos Ubicuos
- **RF-001 (Ubicuo):** El [Nombre del Sistema] debe [comportamiento siempre activo].

### Requisitos Dirigidos por Eventos
- **RF-002 (Evento):** Cuando [evento desencadenante], el [Nombre del Sistema] debe [respuesta observable].

### Requisitos Dirigidos por Estados
- **RF-003 (Estado):** Mientras [estado o precondición activa], el [Nombre del Sistema] debe [respuesta observable].

### Requisitos de Características Opcionales
- **RF-004 (Opción):** Donde [opción habilitada], el [Nombre del Sistema] debe [respuesta observable].

### Requisitos de Comportamiento No Deseado / Excepciones
- **RF-005 (Error):** Si [condición anómala o error], entonces el [Nombre del Sistema] debe [respuesta observable].

### Requisitos Complejos
- **RF-006 (Complejo):** Mientras [estado], cuando [evento], el [Nombre del Sistema] debe [respuesta observable].
```

---

### **6.2. Ejemplo Real: Módulo de Autenticación de Usuarios (`specs/auth/spec.md`)**

```
# spec.md (Ejemplo base)

# Especificación: Módulo de Autenticación de Usuarios

## 1. Contexto y Alcance
Módulo responsable de verificar la identidad de los usuarios y gestionar las sesiones activas en la plataforma.

## 2. Requisitos Funcionales (Notación EARS)

- **RF-001 (Ubicuo):** El Servidor de Autenticación debe almacenar las contraseñas de los usuarios utilizando el algoritmo de derivación de claves Argon2id con salt aleatorio.

- **RF-002 (Evento):** Cuando el Usuario envíe un correo electrónico y una contraseña válidos en el formulario de inicio de sesión, el Servidor de Autenticación debe emitir un token JWT firmado y redirigir al Usuario al panel principal.

- **RF-003 (Estado):** Mientras el Token de Sesión se mantenga vigente y no expirado, el Servidor de Autenticación debe autorizar el acceso a las rutas protegidas de la API.

- **RF-004 (Opción):** Donde la Autenticación de Dos Factores (2FA) esté habilitada en la cuenta, el Servidor de Autenticación debe solicitar el código TOTP de 6 dígitos antes de emitir el token JWT.

- **RF-005 (Error/Excepción):** Si se registran cinco intentos fallidos consecutivos de inicio de sesión para una misma cuenta, entonces el Servidor de Autenticación debe bloquear la cuenta temporalmente por un período de 15 minutos y enviar un correo de notificación al titular.

- **RF-006 (Complejo):** Mientras la cuenta se encuentre bloqueada por intentos fallidos, cuando el Usuario intente autenticarse, el Servidor de Autenticación debe rechazar la solicitud mostrando el tiempo restante de bloqueo.
```

---
