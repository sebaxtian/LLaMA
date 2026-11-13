# Plan técnico - SPEC-001

## Referencias

- `spec.md`: `SPEC-001`.
- `clarify.md`: `SPEC-001`.

## Arquitectura de módulos

Un único script `main.bat` en la raíz del proyecto con un bucle de menú:

1. Resolver la raíz con `%~dp0`.
2. Descubrir los archivos `.bat` del primer nivel de `src/` en orden alfabético.
3. Mostrar menú numerado con la opción de salida.
4. Leer la entrada del usuario y validarla.
5. Ejecutar el script elegido con `call` y volver al menú, o salir.

## Esquemas, tipos e interfaces

- `ROOT`: ruta de la raíz derivada de `%~dp0`.
- `SRC_DIR`: `%ROOT%\src`.
- Lista de scripts: índice numérico 1..N mapeado a cada ruta `.bat` descubierta.
- Entrada: entero entre 1 y N, o la tecla de salida.

## Decisiones técnicas

### DEC-001

- **Decisión:** usar `set /p` para leer la entrada numérica, en lugar de `choice`, porque el número de opciones es variable.
- **Alternativas descartadas:** `choice /c` limita a un conjunto fijo de teclas y no escala con N.

### DEC-002

- **Decisión:** descubrir con `for /f "delims=" %%f in ('dir /b /o:n "src\*.bat"')` para garantizar orden alfabético.
- **Alternativas descartadas:** `for %%f in (src\*.bat)` no garantiza orden estable.

### DEC-003

- **Decisión:** ejecutar el script con `call "%script%"` para que el control retorne al menú.
- **Alternativas descartadas:** invocar sin `call` terminaría el menú.

## Estrategia de testing

- Validación manual en Windows 11.
- Prueba de humo: crear un `.bat` temporal en `src/`, verificar que `main.bat` lo lista, lo ejecuta y retorna al menú.
- Verificar casos borde: `src/` vacío, entrada inválida, nombre con espacios y código de salida distinto de cero.

## Matriz de cobertura

| Requisito | Componente | Prueba / comando |
|---|---|---|
| RF-001 | descubrimiento | listar `.bat` de `src/` en orden |
| RF-002 | ejecución | `call` del script elegido |
| RF-003 | menú | opción de salida |
| RF-004 | validación | entrada inválida -> error y re-solicitar |
| RF-005 | menú | `src/` sin `.bat` -> mensaje y salir |
| RF-006 | bucle | retorno al menú tras ejecutar |
| RNF-001 | raíz | `%~dp0` |
| RNF-002 | ejecución | verificar existencia antes de `call` |
| CB-001 | menú | `src/` vacío |
| CB-002 | ejecución | ruta citada con espacios |
| CB-003 | bucle | código de salida distinto de cero |