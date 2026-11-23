"""Pruebas de los modos `servir` y `medir` del lanzador de SPEC-017.

Fijan la interfaz de `tools/gemma/lanzador.py` para `RF-004`, `RF-006`,
`RF-008`, `RF-009`, `RNF-004` y `RNF-007`, conforme a `CA-003`, `CA-005`,
`CA-007` y `CA-008`, sobre los contratos `C-5`, `C-6`, `C-8` y `C-9` de
`plan.md`, las decisiones `DEC-001`, `DEC-006`, `DEC-010`, `DEC-011`,
`DEC-018`, `DEC-020`, `DEC-021` y `DEC-022`, y los pasos 6 a 10 del flujo de una
ejecución:

- `--modo servir` ejecuta la comprobación previa completa, resuelve las
  opciones efectivas de `C-3` con `perfiles.resolver_opciones`, lanza el
  ejecutable del manifiesto con esas opciones, espera `GET /health` con la
  respuesta `ok` y el tiempo de carga en segundos, mide la memoria con
  `medir.medir_memoria` sobre el árbol del proceso, cierra el servidor y
  escribe 0 registros; devuelve el código de `C-8`.
- `--modo medir --prueba carga --calidad "<texto>"` hace lo anterior, ejecuta la
  sonda cuando la prueba la requiere y deja 1 registro propio de 21 campos con
  el tiempo de carga en segundos, la memoria en MiB, la estabilidad y la marca
  `no disponible` donde falta la fuente; `proposito` es `carga` y el código `0`.
- El manifiesto del árbol temporal declara su bloque `presupuesto_vram` medido
  —el estado que `T-036` dejó en el perfil `rendimiento`—, de modo que el cierre
  es `COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas` y la comprobación 4
  se declara superada con el contexto efectivo de `C-3` y la VRAM sintética. El
  caso del presupuesto pendiente restituye las 3 claves en `null` con la marca
  que nombra la tarea que lo escribe: su cierre es `4 de 5 …, 1 pendiente`, el
  código es `0`, 0 líneas declaran superada la comprobación 4 y el campo 21
  declara el presupuesto como `no disponible` sin estimarlo (`DEC-018` y
  `DEC-025`).
- Las opciones efectivas son las de `C-3` —valor inicial salvo comparación
  completa registrada— y el registro guarda la huella de las `opciones`
  declaradas y no la de las efectivas (`DEC-020`).
- Una prueba fallida no declara superado nada: si la sonda se corta o el
  servidor se detiene, el registro declara estabilidad `se detuvo` y la marca
  `no disponible` correspondiente.

Inyección: la suite levanta 1 servidor HTTP de prueba sobre 1 árbol temporal con
1 ejecutable señuelo y sustituye por dobles los 4 puntos inyectables que el
módulo expone como atributos de módulo —`MEDIR_MEMORIA`, `SONDEAR`,
`LANZAR_SERVIDOR`, y las constantes `URL_BASE` y `PUERTO`—, además de la
consulta de la ayuda del binario, la lectura de su versión y la lectura de los
metadatos del GGUF. Ningún caso invoca `nvidia-smi`, `powershell.exe`, la GPU ni
el binario real, conforme a `DEC-012`.
"""

import contextlib
import http.server
import io
import json
import os
import re
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"

PERFIL = "rendimiento"

# Los 4 modos de `C-8`: esta suite ejerce `servir` y `medir`.
MODO_SERVIR = "servir"
MODO_MEDIR = "medir"

# Forma que el binario enumera para cada eje, según el doble de `T-014`.
OPCIONES_ACEPTADAS = {
    "gpu_layers": "--n-gpu-layers",
    "flash_attn": "--flash-attn",
    "ctx_size": "--ctx-size",
    "ubatch": "--ubatch-size",
    "ncmoe": "--n-cpu-moe",
    "load_mode": "--load-mode",
    "parallel": "--parallel",
}

VERSION_BINARIO = "b8796"
COMMIT_LLAMA_CPP = "3f6b1d1a0"

