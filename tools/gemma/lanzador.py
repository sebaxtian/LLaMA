"""Orquestador de ejecución de SPEC-017.

Implementa la línea de comandos de `C-8` y los modos `comprobar`, `servir`,
`medir` y `comparar` de `DEC-001`, `DEC-003` y `DEC-008` sobre los manifiestos de
perfil de `C-1` en ``src/gemma/perfiles/``.

Modos:

- ``comprobar`` ejecuta las 5 comprobaciones de `C-9`, imprime su salida y
  devuelve el código de `C-8` del resultado sin reinterpretarlo, sin lanzar el
  servidor. La comprobación 4 contrasta el presupuesto medido del perfil con la
  VRAM libre en MiB que informa la consulta de solo lectura
  ``medir.vram_libre_mib`` por el punto inyectable ``VRAM_LIBRE_MIB``; sin esa
  consulta disponible la comprobación se reporta `PENDIENTE` con su motivo y
  ningún valor se estima, y mientras el bloque ``presupuesto_vram`` conserve su
  clave ``pendiente`` se rige por `DEC-018`. El consumo se calcula con el
  `ctx_size` de las opciones efectivas de `C-3`, que el modo resuelve con los
  registros disponibles, y no con el declarado.
- ``servir`` ejecuta la comprobación previa completa, resuelve las opciones
  efectivas de `C-3` con ``perfiles.resolver_opciones`` sobre los registros
  disponibles en ``results/gemma/<perfil>/``, lanza el ejecutable de
  ``artefactos`` con esas opciones, espera ``GET /health`` con la respuesta
  ``ok`` contando el tiempo de carga en segundos, mide la memoria con
  ``medir.medir_memoria`` sobre el árbol del proceso, cierra el servidor y no
  escribe registro alguno.
- ``medir`` hace lo anterior, ejecuta la sonda de `DEC-011` cuando la prueba la
  requiere y deja 1 registro propio de `C-5` con las 22 filas de `C-6` en
  ``results/gemma/<perfil>/`` bajo la raíz recibida; el código de `C-8` es `0`.
  Con la sonda ejecutada imprime, antes de la línea del registro, 1 línea
  ``SONDA: <tokens_generados> tokens en <segundos> s, <tokens_por_segundo>
  tokens/s`` con el conteo del resultado y el tiempo medido alrededor de la
  sonda, o ``SONDA: <tokens> tokens contados antes del corte`` con su motivo
  cuando la sonda se declara `fallida`, de modo que `T-037` transcribe los 2000
  tokens de `CB-003`; la línea no altera el registro ni el código de salida.
- ``comparar`` exige ``--parametro`` y resuelve las opciones efectivas de `C-3`
  con los registros de comparación del perfil. Si la desviación del eje declara
  el bloque completo de `C-7`, usa ese bloque y la elegibilidad de
  ``estado.elegible_para_aprobado`` sin recalcular cifras; si no lo declara,
  ejecuta la campaña de ``EJECUTAR_COMPARACION``, que mide el valor inicial y el
  valor propuesto con su arranque, espera de ``/health``, medición de memoria,
  sonda y registro de propósito ``comparacion``, calcula el bloque de `C-7` con
  ``comparar.comparar`` desde las 2 lecturas y lo escribe en la clave
  ``comparacion`` del registro propuesto. El modo imprime el bloque de las 5
  diferencias y la elegibilidad, y no altera las opciones efectivas de las
  ejecuciones de servicio.

Presupuesto de VRAM: en los modos con carga, la comprobación 4 contrasta el
presupuesto del perfil con la VRAM libre menos el margen de `RNF-007` y toma su
`ctx_size` de las opciones efectivas de `C-3` que el modo ya resolvió, de modo
que el techo corresponde al contexto que el servidor arranca y no al declarado;
mientras el bloque conserve su clave ``pendiente`` el presupuesto no se estima,
el cierre declara `4 de 5 comprobaciones superadas, 1 pendiente`, el campo 21 del
registro lo declara ``no disponible`` y el código sigue siendo `0`.

Memoria de expertos en host: el campo 22 de `C-6` transcribe la primera línea
``CUDA_Host model buffer size = <n> MiB`` del modelo principal en la salida
capturada del servidor, que ``_ServidorProceso.leer_salida`` devuelve antes de
cerrar el proceso; la memoria del borrador no se suma ni se estima, y sin esa
línea el campo declara ``no disponible``, conforme a `DEC-026`.

Puntos inyectables de la suite, como atributos de módulo y sin opciones de
línea de comandos fuera de `C-8`: ``MEDIR_MEMORIA`` (medición de memoria),
``VRAM_LIBRE_MIB`` (VRAM libre de solo lectura para la comprobación 4),
``SONDEAR`` (sonda de contexto), ``LANZAR_SERVIDOR`` (ejecución del binario),
``EJECUTAR_COMPARACION`` (las 2 mediciones reales de la campaña de comparación)
y las constantes ``URL_BASE`` y ``PUERTO`` del punto de acceso. El servidor
lanzado expone ``pid``, ``activo()``, ``leer_salida()`` y ``cerrar()``; la
medición recibe la lista de PID del árbol y la sonda la URL base. Las pruebas
sustituyen además ``binario.opciones_aceptadas``, ``binario.leer_version`` y
``gguf.leer_metadatos``, de modo que ningún caso invoca ``nvidia-smi``,
``powershell.exe``, la GPU ni el binario real, conforme a `DEC-012`.

Decodificación especulativa: el bloque ``especulativa`` de cada manifiesto
declara el modo y su techo conforme a `DEC-024`, de modo que la línea del
servidor añade ``--spec-type draft-mtp --spec-draft-n-max <techo>`` después de
``--model-draft`` cuando el tipo es ``draft-mtp`` y el artefacto está declarado,
y el campo 11 del registro de `C-6` transcribe ese bloque y no la presencia del
artefacto.

Selector de escenarios de `SPEC-018`: ``--listar-escenarios`` enumera los 9
escenarios del catálogo canónico de ``src/gemma/escenarios/catalogo.json`` en el
orden jerárquico de `DEC-004`, con 1 línea por escenario que declara los 5 datos
de `RF-005`, y devuelve el código `0` sin lanzar el servidor. ``--escenario
<id>`` selecciona 1 escenario del catálogo por su identificador exacto: la
ejecución aplica los 9 valores del escenario —los 7 parámetros de
``parametros_ejecucion``, las capas de expertos en CPU y el contexto efectivo—,
declara el identificador en consola y lo transcribe en el bloque ``escenario``
del registro, junto al presupuesto declarado del escenario y las 2 mediciones de
VRAM. Un identificador ausente del catálogo devuelve el código `2` y enumera los
9 identificadores canónicos (`RF-004`); el precheck de recursos de `C-4` se
invoca por el punto ``VERIFICAR_RECURSOS_ESCENARIO`` y su aborto devuelve el
código `3` sin arrancar el servidor (`CB-007`, `RF-007`, `CB-001`, `CB-008`,
`CB-003`). El contexto de 1 escenario ajustado se recalcula con la VRAM libre
medida en el momento del lanzamiento mediante la regla de `RF-009` y `DEC-008`,
de modo que el lanzamiento no reutiliza el valor declarado (`CB-005`).

Selector interactivo de `SPEC-018`: sin `--perfil` ni `--escenario`, el flujo
presenta el menú de los 9 escenarios numerados del 1 al 9 en el orden de
`DEC-004`, con el identificador, las capas de expertos en CPU, el contexto
efectivo en tokens y el presupuesto de VRAM en MiB de `RF-005`, y marca
`[NO EJECUTABLE]` al escenario que `CB-007` no permite seleccionar. La consola se
lee por el punto inyectable ``LEER_ENTRADA``, cuyo valor por omisión es
``input``; 1 selección vacía informa el rechazo y devuelve el código `2` sin
precheck ni lanzamiento, y 1 selección inválida o 1 escenario no ejecutable
informan el rechazo, reimprimen la numeración y vuelven a preguntar. El número
del menú o el identificador canónico resuelven el escenario y, después, el flujo
resuelve el perfil de base —por número o por identificador de la lista de
`DEC-001`— antes de aplicar el flujo de `C-2` y `C-4` a la ejecución. Con la
entrada por omisión, el menú exige 1 terminal y 1 perfil de base único; con
varios perfiles disponibles y sin consola, la invocación sin `--perfil` conserva
el listado de `DEC-001` y devuelve el código `2`.

Contrato:

- ``main(argv=None) -> int`` devuelve el código de `C-8` y no termina por
  ``sys.exit``; el bloque ``if __name__ == "__main__"`` lo convierte en el
  código de proceso con ``raise SystemExit(main())``.
- Sin ``--perfil`` se imprimen los identificadores de perfil disponibles —los
  manifiestos ``*.json`` de ``src/gemma/perfiles/`` salvo
  ``parametros_iniciales.json``— en orden alfabético y se devuelve `2` sin
  lanzar el servidor, conforme a `DEC-001`.
- ``--raiz`` es absoluta y por defecto ``Path(__file__).resolve().parents[2]``,
  que es el directorio que contiene ``tools/``; ningún artefacto de la
  configuración se resuelve desde el directorio actual.
- 1 perfil inexistente o 1 directorio de perfiles sin manifiestos imprime
  ``[ERROR] perfil no declarado: <id>`` y devuelve `2`; 1 ``--modo`` fuera de
  los 4 de `C-8` imprime el mensaje de uso y devuelve `2`; ``--modo medir`` sin
  ``--prueba`` y ``--modo comparar`` sin ``--parametro`` devuelven `2`.
- La huella del registro es la de las ``opciones`` declaradas en el manifiesto
  y no la de las efectivas, conforme a `DEC-020`; la fila 16 de `C-6` declara la
  velocidad de prompt que el resultado de la sonda informa y, cuando no la
  informa, la marca ``no disponible`` sin estimar ningún valor.
- ``--modo comparar`` sin ``--prueba`` declara el nombre determinista
  ``comparacion-<eje>`` en los 2 registros de la campaña; con ``--prueba`` usa
  el nombre recibido.
- ``--modo comparar`` con 1 ``--parametro`` que no nombra 1 desviación del
  perfil imprime ``[ERROR] desviación no declarada: <clave>`` y devuelve `2`.

El módulo usa ``argparse``, ``json``, ``os``, ``re``, ``subprocess``, ``sys``,
``tempfile``, ``time``, ``urllib.error``, ``urllib.request``, ``datetime``,
``timedelta`` y ``pathlib`` de la biblioteca estándar, además de los módulos
locales `binario`, `comparar`, `estado`, `medir`, `perfiles`, `precheck`,
`probe` y `registro`, y no lee ``bin/``, ``models/``, ``llama.cpp/`` ni
``.env``: las rutas llegan desde el manifiesto y la raíz.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import binario
import comparar
import escenarios
import estado
import medir
import perfiles
import precheck
import probe
import registro

__all__ = ["main"]

# Raíz del repositorio derivada de la ubicación del módulo: ``tools/gemma/``
# está 2 niveles por debajo del directorio que contiene ``tools/``, de modo que
# la raíz por defecto no depende del directorio actual, conforme a `C-8`.
RAIZ_POR_DEFECTO = Path(__file__).resolve().parents[2]

# Directorio de manifiestos de perfil, relativo a la raíz (`C-1`, `DEC-002`).
DIRECTORIO_PERFILES = Path("src") / "gemma" / "perfiles"
SUFIJO_MANIFIESTO = ".json"

# `SPEC-018`, `C-1` y `DEC-001`: el catálogo canónico de escenarios cuelga de la
# raíz recibida, de modo que la suite lo copia a su árbol temporal.
RUTA_CATALOGO_ESCENARIOS = (
    Path("src") / "gemma" / "escenarios" / "catalogo.json"
)

# Manifiesto de los 9 ejes de `C-2`: no es 1 perfil, de modo que no se lista ni
# se selecciona con `--perfil`.
MANIFIESTO_INICIAL = "parametros_iniciales"

# `SPEC-018` y `C-2`: el selector interactivo lee la consola por este punto
# inyectable, cuyo valor por omisión es `input`; la suite lo sustituye por 1
# doble que entrega sus líneas sin consola real, conforme a `DEC-012`.
LEER_ENTRADA = input

# Encabezados literales de los 2 menús del flujo interactivo de `DEC-001` y la
# marca del escenario que `CB-007` no permite seleccionar.
ENCABEZADO_MENU_ESCENARIOS = "Escenarios disponibles (--escenario <id>):"
ENCABEZADO_MENU_PERFILES = "Perfiles disponibles (--perfil <id>):"
MARCA_NO_EJECUTABLE = "[NO EJECUTABLE]"

# Los 4 modos de `C-8` y ningún otro.
MODOS = ("comprobar", "servir", "medir", "comparar")
MODO_POR_DEFECTO = "comprobar"
MODO_SERVIR = "servir"
MODO_MEDIR = "medir"
MODO_COMPARAR = "comparar"

# Códigos de `C-8` que emite este módulo: ejecución completada, uso incorrecto
# y medición de memoria no disponible, que es también el código de 1 servidor
# que no llega a quedar en servicio y por tanto no se puede medir.
CODIGO_OK = 0
CODIGO_USO_INCORRECTO = 2
CODIGO_PRECHECK_ESCENARIO = 3
CODIGO_MEDICION_NO_DISPONIBLE = 7

# Punto de acceso del servidor (`DEC-011`): la URL base y el puerto son
# constantes de módulo para que la suite los sustituya sin opciones nuevas.
URL_BASE = "http://127.0.0.1"
PUERTO = 8080
RUTA_SALUD = probe.RUTA_SALUD
ESPERA_SALUD_SEGUNDOS = 600
TIEMPO_LIMITE_SALUD_SEGUNDOS = 30
INTERVALO_SONDEO_SALUD_SEGUNDOS = 0.05
CIERRE_SERVIDOR_SEGUNDOS = 30

# Carpeta de registros de `C-5`, relativa a la raíz recibida: la campaña real
# escribe en ``results/gemma/<perfil>/`` y la suite sobre su árbol temporal.
RUTA_REGISTROS = Path("results") / "gemma"

# `RNF-007`: la VRAM libre tras la carga debe ser de al menos 512 MiB, de modo
# que la comprobación 4 solo se declara superada si el presupuesto cabe además
# en ese margen.
MARGEN_VRAM_MIB = 512

# `C-6` y `DEC-024`: el modo de especulación y su techo viven en el bloque
# `especulativa` de cada manifiesto de perfil, de modo que el lanzador no fija
# ningún techo ni ningún tipo propio.
TIPO_ESPECULATIVA_DRAFT_MTP = "draft-mtp"
BANDERA_TIPO_ESPECULATIVA = "--spec-type"
BANDERA_TECHO_BORRADOR = "--spec-draft-n-max"

# `RF-006` y `T-065`: `--log-verbosity 4` es 1 bandera de registro y no 1 eje de
# `C-2`. Con ese nivel el binario imprime la línea
# `CUDA_Host model buffer size = <n> MiB` del modelo principal, que es la fuente
# del campo 22 de `C-6`; la bandera no entra en la resolución de `C-3` ni en la
# huella de `DEC-020`, que se calcula sobre las `opciones` declaradas.
BANDERA_VERBOSIDAD_REGISTRO = "--log-verbosity"
VERBOSIDAD_REGISTRO = 4

# `C-7`: la prueba que mide la alternativa de contexto menor de `T-041`, cuyo
# registro exige el bloque cuando el eje es `ctx_size` con `131072` tokens.
PRUEBA_ALTERNATIVA_CONTEXTO = "alternativa-contexto-menor"

# `RF-009`, `CB-003` y `DEC-011`: la prueba de contexto sostenido es la de
# `T-037` y requiere la sonda, además de la prueba de carga, que ya la disparaba;
# `T-080` añade la alternativa de contexto menor de `T-041`, cuyo registro exige
# las 2 velocidades del bloque de tiempos y que hasta entonces dejaba los campos
# 16 y 17 en `no disponible` por quedar fuera de esta tupla.
PRUEBAS_CON_SONDA = ("carga", "contexto-sostenido", PRUEBA_ALTERNATIVA_CONTEXTO)

# `C-5`: solo la prueba de carga declara el propósito `carga`; las demás
# mediciones, incluidas `contexto-sostenido` y `alternativa-contexto-menor`,
# conservan el propósito `medicion`.
PRUEBAS_DE_CARGA = ("carga",)

# `C-6`: la marca de la fuente ausente que admite toda fila.
NO_DISPONIBLE = registro.NO_DISPONIBLE

# `C-6`: la fila 16 toma la velocidad de prompt del bloque de tiempos de la
# respuesta del servidor; el resultado de la sonda la informa, cuando la
# informa, en esta clave y ningún valor se estima si falta.
CLAVE_VELOCIDAD_PROMPT = "velocidad_prompt_tokens_por_segundo"

# `C-5` y `C-7`: la campaña de comparación escribe sus 2 registros con el
# propósito `comparacion` y, sin `--prueba`, con el nombre `comparacion-<eje>`.
PROPOSITO_COMPARACION = "comparacion"
PREFIJO_PRUEBA_COMPARACION = "comparacion"

# `C-6`: forma larga que el lanzamiento declara para cada eje de `C-2`; el eje
# `load_mode` viaja como `--load-mode <valor>` porque el binario declara
# `-lm, --load-mode` con los valores `auto`, `none`, `mmap`, `mlock`,
# `mmap+mlock` y `dio`, y no enumera `--no-mmap`; los 2 tipos de caché KV de
# `DEC-028` viajan como `--cache-type-k` y `--cache-type-v` con su valor efectivo.
FORMA_DE_EJE = {
    "gpu_layers": "--n-gpu-layers",
    "flash_attn": "--flash-attn",
    "ctx_size": "--ctx-size",
    "ubatch": "--ubatch-size",
    "ncmoe": "--n-cpu-moe",
    "load_mode": "--load-mode",
    "parallel": "--parallel",
    "cache_type_k": "--cache-type-k",
    "cache_type_v": "--cache-type-v",
}

# `C-6` y `DEC-026`: el campo 22 «Memoria de expertos en host» toma la primera
# línea `CUDA_Host model buffer size = <n> MiB` del modelo principal en la
# salida del servidor; la del draft no se suma ni se estima ningún valor.
PATRON_MEMORIA_EXPERTOS = re.compile(
    r"CUDA_Host model buffer size\s*=\s*(\d+(?:\.\d+)?)\s*MiB"
)


def _crear_parser():
    """Compone el analizador de la línea de comandos de `C-8`."""
    parser = argparse.ArgumentParser(
        prog="lanzador.py",
        description="Orquestador de ejecución de los perfiles de SPEC-017.",
    )
    parser.add_argument(
        "--raiz",
        default=str(RAIZ_POR_DEFECTO),
        help="raíz del repositorio; por defecto, el directorio que contiene tools/",
    )
    parser.add_argument(
        "--perfil",
        default=None,
        help="identificador del perfil; sin él se listan los disponibles",
    )
    parser.add_argument(
        "--escenario",
        default=None,
        help="identificador del escenario del catálogo de SPEC-018",
    )
    parser.add_argument(
        "--listar-escenarios",
        action="store_true",
        help="enumera los 9 escenarios del catálogo y termina",
    )
    parser.add_argument(
        "--modo",
        default=MODO_POR_DEFECTO,
        help="modo de ejecución: " + "|".join(MODOS),
    )
    parser.add_argument("--prueba", default=None, help="nombre de la prueba")
    parser.add_argument(
        "--parametro",
        default=None,
        help="clave del parámetro que se compara en el modo comparar",
    )
    parser.add_argument("--calidad", default=None, help="texto de calidad")
    parser.add_argument("--errores", default=None, help="texto de errores")
    return parser


def _perfiles_disponibles(raiz):
    """Identificadores de los manifiestos de perfil, en orden alfabético.

    Los perfiles son los manifiestos ``*.json`` de ``raiz/src/gemma/perfiles/``
    salvo ``parametros_iniciales.json``, conforme a `C-1` y `DEC-002`; 1
    directorio ausente o sin manifiestos no declara ningún perfil.
    """
    directorio = Path(raiz) / DIRECTORIO_PERFILES
    if not directorio.is_dir():
        return []
    return sorted(
        ruta.stem
        for ruta in directorio.glob("*" + SUFIJO_MANIFIESTO)
        if ruta.is_file() and ruta.stem != MANIFIESTO_INICIAL
    )


def _leer_manifiesto(raiz, identificador):
    """Lee el manifiesto del perfil ya validado contra los disponibles."""
    ruta = Path(raiz) / DIRECTORIO_PERFILES / (identificador + SUFIJO_MANIFIESTO)
    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def _listar_perfiles(raiz, identificadores):
    """Imprime la raíz resuelta y la lista de perfiles de `DEC-001`."""
    print(f"Raíz: {raiz}")
    print(ENCABEZADO_MENU_PERFILES)
    for identificador in identificadores:
        print(f"  {identificador}")


def _cargar_catalogo(raiz):
    """Carga el catálogo de escenarios de `C-1` bajo la raíz recibida.

    La ruta relativa ``src/gemma/escenarios/catalogo.json`` se resuelve contra la
    raíz que llega por ``--raiz`` y nunca contra el directorio actual, de modo
    que la suite trabaja sobre su árbol temporal (`DEC-001`).
    """
    return escenarios.cargar_catalogo(Path(raiz) / RUTA_CATALOGO_ESCENARIOS)


def _listar_escenarios(raiz):
    """Modo ``--listar-escenarios`` de `C-2`: enumera los 9 y devuelve `0`.

    Cada línea declara los 5 datos de `RF-005` —identificador, estado, capas de
    expertos en CPU, contexto efectivo en tokens y presupuesto de VRAM en MiB—
    en el orden jerárquico de `DEC-004`, sin lanzar el servidor ni verificar los
    recursos de escenario alguno.
    """
    catalogo = _cargar_catalogo(raiz)
    print("Raíz: " + str(Path(raiz)))
    print(ENCABEZADO_MENU_ESCENARIOS)
    for escenario in escenarios.listar_escenarios(catalogo):
        contexto = escenario.get("contexto") or {}
        presupuesto = escenario.get("presupuesto_vram") or {}
        print(
            f"  {escenario['id']}: estado={escenario['estado']}, "
            f"capas_cpu_moe={escenario['capas_cpu_moe']}, "
            f"contexto_efectivo={contexto.get('efectivo_tokens')} tokens, "
            f"presupuesto_vram={presupuesto.get('total_mib')} MiB"
        )
    return CODIGO_OK


def _escenario_declarado(catalogo, identificador):
    """Devuelve el escenario de `id` exacto que declara el catálogo, o `None`."""
    declarados = catalogo.get("escenarios") or {}
    escenario = declarados.get(identificador)
    return escenario if isinstance(escenario, dict) else None


def _rechazar_escenario_inexistente(catalogo, identificador):
    """Rechazo de `RF-004`: nombra el identificador y enumera los 9 canónicos."""
    print(
        f"[ERROR] escenario no declarado: {identificador}; --escenario debe "
        "nombrar 1 identificador del catálogo",
        file=sys.stderr,
    )
    disponibles = [
        escenario["id"] for escenario in escenarios.listar_escenarios(catalogo)
    ]
    print("Escenarios disponibles: " + ", ".join(disponibles))


def _entrada_interactiva(identificadores):
    """Indica si la invocación sin `--perfil` presenta el menú de `C-2`.

    Con ``LEER_ENTRADA`` sustituido por 1 punto inyectable, el menú se presenta
    siempre; con el ``input`` por omisión exige 1 perfil de base único y 1
    terminal en la entrada estándar. Con varios perfiles disponibles y sin
    consola, la invocación sin `--perfil` conserva el listado de `DEC-001` y
    devuelve el código `2`, de modo que ninguna ejecución queda a la espera de
    una línea que no va a llegar.
    """
    if LEER_ENTRADA is not input:
        return True
    if len(identificadores) != 1:
        return False
    entrada = getattr(sys, "stdin", None)
    try:
        return bool(entrada is not None and entrada.isatty())
    except (AttributeError, ValueError):
        return False


def _leer_seleccion():
    """Lee 1 línea de la consola por ``LEER_ENTRADA`` y la devuelve sin espacios.

    El final de la entrada se declara como selección vacía, de modo que el flujo
    aborta con el código `2` de `C-2` en lugar de propagar la excepción.
    """
    try:
        linea = LEER_ENTRADA("Selección: ")
    except EOFError:
        return ""
    if linea is None:
        return ""
    return str(linea).strip()


def _imprimir_menu_escenarios(listado):
    """Imprime el menú detallado de `C-2` con la numeración de `DEC-004`.

    Cada línea declara el identificador, las capas de expertos en CPU, el
    contexto efectivo en tokens y el presupuesto de VRAM en MiB que enumera
    `RF-005`, y añade la marca al escenario que `CB-007` no permite seleccionar.
    """
    print(ENCABEZADO_MENU_ESCENARIOS)
    for numero, escenario in enumerate(listado, start=1):
        contexto = escenario.get("contexto") or {}
        presupuesto = escenario.get("presupuesto_vram") or {}
        linea = (
            f"  {numero}) {escenario['id']}: "
            f"capas_cpu_moe={escenario.get('capas_cpu_moe')}, "
            f"contexto_efectivo={contexto.get('efectivo_tokens')} tokens, "
            f"presupuesto_vram={presupuesto.get('total_mib')} MiB"
        )
        if escenario.get("estado") == escenarios.ESTADO_NO_EJECUTABLE:
            linea = f"{linea} {MARCA_NO_EJECUTABLE}"
        print(linea)


def _recordar_menu_escenarios(listado):
    """Reimprime el encabezado y la numeración del menú tras 1 rechazo.

    La reimpresión repite el encabezado literal y la numeración de `DEC-004` sin
    los datos de detalle ni la marca del escenario no ejecutable, que figura 1
    sola vez en el menú detallado; el operador conserva así la referencia de
    números para la línea siguiente.
    """
    print(ENCABEZADO_MENU_ESCENARIOS)
    for numero, escenario in enumerate(listado, start=1):
        print(f"  {numero}) {escenario['id']}")


def _resolver_seleccion_escenario(catalogo, listado, texto):
    """Devuelve el escenario declarado que nombra la selección, o `None`.

    `RF-003` y `RF-004`: 1 número dentro de la numeración resuelve el escenario
    de esa posición y 1 identificador resuelve el declarado con esa clave. 1
    número fuera de rango y 1 identificador ausente del catálogo informan el
    rechazo sin resolver, y `CB-007` rechaza el escenario no ejecutable nombrando
    su identificador.
    """
    if texto.isdigit():
        numero = int(texto)
        if not 1 <= numero <= len(listado):
            print(
                f"[ERROR] selección fuera de rango: {texto}; el menú numera los "
                f"{len(listado)} escenarios del 1 al {len(listado)}",
                file=sys.stderr,
            )
            return None
        escenario = _escenario_declarado(catalogo, listado[numero - 1]["id"])
        if escenario is None:
            _rechazar_escenario_inexistente(catalogo, listado[numero - 1]["id"])
            return None
    else:
        escenario = _escenario_declarado(catalogo, texto)
        if escenario is None:
            _rechazar_escenario_inexistente(catalogo, texto)
            return None
    if escenario.get("estado") == escenarios.ESTADO_NO_EJECUTABLE:
        print(
            f"[ERROR] escenario no ejecutable: {escenario.get('id')}; el menú "
            "no lo selecciona por su estado y vuelve a preguntar",
            file=sys.stderr,
        )
        return None
    return escenario


def _seleccionar_escenario(catalogo):
    """Resuelve 1 escenario por número o por identificador (`RF-003`).

    El menú admite la numeración de `DEC-004` y el identificador canónico exacto.
    1 selección vacía informa el rechazo y devuelve `None`, de modo que el flujo
    aborta con el código `2` de `C-2` sin precheck ni lanzamiento; 1 selección
    inválida y 1 escenario no ejecutable informan el rechazo, reimprimen la
    numeración y vuelven a preguntar.
    """
    listado = escenarios.listar_escenarios(catalogo)
    _imprimir_menu_escenarios(listado)
    while True:
        texto = _leer_seleccion()
        if not texto:
            print(
                "[ERROR] selección vacía: el menú espera 1 número del 1 al "
                f"{len(listado)} o 1 identificador del catálogo",
                file=sys.stderr,
            )
            return None
        escenario = _resolver_seleccion_escenario(catalogo, listado, texto)
        if escenario is not None:
            return escenario
        _recordar_menu_escenarios(listado)


def _imprimir_menu_perfiles(raiz, identificadores):
    """Imprime la raíz resuelta y la numeración de perfiles de `DEC-001`."""
    print(f"Raíz: {raiz}")
    print(ENCABEZADO_MENU_PERFILES)
    for numero, identificador in enumerate(identificadores, start=1):
        print(f"  {numero}) {identificador}")


def _seleccionar_perfil(raiz, identificadores):
    """Resuelve el perfil de base del flujo interactivo, por número o por id.

    Tras resolver el escenario, `C-2` exige 1 perfil de base para los artefactos
    y la comprobación previa. 1 selección vacía informa el rechazo y devuelve
    `None` para abortar con el código `2`; 1 número fuera de la numeración y 1
    identificador ausente de la lista informan el rechazo, reimprimen la
    numeración y vuelven a preguntar.
    """
    _imprimir_menu_perfiles(raiz, identificadores)
    while True:
        texto = _leer_seleccion()
        if not texto:
            print(
                "[ERROR] selección vacía: el menú espera 1 número de perfil o 1 "
                "identificador de la lista",
                file=sys.stderr,
            )
            return None
        if texto in identificadores:
            return texto
        if texto.isdigit():
            numero = int(texto)
            if 1 <= numero <= len(identificadores):
                return identificadores[numero - 1]
        print(
            f"[ERROR] perfil no declarado: {texto}; el menú espera 1 número del "
            f"1 al {len(identificadores)} o 1 identificador de la lista",
            file=sys.stderr,
        )
        _imprimir_menu_perfiles(raiz, identificadores)


def _anunciar_escenario(escenario):
    """Declara en consola el escenario seleccionado y su presupuesto (`RF-003`)."""
    contexto = escenario.get("contexto") or {}
    presupuesto = escenario.get("presupuesto_vram") or {}
    print(
        f"ESCENARIO {escenario.get('id')}: contexto solicitado "
        f"{contexto.get('declarado_tokens')} tokens, presupuesto declarado "
        f"{presupuesto.get('total_mib')} MiB"
    )


def _opciones_del_escenario(escenario, contexto_efectivo):
    """Los 9 ejes de `C-2` con el valor declarado por el escenario.

    Los 7 parámetros de ``parametros_ejecucion`` de `DEC-011` aportan
    ``gpu_layers``, ``flash_attn``, ``ubatch``, ``load_mode``, ``parallel`` y los
    2 tipos de caché KV; ``ncmoe`` toma las capas de expertos en CPU del
    escenario y ``ctx_size`` el contexto efectivo resuelto del lanzamiento.
    """
    parametros = escenario.get("parametros_ejecucion") or {}
    return {
        "gpu_layers": parametros.get("gpu_layers"),
        "flash_attn": parametros.get("flash_attn"),
        "ctx_size": contexto_efectivo,
        "ubatch": parametros.get("ubatch"),
        "ncmoe": escenario.get("capas_cpu_moe"),
        "load_mode": parametros.get("load_mode"),
        "parallel": parametros.get("parallel"),
        "cache_type_k": parametros.get("cache_type_k"),
        "cache_type_v": parametros.get("cache_type_v"),
    }


def _efectivas_del_escenario(escenario):
    """Opciones efectivas del escenario, con el contexto ajustado recalculado.

    `CB-005` y `DEC-008`: el escenario de contexto ajustado deriva sus tokens de
    la VRAM libre medida en el momento del lanzamiento y no del valor declarado
    en la selección; el valor derivado se valida con `CB-003` antes de arrancar.
    Devuelve ``(efectivas, None)`` o ``(None, motivo)`` cuando la VRAM no se
    puede medir o el contexto resuelto no supera el suelo.
    """
    contexto = escenario.get("contexto") or {}
    tokens = contexto.get("efectivo_tokens")
    if contexto.get("tipo") == escenarios.TIPO_CONTEXTO_AJUSTADO:
        vram_libre = _vram_libre_para_comprobar()
        if vram_libre is None:
            return (
                None,
                "VRAM disponible no medible: el contexto ajustado del escenario "
                f"{escenario.get('id')} no se recalcula ni se estima (CB-001)",
            )
        try:
            tokens = escenarios.resolver_contexto_ajustado(escenario, vram_libre)
        except (TypeError, ValueError) as error:
            return (
                None,
                "contexto ajustado no resoluble en el escenario "
                f"{escenario.get('id')}: {error}",
            )
        admisible, motivo = escenarios.validar_contexto_ajustado(escenario, tokens)
        if not admisible:
            return (None, motivo)
    return (
        {"opciones": _opciones_del_escenario(escenario, tokens), "omitidas": []},
        None,
    )


def _verificar_recursos_del_escenario(escenario):
    """Precheck de recursos de `C-4` por el punto ``VERIFICAR_RECURSOS_ESCENARIO``.

    Imprime los hallazgos ``[FALLO]`` que declara el resultado y devuelve su
    código, que es `3` en el primer aborto y `0` sin hallazgos; el lanzamiento no
    se invoca en ningún caso desde aquí.
    """
    resultado = VERIFICAR_RECURSOS_ESCENARIO(escenario)
    hallazgos = list(resultado.get("hallazgos") or ())
    for linea in hallazgos:
        print(linea)
    codigo = resultado.get("codigo")
    if isinstance(codigo, bool) or not isinstance(codigo, int):
        return CODIGO_PRECHECK_ESCENARIO if hallazgos else CODIGO_OK
    return codigo


def _comprobar_escenario(escenario):
    """Modo ``comprobar`` con escenario: diagnóstico de `C-4` sin carga."""
    _anunciar_escenario(escenario)
    return _verificar_recursos_del_escenario(escenario)


def _bloque_de_conformidad(escenario, memoria):
    """Las 4 entradas del bloque ``escenario`` de `C-5` de `SPEC-018`.

    ``registro`` deriva después ``delta_presupuesto_mib``, ``dictamen`` y
    ``conforme_presupuesto`` bajo la regla ``consumo <= presupuesto`` de
    `AMB-010`; sin medición de VRAM asignada, la clave correspondiente vale
    ``None`` y el dictamen declara la ausencia.
    """
    presupuesto = escenario.get("presupuesto_vram") or {}
    return {
        "escenario_id": escenario.get("id"),
        "presupuesto_vram_declarado_mib": presupuesto.get("total_mib"),
        "vram_asignada_medida_mib": memoria.get("vram_usada_mib"),
        "vram_libre_medida_mib": memoria.get("vram_libre_mib"),
    }


def _ruta_ejecutable(manifiesto, raiz):
    """Ruta del ejecutable declarado en `artefactos`, resuelta contra la raíz."""
    relativa = (manifiesto.get("artefactos") or {}).get("ejecutable")
    if not relativa:
        return None
    return Path(raiz) / relativa


def _opciones_aceptadas(manifiesto, raiz):
    """Mapa de opciones que la ayuda del binario enumera, según `DEC-010`.

    Consulta ``binario.opciones_aceptadas`` por atributo de módulo sobre la ruta
    de `artefactos.ejecutable` resuelta contra la raíz. 1 ejecutable ausente deja
    el mapa en `None` en lugar de propagar el ``ValueError`` de la consulta: la
    comprobación 1 de `C-9` ya reporta esa ausencia con el código `4`, que es el
    primer fallo del orden de `C-8`, de modo que el lanzador no aborta antes de
    imprimir la comprobación previa.
    """
    ruta = _ruta_ejecutable(manifiesto, raiz)
    if ruta is None:
        return None
    try:
        return binario.opciones_aceptadas(ruta)
    except ValueError:
        return None


def _vram_libre_para_comprobar():
    """VRAM libre en MiB de la consulta de solo lectura, o `None` si no está.

    `T-068` expone ``medir.vram_libre_mib`` como consulta de solo lectura: no
    lanza el servidor, no carga el modelo, no consulta contadores y no usa
    PowerShell. La herramienta ausente, 1 salida no numérica o 1 error de
    ejecución devuelven `None`, de modo que la comprobación 4 se reporta
    `PENDIENTE` con su motivo y ningún valor se estima, conforme a `DEC-018`.
    """
    try:
        valor = VRAM_LIBRE_MIB()
    except (OSError, ValueError):
        return None
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    return float(valor)


def _comprobar(manifiesto, raiz, argumentos):
    """Modo `comprobar` de `DEC-003`: comprobación previa sin carga.

    Inyecta en ``precheck.ejecutar`` el mapa que la ayuda del binario enumera, la
    VRAM libre en MiB de la consulta de solo lectura de `T-068` y las opciones
    efectivas de `C-3` que resuelven los registros disponibles, de modo que la
    comprobación 4 contrasta el presupuesto con el `ctx_size` que el servidor
    usaría y no con el declarado; imprime la salida de
    ``precheck.formatear_salida`` y devuelve el código de `C-8` del resultado sin
    reinterpretarlo. Sin la consulta disponible no informa
    ``vram_disponible_mib`` y la comprobación 4 queda `PENDIENTE` con su motivo,
    sin estimar ningún valor, conforme a `DEC-018`. No lanza el servidor ni carga
    el modelo.
    """
    opciones_aceptadas = _opciones_aceptadas(manifiesto, raiz)
    efectivas = _opciones_efectivas(manifiesto, raiz, argumentos)
    argumentos_comprobacion = {
        "opciones_aceptadas": opciones_aceptadas,
        "opciones_efectivas": efectivas["opciones"],
    }
    vram_libre = _vram_libre_para_comprobar()
    if vram_libre is not None:
        argumentos_comprobacion["vram_disponible_mib"] = vram_libre
    resultado = precheck.ejecutar(manifiesto, raiz, **argumentos_comprobacion)
    for linea in precheck.formatear_salida(resultado):
        print(linea)
    return resultado["codigo"]


def _presupuesto_pendiente(manifiesto):
    """Indica si el bloque `presupuesto_vram` conserva su clave `pendiente`."""
    bloque = manifiesto.get("presupuesto_vram") or {}
    return precheck.CLAVE_PENDIENTE in bloque


def _vram_disponible_mib():
    """VRAM libre en MiB de la medición de memoria, o `None` si no está.

    Se reutiliza el punto inyectable ``MEDIR_MEMORIA`` con el PID del proceso
    del lanzador: la consulta de la GPU devuelve los totales del adaptador y la
    suite la sustituye por su doble, de modo que ninguna ejecución de prueba
    consulta la GPU real.
    """
    resultado = MEDIR_MEMORIA([os.getpid()])
    if resultado.get("codigo") != CODIGO_OK:
        return None
    libre = resultado.get("vram_libre_mib")
    if isinstance(libre, bool) or not isinstance(libre, int):
        return None
    return libre


def _comprobacion_previa(manifiesto, raiz, efectivas):
    """Comprobación previa completa de los modos con carga.

    Imprime la salida de `C-9` y devuelve el código del primer fallo. La
    comprobación 4 recibe el `ctx_size` de las opciones efectivas de `C-3` que el
    modo ya resolvió, de modo que el techo se contrasta con el contexto con el
    que el servidor arranca y no con el declarado en el manifiesto. Con el
    bloque `presupuesto_vram` completo, la comprobación 4 recibe además la VRAM
    libre menos el margen de `RNF-007`, de modo que declararla superada acredita
    que la carga deja al menos `MARGEN_VRAM_MIB` MiB libres; mientras el bloque
    conserve su clave `pendiente`, el presupuesto no se estima y la comprobación
    se reporta `PENDIENTE` con el código `0` de `DEC-018`.
    """
    opciones_aceptadas = _opciones_aceptadas(manifiesto, raiz)
    disponible = None
    if not _presupuesto_pendiente(manifiesto):
        libre = _vram_disponible_mib()
        if libre is not None:
            disponible = max(libre - MARGEN_VRAM_MIB, 0)

    if disponible is None:
        resultado = precheck.ejecutar(
            manifiesto,
            raiz,
            opciones_aceptadas=opciones_aceptadas,
            opciones_efectivas=efectivas["opciones"],
        )
    else:
        resultado = precheck.ejecutar(
            manifiesto,
            raiz,
            opciones_aceptadas=opciones_aceptadas,
            opciones_efectivas=efectivas["opciones"],
            vram_disponible_mib=disponible,
        )

    for linea in precheck.formatear_salida(resultado):
        print(linea)
    return resultado["codigo"]


def _host():
    """Nombre de host del punto de acceso de `URL_BASE`."""
    resto = URL_BASE.split("://", 1)[-1]
    host = resto.split("/", 1)[0].split(":", 1)[0]
    return host or "127.0.0.1"


def _url_salud():
    """URL absoluta de ``GET /health`` sobre la constante ``PUERTO``."""
    return f"{URL_BASE.rstrip('/')}:{PUERTO}{RUTA_SALUD}"


def _especulativa(manifiesto):
    """Bloque `especulativa` de `DEC-024` del manifiesto, o 1 mapa vacío.

    El bloque declara `tipo`, que admite `draft-mtp` o `ninguno`, y `techo`, que
    es el entero de tokens del borrador con `draft-mtp` y `null` con `ninguno`.
    """
    bloque = manifiesto.get("especulativa")
    return bloque if isinstance(bloque, dict) else {}


def _argumentos_del_servidor(manifiesto, raiz, opciones):
    """Argumentos del binario con las opciones efectivas de `C-3`.

    El modelo, el proyector y el draft se resuelven contra la raíz; cada eje de
    `C-2` declara su forma larga con su valor efectivo, de modo que la carga de
    pesos sin mapa de memoria viaja como `--load-mode none`, que es 1 valor que
    el binario admite. Los 3 artefactos son los que la comprobación 1 de `C-9` ya
    acreditó como presentes. Con `tipo` `draft-mtp` y 1 `artefactos.draft`
    declarado, `DEC-024` añade `--spec-type draft-mtp` y
    `--spec-draft-n-max <techo>` después de `--model-draft`, porque sin esa
    declaración el servidor aborta al cargar `Gemma4Assistant`; con `tipo`
    `ninguno` no añade ninguna de las 2 banderas. El par `--log-verbosity 4` es
    1 bandera de registro y no 1 eje de `C-2`: hace que el binario imprima la
    línea `CUDA_Host model buffer size` del modelo principal, que es la fuente
    del campo 22 de `C-6`, sin alterar las 9 opciones del perfil ni la huella de
    `DEC-020`.
    """
    artefactos = manifiesto.get("artefactos") or {}
    argumentos = [
        "--model",
        str(Path(raiz) / artefactos["modelo"]),
        "--mmproj",
        str(Path(raiz) / artefactos["mmproj"]),
        "--host",
        _host(),
        "--port",
        str(PUERTO),
        BANDERA_VERBOSIDAD_REGISTRO,
        str(VERBOSIDAD_REGISTRO),
    ]
    for eje, forma in FORMA_DE_EJE.items():
        if eje in opciones:
            argumentos.extend([forma, str(opciones[eje])])
    draft = artefactos.get("draft")
    if draft:
        argumentos.extend(["--model-draft", str(Path(raiz) / draft)])
    especulativa = _especulativa(manifiesto)
    if draft and especulativa.get("tipo") == TIPO_ESPECULATIVA_DRAFT_MTP:
        argumentos.extend(
            [
                BANDERA_TIPO_ESPECULATIVA,
                TIPO_ESPECULATIVA_DRAFT_MTP,
                BANDERA_TECHO_BORRADOR,
                str(especulativa.get("techo")),
            ]
        )
    return argumentos


class _ServidorProceso:
    """Servidor lanzado: proceso del binario y su archivo de salida temporal.

    Expone el contrato que consume el orquestador —``pid``, ``activo()``,
    ``leer_salida()`` y ``cerrar()``— de modo que la suite sustituye
    ``LANZAR_SERVIDOR`` por 1 doble con la misma forma y no ejecuta el binario
    real.
    """

    def __init__(self, proceso, salida):
        self._proceso = proceso
        self._salida = salida
        self._cerrado = False

    @property
    def pid(self):
        """Identificador del proceso raíz del servidor."""
        return self._proceso.pid

    def activo(self):
        """Indica si el proceso sigue en ejecución."""
        return self._proceso.poll() is None

    def leer_salida(self):
        """Devuelve el texto capturado del binario sin cerrar el temporal.

        Rebobina el archivo temporal a su inicio y decodifica en UTF-8 con
        reemplazo, de modo que el lanzador lee la línea
        ``CUDA_Host model buffer size`` del registro del servidor antes de
        cerrarlo; tras el cierre el archivo ya no se puede leer y el texto queda
        vacío, que es la marca de fuente ausente del campo 22.
        """
        try:
            self._salida.flush()
            self._salida.seek(0)
            datos = self._salida.read()
        except (OSError, ValueError):
            return ""
        if isinstance(datos, bytes):
            return datos.decode("utf-8", "replace")
        return str(datos)

    def cerrar(self):
        """Termina el servidor, espera su salida y cierra el archivo temporal."""
        if self._cerrado:
            return
        self._cerrado = True
        try:
            if self._proceso.poll() is None:
                self._proceso.terminate()
                try:
                    self._proceso.wait(timeout=CIERRE_SERVIDOR_SEGUNDOS)
                except subprocess.TimeoutExpired:
                    self._proceso.kill()
                    self._proceso.wait(timeout=CIERRE_SERVIDOR_SEGUNDOS)
        finally:
            self._salida.close()


def _lanzar_servidor(ejecutable, argumentos):
    """Lanza el binario con sus argumentos y captura su salida a 1 temporal."""
    salida = tempfile.TemporaryFile()
    try:
        proceso = subprocess.Popen(
            [str(ejecutable), *argumentos],
            stdout=salida,
            stderr=subprocess.STDOUT,
        )
    except OSError as error:
        salida.close()
        raise ValueError(
            f"{ejecutable}: no se pudo lanzar el servidor: {error}"
        ) from error
    return _ServidorProceso(proceso, salida)


def _salud_responde_ok():
    """Indica si ``GET /health`` responde `200` con el estado `ok`."""
    try:
        with urllib.request.urlopen(
            _url_salud(), timeout=TIEMPO_LIMITE_SALUD_SEGUNDOS
        ) as respuesta:
            estado_http = respuesta.status
            cuerpo = respuesta.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError):
        return False
    if estado_http != 200:
        return False
    try:
        datos = json.loads(cuerpo)
    except json.JSONDecodeError:
        return cuerpo.strip() == "ok"
    return isinstance(datos, dict) and datos.get("status") == "ok"


def _esperar_salud(servidor, iniciar):
    """Espera ``GET /health`` respondiendo `ok` y devuelve el tiempo de carga.

    Devuelve ``(segundos, None)`` cuando la salud responde `ok`, o
    ``(None, motivo)`` cuando el proceso termina antes o se agota la espera. El
    tiempo se cuenta en segundos desde el lanzamiento del servidor.
    """
    limite = iniciar + ESPERA_SALUD_SEGUNDOS
    while True:
        if not servidor.activo():
            return None, "el proceso terminó antes de responder la salud"
        if _salud_responde_ok():
            return time.monotonic() - iniciar, None
        if time.monotonic() >= limite:
            return None, f"no respondió ok en {ESPERA_SALUD_SEGUNDOS} s"
        time.sleep(INTERVALO_SONDEO_SALUD_SEGUNDOS)


def _requiere_sonda(prueba):
    """Indica si la prueba requiere la sonda de `RF-009` y `DEC-011`.

    La prueba de carga, la de contexto sostenido de `T-037` y la alternativa de
    contexto menor de `T-041` son las 3 que acreditan `RF-009` y alimentan los
    campos 16 y 17 de `C-6`; cualquier otra ejecución de `medir` no invoca la
    sonda.
    """
    if not prueba:
        return False
    nombre = prueba.strip().lower()
    return any(
        nombre == prefijo or nombre.startswith(prefijo + "-")
        for prefijo in PRUEBAS_CON_SONDA
    )


def _es_prueba_de_carga(prueba):
    """Indica si la prueba declara el propósito `carga` de `C-5`."""
    if not prueba:
        return False
    nombre = prueba.strip().lower()
    return any(
        nombre == prefijo or nombre.startswith(prefijo + "-")
        for prefijo in PRUEBAS_DE_CARGA
    )


def _proposito(prueba):
    """Propósito de `C-5` de la prueba: `carga` o `medicion`."""
    return "carga" if _es_prueba_de_carga(prueba) else "medicion"


def _imprimir_opciones_efectivas(efectivas):
    """Imprime las opciones efectivas de `C-3` y los ejes omitidos."""
    print(
        "Opciones efectivas: "
        + json.dumps(efectivas["opciones"], ensure_ascii=False, sort_keys=True)
    )
    for eje in efectivas["omitidas"]:
        print(
            f"[AVISO] desviación omitida: {eje} (se aplica el valor inicial de C-2)"
        )


def _estabilidad(sonda, servidor):
    """Estabilidad del servidor al cierre, con el vocabulario de `C-6`.

    Con sonda, el resultado de `DEC-011` ya declara la estabilidad observada;
    sin sonda se consulta ``GET /health`` antes de cerrar el servidor.
    """
    if sonda is not None:
        return sonda.get("servidor") or NO_DISPONIBLE
    return (
        "continúa en servicio" if _salud_responde_ok() else "se detuvo"
    )


def _mib_campo(valor):
    """Texto de 1 magnitud en MiB, o la marca de fuente ausente."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return NO_DISPONIBLE
    if isinstance(valor, float):
        return f"{valor:g} MiB"
    return f"{valor} MiB"


