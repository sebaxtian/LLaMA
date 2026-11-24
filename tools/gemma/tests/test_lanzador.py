"""Pruebas en rojo del lanzador y orquestador de SPEC-017.

Fijan la interfaz de `tools/gemma/lanzador.py` para `RF-001` y `CB-001`
conforme a `C-8`, `DEC-001`, `DEC-012` y `DEC-015`:

- `main(argv=None) -> int` devuelve el código de salida de `C-8` en lugar de
  terminar por `sys.exit`, de modo que la suite puede comprobarlo sin capturar
  `SystemExit`.
- Sin `--perfil`, imprime la lista de los 3 identificadores de perfil
  disponibles, en orden alfabético, y devuelve `2` sin lanzar el servidor.
- Con 1 `--perfil` inexistente, o con el directorio de perfiles sin
  manifiestos, imprime `[ERROR] perfil no declarado: <id>` y devuelve `2`.
- Con `--modo` fuera de `comprobar`, `servir`, `medir` y `comparar`, imprime el
  mensaje de uso y devuelve `2`.
- Sin `--raiz`, la raíz del repositorio se resuelve desde la ubicación del
  módulo con `Path(__file__).resolve().parents[2]`, que es el directorio que
  contiene `tools/`, y no desde el directorio actual; la raíz derivada es
  absoluta y sin tramos relativos.
- El modo `comprobar` inyecta en la comprobación previa el mapa de opciones que
  `binario.opciones_aceptadas` deriva de la ayuda del binario, consultado sobre
  la ruta de `artefactos.ejecutable` resuelta contra la raíz, y la VRAM libre en
  MiB que informa la consulta de solo lectura `medir.vram_libre_mib` por el
  punto inyectable `VRAM_LIBRE_MIB`: con el bloque `presupuesto_vram` completo
  la comprobación 4 se resuelve `SUPERADA` o `FALLIDA`, y sin la consulta
  disponible queda `PENDIENTE` con su motivo, conforme a `DEC-018`.
- El modo `comprobar` sobre 1 árbol temporal sin artefactos devuelve `4`, que es
  el código de artefacto requerido ausente de `C-8`, y no lanza el servidor: la
  consulta fallida de la ayuda deja el mapa en `None` y no propaga excepción.
- `--modo comparar` sin `--parametro` imprime el mensaje de argumento ausente y
  devuelve `2`. Con `--parametro`, resuelve las opciones efectivas de `C-3` con
  `perfiles.resolver_opciones`; si la desviación no declara el bloque completo de
  `C-7`, aplica el valor inicial, emite el aviso del eje omitido y deja intactas
  las opciones efectivas de las ejecuciones de servicio. Con el bloque
  registrado, usa ese bloque y la elegibilidad de `estado.elegible_para_aprobado`
  sin recalcular cifras. La ejecución de las 2 mediciones reales queda en el
  punto inyectable `EJECUTAR_COMPARACION`, que `T-038` a `T-042` sustituyen.
- `--modo medir` deja 1 registro cuyo campo 22 «Memoria de expertos en host»
  toma el valor en MiB de la primera línea `CUDA_Host model buffer size` del
  modelo principal en la salida capturada del servidor —la del draft no se suma—
  y declara `no disponible` cuando esa línea falta, conforme a `DEC-026`.

Las 7 primeras pruebas fijan el módulo `tools/gemma/lanzador.py` con dobles: los
árboles temporales se construyen con `tempfile` bajo `tmp/` y la comprobación
previa se sustituye por 1 doble, de modo que no leen `bin/`, no leen `models/` y
no lanzan el servidor, conforme a `DEC-012`. Las 2 pruebas de `T-018` acreditan
el lanzador `.bat` de `DEC-014` y `DEC-015`: `test_bat_desde_directorio_ajeno`
invoca el archivo real con `subprocess` desde 1 directorio temporal que contiene
1 señuelo en la ruta relativa de los pesos, bajo `skipUnless` de la existencia
de los 4 artefactos locales, y `test_bat_sin_cabecera_de_produccion` comprueba
el contenido del archivo sin ejecutarlo.
"""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"

# Los 3 identificadores de perfil disponibles, en orden alfabético.
PERFILES_ESPERADOS = ("rendimiento", "resiliencia", "sin_especulativa")

# Los 4 modos admitidos por `C-8` y ningún otro.
MODOS_ADMITIDOS = ("comprobar", "servir", "medir", "comparar")

# Códigos de `C-8` que esta suite pone a prueba: uso incorrecto y artefacto
# requerido ausente.
CODIGO_USO_INCORRECTO = 2
CODIGO_ARTEFACTO_AUSENTE = 4

# Estados sintéticos de `C-9` con 1 comprobación pendiente, que es la forma que
# declara el perfil real mientras su bloque `presupuesto_vram` conserve la clave
# `pendiente` conforme a `DEC-018`.
ESTADOS_SINTETICOS = ("SUPERADA", "SUPERADA", "SUPERADA", "PENDIENTE", "SUPERADA")

