"""Lector acotado de los metadatos de 1 archivo GGUF de SPEC-017.

Implementa la señal de lectura de `DEC-004` y la reserva de `DEC-016`: el
llamador obtiene el nombre declarado (`general.name`), el tipo de archivo
(`general.file_type`) y el tamaño exacto en bytes, sin recorrer los tensores ni
cargar los pesos. La lectura se detiene al terminar el bloque de metadatos, de
modo que el costo es independiente del tamaño de los pesos y cabe en el margen
de `RNF-001`.

Contrato:

- ``leer_metadatos(ruta)`` devuelve 1 diccionario con exactamente las claves
  ``nombre``, ``file_type`` y ``tamano_bytes``.
- ``nombre`` es el valor de ``general.name`` como texto, o ``None`` si la clave
  falta o no declara 1 texto.
- ``file_type`` es el valor entero de ``general.file_type``, o ``None`` si la
  clave falta o su tipo no es 1 entero; ``DEC-016`` interpreta ese ``None`` como
  señal no concluyente y exige las 2 señales de reserva.
- ``tamano_bytes`` es el tamaño exacto del archivo en bytes.

Claves duplicadas: el formato no prohíbe repetir 1 clave y la lectura no aborta
por ello; prevalece el **último** valor declarado en el bloque de metadatos, que
es el criterio de sobrescritura que aplican los lectores del formato al asignar
sobre el mapa de claves.

Límites de lectura: ninguna lectura puede exceder el tamaño del archivo, así que
antes de consumir bytes se contrasta la cantidad pedida con lo que resta del
archivo. Esa comprobación, aplicada también a la longitud de 1 texto, al
recuento de 1 arreglo y al tamaño de 1 elemento de arreglo, evita reservar
memoria por 1 longitud declarada y corrupta. Toda firma ausente, truncamiento o
metadato ilegible se envuelve en ``ErrorGGUF``, cuyo mensaje nombra la ruta, de
modo que no se propaga 1 ``struct.error``, 1 ``UnicodeDecodeError`` ni 1
``MemoryError`` sin contexto.
"""

from __future__ import annotations

import struct
from pathlib import Path

__all__ = ["ErrorGGUF", "leer_metadatos"]

# Firma que abre todo archivo del formato.
FIRMA_GGUF = b"GGUF"

# Versión mínima admitida: desde la versión 2 los 2 recuentos de la cabecera son
# de 64 bits; la versión 1 usaba recuentos de 32 bits y no se lee aquí.
VERSION_MINIMA = 2

# Tipos de valor del bloque de metadatos y su tamaño fijo en bytes.
TIPO_UINT8 = 0
TIPO_INT8 = 1
TIPO_UINT16 = 2
TIPO_INT16 = 3
TIPO_UINT32 = 4
TIPO_INT32 = 5
TIPO_FLOAT32 = 6
TIPO_BOOL = 7
TIPO_STRING = 8
TIPO_ARRAY = 9
TIPO_UINT64 = 10
TIPO_INT64 = 11
TIPO_FLOAT64 = 12

TAMANO_FIJO = {
    TIPO_UINT8: 1,
    TIPO_INT8: 1,
    TIPO_UINT16: 2,
    TIPO_INT16: 2,
    TIPO_UINT32: 4,
    TIPO_INT32: 4,
    TIPO_FLOAT32: 4,
    TIPO_BOOL: 1,
    TIPO_UINT64: 8,
    TIPO_INT64: 8,
    TIPO_FLOAT64: 8,
}

# Formato de desempaquetado de los tipos enteros que el contrato devuelve.
FORMATO_ENTERO = {
    TIPO_UINT8: "<B",
    TIPO_INT8: "<b",
    TIPO_UINT16: "<H",
    TIPO_INT16: "<h",
    TIPO_UINT32: "<I",
    TIPO_INT32: "<i",
    TIPO_UINT64: "<Q",
    TIPO_INT64: "<q",
}

# Bytes mínimos que consume 1 elemento de arreglo: los tipos de tamaño fijo usan
# su tamaño y 1 texto usa al menos los 8 bytes de su longitud.
TAMANO_ELEMENTO_ARREGLO = dict(TAMANO_FIJO)
TAMANO_ELEMENTO_ARREGLO[TIPO_STRING] = 8

# Bytes mínimos que consume 1 par clave-valor: longitud de la clave en 8 bytes,
# el tipo en 4 y al menos 1 byte de valor.
MINIMO_PAR_METADATO = 13

CLAVE_NOMBRE = "general.name"
CLAVE_FILE_TYPE = "general.file_type"


class ErrorGGUF(ValueError):
    """Archivo GGUF ilegible; el mensaje nombra la ruta y la causa."""


