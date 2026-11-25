"""Carga, orden y admisibilidad del catálogo de escenarios de SPEC-018.

Implementa `RF-004`, `RF-005`, `RF-011`, `CB-004` y `CB-006` conforme a `C-3`
del plan, con las decisiones `DEC-002` (9 identificadores canónicos
invariables), `DEC-004` (orden jerárquico determinista) y `DEC-005` (presupuesto
desglosado en 4 componentes).

Contrato:

- ``cargar_catalogo(ruta_catalogo=None)`` lee el manifiesto canónico
  ``src/gemma/escenarios/catalogo.json``, valida su estructura y devuelve el
  objeto raíz. Falla con ``ValueError`` nombrando el archivo ante un manifiesto
  ausente, ilegible o con JSON inválido, ante 1 clave obligatoria ausente, ante
  1 campo con tipo incoherente y ante el par (capas de expertos en CPU,
  contexto efectivo) repetido, cuyo error identifica los identificadores
  implicados (`CB-004`). El bloque ``aprobacion`` se acepta nulo o ausente y,
  cuando consta, exige las 6 claves de `C-1` con sus tipos y valores válidos,
  de modo que el rechazo nombra la clave que falta o no es válida (`RF-011`,
  `DEC-012`).
- ``listar_escenarios(catalogo)`` devuelve los escenarios ordenados por capas
  de expertos en CPU ascendente y, dentro de cada valor, por contexto efectivo
  ascendente (`DEC-004`), con independencia del orden de declaración del JSON.
  Cada entrada declara ``id``, ``estado``, ``capas_cpu_moe``, ``contexto`` y
  ``presupuesto_vram`` (`RF-005`).
- ``resolver_contexto_ajustado(escenario, vram_libre_mib,
  consumo_kv_por_1024_mib=85.0)`` deriva el contexto efectivo en múltiplos de
  1024 tokens a partir de la VRAM libre real, acotado por el valor nominal
  declarado y sin aplicar suelo: devuelve el valor calculado, incluso si no
  supera 4096 tokens, para que la validación lo rechace (`RF-009`, `DEC-008`).
- ``validar_contexto_ajustado(escenario, tokens_resueltos)`` devuelve
  ``(True, "")`` por encima de 4096 tokens y ``(False, motivo)`` cuando el
  valor resuelto es menor o igual, con el valor y el identificador en el
  motivo (`CB-003`).
- ``validar_admisibilidad_escenario(escenario)`` devuelve ``(True, "")`` para
  los estados ``declarado`` y ``medido`` y ``(False, motivo)`` para
  ``no_ejecutable``, para ``aprobado`` sin aprobación registrada, al que se le
  exige 1 medición nueva, para el contexto ajustado sin valor numérico
  resuelto (`RF-011`, `RF-010`, `CB-006`) y para ``aprobado`` cuyos 4 valores
  conservados difieren de los declarados; en ese último caso el motivo nombra
  la clave y ambos valores y exige 1 medición nueva (`DEC-012`, `CA-008`).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RUTA_CATALOGO = RAIZ / "src" / "gemma" / "escenarios" / "catalogo.json"

# `C-1` y `RF-002`: los 4 estados admitidos por escenario.
ESTADOS = ("declarado", "medido", "aprobado", "no_ejecutable")
ESTADOS_EJECUTABLES = ("declarado", "medido")
ESTADO_NO_EJECUTABLE = "no_ejecutable"
ESTADO_APROBADO = "aprobado"

# `C-1` y `DEC-005`: los 4 componentes del presupuesto de VRAM.
COMPONENTES_VRAM = ("pesos_mib", "cache_kv_mib", "computo_mib", "reserva_mib")

# `C-1` y `RF-005`: los 5 campos que declara la enumeración.
CAMPOS_LISTADO = (
    "id",
    "estado",
    "capas_cpu_moe",
    "contexto",
    "presupuesto_vram",
)

# `C-1`, `RF-011` y `DEC-012`: las 6 claves obligatorias del bloque
# `aprobacion` y los 4 valores que la admisibilidad compara con los declarados.
CLAVES_APROBACION = (
    "capas_cpu_moe",
    "contexto_efectivo_tokens",
    "parametros_ejecucion",
    "presupuesto_vram_total_mib",
    "medicion",
    "confirmacion_propietario",
)

MOTIVO_NO_EJECUTABLE = (
    "escenario no ejecutable: la combinación declarada no alcanza el estado de "
    "servicio en la GPU objetivo"
)
MOTIVO_APROBACION_AUSENTE = (
    "escenario aprobado sin aprobación registrada: exige 1 medición nueva y la "
    "confirmación escrita del propietario"
)

# `C-1` y `RF-009`: tipo de contexto que se deriva de la VRAM libre real.
TIPO_CONTEXTO_AJUSTADO = "ajustado"

# `DEC-008`, `AMB-001` y `CB-003`: granularidad de la derivación, consumo de
# caché KV por bloque de 1024 tokens y suelo mínimo del contexto resuelto.
MULTIPLO_CONTEXTO_TOKENS = 1024
CONSUMO_KV_POR_1024_MIB = 85.0
SUELO_CONTEXTO_RESUELTO_TOKENS = 4096

MOTIVO_CONTEXTO_NO_RESUELTO = (
    "contexto ajustado sin valor numérico resuelto: exige 1 valor efectivo "
    "medido o derivado antes de la selección"
)


def _requerido(contenedor, clave, contexto):
    """Devuelve ``contenedor[clave]`` o falla nombrando la clave ausente."""
    if not isinstance(contenedor, dict) or clave not in contenedor:
        raise ValueError(f"{contexto}: falta la clave obligatoria «{clave}»")
    return contenedor[clave]


def _objeto(valor, campo):
    """Comprueba que 1 campo declara 1 objeto y lo devuelve."""
    if not isinstance(valor, dict):
        raise ValueError(f"{campo}: se esperaba 1 objeto y declara {valor!r}")
    return valor


def _entero(valor, campo):
    """Comprueba que 1 campo declara 1 entero —nunca 1 booleano— y lo devuelve."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"{campo}: se esperaba 1 entero y declara {valor!r}")
    return valor


