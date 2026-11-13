@echo off
setlocal EnableDelayedExpansion

rem Menu principal del proyecto LLaMA.
rem Resuelve la raiz con %~dp0 y no depende del directorio actual ni del PATH.

set "ROOT=%~dp0"
set "SRC=%ROOT%src"

:menu
echo.
echo ==========================================
echo   LLaMA - Menu principal
echo ==========================================
echo.

set /a N=0
for /f "delims=" %%F in ('dir /b /o:n "%SRC%\*.bat" 2^>nul') do (
    set /a N+=1
    set "F!N!=%%F"
    echo   [!N!] %%F
)

if %N% EQU 0 goto :no_scripts

echo.
echo   [0] Salir
echo.
set "OPT="
set /p "OPT=Seleccione una opcion: "

if "%OPT%"=="0" goto :fin

rem Validar que OPT es un numero entero.
set "ISNUM="
for /f "delims=0123456789" %%D in ("%OPT%") do set "ISNUM=0"
if defined ISNUM goto :invalid
if "%OPT%"=="" goto :invalid

rem Validar rango 1..N.
if %OPT% LSS 1 goto :invalid
if %OPT% GTR %N% goto :invalid

rem Resolver el archivo seleccionado.
set "TARGET=%SRC%\!F%OPT%!"
if not exist "%TARGET%" goto :missing

echo.
echo Ejecutando: %TARGET%
echo.
call "%TARGET%"
echo.
echo El script termino con codigo de salida %errorlevel%.
echo.
goto :menu

:invalid
echo.
echo Opcion no valida.
echo.
goto :menu

:missing
echo.
echo El script seleccionado no existe.
echo.
goto :menu

:no_scripts
echo No hay scripts disponibles en src\.
echo.
echo   [0] Salir
echo.
set "OPT="
set /p "OPT=Presione 0 para salir: "
if not "%OPT%"=="0" goto :no_scripts
goto :fin

:fin
endlocal
exit /b 0