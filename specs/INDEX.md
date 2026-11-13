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

## Reglas

- Los IDs `SPEC-NNN` no se reutilizan.
- El estado debe coincidir con el frontmatter de `spec.md`.
- El campo `Rama` debe coincidir con la rama Git real declarada en la spec.
- `Release` se rellena con `vX.Y.Z` al publicar.
