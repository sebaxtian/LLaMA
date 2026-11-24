r"""Pruebas en rojo de la sonda de contexto sostenido de SPEC-017.

Fijan la interfaz de `tools/gemma/probe.py` para `RF-009` y `CB-003` conforme a
`CA-008`, `DEC-011` y `DEC-012`, sobre el contrato que `T-021` acreditó con el
binario real sobre la máquina objetivo:

- La ruta primaria es `POST /completion`; `POST /v1/completions` responde como
  alternativa. Con `stream` verdadero la respuesta llega como fragmentos
  `data: {json}` y el último fragmento antes de `data: [DONE]` declara el
  bloque `timings` con `prompt_n`, `prompt_ms`, `prompt_per_token_ms`,
  `prompt_per_second`, `predicted_n`, `predicted_ms`,
  `predicted_per_token_ms`, `predicted_per_second` y `cache_n`.
- De ese bloque, `DEC-011` toma los tokens generados y la velocidad; el cierre
  de la prueba se comprueba con `GET /health`, y la detención del servidor se
  clasifica como prueba fallida con el número de tokens contados hasta el
  corte, que es lo que `CB-003` exige registrar.

Interfaz que fija esta suite:

- `sondear(base_url, *, cliente=None, tokens_objetivo=2400) -> dict`, donde
  `base_url` es el punto de acceso del servidor y `cliente` es 1 objeto
  inyectable con 2 métodos: `post_flujo(ruta, cuerpo) -> iterable de líneas`,
  que emite las líneas SSE recibidas y lanza `ConnectionError` o `OSError` si
  el servidor se detiene, y `get(ruta) -> (codigo_http, texto)`. Las pruebas
  siempre inyectan el doble; el cliente real con `urllib.request` corresponde
  a `T-023`, y ningún caso de esta suite abre 1 socket, lanza el servidor ni
  lee `bin/`, `models/` o la GPU.
- 1 sola llamada a `post_flujo`, a la ruta `/completion`, con `stream`
  verdadero, `n_predict` igual a `tokens_objetivo` —2400 por defecto y nunca
  menos de 2400—, 1 prompt fijo e `ignore_eos` verdadero, conforme a
  `DEC-011`.
- Resultado con las claves `estado` en `superada` o `fallida`, `fragmentos`
  con el número de fragmentos de contenido no vacío, `tokens_generados`,
  `tokens_por_segundo` leído de `timings.predicted_per_second` o `None` cuando
  el bloque no aparece, y `servidor` en `continúa en servicio` o `se detuvo`.
  En `fallida` añade `motivo` de texto no vacío, y `tokens_generados` conserva
  el número contado hasta el corte.
- La única solicitud declara `ignore_eos` verdadero, además de `prompt`,
  `n_predict` y `stream`: la generación llega a `n_predict` y no se detiene en
  el token de fin de turno, que es lo que la ejecución real sobre la máquina
  objetivo acreditó con `stop processing: n_tokens = 916, truncated = 0` y 908
  tokens generados de 2400 pedidos. El indicador va en la petición y no en el
  manifiesto del perfil.
- El final del flujo se clasifica por `timings` y no por `[DONE]`: si el flujo
  termina y el fragmento final declara `timings`, el estado es `superada`
  aunque no llegue `data: [DONE]`, que es la forma real de 909 líneas con la
  última vacía. Si la transcripción se corta sin `timings`, el estado es
  `fallida` con el número de tokens contados, `tokens_por_segundo` en `None` y
  1 `motivo` que nombra el corte con la raíz `cort`; nada se promueve. Si llega
  a `[DONE]` sin bloque `timings`, el estado es `fallida` con
  `tokens_generados` por conteo de fragmentos, `tokens_por_segundo` en `None` y
  1 `motivo` que nombra `timings`, conforme al riesgo de `DEC-011` sobre el
  binario sin bloque. La falta de `[DONE]` con `timings` no produce `fallida`.
- La sonda no escribe registro ni archivo alguno y no toca `results/`: la
  carpeta de registros la escribe la campaña del operador local, no la sonda.

Los fragmentos y el bloque `timings` son sintéticos; sus 2 valores afirmados
—`predicted_n` 8 y `predicted_per_second` 94.8908077918909— son los que `T-021`
transcribió del binario, y las claves restantes del bloque replican la forma
real sin que la suite afirme su valor. Estas pruebas se ejecutan en rojo
mientras `T-023` no escriba el módulo: la importación de `probe` falla con
`ModuleNotFoundError` y cada caso declara el módulo ausente. Los dobles son
puros en memoria y el único caso con árbol temporal lo construye bajo `tmp/`
con `tempfile`, conforme a `DEC-012`.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"

BASE_URL = "http://127.0.0.1:8080"
RUTA_COMPLETION = "/completion"
RUTA_SALUD = "/health"

# `DEC-011` fija al menos 2400 tokens; el valor por defecto nunca es menor.
TOKENS_OBJETIVO = 2400

ESTADO_SUPERADA = "superada"
ESTADO_FALLIDA = "fallida"
SERVIDOR_EN_SERVICIO = "continúa en servicio"
SERVIDOR_DETENIDO = "se detuvo"

CLAVES_RESULTADO = {
    "estado",
    "fragmentos",
    "tokens_generados",
    "tokens_por_segundo",
    "servidor",
}

# `predicted_n` y `predicted_per_second` son los transcritos por `T-021` para 8
# tokens generados; las demás claves replican la forma del bloque real con
# valores derivados de esas 2 cifras y no se afirman en ningún caso.
PREDICTED_N = 8
PREDICTED_PER_SECOND = 94.8908077918909
TIMINGS = {
    "prompt_n": 5,
    "prompt_ms": 509.552,
    "prompt_per_token_ms": 101.91,
    "prompt_per_second": 9.812502698438243,
    "predicted_n": PREDICTED_N,
    "predicted_ms": 84.307,
    "predicted_per_token_ms": 10.538,
    "predicted_per_second": PREDICTED_PER_SECOND,
    "cache_n": 0,
}

# Fila 16 de `C-6`: `prompt_per_second` del mismo bloque sintético, que `T-051`
# exige devolver como `velocidad_prompt_tokens_por_segundo` y que
# `lanzador._velocidad_de_prompt` ya lee.
PROMPT_PER_SECOND = 9.812502698438243

SALUD_OK = (200, '{"status":"ok"}')


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/probe.py` no exista,
    que es el rojo declarado de `T-022`; `T-023` cierra el caso. No se crea
    `tools/gemma/__init__.py`: el módulo se importa como `probe` con el
    directorio `tools/gemma/` en `sys.path`, igual que las suites existentes.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import probe

    return probe


def _linea(payload):
    """Línea SSE con la forma `data: {json}` que emite el servidor."""
    return "data: " + json.dumps(payload, ensure_ascii=False)


def _fragmento(texto):
    """Fragmento de contenido con 1 token de texto."""
    return _linea({"content": texto, "stop": False})


def _flujo(*, fragmentos, con_timings=True, con_cierre=True):
    """Flujo SSE sintético con fragmentos de contenido y cierre opcionales.

    Con `con_timings`, el último fragmento declara el bloque `timings` con el
    contenido vacío, de modo que no suma fragmento ni token por conteo. Con
    `con_cierre`, la última línea es `data: [DONE]`, igual que el binario real
    de `T-021`; sin ella la transcripción queda cortada.
    """
    lineas = [_fragmento(f"token{i} ") for i in range(fragmentos)]
    if con_timings:
        lineas.append(_linea({"content": "", "stop": True, "timings": TIMINGS}))
    if con_cierre:
        lineas.append("data: [DONE]")
    return lineas


class ClienteDoble:
    """Doble puro en memoria del cliente HTTP de la sonda.

    Registra cada llamada recibida y devuelve el flujo y la salud sintéticos
    que el caso declara, sin abrir socket alguno. `post_flujo` devuelve 1
    iterable de líneas; `get` devuelve la tupla `(codigo_http, texto)` o lanza
    `ConnectionError` cuando el caso declara el servidor detenido, conforme al
    contrato del cliente que `T-023` implementa.
    """

    def __init__(self, flujo, *, salud=SALUD_OK, servidor_detenido=False):
        self.flujo = list(flujo)
        self.salud = salud
        self.servidor_detenido = servidor_detenido
        self.llamadas_post = []
        self.llamadas_get = []

    def post_flujo(self, ruta, cuerpo):
        self.llamadas_post.append((ruta, dict(cuerpo)))
        return iter(self.flujo)

    def get(self, ruta):
        self.llamadas_get.append(ruta)
        if self.servidor_detenido:
            raise ConnectionError(
                f"el servidor no responde en {BASE_URL}{ruta}"
            )
        return self.salud


class CasoDeSonda(unittest.TestCase):
    """Base con la comprobación común de las claves del resultado."""

    def verificar_resultado(self, resultado, estado):
        """Comprueba las claves del contrato y el estado declarado."""
        self.assertIsInstance(resultado, dict)
        self.assertTrue(
            CLAVES_RESULTADO.issubset(resultado),
            f"faltan claves del resultado: {sorted(CLAVES_RESULTADO - set(resultado))}",
        )
        self.assertEqual(resultado["estado"], estado)
        self.assertIn(resultado["servidor"], {SERVIDOR_EN_SERVICIO, SERVIDOR_DETENIDO})
        self.assertIsInstance(resultado["fragmentos"], int)
        self.assertIsInstance(resultado["tokens_generados"], int)
        if estado == ESTADO_FALLIDA:
            self.assertIsInstance(resultado.get("motivo"), str)
            self.assertTrue(
                resultado["motivo"].strip(),
                "1 prueba fallida declara 1 motivo no vacío",
            )


class SolicitudUnicaTest(CasoDeSonda):
    """`RF-009`: 1 sola solicitud de 2400 tokens sobre la ruta primaria."""

    def test_una_sola_solicitud_de_2400_tokens(self):
        modulo = _cargar_modulo()
        doble = ClienteDoble(_flujo(fragmentos=PREDICTED_N))

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.assertEqual(len(doble.llamadas_post), 1)
        ruta, cuerpo = doble.llamadas_post[0]
        self.assertEqual(ruta, RUTA_COMPLETION)
        self.assertNotEqual(ruta, "/v1/completions")
        self.assertIs(cuerpo["stream"], True)
        self.assertEqual(cuerpo["n_predict"], TOKENS_OBJETIVO)
        self.assertGreaterEqual(cuerpo["n_predict"], 2400)
        self.assertIsInstance(cuerpo.get("prompt"), str)
        self.assertTrue(cuerpo["prompt"].strip())
        self.verificar_resultado(resultado, ESTADO_SUPERADA)
        self.assertEqual(resultado["tokens_generados"], PREDICTED_N)

    def test_solicitud_declara_ignore_eos(self):
        """`CA-008`: la solicitud ignora el fin de turno y agota `n_predict`.

        La ejecución real sobre la máquina objetivo generó 908 de 2400 tokens y
        el servidor cerró con `stop processing: n_tokens = 916, truncated = 0`
        al detenerse en el token de fin de turno; con `ignore_eos` verdadero en
        la petición la generación llega al objetivo de `DEC-011`. La clave va en
        el cuerpo de la solicitud y no en el manifiesto del perfil.
        """
        modulo = _cargar_modulo()
        doble = ClienteDoble(_flujo(fragmentos=PREDICTED_N))

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.assertEqual(len(doble.llamadas_post), 1)
        ruta, cuerpo = doble.llamadas_post[0]
        self.assertEqual(ruta, RUTA_COMPLETION)
        self.assertIn("ignore_eos", cuerpo)
        self.assertIs(cuerpo["ignore_eos"], True)
        self.assertIs(cuerpo["stream"], True)
        self.assertEqual(cuerpo["n_predict"], TOKENS_OBJETIVO)
        self.verificar_resultado(resultado, ESTADO_SUPERADA)


class ConteoTest(CasoDeSonda):
    """`RF-009`: conteo de fragmentos y lectura del bloque `timings`."""

    def test_conteo_de_fragmentos_y_timings(self):
        modulo = _cargar_modulo()
        doble = ClienteDoble(_flujo(fragmentos=PREDICTED_N))

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.verificar_resultado(resultado, ESTADO_SUPERADA)
        self.assertEqual(resultado["fragmentos"], PREDICTED_N)
        self.assertEqual(resultado["tokens_generados"], PREDICTED_N)
        self.assertIsInstance(resultado["tokens_por_segundo"], float)
        self.assertEqual(resultado["tokens_por_segundo"], PREDICTED_PER_SECOND)


class FlujoSinCierreTest(CasoDeSonda):
    """`CB-003`: el final del flujo se clasifica por `timings`, no por `[DONE]`.

    La ejecución real sobre la máquina objetivo terminó con 909 líneas cuya
    última está vacía y sin `data: [DONE]`; el fragmento final declaró el bloque
    `timings` y el servidor generó 908 tokens de 2400 pedidos. Por eso la
    ausencia de `[DONE]` con `timings` no rebaja el veredicto: `fallida` queda
    reservada al corte sin `timings` y al error de conexión. El corte sin
    `timings` conserva su veredicto dentro de este mismo caso.
    """

    def test_flujo_sin_cierre_con_timings_es_superada(self):
        modulo = _cargar_modulo()
        doble = ClienteDoble(_flujo(fragmentos=PREDICTED_N, con_cierre=False))

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.verificar_resultado(resultado, ESTADO_SUPERADA)
        self.assertNotIn("motivo", resultado)
        self.assertEqual(resultado["fragmentos"], PREDICTED_N)
        self.assertEqual(resultado["tokens_generados"], PREDICTED_N)
        self.assertEqual(resultado["tokens_por_segundo"], PREDICTED_PER_SECOND)
        self.assertEqual(resultado["servidor"], SERVIDOR_EN_SERVICIO)

        tokens_antes_del_corte = 3
        corte = ClienteDoble(
            _flujo(
                fragmentos=tokens_antes_del_corte,
                con_timings=False,
                con_cierre=False,
            )
        )

        resultado_corte = modulo.sondear(BASE_URL, cliente=corte)

        self.verificar_resultado(resultado_corte, ESTADO_FALLIDA)
        self.assertEqual(resultado_corte["tokens_generados"], tokens_antes_del_corte)
        self.assertIsNone(resultado_corte["tokens_por_segundo"])
        self.assertIn("cort", resultado_corte["motivo"].lower())


class VelocidadDePromptTest(CasoDeSonda):
    """`C-6` fila 16: la sonda devuelve también la velocidad de prompt.

    El resultado declara ``velocidad_prompt_tokens_por_segundo`` con el valor
    de ``timings.prompt_per_second`` del fragmento final, que es la fila 16 de
    `C-6` y la clave que `lanzador._velocidad_de_prompt` ya lee. Sobre el corte
    sin bloque ``timings`` las 2 velocidades quedan en ``None``: ningún valor se
    estima ni se deriva de otra cifra, conforme a `DEC-011`.
    """

    def test_velocidad_de_prompt_en_timings(self):
        modulo = _cargar_modulo()
        # La cifra afirmada es la que el bloque sintético declara, no 1 valor
        # derivado de otra fila: se comprueba contra la fixture y contra el
        # literal, de modo que 1 cambio del fixture no pasa inadvertido.
        self.assertEqual(PROMPT_PER_SECOND, TIMINGS["prompt_per_second"])
        doble = ClienteDoble(_flujo(fragmentos=PREDICTED_N))

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.verificar_resultado(resultado, ESTADO_SUPERADA)
        self.assertIsInstance(
            resultado["velocidad_prompt_tokens_por_segundo"], float
        )
        self.assertEqual(
            resultado["velocidad_prompt_tokens_por_segundo"], PROMPT_PER_SECOND
        )
        self.assertEqual(resultado["tokens_por_segundo"], PREDICTED_PER_SECOND)

        tokens_antes_del_corte = 3
        corte = ClienteDoble(
            _flujo(
                fragmentos=tokens_antes_del_corte,
                con_timings=False,
                con_cierre=False,
            )
        )

        resultado_corte = modulo.sondear(BASE_URL, cliente=corte)

        self.verificar_resultado(resultado_corte, ESTADO_FALLIDA)
        self.assertIsNone(resultado_corte["velocidad_prompt_tokens_por_segundo"])
        self.assertIsNone(resultado_corte["tokens_por_segundo"])
        print(
            "test_velocidad_de_prompt_en_timings: "
            f"prompt_per_second={TIMINGS['prompt_per_second']!r} "
            "velocidad_prompt_tokens_por_segundo="
            f"{resultado['velocidad_prompt_tokens_por_segundo']!r} "
            f"tokens_por_segundo={resultado['tokens_por_segundo']!r} "
            "corte_velocidad_prompt_tokens_por_segundo="
            f"{resultado_corte['velocidad_prompt_tokens_por_segundo']!r} "
            f"corte_tokens_por_segundo={resultado_corte['tokens_por_segundo']!r}"
        )


class ServicioTest(CasoDeSonda):
    """`RF-009`: estabilidad del servidor comprobada al cierre de la sonda."""

    def test_servidor_en_servicio_al_cierre(self):
        modulo = _cargar_modulo()

        doble_en_servicio = ClienteDoble(_flujo(fragmentos=PREDICTED_N))
        resultado = modulo.sondear(BASE_URL, cliente=doble_en_servicio)
        self.verificar_resultado(resultado, ESTADO_SUPERADA)
        self.assertEqual(resultado["servidor"], SERVIDOR_EN_SERVICIO)
        self.assertIn(RUTA_SALUD, doble_en_servicio.llamadas_get)

        doble_detenido = ClienteDoble(
            _flujo(fragmentos=PREDICTED_N), servidor_detenido=True
        )
        resultado = modulo.sondear(BASE_URL, cliente=doble_detenido)
        self.verificar_resultado(resultado, ESTADO_FALLIDA)
        self.assertEqual(resultado["servidor"], SERVIDOR_DETENIDO)
        self.assertEqual(resultado["tokens_generados"], PREDICTED_N)


class TranscripcionCortadaTest(CasoDeSonda):
    """`CB-003`: corte de la transcripción clasificado como prueba fallida."""

    def test_transcripcion_cortada_es_fallida(self):
        modulo = _cargar_modulo()
        tokens_antes_del_corte = 3
        doble = ClienteDoble(
            _flujo(
                fragmentos=tokens_antes_del_corte,
                con_timings=False,
                con_cierre=False,
            )
        )

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.verificar_resultado(resultado, ESTADO_FALLIDA)
        self.assertEqual(resultado["tokens_generados"], tokens_antes_del_corte)
        self.assertEqual(resultado["fragmentos"], tokens_antes_del_corte)
        self.assertIsNone(resultado["tokens_por_segundo"])
        self.assertIn("cort", resultado["motivo"].lower())


class SinTimingsTest(CasoDeSonda):
    """Riesgo de `DEC-011`: `[DONE]` sin bloque `timings` no promueve."""

    def test_sin_timings_clasifica_fallida(self):
        modulo = _cargar_modulo()
        fragmentos = 4
        doble = ClienteDoble(
            _flujo(fragmentos=fragmentos, con_timings=False, con_cierre=True)
        )

        resultado = modulo.sondear(BASE_URL, cliente=doble)

        self.verificar_resultado(resultado, ESTADO_FALLIDA)
        self.assertEqual(resultado["fragmentos"], fragmentos)
        self.assertEqual(resultado["tokens_generados"], fragmentos)
        self.assertIsNone(resultado["tokens_por_segundo"])
        self.assertIn("timings", resultado["motivo"].lower())


class SinRegistroTest(CasoDeSonda):
    """`DEC-012`: la sonda no escribe registro ni toca `results/`."""

    def test_sondear_no_escribe_registro(self):
        modulo = _cargar_modulo()
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        resultados_repo = RAIZ / "results"
        antes_repo = self._fotografia(resultados_repo)

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            raiz = Path(temporal)
            resultados = raiz / "results"
            resultados.mkdir()
            centinela = resultados / "centinela.txt"
            centinela.write_text("sin cambios\n", encoding="utf-8")
            antes = self._fotografia(raiz)

            directorio_anterior = os.getcwd()
            os.chdir(raiz)
            try:
                doble = ClienteDoble(_flujo(fragmentos=PREDICTED_N))
                resultado = modulo.sondear(BASE_URL, cliente=doble)
            finally:
                os.chdir(directorio_anterior)

            self.verificar_resultado(resultado, ESTADO_SUPERADA)
            self.assertEqual(self._fotografia(raiz), antes)

        self.assertEqual(self._fotografia(resultados_repo), antes_repo)

    def _fotografia(self, ruta):
        """Mapa de rutas relativas a contenido o `None` para 1 árbol ausente."""
        if not ruta.exists():
            return None
        return {
            str(elemento.relative_to(ruta)): (
                elemento.read_bytes() if elemento.is_file() else None
            )
            for elemento in sorted(ruta.rglob("*"))
        }


if __name__ == "__main__":
    unittest.main()