def _memoria_expertos_en_host(salida):
    """Memoria de expertos en host del modelo principal, en MiB, o `None`.

    `C-6` y `DEC-026` toman la primera línea
    ``CUDA_Host model buffer size = <n> MiB`` de la salida capturada del
    servidor, que es la del modelo principal porque el binario carga sus pesos
    antes que el borrador. La línea del draft no se suma y ningún valor se
    estima: sin coincidencia la función devuelve `None` y el campo 22 declara
    la marca de fuente ausente.
    """
    if not isinstance(salida, str):
        return None
    for linea in salida.splitlines():
        coincidencia = PATRON_MEMORIA_EXPERTOS.search(linea)
        if coincidencia is None:
            continue
        cantidad = coincidencia.group(1)
        if "." in cantidad:
            return float(cantidad)
        return int(cantidad)
    return None


def _campo_22(salida):
    """Campo 22 de `C-6`: memoria de expertos en host en MiB o fuente ausente."""
    return _mib_campo(_memoria_expertos_en_host(salida))


def _decodificacion(manifiesto):
    """Vocabulario del campo 11 de `C-6` derivado del bloque `especulativa`.

    `DEC-024`: el estado y el techo del borrador se derivan de la declaración
    del manifiesto y no de la mera presencia de `artefactos.draft`, de modo que
    `tipo` `draft-mtp` transcribe el techo del bloque y `tipo` `ninguno`
    transcribe el vocabulario desactivado.
    """
    especulativa = _especulativa(manifiesto)
    if especulativa.get("tipo") == TIPO_ESPECULATIVA_DRAFT_MTP:
        return (
            "activado (techo de borrador "
            f"{especulativa.get('techo')} tokens)"
        )
    return registro.FORMA_11_DESACTIVADO


