"""Comprobación previa sin carga de SPEC-017.

Implementa el modo `comprobar` de `DEC-003` y la salida de `C-9` sobre las 5
comprobaciones: la comprobación 1 contrasta la existencia de los artefactos del
perfil —ejecutable, modelo y `mmproj` siempre, y el modelo `draft` solo cuando el
perfil lo declara—, la comprobación 2 contrasta la cuantización del archivo de
pesos con la regla de `DEC-019` —`nombre_gguf` y `tamano_bytes` como identidad
del archivo, `tipo_gguf` exigido además cuando su valor no es `null`, y la
etiqueta `declarada` tratada como dato de distribución y nunca comparada contra
el nombre interno del archivo—, la comprobación 3 contrasta las opciones
declaradas con las que la ayuda del binario enumera, la comprobación 4 contrasta
el presupuesto de VRAM del perfil con la VRAM disponible y la comprobación 5
contrasta el estado declarado del perfil con su huella de opciones.

Comprobación 3 (`CB-002`, `DEC-010`): consume el mapa `opciones_aceptadas` —eje
de opciones → forma que el binario enumera— con
``binario.verificar_compatibilidad``; 1 eje ausente del mapa o con `None` no está
aceptado. 1 opción rechazada deja la comprobación en `FALLIDA`, nombra la opción
y produce el código `3` de `C-8`. El mapa se inyecta porque lo lee
``binario.opciones_aceptadas`` de la ayuda del binario; 1 mapa ausente no
acredita ninguna opción, de modo que la comprobación nunca se declara `SUPERADA`
sin enumeración del binario.

Comprobación 4 (`DEC-018`, `DEC-028`): el consumo se calcula en MiB como
`pesos_en_vram_mib` más `kv_no_swa_por_1024_tokens_mib` por el `ctx_size` efectivo
de `C-3` entre `1024` más `kv_swa_mib`, que es 1 valor fijo y no depende del
contexto, más `buffer_computo_mib`, y se contrasta con `vram_disponible_mib`. El
bloque declara las 4 claves de `C-1` y la clave retirada
`kv_por_1024_tokens_mib` no existe: 1 bloque que la declare se rechaza con
`ValueError` que nombra la clave, porque su presencia es 1 bloque no conforme. El
`ctx_size` que decide es el de ``opciones_efectivas`` cuando se informa, porque
es el que el servidor arranca; sin ese argumento se conserva el `ctx_size`
declarado en el manifiesto. Mientras el bloque `presupuesto_vram` conserve su
clave `pendiente` la comprobación se reporta `PENDIENTE`, nombra la tarea que
completa el presupuesto, no se declara `SUPERADA` y no produce código `6`; con el
bloque completo y la VRAM disponible informada se resuelve `SUPERADA` o `FALLIDA`
con el código `6`; con la VRAM disponible no informada se reporta `PENDIENTE` con
el motivo, porque 1 presupuesto sin dato de GPU no se contrasta ni se estima.

Comprobación 5 (`C-4`, `DEC-020`): usa ``perfiles.huella_opciones`` y
``perfiles.estado_por_huella`` sobre el registro que acredita el estado, que es
el bloque `aprobacion` del manifiesto cuando declara su `huella_opciones`. 1
perfil en `candidato` es coherente; 1 perfil en `medido` o `aprobado` sin
registro de huella coincidente es incoherente, deja la comprobación en `FALLIDA`
con el motivo de la degradación de `C-4` y no produce código propio, porque
`C-8` no declara ninguno para esta comprobación.

Contrato:

- ``ejecutar(manifiesto, raiz, *, lector_metadatos=None, opciones_aceptadas=None,
  vram_disponible_mib=None, opciones_efectivas=None)`` devuelve 1 diccionario con
  las claves ``comprobaciones`` y ``codigo``. ``comprobaciones`` declara 1 entrada
  por comprobación de `C-9`, en su orden, con ``numero``, ``estado`` en los 3
  valores ``SUPERADA``, ``FALLIDA`` o ``PENDIENTE`` y ``detalle`` de texto.
  ``codigo`` es el entero de `C-8` del primer fallo en el orden de las
  comprobaciones: `4` artefacto requerido ausente, `5` cuantización del archivo
  distinta de la declarada, `3` opción rechazada por el binario y `6` presupuesto
  de VRAM insuficiente, o `0` cuando ninguna comprobación falla.
- ``formatear_salida(resultado)`` devuelve 1 línea por comprobación con la forma
  ``<ESTADO> <n>. <comprobación>: <detalle>``, la línea de cierre
  ``COMPROBACIÓN PREVIA: <n> de 5 comprobaciones superadas`` —con el sufijo
  ``, <m> pendiente`` cuando existe 1 comprobación pendiente— y, cuando el
  resultado declara la clave ``milisegundos``, la línea ``TIEMPO: <n> ms``.

``manifiesto`` llega como diccionario ya leído y ``raiz`` es la raíz contra la
que se resuelven las rutas relativas del bloque ``artefactos``. El lector de
metadatos se inyecta para que la suite use 1 doble y no lea ``bin/``,
``models/`` ni la GPU, conforme a `DEC-012`; por omisión se usa
``gguf.leer_metadatos``.

``verificar_recursos_escenario(escenario, *, medidor_vram=None,
medidor_ram=None)`` implementa el precheck de recursos de `C-4` de `SPEC-018`
sobre 1 escenario ya cargado del catálogo y devuelve 1 diccionario con
``codigo`` —`3` en el primer aborto y `0` sin hallazgos—, ``escenario_id``,
``contexto_solicitado_tokens`` —el ``contexto.declarado_tokens`` solicitado— y
``hallazgos``, 1 secuencia de líneas ``[FALLO] `` vacía cuando el código es `0`.
Evalúa las condiciones en el orden de `C-4`: (1) el estado ``no_ejecutable``
aborta sin medir recursos (`CB-007`, `DEC-003`); (2) el contexto ajustado cuyo
valor resuelto es menor o igual a 4096 tokens aborta con el valor declarado
(`CB-003`, `DEC-008`), y el que no declara valor numérico resuelto también
(`RF-010`); (3) la VRAM no medible aborta sin estimar valor alguno (`CB-001`);
(4) el presupuesto mayor que la VRAM disponible declara ambos valores en MiB
(`RF-007`); (5) la RAM libre del host menor a 8192 MiB con capas de expertos en
CPU declara ambos valores en MiB (`CB-008`, `DEC-006`), y su ausencia de
medición aborta sin estimar. ``medidor_vram`` y ``medidor_ram`` son invocables
sin argumentos que devuelven MiB o `None`; con `None` se usan
``medir.vram_libre_mib`` y ``ram_libre_host_mib``, de modo que la suite inyecta
siempre sus dobles y no toca la GPU ni el host, conforme a `DEC-012`.
`medidor_ram` se consulta solo cuando ``capas_cpu_moe > 0``.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import binario
import escenarios
import gguf
import medir
import perfiles

__all__ = [
    "ejecutar",
    "formatear_salida",
    "ram_libre_host_mib",
    "verificar_recursos_escenario",
]

# Las 5 comprobaciones de `C-9`, en el orden en que se ejecutan y se imprimen.
NOMBRES_COMPROBACIONES = (
    "artefactos del perfil",
    "cuantización del archivo de pesos",
    "opciones frente al binario",
    "presupuesto de VRAM frente a la VRAM disponible",
    "coherencia del perfil frente a su huella y su estado",
)

# Los 3 estados admitidos por `C-9` y ningún otro.
ESTADO_SUPERADA = "SUPERADA"
ESTADO_FALLIDA = "FALLIDA"
ESTADO_PENDIENTE = "PENDIENTE"

# Códigos de `C-8` que produce esta comprobación previa.
CODIGO_OK = 0
CODIGO_OPCION_RECHAZADA = 3
CODIGO_ARTEFACTO_AUSENTE = 4
CODIGO_CUANTIZACION_DIVERGENTE = 5
CODIGO_PRESUPUESTO_INSUFICIENTE = 6
CODIGOS = (
    CODIGO_OK,
    CODIGO_OPCION_RECHAZADA,
    CODIGO_ARTEFACTO_AUSENTE,
    CODIGO_CUANTIZACION_DIVERGENTE,
    CODIGO_PRESUPUESTO_INSUFICIENTE,
)

# Primer fallo → código de `C-8`, en el orden de las comprobaciones. La
# comprobación 5 no declara código propio en `C-8`.
CODIGOS_POR_COMPROBACION = {
    1: CODIGO_ARTEFACTO_AUSENTE,
    2: CODIGO_CUANTIZACION_DIVERGENTE,
    3: CODIGO_OPCION_RECHAZADA,
    4: CODIGO_PRESUPUESTO_INSUFICIENTE,
}

# Los 3 artefactos que todo perfil declara y el `draft`, que es opcional.
ARTEFACTOS_SIEMPRE = ("ejecutable", "modelo", "mmproj")
ARTEFACTO_OPCIONAL = "draft"

# Las 4 claves medidas del bloque `presupuesto_vram` de `C-1` y la marca que
# conserva mientras la primera carga real no las mide; la marca nombra la tarea
# que las escribe y se lee del manifiesto, conforme a `DEC-018`, `DEC-025` y
# `DEC-028`.
CLAVES_PRESUPUESTO = (
    "pesos_en_vram_mib",
    "kv_no_swa_por_1024_tokens_mib",
    "kv_swa_mib",
    "buffer_computo_mib",
)
CLAVE_PENDIENTE = "pendiente"

# Clave retirada por `DEC-028`: el bloque que la declare es 1 bloque no conforme y
# ninguna función de este módulo la lee.
CLAVE_PRESUPUESTO_RETIRADA = "kv_por_1024_tokens_mib"

# Tokens sobre los que se declara la caché no-SWA del presupuesto; la caché SWA
# es 1 valor fijo que no se multiplica por el contexto.
TOKENS_POR_CALCULO_KV = 1024

# Estados que el manifiesto solo conserva con 1 registro de huella coincidente.
ESTADOS_PROMOVIDOS = ("medido", "aprobado")

# `C-4` y `C-2`: el código `3` del aborto del precheck de recursos —el mismo
# valor que la opción rechazada de `C-8`, con otro significado— y el mínimo de
# RAM libre del host cuando el escenario deriva capas de expertos a CPU
# (`CB-008`, `DEC-006`).
CODIGO_ABORTO_RECURSOS = 3
RAM_LIBRE_MINIMA_HOST_MIB = 8192

# Consulta de solo lectura de la RAM física libre del host en KiB: la misma vía
# no interactiva de PowerShell que usa `medir` para los procesos, sin depender
# del perfil del usuario ni del directorio actual (`DEC-006`).
COMANDO_RAM_LIBRE = list(medir.POWERSHELL) + [
    "Get-CimInstance -ClassName Win32_OperatingSystem | "
    "Select-Object -ExpandProperty FreePhysicalMemory"
]


def _detalle_artefactos_ausentes(ausentes):
    """Compone el detalle de la comprobación 1 con las rutas ausentes."""
    etiqueta = "artefacto ausente" if len(ausentes) == 1 else "artefactos ausentes"
    return f"[ERROR] {etiqueta}: " + "; ".join(ausentes)


def _comprobar_artefactos(manifiesto, raiz):
    """Comprobación 1 de `C-9`: existencia de los artefactos del perfil."""
    artefactos = manifiesto.get("artefactos") or {}
    ausentes = []
    presentes = []
    for clave in ARTEFACTOS_SIEMPRE + (ARTEFACTO_OPCIONAL,):
        relativa = artefactos.get(clave)
        if relativa is None:
            if clave == ARTEFACTO_OPCIONAL:
                continue  # el perfil sin decodificación especulativa no lo declara
            ausentes.append(f"{clave} (no declarado)")
            continue
        if (raiz / relativa).exists():
            presentes.append(clave)
        else:
            ausentes.append(f"{clave} {relativa}")
    if ausentes:
        return {
            "numero": 1,
            "estado": ESTADO_FALLIDA,
            "detalle": _detalle_artefactos_ausentes(ausentes),
        }
    return {
        "numero": 1,
        "estado": ESTADO_SUPERADA,
        "detalle": f"{len(presentes)} artefactos presentes: " + ", ".join(presentes),
    }


def _divergencias_cuantizacion(bloque, leidos):
    """Señales exigidas que difieren de la lectura del archivo, según `DEC-019`."""
    divergencias = []
    nombre_declarado = bloque.get("nombre_gguf")
    if nombre_declarado != leidos.get("nombre"):
        divergencias.append("nombre_gguf")
    if bloque.get("tamano_bytes") != leidos.get("tamano_bytes"):
        divergencias.append("tamano_bytes")
    tipo_declarado = bloque.get("tipo_gguf")
    if tipo_declarado is not None and tipo_declarado != leidos.get("file_type"):
        divergencias.append("tipo_gguf")
    return divergencias


def _comprobar_cuantizacion(manifiesto, raiz, lector_metadatos):
    """Comprobación 2 de `C-9`: cuantización del archivo de pesos (`DEC-019`)."""
    bloque = manifiesto.get("cuantizacion") or {}
    declarada = bloque.get("declarada")
    relativa = (manifiesto.get("artefactos") or {}).get("modelo")
    if not relativa:
        return {
            "numero": 2,
            "estado": ESTADO_FALLIDA,
            "detalle": (
                f"[ERROR] cuantización declarada {declarada}, "
                "nombre interno leído no disponible: el perfil no declara el artefacto modelo"
            ),
        }
    ruta = raiz / relativa
    try:
        leidos = lector_metadatos(ruta)
        if not isinstance(leidos, dict):
            raise ValueError("el lector no devolvió 1 diccionario de metadatos")
    except (OSError, ValueError) as exc:
        return {
            "numero": 2,
            "estado": ESTADO_FALLIDA,
            "detalle": (
                f"[ERROR] cuantización declarada {declarada}, "
                f"nombre interno leído no disponible: {ruta}: {exc}"
            ),
        }

    divergencias = _divergencias_cuantizacion(bloque, leidos)
    if divergencias:
        return {
            "numero": 2,
            "estado": ESTADO_FALLIDA,
            "detalle": (
                f"[ERROR] cuantización declarada {declarada}, "
                f"nombre interno leído {leidos.get('nombre')}; "
                f"difieren: {', '.join(divergencias)}"
            ),
        }

    detalle = (
        f"archivo de pesos coincidente: nombre interno {leidos.get('nombre')}, "
        f"{leidos.get('tamano_bytes')} bytes"
    )
    if bloque.get("tipo_gguf") is None:
        detalle += "; tipo_gguf no concluyente (null) con las 2 señales de reserva"
    return {"numero": 2, "estado": ESTADO_SUPERADA, "detalle": detalle}


def _detalle_opciones_rechazadas(rechazadas, opciones):
    """Compone el detalle de la comprobación 3 con las opciones rechazadas."""
    nombradas = [f"{eje} ({opciones.get(eje)})" for eje in rechazadas]
    etiqueta = "opción rechazada" if len(nombradas) == 1 else "opciones rechazadas"
    return f"[ERROR] {etiqueta} por el binario: " + ", ".join(nombradas)


def _comprobar_opciones(manifiesto, opciones_aceptadas):
    """Comprobación 3 de `C-9`: opciones frente al binario (`DEC-010`).

    El mapa se normaliza antes de contrastarlo: 1 eje con `None` no está aceptado,
    igual que 1 eje ausente, y 1 mapa no informado no acredita ninguna opción.
    """
    opciones = manifiesto.get("opciones") or {}
    aceptadas = {
        eje: forma
        for eje, forma in (opciones_aceptadas or {}).items()
        if forma is not None
    }
    rechazadas = binario.verificar_compatibilidad(opciones, aceptadas)
    if rechazadas:
        return {
            "numero": 3,
            "estado": ESTADO_FALLIDA,
            "detalle": _detalle_opciones_rechazadas(rechazadas, opciones),
        }
    enumeradas = [f"{eje} {aceptadas[eje]}" for eje in sorted(opciones)]
    return {
        "numero": 3,
        "estado": ESTADO_SUPERADA,
        "detalle": (
            f"{len(opciones)} opciones enumeradas por el binario: "
            + ", ".join(enumeradas)
        ),
    }


def _texto_mib(valor):
    """Texto de 1 magnitud en MiB, sin decimales."""
    return f"{round(valor)}"


def _consumo_vram_mib(bloque, opciones):
    """Consumo de `C-9` con la fórmula de `DEC-028`.

    Pesos en VRAM más la caché no-SWA proporcional al contexto más la caché SWA
    fija, que no escala con `ctx_size`, más el buffer de cómputo.
    """
    tokens = opciones.get("ctx_size") or 0
    return (
        bloque["pesos_en_vram_mib"]
        + bloque["kv_no_swa_por_1024_tokens_mib"] * tokens / TOKENS_POR_CALCULO_KV
        + bloque["kv_swa_mib"]
        + bloque["buffer_computo_mib"]
    )


def _rechazar_presupuesto_retirado(bloque):
    """Rechaza el bloque que declara la clave retirada por `DEC-028`.

    La clave `kv_por_1024_tokens_mib` desaparece del bloque de 4 claves de `C-1`:
    ninguna función la lee y su presencia es 1 bloque no conforme, de modo que la
    comprobación 4 no puede contrastar 1 presupuesto con 2 cachés de distinta
    forma. El error nombra la clave para que el manifiesto se corrija.
    """
    if CLAVE_PRESUPUESTO_RETIRADA in bloque:
        raise ValueError(
            "presupuesto_vram: el bloque declara la clave retirada "
            f"«{CLAVE_PRESUPUESTO_RETIRADA}» y C-1 exige las 4 claves "
            f"{', '.join(CLAVES_PRESUPUESTO)}: la clave no se lee y su "
            "presencia es 1 bloque no conforme, conforme a DEC-028"
        )


def _detalle_presupuesto_pendiente(marca, faltantes=None):
    """Compone el detalle de la comprobación 4 con la marca `pendiente` del manifiesto.

    La marca nombra la tarea que escribe el presupuesto y se lee del manifiesto: no
    existe constante de tarea en el código y, si la marca falta o no es 1 texto no
    vacío, el detalle no la inventa, conforme a `DEC-018` y `DEC-025`.
    """
    if faltantes:
        detalle = "presupuesto de VRAM incompleto: falta " + ", ".join(faltantes)
    else:
        detalle = "presupuesto de VRAM no medido"
    if isinstance(marca, str) and marca.strip():
        return f"{detalle}: lo completa {marca} en la primera carga real"
    return f"{detalle}: sin marca pendiente que nombre la tarea que lo completa"


def _comprobar_presupuesto(manifiesto, vram_disponible_mib, opciones_efectivas=None):
    """Comprobación 4 de `C-9`: presupuesto de VRAM frente a la disponible.

    El `ctx_size` que decide el consumo es el de ``opciones_efectivas`` cuando la
    resolución de `C-3` se informa, porque es el contexto con el que el servidor
    arranca; sin ese argumento se conserva el declarado en el manifiesto. El
    bloque debe declarar las 4 claves de `C-1` y la clave retirada
    `kv_por_1024_tokens_mib` lo deja no conforme, con `ValueError` que la nombra.
    Ningún camino de esta comprobación emite el código `6` por 1 presupuesto no
    medido: el código solo se produce cuando el bloque está completo y el consumo
    supera la VRAM disponible informada, conforme a `DEC-018` y `DEC-028`.
    """
    bloque = manifiesto.get("presupuesto_vram") or {}
    _rechazar_presupuesto_retirado(bloque)
    marca = bloque.get(CLAVE_PENDIENTE)
    if marca is not None:
        detalle = _detalle_presupuesto_pendiente(marca)
        motivo = bloque.get("motivo")
        if motivo:
            detalle += f"; motivo: {motivo}"
        return {"numero": 4, "estado": ESTADO_PENDIENTE, "detalle": detalle}

    faltantes = [clave for clave in CLAVES_PRESUPUESTO if bloque.get(clave) is None]
    if faltantes:
        return {
            "numero": 4,
            "estado": ESTADO_PENDIENTE,
            "detalle": _detalle_presupuesto_pendiente(marca, faltantes),
        }

    if opciones_efectivas is None:
        opciones = manifiesto.get("opciones") or {}
    else:
        opciones = opciones_efectivas
    tokens = opciones.get("ctx_size") or 0
    consumo = _consumo_vram_mib(bloque, opciones)
    if vram_disponible_mib is None:
        return {
            "numero": 4,
            "estado": ESTADO_PENDIENTE,
            "detalle": (
                f"VRAM disponible no informada: el presupuesto de "
                f"{_texto_mib(consumo)} MiB para {tokens} tokens de contexto no "
                "se contrasta ni se estima"
            ),
        }
    if consumo > vram_disponible_mib:
        return {
            "numero": 4,
            "estado": ESTADO_FALLIDA,
            "detalle": (
                f"[ERROR] presupuesto de VRAM insuficiente: {_texto_mib(consumo)} "
                f"MiB para {tokens} tokens de contexto frente a "
                f"{_texto_mib(vram_disponible_mib)} MiB disponibles"
            ),
        }
    return {
        "numero": 4,
        "estado": ESTADO_SUPERADA,
        "detalle": (
            f"presupuesto de VRAM de {_texto_mib(consumo)} MiB para {tokens} "
            f"tokens de contexto cabe en {_texto_mib(vram_disponible_mib)} MiB "
            "disponibles"
        ),
    }


def _registros_de_aprobacion(manifiesto):
    """Registro que acredita el estado: el bloque `aprobacion` de `C-4`."""
    aprobacion = manifiesto.get("aprobacion")
    if isinstance(aprobacion, dict) and "huella_opciones" in aprobacion:
        return {"aprobacion": aprobacion}
    return {}


def _comprobar_coherencia(manifiesto):
    """Comprobación 5 de `C-9`: estado declarado frente a su huella (`C-4`)."""
    registros = _registros_de_aprobacion(manifiesto)
    try:
        estado_reportado, motivo = perfiles.estado_por_huella(manifiesto, registros)
        huella = perfiles.huella_opciones(manifiesto.get("opciones") or {})
    except ValueError as exc:
        return {
            "numero": 5,
            "estado": ESTADO_FALLIDA,
            "detalle": f"[ERROR] huella de opciones no contrastable: {exc}",
        }

    declarado = manifiesto.get("estado")
    if motivo is not None:
        return {
            "numero": 5,
            "estado": ESTADO_FALLIDA,
            "detalle": (
                f"[ERROR] estado declarado {declarado} degradado a "
                f"{estado_reportado}: {motivo}; la huella de las opciones del "
                f"perfil es {huella}"
            ),
        }
    if declarado in ESTADOS_PROMOVIDOS and not registros:
        return {
            "numero": 5,
            "estado": ESTADO_FALLIDA,
            "detalle": (
                f"[ERROR] estado declarado {declarado} sin registro de huella "
                f"coincidente: la huella de las opciones del perfil es {huella}"
            ),
        }
    return {
        "numero": 5,
        "estado": ESTADO_SUPERADA,
        "detalle": (
            f"estado {declarado} coherente con la huella de las opciones: {huella}"
        ),
    }


def ejecutar(
    manifiesto,
    raiz,
    *,
    lector_metadatos=None,
    opciones_aceptadas=None,
    vram_disponible_mib=None,
    opciones_efectivas=None,
):
    """Ejecuta las 5 comprobaciones de `C-9` sin lanzar el servidor.

    `opciones_aceptadas` es el mapa de la ayuda del binario que consume la
    comprobación 3 y `vram_disponible_mib` la VRAM disponible de la GPU dedicada
    en MiB que consume la comprobación 4. `opciones_efectivas` es el mapa de
    opciones que resuelve `C-3` y del que la comprobación 4 toma su `ctx_size`;
    con `None` se usa el `ctx_size` declarado en el manifiesto. El código
    devuelto es el del primer fallo en el orden de las comprobaciones.
    """
    raiz = Path(raiz)
    if lector_metadatos is None:
        lector_metadatos = gguf.leer_metadatos

    comprobaciones = [
        _comprobar_artefactos(manifiesto, raiz),
        _comprobar_cuantizacion(manifiesto, raiz, lector_metadatos),
        _comprobar_opciones(manifiesto, opciones_aceptadas),
        _comprobar_presupuesto(
            manifiesto, vram_disponible_mib, opciones_efectivas
        ),
        _comprobar_coherencia(manifiesto),
    ]

    codigo = CODIGO_OK
    for comprobacion in comprobaciones:
        if comprobacion["estado"] == ESTADO_FALLIDA:
            codigo = CODIGOS_POR_COMPROBACION.get(comprobacion["numero"], CODIGO_OK)
            break
    return {"comprobaciones": comprobaciones, "codigo": codigo}


def formatear_salida(resultado):
    """Devuelve las líneas de `C-9` para el resultado de `ejecutar`."""
    comprobaciones = sorted(
        resultado.get("comprobaciones", ()), key=lambda comprobacion: comprobacion["numero"]
    )
    lineas = []
    superadas = 0
    pendientes = 0
    for comprobacion in comprobaciones:
        numero = comprobacion["numero"]
        estado = comprobacion["estado"]
        nombre = NOMBRES_COMPROBACIONES[numero - 1]
        lineas.append(f"{estado} {numero}. {nombre}: {comprobacion['detalle']}")
        if estado == ESTADO_SUPERADA:
            superadas += 1
        elif estado == ESTADO_PENDIENTE:
            pendientes += 1

    cierre = (
        f"COMPROBACIÓN PREVIA: {superadas} de {len(NOMBRES_COMPROBACIONES)} "
        "comprobaciones superadas"
    )
    if pendientes:
        cierre += f", {pendientes} pendiente"
    lineas.append(cierre)

    if "milisegundos" in resultado:
        lineas.append(f"TIEMPO: {resultado['milisegundos']} ms")
    return lineas


def ram_libre_host_mib():
    """Devuelve la RAM física libre del host en MiB, o `None` sin PowerShell.

    Consulta de solo lectura de `CB-008` y `DEC-006`: lee ``FreePhysicalMemory``
    del sistema operativo, que llega en KiB, y lo convierte a MiB sin redondear
    hacia arriba. 1 herramienta ausente, 1 consulta fallida y 1 valor no
    numérico devuelven `None` y no estiman magnitud alguna, de modo que el
    precheck aborta sin sustituir la medición por 1 valor inventado.
    """
    try:
        proceso = subprocess.run(
            COMANDO_RAM_LIBRE,
            capture_output=True,
            check=False,
            timeout=medir.TIEMPO_LIMITE_SEGUNDOS,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proceso.returncode != 0:
        return None
    salida = (proceso.stdout or b"").decode("utf-8-sig", errors="replace")
    linea = next((texto.strip() for texto in salida.splitlines() if texto.strip()), "")
    try:
        kib = int(linea)
    except ValueError:
        return None
    return kib // 1024


def _resultado_recursos(escenario, hallazgos):
    """Resultado de `C-4`: código, escenario, contexto solicitado y hallazgos."""
    contexto = escenario.get("contexto") or {}
    return {
        "codigo": CODIGO_ABORTO_RECURSOS if hallazgos else CODIGO_OK,
        "escenario_id": escenario.get("id"),
        "contexto_solicitado_tokens": contexto.get("declarado_tokens"),
        "hallazgos": list(hallazgos),
    }


def _token_resuelto(contexto):
    """Tokens efectivos resueltos de 1 contexto ajustado, o `None` sin valor."""
    tokens = contexto.get("efectivo_tokens")
    if isinstance(tokens, bool) or not isinstance(tokens, int) or tokens <= 0:
        return None
    return tokens


def verificar_recursos_escenario(escenario, *, medidor_vram=None, medidor_ram=None):
    """Precheck de recursos de `C-4` sobre 1 escenario del catálogo.

    Evalúa las condiciones en el orden de `C-4` y aborta en la primera que no se
    cumple, con 1 línea ``[FALLO] `` que declara el motivo y el escenario: el
    estado ``no_ejecutable`` sin medir recursos (`CB-007`), el contexto ajustado
    resuelto menor o igual a 4096 tokens o sin valor numérico (`CB-003`,
    `RF-010`), la VRAM no medible sin estimar (`CB-001`), el presupuesto mayor
    que la VRAM disponible (`RF-007`) y la RAM libre del host insuficiente o no
    medible con capas de expertos en CPU (`CB-008`). Sin hallazgos devuelve el
    código `0` y 1 secuencia vacía. ``medidor_vram`` y ``medidor_ram`` son
    invocables sin argumentos que devuelven MiB o `None`; con `None` se usan
    ``medir.vram_libre_mib`` y ``ram_libre_host_mib``. La VRAM se mide 1 sola
    vez y la RAM solo cuando ``capas_cpu_moe > 0``.
    """
    medir_vram = medir.vram_libre_mib if medidor_vram is None else medidor_vram
    medir_ram = ram_libre_host_mib if medidor_ram is None else medidor_ram
    identificador = escenario.get("id")

    if escenario.get("estado") == escenarios.ESTADO_NO_EJECUTABLE:
        return _resultado_recursos(
            escenario,
            [
                f"[FALLO] Escenario no ejecutable: {identificador}: la "
                "combinación declarada no alcanza el estado de servicio en la "
                "GPU objetivo (CB-007)"
            ],
        )

    contexto = escenario.get("contexto") or {}
    if contexto.get("tipo") == escenarios.TIPO_CONTEXTO_AJUSTADO:
        tokens = _token_resuelto(contexto)
        if tokens is None:
            return _resultado_recursos(
                escenario,
                [
                    "[FALLO] Contexto ajustado sin valor numérico resuelto: el "
                    f"escenario {identificador} no declara «efectivo_tokens» "
                    "positivo y no admite selección (RF-010)"
                ],
            )
        if tokens <= escenarios.SUELO_CONTEXTO_RESUELTO_TOKENS:
            return _resultado_recursos(
                escenario,
                [
                    "[FALLO] Contexto ajustado resuelto insuficiente: "
                    f"{tokens} <= {escenarios.SUELO_CONTEXTO_RESUELTO_TOKENS} "
                    f"tokens en el escenario {identificador} (CB-003)"
                ],
            )

    vram_disponible_mib = medir_vram()
    if vram_disponible_mib is None:
        return _resultado_recursos(
            escenario,
            [
                "[FALLO] VRAM disponible no medible: se aborta el escenario "
                f"{identificador} sin estimar valor alguno (CB-001)"
            ],
        )

    presupuesto = escenario.get("presupuesto_vram") or {}
    requerido_mib = presupuesto.get("total_mib")
    if requerido_mib is not None and vram_disponible_mib < requerido_mib:
        return _resultado_recursos(
            escenario,
            [
                "[FALLO] Presupuesto excede VRAM disponible: requerido "
                f"{_texto_mib(requerido_mib)} MiB, disponible "
                f"{_texto_mib(vram_disponible_mib)} MiB en el escenario "
                f"{identificador} (RF-007)"
            ],
        )

    capas_cpu_moe = escenario.get("capas_cpu_moe") or 0
    if capas_cpu_moe > 0:
        ram_libre_mib = medir_ram()
        if ram_libre_mib is None:
            return _resultado_recursos(
                escenario,
                [
                    "[FALLO] RAM libre de host no medible: se aborta el "
                    f"escenario {identificador}, que deriva {capas_cpu_moe} "
                    "capas de expertos a CPU, sin estimar valor alguno (CB-008)"
                ],
            )
        if ram_libre_mib < RAM_LIBRE_MINIMA_HOST_MIB:
            return _resultado_recursos(
                escenario,
                [
                    "[FALLO] RAM libre de host insuficiente: disponible "
                    f"{_texto_mib(ram_libre_mib)} MiB, requerida "
                    f"{RAM_LIBRE_MINIMA_HOST_MIB} MiB en el escenario "
                    f"{identificador}, que deriva {capas_cpu_moe} capas de "
                    "expertos a CPU (CB-008)"
                ],
            )

    return _resultado_recursos(escenario, [])
