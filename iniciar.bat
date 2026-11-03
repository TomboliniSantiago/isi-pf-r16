@echo off
rem Levanta el backend (FastAPI) y el frontend (Vite) de EugenIA en esta misma ventana.
rem Al cerrar la ventana o presionar Ctrl+C se detienen los dos.
setlocal
chcp 65001 >nul
title EugenIA - Backend + Frontend

set "RAIZ=%~dp0"
set "BACK=%RAIZ%backend"
set "FRONT=%RAIZ%frontend"
set "PUERTO_BACK=8000"

if not exist "%BACK%\.venv\Scripts\python.exe" (
    echo No se encontró el entorno virtual del backend en backend\.venv
    echo Crearlo con:  cd backend  y luego  py -3.12 -m venv .venv  y  .venv\Scripts\python -m pip install -r requirements-dev.txt
    pause
    exit /b 1
)
if not exist "%BACK%\.env" (
    echo Falta backend\.env. Copiar backend\.env.example a backend\.env y completarlo.
    pause
    exit /b 1
)
where npm >nul 2>nul
if errorlevel 1 (
    echo No se encontró npm. Instalar Node.js 20 desde https://nodejs.org
    pause
    exit /b 1
)
if not exist "%FRONT%\node_modules" (
    echo Instalando dependencias del frontend...
    pushd "%FRONT%"
    call npm install
    popd
)

echo Backend:  http://localhost:%PUERTO_BACK%/docs
echo Frontend: http://localhost:5173
echo Para detener ambos: cerrar esta ventana o presionar Ctrl+C.
echo.

rem Backend en segundo plano dentro de esta consola: comparte su ciclo de vida.
start "" /B /D "%BACK%" ".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port %PUERTO_BACK%

rem Frontend en primer plano: el script queda aquí hasta que Vite termina.
pushd "%FRONT%"
call npm run dev -- --open
popd

rem Si Vite terminó por su cuenta (error o Ctrl+C), se detiene también el backend.
rem Se busca el proceso que escucha en el puerto (dirección remota 0.0.0.0:0), sin depender del idioma de Windows.
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /R /C:"127\.0\.0\.1:%PUERTO_BACK%  *0\.0\.0\.0:0 "') do (
    taskkill /F /T /PID %%p >nul 2>nul
)
echo Backend y frontend detenidos.
