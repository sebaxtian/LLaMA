"""Comparación de desviaciones de SPEC-017.

Implementa `RF-012` conforme a `CA-011`, sobre el bloque de comparación `C-7`
de `plan.md` y las decisiones `DEC-002` y `DEC-008`: `leer_registro` lee 1
registro de ejecución de `C-5` y `C-6` escrito por `tools/gemma/registro.py`
sin transcripción manual de las cifras, y `comparar` calcula las 5 diferencias
`delta_*` de `C-7` como propuesta menos inicial desde las filas de magnitud de
los 2 registros.

Contrato:

- ``leer_registro(ruta) -> dict`` devuelve exactamente las claves
  ``frontmatter`` y ``filas``. ``frontmatter`` declara las 11 claves de `C-5`:
  ``opciones_efectivas`` se decodifica del JSON que el registro serializa,
  ``vram_total_mib`` se interpreta como número y las 9 restantes se leen como
  texto; ``id`` es el ``stem`` del archivo. ``filas`` declara las 22 filas de
  `C-6` en su orden, cada 1 con exactamente las claves ``numero``, ``campo`` y
  ``valor``, y el ``valor`` de 1 magnitud conserva su unidad en el texto
  —``16376 MiB``, ``94.89 tokens/s``, ``6.3 s``—.
- Los registros escritos antes de la ampliación a 22 campos declaran 21 filas.
  ``leer_registro`` tolera ese registro y devuelve las 22 filas, con la fila 22
  «Memoria de expertos en host» en ``no disponible`` sintetizada en memoria y
  sin número ni unidad estimados, conforme a `DEC-027`. La síntesis es de
  lectura y no se persiste: el archivo nunca se abre en modo de escritura y sus
  bytes permanecen idénticos antes y después de la lectura, porque `RNF-004`
  exige 0 registros sobrescritos y `CB-005` exige que la evidencia histórica
  conserve su contenido. 1 registro de 22 filas se lee sin cambios; 1 de 23
  filas, 1 con las filas desordenadas y 1 cuya fila 22 no declara 1 número y la
  unidad ``MiB`` siguen lanzando ``ValueError``.
- ``comparar(lectura_inicial, lectura_propuesta, *, parametro, valor_inicial,
  valor_propuesto, alternativa=None) -> dict`` devuelve el bloque de `C-7` con
  exactamente las 10 claves ``parametro``, ``medicion_inicial``,
  ``medicion_propuesta``, ``valor_inicial``, ``valor_propuesto`` y las 5
  ``delta_*`` de velocidad de generación, velocidad de prompt, VRAM asignada,
  VRAM libre y RAM. Cada diferencia es propuesta menos inicial, se calcula
  desde las filas 17, 16, 13, 14 y 15 interpretando la magnitud numérica y no
  el texto completo, y no transcribe ninguna cifra escrita a mano en el
  llamador. Las 2 velocidades se expresan en tokens por segundo sin unidad en
  el valor y las 3 memorias en MiB.
- Cuando ``parametro`` es ``ctx_size`` y ``valor_propuesto`` es ``131072``, el
  bloque añade ``alternativa_contexto`` con ``medicion``, la velocidad de
  prompt y la velocidad de generación de la alternativa de contexto menor
  medida; fuera de ese caso la clave no aparece y, dentro de él, 1
  ``alternativa`` nula se rechaza con ``ValueError`` que nombra la clave.
- Toda irregularidad —registro ilegible, fila ausente, magnitud no numérica o
  ``parametro`` ausente de las opciones efectivas de los 2 registros— lanza
  ``ValueError`` que nombra la clave, la fila o el parámetro, nunca ``KeyError``
  sin contexto.

Alcance: usa solo ``json``, ``pathlib`` y ``re`` de la biblioteca estándar, no
escribe archivos y no lee ``bin/``, ``models/``, ``llama.cpp/`` ni ``.env``,
conforme a `DEC-002` y `DEC-012`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

__all__ = ["leer_registro", "comparar"]

# `C-5`: las 11 claves del frontmatter, en el orden en que se serializan.
CLAVES_FRONTMATTER = (
    "id",
    "fecha_utc",
    "perfil",
    "prueba",
    "proposito",
    "huella_opciones",
    "opciones_efectivas",
    "vram_total_mib",
    "version_binario",
    "commit_llama_cpp",
    "registro_anterior",
)

# `C-6` y `RF-006`: las 22 etiquetas en el orden de la tabla.
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
    "Memoria de expertos en host",
)

# `C-7`: las 5 filas de magnitud que alimentan las diferencias, con su unidad.
FILA_VRAM_ASIGNADA = 13
FILA_VRAM_LIBRE = 14
FILA_RAM = 15
FILA_VELOCIDAD_PROMPT = 16
FILA_VELOCIDAD_GENERACION = 17

# `C-6` y `DEC-027`: la fila 22 declara la memoria de expertos en host en MiB y
# es la que se sintetiza en los registros legados de 21 filas.
FILA_MEMORIA_EXPERTOS = 22
UNIDAD_MEMORIA_EXPERTOS = "MiB"

# `C-6`, `RNF-005` y `DEC-027`: la marca de la fuente ausente, que se escribe sin
# número ni unidad y es el valor sintetizado de la fila 22 del registro legado.
NO_DISPONIBLE = "no disponible"

# `C-7`: cada diferencia, su fila de `C-6` y la unidad que declara esa fila.
DIFERENCIAS = (
    (
        "delta_velocidad_generacion_tokens_por_segundo",
        FILA_VELOCIDAD_GENERACION,
        "tokens/s",
    ),
    (
        "delta_velocidad_prompt_tokens_por_segundo",
        FILA_VELOCIDAD_PROMPT,
        "tokens/s",
    ),
    ("delta_vram_asignada_mib", FILA_VRAM_ASIGNADA, "MiB"),
    ("delta_vram_libre_mib", FILA_VRAM_LIBRE, "MiB"),
    ("delta_ram_mib", FILA_RAM, "MiB"),
)

# `C-7`: el caso de comparación de contexto que añade la alternativa medida.
PARAMETRO_CONTEXTO = "ctx_size"
VALOR_CONTEXTO_PROPUESTO = 131072
CLAVE_ALTERNATIVA = "alternativa_contexto"

# `C-6`: 1 magnitud declara 1 número y después su unidad.
PATRON_NUMERO = re.compile(r"^[+-]?\d+(?:\.\d+)?$")

# `C-5` y `DEC-005`: el frontmatter se delimita con 2 líneas de 3 guiones.
DELIMITADOR = "---"

# `C-6`: las 3 columnas de la tabla del registro.
CLAVES_FILA = ("numero", "campo", "valor")


def leer_registro(ruta):
    """Lee 1 registro de ejecución y devuelve ``frontmatter`` y ``filas``.

    ``frontmatter`` declara las 11 claves de `C-5` con ``opciones_efectivas``
    decodificada del JSON y ``vram_total_mib`` numérica; ``filas`` declara las
    22 filas de `C-6` en su orden con el texto íntegro de cada valor, incluida
    su unidad. La lectura parte del archivo recibido y no del directorio
    actual, y toda irregularidad lanza ``ValueError`` con la clave o la fila.
    """
    camino = Path(ruta)
    texto = _texto_de_archivo(camino)
    cabecera, cuerpo = _partir_frontmatter(texto, camino)
    frontmatter = _frontmatter_de_registro(cabecera, camino)
    filas = _filas_de_registro(cuerpo, camino)
    return {"frontmatter": frontmatter, "filas": filas}


def comparar(
    lectura_inicial,
    lectura_propuesta,
    *,
    parametro,
    valor_inicial,
    valor_propuesto,
    alternativa=None,
):
    """Devuelve el bloque de comparación de 1 desviación, conforme a `C-7`.

    Las 5 diferencias se calculan como propuesta menos inicial desde las filas
    17, 16, 13, 14 y 15 de los 2 registros; ``parametro``, ``valor_inicial`` y
    ``valor_propuesto`` se transcriben desde los argumentos y los
    identificadores desde el frontmatter de cada lectura. En el caso de
    ``ctx_size`` con ``131072`` tokens el bloque añade la alternativa de
    contexto menor medida; fuera de ese caso la clave no aparece.
    """
    filas_inicial = _filas_de_lectura(lectura_inicial, "inicial")
    filas_propuesta = _filas_de_lectura(lectura_propuesta, "propuesta")

    bloque = {
        "parametro": _validar_parametro(
            parametro, lectura_inicial, lectura_propuesta
        ),
        "medicion_inicial": _identificador(lectura_inicial, "inicial"),
        "medicion_propuesta": _identificador(lectura_propuesta, "propuesta"),
        "valor_inicial": valor_inicial,
        "valor_propuesto": valor_propuesto,
    }
    for clave, numero, unidad in DIFERENCIAS:
        bloque[clave] = _diferencia(
            filas_inicial, filas_propuesta, numero, unidad
        )

    if _corresponde_alternativa(parametro, valor_propuesto):
        bloque[CLAVE_ALTERNATIVA] = _alternativa_contexto(alternativa)
    return bloque


def _texto_de_archivo(camino):
    """Lee el archivo como UTF-8 y envuelve el fallo con la ruta."""
    try:
        return camino.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise ValueError(
            f"registro ilegible: no existe el archivo {camino}"
        ) from None
    except OSError as error:
        raise ValueError(f"registro ilegible: {camino}: {error}") from error


def _partir_frontmatter(texto, camino):
    """Separa las líneas del frontmatter y las del cuerpo de la tabla."""
    lineas = texto.splitlines()
    delimitadores = [
        posicion
        for posicion, linea in enumerate(lineas)
        if linea.strip() == DELIMITADOR
    ]
    if len(delimitadores) < 2 or delimitadores[0] != 0:
        raise ValueError(
            f"registro ilegible: {camino} no declara el frontmatter de C-5 "
            f"delimitado por 2 líneas {DELIMITADOR}"
        )
    cierre = delimitadores[1]
    return lineas[1:cierre], lineas[cierre + 1 :]


def _frontmatter_de_registro(cabecera, camino):
    """Decodifica las 11 claves de `C-5` desde el texto del frontmatter."""
    declaradas = {}
    for linea in cabecera:
        if not linea.strip():
            continue
        clave, separador, valor = linea.partition(":")
        if separador != ":" or not clave.strip():
            raise ValueError(
                f"registro ilegible: {camino} declara la línea "
                f"{linea.strip()!r} sin la forma '<clave>: <valor>' de C-5"
            )
        declaradas[clave.strip()] = valor.strip()

    frontmatter = {}
    for clave in CLAVES_FRONTMATTER:
        if clave not in declaradas:
            raise ValueError(
                f"frontmatter: el registro {camino} no declara la clave "
                f"{clave} de C-5"
            )
        frontmatter[clave] = _valor_de_frontmatter(
            clave, declaradas[clave], camino
        )

    if frontmatter["id"] != camino.stem:
        raise ValueError(
            f"frontmatter: el registro {camino} declara el id "
            f"{frontmatter['id']!r} y el archivo se llama "
            f"{camino.stem!r}; C-5 fija el id igual al stem"
        )
    return frontmatter


def _valor_de_frontmatter(clave, texto, camino):
    """Decodifica 1 clave de `C-5`: JSON en las opciones, número en la VRAM."""
    referencia = f"frontmatter: la clave {clave} de {camino}"
    if clave == "opciones_efectivas":
        try:
            opciones = json.loads(texto)
        except ValueError as error:
            raise ValueError(
                f"{referencia} no es 1 JSON válido: {error}"
            ) from error
        if not isinstance(opciones, dict) or not opciones:
            raise ValueError(
                f"{referencia} declara {texto!r}; se espera el objeto de "
                "opciones que aplicó el lanzador"
            )
        return opciones
    if clave == "vram_total_mib":
        if not PATRON_NUMERO.match(texto):
            raise ValueError(
                f"{referencia} declara {texto!r}; se esperan los MiB de la GPU "
                "dedicada"
            )
        return _numero(texto)
    if not texto:
        raise ValueError(
            f"{referencia} está vacía; C-5 exige 1 valor declarado"
        )
    return texto


def _filas_de_registro(cuerpo, camino):
    """Lee las 22 filas de `C-6` en su orden desde la tabla del cuerpo.

    Los registros escritos antes de la ampliación a 22 campos declaran 21
    filas: el lector valida las 21 y devuelve la 22 «Memoria de expertos en
    host» en ``no disponible`` sintetizada en memoria, sin escribir en el
    archivo ni estimar el valor ausente, conforme a `DEC-027`.
    """
    celdas_por_fila = []
    for linea in cuerpo:
        if not linea.strip().startswith("|"):
            continue
        celdas = _celdas(linea)
        if not celdas or not re.fullmatch(r"\d+", celdas[0]):
            continue
        celdas_por_fila.append(celdas)

    filas = []
    for posicion, celdas in enumerate(celdas_por_fila, start=1):
        if posicion > len(CAMPOS_C6):
            raise ValueError(
                f"fila {posicion}: el registro {camino} declara más de las "
                f"{len(CAMPOS_C6)} filas de C-6"
            )
        campo_esperado = CAMPOS_C6[posicion - 1]
        if len(celdas) != 3:
            raise ValueError(
                f"fila {posicion} ({campo_esperado}): el registro {camino} no "
                "declara las 3 columnas de C-6"
            )
        numero, campo, valor = int(celdas[0]), celdas[1], celdas[2]
        if numero != posicion:
            raise ValueError(
                f"fila {posicion} ({campo_esperado}): el registro {camino} "
                f"declara la fila {numero} fuera del orden de RF-006"
            )
        if campo != campo_esperado:
            raise ValueError(
                f"fila {numero} ({campo_esperado}): el registro {camino} "
                f"declara el campo {campo!r} en la fila de C-6"
            )
        if not valor:
            raise ValueError(
                f"fila {numero} ({campo_esperado}): el registro {camino} "
                "declara el valor vacío; C-6 y RNF-005 exigen 0 campos vacíos"
            )
        if numero == FILA_MEMORIA_EXPERTOS and valor != NO_DISPONIBLE:
            _exigir_unidad_de_memoria(valor, numero, campo, camino)
        filas.append({"numero": numero, "campo": campo, "valor": valor})

    if len(filas) == len(CAMPOS_C6) - 1:
        return filas + [_fila_sintetizada_de_memoria()]

    if len(filas) != len(CAMPOS_C6):
        faltantes = [
            numero
            for numero in range(1, len(CAMPOS_C6) + 1)
            if numero not in {fila["numero"] for fila in filas}
        ]
        detalle = (
            f"falta la fila {faltantes[0]} ({CAMPOS_C6[faltantes[0] - 1]})"
            if faltantes
            else f"declara {len(filas)} filas"
        )
        raise ValueError(
            f"fila ausente: el registro {camino} {detalle} y C-6 exige "
            f"{len(CAMPOS_C6)} filas, o las {len(CAMPOS_C6) - 1} del registro "
            "legado que DEC-027 tolera con la fila 22 en no disponible"
        )
    return filas


def _fila_sintetizada_de_memoria():
    """Sintetiza en memoria la fila 22 del registro legado de 21 filas.

    El valor es la marca de la fuente ausente de `RNF-005` y `C-6`, sin número
    ni unidad: esas ejecuciones no midieron la memoria de expertos en host y
    `DEC-027` prohíbe estimarla desde 1 carga posterior. La fila solo vive en
    el diccionario devuelto y no se escribe en el archivo.
    """
    return {
        "numero": FILA_MEMORIA_EXPERTOS,
        "campo": CAMPOS_C6[FILA_MEMORIA_EXPERTOS - 1],
        "valor": NO_DISPONIBLE,
    }


def _exigir_unidad_de_memoria(valor, numero, campo, camino):
    """Exige que la fila 22 declare 1 número y la unidad `MiB` de `C-6`."""
    cantidad, separador, unidad = valor.rpartition(" ")
    if (
        separador != " "
        or unidad != UNIDAD_MEMORIA_EXPERTOS
        or not PATRON_NUMERO.match(cantidad)
    ):
        raise ValueError(
            f"fila {numero} ({campo}): el registro {camino} declara {valor!r} "
            f"sin 1 número y la unidad {UNIDAD_MEMORIA_EXPERTOS!r} de C-6, ni "
            f"la marca {NO_DISPONIBLE!r} de la fuente ausente"
        )


def _celdas(linea):
    """Divide 1 línea de tabla en celdas, respetando la barra escapada."""
    partes = re.split(r"(?<!\\)\|", linea.strip())
    if partes and not partes[0].strip():
        partes = partes[1:]
    if partes and not partes[-1].strip():
        partes = partes[:-1]
    return [parte.strip().replace("\\|", "|") for parte in partes]


def _filas_de_lectura(lectura, etiqueta):
    """Valida la forma de 1 lectura y devuelve sus filas de `C-6`."""
    if not isinstance(lectura, dict):
        raise ValueError(
            f"lectura {etiqueta}: se esperaba 1 mapa con las claves frontmatter "
            f"y filas y se recibió {type(lectura).__name__}"
        )
    filas = lectura.get("filas")
    if not isinstance(filas, list) or len(filas) != len(CAMPOS_C6):
        recibidas = len(filas) if isinstance(filas, list) else 0
        raise ValueError(
            f"lectura {etiqueta}: la clave filas declara {recibidas} filas y "
            f"C-6 exige {len(CAMPOS_C6)}"
        )
    for fila in filas:
        if not isinstance(fila, dict):
            raise ValueError(
                f"lectura {etiqueta}: la clave filas declara 1 fila que no es "
                "1 mapa con numero, campo y valor"
            )
        for clave in CLAVES_FILA:
            if clave not in fila:
                raise ValueError(
                    f"lectura {etiqueta}: 1 fila de C-6 no declara la clave "
                    f"{clave}"
                )
    return filas


def _frontmatter_de_lectura(lectura, etiqueta):
    """Devuelve el frontmatter de 1 lectura o falla nombrando la clave."""
    frontmatter = lectura.get("frontmatter") if isinstance(lectura, dict) else None
    if not isinstance(frontmatter, dict):
        raise ValueError(f"lectura {etiqueta}: falta el frontmatter de C-5")
    return frontmatter


def _identificador(lectura, etiqueta):
    """Devuelve el ``id`` del frontmatter, que es la medición de `C-7`."""
    frontmatter = _frontmatter_de_lectura(lectura, etiqueta)
    identificador = frontmatter.get("id")
    if not isinstance(identificador, str) or not identificador.strip():
        raise ValueError(
            f"lectura {etiqueta}: el frontmatter no declara la clave id de C-5"
        )
    return identificador


def _opciones(lectura, etiqueta):
    """Devuelve las opciones efectivas de 1 lectura."""
    frontmatter = _frontmatter_de_lectura(lectura, etiqueta)
    opciones = frontmatter.get("opciones_efectivas")
    if not isinstance(opciones, dict) or not opciones:
        raise ValueError(
            f"lectura {etiqueta}: el frontmatter no declara la clave "
            "opciones_efectivas de C-5"
        )
    return opciones


def _validar_parametro(parametro, lectura_inicial, lectura_propuesta):
    """Exige que el parámetro figure en las opciones efectivas de las 2."""
    if not isinstance(parametro, str) or not parametro.strip():
        raise ValueError(
            "parametro: se esperaba el eje comparado y se recibió "
            f"{parametro!r}"
        )
    for lectura, etiqueta in (
        (lectura_inicial, "inicial"),
        (lectura_propuesta, "propuesta"),
    ):
        if parametro not in _opciones(lectura, etiqueta):
            raise ValueError(
                f"parametro: {parametro!r} no corresponde a los 2 registros "
                f"porque la medición {etiqueta} no lo declara en sus opciones "
                "efectivas de C-5"
            )
    return parametro


def _diferencia(filas_inicial, filas_propuesta, numero, unidad):
    """Calcula propuesta menos inicial desde la fila de magnitud indicada."""
    inicial = _magnitud(
        _fila(filas_inicial, numero, "inicial"), unidad, "inicial"
    )
    propuesta = _magnitud(
        _fila(filas_propuesta, numero, "propuesta"), unidad, "propuesta"
    )
    valor = propuesta - inicial
    if unidad == "MiB" and float(valor).is_integer():
        return int(valor)
    return float(valor)


def _fila(filas, numero, etiqueta):
    """Devuelve la fila ``numero`` de `C-6` o falla nombrando la fila."""
    for fila in filas:
        if fila["numero"] == numero:
            return fila
    raise ValueError(
        f"fila {numero} ({CAMPOS_C6[numero - 1]}): falta la fila de C-6 en la "
        f"medición {etiqueta}"
    )


def _magnitud(fila, unidad, etiqueta):
    """Interpreta la magnitud numérica de 1 fila y comprueba su unidad."""
    texto = str(fila["valor"])
    cantidad, separador, declarada = texto.rpartition(" ")
    if (
        separador != " "
        or declarada != unidad
        or not PATRON_NUMERO.match(cantidad)
    ):
        raise ValueError(
            f"fila {fila['numero']} ({fila['campo']}): la magnitud {texto!r} no "
            f"declara 1 número y la unidad {unidad!r} de C-6 en la medición "
            f"{etiqueta}"
        )
    return float(cantidad)


def _corresponde_alternativa(parametro, valor_propuesto):
    """Indica si el caso de `C-7` exige la alternativa de contexto menor."""
    return (
        parametro == PARAMETRO_CONTEXTO
        and not isinstance(valor_propuesto, bool)
        and valor_propuesto == VALOR_CONTEXTO_PROPUESTO
    )


def _alternativa_contexto(alternativa):
    """Devuelve la alternativa medida con su identificador y sus 2 velocidades."""
    if alternativa is None:
        raise ValueError(
            f"{CLAVE_ALTERNATIVA}: el caso de {PARAMETRO_CONTEXTO} con "
            f"{VALOR_CONTEXTO_PROPUESTO} tokens exige el registro de la "
            "alternativa de contexto menor medida y no llegó ninguno"
        )
    filas = _filas_de_lectura(alternativa, "alternativa")
    return {
        "medicion": _identificador(alternativa, "alternativa"),
        "velocidad_prompt_tokens_por_segundo": _magnitud(
            _fila(filas, FILA_VELOCIDAD_PROMPT, "alternativa"),
            "tokens/s",
            "alternativa",
        ),
        "velocidad_generacion_tokens_por_segundo": _magnitud(
            _fila(filas, FILA_VELOCIDAD_GENERACION, "alternativa"),
            "tokens/s",
            "alternativa",
        ),
    }


def _numero(texto):
    """Devuelve el número de 1 texto ya validado: entero si es integral."""
    valor = float(texto)
    return int(valor) if valor.is_integer() else valor
