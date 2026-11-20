# Acta de interpretación normativa

*Acto del propietario. Fija la interpretación de la regla de autorreferencia del §16 del protocolo, a efectos del cierre de `AUD-111`.*

## 1. Fecha y autoridad

- Fecha: 2026-11-21 (UTC).
- Autoridad: `Agent Sebaxtian`, propietario del régimen.
- Clave de firma: la declarada en `docs/sdd/firmantes_autorizados`.
- Carácter: interpretación normativa, no aprobación de compuerta.

## 2. Cuestión

La auditoría previa al release v0.7.2 emitió `H-01`, registrado como `AUD-111`, con la regla `docs/sdd/PROTOCOLO_OPERATIVO.md §16:378`. Sostiene que `RF-015` y `CA-016` de `SPEC-016` son autorreferentes porque condicionan la publicación a un resultado de auditoría.

## 3. Interpretación

La prohibición del §16 alcanza a dos conductas: declarar por anticipado el veredicto de una auditoría no realizada, y fijar por anticipado el recuento de hallazgos o el conjunto de dimensiones que esa auditoría emitirá.

La prohibición no alcanza a condicionar la publicación a la verificación de un estado en el momento de publicar. Una condición de estado se comprueba sobre el inventario existente y no predice el contenido de un informe futuro. `RF-015` y `CA-016` exigen que el inventario no tenga hallazgos abiertos al publicar; no declaran el veredicto ni el recuento que emitirá la auditoría siguiente.

En consecuencia, `AUD-111` no acredita una infracción del §16 y se cierra por ratificación de esta interpretación.

## 4. Alcance y límites

- La interpretación se aplica solo a las condiciones de publicación basadas en el estado del inventario.
- No autoriza a una spec a declarar el veredicto, el recuento de hallazgos ni las dimensiones de una auditoría futura.
- No modifica el texto de `RF-015`, `CA-016` ni del §16; fija su lectura.
- No alcanza contratos ni consumidores externos al repositorio.

## 5. Registro

- Hallazgo cerrado: `AUD-111`, con el estado `cerrado por ratificación` en `docs/sdd/inventario_hallazgos.md`.
- Informe de origen: `docs/sdd/auditoria_previa_v0_7_2.md`.
- Claves autorizadas: `docs/sdd/firmantes_autorizados`.
- Firma: commit firmado por el propietario que incorpora este acta.
