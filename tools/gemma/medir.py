"""Medición de memoria del servidor de SPEC-017.

Implementa la fuente de `RF-008`, `RNF-003` y `RNF-007` conforme a `CA-007`,
`DEC-006`, `DEC-012` y `DEC-017`, con los nombres efectivos de contador que el
operador local verificó en `T-012` sobre la máquina objetivo. La medición no
estima valores ausentes: si la consulta de la GPU no está disponible, el
resultado declara el código `7` y ninguna clave de valor.

Contrato:

- ``medir_memoria(pids, *, ejecutor=None)`` recibe los identificadores del árbol
  de procesos del servidor y devuelve 1 diccionario con exactamente las claves
  ``codigo``, ``vram_total_mib``, ``vram_usada_mib``, ``vram_libre_mib``,
  ``residente_mib``, ``desbordamiento_mib`` y ``contador_desbordamiento``.
- ``ejecutor`` es 1 invocable ``ejecutor(comando: list[str]) -> str`` que
  devuelve la salida estándar del comando y lanza ``FileNotFoundError`` cuando
  la herramienta no existe. Con ``None`` el módulo ejecuta los comandos reales
  con ``subprocess``; las pruebas inyectan siempre su doble, conforme a
  `DEC-012`.
- ``vram_libre_mib(*, ejecutor=None)`` es la consulta de solo lectura de
  `T-068`: ejecuta ``nvidia-smi --query-gpu=memory.free`` con formato CSV sin
  cabecera ni unidades, devuelve la VRAM libre en MiB como ``float`` y `None`
  cuando la herramienta no está.
- Orden de consulta: (1) ``nvidia-smi`` con los 3 campos de memoria de la GPU;
  (2) los contadores de proceso por PID; (3) el respaldo de adaptador, solo si
  el conjunto de proceso no aporta filas del árbol; (4) la memoria residente.
- Los bytes se dividen entre ``1048576`` y toda suma se limita a los PID del
  árbol, comparados por PID completo y no por prefijo del nombre de instancia.
- La memoria residente se consulta con ``Get-Process`` y no con
  ``Win32_Process``: en la máquina objetivo ``Win32_Process.WorkingSet64``
  llega vacío para ``llama-server`` mientras ``Get-Process`` devuelve el
  conjunto de trabajo real del mismo PID. La magnitud es el ``WorkingSet64``
  de `DEC-006`; solo cambia la vía de consulta. Cada PID del árbol exige su
  fila: la ausencia se informa como ``ValueError`` que nombra el PID y no se
  suma como ``0`` en silencio.

Desbordamiento: el ``Shared Usage`` del conjunto de proceso es la fuente
primaria; el ``Shared Usage`` del conjunto de adaptador es el respaldo efectivo
de `DEC-017`. El nombre ``Non Local Usage`` del adaptador no está enumerado en
la máquina objetivo y se descarta: no se consulta ni se usa como respaldo.
"""

from __future__ import annotations

import csv
import io
import re
import subprocess

__all__ = ["medir_memoria", "vram_libre_mib"]

# 1 MiB en bytes: divisor de toda magnitud de memoria del contrato.
BYTES_POR_MIB = 1048576

# Tiempo límite de cada consulta, en segundos: los contadores y la consulta de la
# GPU responden en milisegundos, y 1 herramienta que no responde se reporta como
# error de lectura en lugar de bloquear la medición.
TIEMPO_LIMITE_SEGUNDOS = 10

# Consulta 1: los 3 campos de memoria de la GPU dedicada, sin cabecera ni
# unidades, de modo que los valores llegan ya en MiB (DEC-006).
COMANDO_NVIDIA_SMI = [
    "nvidia-smi",
    "--query-gpu=memory.total,memory.used,memory.free",
    "--format=csv,noheader,nounits",
]

# `T-068` y `DEC-018`: la comprobación 4 de `C-9` necesita la VRAM libre sin
# cargar el modelo, de modo que la consulta se acota al campo `memory.free` y
# no consulta contadores, memoria residente ni PowerShell.
COMANDO_VRAM_LIBRE = [
    "nvidia-smi",
    "--query-gpu=memory.free",
    "--format=csv,noheader,nounits",
]

