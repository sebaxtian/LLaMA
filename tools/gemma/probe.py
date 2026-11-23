"""Sonda de contexto sostenido de SPEC-017.

Implementa `RF-009`, `CB-003` y `CA-008` conforme a `DEC-011`: 1 sola solicitud
``POST /completion`` en flujo, con ``stream`` verdadero y 1 prompt fijo, cuenta
los fragmentos con contenido y lee el bloque ``timings`` del último fragmento
para obtener los tokens generados y la velocidad. La estabilidad se comprueba
con ``GET /health`` al cierre y la detención del servidor se clasifica como
prueba fallida con el número de tokens contados hasta el corte, de modo que el
perfil no se promueve. El acotado de `DEC-022` eleva a ``2400`` 1
``tokens_objetivo`` menor y continúa sin ``ValueError``; 1 valor mayor o igual se
usa tal cual.

Contrato:

- ``sondear(base_url, *, cliente=None, tokens_objetivo=2400) -> dict`` devuelve
  ``estado`` en ``superada`` o ``fallida``, ``fragmentos`` con el número de
  fragmentos de contenido no vacío, ``tokens_generados`` desde
  ``timings.predicted_n`` o por conteo de fragmentos, ``tokens_por_segundo``
  desde ``timings.predicted_per_second`` o ``None``,
  ``velocidad_prompt_tokens_por_segundo`` desde ``timings.prompt_per_second`` o
  ``None``, y ``servidor`` en ``continúa en servicio`` o ``se detuvo``. En
  ``fallida`` añade ``motivo`` de texto no vacío.
- ``cliente`` inyectable con ``post_flujo(ruta, cuerpo) -> iterable de líneas``
  y ``get(ruta) -> (codigo_http, texto)``; con ``None`` se construye
  ``ClienteHTTP``, que usa ``urllib.request`` de la biblioteca estándar.
- ``tokens_objetivo`` que no sea 1 entero lanza ``ValueError`` con la clave.

Alcance: la sonda no escribe registro ni archivo alguno, no toca ``results/`` y
no lee ``bin/``, ``models/``, ``llama.cpp/`` ni ``.env``; la carpeta de registros
la escribe la campaña del operador local, conforme a `DEC-012`. La ruta y el
flujo llegan por parámetro y ningún caso de la suite abre 1 socket, porque
siempre inyecta el doble.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

__all__ = ["ClienteHTTP", "sondear"]

# `DEC-011` y `DEC-022`: la solicitud nunca baja de este umbral de tokens.
MINIMO_TOKENS = 2400

# Prompt fijo de `DEC-011`: 2 ejecuciones miden lo mismo sobre la misma carga.
PROMPT_FIJO = "Explica el paso de mensajes en Python"

# Rutas de `DEC-011`: la nativa es la primaria y la salud cierra la sonda.
RUTA_COMPLETION = "/completion"
RUTA_SALUD = "/health"

# Plazos del cliente real, en segundos. La generación de `2400` tokens tarda
# decenas de segundos en la máquina objetivo y la salud responde en milisegundos.
TIEMPO_LIMITE_GENERACION_SEGUNDOS = 600
TIEMPO_LIMITE_SALUD_SEGUNDOS = 30

ESTADO_SUPERADA = "superada"
ESTADO_FALLIDA = "fallida"
SERVIDOR_EN_SERVICIO = "continúa en servicio"
SERVIDOR_DETENIDO = "se detuvo"

PREFIJO_SSE = "data:"
MARCA_CIERRE = "[DONE]"


class ClienteHTTP:
    """Cliente real de la sonda sobre `urllib.request` de la biblioteca estándar.

    ``post_flujo`` abre 1 solicitud en flujo y emite las líneas recibidas;
    ``get`` devuelve la tupla ``(codigo_http, texto)``. La detención del
    servidor o la caída a mitad del flujo se propaga como ``ConnectionError``
    con la URL y el motivo, de modo que ninguna excepción de ``urllib`` se
    propague sin contexto.
    """

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def url(self, ruta):
        """URL absoluta de 1 ruta del servidor, sin duplicar la barra."""
        return self.base_url + (ruta if ruta.startswith("/") else "/" + ruta)

    def post_flujo(self, ruta, cuerpo):
        """Abre la solicitud en flujo y devuelve el iterable de líneas SSE."""
        destino = self.url(ruta)
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        solicitud = urllib.request.Request(
            destino,
            data=datos,
            headers={
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            },
            method="POST",
        )
        try:
            respuesta = urllib.request.urlopen(
                solicitud, timeout=TIEMPO_LIMITE_GENERACION_SEGUNDOS
            )
        except (urllib.error.URLError, OSError) as error:
            raise ConnectionError(
                f"no se pudo abrir el flujo en {destino}: {error}"
            ) from error
        return self._lineas(respuesta, destino)

    def get(self, ruta):
        """Devuelve el código y el texto de 1 consulta simple al servidor."""
        destino = self.url(ruta)
        solicitud = urllib.request.Request(destino, method="GET")
        try:
            with urllib.request.urlopen(
                solicitud, timeout=TIEMPO_LIMITE_SALUD_SEGUNDOS
            ) as respuesta:
                return respuesta.status, respuesta.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as error:
            # 1 código distinto de 200 sigue siendo 1 respuesta del servidor: se
            # devuelve para que la sonda lo clasifique y no se confunda con 1
            # detención.
            return error.code, error.read().decode("utf-8", "replace")
        except (urllib.error.URLError, OSError) as error:
            raise ConnectionError(
                f"el servidor no responde en {destino}: {error}"
            ) from error

    def _lineas(self, respuesta, destino):
        """Emite las líneas del flujo y cierra la respuesta al terminar."""
        try:
            for cruda in respuesta:
                yield cruda.decode("utf-8", "replace").rstrip("\r\n")
        except (ConnectionError, OSError) as error:
            raise ConnectionError(
                f"el flujo se interrumpió en {destino}: {error}"
            ) from error
        finally:
            respuesta.close()


def sondear(base_url, *, cliente=None, tokens_objetivo=2400):
    """Ejecuta la sonda de contexto sostenido y clasifica su resultado.

    ``base_url`` es el punto de acceso del servidor y ``cliente`` permite
    inyectar el doble de la suite; con ``None`` se construye ``ClienteHTTP``.
    ``tokens_objetivo`` se acota a ``MINIMO_TOKENS`` conforme a `DEC-022`.
    """
    url = _validar_url(base_url)
    activo = _validar_cliente(cliente, url)
    cuerpo = {
        "prompt": PROMPT_FIJO,
        "n_predict": _acotar_tokens(tokens_objetivo),
        "stream": True,
    }

    fragmentos, timings, cierre, interrupcion = _consumir_flujo(
        activo, url, cuerpo
    )

    causas = []
    if interrupcion is not None:
        causas.append(
            f"transcripción cortada por la detención del servidor en "
            f"{url}{RUTA_COMPLETION}: {interrupcion}"
        )
    elif not cierre:
        causas.append(
            f"transcripción cortada antes de {MARCA_CIERRE} en "
            f"{url}{RUTA_COMPLETION}: {fragmentos} fragmentos contados"
        )

    if timings is None:
        causas.append(
            f"timings ausente en la respuesta de {url}{RUTA_COMPLETION}: "
            "0 bloque de medición que leer"
        )

    tokens_generados = _tokens_generados(timings, fragmentos)
    tokens_por_segundo = _tokens_por_segundo(timings)
    velocidad_prompt_tokens_por_segundo = _velocidad_de_prompt(timings)

    servidor, causa_servidor = _comprobar_salud(activo, url)
    if causa_servidor is not None:
        causas.append(causa_servidor)

    resultado = {
        "estado": ESTADO_FALLIDA if causas else ESTADO_SUPERADA,
        "fragmentos": fragmentos,
        "tokens_generados": tokens_generados,
        "tokens_por_segundo": tokens_por_segundo,
        "velocidad_prompt_tokens_por_segundo": velocidad_prompt_tokens_por_segundo,
        "servidor": servidor,
    }
    if causas:
        resultado["motivo"] = "; ".join(causas)
    return resultado


def _validar_url(base_url):
    """Valida el punto de acceso y lo normaliza sin la barra final."""
    if not isinstance(base_url, str) or not base_url.strip():
        raise ValueError(
            f"base_url: se esperaba 1 URL no vacía y se recibió {base_url!r}"
        )
    url = base_url.strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError(
            f"base_url: la URL {url!r} no declara el esquema http:// o https://"
        )
    return url.rstrip("/")


def _validar_cliente(cliente, url):
    """Devuelve el cliente inyectado o construye el real sobre ``url``."""
    if cliente is None:
        return ClienteHTTP(url)
    for metodo in ("post_flujo", "get"):
        if not callable(getattr(cliente, metodo, None)):
            raise ValueError(
                f"cliente: falta el método {metodo} del cliente de la sonda "
                f"sobre {url}"
            )
    return cliente


def _acotar_tokens(tokens_objetivo):
    """Acota ``tokens_objetivo`` al mínimo de `DEC-022` sin rechazar la llamada."""
    if isinstance(tokens_objetivo, bool) or not isinstance(tokens_objetivo, int):
        raise ValueError(
            "tokens_objetivo: se esperaba 1 entero y se recibió "
            f"{tokens_objetivo!r}"
        )
    return max(MINIMO_TOKENS, tokens_objetivo)


def _consumir_flujo(activo, url, cuerpo):
    """Recorre 1 sola vez el flujo y devuelve conteo, timings, cierre y corte."""
    fragmentos = 0
    timings = None
    cierre = False
    interrupcion = None
    try:
        for linea in activo.post_flujo(RUTA_COMPLETION, cuerpo):
            carga, es_cierre = _analizar_linea(linea)
            if es_cierre:
                cierre = True
                continue
            if carga is None:
                continue
            bloque = carga.get("timings")
            if isinstance(bloque, dict):
                timings = bloque
            contenido = carga.get("content")
            if isinstance(contenido, str) and contenido:
                fragmentos += 1
    except (ConnectionError, OSError) as error:
        interrupcion = error
    return fragmentos, timings, cierre, interrupcion


def _analizar_linea(linea):
    """Devuelve ``(carga, cierre)`` de 1 línea SSE, o ``(None, False)``."""
    if not isinstance(linea, str):
        return None, False
    texto = linea.strip()
    if not texto:
        return None, False
    if texto.startswith(PREFIJO_SSE):
        texto = texto[len(PREFIJO_SSE):].strip()
    if texto == MARCA_CIERRE:
        return None, True
    try:
        carga = json.loads(texto)
    except json.JSONDecodeError:
        return None, False
    if not isinstance(carga, dict):
        return None, False
    return carga, False


def _tokens_generados(timings, fragmentos):
    """Toma ``predicted_n`` cuando existe y cae al conteo de fragmentos."""
    if timings is not None:
        predicted_n = timings.get("predicted_n")
        if (
            isinstance(predicted_n, int)
            and not isinstance(predicted_n, bool)
            and predicted_n >= 0
        ):
            return predicted_n
    return fragmentos


def _tokens_por_segundo(timings):
    """Lee ``predicted_per_second`` y devuelve ``None`` si no aparece."""
    return _velocidad(timings, "predicted_per_second")


def _velocidad_de_prompt(timings):
    """Lee ``prompt_per_second`` y devuelve ``None`` si no aparece.

    Es la fila 16 de `C-6`. Sin la clave no se estima ni se deriva de otra
    cifra: queda ``None``, igual que ``tokens_por_segundo``.
    """
    return _velocidad(timings, "prompt_per_second")


def _velocidad(timings, clave):
    """Devuelve ``timings[clave]`` como ``float``, o ``None`` sin la clave."""
    if timings is None:
        return None
    valor = timings.get(clave)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    return float(valor)


def _comprobar_salud(activo, url):
    """Cierra la sonda con ``GET /health`` y devuelve estado y causa."""
    try:
        codigo, _texto = activo.get(RUTA_SALUD)
    except (ConnectionError, OSError) as error:
        return (
            SERVIDOR_DETENIDO,
            f"el servidor se detuvo: {url}{RUTA_SALUD} no responde ({error})",
        )
    if codigo != 200:
        return (
            SERVIDOR_EN_SERVICIO,
            f"la comprobación de salud {url}{RUTA_SALUD} respondió {codigo} "
            "y no 200",
        )
    return SERVIDOR_EN_SERVICIO, None
