"""Estados y elegibilidad de promoción de los perfiles de SPEC-017.

Implementa `RF-007`, `CB-004`, `CB-006`, `RNF-003`, `RNF-006` y `RNF-007`
conforme a `CA-004`, `CA-007` y `CA-015`, sobre la tabla de `C-4`, el bloque de
`C-7` y las decisiones `DEC-002` (el estado y las opciones viven en el
manifiesto), `DEC-008` (el valor inicial rige mientras la desviación no declara
1 comparación completa), `DEC-009` (solo la firma `G` acredita la aprobación),
`DEC-012` (funciones puras, sin GPU ni artefactos reales) y `DEC-020` (la huella
se calcula sobre las `opciones` declaradas y no sobre las efectivas).

Contrato:

- ``estado_reportado(manifiesto, registros) -> (estado, motivo | None)``
  aplica `C-4`. ``candidato`` declarado se reporta ``candidato`` sin motivo.
  ``medido`` exige 1 registro cuyo ``huella_opciones`` es igual a
  ``perfiles.huella_opciones(manifiesto["opciones"])``; sin registro
  coincidente se reporta ``candidato`` con 1 motivo que nombra la falta de
  medición o las opciones modificadas. ``aprobado`` exige ``medido`` vigente,
  cada desviación con su bloque de comparación completo de las 10 claves de
  `C-7`, ``aprobacion.umbral_tg_tokens_por_segundo`` presente,
  ``aprobacion.declarado_por`` con fecha, y la última carga con
  ``desbordamiento_mib`` igual a ``0`` y ``vram_libre_mib`` de al menos
  ``512``; si falla 1 condición, el estado reportado es ``candidato`` y el
  motivo la nombra con su valor.
- ``elegible_para_aprobado(manifiesto, registros, ultima_carga) -> (bool,
  motivo | None)`` devuelve ``(True, None)`` solo si se cumplen todas las
  condiciones anteriores. ``ultima_carga`` es el identificador del registro de
  la carga y debe existir en ``registros``: el desbordamiento se lee de su
  fila 19 y la VRAM libre de su fila 14 de `C-6`.
- ``verificar_aprobacion(manifiesto, *, ruta, ejecutor=None) -> (bool, motivo |
  None)`` consulta ``git log --format=%G? -1 -- <ruta>`` y acredita solo la
  firma ``G``; ``N``, ``B`` y ``U`` no acreditan y el motivo transcribe el
  estado leído. ``ejecutor`` es inyectable como ``ejecutor(comando) -> texto``
  con 1 solo ``str``: la suite nunca invoca ``git``, conforme a `DEC-012`.
  Ausente, se consulta con ``subprocess``.

Criterio de última carga: la última carga es el registro cuyo frontmatter
declara ``proposito`` igual a ``carga`` y cuyo identificador, con la forma de
fecha UTC de `C-5` (``<AAAAMMDD>T<HHMMSS>Z-<perfil>-<prueba>``), es el
cronológicamente mayor entre esos registros. Un identificador posterior con
otro propósito —``medicion`` o ``comparacion``— no desplaza la carga. El mismo
criterio lo reutilizan ``estado_reportado`` y ``elegible_para_aprobado``, y no
existe un criterio adicional.

Nivel de las claves: ``huella_opciones`` y el bloque ``comparacion`` se leen en
el ``frontmatter`` de la lectura y, si no están, en el nivel superior del propio
elemento. ``huella_opciones`` se calcula siempre sobre las ``opciones``
declaradas del manifiesto (`DEC-020`), nunca sobre las efectivas.

Alcance: funciones puras salvo la consulta de firma. No escriben archivos, no
tocan `results/` y no leen `bin/`, `models/`, `llama.cpp/` ni `.env`.
"""

from __future__ import annotations

import subprocess

import perfiles

__all__ = [
    "elegible_para_aprobado",
    "estado_reportado",
    "verificar_aprobacion",
]

# `C-4`: la huella conserva `medido` o degrada con este motivo literal.
MOTIVO_OPCIONES_MODIFICADAS = "opciones modificadas"

# Los 3 estados de `RF-007`, en el orden de la tabla de `C-4`.
ESTADOS = ("candidato", "medido", "aprobado")

# `C-7`: el bloque es completo solo si declara estas 10 claves;
# `alternativa_contexto` es adicional y no altera el recuento.
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

