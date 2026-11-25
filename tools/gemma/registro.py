"""Registro de ejecución de SPEC-017.

Implementa `RF-004`, `RF-006`, `RNF-004` y `RNF-005` conforme a `CA-003` y
`CA-005`, sobre los contratos `C-5` y `C-6` de `plan.md` y las decisiones
`DEC-002` y `DEC-020`: 1 solo archivo Markdown por ejecución con el frontmatter
de 11 claves de `C-5` y la tabla de 22 filas de `C-6`, creado con
``os.open(..., O_CREAT | O_EXCL)`` y con sufijo numérico ante colisión, de modo
que ninguna ejecución sobrescribe 1 registro previo.

Contrato:

- ``construir_registro(perfil, prueba, proposito, frontmatter, campos, *,
  instante=None, escenario=None) -> dict`` es pura: valida y devuelve
  exactamente las claves ``id``, ``frontmatter`` y ``filas`` sin escribir
  archivo alguno. ``id`` y
  ``frontmatter["id"]`` declaran la forma ``<AAAAMMDD>T<HHMMSS>Z-<perfil>-
  <prueba>`` en UTC y ``frontmatter["fecha_utc"]`` la forma
  ``YYYY-MM-DDTHH:MM:SSZ``. ``instante`` es 1 ``datetime`` inyectable para fijar
  el reloj; ausente, se toma ``datetime.now(timezone.utc)``, y 1 valor sin zona
  horaria se interpreta como UTC.
- ``frontmatter`` recibido aporta las 6 claves que calcula el orquestador
  —``huella_opciones``, ``opciones_efectivas``, ``vram_total_mib``,
  ``version_binario``, ``commit_llama_cpp`` y ``registro_anterior``—; la huella
  se transcribe como 1 dato recibido, porque `DEC-020` la calcula sobre las
  ``opciones`` declaradas en el manifiesto y no sobre las opciones efectivas.
  ``registro_anterior`` vale ``ninguno`` cuando falta o llega como ``None``.
- ``frontmatter`` admite además 1 clave opcional ``comparacion`` con el bloque
  de `C-7`: las 10 claves ``parametro``, ``medicion_inicial``,
  ``medicion_propuesta``, ``valor_inicial``, ``valor_propuesto`` y las 5
  ``delta_*`` —``delta_velocidad_generacion_tokens_por_segundo``,
  ``delta_velocidad_prompt_tokens_por_segundo``, ``delta_vram_asignada_mib``,
  ``delta_vram_libre_mib`` y ``delta_ram_mib``— más la clave adicional
  ``alternativa_contexto`` del caso de ``ctx_size`` con ``131072`` tokens, que
  no altera el recuento de 10. El bloque se escribe en 1 sola línea
  ``comparacion: <json>`` del frontmatter, después de las 11 claves de `C-5` y
  antes del cierre, en JSON compacto con claves ordenadas, de modo que
  ``comparar.leer_registro`` lo ignora sin fallar y ``json.loads`` lo
  reconstruye con los mismos tipos. Sin ese bloque el archivo no declara la
  línea y el registro conserva exactamente las 11 claves de `C-5`. 1 clave
  ausente de las 10, 1 clave ajena a `C-7` o 1 valor no serializable produce
  ``ValueError`` que nombra la clave.
- ``escenario`` de `SPEC-018` es 1 bloque opcional con las 4 entradas que
  aporta el orquestador —``escenario_id``, ``presupuesto_vram_declarado_mib``,
  ``vram_asignada_medida_mib`` y ``vram_libre_medida_mib``— del que el
  registro deriva ``delta_presupuesto_mib``, ``dictamen`` y
  ``conforme_presupuesto`` bajo la regla ``consumo <= presupuesto`` de
  `AMB-010`, conforme a `RF-008`, `CB-002` y `CA-006`. El bloque declara las 7
  claves en ese orden y se escribe en 1 sola línea
  ``escenario: <json compacto, claves ordenadas>`` después de las 11 claves de
  `C-5` y del bloque de comparación, antes del cierre del frontmatter. Cuando
  falta el presupuesto, la medición del consumo o ambas cosas, las claves no
  contrastables valen ``None`` y el ``dictamen`` declara la ausencia, de modo
  que el registro no inventa valor alguno; 1 clave ajena, 1 identificador sin
  el prefijo ``ESC-`` o 1 MiB fuera de rango producen ``ValueError`` que nombra
  la clave.
- ``campos`` es el mapa ordenado de las 22 etiquetas de `C-6` a su texto. Las
  13 magnitudes —6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19 y 22— declaran su
  unidad en el valor: ``<número> <unidad>`` con ``tokens`` en 6 y 9,
  ``ranuras`` en 7, ``capas`` en 8, ``s`` en 12, ``MiB`` en 13, 14, 15, 19 y
  22, y ``tokens/s`` en 16 y 17; el campo 11 porta su unidad en el techo del
  vocabulario ``activado (techo de borrador N tokens)`` o
  ``desactivado (sin techo de borrador)``, y el campo 18 admite solo
  ``continúa en servicio`` o ``se detuvo``. La marca ``no disponible`` se admite
  en cualquier fila cuando falta la fuente, de modo que el número de campos
  vacíos es 0.
- ``escribir_registro(directorio, registro) -> pathlib.Path`` crea el
  directorio si falta y crea ``directorio/<id>.md`` con
  ``O_CREAT | O_EXCL``; si la ruta existe, aplica el sufijo ``-2``, ``-3`` y
  siguientes al identificador y al nombre del archivo, y el archivo creado
  declara en su frontmatter el identificador con sufijo. Ante 1 valor vacío, 1
  magnitud sin unidad, 1 vocabulario fuera de forma, 1 ``proposito`` inválido o
  1 clave de frontmatter ausente, la función lanza ``ValueError`` que nombra la
  fila, la unidad, el vocabulario o la clave, nunca ``KeyError`` sin contexto.

Alcance: usa solo la biblioteca estándar, no lee ``bin/``, ``models/``,
``llama.cpp/`` ni ``.env`` y no escribe fuera del directorio que recibe. La
carpeta de registros la elige el orquestador, conforme a `DEC-002` y `DEC-012`.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

__all__ = ["construir_registro", "escribir_registro"]

NO_DISPONIBLE = "no disponible"

# `C-5`: los 3 propósitos admitidos.
PROPOSITOS = ("carga", "medicion", "comparacion")

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

# `C-5`: las 6 claves que aporta el orquestador y el registro transcribe.
CLAVES_RECIBIDAS = (
    "huella_opciones",
    "opciones_efectivas",
    "vram_total_mib",
    "version_binario",
    "commit_llama_cpp",
    "registro_anterior",
)

# `C-7`: las 10 claves del bloque de comparación, en el orden del contrato.
CLAVES_COMPARACION = (
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

# `C-7`: la clave adicional del caso de `ctx_size` con `131072` tokens, que no
# altera el recuento de las 10.
CLAVE_ALTERNATIVA = "alternativa_contexto"

# `C-7`: el bloque viaja en esta clave opcional del frontmatter.
CLAVE_COMPARACION = "comparacion"

# `C-5` de `SPEC-018`: el bloque de conformidad presupuestaria viaja en esta
# clave opcional del frontmatter y no altera las 11 claves de `C-5`.
CLAVE_ESCENARIO = "escenario"

# `C-5` de `SPEC-018`: las 4 entradas que aporta el orquestador.
ENTRADAS_ESCENARIO = (
    "escenario_id",
    "presupuesto_vram_declarado_mib",
    "vram_asignada_medida_mib",
    "vram_libre_medida_mib",
)

# `C-5` de `SPEC-018`: las 3 claves que deriva el registro.
CLAVES_DERIVADAS_ESCENARIO = (
    "delta_presupuesto_mib",
    "dictamen",
    "conforme_presupuesto",
)

# `C-5` de `SPEC-018`: las 7 claves del bloque, en el orden de declaración.
CLAVES_ESCENARIO = ENTRADAS_ESCENARIO + CLAVES_DERIVADAS_ESCENARIO

# `C-5` de `SPEC-018`: el identificador declara el prefijo del catálogo.
PREFIJO_ESCENARIO = "ESC-"

# `C-5` de `SPEC-018`: la regla `consumo <= presupuesto` de `AMB-010` y los 3
# dictámenes que declaran la ausencia de contraste sin inventar valores.
DICTAMEN_CONFORME = "conforme"
DICTAMEN_SIN_PRESUPUESTO = "no contrastable: falta el presupuesto declarado"
DICTAMEN_SIN_MEDICION = "no contrastable: falta la medición de VRAM asignada"
DICTAMEN_SIN_AMBOS = (
    "no contrastable: faltan el presupuesto declarado y la medición de VRAM "
    "asignada"
)

# `C-7`: las 3 claves del bloque que declaran 1 texto no vacío.
CLAVES_TEXTO_COMPARACION = (
    "parametro",
    "medicion_inicial",
    "medicion_propuesta",
)

# `C-7`: las 5 claves que declaran 1 diferencia numérica.
CLAVES_DIFERENCIA_COMPARACION = tuple(
    clave for clave in CLAVES_COMPARACION if clave.startswith("delta_")
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

# `C-6`: las 12 filas con unidad de magnitud propia, por número de fila. La
# decimotercera es el campo 11, cuyo vocabulario porta el techo en tokens.
UNIDADES_POR_NUMERO = {
    6: "tokens",
    7: "ranuras",
    8: "capas",
    9: "tokens",
    12: "s",
    13: "MiB",
    14: "MiB",
    15: "MiB",
    16: "tokens/s",
    17: "tokens/s",
    19: "MiB",
    22: "MiB",
}

# `C-6`: el campo 11 declara el estado y, si está activado, el techo del
# borrador; la forma sin techo es literal.
FORMA_11_DESACTIVADO = "desactivado (sin techo de borrador)"
PATRON_11_ACTIVADO = re.compile(r"^activado \(techo de borrador \d+ tokens\)$")

# `C-6`: el campo 18 declara solo la estabilidad observada al cierre.
FORMAS_CAMPO_18 = ("continúa en servicio", "se detuvo")

# `C-6`: 1 magnitud declara 1 número y después su unidad.
PATRON_MAGNITUD = re.compile(r"^\d+(?:\.\d+)?$")

# `C-6`: la fecha de la prueba declara la forma `YYYY-MM-DD`.
PATRON_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# `C-5`: el identificador también es el nombre del archivo, sin separadores.
PATRON_IDENTIFICADOR = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

# Marcas de forma de `C-5`.
FORMATO_ID = "%Y%m%dT%H%M%SZ"
FORMATO_FECHA_UTC = "%Y-%m-%dT%H:%M:%SZ"
REGISTRO_ANTERIOR_AUSENTE = "ninguno"

# `RNF-004`: la creación exclusiva impide la sobrescritura por construcción.
BANDERAS_EXCLUSIVAS = (
    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
)
MODO_ARCHIVO = 0o666

# `C-6`: las 3 columnas de la tabla, en el encabezado y en cada fila.
ENCABEZADO_TABLA = "| N.º | Campo | Valor |"
SEPARADOR_TABLA = "| --- | --- | --- |"


def construir_registro(
    perfil,
    prueba,
    proposito,
    frontmatter,
    campos,
    *,
    instante=None,
    escenario=None,
):
    """Valida y devuelve el registro de 1 ejecución sin escribir archivo.

    ``perfil`` y ``prueba`` forman el identificador junto con el instante UTC;
    ``proposito`` pertenece a ``PROPOSITOS``; ``frontmatter`` aporta las 6
    claves que calcula el orquestador y admite las claves opcionales
    ``comparacion`` de `C-7` y ``escenario`` de `SPEC-018`, que también llega
    como ``escenario``; ``campos`` el texto de las 22 filas de `C-6`. Toda
    irregularidad lanza ``ValueError`` con la fila, la unidad, el vocabulario o
    la clave afectada.
    """
    nombre_perfil = _validar_identificador("perfil", perfil)
    nombre_prueba = _validar_identificador("prueba", prueba)
    momento = _instante_utc(instante)
    identificador = (
        f"{momento.strftime(FORMATO_ID)}-{nombre_perfil}-{nombre_prueba}"
    )

    recibido = _frontmatter_de_c5(frontmatter)
    frontmatter_registro = {
        "id": identificador,
        "fecha_utc": momento.strftime(FORMATO_FECHA_UTC),
        "perfil": nombre_perfil,
        "prueba": nombre_prueba,
        "proposito": _validar_proposito(proposito),
        "huella_opciones": recibido["huella_opciones"],
        "opciones_efectivas": recibido["opciones_efectivas"],
        "vram_total_mib": recibido["vram_total_mib"],
        "version_binario": recibido["version_binario"],
        "commit_llama_cpp": recibido["commit_llama_cpp"],
        "registro_anterior": recibido["registro_anterior"],
    }
    comparacion = _comparacion_de_c7(frontmatter.get(CLAVE_COMPARACION))
    if comparacion is not None:
        # `C-7`: la clave se suma a las 11 de `C-5` solo cuando la prueba es
        # comparativa; sin ella el registro conserva el formato de `T-025`.
        frontmatter_registro[CLAVE_COMPARACION] = comparacion
    bloque_escenario = _escenario_de_c5(
        escenario if escenario is not None else frontmatter.get(CLAVE_ESCENARIO)
    )
    if bloque_escenario is not None:
        # `SPEC-018`: el bloque de conformidad se suma a las 11 claves de `C-5`
        # solo cuando la ejecución declara el escenario del catálogo.
        frontmatter_registro[CLAVE_ESCENARIO] = bloque_escenario

    return {
        "id": identificador,
        "frontmatter": frontmatter_registro,
        "filas": _filas_de_c6(campos),
    }

def escribir_registro(directorio, registro):
    """Crea ``directorio/<id>.md`` sin sobrescribir y devuelve su ruta.

    El directorio se crea si falta. Cuando la ruta ya existe, el identificador
    y el nombre del archivo reciben el sufijo ``-2``, ``-3`` y siguientes, y el
    archivo nuevo transcribe en su frontmatter el identificador con sufijo; el
    archivo previo no se abre ni se modifica.
    """
    carpeta = Path(directorio)
    _validar_registro(registro)
    identificador = registro["id"]
    # Se serializa 1 vez antes de crear nada: 1 valor inválido no deja archivos.
    _texto_del_registro(registro, identificador)

    carpeta.mkdir(parents=True, exist_ok=True)

    sufijo = 1
    while True:
        candidato = identificador if sufijo == 1 else f"{identificador}-{sufijo}"
        ruta = carpeta / f"{candidato}.md"
        try:
            descriptor = os.open(ruta, BANDERAS_EXCLUSIVAS, MODO_ARCHIVO)
        except FileExistsError:
            sufijo += 1
            continue
        break

    texto = _texto_del_registro(registro, candidato)
    try:
        with os.fdopen(descriptor, "wb") as flujo:
            flujo.write(texto.encode("utf-8"))
    except BaseException:
        try:
            ruta.unlink()
        except OSError:
            pass
        raise
    return ruta


def _instante_utc(instante):
    """Devuelve el instante en UTC; ausente, toma el reloj del sistema."""
    if instante is None:
        return datetime.now(timezone.utc)
    if not isinstance(instante, datetime):
        raise ValueError(
            "instante: se esperaba 1 datetime y se recibió "
            f"{type(instante).__name__}"
        )
    if instante.tzinfo is None:
        return instante.replace(tzinfo=timezone.utc)
    return instante.astimezone(timezone.utc)


def _validar_identificador(clave, valor):
    """Valida 1 identificador de perfil o de prueba que compone el nombre."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(
            f"{clave}: se esperaba 1 identificador no vacío y se recibió "
            f"{valor!r}"
        )
    texto = valor.strip()
    if not PATRON_IDENTIFICADOR.match(texto):
        raise ValueError(
            f"{clave}: el identificador {texto!r} no admite separadores ni "
            "espacios porque compone el nombre del archivo del registro"
        )
    return texto


