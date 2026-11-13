# Registro de especificaciones (SPECs)

Registro canónico del proyecto. Cada feature, fix, refactor o cambio de configuración que requiera spec queda registrado aquí.

| ID | Título | Estado | Rama | Release | Ruta |
|---|---|---|---|---|---|
| SPEC-001 | Menú principal main.bat | released | feat/main-menu | v0.2.0 | specs/001-main-menu/ |
| SPEC-002 | Orquestación de subagentes SDD | released | feat/orquestacion-subagentes-sdd | v0.3.0 | specs/002-orquestacion-subagentes-sdd/ |
| SPEC-003 | Validación estricta de la compuerta G4 | implemented | feat/validacion-g4 |  | specs/003-validacion-g4/ |

## Reglas

- Los IDs `SPEC-NNN` no se reutilizan.
- El estado debe coincidir con el frontmatter de `spec.md`.
- El campo `Rama` debe coincidir con la rama Git real declarada en la spec.
- `Release` se rellena con `vX.Y.Z` al publicar.