# `C-6`: las 2 filas que decide la elegibilidad de `C-4`.
FILA_VRAM_LIBRE = 14
FILA_DESBORDAMIENTO = 19

# `C-4`: umbrales de la última carga.
DESBORDAMIENTO_ADMITIDO_MIB = 0.0
VRAM_LIBRE_MINIMA_MIB = 512.0

# `C-5`: el único propósito que identifica la carga.
PROPOSITO_CARGA = "carga"

# `C-6`: la marca que impide certificar 1 magnitud.
NO_DISPONIBLE = "no disponible"

# Marca para distinguir «la clave no está en ningún nivel» de «vale `None`».
_AUSENTE = object()


def estado_reportado(manifiesto, registros):
    """Estado de `C-4` que el sistema reporta para 1 perfil.

    Devuelve ``(estado, motivo)``: el estado declarado se conserva solo si se
    cumplen sus condiciones; si alguna falla, el estado es ``candidato`` y el
    motivo nombra la condición incumplida con su valor.
    """
    declarado = _estado_declarado(manifiesto)
    if declarado == "candidato":
        return ("candidato", None)

    lecturas = _registros(registros)
    motivo = _motivo_huella(manifiesto, lecturas)
    if motivo is not None:
        return ("candidato", motivo)
    if declarado == "medido":
        return ("medido", None)

    motivo = _motivo_de_aprobado(manifiesto, lecturas, _ultima_carga(lecturas))
    if motivo is not None:
        return ("candidato", motivo)
    return ("aprobado", None)


def elegible_para_aprobado(manifiesto, registros, ultima_carga):
    """Indica si el perfil cumple todas las condiciones de `aprobado` de `C-4`.

    ``ultima_carga`` es el identificador del registro de la carga: debe existir
    en ``registros``, declarar ``proposito`` igual a ``carga`` y aportar las
    filas 19 y 14 de `C-6`. La elegibilidad evalúa las condiciones de `C-4` y no
    el estado declarado en el manifiesto.
    """
    lecturas = _registros(registros)
    _lectura_carga(lecturas, ultima_carga)

    motivo = _motivo_de_aprobado(manifiesto, lecturas, ultima_carga)
    if motivo is not None:
        return (False, motivo)
    return (True, None)


def verificar_aprobacion(manifiesto, *, ruta, ejecutor=None):
    """Contrasta la firma del último commit que toca el manifiesto (`DEC-009`).

    Solo la firma ``G`` acredita la aprobación. ``N``, ``B`` y ``U`` no
    acreditan y el motivo transcribe el estado leído. ``ejecutor`` recibe el
    comando como 1 solo ``str`` y devuelve su texto; ausente, se consulta con
    ``subprocess``.
    """
    if not isinstance(manifiesto, dict):
        raise ValueError(
            "manifiesto: se esperaba 1 objeto con el perfil y se recibió "
            f"{type(manifiesto).__name__}"
        )
    if not isinstance(ruta, (str, bytes)) and not hasattr(ruta, "__fspath__"):
        raise ValueError(
            f"ruta: se esperaba la ruta del manifiesto y se recibió {ruta!r}"
        )
    if not str(ruta).strip():
        raise ValueError("ruta: la ruta del manifiesto no puede quedar vacía")

    comando = f"git log --format=%G? -1 -- {ruta}"
    if ejecutor is None:
        salida = _consulta_git(ruta)
    else:
        try:
            salida = ejecutor(comando)
        except OSError as error:
            raise ValueError(
                f"git: no se pudo consultar la firma de «{ruta}»: {error}"
            ) from error

    estado = _estado_de_firma(salida)
    if estado == "G":
        return (True, None)
    if estado in ("N", "B", "U"):
        return (
            False,
            f"la firma del último commit que toca «{ruta}» declara el estado "
            f"«{estado}» y solo «G» acredita la aprobación",
        )
    return (
        False,
        f"la consulta de firma de «{ruta}» no devolvió 1 estado de git "
        f"(`%G?`) reconocible: {estado!r}",
    )


def _estado_declarado(manifiesto):
    """Estado declarado en el manifiesto, validado contra los 3 de `RF-007`."""
    if not isinstance(manifiesto, dict):
        raise ValueError(
            "manifiesto: se esperaba 1 objeto con el perfil y se recibió "
            f"{type(manifiesto).__name__}"
        )
    estado = _requerido(manifiesto, "estado", "manifiesto")
    if estado not in ESTADOS:
        raise ValueError(
            f"manifiesto: el estado «{estado}» no está entre "
            f"{', '.join(ESTADOS)}"
        )
    return estado