def _linea_sonda(sonda, segundos):
    """Línea `SONDA:` de `T-073` con el conteo del resultado de la sonda.

    El modo `medir` imprime el número de tokens que `probe.sondear` devuelve en
    ``tokens_generados``, que hasta `T-072` no llegaba a la salida y que `T-037`
    necesita para acreditar los 2 000 tokens de `CB-003`. Con la sonda
    `superada` la línea declara el tiempo medido por el lanzador alrededor de la
    sonda con 2 decimales y la velocidad de generación del resultado; con la
    sonda `fallida` declara el conteo parcial antes del corte y su motivo. El
    registro de `C-5` y el código de `C-8` no dependen de esta línea.
    """
    tokens = sonda.get("tokens_generados")
    texto_tokens = (
        str(tokens)
        if isinstance(tokens, int) and not isinstance(tokens, bool)
        else NO_DISPONIBLE
    )
    if sonda.get("estado") != "superada":
        motivo = sonda.get("motivo") or "la sonda de contexto no se completó"
        return f"SONDA: {texto_tokens} tokens contados antes del corte: {motivo}"
    if isinstance(segundos, bool) or not isinstance(segundos, (int, float)):
        texto_segundos = "0.00"
    else:
        texto_segundos = f"{float(segundos):.2f}"
    velocidad = sonda.get("tokens_por_segundo")
    if isinstance(velocidad, bool) or not isinstance(velocidad, (int, float)):
        texto_velocidad = NO_DISPONIBLE
    else:
        texto_velocidad = f"{float(velocidad):.2f}"
    return (
        f"SONDA: {texto_tokens} tokens en {texto_segundos} s, "
        f"{texto_velocidad} tokens/s"
    )


