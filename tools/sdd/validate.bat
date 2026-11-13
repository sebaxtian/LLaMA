@echo off
setlocal
REM Validador SDD del proyecto LLaMA.
REM Resuelve la ruta del script mediante %~dp0 para funcionar desde cualquier directorio.

set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%validate.py" %*

exit /b %errorlevel%