class _Lector:
    """Cursores de lectura sobre 1 archivo con el presupuesto de bytes restante."""

    def __init__(self, archivo, ruta, tamano_bytes):
        self._archivo = archivo
        self.ruta = ruta
        self.restante = tamano_bytes

    def _error(self, detalle, causa=None):
        error = ErrorGGUF(f"{self.ruta}: {detalle}")
        if causa is not None:
            raise error from causa
        raise error

    def leer(self, cantidad):
        """Lee exactamente `cantidad` bytes o falla con la ruta en el mensaje."""
        if cantidad < 0 or cantidad > self.restante:
            self._error(
                f"lectura de {cantidad} bytes excedida: restan {self.restante} bytes del archivo"
            )
        try:
            crudo = self._archivo.read(cantidad)
        except (OSError, MemoryError) as exc:
            self._error(f"lectura de {cantidad} bytes fallida", exc)
        if len(crudo) != cantidad:
            self._error(
                f"archivo truncado: se esperaban {cantidad} bytes y se leyeron {len(crudo)}"
            )
        self.restante -= cantidad
        return crudo

    def entero(self, formato, cantidad):
        try:
            return struct.unpack(formato, self.leer(cantidad))[0]
        except struct.error as exc:  # defensa: el tamaño ya está acotado
            self._error(f"entero de {cantidad} bytes ilegible", exc)

    def u32(self):
        return self.entero("<I", 4)

    def u64(self):
        return self.entero("<Q", 8)

    def texto(self):
        longitud = self.u64()
        crudo = self.leer(longitud)
        try:
            return crudo.decode("utf-8")
        except UnicodeDecodeError as exc:
            self._error(f"texto de metadatos de {longitud} bytes con UTF-8 no válido", exc)

    def valor(self, tipo, clave=""):
        """Consume 1 valor del bloque de metadatos y devuelve su contenido legible."""
        tamano = TAMANO_FIJO.get(tipo)
        if tamano is not None:
            crudo = self.leer(tamano)
            if tipo == TIPO_BOOL:
                return crudo != b"\x00"
            formato = FORMATO_ENTERO.get(tipo)
            if formato is None:  # FLOAT32 y FLOAT64 no se interpretan
                return None
            return struct.unpack(formato, crudo)[0]
        if tipo == TIPO_STRING:
            return self.texto()
        if tipo == TIPO_ARRAY:
            return self.arreglo(clave)
        self._error(f"tipo de valor desconocido {tipo} en la clave '{clave}'")

    def arreglo(self, clave):
        tipo_elemento = self.u32()
        tamano_elemento = TAMANO_ELEMENTO_ARREGLO.get(tipo_elemento)
        if tamano_elemento is None:
            self._error(
                f"tipo de elemento desconocido {tipo_elemento} en el arreglo de la clave '{clave}'"
            )
        numero = self.u64()
        if numero > self.restante // tamano_elemento:
            self._error(
                f"arreglo de la clave '{clave}' con {numero} elementos excedido: "
                f"restan {self.restante} bytes del archivo"
            )
        for _ in range(numero):
            self.valor(tipo_elemento, clave)
        return None


def _leer_cabecera(lector):
    """Lee firma, versión y los 2 recuentos de la cabecera."""
    firma = lector.leer(len(FIRMA_GGUF))
    if firma != FIRMA_GGUF:
        lector._error(f"firma del formato ausente: se esperaba {FIRMA_GGUF!r} y se leyó {firma!r}")
    version = lector.u32()
    if version < VERSION_MINIMA:
        lector._error(
            f"versión del formato {version} no admitida: se requiere la versión {VERSION_MINIMA} o posterior"
        )
    lector.u64()  # recuento de tensores: los tensores no se recorren
    numero_claves = lector.u64()  # pares clave-valor del bloque de metadatos
    if numero_claves > lector.restante // MINIMO_PAR_METADATO:
        lector._error(
            f"bloque de metadatos con {numero_claves} pares excedido: "
            f"restan {lector.restante} bytes del archivo"
        )
    return numero_claves


def leer_metadatos(ruta):
    """Devuelve `nombre`, `file_type` y `tamano_bytes` del archivo indicado.

    Solo se leen la cabecera y el bloque de metadatos: los tensores y los pesos
    quedan fuera de la lectura. Cualquier firma ausente, truncamiento o metadato
    ilegible produce `ErrorGGUF`, que es 1 `ValueError` y nombra la ruta.
    """
    ruta = Path(ruta)
    try:
        tamano_bytes = ruta.stat().st_size
    except OSError as exc:
        raise ErrorGGUF(f"{ruta}: no se puede leer el tamaño del archivo: {exc}") from exc

    nombre = None
    file_type = None
    try:
        with open(ruta, "rb") as archivo:
            lector = _Lector(archivo, ruta, tamano_bytes)
            numero_claves = _leer_cabecera(lector)
            for _ in range(numero_claves):
                clave = lector.texto()
                tipo = lector.u32()
                contenido = lector.valor(tipo, clave)
                if clave == CLAVE_NOMBRE:
                    nombre = contenido if isinstance(contenido, str) else None
                elif clave == CLAVE_FILE_TYPE:
                    if isinstance(contenido, int) and not isinstance(contenido, bool):
                        file_type = contenido
                    else:
                        file_type = None
    except ErrorGGUF:
        raise
    except (OSError, MemoryError, struct.error, UnicodeDecodeError, RecursionError) as exc:
        raise ErrorGGUF(f"{ruta}: lectura de metadatos GGUF fallida: {exc}") from exc

    return {"nombre": nombre, "file_type": file_type, "tamano_bytes": tamano_bytes}