def _validar_proposito(proposito):
    """Valida el propósito contra el vocabulario de `C-5`."""
    if proposito not in PROPOSITOS:
        raise ValueError(
            f"proposito: {proposito!r} no pertenece al vocabulario de C-5, "
            f"que admite {' '.join(PROPOSITOS)}"
        )
    return proposito


def _frontmatter_de_c5(frontmatter):
    """Valida las 6 claves recibidas y devuelve sus valores normalizados."""
    if not isinstance(frontmatter, dict):
        raise ValueError(
            "frontmatter: se esperaba 1 mapa con las 6 claves de C-5 y se "
            f"recibió {type(frontmatter).__name__}"
        )
    valores = {}
    for clave in CLAVES_RECIBIDAS:
        if clave not in frontmatter:
            raise ValueError(f"frontmatter: falta la clave {clave} de C-5")
        valores[clave] = _normalizar_clave(clave, frontmatter[clave])
    return valores


def _normalizar_clave(clave, valor):
    """Normaliza 1 clave de `C-5` y rechaza su valor vacío con la clave."""
    referencia = f"frontmatter: la clave {clave}"
    if clave == "registro_anterior":
        if valor is None:
            return REGISTRO_ANTERIOR_AUSENTE
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
        raise ValueError(
            f"{referencia} declara {valor!r}; se espera 1 identificador de "
            "registro previo o None"
        )
    if clave == "opciones_efectivas":
        if not isinstance(valor, dict) or not valor:
            raise ValueError(
                f"{referencia} declara {valor!r}; se espera el objeto de "
                "opciones que aplicó el lanzador"
            )
        return dict(valor)
    if clave == "vram_total_mib":
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(
                f"{referencia} declara {valor!r}; se esperan los MiB de la GPU "
                "dedicada"
            )
        return valor
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(
            f"{referencia} está vacía; C-5 exige 1 valor declarado"
        )
    return valor.strip()