# Clases WMI de los contadores de GPU de Windows 11 verificadas en T-012.
CLASE_PROCESO = "Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory"
CLASE_ADAPTADOR = "Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory"

# Nombres efectivos completos de los contadores de desbordamiento, tal como
# `Get-Counter -ListSet` los enumeró en T-012 (DEC-017).
CONTADOR_PROCESO = r"\GPU Process Memory(*)\Shared Usage"
CONTADOR_ADAPTADOR = r"\GPU Adapter Memory(*)\Shared Usage"

# Columnas del CSV de contadores y del CSV de memoria residente.
COLUMNAS_CONTADORES = ("Name", "DedicatedUsage", "SharedUsage")
COLUMNAS_RESIDENTE = ("Id", "WorkingSet64")

# Instancia de contador de proceso: el PID encabeza el nombre con la forma
# `pid_<n>_luid_...`. El límite derecho impide leer `pid_4242` de `pid_42421`.
PATRON_PID = re.compile(r"^pid_(\d+)(?:_|$)")

# Invocación no interactiva de PowerShell: la consulta no depende del perfil del
# usuario ni del directorio actual.
POWERSHELL = ("powershell.exe", "-NoProfile", "-NonInteractive", "-Command")

# Consulta 4: el conjunto de trabajo de cada proceso, en bytes. La consulta es
# global y el módulo limita la suma a los PID del árbol.
#
# La vía es `Get-Process` y no `Get-CimInstance -ClassName Win32_Process`: en la
# máquina objetivo el `WorkingSet64` de la clase WMI llega vacío para el proceso
# `llama-server` —el mismo PID que `Get-Process` informa con `991612928` bytes—,
# de modo que la consulta por CIM produciría 1 residente no medible. La magnitud
# es la misma de `DEC-006`; la vía de consulta no está fijada por esa decisión.
COMANDO_RESIDENTE = list(POWERSHELL) + [
    "Get-Process -ErrorAction SilentlyContinue | "
    "Select-Object Id,WorkingSet64 | "
    "ConvertTo-Csv -NoTypeInformation"
]


def _comando_contadores(clase):
    """Comando que serializa a CSV los contadores de 1 clase WMI de GPU.

    Las columnas son ``Name``, ``DedicatedUsage`` y ``SharedUsage``, con los 2
    usos en bytes. La clase de adaptador usa las mismas columnas y ningún
    contador fuera de los enumerados en `T-012`.
    """
    return list(POWERSHELL) + [
        f"Get-CimInstance -ClassName {clase} | "
        "Select-Object Name,DedicatedUsage,SharedUsage | "
        "ConvertTo-Csv -NoTypeInformation"
    ]


def _ejecutar_comando(comando):
    """Ejecutor real: ejecuta el comando y devuelve su salida estándar.

    La ausencia de la herramienta se propaga como ``FileNotFoundError``, que es
    el caso del código `7` de `DEC-006`; el plazo agotado y el fallo con código
    distinto de `0` se informan como ``ValueError`` con el comando y el motivo,
    de modo que ninguna excepción del módulo `subprocess` llega sin contexto.
    """
    try:
        proceso = subprocess.run(
            comando,
            capture_output=True,
            check=False,
            timeout=TIEMPO_LIMITE_SEGUNDOS,
        )
    except subprocess.TimeoutExpired as error:
        raise ValueError(
            f"{comando[0]}: la consulta no respondió en {TIEMPO_LIMITE_SEGUNDOS} s"
        ) from error
    if proceso.returncode != 0:
        error = (proceso.stderr or b"").decode("utf-8-sig", errors="replace")
        raise ValueError(
            f"{comando[0]}: la consulta terminó con código {proceso.returncode}: "
            f"{error.strip()!r}"
        )
    return (proceso.stdout or b"").decode("utf-8-sig", errors="replace")