def _registros(registros):
    """Valida el mapa identificador → lectura que reciben las 2 funciones."""
    if not isinstance(registros, dict):
        raise ValueError(
            "registros: se esperaba 1 mapa identificador → registro y se "
            f"recibió {type(registros).__name__}"
        )
    return registros


def _requerido(contenedor, clave, contexto):
    """Devuelve ``contenedor[clave]`` o falla nombrando la clave ausente."""
    if not isinstance(contenedor, dict) or not contenedor:
        raise ValueError(
            f"{contexto}: se esperaba 1 objeto y se recibió "
            f"{type(contenedor).__name__}"
        )
    if clave not in contenedor:
        raise ValueError(f"{contexto}: falta la clave obligatoria «{clave}»")
    return contenedor[clave]


def _clave_lectura(lectura, clave):
    """Lee 1 clave en el frontmatter y, si falta, en el nivel superior."""
    if isinstance(lectura, dict):
        frontmatter = lectura.get("frontmatter")
        if isinstance(frontmatter, dict) and clave in frontmatter:
            return frontmatter[clave]
        if clave in lectura:
            return lectura[clave]
    return _AUSENTE


def _proposito(lectura, identificador):
    """Propósito de `C-5` declarado en el frontmatter de 1 lectura."""
    frontmatter = lectura.get("frontmatter") if isinstance(lectura, dict) else None
    if not isinstance(frontmatter, dict):
        raise ValueError(
            f"registro «{identificador}»: falta el frontmatter de C-5"
        )
    proposito = frontmatter.get("proposito")
    if not isinstance(proposito, str) or not proposito.strip():
        raise ValueError(
            f"registro «{identificador}»: falta la clave «proposito» de C-5"
        )
    return proposito


def _ultima_carga(registros):
    """Identificador de la última carga según el criterio documentado.

    Filtra los registros con ``proposito`` igual a ``carga`` y devuelve el
    identificador cronológicamente mayor: la forma de `C-5` comienza con la
    fecha UTC ``<AAAAMMDD>T<HHMMSS>Z``, de modo que el orden lexicográfico es
    el orden temporal. Sin cargas devuelve ``None``.
    """
    cargas = [
        identificador
        for identificador, lectura in registros.items()
        if _proposito(lectura, identificador) == PROPOSITO_CARGA
    ]
    if not cargas:
        return None
    return max(cargas)


def _lectura_carga(registros, ultima_carga):
    """Lectura de la carga indicada, validada como registro de propósito carga."""
    if not isinstance(ultima_carga, str) or not ultima_carga.strip():
        raise ValueError(
            "ultima_carga: se esperaba el identificador del registro de carga "
            f"y se recibió {ultima_carga!r}"
        )
    if ultima_carga not in registros:
        raise ValueError(
            f"ultima_carga: el registro «{ultima_carga}» no existe entre los "
            "registros recibidos"
        )
    lectura = registros[ultima_carga]
    proposito = _proposito(lectura, ultima_carga)
    if proposito != PROPOSITO_CARGA:
        raise ValueError(
            f"registro «{ultima_carga}»: declara proposito «{proposito}» y la "
            f"elegibilidad exige «{PROPOSITO_CARGA}»"
        )
    return lectura


def _motivo_huella(manifiesto, registros):
    """Motivo del incumplimiento de la huella de `C-4`, o ``None`` si rige.

    La huella se calcula sobre las ``opciones`` declaradas del manifiesto
    (`DEC-020`), nunca sobre las efectivas.
    """
    opciones = _requerido(manifiesto, "opciones", "manifiesto")
    huella = perfiles.huella_opciones(opciones)

    for identificador, lectura in registros.items():
        declarada = _clave_lectura(lectura, "huella_opciones")
        if declarada is _AUSENTE:
            raise ValueError(
                f"registro «{identificador}»: falta la clave "
                "«huella_opciones» en el frontmatter y en el nivel superior"
            )
        if declarada == huella:
            return None

    if not registros:
        return (
            "sin medición: 0 registros declaran la huella de las opciones del "
            "manifiesto y C-4 no conserva el estado sin 1 registro medido"
        )
    return MOTIVO_OPCIONES_MODIFICADAS