def _comparacion_de_c7(bloque):
    """Valida el bloque de `C-7` y lo devuelve ordenado, o ``None`` si falta.

    Exige las 10 claves del contrato, admite ``alternativa_contexto`` como
    clave adicional del caso de ``ctx_size`` con ``131072`` tokens y rechaza
    cualquier otra clave y 1 valor fuera de forma con ``ValueError`` que nombra
    la clave afectada.
    """
    if bloque is None:
        return None
    if not isinstance(bloque, dict):
        raise ValueError(
            f"{CLAVE_COMPARACION}: se esperaba 1 mapa con las 10 claves de C-7 "
            f"y se recibió {type(bloque).__name__}"
        )
    for clave in CLAVES_COMPARACION:
        if clave not in bloque:
            raise ValueError(
                f"{CLAVE_COMPARACION}: falta la clave {clave} de las 10 de C-7, "
                "de modo que el bloque es incompleto"
            )
    admitidas = set(CLAVES_COMPARACION) | {CLAVE_ALTERNATIVA}
    for clave in bloque:
        if clave not in admitidas:
            raise ValueError(
                f"{CLAVE_COMPARACION}: la clave {clave} no pertenece a C-7, "
                f"que declara las 10 claves del bloque más {CLAVE_ALTERNATIVA}"
            )
    for clave in CLAVES_TEXTO_COMPARACION:
        valor = bloque[clave]
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                f"{CLAVE_COMPARACION}: la clave {clave} declara {valor!r}; C-7 "
                "exige 1 texto no vacío"
            )
    for clave in CLAVES_DIFERENCIA_COMPARACION:
        valor = bloque[clave]
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(
                f"{CLAVE_COMPARACION}: la clave {clave} declara {valor!r}; C-7 "
                "exige 1 diferencia numérica"
            )
    ordenado = {clave: bloque[clave] for clave in CLAVES_COMPARACION}
    if CLAVE_ALTERNATIVA in bloque:
        ordenado[CLAVE_ALTERNATIVA] = bloque[CLAVE_ALTERNATIVA]
    _json_comparacion(ordenado)
    return ordenado


