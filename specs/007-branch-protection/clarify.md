# Clarificación — SPEC-007

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados a `spec.md`).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** El protocolo general SDD exige que todo cambio o incremento cuente con una especificación previa aprobada. Asimismo, las ramas permitidas en el flujo Git estándar se limitan a `feat/*`, `fix/*` y `hotfix/*`. No se encontraba formalizado el uso de ramas dedicadas para la preparación y corte de versiones, ni su denominación exacta o exención de spec.
- **Pregunta:** ¿Se admiten ramas auxiliares para la preparación de releases, qué formato exacto deben tener y cuál es su exigencia respecto al ciclo SDD?
- **Respuesta:** Se admiten formalmente ramas auxiliares de empaquetado bajo la nomenclatura `release/*`, empleando guiones en la versión (`release/vX-Y-Z`, por ejemplo `release/v0-2-0`). Estas ramas quedan exentas de requerir una especificación funcional previa, dado que su alcance se restringe exclusivamente al empaquetado, cierre de changelog y preparación de release.
- **Decisión:** Se incorpora en `spec.md` el reconocimiento de ramas `release/vX-Y-Z` como ramas autorizadas sin spec previa dentro de Actores y permisos, Fuera de alcance y en el nuevo caso borde CB-009.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** La redacción preliminar de RF-002, RF-008 y CB-005 contemplaba o toleraba que el Propietario realizara envíos directos (`push`) de commits `chore: prepare release vX.Y.Z` a la rama `dev` mediante excepciones o bypass de protección. Esto vulnera el principio de integración determinista y trazabilidad integral mediante Pull Requests.
- **Pregunta:** ¿Debe permitirse el push directo del commit `chore: prepare release` a la rama `dev` o debe canalizarse obligatoriamente mediante Pull Request?
- **Respuesta:** Se elimina categóricamente todo commit directo a `dev` para la preparación de releases. Toda preparación de release debe realizarse en su rama auxiliar `release/vX-Y-Z` e integrarse hacia `dev` y `main` de manera exclusiva a través de Pull Request.
- **Decisión:** Se reformula CB-005 para rechazar cualquier envío directo de `chore: prepare release` en `dev` sin excepción de actor, exigiendo su canalización por Pull Request. Se ajustan en consecuencia RF-002, RF-008 y CA-001.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** La exigencia de revisiones aprobatorias en Pull Requests dentro de GitHub ("Require pull request reviews before merging") puede ajustarse a uno o más revisores. Al encontrarse el repositorio en fase de desarrollo unipersonal bajo la titularidad de Agent Sebaxtian, exigir 1 o más aprobaciones genera un bloqueo insalvable (deadlock), puesto que GitHub no permite que el autor de un PR apruebe su propia solicitud.
- **Pregunta:** ¿Cuál debe ser el umbral de aprobaciones mínimas requeridas en las reglas de protección remota durante la fase operativa actual?
- **Respuesta:** Se fija el umbral en cero (0) aprobaciones mínimas requeridas (`required_approving_review_count: 0`) para la etapa unipersonal actual, garantizando la apertura formal y auditoría del Pull Request sin incurrir en deadlock. En una etapa colaborativa futura se elevará el requerimiento a una (1) o más aprobaciones.
- **Decisión:** Se incorpora el requisito funcional RF-009 y el criterio CA-010 para especificar 0 aprobaciones mínimas requeridas en la fase unipersonal. Se añade el caso borde CB-010.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** Los requisitos RF-006, CB-003, CB-007, CB-008, CA-005 y CA-007 describían el bloqueo remoto de Pull Requests basado en la superación de comprobaciones de integración continua (CI) en GitHub Actions. Sin embargo, el repositorio no dispone actualmente de flujos de trabajo en `.github/workflows/`. Habilitar la exigencia de status checks específicos en las reglas de protección remota sin la existencia previa de los jobs correspondientes resultaría inoperativo o bloquearía indeterminadamente las integraciones.
- **Pregunta:** ¿Cómo deben articularse los status checks de CI en la regla remota de protección en la presente especificación?
- **Respuesta:** La designación técnica de status checks obligatorios de GitHub Actions se difiere formalmente a una especificación posterior, una vez que los flujos de CI sean desarrollados e integrados en `.github/workflows/`. En la presente especificación, la protección remota blinda la gobernanza de ramas e inmutabilidad, mientras que la validación técnica continúa ejecutándose de modo determinista localmente con `validate.py`.
- **Decisión:** Se condicionan los enunciados de RF-006, CB-003, CB-007, CB-008, CA-005 y CA-007 al aprovisionamiento formal de los flujos de CI, y se aclara explícitamente en Fuera de alcance que la creación de workflows y la designación activa de checks obligatorios en GitHub quedan diferidas a una spec posterior.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** RF-005 y CB-004 prohíben la ejecución de fusiones mediante rebase o squash en `main` y `dev`, imponiendo exclusivamente merge commits sin avance rápido (`merge --no-ff`). Es necesario definir cómo se materializa técnicamente esta prohibición a nivel de plataforma remota.
- **Pregunta:** ¿Qué mecanismo técnico de GitHub debe aplicarse para impedir de forma absoluta las fusiones de tipo squash y rebase?
- **Respuesta:** En los ajustes generales del repositorio en GitHub (`Repository Settings -> General -> Pull Requests`) se deshabilitan explícitamente las opciones `Allow squash merging` y `Allow rebase merging`, manteniendo habilitada de forma exclusiva la opción `Allow merge commits`.
- **Decisión:** Se ratifica en RF-005, CB-004 y CA-004 la desactivación técnica global de las opciones de squash y rebase en los ajustes del repositorio.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** GitHub dispone de una regla de protección ("Require signed commits") que rechaza cualquier commit que no posea firma criptográfica GPG o SSH. En la infraestructura local actual no se cuenta con claves criptográficas estandarizadas en todas las estaciones de trabajo y agentes, por lo que su activación inmediata impediría contribuciones ordinarias legítimas.
- **Pregunta:** ¿Debe exigirse la firma obligatoria de commits en las reglas de protección de esta fase?
- **Respuesta:** No. La regla de verificación de commits firmados ("Require signed commits") debe mantenerse desactivada inicialmente para salvaguardar la continuidad operativa de los entornos de desarrollo locales y agentes.
- **Decisión:** Se añade el requisito RF-010, el caso borde CB-011 y el criterio CA-011 para explicitar la desactivación inicial de la exigencia de commits firmados.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-009

