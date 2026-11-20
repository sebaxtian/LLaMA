#!/usr/bin/env python3
"""Funciones puras del inventario de hallazgos y del veredicto (SPEC-016).

Reciben texto ya leído y devuelven hallazgos. No escriben artefactos, no
consultan Git, no acceden a la red y no crean, mueven ni recrean tags. La
integración en `validate.py` usa estas funciones y conserva su reproducibilidad.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SDD_DIR = ROOT / "docs" / "sdd"
INVENTARIO_PATH = SDD_DIR / "inventario_hallazgos.md"
README_PATH = SDD_DIR / "README.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
REGISTRO_DE_FIRMANTES = SDD_DIR / "firmantes_autorizados"

# C-5 y DEC-001: los cinco informes de origen y el orden de corte del estado.
INFORMES_DE_ORIGEN = (
    "docs/sdd/auditoria_cumplimiento_sdd.md",
    "docs/sdd/auditoria_cierre_v0_7_0.md",
    "docs/sdd/auditoria_final_v0_7_0.md",
    "docs/sdd/auditoria_posterior_v0_7_0.md",
    "docs/sdd/auditoria_final_v0_7_1.md",
)
NOMBRE_DEL_INVENTARIO = "docs/sdd/inventario_hallazgos.md"
IDENTIFICADORES_ESPERADOS = 82

# RF-009 y RF-014: el cierre de los dieciséis hallazgos del corte.
HALLAZGOS_DEL_CIERRE = (
    "AUD-088",
    "AUD-089",
    "AUD-090",
    "AUD-103",
    "AUD-104",
    "AUD-105",
    "AUD-106",
    "AUD-107",
    "AUD-108",
    "AUD-109",
    "AUD-110",
)
EXENCIONES_HISTORICAS = ("AUD-003", "AUD-004", "AUD-005", "AUD-037", "AUD-053")
COMMITS_RATIFICADOS = ("494db2e", "564bac4")

# C-1 y RF-011: los ocho campos obligatorios de una fila del inventario.
CAMPOS_DEL_INVENTARIO = (
    "Identificador",
    "Dimensión",
    "Severidad",
    "Informe de origen",
    "Regla normativa citada",
    "Estado",
    "Evidencia de cierre",
    "Informe que declara el estado",
)
CLAVES_DEL_INVENTARIO = (
    "identificador",
    "dimension",
    "severidad",
    "origen",
    "regla",
    "estado",
    "evidencia",
    "informe_estado",
)

# C-2: vocabulario cerrado del estado.
ESTADO_CERRADO = "cerrado"
ESTADO_PARCIAL = "parcial"
ESTADO_VIGENTE = "vigente"
ESTADO_CERRADO_POR_EXENCION = "cerrado por exención"
ESTADO_CERRADO_POR_RATIFICACION = "cerrado por ratificación"
ESTADOS_CERRADOS = (ESTADO_CERRADO, ESTADO_CERRADO_POR_RATIFICACION)
ESTADOS_ABIERTOS = (ESTADO_PARCIAL, ESTADO_VIGENTE, ESTADO_CERRADO_POR_EXENCION)
ESTADOS = ESTADOS_CERRADOS + ESTADOS_ABIERTOS

# C-1: severidad admitida.
SEVERIDAD_CRITICA = "Crítica"
SEVERIDAD_ALTA = "Alta"
SEVERIDAD_MEDIA = "Media"
SEVERIDAD_BAJA = "Baja"
SEVERIDADES = (SEVERIDAD_CRITICA, SEVERIDAD_ALTA, SEVERIDAD_MEDIA, SEVERIDAD_BAJA)

# C-4 y RF-013: los cuatro veredictos en su orden de precedencia.
NO_CONFORME = "NO CONFORME"
NO_VERIFICABLE = "NO VERIFICABLE"
PARCIAL = "PARCIAL"
CONFORME = "CONFORME"
VEREDICTOS = (NO_CONFORME, NO_VERIFICABLE, PARCIAL, CONFORME)

# RF-010 y CA-010: estados que la nota de cierre admite, incluido `released`.
ESTADOS_POSTERIORES_A_LA_VALIDACION = ("validated", "released")

# C-6 y RF-003: conjunto canónico de los seis artefactos de empaquetado.
ARTEFACTOS_DE_EMPAQUETADO = {
    "A1": "CHANGELOG.md: entrada del release e historial de releases",
    "A2": "specs/INDEX.md: fila de la spec publicada",
    "A3": "spec.md: campos del frontmatter status, version, updated y release",
    "A4": "spec.md: fila del historial de cambios de la versión de release",
    "A5": "spec.md: fila T7 del historial de transiciones",
    "A6": "validation_report.md: línea Release con el tag del release",
}


def _clave(texto: str) -> str:
    """Forma comparable de una celda: sin acentos, sin marcas y en minúsculas."""
    limpio = unicodedata.normalize("NFKD", texto or "")
    limpio = "".join(caracter for caracter in limpio if not unicodedata.combining(caracter))
    limpio = re.sub(r"[`*_]", "", limpio)
    return re.sub(r"\s+", " ", limpio).strip().lower()


_CLAVES_CERRADAS = {_clave(estado) for estado in ESTADOS_CERRADOS}
_CLAVES_ABIERTAS = {_clave(estado) for estado in ESTADOS_ABIERTOS}
_CLAVES_ESTADOS = _CLAVES_CERRADAS | _CLAVES_ABIERTAS
_CLAVES_GRAVES = {_clave(severidad) for severidad in (SEVERIDAD_CRITICA, SEVERIDAD_ALTA)}
_CLAVES_DE_OBSERVACION_GRAVE = _CLAVES_GRAVES | {_clave(SEVERIDAD_MEDIA)}


# ---------------------------------------------------------- C-3 y RF-012
FORMA_DE_CITA_RE = re.compile(
    r"(?P<ruta>[A-Za-z0-9_][A-Za-z0-9_./-]*\.md) §(?P<capitulo>1[0-6]|[1-9]):(?P<linea>\d+)"
)

# C-7 y RF-006: destino del tag en la evidencia de la fila T7.
IDENTIFICADOR_DE_COMMIT_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
ANCESTRIA_RE = re.compile(r"ancestr|ancestro|antecesor", re.IGNORECASE)
MERGE_RE = re.compile(r"\bmerge\b", re.IGNORECASE)
EMPLEO_DEL_EMPAQUETADO_RE = re.compile(
    r"(?:apunta|verificad[oa]|destino|sobre|al|en el)\s+(?:a\s+|al\s+|el\s+)?commit de empaquetado",
    re.IGNORECASE,
)
EVIDENCIA_POR_LINEA_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.md:\d+(?:-\d+)?")

# RF-001 y RF-002: referencia concreta a un informe y salida fijada.
REFERENCIA_A_INFORME_RE = re.compile(
    r"docs/sdd/auditoria_[a-z0-9_]+\.md|auditor[ií]a de cierre|informe de auditor[ií]a de v\d+\.\d+\.\d+",
    re.IGNORECASE,
)
SALIDA_FIJADA_RE = re.compile(
    r"\bNO CONFORME\b|\bNO VERIFICABLE\b|\bPARCIAL\b|\bCONFORME\b|\b\d+ de \d+\s+(?:cerrad|hallazg)"
)
NOTA_DE_AUTORREFERENCIA_RE = re.compile(
    r"^#{2,4}\s+.*autorreferencia", re.IGNORECASE | re.MULTILINE
)

# RF-009 y RF-014: forma de la tabla de cierre y del acta.
HALLAZGO_RE = re.compile(r"^[`*]*?(AUD-\d{3})[`*]*$")
FECHA_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

# RF-010 y CA-010: historial de releases del registro de cambios.
RELEASE_ENCABEZADO_RE = re.compile(r"(?m)^##\s*\[(v\d+\.\d+\.\d+)\]")
HISTORIAL_DE_RELEASES_RE = re.compile(r"(?im)^#{2,4}\s+Historial de releases\s*$")


def _estado_de(fila: dict) -> str:
    """Clave comparable del estado de una fila; rechaza el valor fuera de `C-2`."""
    estado = str(fila.get("estado", ""))
    clave = _clave(estado)
    if clave not in _CLAVES_ESTADOS:
        identificador = fila.get("identificador", "sin identificador")
        raise ValueError(
            f"la fila {identificador} declara el estado «{estado}» fuera del vocabulario de C-2"
        )
    return clave


def _abierta(fila: dict) -> bool:
    return _estado_de(fila) in _CLAVES_ABIERTAS


def cita_valida(celda: str) -> bool:
    """C-3: la celda declara `ruta §capítulo:línea`."""
    return bool(FORMA_DE_CITA_RE.fullmatch(str(celda).strip()))


def _sin_verificacion(fila: dict) -> bool:
    """C-4: fila sin regla citada o sin evidencia de cierre."""
    return not cita_valida(fila.get("regla", "")) or not str(fila.get("evidencia", "")).strip()


def _observaciones_sin_tratamiento(observaciones) -> list[dict]:
    return [
        observacion
        for observacion in observaciones
        if _clave(str(observacion.get("severidad", ""))) in _CLAVES_DE_OBSERVACION_GRAVE
        and not str(observacion.get("tratamiento", "")).strip()
    ]


def veredicto(filas, observaciones=()) -> str:
    """C-4 y RF-013: veredicto calculado desde el inventario con su precedencia."""
    filas = list(filas)
    abiertos = [fila for fila in filas if _abierta(fila)]
    if any(_clave(str(fila.get("severidad", ""))) in _CLAVES_GRAVES for fila in abiertos):
        return NO_CONFORME
    if any(_sin_verificacion(fila) for fila in filas):
        return NO_VERIFICABLE
    if abiertos or _observaciones_sin_tratamiento(observaciones):
        return PARCIAL
    return CONFORME


def _filas_que_sostienen(filas, observaciones) -> list[str]:
    """Filas y observaciones que explican el veredicto calculado (CB-010)."""
    sostienen: list[str] = []
    for fila in filas:
        if _abierta(fila):
            sostienen.append(str(fila.get("identificador", "sin identificador")))
        elif _sin_verificacion(fila):
            sostienen.append(str(fila.get("identificador", "sin identificador")))
    for observacion in _observaciones_sin_tratamiento(observaciones):
        sostienen.append(str(observacion.get("identificador", "sin identificador")))
    return sostienen


def problemas_del_veredicto(declarado: str, filas, observaciones=()) -> list[str]:
    """CB-010: el veredicto declarado que contradice el recuento, con la fila que lo sostiene."""
    calculado = veredicto(filas, observaciones)
    if _clave(str(declarado)) == _clave(calculado):
        return []
    sostienen = _filas_que_sostienen(filas, observaciones)
    detalle = ", ".join(sostienen) if sostienen else "sin fila que lo sostenga"
    return [
        f"el veredicto declarado «{declarado}» contradice el recuento del inventario y el "
        f"cálculo de C-4 devuelve «{calculado}»; lo sostiene {detalle}"
    ]


# --------------------------------------------------- C-1, C-2 y C-5 / RF-011

_CABECERAS_DEL_INVENTARIO = {
    "identificador": "identificador",
    "dimension": "dimension",
    "severidad": "severidad",
    "informe de origen": "origen",
    "regla normativa citada": "regla",
    "estado": "estado",
    "evidencia de cierre": "evidencia",
    "informe que declara el estado": "informe_estado",
}


def _celdas(linea: str) -> list[str]:
    """Celdas de una línea de tabla Markdown."""
    if not linea.strip().startswith("|"):
        return []
    return [celda.strip() for celda in linea.strip().strip("|").split("|")]


def _es_separador(celdas: list[str]) -> bool:
    return bool(celdas) and all(celda and set(celda) <= set("-: ") for celda in celdas)


def _mapa_de_columnas(celdas: list[str]) -> dict[str, int]:
    """Posición de cada campo de `C-1` en la cabecera de la tabla."""
    mapa: dict[str, int] = {}
    for posicion, celda in enumerate(celdas):
        clave = _clave(celda)
        for cabecera, destino in _CABECERAS_DEL_INVENTARIO.items():
            if clave == cabecera or clave.startswith(cabecera):
                mapa.setdefault(destino, posicion)
    return mapa


def _valor(celdas: list[str], posicion: int) -> str:
    if posicion >= len(celdas):
        return ""
    return celdas[posicion].strip().strip("`").strip()


def textos_de_informes() -> dict[str, str]:
    """Texto de cada uno de los cinco informes de origen, por ruta relativa."""
    textos: dict[str, str] = {}
    for ruta in INFORMES_DE_ORIGEN:
        archivo = ROOT / ruta
        textos[ruta] = archivo.read_text(encoding="utf-8") if archivo.exists() else ""
    return textos


def identificadores_de_informes(textos: dict[str, str] | None = None) -> list[str]:
    """C-5: identificadores `AUD-NNN` de los cinco informes, sin duplicado y ascendentes."""
    conjunto = textos if textos is not None else textos_de_informes()
    vistos: set[str] = set()
    for contenido in conjunto.values():
        vistos.update(_identificadores_de_tabla(contenido))
    return sorted(vistos)


def _identificadores_de_tabla(texto: str) -> list[str]:
    """Identificadores que figuran en la primera celda de una fila de tabla."""
    encontrados: list[str] = []
    for linea in texto.splitlines():
        celdas = _celdas(linea)
        if not celdas:
            continue
        coincidencia = HALLAZGO_RE.match(celdas[0])
        if coincidencia:
            encontrados.append(coincidencia.group(1))
    return encontrados


def origen_de_cada_identificador(textos: dict[str, str] | None = None) -> dict[str, str]:
    """Primera ruta de informe que emite cada identificador, en el orden de corte."""
    conjunto = textos if textos is not None else textos_de_informes()
    origen: dict[str, str] = {}
    for ruta, contenido in conjunto.items():
        for identificador in _identificadores_de_tabla(contenido):
            origen.setdefault(identificador, ruta)
    return origen


def filas_del_inventario(texto: str) -> list[dict]:
    """C-1: filas de la tabla de hallazgos con los ocho campos y su línea."""
    lineas = texto.splitlines()
    for indice, linea in enumerate(lineas):
        celdas = _celdas(linea)
        mapa = _mapa_de_columnas(celdas)
        if "identificador" not in mapa:
            continue
        filas: list[dict] = []
        for desplazamiento in range(indice + 1, len(lineas)):
            celdas_fila = _celdas(lineas[desplazamiento])
            if not celdas_fila:
                break
            if _es_separador(celdas_fila):
                continue
            fila = {clave: _valor(celdas_fila, posicion) for clave, posicion in mapa.items()}
            for clave in CLAVES_DEL_INVENTARIO:
                fila.setdefault(clave, "")
            fila["linea"] = desplazamiento + 1
            filas.append(fila)
        return filas
    return []


def problemas_de_corpus(readme: str) -> list[str]:
    """RF-011: la fila del inventario consta en la tabla de inventario del corpus."""
    if f"`{NOMBRE_DEL_INVENTARIO}`" in readme:
        return []
    return [f"docs/sdd/README.md no registra la fila de {NOMBRE_DEL_INVENTARIO}"]


def problemas_de_complecion(texto_inventario: str, textos: dict[str, str] | None = None,
                            readme: str | None = None) -> list[str]:
    """C-5, CB-008 y CB-013: 82 filas para 82 identificadores, con los ocho campos."""
    origen = origen_de_cada_identificador(textos)
    filas = filas_del_inventario(texto_inventario)
    identificadores = [fila["identificador"] for fila in filas]
    problemas: list[str] = []
    if not filas:
        problemas.append(
            f"{NOMBRE_DEL_INVENTARIO}: la tabla de hallazgos no declara filas con los ocho campos"
        )
    for identificador in sorted(origen):
        if identificador not in identificadores:
            problemas.append(
                f"{origen[identificador]}: el hallazgo {identificador} carece de fila en "
                f"{NOMBRE_DEL_INVENTARIO}"
            )
    repetidos = sorted({valor for valor in identificadores if identificadores.count(valor) > 1})
    for identificador in repetidos:
        problemas.append(
            f"{NOMBRE_DEL_INVENTARIO}: el identificador {identificador} figura en más de una fila"
        )
    for fila in filas:
        identificador = fila["identificador"] or "sin identificador"
        if identificador not in origen:
            problemas.append(
                f"{NOMBRE_DEL_INVENTARIO}:{fila['linea']}: la fila {identificador} no corresponde "
                "a un informe de origen de los cinco"
            )
        for campo, clave in zip(CAMPOS_DEL_INVENTARIO, CLAVES_DEL_INVENTARIO):
            if not fila[clave].strip():
                problemas.append(
                    f"{NOMBRE_DEL_INVENTARIO}:{fila['linea']}: la fila {identificador} deja vacío "
                    f"el campo «{campo}»"
                )
        if fila["estado"] and _clave(fila["estado"]) not in _CLAVES_ESTADOS:
            problemas.append(
                f"{NOMBRE_DEL_INVENTARIO}:{fila['linea']}: la fila {identificador} declara el "
                f"estado «{fila['estado']}» fuera del vocabulario de C-2"
            )
    if readme is not None:
        problemas.extend(problemas_de_corpus(readme))
    return problemas


def problemas_de_regla_citada(texto_inventario: str) -> list[str]:
    """C-3, RF-012 y RNF-006: cada hallazgo cita `ruta §capítulo:línea`."""
    problemas: list[str] = []
    for fila in filas_del_inventario(texto_inventario):
        if cita_valida(fila["regla"]):
            continue
        identificador = fila["identificador"] or "sin identificador"
        problemas.append(
            f"{NOMBRE_DEL_INVENTARIO}:{fila['linea']}: el hallazgo {identificador} no cita la "
            f"regla con la forma «ruta §capítulo:línea»: «{fila['regla']}»"
        )
    return problemas


def clasificar_juicios(juicios) -> tuple[list[dict], list[dict]]:
    """RF-012 y CB-009: el juicio con regla citada es hallazgo; sin regla es observación."""
    hallazgos: list[dict] = []
    observaciones: list[dict] = []
    for juicio in juicios:
        destino = hallazgos if cita_valida(juicio.get("regla", "")) else observaciones
        destino.append(juicio)
    return hallazgos, observaciones


# ------------------------------------------- C-6 y RF-003 / conjunto de 6 artefactos

CLAVE_DE_ARTEFACTO_RE = re.compile(r"^`?(A[1-6])`?$")


def claves_declaradas(texto: str) -> list[str]:
    """Claves `A1` a `A6` que la enumeración de empaquetado declara en su primera celda."""
    claves: list[str] = []
    for linea in texto.splitlines():
        celdas = _celdas(linea)
        if not celdas:
            continue
        coincidencia = CLAVE_DE_ARTEFACTO_RE.match(celdas[0])
        if coincidencia:
            claves.append(coincidencia.group(1))
    return claves


def seis_artefactos(texto_rango3: str, texto_rango4: str) -> list[str]:
    """C-6 y CB-003: las dos enumeraciones declaran las mismas 6 claves."""
    declaradas3 = claves_declaradas(texto_rango3)
    declaradas4 = claves_declaradas(texto_rango4)
    problemas: list[str] = []
    for clave, modificacion in ARTEFACTOS_DE_EMPAQUETADO.items():
        if clave not in declaradas3:
            problemas.append(
                f"la enumeración de §15 del rango 3 no declara el artefacto {clave} "
                f"({modificacion})"
            )
        if clave not in declaradas4:
            problemas.append(
                f"la enumeración del paso 3 del rango 4 no declara el artefacto {clave} "
                f"({modificacion})"
            )
    for clave in sorted(set(declaradas3) - set(ARTEFACTOS_DE_EMPAQUETADO)):
        problemas.append(f"la enumeración del rango 3 declara la clave {clave} fuera de las 6")
    for clave in sorted(set(declaradas4) - set(ARTEFACTOS_DE_EMPAQUETADO)):
        problemas.append(f"la enumeración del rango 4 declara la clave {clave} fuera de las 6")
    return problemas


# ------------------------------------------------- C-7 y RF-006 / destino del tag


def fila_t7(texto: str) -> list[str] | None:
    """Celdas de la fila T7 del historial de transiciones."""
    for linea in texto.splitlines():
        celdas = _celdas(linea)
        if len(celdas) >= 6 and _clave(celdas[1]) == "t7":
            return celdas
    return None


def release_del_frontmatter(texto: str) -> str:
    """Valor del campo `release` del frontmatter."""
    coincidencia = re.search(r"(?m)^release:\s*(.*)$", texto)
    return coincidencia.group(1).strip().strip('"').strip() if coincidencia else ""


def destino_del_tag(texto_espec: str) -> list[str]:
    """C-7 y RF-006: la evidencia de la fila T7 declara el commit de merge en `main`."""
    celdas = fila_t7(texto_espec)
    if celdas is None:
        return ["la spec no declara la fila T7 del historial de transiciones"]
    destino = celdas[3]
    evidencia = celdas[-1]
    problemas: list[str] = []
    if _clave(destino) != "released":
        problemas.append(
            f"la fila T7 declara el destino «{destino}» y el contrato exige «released»"
        )
    if EMPLEO_DEL_EMPAQUETADO_RE.search(evidencia):
        problemas.append(
            "la fila T7 declara el commit de empaquetado como destino del tag; el tag anotado "
            "apunta al commit de merge publicado en `main`"
        )
    if not IDENTIFICADOR_DE_COMMIT_RE.search(evidencia):
        problemas.append(
            "la evidencia de la fila T7 no declara el identificador del commit de merge de 7 a 40 "
            "caracteres hexadecimales"
        )
    if not re.search(r"\bmain\b", evidencia):
        problemas.append("la evidencia de la fila T7 no declara `main` como rama del commit de merge")
    if not MERGE_RE.search(evidencia):
        problemas.append("la evidencia de la fila T7 no declara la palabra `merge`")
    if not ANCESTRIA_RE.search(evidencia):
        problemas.append("la evidencia de la fila T7 no declara la ancestría con el commit de empaquetado")
    release = release_del_frontmatter(texto_espec)
    if not release:
        problemas.append("la spec no conserva el campo `release` del frontmatter")
    elif release not in evidencia:
        problemas.append(f"la evidencia de la fila T7 no declara el release `{release}`")
    return problemas


def alteracion_del_destino(texto_antes: str, texto_despues: str) -> list[str]:
    """CB-004: la corrección no altera el destino `released`, el campo `release` ni el identificador."""
    problemas: list[str] = []
    release_antes = release_del_frontmatter(texto_antes)
    release_despues = release_del_frontmatter(texto_despues)
    if release_antes != release_despues:
        problemas.append(
            f"la corrección altera el campo `release` del frontmatter: «{release_antes}» frente a "
            f"«{release_despues}»"
        )
    celdas_antes = fila_t7(texto_antes)
    celdas_despues = fila_t7(texto_despues)
    if celdas_antes and celdas_despues:
        if _clave(celdas_antes[3]) != _clave(celdas_despues[3]):
            problemas.append(
                f"la corrección altera el destino de la fila T7: «{celdas_antes[3]}» frente a "
                f"«{celdas_despues[3]}»"
            )
        identificador_antes = re.search(r"v\d+\.\d+\.\d+", celdas_antes[-1])
        identificador_despues = re.search(r"v\d+\.\d+\.\d+", celdas_despues[-1])
        if (identificador_antes.group(0) if identificador_antes else "") != (
                identificador_despues.group(0) if identificador_despues else ""):
            problemas.append(
                "la corrección altera el identificador del release en la evidencia de la fila T7"
            )
    return problemas


# ------------------------------------------- RF-001 y RF-002 / autorreferencia

BLOQUES_DEL_CONTRATO_RE = r"(?m)^###\s+((?:RF|RNF|CB|CA)-\d{3})\s*$"
BLOQUES_DE_TAREAS_RE = r"(?m)^###\s+(T-\d{3})\s*$"


def _bloques(texto: str, patron: str) -> list[tuple[str, str]]:
    """Bloques delimitados por los encabezados que el patrón reconoce."""
    marcas = list(re.finditer(patron, texto))
    bloques: list[tuple[str, str]] = []
    for posicion, marca in enumerate(marcas):
        inicio = marca.end()
        fin = marcas[posicion + 1].start() if posicion + 1 < len(marcas) else len(texto)
        bloques.append((marca.group(1), texto[inicio:fin]))
    return bloques


def nota_de_autorreferencia(texto_reporte: str) -> bool:
    """RF-002: el reporte porta la nota que habilita la referencia a un informe concreto."""
    if not NOTA_DE_AUTORREFERENCIA_RE.search(texto_reporte):
        return False
    return bool(re.search(r"\bRF-001\b", texto_reporte)) and bool(
        re.search(r"rol de auditor[ií]a", texto_reporte, re.IGNORECASE)
    )


def autorreferencia(texto_contrato: str, texto_reporte: str = "",
                    texto_tareas: str = "") -> list[str]:
    """RF-001, CB-006 y RNF-001: una spec no fija la salida de un informe posterior."""
    admitida = nota_de_autorreferencia(texto_reporte)
    problemas: list[str] = []
    bloques = _bloques(texto_contrato, BLOQUES_DEL_CONTRATO_RE)
    bloques += _bloques(texto_tareas, BLOQUES_DE_TAREAS_RE)
    for identificador, bloque in bloques:
        if not REFERENCIA_A_INFORME_RE.search(bloque):
            continue
        if not SALIDA_FIJADA_RE.search(bloque):
            continue
        if admitida:
            continue
        problemas.append(
            f"{identificador} fija el veredicto, el recuento o las dimensiones de un informe de "
            "auditoría posterior a la aprobación de la spec; la referencia solo se admite como "
            "evidencia y la nota de autorreferencia del reporte no consta"
        )
    return problemas


# ------------------------------------------ RF-009 y RF-014 / cierre de los dieciséis

_CABECERAS_DEL_CIERRE = {
    "hallazgo": "identificador",
    "identificador": "identificador",
    "observacion": "identificador",
    "artefacto": "artefacto",
    "evidencia": "evidencia",
    "estado": "estado",
}


def _mapa_del_cierre(celdas: list[str]) -> dict[str, int]:
    mapa: dict[str, int] = {}
    for posicion, celda in enumerate(celdas):
        clave = _clave(celda)
        for cabecera, destino in _CABECERAS_DEL_CIERRE.items():
            if clave == cabecera or clave.startswith(cabecera):
                mapa.setdefault(destino, posicion)
    return mapa


def filas_del_cierre(texto: str) -> list[dict]:
    """Filas de la tabla de cierre: hallazgo, artefacto, evidencia y estado."""
    lineas = texto.splitlines()
    for indice, linea in enumerate(lineas):
        celdas = _celdas(linea)
        mapa = _mapa_del_cierre(celdas)
        if "identificador" not in mapa or "artefacto" not in mapa:
            continue
        filas: list[dict] = []
        for desplazamiento in range(indice + 1, len(lineas)):
            celdas_fila = _celdas(lineas[desplazamiento])
            if not celdas_fila:
                break
            if _es_separador(celdas_fila):
                continue
            coincidencia = HALLAZGO_RE.match(celdas_fila[0].strip())
            if not coincidencia:
                continue
            filas.append({
                "identificador": coincidencia.group(1),
                "artefacto": _valor(celdas_fila, mapa["artefacto"]),
                "evidencia": _valor(celdas_fila, mapa.get("evidencia", 0))
                if "evidencia" in mapa else "",
                "estado": _valor(celdas_fila, mapa.get("estado", 0)) if "estado" in mapa else "",
                "linea": desplazamiento + 1,
            })
        return filas
    return []


def cierre_de_los_dieciseis(texto: str) -> list[str]:
    """RF-009, RF-014 y CB-001: 11 cierres por artefacto y 5 por ratificación firmada."""
    filas = filas_del_cierre(texto)
    por_identificador = {fila["identificador"]: fila for fila in filas}
    problemas: list[str] = []
    for identificador in HALLAZGOS_DEL_CIERRE + EXENCIONES_HISTORICAS:
        if identificador not in por_identificador:
            problemas.append(f"la tabla de cierre no declara la fila de {identificador}")
    for identificador in HALLAZGOS_DEL_CIERRE:
        fila = por_identificador.get(identificador)
        if fila is None:
            continue
        con_evidencia = bool(fila["artefacto"]) and bool(
            EVIDENCIA_POR_LINEA_RE.search(fila["evidencia"])
        )
        if con_evidencia:
            if _clave(fila["estado"]) != _clave(ESTADO_CERRADO):
                problemas.append(
                    f"{identificador}: el artefacto cierra la observación y el estado declarado es "
                    f"«{fila['estado']}» en lugar de «{ESTADO_CERRADO}»"
                )
        elif _clave(fila["estado"]) == _clave(ESTADO_CERRADO):
            problemas.append(
                f"{identificador}: la observación carece de artefacto o de evidencia por ruta y "
                "línea, de modo que queda vigente y no se declara cerrada"
            )
    for identificador in EXENCIONES_HISTORICAS:
        fila = por_identificador.get(identificador)
        if fila is None:
            continue
        if _clave(fila["estado"]) != _clave(ESTADO_CERRADO_POR_RATIFICACION):
            problemas.append(
                f"{identificador}: la violación histórica exige el estado "
                f"«{ESTADO_CERRADO_POR_RATIFICACION}» y declara «{fila['estado']}»"
            )
        if not IDENTIFICADOR_DE_COMMIT_RE.search(fila["evidencia"]):
            problemas.append(
                f"{identificador}: la ratificación no declara el identificador del commit firmado "
                "por una clave de docs/sdd/firmantes_autorizados"
            )
    return problemas


def problemas_del_acta(texto_acta: str) -> list[str]:
    """C-9 y CB-011: el acta declara fecha, alcance, rutas y efecto retroactivo limitado."""
    problemas: list[str] = []
    if not FECHA_ISO_RE.search(texto_acta) or "UTC" not in texto_acta:
        problemas.append("el acta no declara la fecha UTC de la ratificación")
    for identificador in EXENCIONES_HISTORICAS:
        if identificador not in texto_acta:
            problemas.append(f"el acta no declara la exención {identificador} en su alcance")
    for commit in COMMITS_RATIFICADOS:
        if commit not in texto_acta:
            problemas.append(f"el acta no declara el commit ratificado {commit}")
    rutas = set(re.findall(r"`([^`]+\.md)`", texto_acta))
    if len(rutas) < 3:
        problemas.append(
            f"el acta declara {len(rutas)} rutas publicadas y el alcance exige las rutas afectadas"
        )
    if not re.search(r"retroactiv", texto_acta, re.IGNORECASE):
        problemas.append("el acta no declara el efecto retroactivo de la ratificación")
    elif not re.search(r"r[eé]gimen", texto_acta, re.IGNORECASE) or not re.search(
            r"limitad|no alcanza", texto_acta, re.IGNORECASE):
        problemas.append("el acta no limita el efecto retroactivo al régimen")
    if "docs/sdd/firmantes_autorizados" not in texto_acta:
        problemas.append("el acta no referencia la lista de docs/sdd/firmantes_autorizados")
    return problemas


def ratificacion_admitida(estado_de_firma: str, huella: str, autorizadas,
                          texto_acta: str = "") -> list[str]:
    """C-9, CB-002 y RNF-008: la firma verificable y la clave autorizada habilitan el acta."""
    problemas: list[str] = []
    if str(estado_de_firma).strip() != "G":
        problemas.append(
            f"el commit del acta declara el estado de firma «{estado_de_firma}» y el contrato "
            "exige una firma verificable «G»"
        )
    if huella not in set(autorizadas):
        problemas.append(
            f"la huella de la clave firmante {huella} no figura en "
            "docs/sdd/firmantes_autorizados"
        )
    if texto_acta:
        problemas.extend(problemas_del_acta(texto_acta))
    return problemas


# ------------------------------------- RF-010 y CA-010 / historial de releases

VERSION_RE = re.compile(r"`?(v\d+\.\d+\.\d+)`?")


def _version(valor: str) -> tuple[int, int, int]:
    coincidencia = VERSION_RE.search(valor)
    if not coincidencia:
        return (0, 0, 0)
    return tuple(int(parte) for parte in coincidencia.group(1).lstrip("v").split("."))  # type: ignore[return-value]


def releases_publicados(changelog: str) -> list[str]:
    """Tags de los releases que declaran encabezado en el registro de cambios."""
    return RELEASE_ENCABEZADO_RE.findall(changelog)


def seccion_del_historial(changelog: str) -> str:
    """Texto de la sección «Historial de releases»."""
    coincidencia = HISTORIAL_DE_RELEASES_RE.search(changelog)
    if not coincidencia:
        return ""
    resto = changelog[coincidencia.end():]
    siguiente = re.search(r"(?m)^#{1,4}\s+", resto)
    return resto[: siguiente.start()] if siguiente else resto


def filas_del_historial_de_releases(changelog: str) -> list[list[str]]:
    """Filas de versión, fecha y tag de la sección «Historial de releases»."""
    filas: list[list[str]] = []
    for linea in seccion_del_historial(changelog).splitlines():
        celdas = _celdas(linea)
        if len(celdas) < 3 or not VERSION_RE.fullmatch(celdas[0]):
            continue
        filas.append([celda.strip().strip("`") for celda in celdas])
    return filas


def problemas_de_historial_de_releases(changelog: str) -> list[str]:
    """RF-010: una fila por release publicado, en orden ascendente y con su fecha y su tag.

    La comprobación regularizada admite las filas que el empaquetado escribe: exige la fila de
    cada release publicado y no equipara el número de filas con el número de encabezados.
    """
    publicados = releases_publicados(changelog)
    if not publicados:
        return ["el registro de cambios no declara releases publicados"]
    filas = filas_del_historial_de_releases(changelog)
    if not filas:
        return ["el registro de cambios no declara la sección «Historial de releases»"]
    declarados = [fila[0] for fila in filas]
    problemas: list[str] = []
    if declarados != sorted(declarados, key=_version):
        problemas.append(f"el historial no está en orden ascendente: {declarados}")
    for version in publicados:
        if declarados.count(version) == 0:
            problemas.append(f"el historial no registra el release {version}")
        elif declarados.count(version) > 1:
            problemas.append(f"el historial declara más de una fila para el release {version}")
    for fila in filas:
        if not FECHA_ISO_RE.fullmatch(fila[1]):
            problemas.append(f"la fila de {fila[0]} no declara la fecha ISO")
        if fila[0] != fila[2].strip().strip("`"):
            problemas.append(f"la fila de {fila[0]} no declara el tag")
    return problemas