def _json_comparacion(bloque):
    """Serializa el bloque de `C-7` en JSON compacto con claves ordenadas."""
    try:
        return json.dumps(
            bloque, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{CLAVE_COMPARACION}: el bloque de C-7 no es serializable en JSON: "
            f"{error}"
        ) from error


def _escenario_de_c5(bloque):
    """Valida el bloque de `SPEC-018` y devuelve sus 7 claves en orden.

    ``bloque`` aporta las 4 entradas del orquestador; el registro deriva
    ``delta_presupuesto_mib`` como consumo medido menos presupuesto declarado,
    ``conforme_presupuesto`` bajo la regla ``consumo <= presupuesto`` de
    `AMB-010` y ``dictamen`` como su forma legible. 1 entrada ausente o
    ``None`` no se sustituye por estimación alguna: la clave no contrastable
    vale ``None`` y el dictamen declara la ausencia. Las claves derivadas se
    recalculan siempre, de modo que la función es idempotente sobre su propio
    resultado y ``escribir_registro`` vuelve a validar el bloque ya derivado.
    """
    if bloque is None:
        return None
    if not isinstance(bloque, dict):
        raise ValueError(
            f"{CLAVE_ESCENARIO}: se esperaba 1 mapa con las 4 entradas de C-5 y "
            f"se recibió {type(bloque).__name__}"
        )
    admitidas = set(CLAVES_ESCENARIO)
    for clave in bloque:
        if clave not in admitidas:
            raise ValueError(
                f"{CLAVE_ESCENARIO}: la clave {clave} no pertenece a C-5 de "
                "SPEC-018, que declara las 4 entradas del orquestador y las 3 "
                "claves derivadas"
            )
    identificador = _escenario_id(bloque.get("escenario_id"))
    presupuesto = _mib_de_escenario(
        "presupuesto_vram_declarado_mib",
        bloque.get("presupuesto_vram_declarado_mib"),
        positivo=True,
    )
    asignada = _mib_de_escenario(
        "vram_asignada_medida_mib",
        bloque.get("vram_asignada_medida_mib"),
        positivo=False,
    )
    libre = _mib_de_escenario(
        "vram_libre_medida_mib",
        bloque.get("vram_libre_medida_mib"),
        positivo=False,
    )
    delta, dictamen, conforme = _dictamen_de_presupuesto(presupuesto, asignada)
    return {
        "escenario_id": identificador,
        "presupuesto_vram_declarado_mib": presupuesto,
        "vram_asignada_medida_mib": asignada,
        "vram_libre_medida_mib": libre,
        "delta_presupuesto_mib": delta,
        "dictamen": dictamen,
        "conforme_presupuesto": conforme,
    }