# Forma que el binario enumera para cada eje de `C-2`, según el doble de `T-014`,
# con los 9 ejes de `DEC-028` en el orden de `C-2`.
OPCIONES_ACEPTADAS = {
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

# `T-065`: banderas fijas del lanzamiento que no son ejes de `C-2`. Las 5 del
# modelo, el proyector y el punto de acceso; las 2 del bloque `especulativa` de
# `DEC-024`, que la ayuda del binario enumera y el contrato `C-6` registra en su
# fila 11; y `--log-verbosity`, que es 1 bandera de registro y no 1 eje del
# perfil, de modo que no entra en la resolución de `C-3` ni en la huella de
# `DEC-020`. La guardia del conjunto la admite junto a las anteriores.
BANDERAS_FIJAS = (
    "--model",
    "--mmproj",
    "--host",
    "--port",
    "--model-draft",
    "--spec-type",
    "--spec-draft-n-max",
    "--log-verbosity",
)

# Lanzador `.bat` de `DEC-014`, sustituido en su misma ruta.
LANZADOR_BAT = RAIZ / "src" / "gemma" / "unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat"

# Directorio del modelo dentro de `models/` y 4 artefactos que los perfiles con
# borrador declaran en `C-1`; sin ellos la ejecución real se omite.
DIRECTORIO_MODELO = "models/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF"
ARTEFACTOS_REALES = (
    RAIZ / "bin" / "llama-master-bin-win-rtx5060ti-cuda-13.5-x64" / "llama-server.exe",
    RAIZ / DIRECTORIO_MODELO / "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf",
    RAIZ / DIRECTORIO_MODELO / "mmproj-BF16.gguf",
    RAIZ / DIRECTORIO_MODELO / "mtp-gemma-4-26B-A4B-it-Q4_0.gguf",
)

# Ruta relativa del archivo de pesos: el señuelo del directorio temporal se
# escribe ahí para demostrar que el `.bat` no resuelve artefactos desde el
# directorio actual, conforme a `RF-001` y `CB-001`.
RUTA_RELATIVA_PESOS = DIRECTORIO_MODELO + "/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf"

# Etiquetas de las 3 vías de `DEC-015`; la línea `Intérprete:` nombra 1.
VIAS_INTERPRETE = ("LLAMA_PYTHON", "py -3", "LOCALAPPDATA")

# Mediciones sintéticas de la campaña de comparación de `T-049`: la propuesta
# asigna 100 MiB más de VRAM, deja 49 MiB menos libres y usa 40 MiB más de RAM,
# de modo que las 3 diferencias de memoria de `C-7` tienen signo propio. Las
# cifras son sintéticas y 0 valores provienen de la máquina objetivo.
MEMORIA_INICIAL = {
    "codigo": 0,
    "vram_total_mib": 16376,
    "vram_usada_mib": 14200,
    "vram_libre_mib": 1449,
    "residente_mib": 2410,
    "desbordamiento_mib": 0,
}

MEMORIA_PROPUESTA = {
    "codigo": 0,
    "vram_total_mib": 16376,
    "vram_usada_mib": 14300,
    "vram_libre_mib": 1400,
    "residente_mib": 2450,
    "desbordamiento_mib": 0,
}

# Resultado sintético de la sonda de `DEC-011`: `C-6` toma de su bloque de
# tiempos la velocidad de generación de la fila 17 y, cuando la informa, la de
# prompt de la fila 16.
SONDA_INICIAL = {
    "estado": "superada",
    "fragmentos": 2400,
    "tokens_generados": 2400,
    "tokens_por_segundo": 90.0,
    "velocidad_prompt_tokens_por_segundo": 80.0,
    "servidor": "continúa en servicio",
}

SONDA_PROPUESTA = {
    "estado": "superada",
    "fragmentos": 2400,
    "tokens_generados": 2400,
    "tokens_por_segundo": 93.25,
    "velocidad_prompt_tokens_por_segundo": 84.5,
    "servidor": "continúa en servicio",
}

# Las 5 diferencias de `C-7` del par sintético: propuesta menos inicial.
DIFERENCIAS_UBATCH = {
    "delta_velocidad_generacion_tokens_por_segundo": 3.25,
    "delta_velocidad_prompt_tokens_por_segundo": 4.5,
    "delta_vram_asignada_mib": 100,
    "delta_vram_libre_mib": -49,
    "delta_ram_mib": 40,
}

# Eje comparado por `T-049` y sus 2 valores: inicial de `C-2` y propuesto por el
# perfil `rendimiento`.
PARAMETRO_COMPARADO = "ubatch"
VALOR_INICIAL_COMPARADO = 512
VALOR_PROPUESTO_COMPARADO = 1120
PRUEBA_COMPARADA = "comparacion-ubatch"

# `T-083`: comparación que el perfil `rendimiento` cita para `ncmoe` —el registro
# propuesto de `T-082`, que midió el valor `9`— y cuyo bloque completo de `C-7` la
# campaña de `ubatch` hereda.
COMPARACION_NCMOE = "20261124T191126Z-rendimiento-comparacion-ncmoe"
NCMOE_ADOPTADO = 9

# Cierre de `C-9` con el bloque `presupuesto_vram` del perfil completo y la VRAM
# libre real de la máquina, y cierre con la comprobación 4 resuelta `FALLIDA`
# cuando esa VRAM no alcanza el presupuesto; `PENDIENTE` deja de ser admisible
# en cuanto el bloque está completo, conforme a `DEC-018`.
CIERRE_COMPLETO = "COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas"
CIERRE_FALLIDO = "COMPROBACIÓN PREVIA: 4 de 5 comprobaciones superadas"

# Plazo de la ejecución real: la consulta de ayuda del binario es la parte lenta.
PLAZO_SEGUNDOS = 300

# Presupuesto medido del bloque `presupuesto_vram` de 4 claves de `T-077`, con la
# medición de `T-076` —`q8_0` y `flash_attn on` a `4096`: `12488.33` MiB de pesos,
# `10.625` MiB de caché no-SWA por `1024` tokens, `159.38` MiB de caché SWA fija y
# `538.40` MiB de buffer de cómputo—, es decir `13228.61` MiB con `4096` tokens
# efectivos. Los casos que ejercitan la comprobación 4 con 1 bloque completo lo
# construyen con estos valores medidos y 0 se estiman.
PRESUPUESTO_MEDIDO = {
    "pesos_en_vram_mib": 12488.33,
    "kv_no_swa_por_1024_tokens_mib": 10.625,
    "kv_swa_mib": 159.38,
    "buffer_computo_mib": 538.40,
}


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/lanzador.py` no
    exista, que es el rojo declarado de `T-016`; `T-017` cierra el caso. No se
    crea `tools/gemma/__init__.py`: el módulo se importa como `lanzador` con el
    directorio `tools/gemma/` en `sys.path`, igual que `test_precheck.py` y
    `test_perfiles.py`.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import lanzador

    return lanzador


def _manifiesto_de_perfil(nombre):
    """Lee 1 manifiesto versionado de `src/gemma/perfiles/`."""
    ruta = DIRECTORIO_PERFILES / nombre
    return json.loads(ruta.read_text(encoding="utf-8"))


def _resultado_sintetico():
    """Resultado con la forma de `C-9`, sin ejecutar ninguna comprobación."""
    return {
        "comprobaciones": [
            {"numero": numero, "estado": estado, "detalle": f"detalle {numero}"}
            for numero, estado in enumerate(ESTADOS_SINTETICOS, start=1)
        ],
        "codigo": 0,
        "milisegundos": 0,
    }


class _VramLibreDoble:
    """Doble de `VRAM_LIBRE_MIB`: informa la VRAM libre sin consultar la GPU.

    El modo `comprobar` pasa ese valor a `precheck.ejecutar` en
    `vram_disponible_mib`; con el doble, ningún caso de la suite invoca
    `nvidia-smi`, conforme a `DEC-012`.
    """

    def __init__(self, valor=16376.0):
        self.valor = valor
        self.llamadas = 0

    def __call__(self):
        self.llamadas += 1
        return self.valor


class _EjecutarDoble:
    """Doble de `precheck.ejecutar` que registra la raíz recibida.

    El modo `comprobar` no lanza el servidor ni carga el modelo, y este doble
    impide además que la prueba lea los artefactos reales del repositorio.
    """

    def __init__(self):
        self.llamadas = []

    def raiz_recibida(self):
        """Devuelve la raíz de la primera llamada, o `None` si no hubo llamada."""
        if not self.llamadas:
            return None
        return self.llamadas[0]["raiz"]

    def __call__(self, *args, **kwargs):
        raiz = kwargs.get("raiz")
        if raiz is None and len(args) > 1:
            raiz = args[1]
        self.llamadas.append({"args": args, "kwargs": kwargs, "raiz": raiz})
        return _resultado_sintetico()


# `T-061`: registro sintético del servidor con la línea `CUDA_Host model buffer
# size` del modelo principal primero y la del draft después, de modo que el campo
# 22 toma solo la del modelo y no suma la del borrador, conforme a `DEC-026`.
LOG_SERVIDOR = "\n".join(
    (
        "load_model: initializing, n_slots = 1, n_ctx_slot = 4096",
        "load_tensors: loading model tensors",
        "load_tensors: CUDA0 model buffer size = 11123.66 MiB",
        "load_tensors: CUDA_Host model buffer size = 2846.25 MiB",
        "load_tensors: CPU model buffer size = 12.00 MiB",
        "load_tensors: loading model tensors for the draft",
        "load_tensors: CUDA0 model buffer size = 225.21 MiB",
        "load_tensors: CUDA_Host model buffer size = 96.50 MiB",
        "srv  update_slots: all slots are idle",
    )
) + "\n"

# El mismo registro sin la línea del modelo principal: el campo 22 declara la
# marca de fuente ausente y ningún valor se estima.
LOG_SIN_EXPERTOS = "\n".join(
    (
        "load_model: initializing, n_slots = 1, n_ctx_slot = 4096",
        "load_tensors: CUDA0 model buffer size = 11123.66 MiB",
        "load_tensors: CPU model buffer size = 12.00 MiB",
        "srv  update_slots: all slots are idle",
    )
) + "\n"

# Valor del campo 22 que fija el registro sintético: el del modelo principal.
MEMORIA_EXPERTOS_HOST = "2846.25 MiB"


class _ServidorDoble:
    """Doble del servidor lanzado: identificador, actividad, salida y cierre.

    Registra que se cerró para que el caso acredite que cada medición de la
    campaña cierra su propio servidor antes de la siguiente. ``leer_salida``
    devuelve el registro sintético del binario, que es la fuente del campo 22 de
    `C-6`, sin ejecutar el servidor real.
    """

    def __init__(self, pid, salida=""):
        self.pid = pid
        self.cerrado = False
        self._salida = salida
        self.lecturas = 0

    def activo(self):
        """Indica que el proceso sigue en ejecución hasta que se cierra."""
        return not self.cerrado

    def leer_salida(self):
        """Devuelve el texto capturado del binario, sin cerrar el proceso."""
        self.lecturas += 1
        return self._salida

    def cerrar(self):
        """Marca el servidor como cerrado."""
        self.cerrado = True


class _LanzarDoble:
    """Doble de `LANZAR_SERVIDOR` que registra ejecutable, argumentos y cierres."""

    def __init__(self, pid=4321, salida=LOG_SERVIDOR):
        self.llamadas = []
        self.servidores = []
        self._pid = pid
        self._salida = salida

    def __call__(self, ejecutable, argumentos):
        self.llamadas.append(
            {
                "ejecutable": Path(ejecutable),
                "argumentos": [str(argumento) for argumento in argumentos],
            }
        )
        servidor = _ServidorDoble(self._pid, self._salida)
        self.servidores.append(servidor)
        return servidor

    def valores_de(self, forma):
        """Valor que cada lanzamiento declaró para la forma larga indicada."""
        valores = []
        for llamada in self.llamadas:
            argumentos = llamada["argumentos"]
            if forma not in argumentos:
                valores.append(None)
                continue
            valores.append(argumentos[argumentos.index(forma) + 1])
        return valores


class _MedirDoble:
    """Doble de `MEDIR_MEMORIA` que devuelve 1 medición sintética por llamada."""

    def __init__(self, mediciones):
        self.mediciones = list(mediciones)
        self.llamadas = []

    def __call__(self, pids, **kwargs):
        self.llamadas.append({"pids": list(pids), "kwargs": dict(kwargs)})
        indice = min(len(self.llamadas), len(self.mediciones)) - 1
        return dict(self.mediciones[indice])


class _SondaDoble:
    """Doble de `SONDEAR` que devuelve 1 resultado sintético por llamada."""

    def __init__(self, resultados):
        self.resultados = list(resultados)
        self.llamadas = []

    def __call__(self, base_url, **kwargs):
        self.llamadas.append({"base_url": base_url, "kwargs": dict(kwargs)})
        indice = min(len(self.llamadas), len(self.resultados)) - 1
        return dict(self.resultados[indice])


def _respuesta_de_salud():
    """Respuesta sintética de `GET /health`, sin abrir socket.

    `urllib.request.urlopen` es la consulta que el lanzador hace a la ruta
    `/health`; su doble devuelve `200` con el cuerpo `ok`, de modo que la espera
    de la salud de cada medición no toca la red ni el servidor real.
    """
    respuesta = mock.MagicMock()
    respuesta.status = 200
    respuesta.read.return_value = b'{"status": "ok"}'
    respuesta.__enter__.return_value = respuesta
    respuesta.__exit__.return_value = False
    return respuesta


class LanzadorTest(unittest.TestCase):
    """Fija la línea de comandos y los códigos de salida de `C-8`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    def _ejecutar_main(self, argumentos):
        """Invoca `main` capturando las 2 salidas y devuelve el código real."""
        modulo = _cargar_modulo()
        salida = io.StringIO()
        errores = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = modulo.main(argumentos)
        self.assertIsInstance(
            codigo,
            int,
            "main devuelve el código de C-8 como entero y no termina por sys.exit",
        )
        return codigo, salida.getvalue(), errores.getvalue()

    def _texto(self, salida, errores):
        """Une las 2 salidas porque el mensaje puede ir a cualquiera de ellas."""
        return salida + errores

    def _crear_arbol(self, manifiestos=("rendimiento.json",), artefactos=False):
        """Crea 1 raíz temporal con sus manifiestos y, si se pide, sus artefactos.

        Las rutas relativas de `artefactos` se resuelven contra la raíz temporal
        que recibe `--raiz`, de modo que ningún caso toca `bin/` ni `models/`.
        """
        directorio = self.raiz / "src" / "gemma" / "perfiles"
        directorio.mkdir(parents=True, exist_ok=True)
        for nombre in manifiestos:
            (directorio / nombre).write_text(
                json.dumps(_manifiesto_de_perfil(nombre), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if artefactos:
            for nombre in manifiestos:
                manifiesto = _manifiesto_de_perfil(nombre)
                for relativa in manifiesto["artefactos"].values():
                    if relativa is None:
                        continue
                    ruta = self.raiz / relativa
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                    ruta.write_bytes(b"artefacto sintetico")
        return directorio

    def _sustituir_comprobacion_previa(self):
        """Sustituye las dependencias que leerían artefactos del repositorio.

        `precheck.ejecutar`, `binario.opciones_aceptadas`, `binario.leer_version`
        y `VRAM_LIBRE_MIB` son las 4 funciones que el modo `comprobar` invoca
        sobre rutas del árbol o sobre la GPU; con estos dobles la prueba de la
        raíz por defecto no lee `bin/` ni `models/` ni consulta `nvidia-smi`,
        conforme a `DEC-012`.
        """
        import binario
        import precheck

        doble = _EjecutarDoble()
        pila = contextlib.ExitStack()
        self.addCleanup(pila.close)
        pila.enter_context(mock.patch.object(precheck, "ejecutar", doble))
        pila.enter_context(
            mock.patch.object(
                binario,
                "opciones_aceptadas",
                lambda ejecutable: dict(OPCIONES_ACEPTADAS),
            )
        )
        pila.enter_context(
            mock.patch.object(
                binario,
                "leer_version",
                lambda ejecutable: {"version": "sintetica", "commit": "sintetico"},
            )
        )
        modulo = _cargar_modulo()
        pila.enter_context(
            mock.patch.object(modulo, "VRAM_LIBRE_MIB", _VramLibreDoble())
        )
        if hasattr(modulo, "ejecutar"):
            pila.enter_context(mock.patch.object(modulo, "ejecutar", doble))
        return doble

    def _sustituir_vram_libre(self, valor=16376.0):
        """Sustituye `VRAM_LIBRE_MIB` por 1 doble que no consulta la GPU.

        Devuelve el doble para que el caso acredite que la consulta se usó 1
        sola vez; con él, la comprobación 4 se contrasta con 1 valor declarado y
        ningún caso invoca `nvidia-smi`, conforme a `DEC-012`.
        """
        modulo = _cargar_modulo()
        doble = _VramLibreDoble(valor)
        pila = contextlib.ExitStack()
        self.addCleanup(pila.close)
        pila.enter_context(mock.patch.object(modulo, "VRAM_LIBRE_MIB", doble))
        return doble

    def _ruta_manifiesto(self, nombre="rendimiento"):
        """Ruta del manifiesto copiado al árbol temporal."""
        return self.raiz / "src" / "gemma" / "perfiles" / f"{nombre}.json"

    def _leer_manifiesto_del_arbol(self, nombre="rendimiento"):
        """Lee del árbol temporal el manifiesto copiado por `_crear_arbol`."""
        ruta = self._ruta_manifiesto(nombre)
        return ruta, json.loads(ruta.read_text(encoding="utf-8"))

    def _escribir_manifiesto(self, ruta, manifiesto):
        """Serializa el manifiesto con la forma de `C-1` en el árbol temporal."""
        ruta.write_text(
            json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _campos_de_c6(self):
        """Mapa de las 22 etiquetas de `C-6` a su texto conforme."""
        return {
            "Fecha de la prueba": "2026-11-22",
            "Nombre de la prueba": "prueba sintetica",
            "Versión del binario": "sintetica",
            "Commit de llama.cpp": "sintetico",
            "Modelo y cuantización": "Gemma-4-26B-A4B-it-qat-GGUF UD-Q4_K_XL",
            "Contexto configurado": "4096 tokens",
            "Ranuras del servidor": "1 ranuras",
            "Capas de expertos en CPU": "0 capas",
            "Micro-lote": "512 tokens",
            "Atención rápida": "desactivado",
            "Decodificación especulativa": "activado (techo de borrador 3 tokens)",
            "Tiempo de carga": "6.30 s",
            "VRAM asignada": "14200 MiB",
            "VRAM libre": "1449 MiB",
            "RAM utilizada": "2410 MiB",
            "Velocidad de prompt": "9.81 tokens/s",
            "Velocidad de generación": "94.89 tokens/s",
            "Estabilidad del servidor": "continúa en servicio",
            "Desbordamiento hacia memoria compartida": "0 MiB",
            "Calidad funcional de la respuesta": "sintetica",
            "Errores y advertencias": "sin errores",
            "Memoria de expertos en host": MEMORIA_EXPERTOS_HOST,
        }

    def _escribir_registro(self, manifiesto, prueba, proposito, instante):
        """Escribe 1 registro de `C-5` en el árbol temporal y devuelve su ruta.

        La huella es la de las `opciones` declaradas del manifiesto, conforme a
        `DEC-020`, de modo que la elegibilidad de `estado` puede contrastarla.
        """
        import perfiles
        import registro

        frontmatter = {
            "huella_opciones": perfiles.huella_opciones(manifiesto["opciones"]),
            "opciones_efectivas": dict(manifiesto["opciones"]),
            "vram_total_mib": 16376,
            "version_binario": "sintetica",
            "commit_llama_cpp": "sintetico",
            "registro_anterior": None,
        }
        construido = registro.construir_registro(
            manifiesto["id"],
            prueba,
            proposito,
            frontmatter,
            self._campos_de_c6(),
            instante=instante,
        )
        directorio = self.raiz / "results" / "gemma" / manifiesto["id"]
        return registro.escribir_registro(directorio, construido)

    def _anotar_comparacion(self, ruta, bloque):
        """Inserta el bloque `comparacion` de `C-7` en el frontmatter del registro.

        `comparar.leer_registro` lee las 11 claves de `C-5` e ignora esta clave
        adicional, y el modo `comparar` la recupera como bloque registrado.
        """
        lineas = ruta.read_text(encoding="utf-8").splitlines()
        cierre = lineas.index("---", 1)
        lineas.insert(
            cierre,
            "comparacion: " + json.dumps(bloque, ensure_ascii=False, sort_keys=True),
        )
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def test_sin_perfil_lista_y_devuelve_2(self):
        codigo, salida, errores = self._ejecutar_main([])

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        texto = self._texto(salida, errores)
        for identificador in PERFILES_ESPERADOS:
            self.assertIn(
                identificador,
                texto,
                f"la lista de perfiles nombra {identificador}",
            )
        posiciones = [texto.index(identificador) for identificador in PERFILES_ESPERADOS]
        self.assertEqual(
            sorted(posiciones),
            posiciones,
            "los 3 identificadores se listan en orden alfabético",
        )

    def test_perfil_inexistente_devuelve_2(self):
        identificador = "perfil_inexistente"
        codigo, salida, errores = self._ejecutar_main(["--perfil", identificador])

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        self.assertIn(
            f"[ERROR] perfil no declarado: {identificador}",
            self._texto(salida, errores),
            "el mensaje nombra el perfil no declarado",
        )

        # El directorio de perfiles sin manifiestos produce el mismo mensaje.
        self._crear_arbol(manifiestos=())
        codigo_vacio, salida_vacia, errores_vacios = self._ejecutar_main(
            ["--raiz", str(self.raiz), "--perfil", "rendimiento"]
        )
        self.assertEqual(CODIGO_USO_INCORRECTO, codigo_vacio)
        self.assertIn(
            "[ERROR] perfil no declarado: rendimiento",
            self._texto(salida_vacia, errores_vacios),
            "el directorio sin manifiestos no declara ningún perfil",
        )

    def test_modo_invalido_devuelve_2(self):
        codigo, salida, errores = self._ejecutar_main(
            ["--perfil", "rendimiento", "--modo", "volcar"]
        )

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        texto = self._texto(salida, errores)
        self.assertIn("volcar", texto, "el mensaje nombra el modo no admitido")
        self.assertIn("--modo", texto, "el mensaje de uso declara la forma del argumento")

    def test_raiz_por_defecto_es_la_del_repositorio(self):
        doble = self._sustituir_comprobacion_previa()

        codigo, salida, errores = self._ejecutar_main(
            ["--perfil", "rendimiento", "--modo", "comprobar"]
        )

        self.assertEqual(
            1,
            len(doble.llamadas),
            "sin --raiz el modo comprobar ejecuta la comprobación previa 1 sola vez",
        )
        raiz_recibida = doble.raiz_recibida()
        self.assertIsNotNone(raiz_recibida, "la comprobación previa recibe la raíz")
        raiz = Path(raiz_recibida)
        self.assertTrue(
            raiz.is_absolute(),
            "la raíz derivada de la ubicación del módulo es absoluta",
        )
        self.assertEqual(
            (),
            tuple(parte for parte in raiz.parts if parte in (".", "..")),
            "la raíz derivada no contiene tramos relativos",
        )
        self.assertEqual(
            RAIZ,
            raiz.resolve(),
            "la raíz por defecto es el directorio que contiene tools/, derivado con parents[2]",
        )
        self.assertEqual(0, codigo, "la comprobación sintética superada devuelve el código 0")

    def test_comprobar_sin_artefactos_devuelve_4(self):
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=False)
        self._sustituir_vram_libre()

        with mock.patch("subprocess.Popen") as popen:
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--modo",
                    "comprobar",
                ]
            )

        self.assertEqual(
            CODIGO_ARTEFACTO_AUSENTE,
            codigo,
            "el árbol temporal sin artefactos devuelve el código de C-8 para artefacto ausente",
        )
        self.assertFalse(
            popen.called,
            "el modo comprobar no lanza el servidor ni ejecuta el binario",
        )

    def test_comprobar_inyecta_opciones_aceptadas(self):
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=False)
        manifiesto = _manifiesto_de_perfil("rendimiento.json")
        ejecutable_esperado = (
            self.raiz / manifiesto["artefactos"]["ejecutable"]
        ).resolve()

        _cargar_modulo()
        import binario
        import precheck

        consultas = []
        doble_ejecutar = _EjecutarDoble()
        vram = _VramLibreDoble(15172.0)

        def doble_opciones_aceptadas(ejecutable):
            consultas.append(Path(ejecutable))
            return dict(OPCIONES_ACEPTADAS)

        with mock.patch.object(binario, "opciones_aceptadas", doble_opciones_aceptadas):
            with mock.patch.object(precheck, "ejecutar", doble_ejecutar):
                with mock.patch.object(
                    _cargar_modulo(), "VRAM_LIBRE_MIB", vram
                ):
                    codigo, salida, errores = self._ejecutar_main(
                        [
                            "--raiz",
                            str(self.raiz),
                            "--perfil",
                            "rendimiento",
                            "--modo",
                            "comprobar",
                        ]
                    )

        self.assertEqual(
            1,
            len(consultas),
            "el modo comprobar consulta la ayuda del binario 1 sola vez",
        )
        self.assertEqual(
            ejecutable_esperado,
            consultas[0].resolve(),
            "la consulta recibe la ruta de artefactos.ejecutable resuelta contra la raíz",
        )
        self.assertEqual(
            1,
            len(doble_ejecutar.llamadas),
            "el modo comprobar ejecuta la comprobación previa 1 sola vez",
        )
        recibido = doble_ejecutar.llamadas[0]["kwargs"]
        self.assertEqual(
            OPCIONES_ACEPTADAS,
            recibido.get("opciones_aceptadas"),
            "la comprobación previa recibe el mapa de las 9 formas largas del binario",
        )
        self.assertEqual(
            15172.0,
            recibido.get("vram_disponible_mib"),
            "la comprobación previa recibe la VRAM libre en MiB que informa la "
            "consulta de solo lectura de T-068",
        )
        self.assertEqual(
            1,
            vram.llamadas,
            "el modo comprobar consulta la VRAM libre 1 sola vez",
        )
        self.assertEqual(
            0, codigo, "la comprobación sintética superada devuelve el código 0"
        )
        print(
            "test_comprobar_inyecta_opciones_aceptadas: consulta="
            f"{consultas[0].resolve()} opciones_aceptadas="
            + json.dumps(recibido.get("opciones_aceptadas"), sort_keys=True)
            + f" vram_disponible_mib={recibido.get('vram_disponible_mib')}"
        )

    def test_comprobar_usa_la_vram_libre_informada(self):
        """`T-068`: la comprobación 4 se resuelve con la VRAM libre de la consulta.

        La comprobación previa es la real y la consulta de la VRAM libre se
        sustituye por 1 doble que informa `16376` MiB, por encima del presupuesto
        medido de `rendimiento` —`16200.62` MiB para los `4096` tokens efectivos
        de `C-3`—, de modo que la comprobación 4 se declara `SUPERADA` y el
        cierre es `5 de 5` con el código `0` de `C-8`. El lector de metadatos y
        la ayuda del binario se sustituyen por dobles porque los artefactos del
        árbol temporal son señuelos; ningún caso ejecuta el binario ni consulta
        la GPU, conforme a `DEC-012`.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        # `T-069` devuelve el bloque `presupuesto_vram` de `rendimiento` a
        # `pendiente` con la marca `T-071`: el caso completa el manifiesto copiado
        # con los 3 valores que `T-036` midió, de modo que la comprobación 4 se
        # resuelve con la VRAM libre informada y no por la marca pendiente.
        ruta_manifiesto, manifiesto = self._leer_manifiesto_del_arbol()
        manifiesto["presupuesto_vram"] = dict(PRESUPUESTO_MEDIDO)
        self._escribir_manifiesto(ruta_manifiesto, manifiesto)
        modulo = _cargar_modulo()
        import binario
        import gguf

        cuantizacion = manifiesto["cuantizacion"]
        vram = _VramLibreDoble(16376.0)

        def doble_metadatos(ruta):
            return {
                "nombre": cuantizacion["nombre_gguf"],
                "file_type": cuantizacion["tipo_gguf"],
                "tamano_bytes": cuantizacion["tamano_bytes"],
            }

        with mock.patch.object(
            binario, "opciones_aceptadas", lambda ruta: dict(OPCIONES_ACEPTADAS)
        ):
            with mock.patch.object(gguf, "leer_metadatos", doble_metadatos):
                with mock.patch.object(modulo, "VRAM_LIBRE_MIB", vram):
                    codigo, salida, errores = self._ejecutar_main(
                        [
                            "--raiz",
                            str(self.raiz),
                            "--perfil",
                            "rendimiento",
                            "--modo",
                            "comprobar",
                        ]
                    )

        lineas = salida.splitlines()
        superadas_4 = [linea for linea in lineas if linea.startswith("SUPERADA 4.")]
        cierres = [
            linea for linea in lineas if linea.startswith("COMPROBACIÓN PREVIA:")
        ]

        self.assertEqual(
            1,
            vram.llamadas,
            "el modo comprobar consulta la VRAM libre 1 sola vez",
        )
        self.assertEqual(
            1,
            len(superadas_4),
            "con la VRAM libre informada la comprobación 4 se resuelve superada",
        )
        self.assertIn(
            "4096 tokens de contexto",
            superadas_4[0],
            "el detalle declara el contexto efectivo con el que arranca el servidor",
        )
        self.assertIn(
            "16376 MiB disponibles",
            superadas_4[0],
            "el detalle declara la VRAM libre en MiB que informó la consulta",
        )
        self.assertFalse(
            [linea for linea in lineas if linea.startswith("PENDIENTE ")],
            "con el bloque completo y la VRAM informada 0 comprobaciones quedan pendientes",
        )
        self.assertEqual(
            [CIERRE_COMPLETO],
            cierres,
            "el cierre declara las 5 comprobaciones superadas",
        )
        self.assertEqual(
            0, codigo, "la comprobación previa completa devuelve el código 0 de C-8"
        )

        print(
            "test_comprobar_usa_la_vram_libre_informada: "
            f"vram_disponible_mib={vram.valor} | {superadas_4[0]} | "
            f"cierre={cierres[0]} | codigo={codigo}"
        )

    def test_argumentos_del_servidor_usan_la_forma_del_binario(self):
        """`T-052`: el lanzamiento declara las banderas que el binario enumera.

        El binario compilado declara `-lm, --load-mode` con el valor `none` y no
        admite `--no-mmap`, que responde `error: invalid argument: --no-mmap`.
        La prueba toma el mapa de `binario.opciones_aceptadas` sobre la ruta de
        `artefactos.ejecutable` con 1 doble de las 9 formas largas de la ayuda y
        contrasta cada bandera de las opciones efectivas con ese mapa, de modo
        que la prueba falla si el lanzador vuelve a introducir 1 bandera que el
        binario no enumera.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",))
        _, manifiesto = self._leer_manifiesto_del_arbol()
        modulo = _cargar_modulo()
        import binario
        import perfiles

        ejecutable = self.raiz / manifiesto["artefactos"]["ejecutable"]

        def doble_opciones_aceptadas(ruta):
            return dict(OPCIONES_ACEPTADAS)

        with mock.patch.object(
            binario, "opciones_aceptadas", doble_opciones_aceptadas
        ):
            mapa = binario.opciones_aceptadas(ejecutable)

        opciones = perfiles.resolver_opciones(manifiesto, {})["opciones"]
        argumentos = modulo._argumentos_del_servidor(
            manifiesto, self.raiz, opciones
        )
        print(
            "test_argumentos_del_servidor_usan_la_forma_del_binario: "
            f"opciones={json.dumps(opciones, ensure_ascii=False, sort_keys=True)} "
            "argumentos=" + " ".join(argumentos)
        )

        self.assertEqual(
            9,
            len(opciones),
            "las opciones efectivas del perfil son los 9 ejes de C-2",
        )
        self.assertEqual(
            "none",
            opciones["load_mode"],
            "el valor efectivo de load_mode es none, que es el que el binario admite",
        )
        pares = [
            argumentos[indice : indice + 2]
            for indice in range(len(argumentos) - 1)
        ]
        self.assertIn(
            ["--load-mode", "none"],
            pares,
            "--load-mode viaja como bandera y none como su argumento; el binario "
            "declara -lm, --load-mode con el valor none",
        )
        # `DEC-028`: los 2 tipos de caché KV viajan con su valor efectivo.
        self.assertIn(
            ["--cache-type-k", "q8_0"],
            pares,
            "el lanzamiento declara --cache-type-k q8_0",
        )
        self.assertIn(
            ["--cache-type-v", "q8_0"],
            pares,
            "el lanzamiento declara --cache-type-v q8_0",
        )
        self.assertEqual(
            0,
            argumentos.count("--no-mmap"),
            "--no-mmap no es 1 bandera del binario: responde "
            "error: invalid argument: --no-mmap",
        )

        permitidas = set(mapa.values()) | set(BANDERAS_FIJAS)
        banderas = [
            argumento for argumento in argumentos if argumento.startswith("--")
        ]
        self.assertEqual(
            [],
            [bandera for bandera in banderas if bandera not in permitidas],
            "cada bandera del lanzamiento pertenece a binario.opciones_aceptadas, "
            "es 1 de las 5 banderas fijas del modelo, el proyector, el punto de "
            "acceso y el draft, es 1 de las 2 que declara DEC-024 o es la de "
            "registro que declara T-065",
        )
        for eje, forma in mapa.items():
            self.assertIn(
                forma,
                argumentos,
                f"el lanzamiento declara la forma {forma} que el binario enumera "
                f"para el eje {eje}",
            )
            self.assertEqual(
                str(opciones[eje]),
                argumentos[argumentos.index(forma) + 1],
                f"la bandera {forma} declara el valor efectivo del eje {eje}",
            )

    def test_argumentos_incluyen_la_bandera_de_registro_de_verbosidad(self):
        """`T-065`: los argumentos declaran `--log-verbosity 4` y la guardia la admite.

        `--log-verbosity 4` hace que el binario imprima la línea
        `CUDA_Host model buffer size = <n> MiB` del modelo principal, que es la
        fuente del campo 22 de `C-6` desde `T-061`. La bandera es de registro y
        no 1 eje de `C-2`: las opciones efectivas siguen siendo los 9 ejes del
        perfil, el doble `OPCIONES_ACEPTADAS` no la enumera entre ellos y el
        conjunto `permitidas` de la guardia de banderas la admite junto a las 5
        banderas fijas, las 2 de `DEC-024` y las 9 formas del binario. Ningún
        caso ejecuta el binario ni consulta la GPU.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",))
        _, manifiesto = self._leer_manifiesto_del_arbol()
        modulo = _cargar_modulo()
        import perfiles

        opciones = perfiles.resolver_opciones(manifiesto, {})["opciones"]
        argumentos = modulo._argumentos_del_servidor(
            manifiesto, self.raiz, opciones
        )
        print(
            "test_argumentos_incluyen_la_bandera_de_registro_de_verbosidad: "
            "argumentos=" + " ".join(argumentos)
        )

        pares = [
            argumentos[indice : indice + 2]
            for indice in range(len(argumentos) - 1)
        ]
        self.assertIn(
            ["--log-verbosity", "4"],
            pares,
            "el lanzamiento declara --log-verbosity 4 para que el binario "
            "imprima CUDA_Host model buffer size, que es la fuente del campo 22",
        )

        self.assertEqual(
            9,
            len(opciones),
            "las opciones efectivas siguen siendo los 9 ejes de C-2: la bandera "
            "de registro no entra en la resolución de C-3",
        )
        self.assertNotIn(
            "log_verbosity",
            opciones,
            "--log-verbosity es 1 bandera de registro y no 1 eje de C-2",
        )
        mapa = dict(OPCIONES_ACEPTADAS)
        self.assertNotIn(
            "--log-verbosity",
            mapa.values(),
            "el doble de la ayuda del binario no enumera --log-verbosity entre "
            "los 9 ejes",
        )
        permitidas = set(mapa.values()) | set(BANDERAS_FIJAS)
        self.assertIn(
            "--log-verbosity",
            permitidas,
            "la guardia de banderas admite --log-verbosity en su conjunto de "
            "banderas permitidas sin debilitar la aserción de 0 banderas fuera "
            "de ese conjunto",
        )

    def _campo_11_de(self, manifiesto):
        """Campo 11 de `C-6` que el lanzador deriva del bloque `especulativa`.

        Toma el valor del mapa de las 21 filas que `_campos_de_c6` compone, con
        los datos sintéticos del resto de filas, de modo que la prueba contrasta
        el campo 11 del registro y no 1 función auxiliar aislada.
        """
        modulo = _cargar_modulo()
        memoria = {
            "codigo": 0,
            "vram_total_mib": 16376,
            "vram_usada_mib": 14200,
            "vram_libre_mib": 1449,
            "residente_mib": 2410,
            "desbordamiento_mib": 0,
        }
        campos = modulo._campos_de_c6(
            manifiesto,
            mock.Mock(calidad=None, prueba=None, errores=None),
            manifiesto["opciones"],
            1.0,
            memoria,
            None,
            "continúa en servicio",
            "sintetica",
            "sintetico",
            datetime(2026, 11, 22, 10, 0, 0, tzinfo=timezone.utc),
        )
        return campos["Decodificación especulativa"]

    def test_argumentos_y_campo_11_de_especulativa(self):
        """`T-054`: el bloque `especulativa` de `DEC-024` fija las 2 banderas y el campo 11.

        Con 1 manifiesto de tipo `draft-mtp` y techo `3`, el lanzamiento declara
        `--spec-type draft-mtp` y `--spec-draft-n-max 3` después de
        `--model-draft`, y el campo 11 del registro es
        `activado (techo de borrador 3 tokens)`. Con el perfil
        `sin_especulativa`, que declara tipo `ninguno` y techo `null`, ninguna de
        las 2 banderas aparece y el campo 11 es
        `desactivado (sin techo de borrador)`. El bloque se deriva de la
        declaración del manifiesto y no de la presencia del artefacto `draft`:
        con `draft-mtp` y `artefactos.draft` en `null` el campo 11 sigue activado
        y las 2 banderas no se añaden. Ningún caso ejecuta el binario.
        """
        self._crear_arbol(
            manifiestos=("rendimiento.json", "sin_especulativa.json")
        )
        modulo = _cargar_modulo()
        import perfiles

        _, rendimiento = self._leer_manifiesto_del_arbol("rendimiento")
        opciones = perfiles.resolver_opciones(rendimiento, {})["opciones"]
        argumentos = modulo._argumentos_del_servidor(
            rendimiento, self.raiz, opciones
        )
        campo_11 = self._campo_11_de(rendimiento)

        self.assertEqual(
            {"tipo": "draft-mtp", "techo": 3},
            rendimiento["especulativa"],
            "el perfil rendimiento declara el bloque de DEC-024 con techo 3",
        )
        self.assertIn(
            "--model-draft",
            argumentos,
            "el manifiesto declara el artefacto draft y el lanzamiento lo aplica",
        )
        self.assertIn(
            "--spec-type",
            argumentos,
            "DEC-024 exige --spec-type para cargar el borrador Gemma4Assistant",
        )
        self.assertEqual(
            "draft-mtp",
            argumentos[argumentos.index("--spec-type") + 1],
            "--spec-type declara el tipo draft-mtp del bloque especulativa",
        )
        self.assertIn(
            "--spec-draft-n-max",
            argumentos,
            "DEC-024 exige el techo del borrador en --spec-draft-n-max",
        )
        self.assertEqual(
            "3",
            argumentos[argumentos.index("--spec-draft-n-max") + 1],
            "--spec-draft-n-max declara el techo de 3 tokens del bloque",
        )
        self.assertLess(
            argumentos.index("--model-draft"),
            argumentos.index("--spec-type"),
            "las 2 banderas de DEC-024 se añaden después de --model-draft",
        )
        self.assertLess(
            argumentos.index("--spec-type"),
            argumentos.index("--spec-draft-n-max"),
            "--spec-type precede a --spec-draft-n-max en la línea del servidor",
        )
        self.assertEqual(
            "activado (techo de borrador 3 tokens)",
            campo_11,
            "el campo 11 declara el techo del bloque especulativa del manifiesto",
        )

        _, sin_especulativa = self._leer_manifiesto_del_arbol("sin_especulativa")
        opciones_sin = perfiles.resolver_opciones(sin_especulativa, {})["opciones"]
        argumentos_sin = modulo._argumentos_del_servidor(
            sin_especulativa, self.raiz, opciones_sin
        )
        campo_11_sin = self._campo_11_de(sin_especulativa)

        self.assertEqual(
            {"tipo": "ninguno", "techo": None},
            sin_especulativa["especulativa"],
            "el perfil sin_especulativa declara tipo ninguno y techo null",
        )
        self.assertNotIn(
            "--spec-type",
            argumentos_sin,
            "el tipo ninguno no declara modo de especulación",
        )
        self.assertNotIn(
            "--spec-draft-n-max",
            argumentos_sin,
            "el tipo ninguno no declara techo de borrador",
        )
        self.assertEqual(
            "desactivado (sin techo de borrador)",
            campo_11_sin,
            "el campo 11 transcribe el tipo ninguno del bloque",
        )

        # `DEC-024`: el campo 11 se deriva del bloque y no de la presencia del
        # artefacto draft, de modo que sin draft el tipo draft-mtp sigue activado
        # y las 2 banderas no se añaden porque el manifiesto no declara borrador.
        sin_artefacto = json.loads(json.dumps(rendimiento))
        sin_artefacto["artefactos"]["draft"] = None
        argumentos_sin_artefacto = modulo._argumentos_del_servidor(
            sin_artefacto, self.raiz, opciones
        )
        self.assertNotIn("--model-draft", argumentos_sin_artefacto)
        self.assertNotIn("--spec-type", argumentos_sin_artefacto)
        self.assertNotIn("--spec-draft-n-max", argumentos_sin_artefacto)
        self.assertEqual(
            "activado (techo de borrador 3 tokens)",
            self._campo_11_de(sin_artefacto),
            "el campo 11 se deriva del bloque y no de la presencia del artefacto",
        )

        print(
            "test_argumentos_y_campo_11_de_especulativa: draft-mtp argumentos="
            + " ".join(argumentos)
            + f" campo11={campo_11} | ninguno campo11={campo_11_sin} "
            "banderas_sin_artefacto=0"
        )

    def test_comparar_sin_parametro_devuelve_2(self):
        codigo, salida, errores = self._ejecutar_main(
            ["--perfil", "rendimiento", "--modo", "comparar"]
        )

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        self.assertIn(
            "--parametro",
            self._texto(salida, errores),
            "el mensaje de argumento ausente nombra el argumento --parametro",
        )

    def test_modo_comparar_desviacion_sin_comparacion(self):
        """Modo `comparar`: valor inicial sin bloque de `C-7` y bloque registrado.

        Primero comprueba el caso del eje `ubatch` cuya desviación no declara
        comparación: el modo aplica el valor inicial, emite el aviso del eje
        omitido de `C-3`, deja intactas las opciones efectivas de las ejecuciones
        de servicio y devuelve el código `0` de `C-8` con el motivo del bloque
        pendiente. Después registra un bloque completo de `C-7` y comprueba que el
        modo usa ese bloque y la elegibilidad de `estado.elegible_para_aprobado`
        sin recalcular las cifras.
        """
        _cargar_modulo()
        import perfiles

        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=False)
        ruta_manifiesto, manifiesto = self._leer_manifiesto_del_arbol()
        bytes_antes = ruta_manifiesto.read_bytes()

        with mock.patch("subprocess.Popen") as popen:
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--modo",
                    "comparar",
                    "--parametro",
                    "ubatch",
                ]
            )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "una desviación sin comparación completa resuelve con el código 0 de C-8",
        )
        self.assertFalse(
            popen.called,
            "el modo comparar de T-031 no lanza el servidor ni ejecuta el binario",
        )
        self.assertIn(
            "[AVISO] desviación omitida: ubatch",
            texto,
            "C-3 emite el aviso del eje cuya comparación falta",
        )
        self.assertIn(
            "COMPARACIÓN:",
            texto,
            "el modo comparar reporta el motivo del bloque pendiente",
        )
        self.assertIn(
            "ubatch",
            texto,
            "el motivo nombra el eje comparado",
        )
        self.assertIn(
            "valor inicial",
            texto,
            "el motivo declara que rige el valor inicial de C-2",
        )

        servicio = perfiles.resolver_opciones(manifiesto, {})
        self.assertEqual(
            512,
            servicio["opciones"]["ubatch"],
            "la desviación sin comparación conserva el valor inicial de C-2",
        )
        self.assertIn(
            "ubatch",
            servicio["omitidas"],
            "la desviación sin comparación figura como omitida",
        )
        self.assertIn(
            json.dumps(servicio["opciones"], ensure_ascii=False, sort_keys=True),
            texto,
            "el modo imprime las mismas opciones efectivas que las ejecuciones de servicio",
        )
        self.assertEqual(
            bytes_antes,
            ruta_manifiesto.read_bytes(),
            "el modo comparar no altera el manifiesto ni lo que sirve",
        )

        # Segunda mitad: 1 bloque de C-7 completo registrado por la campaña.
        ruta_carga = self._escribir_registro(
            manifiesto,
            "carga",
            "carga",
            datetime(2026, 11, 22, 10, 0, 0, tzinfo=timezone.utc),
        )
        ruta_comparacion = self._escribir_registro(
            manifiesto,
            "comparacion-micro-lote",
            "comparacion",
            datetime(2026, 11, 22, 10, 0, 1, tzinfo=timezone.utc),
        )
        bloque = {
            "parametro": "ubatch",
            "medicion_inicial": ruta_carga.stem,
            "medicion_propuesta": ruta_comparacion.stem,
            "valor_inicial": 512,
            "valor_propuesto": 1120,
            # Cifras deliberadamente distintas de las filas: si el modo las
            # recalculara en vez de usar el bloque, la comparación no coincidiría.
            "delta_velocidad_generacion_tokens_por_segundo": 1.25,
            "delta_velocidad_prompt_tokens_por_segundo": -2.5,
            "delta_vram_asignada_mib": 3,
            "delta_vram_libre_mib": -4,
            "delta_ram_mib": 5,
        }
        self._anotar_comparacion(ruta_comparacion, bloque)
        for desviacion in manifiesto["desviaciones"]:
            if desviacion["parametro"] == "ubatch":
                desviacion["comparacion"] = ruta_comparacion.stem
        self._escribir_manifiesto(ruta_manifiesto, manifiesto)

        codigo_completo, salida_completa, errores_completos = self._ejecutar_main(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                "rendimiento",
                "--modo",
                "comparar",
                "--parametro",
                "ubatch",
            ]
        )
        texto_completo = self._texto(salida_completa, errores_completos)
        lineas_bloque = [
            linea for linea in salida_completa.splitlines() if linea.startswith("COMPARACIÓN:")
        ]
        lineas_elegibilidad = [
            linea
            for linea in salida_completa.splitlines()
            if linea.startswith("ELEGIBILIDAD:")
        ]

        self.assertEqual(
            0,
            codigo_completo,
            "con el bloque de C-7 registrado el modo comparar devuelve el código 0",
        )
        self.assertEqual(
            1,
            len(lineas_bloque),
            "el modo comparar imprime 1 bloque de comparación",
        )
        self.assertIn(
            json.dumps(bloque, ensure_ascii=False, sort_keys=True),
            texto_completo,
            "el modo usa el bloque registrado sin recalcular sus cifras",
        )
        self.assertEqual(
            1,
            len(lineas_elegibilidad),
            "el modo comparar reporta 1 elegibilidad de estado.elegible_para_aprobado",
        )
        self.assertIn(
            '"elegible": false',
            lineas_elegibilidad[0],
            "la elegibilidad reportada es la de estado y no 1 cálculo propio",
        )
        self.assertIn(
            '"ubatch": 1120',
            texto_completo,
            "con el bloque completo la resolución aplica el valor propuesto de C-3",
        )
        servicio_completo = perfiles.resolver_opciones(manifiesto, {})
        self.assertEqual(
            512,
            servicio_completo["opciones"]["ubatch"],
            "registrar la comparación no altera las opciones efectivas de las ejecuciones de servicio",
        )

        print(
            "test_modo_comparar_desviacion_sin_comparacion: "
            f"sin_comparacion_codigo={codigo} aviso=desviación omitida ubatch "
            f"opciones_servicio="
            f"{json.dumps(servicio['opciones'], ensure_ascii=False, sort_keys=True)} | "
            f"bloque={lineas_bloque[0]} | elegibilidad={lineas_elegibilidad[0]}"
        )

    def test_modo_comparar_ejecuta_2_mediciones(self):
        """`T-049`: 2 mediciones reales, bloque de `C-7` y servicio sin desviación.

        La campaña sustituye `LANZAR_SERVIDOR`, `MEDIR_MEMORIA` y `SONDEAR` por
        dobles de valores sintéticos; la espera de `/health` sustituye
        `urllib.request.urlopen` y la lectura de la versión del binario se
        sustituye con el doble de la comprobación previa, de modo que ningún caso
        ejecuta el binario real, `nvidia-smi`, `powershell.exe` ni la GPU. Los
        artefactos del árbol temporal son señuelos: la campaña solo contrasta su
        existencia antes de arrancar el servidor.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        _, manifiesto = self._leer_manifiesto_del_arbol()
        self._sustituir_comprobacion_previa()

        modulo = _cargar_modulo()
        lanzar = _LanzarDoble()
        medir = _MedirDoble([MEMORIA_INICIAL, MEMORIA_PROPUESTA])
        sondear = _SondaDoble([SONDA_INICIAL, SONDA_PROPUESTA])

        with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
            with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                with mock.patch.object(modulo, "SONDEAR", sondear):
                    with mock.patch(
                        "urllib.request.urlopen",
                        return_value=_respuesta_de_salud(),
                    ):
                        codigo, salida, errores = self._ejecutar_main(
                            [
                                "--raiz",
                                str(self.raiz),
                                "--perfil",
                                "rendimiento",
                                "--modo",
                                "comparar",
                                "--parametro",
                                PARAMETRO_COMPARADO,
                            ]
                        )

        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "la campaña de comparación completa devuelve el código 0 de C-8",
        )
        self.assertEqual(
            2,
            len(medir.llamadas),
            "la campaña mide la memoria en las 2 mediciones",
        )
        self.assertEqual(
            2,
            len(sondear.llamadas),
            "la campaña ejecuta la sonda de DEC-011 en las 2 mediciones",
        )
        self.assertEqual(
            2,
            len(lanzar.llamadas),
            "la campaña arranca el servidor 2 veces, 1 por valor del eje",
        )
        self.assertEqual(
            [str(VALOR_INICIAL_COMPARADO), str(VALOR_PROPUESTO_COMPARADO)],
            lanzar.valores_de("--ubatch-size"),
            "la primera medición aplica el valor inicial y la segunda el propuesto",
        )
        mediciones = len(lanzar.llamadas)
        valores_comparados = lanzar.valores_de("--ubatch-size")
        self.assertEqual(
            [True, True],
            [servidor.cerrado for servidor in lanzar.servidores],
            "cada medición cierra su propio servidor",
        )
        self.assertEqual(
            "http://127.0.0.1:8080",
            sondear.llamadas[0]["base_url"],
            "la sonda recibe la URL base y el puerto de las constantes del módulo",
        )

        import comparar
        import perfiles

        registros = sorted(
            (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
        )
        self.assertEqual(
            2,
            len(registros),
            "la campaña deja 2 registros propios en results/gemma/rendimiento/",
        )
        lecturas = [comparar.leer_registro(ruta) for ruta in registros]
        identificadores = [lectura["frontmatter"]["id"] for lectura in lecturas]
        self.assertEqual(
            {"comparacion"},
            {lectura["frontmatter"]["proposito"] for lectura in lecturas},
            "los 2 registros declaran el propósito comparacion de C-5",
        )
        self.assertEqual(
            len(identificadores),
            len(set(identificadores)),
            "los 2 registros declaran identificadores distintos",
        )
        self.assertEqual(
            {PRUEBA_COMPARADA},
            {lectura["frontmatter"]["prueba"] for lectura in lecturas},
            "los 2 registros declaran el nombre de la prueba de la campaña",
        )
        self.assertEqual(
            [VALOR_INICIAL_COMPARADO, VALOR_PROPUESTO_COMPARADO],
            [
                lectura["frontmatter"]["opciones_efectivas"][PARAMETRO_COMPARADO]
                for lectura in lecturas
            ],
            "cada registro transcribe el valor efectivo del eje que midió",
        )
        self.assertEqual(
            perfiles.huella_opciones(manifiesto["opciones"]),
            lecturas[0]["frontmatter"]["huella_opciones"],
            "la huella es la de las opciones declaradas y no las efectivas, según DEC-020",
        )

        lineas_bloque = [
            linea for linea in salida.splitlines() if linea.startswith("COMPARACIÓN:")
        ]
        self.assertEqual(
            1,
            len(lineas_bloque),
            "el modo imprime 1 bloque de comparación con las 5 diferencias",
        )
        bloque = json.loads(lineas_bloque[0].split(":", 1)[1].strip())
        self.assertEqual(PARAMETRO_COMPARADO, bloque["parametro"])
        self.assertEqual(VALOR_INICIAL_COMPARADO, bloque["valor_inicial"])
        self.assertEqual(VALOR_PROPUESTO_COMPARADO, bloque["valor_propuesto"])
        self.assertEqual(
            identificadores[0],
            bloque["medicion_inicial"],
            "el bloque cita el registro del valor inicial",
        )
        self.assertEqual(
            identificadores[1],
            bloque["medicion_propuesta"],
            "el bloque cita el registro del valor propuesto",
        )
        self.assertEqual(
            set(DIFERENCIAS_UBATCH)
            | {
                "parametro",
                "medicion_inicial",
                "medicion_propuesta",
                "valor_inicial",
                "valor_propuesto",
            },
            set(bloque),
            "el bloque declara las 10 claves de C-7 y ninguna otra",
        )
        for clave, esperado in DIFERENCIAS_UBATCH.items():
            self.assertEqual(
                esperado,
                bloque[clave],
                f"{clave} es la diferencia de propuesta menos inicial",
            )

        texto_propuesto = registros[1].read_text(encoding="utf-8")
        lineas_comparacion = [
            linea
            for linea in texto_propuesto.splitlines()
            if linea.startswith("comparacion:")
        ]
        self.assertEqual(
            1,
            len(lineas_comparacion),
            "el registro propuesto transcribe el bloque en su clave comparacion",
        )
        self.assertEqual(
            bloque,
            json.loads(lineas_comparacion[0].split(":", 1)[1].strip()),
            "el bloque escrito en el registro es el que el modo imprimió",
        )
        self.assertIn(
            "ELEGIBILIDAD:",
            texto,
            "el modo reporta la elegibilidad de estado.elegible_para_aprobado",
        )

        # Con los 2 registros ya escritos, el modo `servir` resuelve sus opciones
        # con los registros disponibles y conserva el valor inicial del eje: la
        # desviación del manifiesto todavía no declara su comparación.
        with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
            with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                with mock.patch.object(modulo, "SONDEAR", sondear):
                    with mock.patch(
                        "urllib.request.urlopen",
                        return_value=_respuesta_de_salud(),
                    ):
                        codigo_servicio, salida_servicio, errores_servicio = (
                            self._ejecutar_main(
                                [
                                    "--raiz",
                                    str(self.raiz),
                                    "--perfil",
                                    "rendimiento",
                                    "--modo",
                                    "servir",
                                ]
                            )
                        )

        self.assertEqual(
            0,
            codigo_servicio,
            "el modo servir resuelve con los registros disponibles y supera la comprobación previa",
        )
        texto_servicio = self._texto(salida_servicio, errores_servicio)
        lineas_opciones = [
            linea
            for linea in salida_servicio.splitlines()
            if linea.startswith("Opciones efectivas: ")
        ]
        self.assertEqual(
            1,
            len(lineas_opciones),
            "el modo servir imprime 1 sola vez sus opciones efectivas",
        )
        opciones_servicio = json.loads(lineas_opciones[0].split(": ", 1)[1])
        self.assertEqual(
            9,
            len(opciones_servicio),
            "las opciones del servicio siguen siendo los 9 ejes de C-2",
        )
        self.assertEqual(
            VALOR_INICIAL_COMPARADO,
            opciones_servicio[PARAMETRO_COMPARADO],
            "mientras la desviación no declare su comparación, el servicio conserva el valor inicial",
        )
        self.assertEqual(
            4096,
            opciones_servicio["ctx_size"],
            "el contexto efectivo es el inicial mientras la desviación no declare su comparación",
        )
        self.assertEqual("on", opciones_servicio["flash_attn"])
        self.assertIn(
            f"[AVISO] desviación omitida: {PARAMETRO_COMPARADO}",
            texto_servicio,
            "el servicio avisa del eje cuya comparación no está declarada en el manifiesto",
        )

        print(
            "test_modo_comparar_ejecuta_2_mediciones: "
            f"mediciones={mediciones} "
            f"{PARAMETRO_COMPARADO}={valores_comparados} "
            f"registros={identificadores} bloque={lineas_bloque[0]} "
            f"servicio={lineas_opciones[0]}"
        )

    def test_modo_comparar_conserva_ncmoe_adoptado(self):
        """`T-079` y `T-083`: las 2 mediciones de `ubatch` corren con `ncmoe` `9`.

        El perfil `rendimiento` cita en `C-3` el registro propuesto de `T-082`
        `20261124T191126Z-rendimiento-comparacion-ncmoe`, cuyo bloque completo de
        `C-7` adopta `ncmoe` `9`. La campaña parte de las opciones efectivas
        adoptadas y sustituye solo el eje comparado, de modo que las 2 mediciones
        de `ubatch` declaran `--n-cpu-moe 9` y la diferencia de `C-7` es
        atribuible a ese eje; con la resolución sin registros que `T-079`
        corrige, ambas declaraban `--n-cpu-moe 0`. El registro adoptado es
        sintético, la espera de `/health` y las 2 mediciones se sustituyen por
        dobles y ningún caso ejecuta el binario, `nvidia-smi` ni la GPU,
        conforme a `DEC-012`.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        _, manifiesto = self._leer_manifiesto_del_arbol()
        self._sustituir_comprobacion_previa()

        desviacion_ncmoe = next(
            desviacion
            for desviacion in manifiesto["desviaciones"]
            if desviacion["parametro"] == "ncmoe"
        )
        ruta_ncmoe = self._escribir_registro(
            manifiesto,
            "comparacion-ncmoe",
            "comparacion",
            datetime(2026, 11, 24, 19, 11, 26, tzinfo=timezone.utc),
        )
        self.assertEqual(
            COMPARACION_NCMOE,
            ruta_ncmoe.stem,
            "el registro adoptado declara el identificador que cita el perfil",
        )
        self.assertEqual(
            COMPARACION_NCMOE,
            desviacion_ncmoe["comparacion"],
            "el perfil rendimiento adopta ncmoe con esta comparación",
        )
        self._anotar_comparacion(
            ruta_ncmoe,
            {
                "parametro": "ncmoe",
                "medicion_inicial": "20261124T191036Z-rendimiento-comparacion-ncmoe",
                "medicion_propuesta": ruta_ncmoe.stem,
                "valor_inicial": 0,
                "valor_propuesto": NCMOE_ADOPTADO,
                "delta_velocidad_generacion_tokens_por_segundo": 1.0,
                "delta_velocidad_prompt_tokens_por_segundo": 2.0,
                "delta_vram_asignada_mib": -3,
                "delta_vram_libre_mib": 4,
                "delta_ram_mib": 5,
            },
        )

        modulo = _cargar_modulo()
        lanzar = _LanzarDoble()
        medir = _MedirDoble([MEMORIA_INICIAL, MEMORIA_PROPUESTA])
        sondear = _SondaDoble([SONDA_INICIAL, SONDA_PROPUESTA])

        with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
            with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                with mock.patch.object(modulo, "SONDEAR", sondear):
                    with mock.patch(
                        "urllib.request.urlopen",
                        return_value=_respuesta_de_salud(),
                    ):
                        codigo, salida, errores = self._ejecutar_main(
                            [
                                "--raiz",
                                str(self.raiz),
                                "--perfil",
                                "rendimiento",
                                "--modo",
                                "comparar",
                                "--parametro",
                                PARAMETRO_COMPARADO,
                            ]
                        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "la campaña hereda la comparación adoptada y devuelve el código 0",
        )
        self.assertEqual(
            2,
            len(lanzar.llamadas),
            "la campaña arranca el servidor 1 vez por valor de ubatch",
        )
        self.assertEqual(
            [str(NCMOE_ADOPTADO), str(NCMOE_ADOPTADO)],
            lanzar.valores_de("--n-cpu-moe"),
            "las 2 mediciones de ubatch conservan el ncmoe adoptado en 9",
        )
        self.assertEqual(
            [str(VALOR_INICIAL_COMPARADO), str(VALOR_PROPUESTO_COMPARADO)],
            lanzar.valores_de("--ubatch-size"),
            "solo el eje comparado cambia entre las 2 mediciones",
        )
        self.assertEqual(
            ["4096", "4096"],
            lanzar.valores_de("--ctx-size"),
            "el eje no comparado conserva la opción efectiva del perfil",
        )

        import comparar

        lecturas = [
            comparar.leer_registro(ruta)
            for ruta in sorted(
                (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
            )
            if ruta.stem != COMPARACION_NCMOE
        ]
        self.assertEqual(
            2,
            len(lecturas),
            "la campaña deja sus 2 registros junto al registro adoptado",
        )
        self.assertEqual(
            [NCMOE_ADOPTADO, NCMOE_ADOPTADO],
            [
                lectura["frontmatter"]["opciones_efectivas"]["ncmoe"]
                for lectura in lecturas
            ],
            "cada registro transcribe el ncmoe adoptado en sus opciones efectivas",
        )
        self.assertIn(
            "COMPARACIÓN:",
            texto,
            "la campaña completa reporta el bloque de C-7",
        )

        print(
            "test_modo_comparar_conserva_ncmoe_adoptado: "
            f"mediciones={len(lanzar.llamadas)} "
            f"ncmoe={lanzar.valores_de('--n-cpu-moe')} "
            f"{PARAMETRO_COMPARADO}={lanzar.valores_de('--ubatch-size')} "
            f"ctx_size={lanzar.valores_de('--ctx-size')} "
            f"omitidas={texto.count('desviación omitida')}"
        )

    def test_campo_22_lee_memoria_de_expertos_en_host(self):
        """`T-061`: el campo 22 toma `CUDA_Host model buffer size` del registro.

        El servidor se sustituye por 1 doble que expone la salida capturada: con
        el registro sintético de `LOG_SERVIDOR` el campo 22 vale el de la línea
        del modelo principal —`2846.25 MiB`— y no la suma con la línea del draft,
        que también aparece en el log. Con `LOG_SIN_EXPERTOS`, que no declara esa
        línea, el campo 22 declara `no disponible` sin estimar ningún número. Los
        2 casos escriben su registro con `--modo medir` sobre el árbol temporal y
        ninguno ejecuta el binario, la GPU ni el servidor real, conforme a
        `DEC-012`.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()

        modulo = _cargar_modulo()
        medir = _MedirDoble([MEMORIA_INICIAL])
        sondear = _SondaDoble([SONDA_INICIAL])

        def _ejecutar_con(salida_servidor, prueba):
            """Ejecuta el modo `medir` con 1 salida capturada sintética."""
            lanzar = _LanzarDoble(salida=salida_servidor)
            with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
                with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                    with mock.patch.object(modulo, "SONDEAR", sondear):
                        with mock.patch(
                            "urllib.request.urlopen",
                            return_value=_respuesta_de_salud(),
                        ):
                            codigo, salida, errores = self._ejecutar_main(
                                [
                                    "--raiz",
                                    str(self.raiz),
                                    "--perfil",
                                    "rendimiento",
                                    "--modo",
                                    "medir",
                                    "--prueba",
                                    prueba,
                                    "--calidad",
                                    "sintetica",
                                ]
                            )
            self.assertEqual(
                0,
                codigo,
                f"el modo medir con la prueba {prueba} devuelve el código 0 de C-8",
            )
            self.assertEqual(
                1,
                len(lanzar.servidores),
                "el modo medir arranca el servidor 1 sola vez",
            )
            self.assertEqual(
                1,
                lanzar.servidores[0].lecturas,
                "el campo 22 lee la salida capturada antes de cerrar el servidor",
            )
            self.assertTrue(
                lanzar.servidores[0].cerrado,
                "el servidor se cierra después de leer su salida",
            )
            return self._texto(salida, errores)

        _ejecutar_con(LOG_SERVIDOR, "carga")
        _ejecutar_con(LOG_SIN_EXPERTOS, "carga-sin-host")

        import comparar

        rutas = sorted(
            (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
        )
        self.assertEqual(
            2,
            len(rutas),
            "cada ejecución del modo medir deja 1 registro propio",
        )
        por_prueba = {
            lectura["frontmatter"]["prueba"]: lectura
            for lectura in (comparar.leer_registro(ruta) for ruta in rutas)
        }
        self.assertEqual(
            {"carga", "carga-sin-host"},
            set(por_prueba),
            "los 2 registros declaran el nombre de su prueba",
        )
        campo_22 = {
            prueba: {
                fila["numero"]: fila["valor"]
                for fila in por_prueba[prueba]["filas"]
            }[22]
            for prueba in por_prueba
        }
        self.assertEqual(
            22,
            len(por_prueba["carga"]["filas"]),
            "el registro declara las 22 filas de C-6",
        )
        self.assertEqual(
            MEMORIA_EXPERTOS_HOST,
            campo_22["carga"],
            "el campo 22 es la memoria de expertos en host del modelo principal "
            "y no la suma con la línea del draft",
        )
        self.assertEqual(
            "no disponible",
            campo_22["carga-sin-host"],
            "sin la línea CUDA_Host model buffer size el campo 22 declara "
            "no disponible",
        )
        self.assertFalse(
            any(caracter.isdigit() for caracter in campo_22["carga-sin-host"]),
            "el campo 22 no estima ningún número cuando la fuente falta",
        )

        print(
            "test_campo_22_lee_memoria_de_expertos_en_host: "
            f"linea='load_tensors: CUDA_Host model buffer size = "
            f"{MEMORIA_EXPERTOS_HOST}' campo22={campo_22['carga']!r} "
            f"draft_no_sumado=carga campo22_sin_linea="
            f"{campo_22['carga-sin-host']!r}"
        )


class LanzadorBatTest(unittest.TestCase):
    """Fija el lanzador `.bat` de `RF-001` y `CB-001` sobre `DEC-014`, `DEC-015` y `DEC-018`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.senuelo = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    @unittest.skipUnless(
        LANZADOR_BAT.exists() and all(ruta.exists() for ruta in ARTEFACTOS_REALES),
        "faltan el lanzador .bat o los 4 artefactos locales de los perfiles con borrador",
    )
    def test_bat_desde_directorio_ajeno(self):
        """Ejecuta el `.bat` real desde 1 directorio temporal con 1 señuelo.

        El señuelo ocupa la ruta relativa de los pesos dentro del directorio
        temporal; si el lanzador resolviera los artefactos desde el directorio
        actual, la comprobación 2 leería ese archivo señuelo y la salida
        nombraría una ruta bajo el directorio temporal. El intérprete se declara
        en `LLAMA_PYTHON` —vía 1 de `DEC-015`— con el `PATH` sin Python, y la
        ejecución no se omite cuando los artefactos existen: su plazo cubre la
        consulta de ayuda del binario. El perfil es `resiliencia`, cuyo
        `presupuesto_vram` de 4 claves mide `T-083` con el arranque de `ncmoe` `9` de
        `T-082` —`11263.21` MiB de pesos, `10.625` MiB de caché no-SWA por `1024`
        tokens, `159.38` MiB de caché SWA fija y `1661.77` MiB de buffer de cómputo—,
        es decir `13126.86` MiB para `4096` tokens efectivos, y el modo `comprobar`
        consulta la VRAM libre real por `nvidia-smi`, de modo que la comprobación 4 se
        resuelve `SUPERADA` con el cierre `5 de 5` cuando esa VRAM alcanza los `13127`
        MiB y `FALLIDA` con el código `6` cuando no alcanza; `PENDIENTE` deja de
        ser admisible en cuanto el bloque está completo, conforme a `DEC-018`.
        """
        ruta_senuelo = self.senuelo / RUTA_RELATIVA_PESOS
        ruta_senuelo.parent.mkdir(parents=True, exist_ok=True)
        ruta_senuelo.write_bytes(b"senuelo: no es 1 archivo GGUF")

        # Vía 1 de `DEC-015`: se declara el intérprete en `LLAMA_PYTHON` y se
        # retira Python del `PATH` para que la resolución no dependa de él.
        entorno = dict(os.environ)
        entorno["LLAMA_PYTHON"] = sys.executable
        entorno["PATH"] = os.pathsep.join(
            entrada
            for entrada in os.environ.get("PATH", "").split(os.pathsep)
            if "python" not in entrada.lower()
        )

        resultado = subprocess.run(
            [str(LANZADOR_BAT), "--perfil", "resiliencia", "--modo", "comprobar"],
            cwd=str(self.senuelo),
            env=entorno,
            capture_output=True,
            timeout=PLAZO_SEGUNDOS,
        )
        salida = resultado.stdout.decode("utf-8", "replace") + resultado.stderr.decode(
            "utf-8", "replace"
        )
        lineas = salida.splitlines()

        self.assertIn(
            resultado.returncode,
            (0, 6),
            "la comprobación previa resuelve con el código 0 de C-8 o con el 6 del presupuesto insuficiente",
        )

        lineas_interprete = [linea for linea in lineas if linea.startswith("Intérprete:")]
        self.assertEqual(
            1,
            len(lineas_interprete),
            "el .bat imprime 1 sola línea Intérprete: <ruta> (<vía>)",
        )
        linea_interprete = lineas_interprete[0]
        self.assertTrue(
            any(via in linea_interprete for via in VIAS_INTERPRETE),
            "la línea Intérprete nombra 1 de las 3 vías de DEC-015",
        )

        indice_comprobaciones = [
            indice
            for indice, linea in enumerate(lineas)
            if linea.startswith(("SUPERADA ", "FALLIDA ", "PENDIENTE "))
        ]
        self.assertTrue(indice_comprobaciones, "el orquestador imprime las comprobaciones")
        self.assertLess(
            lineas.index(linea_interprete),
            indice_comprobaciones[0],
            "Intérprete precede a la primera línea del orquestador",
        )

        cierres = [linea for linea in lineas if linea.startswith("COMPROBACIÓN PREVIA:")]
        self.assertEqual(
            1,
            len(cierres),
            "el orquestador imprime 1 sola línea de cierre de C-9",
        )
        self.assertFalse(
            [linea for linea in lineas if linea.startswith("PENDIENTE ")],
            "0 comprobaciones quedan pendientes: el bloque presupuesto_vram de "
            "resiliencia está completo desde T-083 y DEC-018 deja de admitir el estado",
        )

        superadas_4 = [linea for linea in lineas if linea.startswith("SUPERADA 4.")]
        fallidas_4 = [linea for linea in lineas if linea.startswith("FALLIDA 4.")]
        if superadas_4:
            self.assertEqual(
                1,
                len(superadas_4),
                "la comprobación 4 se declara 1 sola vez y superada",
            )
            self.assertEqual(
                [CIERRE_COMPLETO],
                cierres,
                "con la VRAM libre de la máquina el cierre es de 5 de 5",
            )
            self.assertEqual(
                0,
                resultado.returncode,
                "la comprobación previa superada devuelve el código 0 de C-8",
            )
            self.assertIn(
                "13127 MiB",
                superadas_4[0],
                "el detalle declara el presupuesto medido del perfil en MiB",
            )
            self.assertIn(
                "4096 tokens",
                superadas_4[0],
                "el detalle declara el contexto efectivo con el que arranca el servidor",
            )
            estado_4 = superadas_4[0]
        else:
            self.assertEqual(
                1,
                len(fallidas_4),
                "si la VRAM libre no alcanza, la comprobación 4 se resuelve fallida y no pendiente",
            )
            self.assertEqual(
                [CIERRE_FALLIDO],
                cierres,
                "con la comprobación 4 fallida el cierre declara 4 de 5 y ninguna pendiente",
            )
            self.assertEqual(
                6,
                resultado.returncode,
                "el presupuesto insuficiente devuelve el código 6 de C-8",
            )
            self.assertIn(
                "[ERROR] presupuesto de VRAM insuficiente",
                fallidas_4[0],
                "el detalle declara el presupuesto insuficiente frente a la VRAM libre real",
            )
            self.assertIn(
                "13127 MiB",
                fallidas_4[0],
                "el detalle declara el presupuesto medido del perfil en MiB",
            )
            self.assertIn(
                "4096 tokens",
                fallidas_4[0],
                "el detalle declara el contexto efectivo con el que arranca el servidor",
            )
            estado_4 = fallidas_4[0]

        for ruta_temporal in (str(self.senuelo), str(self.senuelo.resolve())):
            self.assertNotIn(
                ruta_temporal.lower(),
                salida.lower(),
                "0 rutas de la salida cuelgan del directorio temporal del señuelo",
            )

        print(
            "test_bat_desde_directorio_ajeno: "
            f"{linea_interprete} | cierre={cierres[0]} | "
            f"comprobacion4={estado_4} | codigo={resultado.returncode}"
        )

    def test_bat_sin_cabecera_de_produccion(self):
        """Comprueba el contenido del `.bat` sin ejecutarlo, según `DEC-014`."""
        self.assertTrue(
            LANZADOR_BAT.exists(),
            f"falta el lanzador .bat de DEC-014: {LANZADOR_BAT}",
        )
        texto = LANZADOR_BAT.read_text(encoding="utf-8")
        minusculas = texto.lower()

        self.assertNotIn(
            "línea base de producción",
            minusculas,
            "el .bat no declara la cabecera de producción de DEC-014",
        )
        self.assertNotIn(
            "perfil rendimiento máximo",
            minusculas,
            "el .bat no declara el perfil rendimiento máximo de DEC-014",
        )
        self.assertIn(
            "%~dp0",
            texto,
            "la raíz se resuelve desde la ubicación del propio archivo",
        )
        self.assertIn(
            "LLAMA_PYTHON",
            texto,
            "la vía 1 de DEC-015 es la variable de entorno LLAMA_PYTHON",
        )
        self.assertIn(
            "py.exe",
            texto,
            "la vía 2 de DEC-015 es %SystemRoot%\\py.exe con -3",
        )
        self.assertIn(
            "LOCALAPPDATA",
            texto,
            "la vía 3 de DEC-015 es la búsqueda bajo %LOCALAPPDATA%",
        )
        self.assertIn(
            "setlocal EnableExtensions",
            texto,
            "el .bat habilita las extensiones de cmd sin ocultar los errores",
        )
        self.assertIn(
            "Intérprete: ",
            texto,
            "el .bat imprime la línea Intérprete de DEC-015",
        )
        self.assertIn(
            "exit /b %errorlevel%",
            texto,
            "el .bat devuelve el código del orquestador sin reinterpretarlo",
        )
        self.assertNotIn(
            "llama-server.exe",
            minusculas,
            "0 rutas de artefactos en el .bat: las resuelve el orquestador",
        )
        self.assertNotIn(
            ".gguf",
            minusculas,
            "0 rutas de pesos en el .bat: las resuelve el orquestador",
        )
        self.assertNotIn(
            "..\\..\\bin",
            minusculas,
            "0 rutas de artefactos relativas al directorio actual",
        )
        self.assertNotIn(
            "..\\..\\models",
            minusculas,
            "0 rutas de pesos relativas al directorio actual",
        )

        lineas = [linea.strip() for linea in texto.splitlines() if linea.strip()]
        self.assertEqual(
            "exit /b %errorlevel%",
            lineas[-1],
            "el .bat termina devolviendo el código del orquestador",
        )


if __name__ == "__main__":
    unittest.main()