def _numero(valor, campo):
    """Comprueba que 1 campo declara 1 número —nunca 1 booleano— y lo devuelve."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo}: se esperaba 1 número y declara {valor!r}")
    return valor


def _texto(valor, campo):
    """Comprueba que 1 campo declara 1 texto no vacío y lo devuelve."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(
            f"{campo}: se esperaba 1 texto no vacío y declara {valor!r}"
        )
    return valor


def _leer_json(ruta):
    """Lee 1 manifiesto UTF-8 y devuelve su raíz, nombrando el archivo al fallar."""
    try:
        texto = ruta.read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError(
            f"{ruta}: no se pudo leer el catálogo de escenarios: {error}"
        ) from error
    except UnicodeDecodeError as error:
        raise ValueError(
            f"{ruta}: el catálogo de escenarios no es UTF-8 válido: {error}"
        ) from error
    try:
        return json.loads(texto)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{ruta}: el catálogo de escenarios no declara JSON válido: {error}"
        ) from error


def _validar_contexto(contexto, contexto_error):
    """Valida el bloque ``contexto`` de `C-1` y devuelve sus tokens efectivos."""
    _objeto(contexto, f"{contexto_error}.contexto")
    tipo = _requerido(contexto, "tipo", f"{contexto_error}.contexto")
    if tipo not in ("fijo", "ajustado"):
        raise ValueError(
            f"{contexto_error}.contexto.tipo: declara {tipo!r} y no «fijo» ni "
            "«ajustado»"
        )
    declarado = _entero(
        _requerido(contexto, "declarado_tokens", f"{contexto_error}.contexto"),
        f"{contexto_error}.contexto.declarado_tokens",
    )
    efectivo = _entero(
        _requerido(contexto, "efectivo_tokens", f"{contexto_error}.contexto"),
        f"{contexto_error}.contexto.efectivo_tokens",
    )
    if declarado <= 0 or efectivo <= 0:
        raise ValueError(
            f"{contexto_error}.contexto: declara {declarado} tokens declarados y "
            f"{efectivo} efectivos"
        )
    return efectivo


