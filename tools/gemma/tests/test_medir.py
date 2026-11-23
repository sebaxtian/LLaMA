r"""Pruebas en rojo de la medición de memoria de SPEC-017.

Fijan la interfaz de `tools/gemma/medir.py` para `RF-008`, `RNF-003` y
`RNF-007` conforme a `CA-007`, `DEC-006`, `DEC-012` y `DEC-017`, con los
nombres efectivos que el operador local verificó en `T-012` con
`Get-Counter -ListSet 'GPU Process Memory','GPU Adapter Memory'` sobre la
máquina objetivo:

- Proceso: `\GPU Process Memory(*)\Shared Usage` y
  `\GPU Process Memory(*)\Dedicated Usage`, entre otros —la lista quedó
  truncada por el formato de tabla de PowerShell—.
- Adaptador: `\GPU Adapter Memory(*)\Shared Usage`,
  `\GPU Adapter Memory(*)\Dedicated Usage` y
  `\GPU Adapter Memory(*)\Total Committed` —lista completa—.

Consecuencia conforme a `DEC-017`: el nombre
`\GPU Adapter Memory(*)\Non Local Usage` que `DEC-006` mencionaba como
respaldo del reparto no local no está enumerado y se descarta; el respaldo
efectivo del desbordamiento es el `Shared Usage` del conjunto de adaptador.
El contador usado se declara con su nombre efectivo completo en la clave
`contador_desbordamiento` del resultado.

Interfaz que fija esta suite:

- `medir_memoria(pids, *, ejecutor=None) -> dict`, donde `pids` es la lista
  de identificadores del árbol de procesos del servidor y `ejecutor` es 1
  invocable `ejecutor(comando: list[str]) -> str` que devuelve la salida
  estándar del comando y lanza `FileNotFoundError` cuando la herramienta no
  existe. Las pruebas siempre inyectan el doble; el ejecutor real con
  `subprocess` corresponde a `T-020`, y ningún caso de esta suite invoca
  `powershell.exe`, `nvidia-smi` ni proceso real alguno.
- Orden de consulta: (1) `nvidia-smi` con el comando exacto
  `COMANDO_NVIDIA_SMI`; (2) los contadores de proceso por PID con
  `Get-CimInstance` sobre la clase `CLASE_PROCESO`, serializado a CSV con las
  columnas `Name`, `DedicatedUsage`, `SharedUsage` en bytes, donde `Name`
  porta el PID con la forma `pid_<n>_luid_...`; (3) como respaldo, la clase
  `CLASE_ADAPTADOR` con las mismas columnas; (4) la memoria residente con
  `WorkingSet64` de cada PID, serializada a CSV con las columnas `Id`,
  `WorkingSet64` en bytes.
- El doble admite las 2 formas de consulta que `T-020` puede elegir: 1
  consulta global, cuyo CSV completo devuelve y cuyas filas del árbol filtra
  el módulo, o 1 consulta por PID, en cuyo caso el doble devuelve solo las
  filas de los PID citados en el comando. En ambas formas la medición se
  limita al árbol de procesos del servidor.
- La consulta de la memoria residente usa `Get-Process` y no `Win32_Process`,
  conforme a `T-055`: `Get-CimInstance -ClassName Win32_Process` devuelve
  `WorkingSet64` vacío para el proceso `llama-server` en la máquina objetivo,
  mientras que `Get-Process` devuelve el conjunto de trabajo real del mismo
  PID. La magnitud medida sigue siendo el `WorkingSet64` de `DEC-006`: cambia
  solo la vía de consulta. 1 PID del árbol sin fila en la consulta se informa
  como `ValueError` que lo nombra, y 0 PIDs se suman como `0` en silencio.
- Resultado con `ejecutor` disponible: exactamente las 7 claves de
  `CLAVES_RESULTADO`, con `codigo` `0`, los 3 valores de VRAM en MiB tal como
  los entrega la consulta sin unidades, `residente_mib` y
  `desbordamiento_mib` sumados sobre los PID del árbol tras dividir los
  bytes entre `1048576`, y `contador_desbordamiento` con el nombre efectivo
  del contador usado.
- Si `nvidia-smi` no está disponible (`FileNotFoundError`), el resultado es
  exactamente `{"codigo": 7}`, sin ninguna clave de valor y sin estimación
  de valores ausentes, conforme a `DEC-006` y al riesgo del eGPU USB4.

Estas pruebas se ejecutan en rojo mientras `T-020` no escriba el módulo: la
importación de `medir` falla con `ModuleNotFoundError` y cada caso declara el
módulo ausente. Los dobles son puros en memoria; la suite no usa `tempfile`,
no lee `bin/`, `models/` ni la GPU y no escribe archivo alguno, conforme a
`DEC-012`.
"""