def _escenario_id(valor):
    """Valida el identificador canónico del escenario ejecutado."""
    if valor is None:
        raise ValueError(
            f"{CLAVE_ESCENARIO}: falta la clave escenario_id de C-5, que "
            "identifica el escenario del catálogo que se ejecutó"
        )
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(
            f"{CLAVE_ESCENARIO}: la clave escenario_id declara {valor!r}; C-5 "
            "exige 1 identificador no vacío"
        )
    texto = valor.strip()
    if not texto.startswith(PREFIJO_ESCENARIO):
        raise ValueError(
            f"{CLAVE_ESCENARIO}: la clave escenario_id declara {texto!r}; el "
            f"identificador del catálogo declara el prefijo {PREFIJO_ESCENARIO}"
        )
    return texto


def _mib_de_escenario(clave, valor, *, positivo):
    """Valida 1 entrada en MiB; ``None`` la declara no contrastable."""
    if valor is None:
        return None
    forma = "mayor que 0" if positivo else "no negativo"
    mensaje = (
        f"{CLAVE_ESCENARIO}: la clave {clave} declara {valor!r}; C-5 exige "
        f"1 número {forma} en MiB"
    )
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(mensaje)
    fuera_de_rango = valor <= 0 if positivo else valor < 0
    if fuera_de_rango:
        raise ValueError(mensaje)
    return valor


