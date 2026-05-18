@echo off
cd /d "%~dp0"

echo.
echo  ============================================
echo   ComfyUI Video Generator - Web App
echo  ============================================
echo.

:: Aktywuj .streamlit_env (główne środowisko projektu)
if exist "..\\.streamlit_env\\Scripts\\activate.bat" (
    echo  [*] Aktywowanie .streamlit_env...
    call "..\\.streamlit_env\\Scripts\\activate.bat"
) else if exist "venv\\Scripts\\activate.bat" (
    echo  [*] Aktywowanie venv...
    call venv\\Scripts\\activate.bat
)

:: Sprawdź czy FastAPI jest zainstalowane
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo  [!] Brak zaleznosci. Instalowanie...
    pip install -r requirements_app.txt
    echo.
)

echo  [*] Uruchamianie serwera na http://0.0.0.0:8000
echo  [*] Lokalnie:  http://127.0.0.1:8000
echo  [*] Sieciowo:  http://%COMPUTERNAME%:8000
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