def _validar_presupuesto(presupuesto, contexto_error):
    """Valida el desglose de `C-1` y `DEC-005` de 1 presupuesto de VRAM."""
    _objeto(presupuesto, f"{contexto_error}.presupuesto_vram")
    total = _entero(
        _requerido(presupuesto, "total_mib", f"{contexto_error}.presupuesto_vram"),
        f"{contexto_error}.presupuesto_vram.total_mib",
    )
    if total <= 0:
        raise ValueError(
            f"{contexto_error}.presupuesto_vram.total_mib: declara {total} MiB"
        )
    desglose = _objeto(
        _requerido(
            presupuesto, "desglose", f"{contexto_error}.presupuesto_vram"
        ),
        f"{contexto_error}.presupuesto_vram.desglose",
    )
    suma = 0
    for componente in COMPONENTES_VRAM:
        valor = _entero(
            _requerido(
                desglose,
                componente,
                f"{contexto_error}.presupuesto_vram.desglose",
            ),
            f"{contexto_error}.presupuesto_vram.desglose.{componente}",
        )
        if valor < 0:
            raise ValueError(
                f"{contexto_error}.presupuesto_vram.desglose.{componente}: "
                f"declara {valor} MiB"
            )
        suma += valor
    if suma != total:
        raise ValueError(
            f"{contexto_error}.presupuesto_vram: el total {total} MiB no coincide "
            f"con la suma {suma} MiB de los 4 componentes"
        )


def _validar_aprobacion(escenario, contexto_error):
    """Valida el bloque ``aprobacion`` de `C-1` y `DEC-012` cuando consta.

    El bloque nulo o ausente es válido: solo los escenarios con aprobación
    registrada declaran el objeto con las 6 claves obligatorias. 1 clave
    ausente o 1 valor con tipo o rango inválido aborta con ``ValueError`` que
    nombra la clave.
    """
    if "aprobacion" not in escenario:
        return
    bloque = escenario["aprobacion"]
    if bloque is None:
        return
    ruta = f"{contexto_error}.aprobacion"
    _objeto(bloque, ruta)
    for clave in CLAVES_APROBACION:
        _requerido(bloque, clave, ruta)
    capas = _entero(bloque["capas_cpu_moe"], f"{ruta}.capas_cpu_moe")
    if capas < 0:
        raise ValueError(f"{ruta}.capas_cpu_moe: declara {capas} capas")
    efectivo = _entero(
        bloque["contexto_efectivo_tokens"], f"{ruta}.contexto_efectivo_tokens"
    )
    if efectivo <= 0:
        raise ValueError(
            f"{ruta}.contexto_efectivo_tokens: declara {efectivo} tokens"
        )
    parametros = _objeto(
        bloque["parametros_ejecucion"], f"{ruta}.parametros_ejecucion"
    )
    if not parametros:
        raise ValueError(
            f"{ruta}.parametros_ejecucion: no declara parámetro alguno"
        )
    total = _entero(
        bloque["presupuesto_vram_total_mib"],
        f"{ruta}.presupuesto_vram_total_mib",
    )
    if total <= 0:
        raise ValueError(
            f"{ruta}.presupuesto_vram_total_mib: declara {total} MiB"
        )
    _texto(bloque["medicion"], f"{ruta}.medicion")
    _texto(
        bloque["confirmacion_propietario"],
        f"{ruta}.confirmacion_propietario",
    )