def _dictamen_de_presupuesto(presupuesto, asignada):
    """Aplica la regla ``consumo <= presupuesto`` de `AMB-010`.

    Devuelve la tupla ``(delta, dictamen, conforme)``; sin las 2 magnitudes no
    hay contraste y las 3 posiciones declaran la ausencia con ``None``.
    """
    if presupuesto is None and asignada is None:
        return None, DICTAMEN_SIN_AMBOS, None
    if presupuesto is None:
        return None, DICTAMEN_SIN_PRESUPUESTO, None
    if asignada is None:
        return None, DICTAMEN_SIN_MEDICION, None
    delta = asignada - presupuesto
    if delta > 0:
        return delta, f"excede presupuesto por {delta} MiB", False
    return delta, DICTAMEN_CONFORME, True


def _json_escenario(bloque):
    """Serializa el bloque de `SPEC-018` en JSON compacto, claves ordenadas."""
    try:
        return json.dumps(
            bloque, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{CLAVE_ESCENARIO}: el bloque de C-5 no es serializable en JSON: "
            f"{error}"
        ) from error


def _filas_de_c6(campos):
    """Valida y devuelve las 22 filas de `C-6` en el orden de `RF-006`."""
    if not isinstance(campos, dict):
        raise ValueError(
            "campos: se esperaba 1 mapa de etiqueta a texto con las 22 filas "
            f"de C-6 y se recibió {type(campos).__name__}"
        )
    filas = []
    for numero, campo in enumerate(CAMPOS_C6, start=1):
        if campo not in campos:
            raise ValueError(
                f"fila {numero} ({campo}): falta el valor de la fila de C-6"
            )
        filas.append(
            {
                "numero": numero,
                "campo": campo,
                "valor": _validar_valor(numero, campo, campos[campo]),
            }
        )
    return filas


