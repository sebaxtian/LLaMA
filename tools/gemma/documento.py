"""Verificación documental de la línea base de SPEC-017.

Implementa `RF-005`, `RNF-002` y `CB-005` conforme a `CA-004` y `CA-006`, sobre
la línea base documental `C-10` de `plan.md` y las decisiones `DEC-013` y
`DEC-023`.

`C-10` exige en ``docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md`` 3 secciones de
nivel 2 —``## Configuración candidata``, ``## Resultado medido`` y
``## Configuración aprobada``— con estos títulos exactos y en este orden, cada
perfil en la sección de su estado declarado con la marca ``Estado: candidato``,
``Estado: medido`` o ``Estado: aprobado``, ninguna expresión vetada
—``línea base de producción``, ``perfil rendimiento máximo`` y ``optimizado``—
dentro de la sección de configuración aprobada, y el archivo en UTF-8 sin marca
de orden de bytes y sin secuencias de doble codificación.

Contrato:

- ``analizar(ruta) -> list[dict]`` devuelve 1 lista de hallazgos, cada 1 con
  ``ruta``, ``linea`` entera de base 1, ``regla`` y ``detalle``; la lista es
  vacía cuando el documento es conforme. Las reglas son ``secciones``,
  ``estado``, ``candidato_en_aprobada``, ``expresion_vetada``, ``bom`` y
  ``doble_codificacion``.
- ``comparar_historicos(ruta, registros) -> list[dict]`` contrasta las citas de
  valores medidos y de identificadores de prueba que el documento declara
  contra el mapa ``registros`` —identificador a lectura con las claves
  ``frontmatter`` y ``filas``, como la que devuelve ``comparar.leer_registro``—
  y devuelve 1 hallazgo por valor o identificador alterado, con ``regla`` igual
  a ``valor_alterado`` o a ``identificador_alterado``. La comparación no admite
  tolerancia: 1 cifra distinta es 1 alteración aunque su diferencia sea mínima.
- ``main(argv) -> int`` resuelve el documento desde ``--raiz``, añade la
  comparación con ``--comparar`` leyendo los registros de ``results/gemma/`` del
  árbol recibido con ``comparar.leer_registro`` y sin consultar Git, y devuelve
  `9` con al menos 1 hallazgo, `0` sin hallazgos y `2` solo por uso incorrecto,
  conforme a `C-8` y `DEC-023`.

Las 2 funciones de verificación son puras: no modifican el documento ni
escriben archivos, porque la normalización corresponde al agente ``documenter``
conforme a `DEC-013`. El módulo usa ``pathlib``, ``re`` y ``sys`` de la
biblioteca estándar, además del módulo local ``comparar``, y no lee ``bin/``,
``models/``, ``llama.cpp/`` ni ``.env``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import comparar
except ModuleNotFoundError:  # pragma: no cover - ejecución como script
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import comparar

__all__ = ["analizar", "comparar_historicos", "main"]

# `C-10`: el documento de la línea base documental y su ruta relativa a la raíz.
NOMBRE_DOCUMENTO = "Gemma-4-26B-A4B-it-qat-GGUF.md"
RUTA_DOCUMENTO = Path("docs") / "gemma" / NOMBRE_DOCUMENTO

# `C-10`: los 3 títulos de nivel 2, con su texto exacto y en su orden.
SECCION_CANDIDATA = "## Configuración candidata"
SECCION_MEDIDO = "## Resultado medido"
SECCION_APROBADA = "## Configuración aprobada"
SECCIONES = (SECCION_CANDIDATA, SECCION_MEDIDO, SECCION_APROBADA)

# `C-10`: la sección que corresponde a cada marca de estado de 1 perfil.
SECCION_POR_ESTADO = {
    "candidato": SECCION_CANDIDATA,
    "medido": SECCION_MEDIDO,
    "aprobado": SECCION_APROBADA,
}

# `C-10`: las 3 expresiones vetadas dentro de la sección aprobada.
EXPRESIONES_VETADAS = (
    "línea base de producción",
    "perfil rendimiento máximo",
    "optimizado",
)

# `RNF-002`: la marca de orden de bytes al inicio del archivo.
PREFIJO_BOM = b"\xef\xbb\xbf"

# `RNF-002`: las secuencias típicas de UTF-8 leído como Latin-1 y re-escrito en
# UTF-8 —la ``Ã`` inicial de las minúsculas acentuadas, la ``Â`` de los signos
# de control y la ``â€`` de la puntuación—; el texto correcto en español no
# contiene ninguna de ellas, de modo que 0 falsos positivos.
SECUENCIAS_DOBLE_CODIFICACION = ("Ã©", "Ã³", "Ã±", "Â", "â€")

# `C-10`: 1 perfil declara su estado con esta marca y 1 de sus 3 valores.
PATRON_ESTADO = re.compile(r"Estado:\s*(candidato|medido|aprobado)")

# `CB-005` y `C-5`: los identificadores de registro que el documento cita.
PATRON_IDENTIFICADOR = re.compile(
    r"(?<![0-9A-Za-z])[0-9]{8}T[0-9]{6}Z-[0-9A-Za-z_.-]*[0-9A-Za-z]"
)

# `RF-006` y `C-6`: los campos de magnitud con su número de fila y su unidad.
MAGNITUDES = {
    "Contexto configurado": (6, "tokens"),
    "Ranuras del servidor": (7, "ranuras"),
    "Capas de expertos en CPU": (8, "capas"),
    "Micro-lote": (9, "tokens"),
    "Tiempo de carga": (12, "s"),
    "VRAM asignada": (13, "MiB"),
    "VRAM libre": (14, "MiB"),
    "RAM utilizada": (15, "MiB"),
    "Velocidad de prompt": (16, "tokens/s"),
    "Velocidad de generación": (17, "tokens/s"),
    "Desbordamiento hacia memoria compartida": (19, "MiB"),
}

# `C-6`: las formas de la unidad de velocidad que admite 1 cita del documento.
ALIAS_UNIDADES = {"t/s": "tokens/s", "tok/s": "tokens/s"}

# `CB-005`: 1 cita declara el número y, opcionalmente, su unidad.
PATRON_MAGNITUD = re.compile(
    r"([+-]?\d[\d.,]*)(?:\s+([A-Za-z%]+(?:/[A-Za-z]+)?))?"
)

# `CB-005`: 1 línea de viñeta o de tabla declara 1 magnitud con su unidad.
PATRON_CITA_SIN_ETIQUETA = re.compile(
    r"(?<![\w.,])([+-]?\d[\d.,]*)\s+"
    r"(tokens/s|t/s|tok/s|MiB|tokens|capas|ranuras|s)(?![\w/])"
)

# `DEC-023` y `DEC-005`: los registros de ejecución viven en esta carpeta.
DIRECTORIO_REGISTROS = Path("results") / "gemma"
SUFIJO_REGISTRO = ".md"

# `C-8` y `DEC-023`: códigos de salida de la verificación documental.
CODIGO_OK = 0
CODIGO_USO_INCORRECTO = 2
CODIGO_HALLAZGOS = 9

# `C-8`: el uso admitido de la línea de comandos.
USO = "uso: documento.py --raiz <ruta> [--comparar]"


def analizar(ruta):
    """Devuelve los hallazgos de conformidad del documento con `C-10`.

    Comprueba la marca de orden de bytes, las 3 secciones de nivel 2 en su
    orden, la sección que corresponde a la marca de estado de cada perfil, las
    3 expresiones vetadas dentro de ``## Configuración aprobada`` y las
    secuencias de doble codificación de `RNF-002`. Cada hallazgo declara la
    ruta, la línea de base 1 donde aparece y su regla; 1 documento conforme
    produce 1 lista vacía. La función no modifica el archivo.
    """
    camino, contenido, texto = _leer_documento(ruta)
    lineas = texto.splitlines()

    hallazgos = []
    if contenido.startswith(PREFIJO_BOM):
        hallazgos.append(
            _hallazgo(
                camino,
                1,
                "bom",
                "el archivo empieza con la marca de orden de bytes y RNF-002 "
                "exige 1 archivo UTF-8 sin ella",
            )
        )
    hallazgos.extend(_hallazgos_de_secciones(camino, lineas))
    hallazgos.extend(_hallazgos_de_estado(camino, lineas))
    hallazgos.extend(_hallazgos_de_expresion_vetada(camino, lineas))
    hallazgos.extend(_hallazgos_de_doble_codificacion(camino, lineas))
    hallazgos.sort(key=lambda hallazgo: hallazgo["linea"])
    return hallazgos


def comparar_historicos(ruta, registros):
    """Contrasta las citas del documento con las lecturas de ``registros``.

    Recorre cada identificador de registro que el documento cita y compara las
    magnitudes de `C-6` que declara en su bloque contra la lectura homónima,
    aceptando el valor con o sin unidad y sin tolerancia. 1 identificador que
    el mapa no declara y 1 cifra distinta de la registrada producen 1 hallazgo
    con ``regla`` ``identificador_alterado`` o ``valor_alterado`` y la línea
    exacta. La función no modifica el documento ni escribe archivos.
    """
    camino, _contenido, texto = _leer_documento(ruta)
    mapa = _mapa_de_registros(registros)

    hallazgos = []
    for identificador, numero_cita, bloque in _citas_de_registro(
        texto.splitlines()
    ):
        lectura = mapa.get(identificador)
        if lectura is None:
            hallazgos.append(
                _hallazgo(
                    camino,
                    numero_cita,
                    "identificador_alterado",
                    f"el documento cita {identificador!r} y el conjunto de "
                    "lecturas de results/gemma/ no lo declara",
                )
            )
            continue
        hallazgos.extend(_hallazgos_de_valores(camino, bloque, lectura))
    hallazgos.sort(key=lambda hallazgo: hallazgo["linea"])
    return hallazgos


def main(argv=None):
    """Ejecuta la verificación documental y devuelve el código de `C-8`.

    ``--raiz`` resuelve ``docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md`` del árbol
    recibido y ``--comparar`` añade el contraste con los registros de
    ``results/gemma/`` de ese árbol, conforme a `DEC-023`. Devuelve `9` con al
    menos 1 hallazgo, `0` sin hallazgos y `2` solo por uso incorrecto; 1
    documento ilegible también devuelve `9`, porque la verificación no puede
    declararlo conforme, y lo informa por la salida de error.
    """
    argumentos = list(sys.argv[1:] if argv is None else argv)

    raiz = Path(__file__).resolve().parents[2]
    comparar_con_registros = False
    indice = 0
    while indice < len(argumentos):
        argumento = argumentos[indice]
        if argumento == "--raiz":
            if indice + 1 >= len(argumentos):
                return _error_de_uso("--raiz exige 1 ruta")
            raiz = Path(argumentos[indice + 1])
            indice += 2
        elif argumento.startswith("--raiz="):
            valor = argumento.partition("=")[2]
            if not valor:
                return _error_de_uso("--raiz exige 1 ruta")
            raiz = Path(valor)
            indice += 1
        elif argumento == "--comparar":
            comparar_con_registros = True
            indice += 1
        else:
            return _error_de_uso(f"argumento no admitido: {argumento}")

    if not str(raiz).strip():
        return _error_de_uso("--raiz exige 1 ruta")

    ruta = raiz / RUTA_DOCUMENTO
    try:
        hallazgos = analizar(ruta)
        if comparar_con_registros:
            hallazgos.extend(comparar_historicos(ruta, _registros_de(raiz)))
    except ValueError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return CODIGO_HALLAZGOS

    for hallazgo in hallazgos:
        print(
            f"{hallazgo['ruta']}:{hallazgo['linea']}: "
            f"{hallazgo['regla']}: {hallazgo['detalle']}"
        )
    return CODIGO_HALLAZGOS if hallazgos else CODIGO_OK


def _leer_documento(ruta):
    """Lee el documento y devuelve su ruta, sus bytes y su texto sin marca."""
    camino = Path(ruta)
    try:
        contenido = camino.read_bytes()
    except FileNotFoundError:
        raise ValueError(
            f"documento ilegible: no existe el archivo {camino}"
        ) from None
    except OSError as error:
        raise ValueError(f"documento ilegible: {camino}: {error}") from error
    try:
        texto = contenido.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError(
            f"documento ilegible: {camino} no está codificado en UTF-8: {error}"
        ) from error
    return camino, contenido, texto


def _hallazgo(camino, linea, regla, detalle):
    """Devuelve 1 hallazgo con la ruta, la línea de base 1 y su regla."""
    return {
        "ruta": str(camino),
        "linea": int(linea),
        "regla": regla,
        "detalle": detalle,
    }


def _hallazgos_de_secciones(camino, lineas):
    """Comprueba que las 3 secciones de `C-10` existen en su orden."""
    posiciones = {titulo: [] for titulo in SECCIONES}
    for numero, linea in enumerate(lineas, start=1):
        titulo = linea.strip()
        if titulo in posiciones:
            posiciones[titulo].append(numero)

    for indice, titulo in enumerate(SECCIONES):
        if posiciones[titulo]:
            continue
        previas = posiciones[SECCIONES[indice - 1]] if indice else []
        referencia = previas[0] if previas else 1
        return [
            _hallazgo(
                camino,
                referencia,
                "secciones",
                f"falta la sección {titulo!r} de C-10",
            )
        ]

    duplicadas = [
        (titulo, posiciones[titulo][1])
        for titulo in SECCIONES
        if len(posiciones[titulo]) > 1
    ]
    if duplicadas:
        titulo, numero = duplicadas[0]
        return [
            _hallazgo(
                camino,
                numero,
                "secciones",
                f"la sección {titulo!r} de C-10 aparece más de una vez",
            )
        ]

    ordenadas = sorted(
        (posiciones[titulo][0], titulo) for titulo in SECCIONES
    )
    for indice, (_numero, titulo) in enumerate(ordenadas):
        if titulo == SECCIONES[indice]:
            continue
        return [
            _hallazgo(
                camino,
                ordenadas[indice][0],
                "secciones",
                f"la sección {titulo!r} figura donde C-10 exige "
                f"{SECCIONES[indice]!r}",
            )
        ]
    return []


def _hallazgos_de_estado(camino, lineas):
    """Comprueba que cada perfil figure en la sección de su marca de estado."""
    hallazgos = []
    actual = None
    for numero, linea in enumerate(lineas, start=1):
        titulo = linea.strip()
        if titulo.startswith("## "):
            actual = titulo
            continue
        coincidencia = PATRON_ESTADO.search(linea)
        if coincidencia is None:
            continue
        estado = coincidencia.group(1)
        esperada = SECCION_POR_ESTADO[estado]
        if actual == esperada:
            continue
        regla = (
            "candidato_en_aprobada"
            if estado == "candidato" and actual == SECCION_APROBADA
            else "estado"
        )
        donde = actual if actual is not None else "ninguna sección"
        hallazgos.append(
            _hallazgo(
                camino,
                numero,
                regla,
                f"el perfil declara {estado} y figura en {donde!r}, mientras "
                f"C-10 exige {esperada!r}",
            )
        )
    return hallazgos


def _hallazgos_de_expresion_vetada(camino, lineas):
    """Busca las 3 expresiones vetadas dentro de `C-10` aprobada."""
    hallazgos = []
    dentro = False
    for numero, linea in enumerate(lineas, start=1):
        titulo = linea.strip()
        if titulo.startswith("## "):
            dentro = titulo == SECCION_APROBADA
            continue
        if not dentro:
            continue
        plegada = linea.casefold()
        for expresion in EXPRESIONES_VETADAS:
            if expresion.casefold() not in plegada:
                continue
            hallazgos.append(
                _hallazgo(
                    camino,
                    numero,
                    "expresion_vetada",
                    f"la sección aprobada declara {expresion!r}, que C-10 veta",
                )
            )
            break
    return hallazgos


def _hallazgos_de_doble_codificacion(camino, lineas):
    """Busca las secuencias de UTF-8 leído como Latin-1 de `RNF-002`."""
    hallazgos = []
    for numero, linea in enumerate(lineas, start=1):
        for secuencia in SECUENCIAS_DOBLE_CODIFICACION:
            if secuencia not in linea:
                continue
            hallazgos.append(
                _hallazgo(
                    camino,
                    numero,
                    "doble_codificacion",
                    f"la línea declara la secuencia {secuencia!r} de doble "
                    "codificación y RNF-002 exige 0",
                )
            )
    return hallazgos


def _citas_de_registro(lineas):
    """Agrupa las líneas que siguen a cada identificador de registro citado."""
    citas = []
    actual = None
    for numero, linea in enumerate(lineas, start=1):
        identificador = _identificador_citado(linea)
        if identificador is not None:
            if actual is not None:
                citas.append(actual)
            actual = (identificador, numero, [])
            continue
        if actual is None:
            continue
        if linea.strip().startswith("#"):
            citas.append(actual)
            actual = None
            continue
        actual[2].append((numero, linea))
    if actual is not None:
        citas.append(actual)
    return citas


def _identificador_citado(linea):
    """Devuelve el primer identificador de registro de la línea o ``None``."""
    coincidencia = PATRON_IDENTIFICADOR.search(linea)
    return coincidencia.group(0) if coincidencia is not None else None


def _mapa_de_registros(registros):
    """Valida el mapa identificador a lectura y lo devuelve normalizado."""
    if not isinstance(registros, dict):
        raise ValueError(
            "registros: se esperaba 1 mapa identificador a lectura y se "
            f"recibió {type(registros).__name__}"
        )
    mapa = {}
    for identificador, lectura in registros.items():
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError(
                "registros: 1 clave no es 1 identificador de registro"
            )
        if not isinstance(lectura, dict) or "filas" not in lectura:
            raise ValueError(
                f"registros: la lectura de {identificador!r} no declara las "
                "claves frontmatter y filas de comparar.leer_registro"
            )
        mapa[identificador] = lectura
    return mapa


def _hallazgos_de_valores(camino, bloque, lectura):
    """Contrasta las magnitudes citadas contra las filas de 1 lectura."""
    filas = {
        fila.get("numero"): fila.get("valor", "")
        for fila in lectura["filas"]
        if isinstance(fila, dict)
    }
    identificador = _identificador_de_lectura(lectura)

    hallazgos = []
    consumidas = set()
    for numero, linea in bloque:
        etiquetadas = _citas_etiquetadas(linea)
        if not etiquetadas:
            continue
        consumidas.add(numero)
        for campo, citado in etiquetadas:
            hallazgo = _comparar_valor(
                camino, numero, campo, citado, filas, identificador
            )
            if hallazgo is not None:
                hallazgos.append(hallazgo)

    for numero, linea in bloque:
        if numero in consumidas:
            continue
        hallazgos.extend(
            _comparar_citas_sin_etiqueta(
                camino, numero, linea, filas, identificador
            )
        )
    return hallazgos


def _identificador_de_lectura(lectura):
    """Devuelve el ``id`` de la lectura o el nombre del registro ausente."""
    frontmatter = lectura.get("frontmatter")
    if isinstance(frontmatter, dict):
        identificador = frontmatter.get("id")
        if isinstance(identificador, str) and identificador.strip():
            return identificador
    return "el registro"


def _citas_etiquetadas(linea):
    """Devuelve las citas ``<campo de C-6>: <valor>`` de la línea."""
    citas = []
    for campo in MAGNITUDES:
        posicion = linea.find(campo)
        if posicion < 0:
            continue
        resto = linea[posicion + len(campo) :]
        coincidencia = re.match(r"\s*:\s*(.*)$", resto)
        if coincidencia is None:
            continue
        citas.append((campo, coincidencia.group(1).strip()))
    return citas


def _comparar_valor(camino, numero, campo, citado, filas, identificador):
    """Compara 1 cita etiquetada con la fila homónima de la lectura."""
    numero_fila, unidad = MAGNITUDES[campo]
    registrado = filas.get(numero_fila)
    if registrado is None:
        return None
    esperada = _magnitud(registrado)
    if esperada is None:
        return None

    mostrado = citado.strip().strip("`").strip()
    obtenida = _magnitud(mostrado)
    if obtenida is None:
        if not mostrado:
            return None
        return _hallazgo(
            camino,
            numero,
            "valor_alterado",
            f"la fila {numero_fila} ({campo}) cita {mostrado!r} y la lectura "
            f"{identificador!r} declara {registrado!r}",
        )

    valor, unidad_citada = obtenida
    if valor == esperada[0] and (
        not unidad_citada or unidad_citada == esperada[1]
    ):
        return None
    return _hallazgo(
        camino,
        numero,
        "valor_alterado",
        f"la fila {numero_fila} ({campo}) cita {mostrado!r} y la lectura "
        f"{identificador!r} declara {registrado!r}",
    )


def _comparar_citas_sin_etiqueta(camino, numero, linea, filas, identificador):
    """Compara las magnitudes sin etiqueta de 1 viñeta o fila de tabla."""
    despojada = linea.strip()
    if not despojada.startswith(("-", "|")):
        return []

    registradas = []
    for valor in filas.values():
        magnitud = _magnitud(valor)
        if magnitud is not None:
            registradas.append(magnitud)

    hallazgos = []
    for coincidencia in PATRON_CITA_SIN_ETIQUETA.finditer(linea):
        valor = _numero(coincidencia.group(1))
        if valor is None:
            continue
        unidad = _unidad(coincidencia.group(2))
        if any(
            valor == registrado and unidad == unidad_registrada
            for registrado, unidad_registrada in registradas
        ):
            continue
        hallazgos.append(
            _hallazgo(
                camino,
                numero,
                "valor_alterado",
                f"la cita {coincidencia.group(0)!r} no corresponde a ninguna "
                f"magnitud de la lectura {identificador!r}",
            )
        )
    return hallazgos


def _magnitud(texto):
    """Interpreta 1 valor con número y unidad opcional, o devuelve ``None``."""
    limpio = str(texto).strip().strip("`").strip()
    coincidencia = PATRON_MAGNITUD.match(limpio)
    if coincidencia is None:
        return None
    valor = _numero(coincidencia.group(1))
    if valor is None:
        return None
    return valor, _unidad(coincidencia.group(2))


def _unidad(texto):
    """Normaliza la unidad de 1 cita a la que declara la fila de `C-6`."""
    if not texto:
        return ""
    return ALIAS_UNIDADES.get(texto.strip(), texto.strip())


def _numero(texto):
    """Convierte 1 cifra decimal o con separadores de millar en número."""
    limpio = str(texto).strip()
    if re.fullmatch(r"[+-]?\d{1,3}(?:\.\d{3})+(?:,\d+)?", limpio):
        limpio = limpio.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"[+-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?", limpio):
        limpio = limpio.replace(",", "")
    elif re.fullmatch(r"[+-]?\d+(?:[.,]\d+)?", limpio):
        limpio = limpio.replace(",", ".")
    else:
        return None
    return float(limpio)


def _registros_de(raiz):
    """Lee los registros de ``results/gemma/`` del árbol recibido."""
    directorio = Path(raiz) / DIRECTORIO_REGISTROS
    if not directorio.is_dir():
        return {}
    registros = {}
    for ruta in sorted(directorio.rglob(f"*{SUFIJO_REGISTRO}")):
        lectura = comparar.leer_registro(ruta)
        frontmatter = lectura.get("frontmatter")
        identificador = (
            frontmatter.get("id") if isinstance(frontmatter, dict) else None
        )
        if not isinstance(identificador, str) or not identificador:
            raise ValueError(
                f"registro ilegible: {ruta} no declara el id de C-5"
            )
        registros[identificador] = lectura
    return registros


def _error_de_uso(detalle):
    """Imprime el uso incorrecto de `C-8` y devuelve su código."""
    print(f"[ERROR] {detalle}", file=sys.stderr)
    print(USO, file=sys.stderr)
    return CODIGO_USO_INCORRECTO


if __name__ == "__main__":
    raise SystemExit(main())