def _velocidad_de_generacion(sonda):
    """Velocidad de generación en tokens por segundo, o fuente ausente."""
    if sonda is None:
        return NO_DISPONIBLE
    valor = sonda.get("tokens_por_segundo")
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return NO_DISPONIBLE
    return f"{float(valor):.2f} tokens/s"


def _velocidad_de_prompt(sonda):
    """Velocidad de prompt en tokens por segundo, o fuente ausente.

    `C-6` toma la fila 16 del bloque de tiempos de la respuesta del servidor y
    el resultado de la sonda de `DEC-011` puede informarla en la clave
    ``velocidad_prompt_tokens_por_segundo``. Cuando no la informa, o cuando la
    sonda no se ejecutó, la fila declara la marca de fuente ausente y ningún
    valor se estima.
    """
    if sonda is None:
        return NO_DISPONIBLE
    valor = sonda.get(CLAVE_VELOCIDAD_PROMPT)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return NO_DISPONIBLE
    return f"{float(valor):.2f} tokens/s"


def _campo_21(manifiesto, argumentos, memoria, sonda):
    """Campo 21 de `C-6`: errores y advertencias declarados y observados.

    Mientras el bloque `presupuesto_vram` conserve su clave `pendiente`, el
    presupuesto se declara ``no disponible`` y no se estima (`DEC-018`); la
    prueba de contexto fallida transcribe su motivo con el número de tokens
    contados antes del corte y sin declarar superado nada (`CB-003`), y la VRAM
    libre por debajo de `RNF-007` queda registrada.
    """
    partes = []
    if argumentos.errores and argumentos.errores.strip():
        partes.append(argumentos.errores.strip())
    if _presupuesto_pendiente(manifiesto):
        partes.append(f"presupuesto de VRAM: {NO_DISPONIBLE}")
    if sonda is not None and sonda.get("estado") != "superada":
        motivo = sonda.get("motivo") or "la sonda de contexto no se completó"
        tokens = sonda.get("tokens_generados")
        if isinstance(tokens, int) and not isinstance(tokens, bool):
            motivo = f"{motivo}; {tokens} tokens contados antes del corte"
        partes.append(f"prueba de contexto fallida: {motivo}")
    libre = memoria.get("vram_libre_mib")
    if (
        isinstance(libre, int)
        and not isinstance(libre, bool)
        and libre < MARGEN_VRAM_MIB
    ):
        partes.append(
            f"VRAM libre por debajo de {MARGEN_VRAM_MIB} MiB: {libre} MiB"
        )
    return "; ".join(partes) if partes else "sin errores"