def _validar_valor(numero, campo, valor):
    """Valida el valor de 1 fila y lo devuelve sin espacios de borde."""
    referencia = f"fila {numero} ({campo})"
    if not isinstance(valor, str):
        raise ValueError(
            f"{referencia}: se esperaba 1 valor de texto y se recibió {valor!r}"
        )
    texto = valor.strip()
    if not texto:
        raise ValueError(
            f"{referencia}: el valor está vacío; C-6 y RNF-005 exigen 0 campos "
            "vacíos"
        )
    if texto == NO_DISPONIBLE:
        return texto
    if numero == 1:
        if not PATRON_FECHA.match(texto):
            raise ValueError(
                f"{referencia}: la fecha {texto!r} no declara la forma "
                "YYYY-MM-DD de C-6"
            )
        return texto
    if numero == 11:
        if texto == FORMA_11_DESACTIVADO or PATRON_11_ACTIVADO.match(texto):
            return texto
        raise ValueError(
            f"{referencia}: el vocabulario de C-6 es 'activado (techo de "
            f"borrador N tokens)' o '{FORMA_11_DESACTIVADO}' y se recibió "
            f"{texto!r}"
        )
    if numero == 18:
        if texto in FORMAS_CAMPO_18:
            return texto
        raise ValueError(
            f"{referencia}: el vocabulario de C-6 es "
            f"{' o '.join(FORMAS_CAMPO_18)} y se recibió {texto!r}"
        )
    unidad = UNIDADES_POR_NUMERO.get(numero)
    if unidad is None:
        return texto
    cantidad, separador, declarada = texto.rpartition(" ")
    if (
        separador != " "
        or declarada != unidad
        or not PATRON_MAGNITUD.match(cantidad)
    ):
        raise ValueError(
            f"{referencia}: la magnitud {texto!r} no declara la forma "
            f"'<número> {unidad}' que exige C-6"
        )
    return texto