def _validar_escenario(identificador, escenario):
    """Valida 1 escenario de `C-1` y devuelve el par (capas, contexto) de `CB-004`."""
    contexto_error = f"escenario «{identificador}»"
    _objeto(escenario, contexto_error)
    declarado = _requerido(escenario, "id", contexto_error)
    if declarado != identificador:
        raise ValueError(
            f"{contexto_error}: declara el campo id {declarado!r} y no "
            f"{identificador!r}"
        )
    estado = _requerido(escenario, "estado", contexto_error)
    if estado not in ESTADOS:
        raise ValueError(
            f"{contexto_error}.estado: declara {estado!r} y no 1 de "
            f"{', '.join(ESTADOS)}"
        )
    capas = _entero(
        _requerido(escenario, "capas_cpu_moe", contexto_error),
        f"{contexto_error}.capas_cpu_moe",
    )
    if capas < 0:
        raise ValueError(f"{contexto_error}.capas_cpu_moe: declara {capas} capas")
    efectivo = _validar_contexto(
        _requerido(escenario, "contexto", contexto_error), contexto_error
    )
    _validar_presupuesto(
        _requerido(escenario, "presupuesto_vram", contexto_error), contexto_error
    )
    ram = _entero(
        _requerido(escenario, "ram_sistema_requerida_mib", contexto_error),
        f"{contexto_error}.ram_sistema_requerida_mib",
    )
    if ram < 0:
        raise ValueError(
            f"{contexto_error}.ram_sistema_requerida_mib: declara {ram} MiB"
        )
    parametros = _objeto(
        _requerido(escenario, "parametros_ejecucion", contexto_error),
        f"{contexto_error}.parametros_ejecucion",
    )
    if not parametros:
        raise ValueError(
            f"{contexto_error}.parametros_ejecucion: no declara parámetro alguno"
        )
    _validar_aprobacion(escenario, contexto_error)
    return (capas, efectivo)


def cargar_catalogo(ruta_catalogo=None):
    """Carga y valida el catálogo de escenarios de `C-3` y `CB-004`."""
    ruta = RUTA_CATALOGO if ruta_catalogo is None else Path(ruta_catalogo)
    datos = _leer_json(ruta)
    _objeto(datos, f"{ruta}: la raíz del catálogo")
    for clave in ("version", "modelo", "escenarios"):
        _requerido(datos, clave, f"{ruta}: la raíz del catálogo")
    escenarios = _objeto(
        datos["escenarios"], f"{ruta}: la clave «escenarios»"
    )
    if not escenarios:
        raise ValueError(f"{ruta}: el catálogo no declara escenario alguno")

    pares = {}
    for identificador, escenario in escenarios.items():
        par = _validar_escenario(identificador, escenario)
        anterior = pares.get(par)
        if anterior is not None:
            raise ValueError(
                f"{ruta}: los escenarios «{anterior}» y «{identificador}» declaran "
                f"el mismo par de capas de expertos en CPU y contexto {par}"
            )
        pares[par] = identificador
    return datos


def _clave_orden(escenario):
    """Clave jerárquica de `DEC-004`: capas ascendente y contexto efectivo ascendente."""
    return (
        escenario["capas_cpu_moe"],
        escenario["contexto"]["efectivo_tokens"],
        escenario["id"],
    )


def listar_escenarios(catalogo):
    """Enumera los escenarios con el orden determinista jerárquico de `DEC-004`."""
    escenarios = _objeto(
        _requerido(catalogo, "escenarios", "catálogo"),
        "catálogo: la clave «escenarios»",
    )
    listado = []
    for identificador, escenario in escenarios.items():
        contexto_error = f"escenario «{identificador}»"
        _objeto(escenario, contexto_error)
        for campo in CAMPOS_LISTADO:
            _requerido(escenario, campo, contexto_error)
        listado.append(
            {campo: escenario[campo] for campo in CAMPOS_LISTADO}
        )
    return sorted(listado, key=_clave_orden)