# Valores sintéticos en MiB de la medición de memoria: nunca son 1 medición real
# de la máquina y la VRAM libre cubre el presupuesto completo del caso de 5 de 5.
MEMORIA_SINTETICA = {
    "codigo": 0,
    "vram_total_mib": 16311,
    "vram_usada_mib": 14872,
    "vram_libre_mib": 1449,
    "residente_mib": 2410,
    "desbordamiento_mib": 0,
    "contador_desbordamiento": r"\GPU Process Memory(*)\Shared Usage",
}

# Resultado sintético de la sonda de `DEC-011` cuando el servidor continúa.
SONDA_SUPERADA = {
    "estado": "superada",
    "fragmentos": 2400,
    "tokens_generados": 2400,
    "tokens_por_segundo": 42.5,
    "servidor": "continúa en servicio",
}

# Resultado sintético de la sonda cuando la transcripción se corta: la prueba es
# fallida, no declara velocidad y el servidor se detuvo, conforme a `CB-003`.
SONDA_FALLIDA = {
    "estado": "fallida",
    "fragmentos": 1200,
    "tokens_generados": 1200,
    "tokens_por_segundo": None,
    "servidor": "se detuvo",
    "motivo": "transcripción cortada por la detención del servidor",
}

# Cierre de `C-9` con la comprobación 4 en `PENDIENTE` (`DEC-018`) y con el
# bloque `presupuesto_vram` completo.
CIERRE_PENDIENTE = "COMPROBACIÓN PREVIA: 4 de 5 comprobaciones superadas, 1 pendiente"
CIERRE_COMPLETO = "COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas"

# Presupuesto completo del caso de 5 de 5: consumo de 238 MiB para los 131072
# tokens de contexto declarados en el manifiesto, que cabe en la VRAM libre
# sintética menos el margen de `RNF-007`.
PRESUPUESTO_COMPLETO = {
    "pesos_en_vram_mib": 100,
    "kv_por_1024_tokens_mib": 1,
    "buffer_computo_mib": 10,
}

NO_DISPONIBLE = "no disponible"

# Las 21 etiquetas de `C-6`, en el orden de `RF-006`.
CAMPOS_C6 = (
    "Fecha de la prueba",
    "Nombre de la prueba",
    "Versión del binario",
    "Commit de llama.cpp",
    "Modelo y cuantización",
    "Contexto configurado",
    "Ranuras del servidor",
    "Capas de expertos en CPU",
    "Micro-lote",
    "Atención rápida",
    "Decodificación especulativa",
    "Tiempo de carga",
    "VRAM asignada",
    "VRAM libre",
    "RAM utilizada",
    "Velocidad de prompt",
    "Velocidad de generación",
    "Estabilidad del servidor",
    "Desbordamiento hacia memoria compartida",
    "Calidad funcional de la respuesta",
    "Errores y advertencias",
)

PATRON_TIEMPO_CARGA = re.compile(r"^\d+\.\d+ s$")
PATRON_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CALIDAD = "respuesta correcta y completa"


class _ManejadorSalud(http.server.BaseHTTPRequestHandler):
    """Servidor HTTP de prueba: solo `GET /health` responde `ok`.

    La sonda se sustituye por 1 doble, de modo que el camino `POST` no se
    ejerce y no necesita respuesta. Cada consulta de salud suma en el contador
    del servidor para acreditar que el lanzador esperó esa ruta.
    """

    def do_GET(self):  # noqa: N802 - nombre impuesto por BaseHTTPRequestHandler
        ruta = self.path.split("?", 1)[0]
        if ruta == "/health":
            self.server.salud_consultas += 1
            cuerpo = json.dumps({"status": "ok"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)
            return
        self.send_error(404)

    def do_POST(self):  # noqa: N802 - nombre impuesto por BaseHTTPRequestHandler
        self.send_error(404)

    def log_message(self, formato, *argumentos):
        """Silencia el registro del servidor de prueba."""


class _ServidorPrueba:
    """Servidor HTTP de prueba sobre 1 puerto efímero de la interfaz local."""

    def __init__(self):
        self.httpd = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), _ManejadorSalud
        )
        self.httpd.daemon_threads = True
        self.httpd.salud_consultas = 0
        self.hilo = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.hilo.start()

    @property
    def puerto(self):
        return self.httpd.server_address[1]

    @property
    def salud_consultas(self):
        return self.httpd.salud_consultas

    @property
    def cerrado(self):
        return self.httpd.socket.fileno() == -1

    def cerrar(self):
        if self.cerrado:
            return
        self.httpd.shutdown()
        self.httpd.server_close()
        self.hilo.join(5)


