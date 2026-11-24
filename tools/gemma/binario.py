"""Lectura de la versión y de las opciones del binario de SPEC-017.

Implementa la comprobación de `DEC-010` para `RF-013` y `CB-002` sin lanzar el
servidor ni cargar el modelo: interroga al propio binario con `--version` y con
`--help` antes de la primera prueba medida. La fuente de las opciones aceptadas
es la ayuda que la versión en uso enumera y no 1 lista mantenida a mano, de modo
que la comprobación no envejece con cada actualización del binario.

Contrato:

- ``leer_version(ejecutable)`` devuelve 1 diccionario con exactamente las claves
  ``version`` y ``commit``, leídas de la línea de versión de ``--version``. Si la
  salida no declara alguna de las 2, lanza ``ValueError`` con 1 mensaje que
  nombra lo ausente.
- ``opciones_aceptadas(ejecutable)`` devuelve 1 mapa ``eje de C-2 → forma larga
  que la ayuda enumera para el eje``; el eje cuya opción no aparece en la ayuda
  no figura en el mapa.
- ``verificar_compatibilidad(opciones, aceptadas)`` devuelve la lista ordenada
  de los ejes declarados en ``opciones`` que no figuran en ``aceptadas``.

Alcance: el código ``3`` de `C-8` no lo emite este módulo, porque aquí no hay
perfil ni ejecución que abortar; lo produce la comprobación 3 de `precheck` en
`T-015`. Este módulo solo informa qué ejes no aparecen enumerados por la ayuda.

Ejecución: las 2 consultas usan 1 tiempo límite y no interpretan el código de
salida del binario, que `llama-server` emite con valor distinto de `0` en algunas
versiones incluso al imprimir la ayuda. El ejecutable ausente, el que no responde
y el que no puede iniciarse se envuelven en ``ValueError`` con la ruta y el
motivo, de modo que no se propaga 1 ``CalledProcessError`` ni 1 ``OSError`` sin
contexto. El módulo no resuelve rutas de ``bin/`` ni de ``models/``: las recibe
por parámetro, conforme a `DEC-012`.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

__all__ = ["leer_version", "opciones_aceptadas", "verificar_compatibilidad"]

# Tiempo límite de cada consulta, en segundos: las 2 salidas se imprimen y
# terminan en milisegundos, y 1 binario que no responde en este plazo se reporta
# como error de lectura en lugar de bloquear la comprobación de `RNF-001`.
TIEMPO_LIMITE_SEGUNDOS = 5

# Los 9 ejes de `C-2` —los 7 iniciales más los 2 tipos de caché KV de
# `DEC-028`—, con el identificador que el perfil declara.
EJES = (
    "cache_type_k",
    "cache_type_v",
    "ctx_size",
    "flash_attn",
    "gpu_layers",
    "load_mode",
    "ncmoe",
    "parallel",
    "ubatch",
)

# Grafías alternativas de cada eje: la forma larga que no se deriva del
# identificador —`ubatch` se escribe `--ubatch-size`, `ncmoe` se escribe
# `--n-cpu-moe`, `cache_type_k` se escribe `--cache-type-k` y `cache_type_v` se
# escribe `--cache-type-v`— y las formas cortas conocidas de la ayuda del
# binario. El identificador del eje y la opción son grafías distintas, así que
# esta correspondencia es dato del contrato y no 1 lista de opciones aceptadas:
# la ayuda sigue decidiendo si el eje existe.
ALTERNATIVAS_DEL_EJE = {
    "cache_type_k": ("cache-type-k", "ctk"),
    "cache_type_v": ("cache-type-v", "ctv"),
    "ctx_size": ("c",),
    "flash_attn": ("fa",),
    "gpu_layers": ("n-gpu-layers", "ngl"),
    "load_mode": ("lm",),
    "ncmoe": ("n-cpu-moe", "ncmoe"),
    "parallel": ("np",),
    "ubatch": ("ubatch-size", "ub"),
}

# Línea de versión: `version: <versión> (build <número>, commit <commit>)` en las
# compilaciones recientes y `version: <número> (<commit>)` en las anteriores.
PATRON_VERSION = re.compile(r"\bversion[:\s]+([^\s()]+)", re.IGNORECASE)

# Formas de la línea de versión que portan el commit: la etiqueta `commit` y el
# identificador entre paréntesis cuando la línea no la declara.
PATRONES_COMMIT = (
    re.compile(r"commit[:\s]+([0-9A-Fa-f]{6,40})", re.IGNORECASE),
    re.compile(r"\(([0-9A-Fa-f]{6,40})\)"),
)

# Opciones de la ayuda: 1 o 2 guiones y 1 nombre. El límite izquierdo excluye
# las líneas de guiones que separan las secciones de la ayuda.
PATRON_OPCION = re.compile(r"(?<![\w-])(--?[A-Za-z][A-Za-z0-9-]*)")


def _texto(datos):
    """Decodifica la salida capturada del binario, que llega en bytes."""
    if not datos:
        return ""
    return datos.decode("utf-8", errors="replace")


def _ejecutar(ejecutable, argumento):
    """Ejecuta `<ejecutable> <argumento>` y devuelve su salida estándar y de error.

    El código de salida no se interpreta: `--help` y `--version` imprimen y
    terminan, y el texto es lo único que el contrato lee. La ausencia del
    ejecutable, el plazo agotado y el fallo de inicio se informan como
    ``ValueError`` con la ruta, de modo que el llamador nunca recibe 1 excepción
    del módulo `subprocess` sin contexto.
    """
    ruta = Path(ejecutable)
    if not ruta.is_file():
        raise ValueError(f"{ruta}: el ejecutable no existe o no es 1 archivo")
    try:
        proceso = subprocess.run(
            [str(ruta), argumento],
            capture_output=True,
            check=False,
            timeout=TIEMPO_LIMITE_SEGUNDOS,
        )
    except subprocess.TimeoutExpired as error:
        raise ValueError(
            f"{ruta}: {argumento} no respondió en {TIEMPO_LIMITE_SEGUNDOS} s"
        ) from error
    except OSError as error:
        raise ValueError(f"{ruta}: no se pudo ejecutar {argumento}: {error}") from error
    return _texto(proceso.stdout) + "\n" + _texto(proceso.stderr)


def _commit(texto):
    """Devuelve el commit de la línea de versión, o `None` si no la declara."""
    for patron in PATRONES_COMMIT:
        coincidencia = patron.search(texto)
        if coincidencia is not None:
            return coincidencia.group(1)
    return None


def _grafias(eje):
    """Formas con que la ayuda puede escribir el eje; la forma larga va primero."""
    return (eje.replace("_", "-"),) + ALTERNATIVAS_DEL_EJE[eje]


def leer_version(ejecutable):
    """Lee la versión y el commit de la salida de `--version` del binario.

    Devuelve 1 diccionario con exactamente las claves ``version`` y ``commit``.
    Lanza ``ValueError`` con la ruta y lo ausente cuando la salida no declara la
    versión o no declara el commit.
    """
    salida = _ejecutar(ejecutable, "--version")
    for linea in salida.splitlines():
        coincidencia = PATRON_VERSION.search(linea)
        if coincidencia is None:
            continue
        commit = _commit(linea)
        if commit is None:
            commit = _commit(salida)
        if commit is None:
            raise ValueError(
                f"{Path(ejecutable)}: la salida de --version no declara el "
                f"commit: {linea.strip()!r}"
            )
        return {"version": coincidencia.group(1), "commit": commit}
    raise ValueError(
        f"{Path(ejecutable)}: la salida de --version no declara la versión: "
        f"{salida.strip()!r}"
    )


def opciones_aceptadas(ejecutable):
    """Deriva de `--help` el mapa de cada eje de `C-2` a su forma larga.

    La presencia de la forma en la ayuda decide si el eje entra en el mapa y cuál
    de sus grafías se conserva: se prefiere la forma larga que la ayuda enumera y
    la forma corta solo acredita que la opción existe. El eje que la ayuda no
    enumera no figura en el mapa.
    """
    enumeradas = set(PATRON_OPCION.findall(_ejecutar(ejecutable, "--help")))
    aceptadas = {}
    for eje in EJES:
        grafias = _grafias(eje)
        for grafia in grafias:
            if f"--{grafia}" in enumeradas:
                aceptadas[eje] = f"--{grafia}"
                break
        else:
            if any(f"-{grafia}" in enumeradas for grafia in grafias):
                aceptadas[eje] = f"--{grafias[0]}"
    return aceptadas


def verificar_compatibilidad(opciones, aceptadas):
    """Devuelve los ejes de ``opciones`` que la ayuda no enumera.

    La lista va ordenada alfabéticamente y nombra solo ejes declarados por el
    perfil, de modo que 1 opción extra del binario no produce rechazo. El código
    de salida lo emite `precheck` a partir de esta lista.
    """
    return sorted(eje for eje in opciones if eje not in aceptadas)