def _campos_de_c6(
    manifiesto,
    argumentos,
    opciones,
    carga,
    memoria,
    sonda,
    estabilidad,
    version,
    commit,
    instante,
    prueba=None,
    salida_servidor=None,
):
    """Mapa de las 22 etiquetas de `C-6` a su texto, en el orden de `RF-006`.

    ``prueba`` sustituye el nombre de `--prueba` en la fila 2, de modo que la
    campaña de comparación puede declarar el nombre que compone su identificador
    cuando ``--prueba`` no llega. ``salida_servidor`` es el texto capturado del
    binario: de él toma el campo 22 la memoria de expertos en host del modelo
    principal y, sin él, la fila declara la marca de fuente ausente.
    """
    cuantizacion = manifiesto.get("cuantizacion") or {}
    calidad = (argumentos.calidad or "").strip()
    nombre_prueba = (
        prueba if prueba is not None else argumentos.prueba or ""
    ).strip()
    return {
        "Fecha de la prueba": instante.strftime("%Y-%m-%d"),
        "Nombre de la prueba": nombre_prueba,
        "Versión del binario": version,
        "Commit de llama.cpp": commit,
        "Modelo y cuantización": (
            f"{manifiesto.get('modelo')} {cuantizacion.get('declarada')}"
        ).strip(),
        "Contexto configurado": f"{opciones.get('ctx_size')} tokens",
        "Ranuras del servidor": f"{opciones.get('parallel')} ranuras",
        "Capas de expertos en CPU": f"{opciones.get('ncmoe')} capas",
        "Micro-lote": f"{opciones.get('ubatch')} tokens",
        "Atención rápida": (
            "activado" if opciones.get("flash_attn") == "on" else "desactivado"
        ),
        "Decodificación especulativa": _decodificacion(manifiesto),
        "Tiempo de carga": f"{carga:.2f} s",
        "VRAM asignada": _mib_campo(memoria.get("vram_usada_mib")),
        "VRAM libre": _mib_campo(memoria.get("vram_libre_mib")),
        "RAM utilizada": _mib_campo(memoria.get("residente_mib")),
        # `C-6` y `DEC-011`: el bloque de tiempos informa la velocidad de
        # generación y, cuando la informa, la de prompt.
        "Velocidad de prompt": _velocidad_de_prompt(sonda),
        "Velocidad de generación": _velocidad_de_generacion(sonda),
        "Estabilidad del servidor": estabilidad,
        "Desbordamiento hacia memoria compartida": _mib_campo(
            memoria.get("desbordamiento_mib")
        ),
        "Calidad funcional de la respuesta": calidad or NO_DISPONIBLE,
        "Errores y advertencias": _campo_21(manifiesto, argumentos, memoria, sonda),
        # `C-6` y `DEC-026`: el campo 22 toma la memoria de expertos en host del
        # modelo principal en el registro del servidor, sin sumar la del draft.
        "Memoria de expertos en host": _campo_22(salida_servidor),
    }


def _version_del_binario(ejecutable):
    """Versión y commit leídos de la salida del binario, o fuente ausente."""
    if ejecutable is None:
        return NO_DISPONIBLE, NO_DISPONIBLE
    try:
        datos = binario.leer_version(ejecutable)
    except (OSError, ValueError):
        return NO_DISPONIBLE, NO_DISPONIBLE
    return (
        str(datos.get("version") or NO_DISPONIBLE),
        str(datos.get("commit") or NO_DISPONIBLE),
    )