SI un actor crea una rama auxiliar para empaquetado de versión con nomenclatura `release/vX-Y-Z`, ENTONCES el sistema DEBE admitir la creación y procesamiento de dicha rama sin exigir una especificación funcional previa.

### CB-010

SI el autor de un Pull Request en fase unipersonal solicita la integración del cambio habiendo superado los requisitos estructurales sin contar con aprobaciones de terceros, ENTONCES el sistema DEBE permitir la fusión sin incurrir en bloqueo por falta de aprobadores.

### CB-011

SI un commit incorporado en un Pull Request no cuenta con firma digital GPG o SSH, ENTONCES el sistema DEBE aceptar el commit sin rechazarlo por ausencia de firma criptográfica.

## Parches aplicados a `spec.md`

- [x] Frontmatter: estado actualizado a `clarified`, versión incrementada a `0.2.0` y fecha sincronizada (AMB-001 a AMB-006).
- [x] Actores y permisos: inclusión formal de ramas `release/vX-Y-Z` y acotación del mecanismo de bypass a situaciones críticas no rutinarias (AMB-001, AMB-002).
- [x] RF-002: eliminación de excepción de bypass rutinario para envíos directos (AMB-002).
- [x] RF-005: explicitación de commit de merge sin avance rápido vía Pull Request y desactivación técnica de squash y rebase (AMB-005).
- [x] RF-006: condicionamiento de comprobaciones automatizadas a la futura existencia de flujos de CI (AMB-004).
- [x] RF-008: circunscripción del bypass de protección a emergencias críticas autorizadas por el Propietario (AMB-002).
- [x] RF-009: requisito funcional de 0 revisiones aprobatorias mínimas requeridas en fase unipersonal (AMB-003).
- [x] RF-010: requisito funcional de no exigencia de firmas criptográficas en commits (AMB-006).
- [x] CB-003, CB-007, CB-008: condicionamiento formal al aprovisionamiento de flujos de CI (AMB-004).
- [x] CB-004: ratificación del bloqueo técnico de squash y rebase en ajustes de repositorio (AMB-005).
- [x] CB-005: rechazo sin excepción de push directo de `chore: prepare release` a `dev` (AMB-002).
- [x] CB-009: admisión formal de ramas `release/vX-Y-Z` exentas de spec previa (AMB-001).
- [x] CB-010: ausencia de bloqueo por falta de revisiones de terceros en etapa unipersonal (AMB-003).
- [x] CB-011: aceptación de commits sin firma criptográfica (AMB-006).
- [x] Fuera de alcance: diferimiento formal de flujos de CI y status checks en GitHub Actions a spec posterior (AMB-004), y admisión de ramas `release/vX-Y-Z` (AMB-001).
- [x] Criterios de aceptación CA-001 a CA-011: actualización de coberturas y redacción con trazabilidad completa para los nuevos requisitos y casos borde (AMB-001 a AMB-006).
- [x] Historial de cambios: registro de versión 0.2.0 tras etapa de clarificación.

## Decisiones de negocio

- Las ramas `release/vX-Y-Z` constituyen el único tipo de rama temporal exento de redacción de spec, dado que no introducen cambios de comportamiento funcional, limitándose al cierre documental y corte de release.
- La eliminación del commit directo en `dev` para releases garantiza que todo el historial de las ramas protegidas proceda incondicionalmente de fusiones gobernadas vía Pull Request.
- La fijación de 0 revisiones requeridas responde a la realidad unipersonal del proyecto, programándose su elevación a 1 en el momento en que se formalice la incorporación de revisores adicionales.
- Los status checks automáticos en GitHub se implementarán en una especificación complementaria dedicada a CI, evitando dependencias circulares o bloqueos tempranos en la configuración de protección remota.
