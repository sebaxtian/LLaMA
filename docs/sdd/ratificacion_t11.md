# Acta de ratificación de la transición T11

*Acto del propietario. Ratifica la incorporación de la transición `T11` al protocolo operativo y al validador, a efectos del cierre de `H-02` del informe `docs/sdd/auditoria_release_v0_8_0.md`.*

## 1. Fecha y autoridad

- Fecha: 2026-11-24 (UTC).
- Autoridad: `Agent Sebaxtian`, propietario del régimen.
- Clave de firma: la declarada en `docs/sdd/firmantes_autorizados`.
- Carácter: ratificación de una modificación de la base incorporada sin spec previa, no aprobación de compuerta.

## 2. Cuestión

El commit `c5d1b1d`, sellado `feat(spec-017)`, incorporó la transición `T11` a la tabla de §5 de `docs/sdd/PROTOCOLO_OPERATIVO.md`, la constante homónima de `tools/sdd/validate.py` y 65 líneas de prueba en `tools/sdd/tests/test_validate.py`. La habilitación consta en la «Constancia de corrección» de `docs/sdd/PROTOCOLO_OPERATIVO.md §5:137`, que declara la incorporación «por corrección autorizada directamente por el propietario, sin spec intermedia», y `docs/constitution.md §8:84` exige spec aprobada previa para todo cambio de la base que no sea exclusivamente editorial. El informe previo al release lo registra como `H-02`, de severidad `Alta`.

## 3. Ratificación

El propietario ratifica el acto y sus efectos: la transición `T11` que admite la reversión a `draft` desde `tasked`, `implementing`, `implemented` y `validated` cuando el propietario aprueba un cambio de requisito; la constante que la implementa en el validador; las pruebas que la acreditan; y la constancia que la declara.

La ratificación no convierte la vía en precedente: ningún cambio de los rangos 1 a 4 se incorpora en lo sucesivo sin spec aprobada, y la única excepción sigue siendo el cambio exclusivamente editorial. No modifica el texto de la constitución, del protocolo ni del validador: fija el alcance del acto ya ejecutado y acredita su autoría.

## 4. Alcance y límites

- La ratificación alcanza solo a `T11` y a sus tres implementaciones.
- No autoriza cambios futuros sin spec.
- No altera requisitos, casos borde ni criterios de aceptación de `SPEC-017`.
- No declara compuerta alguna.
- El cambio queda registrado en `CHANGELOG.md` bajo `Unreleased`.

## 5. Registro

- Hallazgo cerrado: `H-02`, con la fila `AUD-115` de `docs/sdd/inventario_hallazgos.md` en el estado `cerrado por ratificación`.
- Informe de origen: `docs/sdd/auditoria_release_v0_8_0.md`.
- Commit ratificado: `c5d1b1d`, con la constancia `docs/sdd/PROTOCOLO_OPERATIVO.md §5:137`.
- Claves autorizadas: `docs/sdd/firmantes_autorizados`.
- Firma: commit firmado por el propietario que incorpora este acta.