def _arbol(pids):
    """Convierte los PID recibidos en 1 conjunto y valida cada identificador."""
    if pids is None:
        raise ValueError("pids: falta la lista de identificadores del árbol")
    arbol = set()
    for pid in pids:
        if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
            raise ValueError(f"pids: el PID {pid!r} no es 1 identificador válido")
        arbol.add(pid)
    if not arbol:
        raise ValueError("pids: la lista del árbol de procesos está vacía")
    return arbol


def _entero(valor, contexto):
    """Convierte 1 campo numérico de CSV y nombra el contexto si no lo es."""
    try:
        return int(str(valor).strip())
    except (TypeError, ValueError):
        raise ValueError(
            f"{contexto}: el valor {valor!r} no es 1 entero"
        ) from None


def _filas(csv_texto, columnas, origen):
    """Lee el CSV de 1 consulta y exige que cada fila declare sus columnas.

    La cabecera sola produce 0 filas. La fila a la que le falta 1 columna del
    contrato se informa como ``ValueError`` con el nombre de esa columna y el
    origen de la consulta, nunca como ``KeyError``.
    """
    lector = csv.DictReader(io.StringIO(csv_texto))
    filas = []
    for fila in lector:
        for columna in columnas:
            if fila.get(columna) is None:
                raise ValueError(
                    f"{origen}: la fila {fila.get('Name') or fila.get('Id') or '?'} "
                    f"no declara la columna {columna!r}"
                )
        filas.append(fila)
    return filas


def _pid_de_nombre(nombre):
    """Devuelve el PID que encabeza 1 nombre de instancia, o `None`.

    El nombre de adaptador no porta PID y el de 1 instancia total tampoco: esas
    filas no pertenecen al árbol y se descartan sin abortar la medición.
    """
    coincidencia = PATRON_PID.match((nombre or "").strip())
    if coincidencia is None:
        return None
    return int(coincidencia.group(1))


def _bytes_de_filas(filas, columna, arbol=None):
    """Suma 1 columna en bytes de las filas, limitada al árbol si se pide.

    Con ``arbol`` se exige que la fila declare ``Name`` con la forma
    ``pid_<n>_luid_...`` y se compara el PID completo; la fila sin PID no se
    atribuye al servidor. Sin ``arbol`` se suman todas las filas recibidas.
    """
    total = 0
    for fila in filas:
        if arbol is not None and _pid_de_nombre(fila["Name"]) not in arbol:
            continue
        total += _entero(fila[columna], f"fila {fila['Name']}: columna {columna}")
    return total


def _bytes_residente(filas, arbol):
    """Suma el `WorkingSet64` en bytes de los PID del árbol.

    `Get-Process` devuelve 1 fila por proceso con su conjunto de trabajo real,
    de modo que 1 PID del árbol sin fila significa que la consulta no midió ese
    proceso: se informa como ``ValueError`` que nombra los PID ausentes y no se
    suma ``0`` en silencio. Las filas de PID ajenos al árbol se descartan y no
    abortan la medición; 1 `WorkingSet64` no entero se informa con su PID.
    """
    total = 0
    vistos = set()
    for fila in filas:
        pid = _entero(fila["Id"], "WorkingSet64: columna Id")
        if pid in arbol:
            total += _entero(fila["WorkingSet64"], f"PID {pid}: columna WorkingSet64")
            vistos.add(pid)
    ausentes = sorted(arbol - vistos)
    if ausentes:
        raise ValueError(
            "WorkingSet64: la consulta no devolvió los PID "
            f"{', '.join(str(pid) for pid in ausentes)} del árbol"
        )
    return total


def _vram(salida):
    """Lee los 3 valores en MiB de la primera línea de la consulta de la GPU."""
    linea = next((texto for texto in salida.splitlines() if texto.strip()), "")
    if not linea:
        raise ValueError(
            "nvidia-smi: la consulta no devolvió la memoria de la GPU dedicada"
        )
    campos = [campo.strip() for campo in linea.split(",")]
    claves = ("vram_total_mib", "vram_usada_mib", "vram_libre_mib")
    if len(campos) < len(claves):
        raise ValueError(
            "nvidia-smi: la consulta no declaró "
            f"{', '.join(claves)}: {linea.strip()!r}"
        )
    return {
        clave: _entero(campo, f"nvidia-smi: columna {clave}")
        for clave, campo in zip(claves, campos)
    }