def _validar_registro(registro):
    """Comprueba la forma del registro antes de crear archivo alguno."""
    if not isinstance(registro, dict):
        raise ValueError(
            "registro: se esperaba 1 mapa con id, frontmatter y filas y se "
            f"recibió {type(registro).__name__}"
        )
    identificador = registro.get("id")
    if not isinstance(identificador, str) or not PATRON_IDENTIFICADOR.match(
        identificador
    ):
        raise ValueError(
            f"registro: el id {identificador!r} no declara la forma "
            "<AAAAMMDD>T<HHMMSS>Z-<perfil>-<prueba> de C-5"
        )
    frontmatter = registro.get("frontmatter")
    if not isinstance(frontmatter, dict):
        raise ValueError("registro: falta el frontmatter de C-5")
    if frontmatter.get("id") != identificador:
        raise ValueError(
            "registro: el frontmatter declara el id "
            f"{frontmatter.get('id')!r} y el registro declara "
            f"{identificador!r}"
        )
    filas = registro.get("filas")
    if not isinstance(filas, list) or len(filas) != len(CAMPOS_C6):
        recibidas = len(filas) if isinstance(filas, list) else 0
        raise ValueError(
            f"registro: se esperaban {len(CAMPOS_C6)} filas de C-6 y se "
            f"recibieron {recibidas}"
        )
    for fila in filas:
        if not isinstance(fila, dict):
            raise ValueError(
                "registro: cada fila de C-6 debe ser 1 mapa con numero, campo "
                "y valor"
            )
        for clave in ("numero", "campo", "valor"):
            if clave not in fila:
                raise ValueError(
                    f"registro: 1 fila de C-6 no declara la clave {clave}"
                )


def _texto_del_registro(registro, identificador):
    """Serializa el registro completo con el identificador indicado.

    Las 11 claves de `C-5` se escriben en su orden y, cuando el frontmatter
    declara los bloques opcionales, después de ellas se escriben 1 línea
    ``comparacion:`` de `C-7` y 1 línea ``escenario:`` de `SPEC-018`, en ese
    orden y antes del cierre, cada una con su objeto en JSON de 1 sola línea.
    """
    frontmatter = dict(registro["frontmatter"])
    frontmatter["id"] = identificador

    lineas = ["---"]
    for clave in CLAVES_FRONTMATTER:
        if clave not in frontmatter:
            raise ValueError(
                "registro: el frontmatter no declara la clave "
                f"{clave} de C-5"
            )
        lineas.append(f"{clave}: {_valor_serializado(clave, frontmatter[clave])}")
    comparacion = _comparacion_de_c7(frontmatter.get(CLAVE_COMPARACION))
    if comparacion is not None:
        lineas.append(f"{CLAVE_COMPARACION}: {_json_comparacion(comparacion)}")
    escenario = _escenario_de_c5(frontmatter.get(CLAVE_ESCENARIO))
    if escenario is not None:
        lineas.append(f"{CLAVE_ESCENARIO}: {_json_escenario(escenario)}")
    lineas.extend(["---", "", ENCABEZADO_TABLA, SEPARADOR_TABLA])
    for fila in registro["filas"]:
        lineas.append(
            f"| {fila['numero']} | {_celda(fila['campo'])} | "
            f"{_celda(fila['valor'])} |"
        )
    return "\n".join(lineas) + "\n"


def _valor_serializado(clave, valor):
    """Serializa 1 valor del frontmatter; las opciones van en JSON."""
    if clave == "opciones_efectivas":
        try:
            return json.dumps(valor, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "frontmatter: la clave opciones_efectivas no es serializable "
                f"en JSON: {error}"
            ) from error
    return str(valor)


def _celda(valor):
    """Prepara 1 celda: sin saltos de línea y con la barra escapada."""
    texto = str(valor).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    return texto.strip().replace("|", "\\|")
