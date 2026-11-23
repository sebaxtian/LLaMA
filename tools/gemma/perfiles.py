"""Resolución de opciones efectivas y huella de perfiles de SPEC-017.

Implementa `RF-014` y `CB-006` conforme a `C-3`, `C-4` y `C-7` del plan, con las
decisiones `DEC-008` (primacía del valor inicial), `DEC-012` (funciones puras,
sin GPU ni artefactos reales) y `DEC-020` (la huella se calcula sobre las
`opciones` declaradas del manifiesto, nunca sobre las efectivas).

Contrato:

- ``huella_opciones(opciones)`` devuelve el ``SHA-256`` hexadecimal de la
  serialización canónica con claves ordenadas y sin espacios (`C-4`).
- ``resolver_opciones(manifiesto, registros)`` devuelve las claves ``opciones``
  y ``omitidas``: por cada eje rige el valor inicial de `C-2` salvo que su
  desviación declare ``comparacion`` con 1 identificador presente en
  ``registros`` y ese registro declare completo el bloque de 10 claves de `C-7`;
  en ese caso rige ``valor_propuesto`` (`C-3`).
- ``estado_por_huella(manifiesto, registros)`` devuelve ``(candidato, "opciones
  modificadas")`` cuando el estado declarado es ``medido`` o ``aprobado`` y 1
  registro declara 1 ``huella_opciones`` distinta de la de las opciones
  declaradas; si coincide, o el estado declarado es ``candidato``, devuelve el
  estado con motivo ``None`` (`C-4`). Las demás condiciones de `aprobado`
  corresponden a ``tools/gemma/estado.py``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RUTA_PARAMETROS_INICIALES = (
    RAIZ / "src" / "gemma" / "perfiles" / "parametros_iniciales.json"
)

# Las 10 claves del bloque de comparación de `C-7`: el bloque es completo solo si
# las declara todas; `alternativa_contexto` es adicional y no altera el recuento.
CAMPOS_COMPARACION = (
    "parametro",
    "medicion_inicial",
    "medicion_propuesta",
    "valor_inicial",
    "valor_propuesto",
    "delta_velocidad_generacion_tokens_por_segundo",
    "delta_velocidad_prompt_tokens_por_segundo",
    "delta_vram_asignada_mib",
    "delta_vram_libre_mib",
    "delta_ram_mib",
)

ESTADOS = ("candidato", "medido", "aprobado")
MOTIVO_OPCIONES_MODIFICADAS = "opciones modificadas"


def _requerido(contenedor, clave, contexto):
    """Devuelve ``contenedor[clave]`` o falla nombrando la clave ausente."""
    if not isinstance(contenedor, dict) or clave not in contenedor:
        raise ValueError(f"{contexto}: falta la clave obligatoria «{clave}»")
    return contenedor[clave]


def opciones_iniciales():
    """Valores iniciales de los 7 ejes de `C-2` declarados en el proyecto."""
    try:
        datos = json.loads(RUTA_PARAMETROS_INICIALES.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError(
            f"{RUTA_PARAMETROS_INICIALES}: no se pudo leer los parámetros "
            f"iniciales: {error}"
        ) from error
    if not isinstance(datos, dict) or not datos:
        raise ValueError(
            f"{RUTA_PARAMETROS_INICIALES}: los parámetros iniciales no declaran ejes"
        )
    iniciales = {}
    for eje, entrada in datos.items():
        if not isinstance(entrada, dict) or "valor" not in entrada:
            raise ValueError(f"parámetro inicial «{eje}»: falta la clave «valor»")
        iniciales[eje] = entrada["valor"]
    return iniciales


def huella_opciones(opciones):
    """Huella `SHA-256` canónica de `C-4`, sobre las opciones declaradas (`DEC-020`)."""
    if not isinstance(opciones, dict):
        raise ValueError("opciones: se esperaba 1 objeto con las opciones declaradas")
    serializacion = json.dumps(
        opciones, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(serializacion.encode("utf-8")).hexdigest()


def _comparacion_completa(desviacion, registros):
    """Indica si la desviación aplica su valor propuesto conforme a `C-3` y `C-7`."""
    identificador = desviacion.get("comparacion")
    if identificador is None:
        return False
    if not isinstance(registros, dict):
        raise ValueError("registros: se esperaba 1 mapa identificador → registro")
    registro = registros.get(identificador)
    if not isinstance(registro, dict):
        return False
    bloque = registro.get("comparacion")
    if not isinstance(bloque, dict):
        return False
    return all(clave in bloque for clave in CAMPOS_COMPARACION)


def resolver_opciones(manifiesto, registros):
    """Opciones efectivas de `C-3` y los ejes cuya desviación se omitió."""
    declaradas = _requerido(manifiesto, "opciones", "manifiesto")
    if not isinstance(declaradas, dict):
        raise ValueError("manifiesto: la clave «opciones» debe declarar 1 objeto")
    desviaciones = manifiesto.get("desviaciones") or []
    if not isinstance(desviaciones, list):
        raise ValueError("manifiesto: la clave «desviaciones» debe declarar 1 lista")

    opciones = opciones_iniciales()
    omitidas = []
    for desviacion in desviaciones:
        parametro = _requerido(desviacion, "parametro", "desviación")
        contexto = f"desviación «{parametro}»"
        _requerido(desviacion, "valor_inicial", contexto)
        propuesto = _requerido(desviacion, "valor_propuesto", contexto)
        if _comparacion_completa(desviacion, registros):
            opciones[parametro] = propuesto
        else:
            omitidas.append(parametro)

    return {"opciones": opciones, "omitidas": sorted(omitidas)}


def estado_por_huella(manifiesto, registros):
    """Estado conservado o degradado por la huella de `C-4` (`CB-006`)."""
    opciones = _requerido(manifiesto, "opciones", "manifiesto")
    estado = _requerido(manifiesto, "estado", "manifiesto")
    if estado not in ESTADOS:
        raise ValueError(
            f"manifiesto: el estado «{estado}» no está entre {', '.join(ESTADOS)}"
        )
    if estado == "candidato":
        return ("candidato", None)
    if not isinstance(registros, dict):
        raise ValueError("registros: se esperaba 1 mapa identificador → registro")

    huella = huella_opciones(opciones)
    for identificador, registro in registros.items():
        huella_registro = _requerido(
            registro, "huella_opciones", f"registro «{identificador}»"
        )
        if huella_registro != huella:
            return ("candidato", MOTIVO_OPCIONES_MODIFICADAS)
    return (estado, None)