import csv
import io
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"

# Árbol de procesos sintético del servidor y 2 PID que no pertenecen a él:
# uno ajeno y otro cuyo nombre contiene el texto del PID 4242 como prefijo.
PIDS = [4242, 4343]
PID_AJENO = 9999
PID_SUPERSTRING = 42421

BYTES_POR_MIB = 1048576

CLASE_PROCESO = "Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory"
CLASE_ADAPTADOR = "Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory"

# Nombres efectivos enumerados por `Get-Counter -ListSet` en `T-012`.
CONTADOR_PROCESO = r"\GPU Process Memory(*)\Shared Usage"
CONTADOR_ADAPTADOR = r"\GPU Adapter Memory(*)\Shared Usage"
# Nombre que `DEC-006` mencionaba como respaldo y que `T-012` no enumeró en
# el conjunto de adaptador: descartado conforme a `DEC-017`.
CONTADOR_DESCARTADO = "Non Local Usage"

COMANDO_NVIDIA_SMI = [
    "nvidia-smi",
    "--query-gpu=memory.total,memory.used,memory.free",
    "--format=csv,noheader,nounits",
]
SALIDA_NVIDIA_SMI = "16376, 14200, 2176"

CLAVES_RESULTADO = {
    "codigo",
    "vram_total_mib",
    "vram_usada_mib",
    "vram_libre_mib",
    "residente_mib",
    "desbordamiento_mib",
    "contador_desbordamiento",
}


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/medir.py` no
    exista, que es el rojo declarado de `T-019`; `T-020` cierra el caso. No
    se crea `tools/gemma/__init__.py`: el módulo se importa como `medir` con
    el directorio `tools/gemma/` en `sys.path`, igual que las suites
    existentes.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import medir

    return medir


def _nombre_proceso(pid):
    """Nombre de instancia de contador con la forma `pid_<n>_luid_...`."""
    return f"pid_{pid}_luid_0x00000000_0x0000ABCD_phys_0"


def _csv_contadores(filas):
    """CSV de contadores con las columnas `Name,DedicatedUsage,SharedUsage`.

    `filas` es 1 lista de tuplas `(Name, DedicatedUsage, SharedUsage)` con
    los 2 usos en bytes; la lista vacía produce el CSV con solo la cabecera.
    """
    buffer = io.StringIO()
    escritor = csv.writer(buffer, lineterminator="\n")
    escritor.writerow(["Name", "DedicatedUsage", "SharedUsage"])
    escritor.writerows(filas)
    return buffer.getvalue()


def _csv_residente(filas):
    """CSV de memoria residente con las columnas `Id,WorkingSet64`.

    `filas` es 1 lista de tuplas `(Id, WorkingSet64)` con el identificador
    de proceso y su conjunto de trabajo en bytes.
    """
    buffer = io.StringIO()
    escritor = csv.writer(buffer, lineterminator="\n")
    escritor.writerow(["Id", "WorkingSet64"])
    escritor.writerows(filas)
    return buffer.getvalue()


def _csv_get_process(filas):
    """CSV con la forma literal que `Get-Process | ConvertTo-Csv` produce.

    `ConvertTo-Csv -NoTypeInformation` cita la cabecera y cada valor, de modo
    que la cabecera de esta consulta es `"Id","WorkingSet64"`. `filas` es 1
    lista de tuplas `(Id, WorkingSet64)` con el conjunto de trabajo en bytes.
    """
    lineas = ['"Id","WorkingSet64"']
    lineas.extend(f'"{pid}","{working_set}"' for pid, working_set in filas)
    return "\n".join(lineas) + "\n"


# Filas del árbol: 512 MiB + 256 MiB de memoria compartida y 2048 MiB +
# 1024 MiB de conjunto de trabajo, todas en bytes exactos.
FILAS_PROCESO_ARBOL = [
    (_nombre_proceso(4242), 14889787392, 536870912),
    (_nombre_proceso(4343), 0, 268435456),
]
FILAS_RESIDENTE_ARBOL = [
    (4242, 2147483648),
    (4343, 1073741824),
]
# Única fila del adaptador: 768 MiB de memoria compartida en bytes.
FILA_ADAPTADOR = ("luid_0x00000000_0x0000ABCD_phys_0", 14889787392, 805306368)


def _tipo_consulta(comando):
    """Clasifica el comando por la fuente que consulta, para fijar el orden."""
    texto = " ".join(comando)
    if comando and "nvidia-smi" in comando[0]:
        return "nvidia-smi"
    if CLASE_PROCESO in texto:
        return "proceso"
    if CLASE_ADAPTADOR in texto:
        return "adaptador"
    if "WorkingSet64" in texto:
        return "residente"
    return "desconocida"


class EjecutorDoble:
    """Doble puro en memoria de `ejecutor(comando: list[str]) -> str`.

    Registra cada comando recibido y devuelve la salida sintética que
    corresponde a la consulta, sin invocar proceso real alguno. Lanza
    `FileNotFoundError` para `nvidia-smi` cuando el caso lo declara ausente.
    Admite las 2 formas de consulta que `T-020` puede elegir: 1 consulta
    global —devuelve el CSV completo y el módulo filtra las filas del
    árbol— o 1 consulta por PID —devuelve solo las filas de los PID citados
    en el comando—. Un comando que no corresponde a ninguna de las 4
    fuentes fijadas es 1 error del doble, no 1 salida silenciosa.
    """

    def __init__(
        self,
        *,
        salida_nvidia_smi=SALIDA_NVIDIA_SMI,
        csv_proceso=None,
        csv_adaptador=None,
        csv_residente=None,
        nvidia_smi_ausente=False,
    ):
        self.salida_nvidia_smi = salida_nvidia_smi
        self.csv_proceso = (
            _csv_contadores(FILAS_PROCESO_ARBOL)
            if csv_proceso is None
            else csv_proceso
        )
        self.csv_adaptador = (
            _csv_contadores([FILA_ADAPTADOR])
            if csv_adaptador is None
            else csv_adaptador
        )
        self.csv_residente = (
            _csv_residente(FILAS_RESIDENTE_ARBOL)
            if csv_residente is None
            else csv_residente
        )
        self.nvidia_smi_ausente = nvidia_smi_ausente
        self.llamadas = []

    def __call__(self, comando):
        comando = list(comando)
        self.llamadas.append(comando)
        texto = " ".join(comando)
        if comando and "nvidia-smi" in comando[0]:
            if self.nvidia_smi_ausente:
                raise FileNotFoundError(
                    2, "No such file or directory", "nvidia-smi"
                )
            return self.salida_nvidia_smi
        if CLASE_PROCESO in texto:
            return self._filtrar(self.csv_proceso, texto, "Name")
        if CLASE_ADAPTADOR in texto:
            return self.csv_adaptador
        if "WorkingSet64" in texto:
            return self._filtrar(self.csv_residente, texto, "Id")
        raise AssertionError(f"comando no reconocido por el doble: {comando!r}")

    def _filtrar(self, csv_texto, texto, columna):
        """Devuelve solo las filas de los PID citados en el comando, si los cita.

        Sin PID citados devuelve el CSV completo: la consulta es global y el
        módulo debe limitar la suma al árbol. La cita se detecta con límite
        de dígito, de modo que `pid_4242` no cita a `pid_42421`.
        """
        lector = csv.DictReader(io.StringIO(csv_texto))
        filas = list(lector)
        if not filas:
            return csv_texto
        if columna == "Name":
            pids = [
                int(re.search(r"pid_(\d+)", fila["Name"]).group(1))
                for fila in filas
            ]
            citados = {
                pid for pid in pids if re.search(rf"pid_{pid}(?!\d)", texto)
            }
        else:
            pids = [int(fila["Id"]) for fila in filas]
            citados = {
                pid
                for pid in pids
                if re.search(rf"(?<!\d){pid}(?!\d)", texto)
            }
        if not citados:
            return csv_texto
        buffer = io.StringIO()
        escritor = csv.writer(buffer, lineterminator="\n")
        escritor.writerow(lector.fieldnames)
        for fila, pid in zip(filas, pids):
            if pid in citados:
                escritor.writerow([fila[campo] for campo in lector.fieldnames])
        return buffer.getvalue()


class MedicionMemoriaTest(unittest.TestCase):
    """Los 8 casos de la fila «Unidad: medición de memoria» de la estrategia."""

    def test_vram_tres_valores_en_mib(self):
        modulo = _cargar_modulo()
        doble = EjecutorDoble()

        resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

        self.assertEqual(CLAVES_RESULTADO, set(resultado))
        self.assertEqual(0, resultado["codigo"])
        self.assertEqual(
            16376,
            resultado["vram_total_mib"],
            "la VRAM total es el primer campo de la consulta sin unidades, en MiB",
        )
        self.assertEqual(
            14200,
            resultado["vram_usada_mib"],
            "la VRAM usada es el segundo campo de la consulta sin unidades, en MiB",
        )
        self.assertEqual(
            2176,
            resultado["vram_libre_mib"],
            "la VRAM libre es el tercer campo de la consulta sin unidades, en MiB",
        )
        self.assertEqual(
            COMANDO_NVIDIA_SMI,
            doble.llamadas[0],
            "la consulta 1 es nvidia-smi con los 3 campos y el formato CSV sin cabecera ni unidades",
        )

    def test_desbordamiento_en_mib_desde_contadores_verificados(self):
        modulo = _cargar_modulo()
        doble = EjecutorDoble(csv_proceso=_csv_contadores(FILAS_PROCESO_ARBOL))

        resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

        self.assertEqual(0, resultado["codigo"])
        self.assertEqual(
            (536870912 + 268435456) // BYTES_POR_MIB,
            resultado["desbordamiento_mib"],
            "el desbordamiento suma el SharedUsage en bytes de los 2 PID del árbol y lo divide entre 1048576",
        )
        self.assertEqual(768, resultado["desbordamiento_mib"])
        self.assertEqual(
            CONTADOR_PROCESO,
            resultado["contador_desbordamiento"],
            "el contador usado es el Shared Usage de proceso enumerado en T-012, con su nombre efectivo completo",
        )
        tipos = [_tipo_consulta(comando) for comando in doble.llamadas]
        self.assertEqual("nvidia-smi", tipos[0])
        self.assertIn("proceso", tipos)
        self.assertIn("residente", tipos)
        self.assertLess(
            tipos.index("proceso"),
            tipos.index("residente"),
            "los contadores de proceso se consultan antes que la memoria residente",
        )
        self.assertNotIn(
            "adaptador",
            tipos,
            "con filas de proceso del árbol no se consulta el respaldo de adaptador",
        )
        consultas = [" ".join(comando) for comando in doble.llamadas]
        self.assertTrue(
            any(
                CLASE_PROCESO in texto and "Get-CimInstance" in texto
                for texto in consultas
            ),
            "la consulta de proceso usa Get-CimInstance sobre la clase verificada",
        )

    def test_contador_de_proceso_ausente_usa_adaptador(self):
        modulo = _cargar_modulo()
        variantes = (
            ("csv vacío", _csv_contadores([])),
            (
                "sin filas del árbol",
                _csv_contadores([(_nombre_proceso(PID_AJENO), 0, 8589934592)]),
            ),
        )
        for etiqueta, csv_proceso in variantes:
            with self.subTest(caso=etiqueta):
                doble = EjecutorDoble(
                    csv_proceso=csv_proceso,
                    csv_adaptador=_csv_contadores([FILA_ADAPTADOR]),
                )

                resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

                self.assertEqual(0, resultado["codigo"])
                self.assertEqual(
                    805306368 // BYTES_POR_MIB,
                    resultado["desbordamiento_mib"],
                    "sin filas de proceso del árbol el desbordamiento es el SharedUsage del adaptador convertido a MiB",
                )
                self.assertEqual(768, resultado["desbordamiento_mib"])
                self.assertEqual(
                    CONTADOR_ADAPTADOR,
                    resultado["contador_desbordamiento"],
                    "el respaldo efectivo es el Shared Usage del conjunto de adaptador enumerado en T-012",
                )
                self.assertNotIn(
                    CONTADOR_DESCARTADO,
                    resultado["contador_desbordamiento"],
                    "Non Local Usage del adaptador no está enumerado en T-012 y se descarta conforme a DEC-017",
                )
                tipos = [_tipo_consulta(comando) for comando in doble.llamadas]
                self.assertIn("proceso", tipos)
                self.assertIn("adaptador", tipos)
                self.assertLess(
                    tipos.index("proceso"),
                    tipos.index("adaptador"),
                    "el respaldo de adaptador se consulta después del conjunto de proceso",
                )
                for comando in doble.llamadas:
                    texto = " ".join(comando)
                    if CLASE_ADAPTADOR in texto:
                        self.assertNotIn("Non Local Usage", texto)
                        self.assertNotIn("NonLocalUsage", texto)

    def test_residente_en_mib(self):
        modulo = _cargar_modulo()
        doble = EjecutorDoble(
            csv_residente=_csv_residente(
                [(4242, 3221225472), (4343, 536870912)]
            )
        )

        resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

        self.assertEqual(0, resultado["codigo"])
        self.assertEqual(
            (3221225472 + 536870912) // BYTES_POR_MIB,
            resultado["residente_mib"],
            "la residente suma el WorkingSet64 en bytes de los PID del árbol y lo divide entre 1048576",
        )
        self.assertEqual(3584, resultado["residente_mib"])
        consultas = [" ".join(comando) for comando in doble.llamadas]
        self.assertTrue(
            any("WorkingSet64" in texto for texto in consultas),
            "la memoria residente se consulta con WorkingSet64 de cada PID del árbol",
        )

    def test_herramienta_ausente_codigo_7(self):
        modulo = _cargar_modulo()
        doble = EjecutorDoble(nvidia_smi_ausente=True)

        resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

        self.assertEqual(
            {"codigo": 7},
            resultado,
            "sin nvidia-smi el resultado es exactamente codigo 7, sin ninguna clave de valor declarada (DEC-006)",
        )
        self.assertEqual(
            1,
            len(doble.llamadas),
            "la ausencia de la herramienta corta la medición: no se consulta otra fuente ni se estima valor alguno",
        )

    def test_pid_ajeno_no_se_suma(self):
        modulo = _cargar_modulo()
        filas_proceso = FILAS_PROCESO_ARBOL + [
            (_nombre_proceso(PID_AJENO), 0, 8589934592),
            (_nombre_proceso(PID_SUPERSTRING), 0, 4294967296),
        ]
        filas_residente = FILAS_RESIDENTE_ARBOL + [
            (PID_AJENO, 17179869184),
            (PID_SUPERSTRING, 8589934592),
        ]
        doble = EjecutorDoble(
            csv_proceso=_csv_contadores(filas_proceso),
            csv_residente=_csv_residente(filas_residente),
        )

        resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

        self.assertEqual(0, resultado["codigo"])
        self.assertEqual(
            768,
            resultado["desbordamiento_mib"],
            "solo el SharedUsage de los PID del árbol: la paginación del escritorio no se atribuye al servidor",
        )
        self.assertEqual(
            3072,
            resultado["residente_mib"],
            "solo el WorkingSet64 de los PID del árbol, sin el PID ajeno ni el que contiene su texto como prefijo",
        )

    def test_residente_desde_get_process(self):
        modulo = _cargar_modulo()
        doble = EjecutorDoble(
            csv_residente=_csv_get_process(FILAS_RESIDENTE_ARBOL)
        )

        resultado = modulo.medir_memoria(PIDS, ejecutor=doble)

        self.assertEqual(0, resultado["codigo"])
        self.assertEqual(
            (2147483648 + 1073741824) // BYTES_POR_MIB,
            resultado["residente_mib"],
            "el CSV de Get-Process con las columnas Id y WorkingSet64 produce la residente de los PID del árbol en MiB",
        )
        self.assertEqual(3072, resultado["residente_mib"])
        consultas = [" ".join(comando) for comando in doble.llamadas]
        residentes = [texto for texto in consultas if "WorkingSet64" in texto]
        self.assertTrue(
            residentes,
            "la memoria residente se consulta con la magnitud WorkingSet64 de cada PID del árbol",
        )
        for texto in residentes:
            self.assertIn(
                "Get-Process",
                texto,
                "la residente se consulta con Get-Process, que devuelve el WorkingSet64 real del PID en la máquina objetivo",
            )
        for texto in consultas:
            self.assertNotIn(
                "Win32_Process",
                texto,
                "0 comandos de la medición consultan Win32_Process, cuyo WorkingSet64 llega vacío para llama-server",
            )

    def test_pid_del_arbol_ausente_falla(self):
        modulo = _cargar_modulo()
        doble = EjecutorDoble(
            csv_residente=_csv_get_process([(4242, 2147483648)])
        )

        with self.assertRaises(ValueError) as capturado:
            modulo.medir_memoria(PIDS, ejecutor=doble)

        mensaje = str(capturado.exception)
        self.assertIn(
            "4343",
            mensaje,
            "el ValueError nombra el PID del árbol que la consulta no devolvió, en lugar de sumar 0 en silencio",
        )


if __name__ == "__main__":
    unittest.main()