def _registro_anterior(directorio):
    """Identificador del registro previo del perfil, o `None` si no hay."""
    if not directorio.is_dir():
        return None
    rutas = sorted(directorio.glob("*.md"))
    return rutas[-1].stem if rutas else None


def _construir_registro(
    manifiesto,
    raiz,
    argumentos,
    efectivas,
    carga,
    memoria,
    sonda,
    estabilidad,
    *,
    prueba=None,
    proposito=None,
    comparacion=None,
    instante=None,
    salida_servidor=None,
    escenario=None,
):
    """Construye en memoria el registro de `C-5` y devuelve su carpeta.

    La huella es la de las ``opciones`` declaradas en el manifiesto y no la de
    las efectivas, conforme a `DEC-020`; la carpeta de registros cuelga de la
    raíz recibida, de modo que la suite escribe en su árbol temporal. ``prueba``,
    ``proposito`` e ``instante`` se inyectan para la campaña de comparación y,
    ausentes, conservan el nombre de `--prueba`, el propósito de la prueba y el
    reloj del sistema. ``comparacion`` añade a la clave opcional de `C-7` el
    bloque que la campaña calcula antes de escribir el registro y
    ``salida_servidor`` es el texto capturado del binario del que el campo 22
    toma la memoria de expertos en host. ``escenario`` añade el bloque de
    conformidad presupuestaria de `C-5` de `SPEC-018` cuando la ejecución
    declara 1 escenario del catálogo.
    """
    momento = instante if instante is not None else datetime.now(timezone.utc)
    identificador = manifiesto.get("id") or argumentos.perfil
    nombre = (prueba if prueba is not None else argumentos.prueba or "").strip()
    directorio = Path(raiz) / RUTA_REGISTROS / identificador
    version, commit = _version_del_binario(_ruta_ejecutable(manifiesto, raiz))

    frontmatter = {
        "huella_opciones": perfiles.huella_opciones(
            manifiesto.get("opciones") or {}
        ),
        "opciones_efectivas": dict(efectivas["opciones"]),
        "vram_total_mib": memoria["vram_total_mib"],
        "version_binario": version,
        "commit_llama_cpp": commit,
        "registro_anterior": _registro_anterior(directorio),
    }
    if comparacion is not None:
        frontmatter[registro.CLAVE_COMPARACION] = dict(comparacion)
    campos = _campos_de_c6(
        manifiesto,
        argumentos,
        efectivas["opciones"],
        carga,
        memoria,
        sonda,
        estabilidad,
        version,
        commit,
        momento,
        nombre,
        salida_servidor,
    )
    construido = registro.construir_registro(
        identificador,
        nombre,
        proposito if proposito is not None else _proposito(nombre),
        frontmatter,
        campos,
        instante=momento,
        escenario=escenario,
    )
    return construido, directorio


def _crear_registro(
    manifiesto,
    raiz,
    argumentos,
    efectivas,
    carga,
    memoria,
    sonda,
    estabilidad,
    salida_servidor=None,
    escenario=None,
):
    """Crea el registro de `C-5` de 1 ejecución y devuelve su ruta.

    La huella es la de las ``opciones`` declaradas en el manifiesto y no la de
    las efectivas, conforme a `DEC-020`; la carpeta de registros cuelga de la
    raíz recibida, de modo que la suite escribe en su árbol temporal.
    ``salida_servidor`` es el texto capturado del binario, del que el campo 22
    toma la memoria de expertos en host. ``escenario`` es el bloque de
    conformidad presupuestaria de `C-5` de `SPEC-018`, presente solo cuando la
    ejecución declara 1 escenario del catálogo.
    """
    construido, directorio = _construir_registro(
        manifiesto,
        raiz,
        argumentos,
        efectivas,
        carga,
        memoria,
        sonda,
        estabilidad,
        salida_servidor=salida_servidor,
        escenario=escenario,
    )
    ruta = registro.escribir_registro(directorio, construido)
    print(f"REGISTRO: {construido['id']}")
    print(f"Registro: {ruta}")
    return ruta


def _directorio_de_registros(raiz, manifiesto, argumentos):
    """Carpeta de registros del perfil bajo la raíz recibida (`C-5`)."""
    identificador = manifiesto.get("id") or argumentos.perfil
    return Path(raiz) / RUTA_REGISTROS / identificador


def _bloque_de_comparacion_del_archivo(ruta):
    """Bloque `comparacion` de `C-7` declarado por 1 registro, o `None`.

    `C-7` sitúa el bloque en la clave ``comparacion`` del registro de la prueba
    de comparación; `comparar.leer_registro` lee las 11 claves de `C-5` e ignora
    esa clave adicional, de modo que el orquestador la recupera aquí sin
    recalcular ninguna cifra.
    """
    try:
        texto = ruta.read_text(encoding="utf-8-sig")
    except OSError:
        return None
    for linea in texto.splitlines():
        clave, separador, valor = linea.partition(":")
        if separador != ":" or clave.strip() != "comparacion":
            continue
        try:
            bloque = json.loads(valor.strip())
        except json.JSONDecodeError:
            return None
        return bloque if isinstance(bloque, dict) else None
    return None


def _leer_registros(raiz, manifiesto, argumentos):
    """Mapa identificador → lectura de los registros del perfil (`C-3`).

    Cada lectura declara ``frontmatter`` y ``filas`` —la forma que devuelve
    ``comparar.leer_registro``— y, cuando el registro es de la prueba de
    comparación, el bloque ``comparacion`` de `C-7` en el nivel superior. No lee
    ``bin/``, ``models/`` ni la GPU y parte de la raíz recibida.
    """
    directorio = _directorio_de_registros(raiz, manifiesto, argumentos)
    registros = {}
    if not directorio.is_dir():
        return registros
    for ruta in sorted(directorio.glob("*.md")):
        try:
            lectura = comparar.leer_registro(ruta)
        except ValueError as error:
            raise ValueError(f"{ruta}: {error}") from error
        bloque = _bloque_de_comparacion_del_archivo(ruta)
        if bloque is not None:
            lectura["comparacion"] = bloque
        registros[lectura["frontmatter"]["id"]] = lectura
    return registros


def _opciones_efectivas(manifiesto, raiz, argumentos):
    """Opciones efectivas de `C-3` resueltas con los registros disponibles.

    La comprobación 4 de `C-9` consume el `ctx_size` de este mapa, que es el
    contexto con el que el servidor arranca. Los registros cuelgan de
    ``results/gemma/<perfil>/`` bajo la raíz recibida y el mapa queda vacío
    cuando esa carpeta no existe, de modo que los ejes conservan el valor
    inicial de `C-2`; 1 registro ilegible tampoco impide la comprobación previa,
    porque su lectura no forma parte de las 5 comprobaciones y la resolución cae
    al mismo valor inicial que usan las ejecuciones de servicio de `DEC-008`.
    """
    try:
        registros = _leer_registros(raiz, manifiesto, argumentos)
    except ValueError:
        registros = {}
    return perfiles.resolver_opciones(manifiesto, registros)


def _desviacion_de(manifiesto, parametro):
    """Desviación del perfil cuyo `parametro` es la clave recibida, o `None`."""
    for desviacion in manifiesto.get("desviaciones") or []:
        if isinstance(desviacion, dict) and desviacion.get("parametro") == parametro:
            return desviacion
    return None


def _bloque_registrado(registros, desviacion):
    """Bloque completo de `C-7` que la desviación tiene registrado, o `None`."""
    referencia = (desviacion or {}).get("comparacion")
    if not isinstance(referencia, str):
        return None
    lectura = registros.get(referencia)
    if not isinstance(lectura, dict):
        return None
    bloque = lectura.get("comparacion")
    if not isinstance(bloque, dict):
        return None
    if any(clave not in bloque for clave in perfiles.CAMPOS_COMPARACION):
        return None
    return bloque


def _artefacto_ausente(manifiesto, raiz):
    """Primer artefacto del perfil que no existe, o `None` si están los 3.

    La campaña de comparación arranca el binario 2 veces, de modo que contrasta
    antes la existencia de los artefactos de la comprobación 1 de `C-9` y, si
    falta 1, no lanza nada: la medición correspondería a 1 carga que no puede
    ejecutarse. El artefacto opcional `draft` solo se exige cuando el manifiesto
    lo declara.
    """
    artefactos = manifiesto.get("artefactos") or {}
    for clave in precheck.ARTEFACTOS_SIEMPRE + (precheck.ARTEFACTO_OPCIONAL,):
        relativa = artefactos.get(clave)
        if relativa is None:
            if clave == precheck.ARTEFACTO_OPCIONAL:
                continue
            return f"{clave} (no declarado)"
        if not (Path(raiz) / relativa).exists():
            return f"{clave} {relativa}"
    return None


def _prueba_de_comparacion(argumentos, parametro):
    """Nombre de la prueba de la campaña: el de `--prueba` o `comparacion-<eje>`.

    `C-8` no exige `--prueba` en el modo `comparar`, y `C-5` exige 1 nombre de
    prueba que componga el identificador del registro; sin `--prueba`, la
    campaña declara el nombre determinista `comparacion-<eje>`, de modo que los
    2 registros del eje son identificables sin intervención del operador.
    """
    nombre = (argumentos.prueba or "").strip()
    return nombre or f"{PREFIJO_PRUEBA_COMPARACION}-{parametro}"


def _opciones_de_comparacion(manifiesto, parametro, valor, registros):
    """Opciones de 1 medición: las efectivas adoptadas y el eje en su valor.

    La campaña compara 1 eje por vez y conserva los otros en la opción efectiva
    adoptada —las comparaciones que el perfil declara en `C-3` y constan entre
    sus ``registros``—, de modo que las 5 diferencias del bloque de `C-7` son
    atribuibles al eje comparado; el valor recibido es el inicial o el propuesto
    de la desviación de `C-3`. `T-079` corrige la resolución sin registros: con
    `ncmoe` adoptado en `6`, la comparación de `ubatch` corre a `ncmoe` `6` en
    las 2 mediciones y no a `0`.
    """
    adoptadas = perfiles.resolver_opciones(manifiesto, registros)
    opciones = dict(adoptadas["opciones"])
    opciones[parametro] = valor
    return {"opciones": opciones, "omitidas": list(adoptadas["omitidas"])}


def _medicion_de_comparacion(manifiesto, raiz, argumentos, parametro, valor):
    """Ejecuta 1 medición de la campaña y devuelve sus datos, o `None`.

    Repite el flujo de 1 ejecución de `plan.md`: lanza el ejecutable con las
    opciones del eje en el valor recibido, espera `GET /health`, mide la memoria
    del árbol del proceso, ejecuta la sonda de `DEC-011` —las 5 diferencias de
    `C-7` incluyen las 2 velocidades del bloque de tiempos, de modo que la
    comparación requiere la sonda en las 2 mediciones—, lee la salida capturada
    del servidor —de la que el campo 22 toma la memoria de expertos en host— y
    cierra el servidor. No escribe archivo alguno: el registro lo construye y lo
    escribe la campaña. Las opciones parten de las efectivas adoptadas por el
    perfil y solo el eje comparado recibe el valor recibido; 1 registro adoptado
    ilegible degrada a los valores iniciales sin abortar y lo declara. 1 fallo de
    arranque, de salud o de medición de memoria devuelve `None` con su mensaje,
    sin declarar ninguna cifra.
    """
    try:
        registros = _leer_registros(raiz, manifiesto, argumentos)
    except ValueError as error:
        print(
            "[AVISO] comparación con las opciones iniciales: 1 registro "
            f"adoptado no se pudo leer: {error}",
            file=sys.stderr,
        )
        registros = {}
    efectivas = _opciones_de_comparacion(
        manifiesto, parametro, valor, registros
    )
    ejecutable = _ruta_ejecutable(manifiesto, raiz)
    argumentos_servidor = _argumentos_del_servidor(
        manifiesto, raiz, efectivas["opciones"]
    )
    # `C-6`: el tiempo de carga se cuenta desde el lanzamiento del servidor.
    iniciar = time.monotonic()
    try:
        servidor = LANZAR_SERVIDOR(ejecutable, argumentos_servidor)
    except (OSError, ValueError) as error:
        print(f"[ERROR] no se pudo lanzar el servidor: {error}", file=sys.stderr)
        return None

    try:
        carga, motivo = _esperar_salud(servidor, iniciar)
        if carga is None:
            print(
                f"[ERROR] el servidor no quedó en servicio: {motivo}",
                file=sys.stderr,
            )
            return None
        memoria = MEDIR_MEMORIA([servidor.pid])
        sonda = SONDEAR(f"{URL_BASE.rstrip('/')}:{PUERTO}")
        estabilidad = _estabilidad(sonda, servidor)
        # `C-6` y `DEC-026`: la salida se lee antes de cerrar el proceso, porque
        # tras el cierre el archivo temporal ya no se puede leer.
        salida_servidor = servidor.leer_salida()
    finally:
        servidor.cerrar()

    if memoria.get("codigo") != CODIGO_OK:
        print(
            "[ERROR] medición de memoria no disponible: la comparación no "
            "declara valores de memoria",
            file=sys.stderr,
        )
        return None
    return {
        "efectivas": efectivas,
        "carga": carga,
        "memoria": memoria,
        "sonda": sonda,
        "estabilidad": estabilidad,
        "salida_servidor": salida_servidor,
    }