def _motivo_desviaciones(manifiesto, registros):
    """Motivo de la primera desviación sin comparación completa de `C-7`."""
    desviaciones = manifiesto.get("desviaciones")
    if desviaciones is None:
        return None
    if not isinstance(desviaciones, list):
        raise ValueError(
            "manifiesto: la clave «desviaciones» debe declarar 1 lista"
        )

    for desviacion in desviaciones:
        parametro = _requerido(desviacion, "parametro", "desviación")
        referencia = desviacion.get("comparacion")
        if referencia is None:
            return (
                f"desviación «{parametro}»: no declara comparación y C-4 "
                "exige el bloque completo de C-7"
            )
        if referencia not in registros:
            return (
                f"desviación «{parametro}»: el registro de comparación "
                f"«{referencia}» no existe entre los registros recibidos"
            )
        bloque = _clave_lectura(registros[referencia], "comparacion")
        if bloque is _AUSENTE or not isinstance(bloque, dict):
            return (
                f"desviación «{parametro}»: el registro «{referencia}» no "
                "declara el bloque de comparación de C-7"
            )
        faltantes = [clave for clave in CAMPOS_COMPARACION if clave not in bloque]
        if faltantes:
            return (
                f"desviación «{parametro}»: el bloque de comparación del "
                f"registro «{referencia}» no declara "
                f"{', '.join(faltantes)} de C-7"
            )
    return None


def _motivo_umbral(manifiesto):
    """Motivo del umbral ausente de `RNF-006`, o ``None`` si está declarado."""
    aprobacion = manifiesto.get("aprobacion")
    if not isinstance(aprobacion, dict):
        return (
            "aprobacion: el manifiesto no declara el bloque y RNF-006 exige "
            "«umbral_tg_tokens_por_segundo»"
        )
    umbral = aprobacion.get("umbral_tg_tokens_por_segundo")
    if umbral is None:
        return (
            "aprobacion: falta la clave «umbral_tg_tokens_por_segundo» que "
            "exige RNF-006"
        )
    if isinstance(umbral, bool) or not isinstance(umbral, (int, float)):
        return (
            "aprobacion: «umbral_tg_tokens_por_segundo» declara "
            f"{umbral!r} y RNF-006 exige 1 número en tokens por segundo"
        )
    return None


def _motivo_declaracion(manifiesto):
    """Motivo de la declaración de aprobación incompleta, o ``None`` si rige."""
    aprobacion = manifiesto.get("aprobacion")
    if not isinstance(aprobacion, dict):
        return (
            "aprobacion: falta el bloque y C-4 exige «declarado_por» con "
            "«fecha»"
        )
    declarado_por = aprobacion.get("declarado_por")
    if not isinstance(declarado_por, str) or not declarado_por.strip():
        return (
            "aprobacion: «declarado_por» no declara el nombre de quien aprueba "
            "y C-4 lo exige con fecha"
        )
    fecha = aprobacion.get("fecha")
    if not isinstance(fecha, str) or not fecha.strip():
        return (
            "aprobacion: falta la clave «fecha» de la declaración y C-4 exige "
            f"«declarado_por» con fecha; se leyó {fecha!r}"
        )
    return None


def _motivo_carga(registros, ultima_carga):
    """Motivo del incumplimiento de las filas 19 y 14 de la última carga."""
    lectura = _lectura_carga(registros, ultima_carga)

    desbordamiento = _magnitud_mib(lectura, FILA_DESBORDAMIENTO, ultima_carga)
    if desbordamiento is None:
        return (
            f"la última carga «{ultima_carga}» declara «{NO_DISPONIBLE}» en la "
            "fila 19 (desbordamiento) y RNF-003 exige 0 MiB"
        )
    if desbordamiento != DESBORDAMIENTO_ADMITIDO_MIB:
        return (
            f"la última carga «{ultima_carga}» declara desbordamiento de "
            f"{_texto_fila(lectura, FILA_DESBORDAMIENTO)} y RNF-003 exige "
            f"{DESBORDAMIENTO_ADMITIDO_MIB:g} MiB"
        )

    libre = _magnitud_mib(lectura, FILA_VRAM_LIBRE, ultima_carga)
    if libre is None:
        return (
            f"la última carga «{ultima_carga}» declara «{NO_DISPONIBLE}» en la "
            "fila 14 (VRAM libre) y RNF-007 exige al menos "
            f"{VRAM_LIBRE_MINIMA_MIB:g} MiB"
        )
    if libre < VRAM_LIBRE_MINIMA_MIB:
        return (
            f"la última carga «{ultima_carga}» declara "
            f"{_texto_fila(lectura, FILA_VRAM_LIBRE)} de VRAM libre y RNF-007 "
            f"exige al menos {VRAM_LIBRE_MINIMA_MIB:g} MiB"
        )
    return None


