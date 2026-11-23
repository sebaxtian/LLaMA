@echo off
rem ==============================================================================
rem Lanzador de SPEC-017 del modelo Gemma-4-26B-A4B-it-qat-GGUF.
rem Resuelve la raiz desde la ubicacion del propio archivo con %~dp0 y el
rem interprete con las 3 vias de DEC-015: no depende del directorio actual ni del
rem PATH. Toda decision sobre perfiles, artefactos y comprobaciones corresponde a
rem tools\gemma\lanzador.py (DEC-001, DEC-014).
rem ==============================================================================
setlocal EnableExtensions

rem Raiz del repositorio: este archivo vive en src\gemma\, 2 niveles debajo.
for %%R in ("%~dp0..\..") do set "RAIZ=%%~fR"

set "PYTHON="
set "PY_ARGS="
set "VIA="

rem Via 1 de DEC-015: LLAMA_PYTHON, solo si la ruta que declara existe.
if defined LLAMA_PYTHON if exist "%LLAMA_PYTHON%" (
  set "PYTHON=%LLAMA_PYTHON%"
  set "VIA=LLAMA_PYTHON"
)

rem Via 2 de DEC-015: py.exe del sistema con -3, sin busqueda en el PATH.
if not defined PYTHON if exist "%SystemRoot%\py.exe" (
  set "PYTHON=%SystemRoot%\py.exe"
  set "PY_ARGS=-3"
  set "VIA=py -3"
)

rem Via 3 de DEC-015: python.exe bajo %LOCALAPPDATA%\Programs\Python\Python3*,
rem de la version mas alta a la mas baja. El patron Python3?? cubre las versiones
rem con menor de 2 digitos (3.10 en adelante) y Python3? las de 1 digito (3.9);
rem la ultima coincidencia de cada patron es la version mas alta.
if not defined PYTHON (
  for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3??") do (
    if exist "%%D\python.exe" (
      set "PYTHON=%%D\python.exe"
      set "VIA=LOCALAPPDATA\Programs\Python"
    )
  )
  if not defined PYTHON for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3?") do (
    if exist "%%D\python.exe" (
      set "PYTHON=%%D\python.exe"
      set "VIA=LOCALAPPDATA\Programs\Python"
    )
  )
)

rem Las 3 vias fallaron: se informa y se devuelve el codigo 8 de C-8 sin invocar
rem el orquestador ni ejecutar comprobacion alguna.
if not defined PYTHON (
  >&2 echo [ERROR] intérprete no disponible
  >&2 echo Vias comprobadas: LLAMA_PYTHON, %SystemRoot%\py.exe -3, %LOCALAPPDATA%\Programs\Python\Python3*
  exit /b 8
)

for %%P in ("%PYTHON%") do set "PYTHON=%%~fP"
echo Intérprete: %PYTHON% (%VIA%)

rem Delegacion en el orquestador con la raiz absoluta y los argumentos recibidos:
rem el codigo del orquestador se devuelve sin reinterpretarlo.
"%PYTHON%" %PY_ARGS% "%RAIZ%\tools\gemma\lanzador.py" --raiz "%RAIZ%" %*
exit /b %errorlevel%