class _ProcesoDoble:
    """Doble del servidor lanzado: identificador, actividad y cierre.

    `cerrar` apaga el servidor HTTP de prueba, de modo que la prueba acredita
    que el lanzador lo cierra y que después no acepta conexiones.
    """

    def __init__(self, servidor):
        self.pid = os.getpid()
        self._servidor = servidor
        self.cerrado = False
        self.consultas_activo = 0

    def activo(self):
        self.consultas_activo += 1
        return not self.cerrado

    def cerrar(self):
        self.cerrado = True
        self._servidor.cerrar()


class _LanzarDoble:
    """Doble de `LANZAR_SERVIDOR` que registra ejecutable y argumentos."""

    def __init__(self, proceso):
        self.proceso = proceso
        self.llamadas = []

    def __call__(self, ejecutable, argumentos):
        self.llamadas.append(
            {
                "ejecutable": Path(ejecutable),
                "argumentos": [str(argumento) for argumento in argumentos],
            }
        )
        return self.proceso


class _MedirDoble:
    """Doble de `MEDIR_MEMORIA` con valores sintéticos en MiB."""

    def __init__(self):
        self.llamadas = []
        self.resultado = dict(MEMORIA_SINTETICA)

    def __call__(self, pids, **kwargs):
        self.llamadas.append({"pids": list(pids), "kwargs": dict(kwargs)})
        return dict(self.resultado)


class _SondaDoble:
    """Doble de `SONDEAR` que registra la URL base y devuelve 1 resultado fijo."""

    def __init__(self):
        self.llamadas = []
        self.resultado = dict(SONDA_SUPERADA)

    def __call__(self, base_url, **kwargs):
        self.llamadas.append({"base_url": base_url, "kwargs": dict(kwargs)})
        return dict(self.resultado)


def _cargar_modulo():
    """Importa el módulo bajo prueba como `lanzador` desde `tools/gemma/`."""
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import lanzador

    return lanzador


def _manifiesto_versionado():
    """Lee el manifiesto versionado del perfil `rendimiento`."""
    return json.loads(
        (DIRECTORIO_PERFILES / (PERFIL + ".json")).read_text(encoding="utf-8")
    )


def _marca_pendiente_de_resiliencia():
    """Marca `pendiente` del perfil que aún no escribe su presupuesto.

    `T-057` devolvió el bloque `presupuesto_vram` de `resiliencia` a `pendiente`
    conforme a `DEC-025`, y la marca nombra la tarea que lo escribe; la prueba la
    lee del manifiesto y no de 1 literal del código.
    """
    manifiesto = json.loads(
        (DIRECTORIO_PERFILES / "resiliencia.json").read_text(encoding="utf-8")
    )
    return manifiesto["presupuesto_vram"]["pendiente"]


# Marca real del perfil con el presupuesto devuelto a `pendiente` por `DEC-025`.
MARCA_PENDIENTE = _marca_pendiente_de_resiliencia()


def _lineas_frontmatter(texto):
    """Pares `clave: valor` del bloque delimitado por `---`."""
    lineas = texto.splitlines()
    cierre = lineas.index("---", 1)
    pares = {}
    for linea in lineas[1:cierre]:
        if not linea.strip():
            continue
        clave, _, valor = linea.partition(":")
        pares[clave.strip()] = valor.strip()
    return pares


def _filas_del_archivo(texto):
    """Filas de la tabla del registro como `(numero, campo, valor)`."""
    filas = []
    for linea in texto.splitlines():
        recortada = linea.strip()
        if not recortada.startswith("|"):
            continue
        celdas = [celda.strip() for celda in recortada.strip("|").split("|")]
        if len(celdas) < 3 or not celdas[0].isdigit():
            continue
        filas.append((int(celdas[0]), celdas[1], celdas[2]))
    return filas