def resolver_contexto_ajustado(
    escenario,
    vram_libre_mib,
    consumo_kv_por_1024_mib=CONSUMO_KV_POR_1024_MIB,
):
    """Deriva el contexto efectivo de `RF-009` y `DEC-008` en múltiplos de 1024.

    La VRAM disponible para la caché KV es la VRAM libre menos la parte del
    presupuesto declarado que no corresponde a la caché —pesos, cómputo y
    reserva—; el número de bloques de 1024 tokens es el cociente entero entre
    esa VRAM y el consumo por bloque. El resultado nunca supera el valor
    nominal declarado ni es negativo y no aplica suelo: si no supera
    4096 tokens, devuelve el valor calculado para que la validación lo rechace
    (`CB-003`).
    """
    contexto_error = "escenario"
    _objeto(escenario, contexto_error)
    libre = _numero(vram_libre_mib, "vram_libre_mib")
    consumo = _numero(consumo_kv_por_1024_mib, "consumo_kv_por_1024_mib")
    if consumo <= 0:
        raise ValueError(
            "consumo_kv_por_1024_mib: declara "
            f"{consumo_kv_por_1024_mib!r} y no 1 consumo positivo"
        )
    contexto = _objeto(
        _requerido(escenario, "contexto", contexto_error),
        f"{contexto_error}.contexto",
    )
    base = _entero(
        _requerido(contexto, "declarado_tokens", f"{contexto_error}.contexto"),
        f"{contexto_error}.contexto.declarado_tokens",
    )
    presupuesto = _objeto(
        _requerido(escenario, "presupuesto_vram", contexto_error),
        f"{contexto_error}.presupuesto_vram",
    )
    total = _entero(
        _requerido(presupuesto, "total_mib", f"{contexto_error}.presupuesto_vram"),
        f"{contexto_error}.presupuesto_vram.total_mib",
    )
    desglose = _objeto(
        _requerido(
            presupuesto, "desglose", f"{contexto_error}.presupuesto_vram"
        ),
        f"{contexto_error}.presupuesto_vram.desglose",
    )
    cache_kv = _entero(
        _requerido(
            desglose, "cache_kv_mib", f"{contexto_error}.presupuesto_vram.desglose"
        ),
        f"{contexto_error}.presupuesto_vram.desglose.cache_kv_mib",
    )
    vram_kv = libre - (total - cache_kv)
    bloques = math.floor(vram_kv / consumo)
    derivado = max(bloques, 0) * MULTIPLO_CONTEXTO_TOKENS
    return min(base, derivado)


def validar_contexto_ajustado(escenario, tokens_resueltos):
    """Veredicto de `CB-003` sobre el contexto resuelto, como ``(admisible, motivo)``."""
    _objeto(escenario, "escenario")
    tokens = _entero(tokens_resueltos, "tokens_resueltos")
    if tokens > SUELO_CONTEXTO_RESUELTO_TOKENS:
        return (True, "")
    identificador = escenario.get("id")
    referencia = (
        f"escenario «{identificador}»"
        if isinstance(identificador, str) and identificador
        else "escenario sin identificador"
    )
    return (
        False,
        f"{referencia}: el contexto ajustado resuelto de {tokens} tokens no "
        f"supera el suelo de {SUELO_CONTEXTO_RESUELTO_TOKENS} tokens (`CB-003`)",
    )


def _falta_contexto_resuelto(escenario):
    """Indica si 1 escenario ajustado carece de valor de contexto numérico (`RF-010`)."""
    contexto = escenario.get("contexto")
    if not isinstance(contexto, dict):
        return False
    if contexto.get("tipo") != TIPO_CONTEXTO_AJUSTADO:
        return False
    for campo in ("declarado_tokens", "efectivo_tokens"):
        valor = contexto.get(campo)
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            return True
    return False


def _valor_anidado(contenedor, *ruta):
    """Devuelve el valor de 1 ruta anidada o ``None`` si la ruta no existe."""
    actual = contenedor
    for clave in ruta:
        if not isinstance(actual, dict) or clave not in actual:
            return None
        actual = actual[clave]
    return actual