def _texto_fila(lectura, numero):
    """Texto íntegro de la fila `numero` de `C-6` de 1 lectura."""
    filas = lectura.get("filas") if isinstance(lectura, dict) else None
    if not isinstance(filas, list) or len(filas) < numero:
        raise ValueError(
            f"registro: falta la fila {numero} de C-6 entre las "
            f"{len(filas) if isinstance(filas, list) else 0} filas recibidas"
        )
    fila = filas[numero - 1]
    if not isinstance(fila, dict):
        raise ValueError(
            f"registro: la fila {numero} de C-6 no declara numero, campo y valor"
        )
    if "numero" in fila and fila["numero"] != numero:
        raise ValueError(
            f"registro: la fila {numero} de C-6 declara el número "
            f"{fila['numero']!r}"
        )
    if not isinstance(fila.get("valor"), str):
        raise ValueError(
            f"registro: la fila {numero} de C-6 no declara el valor de texto"
        )
    return fila["valor"]


def _magnitud_mib(lectura, numero, identificador):
    """Magnitud en MiB de 1 fila de `C-6`, o ``None`` si es `no disponible`."""
    texto = _texto_fila(lectura, numero)
    if texto == NO_DISPONIBLE:
        return None
    cantidad, separador, unidad = texto.rpartition(" ")
    if separador != " " or unidad != "MiB":
        raise ValueError(
            f"registro «{identificador}»: la fila {numero} de C-6 declara "
            f"{texto!r} y la magnitud no lleva la unidad MiB"
        )
    try:
        return float(cantidad)
    except ValueError as error:
        raise ValueError(
            f"registro «{identificador}»: la fila {numero} de C-6 declara "
            f"{texto!r} y el número de MiB no se puede interpretar"
        ) from error


def _motivo_de_aprobado(manifiesto, registros, ultima_carga):
    """Primer motivo que impide `aprobado` conforme a `C-4`, o ``None``."""
    motivo = _motivo_huella(manifiesto, registros)
    if motivo is not None:
        return motivo
    motivo = _motivo_desviaciones(manifiesto, registros)
    if motivo is not None:
        return motivo
    motivo = _motivo_umbral(manifiesto)
    if motivo is not None:
        return motivo
    motivo = _motivo_declaracion(manifiesto)
    if motivo is not None:
        return motivo
    if ultima_carga is None:
        return (
            "la última carga: 0 registros declaran proposito «carga» y C-4 "
            "exige 1 carga registrada con desbordamiento de 0 MiB y al menos "
            f"{VRAM_LIBRE_MINIMA_MIB:g} MiB de VRAM libre"
        )
    return _motivo_carga(registros, ultima_carga)


def _consulta_git(ruta):
    """Texto de ``git log --format=%G? -1 -- <ruta>`` ejecutado con subprocess."""
    argumentos = ["git", "log", "--format=%G?", "-1", "--", str(ruta)]
    try:
        proceso = subprocess.run(
            argumentos, capture_output=True, text=True, check=False
        )
    except OSError as error:
        raise ValueError(
            f"git: no se pudo consultar la firma de «{ruta}»: {error}"
        ) from error
    if proceso.returncode != 0:
        detalle = (proceso.stderr or "").strip()
        raise ValueError(
            f"git: la consulta de firma de «{ruta}» terminó con código "
            f"{proceso.returncode}: {detalle}"
        )
    return proceso.stdout


def _estado_de_firma(salida):
    """Primer estado de firma de la salida de ``%G?``, sin espacios."""
    if not isinstance(salida, str):
        raise ValueError(
            "ejecutor: se esperaba 1 texto con el estado de firma y se recibió "
            f"{type(salida).__name__}"
        )
    for linea in salida.splitlines():
        if linea.strip():
            return linea.strip()
    return ""