class ModosTest(unittest.TestCase):
    """Fija los modos `servir` y `medir` del lanzador sobre `C-5`, `C-6` y `C-9`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)

        self.manifiesto = _manifiesto_versionado()
        self.directorio_perfiles = self.raiz / "src" / "gemma" / "perfiles"
        self.directorio_perfiles.mkdir(parents=True, exist_ok=True)
        self._escribir_manifiesto(self.manifiesto)

        # `T-036` midió el bloque `presupuesto_vram` del perfil: el estado por defecto
        # de los modos es el de 1 presupuesto medido, que es el que el `rendimiento`
        # versionado declara. El caso del presupuesto pendiente lo restituye con su
        # marca dentro de su propia prueba, conforme a `DEC-018` y `DEC-025`.
        self._completar_presupuesto()

        # Ejecutable, modelo, proyector y draft señuelo: la comprobación 1 de
        # `C-9` solo contrasta su existencia y ninguno se ejecuta.
        for relativa in self.manifiesto["artefactos"].values():
            if relativa is None:
                continue
            ruta = self.raiz / relativa
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(b"senuelo: no es 1 artefacto real")

        self.servidor = _ServidorPrueba()
        self.addCleanup(self.servidor.cerrar)

        self.modulo = _cargar_modulo()
        import binario
        import gguf

        self.medir = _MedirDoble()
        self.sonda = _SondaDoble()
        self.proceso = _ProcesoDoble(self.servidor)
        self.lanzar = _LanzarDoble(self.proceso)

        self._pila = contextlib.ExitStack()
        self.addCleanup(self._pila.close)
        self._pila.enter_context(
            mock.patch.object(self.modulo, "MEDIR_MEMORIA", self.medir)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "SONDEAR", self.sonda)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "LANZAR_SERVIDOR", self.lanzar)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "URL_BASE", "http://127.0.0.1")
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "PUERTO", self.servidor.puerto)
        )
        self._pila.enter_context(
            mock.patch.object(
                binario,
                "opciones_aceptadas",
                lambda ejecutable: dict(OPCIONES_ACEPTADAS),
            )
        )
        self._pila.enter_context(
            mock.patch.object(
                binario,
                "leer_version",
                lambda ejecutable: {
                    "version": VERSION_BINARIO,
                    "commit": COMMIT_LLAMA_CPP,
                },
            )
        )
        self._pila.enter_context(
            mock.patch.object(gguf, "leer_metadatos", self._metadatos)
        )

    def tearDown(self):
        self._pila.close()
        self.servidor.cerrar()
        self._temporal.cleanup()

    def _metadatos(self, ruta):
        """Doble del lector GGUF: devuelve las 2 señales de `DEC-019`.

        El perfil declara `tipo_gguf` en `null` y las 2 señales de identidad
        —`nombre_gguf` y `tamano_bytes`— coinciden, de modo que la comprobación
        2 de `C-9` se declara superada sin leer el archivo real.
        """
        cuantizacion = self._manifiesto()["cuantizacion"]
        return {
            "nombre": cuantizacion["nombre_gguf"],
            "file_type": cuantizacion["tipo_gguf"],
            "tamano_bytes": cuantizacion["tamano_bytes"],
        }

    def _manifiesto(self):
        """Lee el manifiesto del árbol temporal, que puede haberse completado."""
        ruta = self.directorio_perfiles / (PERFIL + ".json")
        return json.loads(ruta.read_text(encoding="utf-8"))

    def _escribir_manifiesto(self, manifiesto):
        """Escribe el manifiesto del árbol temporal con la forma versionada."""
        (self.directorio_perfiles / (PERFIL + ".json")).write_text(
            json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _completar_presupuesto(self):
        """Sustituye el bloque `presupuesto_vram` pendiente por 1 bloque medido."""
        manifiesto = self._manifiesto()
        manifiesto["presupuesto_vram"] = dict(PRESUPUESTO_COMPLETO)
        self._escribir_manifiesto(manifiesto)

    def _ejecutar(self, argumentos):
        """Invoca `main` capturando las 2 salidas y devuelve el código real."""
        salida = io.StringIO()
        errores = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = self.modulo.main(argumentos)
        self.assertIsInstance(
            codigo,
            int,
            "main devuelve el código de C-8 como entero y no termina por sys.exit",
        )
        return codigo, salida.getvalue(), errores.getvalue()

    def _texto(self, salida, errores):
        return salida + errores

    def _argumentos_lanzados(self):
        self.assertEqual(
            1,
            len(self.lanzar.llamadas),
            "el lanzador lanza el ejecutable del manifiesto 1 sola vez",
        )
        return self.lanzar.llamadas[0]["argumentos"]

    def _efectivas(self):
        import perfiles

        return perfiles.resolver_opciones(self.manifiesto, {})

    def _registros(self):
        return sorted(
            (self.raiz / "results" / "gemma" / PERFIL).glob("*.md")
        )

    def _unico_registro(self):
        rutas = self._registros()
        self.assertEqual(
            1,
            len(rutas),
            "el modo medir deja 1 registro propio en el árbol temporal",
        )
        texto = rutas[0].read_text(encoding="utf-8")
        return rutas[0], _lineas_frontmatter(texto), _filas_del_archivo(texto)

    def test_modo_servir_espera_salud_y_cierra(self):
        codigo, salida, errores = self._ejecutar(
            ["--raiz", str(self.raiz), "--perfil", PERFIL, "--modo", MODO_SERVIR]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "el modo servir superado devuelve el código 0 de C-8",
        )

        llamada = self.lanzar.llamadas[0] if self.lanzar.llamadas else None
        self.assertIsNotNone(llamada, "el modo servir lanza el ejecutable")
        self.assertEqual(
            (self.raiz / self.manifiesto["artefactos"]["ejecutable"]).resolve(),
            llamada["ejecutable"].resolve(),
            "el ejecutable lanzado es el de artefactos.ejecutable resuelto contra la raíz",
        )

        argumentos = self._argumentos_lanzados()
        efectivas = self._efectivas()["opciones"]
        self.assertEqual(
            4096,
            efectivas["ctx_size"],
            "las desviaciones sin comparación conservan el valor inicial de C-3",
        )
        for forma, valor in (
            ("--n-gpu-layers", efectivas["gpu_layers"]),
            ("--flash-attn", efectivas["flash_attn"]),
            ("--ctx-size", efectivas["ctx_size"]),
            ("--ubatch-size", efectivas["ubatch"]),
            ("--n-cpu-moe", efectivas["ncmoe"]),
            ("--parallel", efectivas["parallel"]),
        ):
            self.assertIn(forma, argumentos, f"el lanzamiento declara {forma}")
            self.assertIn(
                str(valor),
                argumentos,
                f"el lanzamiento aplica el valor efectivo de {forma}",
            )
        self.assertNotIn(
            "131072",
            argumentos,
            "el lanzamiento no aplica la desviación de ctx_size sin comparación",
        )
        self.assertIn("--host", argumentos)
        self.assertIn("127.0.0.1", argumentos)
        self.assertIn("--port", argumentos)
        self.assertIn(
            str(self.servidor.puerto),
            argumentos,
            "el lanzamiento declara el puerto de la constante PUERTO",
        )
        self.assertTrue(
            any(argumento.endswith(".gguf") for argumento in argumentos),
            "el lanzamiento declara la ruta absoluta del archivo de pesos",
        )

        self.assertGreaterEqual(
            self.servidor.salud_consultas,
            1,
            "el modo servir espera GET /health antes de medir la memoria",
        )
        self.assertEqual(
            2,
            len(self.medir.llamadas),
            "el modo servir mide la VRAM en la comprobación previa y la memoria al servir",
        )
        self.assertEqual(
            [os.getpid()],
            self.medir.llamadas[0]["pids"],
            "la comprobación 4 mide la VRAM del proceso del lanzador",
        )
        self.assertEqual(
            [self.proceso.pid],
            self.medir.llamadas[-1]["pids"],
            "la medición del servicio recibe el árbol del proceso del servidor",
        )
        self.assertTrue(self.proceso.cerrado, "el modo servir cierra el servidor")
        self.assertTrue(
            self.servidor.cerrado,
            "tras el cierre el servidor de prueba ya no acepta conexiones",
        )
        self.assertEqual(
            [],
            self._registros(),
            "el modo servir no escribe registro alguno",
        )
        self.assertFalse(
            (self.raiz / "results").exists(),
            "el modo servir no crea la carpeta de registros",
        )
        self.assertEqual([], self.sonda.llamadas, "el modo servir no ejecuta la sonda")
        self.assertIn(CIERRE_COMPLETO, texto)
        self.assertIn("SUPERADA 4.", texto)

        print(
            "test_modo_servir_espera_salud_y_cierra: "
            f"codigo={codigo} salud={self.servidor.salud_consultas} "
            f"memoria={[llamada['pids'] for llamada in self.medir.llamadas]} "
            f"cerrado={self.proceso.cerrado} registros={len(self._registros())}"
        )

    def test_modo_medir_crea_registro_de_21_campos(self):
        codigo, salida, errores = self._ejecutar(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                PERFIL,
                "--modo",
                MODO_MEDIR,
                "--prueba",
                "carga",
                "--calidad",
                CALIDAD,
            ]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(0, codigo, "el modo medir superado devuelve el código 0")
        self.assertEqual(
            1,
            len(self.sonda.llamadas),
            "la prueba de carga requiere la sonda de RF-009 y se ejecuta 1 vez",
        )
        self.assertEqual(
            f"http://127.0.0.1:{self.servidor.puerto}",
            self.sonda.llamadas[0]["base_url"],
            "la sonda recibe la URL base y el puerto de las constantes del módulo",
        )
        self.assertTrue(self.servidor.cerrado, "el modo medir cierra el servidor")

        ruta, frontmatter, filas = self._unico_registro()
        self.assertEqual(
            [numero for numero, _, _ in filas],
            list(range(1, 22)),
            "el registro declara las 21 filas de C-6 en el orden de RF-006",
        )
        self.assertEqual([campo for _, campo, _ in filas], list(CAMPOS_C6))

        valores = {numero: valor for numero, _, valor in filas}
        self.assertEqual("carga", frontmatter["proposito"])
        self.assertRegex(valores[1], PATRON_FECHA)
        self.assertEqual("carga", valores[2])
        self.assertEqual(VERSION_BINARIO, valores[3])
        self.assertEqual(COMMIT_LLAMA_CPP, valores[4])
        self.assertEqual("4096 tokens", valores[6])
        self.assertEqual("1 ranuras", valores[7])
        self.assertEqual("0 capas", valores[8])
        self.assertEqual("512 tokens", valores[9])
        self.assertRegex(
            valores[12],
            PATRON_TIEMPO_CARGA,
            "el tiempo de carga se declara en segundos y con su unidad",
        )
        self.assertGreaterEqual(float(valores[12].split(" ")[0]), 0.0)
        self.assertEqual(
            f"{MEMORIA_SINTETICA['vram_usada_mib']} MiB", valores[13]
        )
        self.assertEqual(f"{MEMORIA_SINTETICA['vram_libre_mib']} MiB", valores[14])
        self.assertEqual(f"{MEMORIA_SINTETICA['residente_mib']} MiB", valores[15])
        self.assertEqual(NO_DISPONIBLE, valores[16])
        self.assertEqual(
            f"{SONDA_SUPERADA['tokens_por_segundo']:.2f} tokens/s", valores[17]
        )
        self.assertEqual("continúa en servicio", valores[18])
        self.assertEqual(
            f"{MEMORIA_SINTETICA['desbordamiento_mib']} MiB", valores[19]
        )
        self.assertEqual(CALIDAD, valores[20])
        self.assertEqual("sin errores", valores[21])

        import perfiles

        self.assertEqual(
            perfiles.huella_opciones(self.manifiesto["opciones"]),
            frontmatter["huella_opciones"],
            "la huella del registro es la de las opciones declaradas (DEC-020)",
        )
        self.assertEqual(
            self._efectivas()["opciones"],
            json.loads(frontmatter["opciones_efectivas"]),
            "el frontmatter transcribe las opciones efectivas de C-3",
        )
        self.assertEqual(
            4096,
            json.loads(frontmatter["opciones_efectivas"])["ctx_size"],
            "las opciones efectivas conservan el valor inicial de C-3",
        )
        self.assertEqual(
            str(MEMORIA_SINTETICA["vram_total_mib"]), frontmatter["vram_total_mib"]
        )
        self.assertEqual("ninguno", frontmatter["registro_anterior"])
        self.assertIn(CIERRE_COMPLETO, texto)
        self.assertEqual(ruta.parent, self.raiz / "results" / "gemma" / PERFIL)

        print(
            "test_modo_medir_crea_registro_de_21_campos: registro="
            f"{ruta.stem} campos={len(filas)} carga={valores[12]} "
            f"proposito={frontmatter['proposito']} codigo={codigo}"
        )

    def test_cierre_cuatro_de_cinco_con_presupuesto_pendiente(self):
        # El caso del presupuesto pendiente se construye sobre el manifiesto temporal
        # con la marca que nombra la tarea que lo escribe: el bloque queda en `null`
        # sin estimar ningún valor, conforme a `DEC-018` y `DEC-025`.
        manifiesto = self._manifiesto()
        manifiesto["presupuesto_vram"] = {
            "pesos_en_vram_mib": None,
            "kv_por_1024_tokens_mib": None,
            "buffer_computo_mib": None,
            "pendiente": MARCA_PENDIENTE,
        }
        self._escribir_manifiesto(manifiesto)

        codigo, salida, errores = self._ejecutar(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                PERFIL,
                "--modo",
                MODO_MEDIR,
                "--prueba",
                "carga",
            ]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(0, codigo, "1 presupuesto pendiente no es 1 fallo de C-8")
        self.assertIn(CIERRE_PENDIENTE, texto)
        self.assertNotIn("SUPERADA 4.", texto)
        self.assertIn("PENDIENTE 4.", texto)
        self.assertIn(
            MARCA_PENDIENTE,
            texto,
            "el detalle de la comprobación 4 nombra la tarea leída de la marca",
        )

        _, _, filas = self._unico_registro()
        campo_21 = {numero: valor for numero, _, valor in filas}[21]
        self.assertIn(
            NO_DISPONIBLE,
            campo_21,
            "el campo 21 declara el presupuesto como no disponible",
        )
        self.assertIsNone(
            re.search(r"\d", campo_21),
            f"el campo 21 no estima el presupuesto: {campo_21!r}",
        )

        print(
            "test_cierre_cuatro_de_cinco_con_presupuesto_pendiente: "
            f"cierre={CIERRE_PENDIENTE} campo21={campo_21!r} codigo={codigo}"
        )

    def test_cierre_cinco_de_cinco_con_bloque_completo(self):
        self._completar_presupuesto()

        codigo, salida, errores = self._ejecutar(
            ["--raiz", str(self.raiz), "--perfil", PERFIL, "--modo", MODO_SERVIR]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(0, codigo, "el presupuesto completo y suficiente devuelve 0")
        self.assertIn(CIERRE_COMPLETO, texto)
        self.assertIn("SUPERADA 4.", texto)
        self.assertNotIn("pendiente", texto.lower())
        self.assertEqual([], self._registros(), "el modo servir no escribe registro")

        print(
            "test_cierre_cinco_de_cinco_con_bloque_completo: "
            f"cierre={CIERRE_COMPLETO} codigo={codigo}"
        )

    def test_registro_de_prueba_fallida_no_promueve(self):
        self.sonda.resultado = dict(SONDA_FALLIDA)

        codigo, salida, errores = self._ejecutar(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                PERFIL,
                "--modo",
                MODO_MEDIR,
                "--prueba",
                "carga",
                "--calidad",
                CALIDAD,
            ]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(0, codigo, "la ejecución terminó y dejó su registro")
        self.assertIn(CIERRE_COMPLETO, texto)

        ruta, _, filas = self._unico_registro()
        valores = {numero: valor for numero, _, valor in filas}
        self.assertEqual("se detuvo", valores[18])
        self.assertEqual(NO_DISPONIBLE, valores[17])
        self.assertIn(SONDA_FALLIDA["motivo"], valores[21])
        for _, _, valor in filas:
            self.assertNotIn(
                "superad",
                valor.lower(),
                "1 prueba fallida no declara superado nada en el registro",
            )

        print(
            "test_registro_de_prueba_fallida_no_promueve: registro="
            f"{ruta.stem} estabilidad={valores[18]} generacion={valores[17]}"
        )


if __name__ == "__main__":
    unittest.main()
