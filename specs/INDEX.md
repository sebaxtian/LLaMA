# Registro de especificaciones (SPECs)

Registro canónico del proyecto. Cada feature, fix, refactor o cambio de configuración que requiera spec queda registrado aquí.

| ID | Título | Estado | Rama | Release | Ruta |
|---|---|---|---|---|---|
| SPEC-001 | Menú principal main.bat | released | feat/main-menu | v0.2.0 | specs/001-main-menu/ |
| SPEC-002 | Orquestación de subagentes SDD | released | feat/orquestacion-subagentes-sdd | v0.3.0 | specs/002-orquestacion-subagentes-sdd/ |
| SPEC-003 | Validación estricta de la compuerta G4 | released | feat/validacion-g4 | v0.3.1 | specs/003-validacion-g4/ |
| SPEC-004 | Subagente documenter para correcciones normativas | released | feat/editor-documentacion | v0.4.0 | specs/004-editor-documentacion/ |
| SPEC-005 | Compuertas completas y deuda residual | released | feat/compuertas-completas | v0.5.0 | specs/005-compuertas-completas/ |
| SPEC-006 | Cierre de observaciones de documentación | released | feat/observaciones-cierre | v0.5.1 | specs/006-observaciones-cierre/ |
| SPEC-007 | Protección determinista de ramas GitHub | released | feat/branch-protection | v0.6.0 | specs/007-branch-protection/ |
| SPEC-008 | Auditoría de cumplimiento SDD | released | feat/auditoria-cumplimiento-sdd | v0.7.0 | specs/008-auditoria-cumplimiento-sdd/ |
| SPEC-009 | Nueva base normativa SDD | released | feat/base-normativa-sdd-v2 | v0.7.0 | specs/009-base-normativa-sdd/ |
| SPEC-010 | Mecanismo de control SDD verificable | released | feat/mecanismo-control-sdd | v0.7.0 | specs/010-mecanismo-control-sdd/ |
| SPEC-011 | Práctica operativa SDD verificable | released | feat/practica-operativa-sdd | v0.7.0 | specs/011-practica-operativa-sdd/ |
| SPEC-012 | Trazabilidad profunda SDD verificable | released | feat/trazabilidad-profunda-sdd | v0.7.0 | specs/012-trazabilidad-profunda-sdd/ |
| SPEC-013 | Cierre de la reauditoría de conformidad | released | feat/reauditoria-cierre | v0.7.0 | specs/013-cierre-reauditoria-conformidad/ |
| SPEC-014 | Cierre de las observaciones de la reauditoría final | released | feat/cierre-observaciones-finales | v0.7.0 | specs/014-cierre-observaciones-finales/ |
| SPEC-015 | Cierre de la auditoría posterior al release | released | feat/cierre-auditoria-posterior | v0.7.1 | specs/015-cierre-auditoria-posterior/ |
| SPEC-016 | Cierre de la auditoría de v0.7.1 | validated | feat/cierre-auditoria-v0-7-1 | — | specs/016-cierre-auditoria-v0-7-1/ |

## Reglas

- Los IDs `SPEC-NNN` no se reutilizan.
- El estado debe coincidir con el frontmatter de `spec.md`.
- El campo `Rama` debe coincidir con la rama Git real declarada en la spec.
- `Release` se rellena con `vX.Y.Z` al publicar.