def _mib(bytes_):
    """Convierte bytes a MiB enteros, sin redondear hacia arriba."""
    return bytes_ // BYTES_POR_MIB


def _vram_libre(salida):
    """Lee la VRAM libre en MiB de la primera línea no vacía de la consulta.

    1 salida vacía o 1 campo no numérico se informan como ``ValueError`` con su
    contexto: el módulo no estima ningún valor. El campo se toma antes de la
    primera coma porque el formato declarado no porta cabecera ni unidades.
    """
    linea = next((texto for texto in salida.splitlines() if texto.strip()), "")
    if not linea:
        raise ValueError(
            "nvidia-smi: la consulta de la VRAM libre no devolvió ningún valor"
        )
    campo = linea.split(",", 1)[0].strip()
    try:
        return float(campo)
    except ValueError:
        raise ValueError(
            f"nvidia-smi: la VRAM libre {campo!r} no es 1 número en MiB"
        ) from None


def vram_libre_mib(*, ejecutor=None):
    """Devuelve la VRAM libre de la GPU dedicada en MiB, o `None` sin herramienta.

    Consulta de solo lectura de `T-068` para la comprobación 4 de `C-9`: ejecuta
    ``COMANDO_VRAM_LIBRE`` y devuelve el valor en MiB como ``float``. Con
    ``FileNotFoundError`` devuelve ``None`` y no consulta otra fuente ni estima
    valor alguno, de modo que la comprobación 4 se reporta `PENDIENTE` con su
    motivo, conforme a `DEC-018`. ``ejecutor`` es el mismo invocable inyectable
    de ``medir_memoria``: el módulo no lanza PowerShell en esta consulta.
    """
    ejecutar = _ejecutar_comando if ejecutor is None else ejecutor
    try:
        salida = ejecutar(list(COMANDO_VRAM_LIBRE))
    except FileNotFoundError:
        return None
    return _vram_libre(salida)


def medir_memoria(pids, *, ejecutor=None):
    """Mide la memoria del servidor y devuelve el resultado de `C-5`.

    Devuelve las 7 claves del contrato con ``codigo`` `0`. Si ``nvidia-smi`` no
    está disponible, devuelve exactamente ``{"codigo": 7}`` y no consulta otra
    fuente ni estima valor alguno. Los errores de entrada se informan como
    ``ValueError`` con la clave o el PID ausente.
    """
    arbol = _arbol(pids)
    ejecutar = _ejecutar_comando if ejecutor is None else ejecutor

    try:
        salida_gpu = ejecutar(list(COMANDO_NVIDIA_SMI))
    except FileNotFoundError:
        return {"codigo": 7}

    resultado = {"codigo": 0}
    resultado.update(_vram(salida_gpu))

    filas_proceso = _filas(
        ejecutar(_comando_contadores(CLASE_PROCESO)),
        COLUMNAS_CONTADORES,
        CLASE_PROCESO,
    )
    if any(_pid_de_nombre(fila["Name"]) in arbol for fila in filas_proceso):
        bytes_desbordamiento = _bytes_de_filas(
            filas_proceso, "SharedUsage", arbol
        )
        contador = CONTADOR_PROCESO
    else:
        filas_adaptador = _filas(
            ejecutar(_comando_contadores(CLASE_ADAPTADOR)),
            COLUMNAS_CONTADORES,
            CLASE_ADAPTADOR,
        )
        bytes_desbordamiento = _bytes_de_filas(filas_adaptador, "SharedUsage")
        contador = CONTADOR_ADAPTADOR

    filas_residente = _filas(
        ejecutar(list(COMANDO_RESIDENTE)),
        COLUMNAS_RESIDENTE,
        "WorkingSet64",
    )
    bytes_residente = _bytes_residente(filas_residente, arbol)

    resultado["residente_mib"] = _mib(bytes_residente)
    resultado["desbordamiento_mib"] = _mib(bytes_desbordamiento)
    resultado["contador_desbordamiento"] = contador
    return resultado