def _diferencia_parametros(declarados, conservados):
    """Devuelve la primera diferencia de ``parametros_ejecucion`` como tupla.

    La tupla declara la clave interna que difiere —con el prefijo
    ``parametros_ejecucion``—, el valor declarado y el valor conservado; si los
    2 objetos coinciden devuelve ``None`` (`DEC-012`).
    """
    if not isinstance(declarados, dict) or not isinstance(conservados, dict):
        return ("parametros_ejecucion", declarados, conservados)
    for clave, conservado in conservados.items():
        if clave not in declarados or declarados[clave] != conservado:
            return (
                f"parametros_ejecucion.{clave}",
                declarados.get(clave),
                conservado,
            )
    for clave, declarado in declarados.items():
        if clave not in conservados:
            return (f"parametros_ejecucion.{clave}", declarado, None)
    return None


def _diferencia_aprobacion(escenario, bloque):
    """Devuelve la primera diferencia de `DEC-012` como ``(clave, declarado, conservado)``.

    Compara los 4 valores conservados por la aprobación con los declarados por
    el escenario, en el orden de `C-1`: capas de expertos en CPU, contexto
    efectivo en tokens, parámetros de ejecución y presupuesto de VRAM en MiB.
    """
    conservado = bloque.get("capas_cpu_moe")
    if escenario.get("capas_cpu_moe") != conservado:
        return ("capas_cpu_moe", escenario.get("capas_cpu_moe"), conservado)
    conservado = bloque.get("contexto_efectivo_tokens")
    declarado = _valor_anidado(escenario, "contexto", "efectivo_tokens")
    if declarado != conservado:
        return ("contexto_efectivo_tokens", declarado, conservado)
    diferencia = _diferencia_parametros(
        escenario.get("parametros_ejecucion"),
        bloque.get("parametros_ejecucion"),
    )
    if diferencia is not None:
        return diferencia
    conservado = bloque.get("presupuesto_vram_total_mib")
    declarado = _valor_anidado(escenario, "presupuesto_vram", "total_mib")
    if declarado != conservado:
        return ("presupuesto_vram_total_mib", declarado, conservado)
    return None


def _motivo_revocacion(escenario, clave, declarado, conservado):
    """Motivo de `CB-006` y `DEC-012` que nombra la clave y ambos valores."""
    identificador = escenario.get("id")
    referencia = (
        f"escenario «{identificador}»"
        if isinstance(identificador, str) and identificador
        else "escenario sin identificador"
    )
    return (
        f"{referencia}: la aprobación conserva «{clave}» con el valor "
        f"{conservado!r} y el escenario declara {declarado!r}; la diferencia "
        "revoca la condición de aprobado y exige 1 medición nueva (`CB-006`)"
    )


def validar_admisibilidad_escenario(escenario):
    """Admisibilidad de selección de `RF-011` y `CB-006` como ``(admisible, motivo)``."""
    _objeto(escenario, "escenario")
    estado = escenario.get("estado")
    if estado == ESTADO_NO_EJECUTABLE:
        return (False, MOTIVO_NO_EJECUTABLE)
    if estado == ESTADO_APROBADO:
        aprobacion = escenario.get("aprobacion")
        if not isinstance(aprobacion, dict) or not aprobacion:
            return (False, MOTIVO_APROBACION_AUSENTE)
        diferencia = _diferencia_aprobacion(escenario, aprobacion)
        if diferencia is not None:
            return (False, _motivo_revocacion(escenario, *diferencia))
        return (True, "")
    if estado in ESTADOS_EJECUTABLES:
        if _falta_contexto_resuelto(escenario):
            return (False, MOTIVO_CONTEXTO_NO_RESUELTO)
        return (True, "")
    return (
        False,
        f"estado {estado!r} no admitido: no consta entre "
        f"{', '.join(ESTADOS_EJECUTABLES)}",
    )