def _identificador_de_registro(perfil, prueba, instante):
    """Identificador de `C-5` que `registro` compone para el instante recibido."""
    return f"{instante.strftime(registro.FORMATO_ID)}-{perfil}-{prueba}"


def _instante_de_registro_libre(directorio, perfil, prueba, instante):
    """Primer instante, desde el recibido, cuyo registro no existe todavía.

    `RNF-004` prohíbe sobrescribir: `registro.escribir_registro` resolvería 1
    colisión con el sufijo `-2` y el archivo declararía 1 identificador distinto
    del que el bloque de `C-7` cita como medición propuesta. La campaña elige el
    primer segundo libre, de modo que el bloque y el archivo declaran el mismo
    identificador sin sobrescribir ninguno.
    """
    candidato = instante
    while True:
        ruta = directorio / (
            _identificador_de_registro(perfil, prueba, candidato) + ".md"
        )
        if not ruta.exists():
            return candidato
        candidato += timedelta(seconds=1)


def _directorios_de_registros(raiz):
    """Carpetas `results/gemma/<perfil>/` bajo la raíz recibida, en orden."""
    base = Path(raiz) / RUTA_REGISTROS
    if not base.is_dir():
        return []
    return [ruta for ruta in sorted(base.glob("*")) if ruta.is_dir()]


def _es_prueba_de_alternativa(prueba):
    """Indica si la prueba nombra la alternativa de contexto menor de `T-041`."""
    nombre = (prueba or "").strip().lower()
    return nombre == PRUEBA_ALTERNATIVA_CONTEXTO or nombre.startswith(
        PRUEBA_ALTERNATIVA_CONTEXTO + "-"
    )


def _registro_de_alternativa(raiz, manifiesto, argumentos):
    """Lectura del registro de la alternativa de contexto menor, o `None`.

    `C-7` exige el registro de la alternativa de contexto menor cuando el eje es
    `ctx_size` con `131072` tokens; `T-041` lo mide con la prueba
    `alternativa-contexto-menor`, que puede declararse en el perfil comparado o
    en otro perfil bajo la misma raíz. La búsqueda no estima nada: sin registro,
    el bloque no se calcula y la comparación queda pendiente.
    """
    propio = _directorio_de_registros(raiz, manifiesto, argumentos)
    candidatos = [propio] + [
        directorio
        for directorio in _directorios_de_registros(raiz)
        if directorio != propio
    ]
    for directorio in candidatos:
        for ruta in sorted(directorio.glob("*.md"), reverse=True):
            try:
                lectura = comparar.leer_registro(ruta)
            except ValueError:
                continue
            if _es_prueba_de_alternativa(lectura["frontmatter"].get("prueba")):
                return lectura
    return None


def _ejecutar_comparacion(manifiesto, raiz, argumentos, desviacion):
    """Ejecuta las 2 mediciones reales de la comparación de 1 desviación.

    Mide el valor inicial y el valor propuesto del eje con el arranque del
    servidor, la espera de `/health`, la medición de memoria y la sonda de
    `DEC-011` de cada ejecución, y deja 1 registro con propósito ``comparacion``
    por medición en ``results/gemma/<perfil>/``. La segunda medición construye su
    registro en memoria y, antes de escribirlo, calcula el bloque de `C-7` con
    ``comparar.comparar`` desde las 2 lecturas, de modo que el bloque y el
    archivo nacen juntos y ningún registro previo se abre ni se sobrescribe
    (`RNF-004`). Devuelve el bloque, o `None` cuando la campaña no puede
    completarse —artefacto ausente, servidor que no queda en servicio, memoria
    no medible o bloque no calculable—; en ese caso ninguna cifra se estima y el
    modo reporta la comparación pendiente.
    """
    if not isinstance(desviacion, dict):
        return None
    parametro = (desviacion.get("parametro") or "").strip()
    if not parametro:
        return None
    valor_inicial = desviacion.get("valor_inicial")
    valor_propuesto = desviacion.get("valor_propuesto")
    if valor_inicial is None or valor_propuesto is None:
        print(
            f"[AVISO] comparación no medible: la desviación {parametro} no "
            "declara valor_inicial y valor_propuesto",
            file=sys.stderr,
        )
        return None

    ausente = _artefacto_ausente(manifiesto, raiz)
    if ausente is not None:
        print(
            f"[AVISO] comparación no medible: falta el artefacto {ausente}; "
            "las 2 mediciones no se ejecutan"
        )
        return None

    prueba = _prueba_de_comparacion(argumentos, parametro)
    perfil = manifiesto.get("id") or argumentos.perfil

    # 1ª medición: valor inicial, con su registro propio ya escrito.
    iniciales = _medicion_de_comparacion(
        manifiesto, raiz, argumentos, parametro, valor_inicial
    )
    if iniciales is None:
        return None
    construido_inicial, directorio = _construir_registro(
        manifiesto,
        raiz,
        argumentos,
        iniciales["efectivas"],
        iniciales["carga"],
        iniciales["memoria"],
        iniciales["sonda"],
        iniciales["estabilidad"],
        prueba=prueba,
        proposito=PROPOSITO_COMPARACION,
        instante=datetime.now(timezone.utc),
        salida_servidor=iniciales["salida_servidor"],
    )
    try:
        ruta_inicial = registro.escribir_registro(directorio, construido_inicial)
        lectura_inicial = comparar.leer_registro(ruta_inicial)
    except (OSError, ValueError) as error:
        print(
            f"[ERROR] registro de comparación no declarable: {error}",
            file=sys.stderr,
        )
        return None
    print(
        f"MEDICIÓN inicial: {parametro}={valor_inicial} "
        f"REGISTRO: {lectura_inicial['frontmatter']['id']}"
    )

    # 2ª medición: valor propuesto, con su registro todavía en memoria.
    propuestas = _medicion_de_comparacion(
        manifiesto, raiz, argumentos, parametro, valor_propuesto
    )
    if propuestas is None:
        return None
    construido_propuesto, _ = _construir_registro(
        manifiesto,
        raiz,
        argumentos,
        propuestas["efectivas"],
        propuestas["carga"],
        propuestas["memoria"],
        propuestas["sonda"],
        propuestas["estabilidad"],
        prueba=prueba,
        proposito=PROPOSITO_COMPARACION,
        instante=_instante_de_registro_libre(
            directorio, perfil, prueba, datetime.now(timezone.utc)
        ),
        salida_servidor=propuestas["salida_servidor"],
    )

    try:
        bloque = comparar.comparar(
            lectura_inicial,
            construido_propuesto,
            parametro=parametro,
            valor_inicial=valor_inicial,
            valor_propuesto=valor_propuesto,
            alternativa=_registro_de_alternativa(raiz, manifiesto, argumentos),
        )
    except ValueError as error:
        print(
            f"[ERROR] bloque de comparación no calculable: {error}",
            file=sys.stderr,
        )
        return None

    # `RNF-004`: el bloque viaja en la clave de `C-7` del registro nuevo y el
    # registro nacido en memoria es el único archivo que la campaña crea para el
    # valor propuesto.
    construido_propuesto["frontmatter"][registro.CLAVE_COMPARACION] = bloque
    try:
        ruta_propuesta = registro.escribir_registro(
            directorio, construido_propuesto
        )
    except (OSError, ValueError) as error:
        print(
            f"[ERROR] registro de comparación no declarable: {error}",
            file=sys.stderr,
        )
        return None
    print(
        f"MEDICIÓN propuesta: {parametro}={valor_propuesto} "
        f"REGISTRO: {ruta_propuesta.stem}"
    )
    return bloque


# Punto inyectable de la campaña de comparación: la suite sustituye este atributo
# de módulo por 1 callable con la misma firma, de modo que el modo `comparar` se
# prueba sin medir y la campaña real conserva su único punto de entrada.
EJECUTAR_COMPARACION = _ejecutar_comparacion


def _reportar_elegibilidad(manifiesto, registros):
    """Imprime la elegibilidad de `C-4` de `estado.elegible_para_aprobado`.

    La última carga es el registro con ``proposito`` igual a ``carga`` cuyo
    identificador es cronológicamente mayor; sin cargas la elegibilidad no se
    evalúa. Ninguna cifra se recalcula: el veredicto y el motivo son los de
    ``tools/gemma/estado.py``.
    """
    cargas = [
        identificador
        for identificador, lectura in registros.items()
        if (lectura.get("frontmatter") or {}).get("proposito") == "carga"
    ]
    if not cargas:
        print(
            "ELEGIBILIDAD: no evaluable: 0 registros declaran proposito «carga»"
        )
        return CODIGO_OK
    try:
        elegible, motivo = estado.elegible_para_aprobado(
            manifiesto, registros, max(cargas)
        )
    except ValueError as error:
        print(f"ELEGIBILIDAD: no evaluable: {error}")
        return CODIGO_USO_INCORRECTO
    print(
        "ELEGIBILIDAD: "
        + json.dumps(
            {"elegible": elegible, "motivo": motivo},
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return CODIGO_OK


def _comparar(manifiesto, raiz, argumentos):
    """Modo `comparar` de `DEC-008`: resuelve 1 desviación y reporta su estado.

    Exige ``--parametro`` —validado en ``main``—, exige que la clave nombre 1
    desviación del perfil, resuelve las opciones efectivas de `C-3` con
    ``perfiles.resolver_opciones`` sobre los registros del perfil y emite el
    aviso del eje omitido. Si la desviación no declara el bloque completo de
    `C-7`, ejecuta la campaña de ``EJECUTAR_COMPARACION``, que mide el valor
    inicial y el propuesto y deja sus 2 registros con propósito ``comparacion``;
    si lo declara, usa ese bloque y la elegibilidad de
    ``estado.elegible_para_aprobado`` sin recalcular cifras. Las opciones
    efectivas de las ejecuciones de servicio no cambian: la campaña no edita el
    manifiesto, de modo que la desviación sigue sin comparación declarada hasta
    que el propietario la registre.
    """
    parametro = (argumentos.parametro or "").strip()
    desviacion = _desviacion_de(manifiesto, parametro)
    if desviacion is None:
        print(
            f"[ERROR] desviación no declarada: {parametro}; --parametro debe "
            "nombrar 1 eje de desviaciones del perfil",
            file=sys.stderr,
        )
        return CODIGO_USO_INCORRECTO

    try:
        registros = _leer_registros(raiz, manifiesto, argumentos)
    except ValueError as error:
        print(f"[ERROR] registro de comparación ilegible: {error}", file=sys.stderr)
        return CODIGO_USO_INCORRECTO

    efectivas = perfiles.resolver_opciones(manifiesto, registros)
    _imprimir_opciones_efectivas(efectivas)

    bloque = _bloque_registrado(registros, desviacion)
    if bloque is None:
        bloque = EJECUTAR_COMPARACION(manifiesto, raiz, argumentos, desviacion)

    if bloque is None:
        print(
            f"COMPARACIÓN: {parametro} sin bloque de C-7 registrado; se aplica "
            "el valor inicial de C-2 a lo que sirve y la comparación queda "
            "pendiente de la campaña de medición"
        )
        return CODIGO_OK

    print("COMPARACIÓN: " + json.dumps(bloque, ensure_ascii=False, sort_keys=True))
    return _reportar_elegibilidad(manifiesto, registros)


def _servir_o_medir(manifiesto, raiz, argumentos, escenario=None):
    """Modos `servir` y `medir`: carga medida del perfil de `C-1`.

    Sigue el flujo de una ejecución de `plan.md`: comprobación previa completa,
    opciones efectivas de `C-3`, lanzamiento con esas opciones, espera de la
    salud con el tiempo de carga, medición de memoria, sonda cuando la prueba la
    requiere, lectura de la salida capturada del servidor y cierre del proceso.
    Las opciones efectivas se resuelven 1 sola vez, con los registros disponibles
    en ``results/gemma/<perfil>/``, y ese mismo resultado alimenta la
    comprobación 4 y el lanzamiento, de modo que el presupuesto se contrasta con
    el contexto que el servidor usa. Solo `medir` escribe el registro de `C-5`;
    `servir` deja 0 registros y declara el campo 22 como fuente ausente.

    Con ``escenario``, la ejecución aplica los 9 valores del escenario del
    catálogo en lugar de los ejes del perfil: declara el identificador en
    consola, ejecuta el precheck de recursos de `C-4` por
    ``VERIFICAR_RECURSOS_ESCENARIO`` antes de arrancar y recalcula el contexto
    ajustado con la VRAM libre del lanzamiento (`CB-005`). El registro de
    `medir` transcribe además el bloque de conformidad presupuestaria de `C-5`
    de `SPEC-018`.
    """
    # `C-3` y `DEC-008`: el valor efectivo de cada eje es el inicial mientras su
    # desviación no declare 1 comparación completa y pasa a ser el propuesto en
    # cuanto esa comparación consta entre los registros del perfil.
    efectivas_perfil = _opciones_efectivas(manifiesto, raiz, argumentos)

    if escenario is not None:
        # `C-2` y `C-4`: el escenario se anuncia y su precheck de recursos
        # aborta con el código 3 antes de lanzar nada.
        _anunciar_escenario(escenario)
        codigo_escenario = _verificar_recursos_del_escenario(escenario)
        if codigo_escenario != CODIGO_OK:
            return codigo_escenario

    codigo = _comprobacion_previa(manifiesto, raiz, efectivas_perfil)
    if codigo != CODIGO_OK:
        return codigo

    if escenario is None:
        efectivas = efectivas_perfil
    else:
        efectivas, motivo = _efectivas_del_escenario(escenario)
        if efectivas is None:
            print(f"[FALLO] {motivo}", file=sys.stderr)
            return CODIGO_PRECHECK_ESCENARIO

    _imprimir_opciones_efectivas(efectivas)

    ejecutable = _ruta_ejecutable(manifiesto, raiz)
    argumentos_servidor = _argumentos_del_servidor(
        manifiesto, raiz, efectivas["opciones"]
    )
    # `C-6`: el tiempo de carga se cuenta desde el lanzamiento del servidor.
    iniciar = time.monotonic()
    try:
        servidor = LANZAR_SERVIDOR(ejecutable, argumentos_servidor)
    except (OSError, ValueError) as error:
        print(f"[ERROR] no se pudo lanzar el servidor: {error}", file=sys.stderr)
        return CODIGO_MEDICION_NO_DISPONIBLE

    sonda = None
    segundos_sonda = None
    try:
        carga, motivo = _esperar_salud(servidor, iniciar)
        if carga is None:
            print(
                f"[ERROR] el servidor no quedó en servicio: {motivo}",
                file=sys.stderr,
            )
            return CODIGO_MEDICION_NO_DISPONIBLE
        memoria = MEDIR_MEMORIA([servidor.pid])
        if argumentos.modo == MODO_MEDIR and _requiere_sonda(argumentos.prueba):
            # `T-073`: el tiempo se mide alrededor de la sonda y se declara en la
            # línea `SONDA:` junto al conteo del resultado, antes del registro.
            inicio_sonda = time.monotonic()
            sonda = SONDEAR(f"{URL_BASE.rstrip('/')}:{PUERTO}")
            segundos_sonda = time.monotonic() - inicio_sonda
        estabilidad = _estabilidad(sonda, servidor)
        # `C-6` y `DEC-026`: el campo 22 toma la memoria de expertos en host de
        # la salida capturada, que se lee antes de cerrar el proceso.
        salida_servidor = servidor.leer_salida()
    finally:
        servidor.cerrar()

    if memoria.get("codigo") != CODIGO_OK:
        print(
            "[ERROR] medición de memoria no disponible: la ejecución no declara "
            "valores de memoria",
            file=sys.stderr,
        )
        return CODIGO_MEDICION_NO_DISPONIBLE

    print(
        f"SERVIDOR: cerrado tras {carga:.2f} s de carga en "
        f"{URL_BASE.rstrip('/')}:{PUERTO}"
    )
    print(
        "MEMORIA: "
        f"VRAM total {memoria.get('vram_total_mib')} MiB, "
        f"usada {memoria.get('vram_usada_mib')} MiB, "
        f"libre {memoria.get('vram_libre_mib')} MiB, "
        f"residente {memoria.get('residente_mib')} MiB, "
        f"desbordamiento {memoria.get('desbordamiento_mib')} MiB"
    )
    print(f"ESTABILIDAD: {estabilidad}")

    # `T-073` y `CB-003`: el conteo de la sonda se imprime antes de la línea del
    # registro de `C-5`, sin cambiar ni el registro ni el código de `C-8`.
    if argumentos.modo == MODO_MEDIR and sonda is not None:
        print(_linea_sonda(sonda, segundos_sonda))

    if argumentos.modo == MODO_SERVIR:
        return CODIGO_OK

    bloque_escenario = None
    if escenario is not None:
        # `C-5` de `SPEC-018`: el bloque declara el identificador, el
        # presupuesto del escenario y las 2 mediciones de VRAM; `registro`
        # deriva el delta y el dictamen de conformidad.
        bloque_escenario = _bloque_de_conformidad(escenario, memoria)

    try:
        _crear_registro(
            manifiesto,
            raiz,
            argumentos,
            efectivas,
            carga,
            memoria,
            sonda,
            estabilidad,
            salida_servidor,
            escenario=bloque_escenario,
        )
    except ValueError as error:
        print(f"[ERROR] registro no declarable: {error}", file=sys.stderr)
        return CODIGO_USO_INCORRECTO
    return CODIGO_OK


def main(argv=None):
    """Ejecuta la línea de comandos de `C-8` y devuelve su código de salida."""
    parser = _crear_parser()
    try:
        argumentos = parser.parse_args(argv)
    except SystemExit:
        # argparse termina por `SystemExit` ante 1 argumento mal formado; el
        # código de uso incorrecto de `C-8` se devuelve en lugar de propagarse.
        return CODIGO_USO_INCORRECTO

    raiz = Path(argumentos.raiz).resolve()

    # `SPEC-018` y `C-2`: el listado de escenarios no exige `--perfil` y
    # devuelve el código 0 sin lanzar el servidor.
    if argumentos.listar_escenarios:
        try:
            return _listar_escenarios(raiz)
        except ValueError as error:
            print(
                f"[ERROR] catálogo de escenarios no disponible: {error}",
                file=sys.stderr,
            )
            return CODIGO_USO_INCORRECTO

    identificadores = _perfiles_disponibles(raiz)

    if argumentos.modo not in MODOS:
        print(
            f"[ERROR] modo no admitido: {argumentos.modo}; "
            f"--modo admite {'|'.join(MODOS)}",
            file=sys.stderr,
        )
        return CODIGO_USO_INCORRECTO

    # `SPEC-018` y `C-2`: sin `--perfil` ni `--escenario` el flujo interactivo
    # resuelve primero el escenario del catálogo y después el perfil de base; con
    # varios perfiles y sin consola, el listado de `DEC-001` se conserva.
    escenario = None
    if argumentos.perfil is None:
        if argumentos.escenario or not _entrada_interactiva(identificadores):
            _listar_perfiles(raiz, identificadores)
            return CODIGO_USO_INCORRECTO
        try:
            catalogo = _cargar_catalogo(raiz)
        except ValueError as error:
            print(
                f"[ERROR] catálogo de escenarios no disponible: {error}",
                file=sys.stderr,
            )
            return CODIGO_USO_INCORRECTO
        escenario = _seleccionar_escenario(catalogo)
        if escenario is None:
            return CODIGO_USO_INCORRECTO
        identificador = _seleccionar_perfil(raiz, identificadores)
        if identificador is None:
            return CODIGO_USO_INCORRECTO
        argumentos.perfil = identificador
    else:
        if argumentos.perfil not in identificadores:
            print(
                f"[ERROR] perfil no declarado: {argumentos.perfil}",
                file=sys.stderr,
            )
            return CODIGO_USO_INCORRECTO

        # `RF-004` y `C-2`: el identificador de escenario se contrasta con el
        # catálogo antes de resolver los argumentos del modo; 1 identificador
        # ausente devuelve el código 2 y enumera los 9 canónicos.
        if argumentos.escenario:
            try:
                catalogo = _cargar_catalogo(raiz)
            except ValueError as error:
                print(
                    f"[ERROR] catálogo de escenarios no disponible: {error}",
                    file=sys.stderr,
                )
                return CODIGO_USO_INCORRECTO
            escenario = _escenario_declarado(catalogo, argumentos.escenario)
            if escenario is None:
                _rechazar_escenario_inexistente(catalogo, argumentos.escenario)
                return CODIGO_USO_INCORRECTO

    if argumentos.modo == MODO_COMPARAR and argumentos.parametro is None:
        print(
            "[ERROR] argumento ausente: --parametro <clave> es obligatorio en "
            "--modo comparar",
            file=sys.stderr,
        )
        return CODIGO_USO_INCORRECTO

    if argumentos.modo == MODO_MEDIR and not (argumentos.prueba or "").strip():
        print(
            "[ERROR] argumento ausente: --prueba <nombre> es obligatorio en "
            "--modo medir",
            file=sys.stderr,
        )
        return CODIGO_USO_INCORRECTO

    manifiesto = _leer_manifiesto(raiz, argumentos.perfil)

    if argumentos.modo == "comprobar":
        if escenario is not None:
            return _comprobar_escenario(escenario)
        return _comprobar(manifiesto, raiz, argumentos)

    if argumentos.modo in (MODO_SERVIR, MODO_MEDIR):
        return _servir_o_medir(manifiesto, raiz, argumentos, escenario)

    return _comparar(manifiesto, raiz, argumentos)


# Puntos inyectables de la suite, conforme a `DEC-012`: la medición de memoria,
# la consulta de VRAM libre de solo lectura, la sonda, la ejecución del binario y
# el precheck de recursos del escenario se sustituyen por dobles sin opciones de
# línea de comandos fuera de `C-2` y `C-8`.
MEDIR_MEMORIA = medir.medir_memoria
VRAM_LIBRE_MIB = medir.vram_libre_mib
SONDEAR = probe.sondear
LANZAR_SERVIDOR = _lanzar_servidor
VERIFICAR_RECURSOS_ESCENARIO = precheck.verificar_recursos_escenario


if __name__ == "__main__":
    raise SystemExit(main())
