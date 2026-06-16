@echo off
cd /d "%~dp0"

echo.
echo  ============================================
echo   ComfyUI Video Generator - TRYB DEV
echo  ============================================
echo.
echo  UWAGA: --reload restartuje serwer przy zmianach plikow.
echo  Nie generuj filmow w tym trybie - restart przerwie generowanie!
echo.

:: Aktywuj .streamlit_env
if exist "..\\.streamlit_env\\Scripts\\activate.bat" (
    echo  [*] Aktywowanie .streamlit_env...
    call "..\\.streamlit_env\\Scripts\\activate.bat"
) else if exist "venv\\Scripts\\activate.bat" (
    call venv\\Scripts\\activate.bat
)

echo  [*] Uruchamianie serwera DEV na http://127.0.0.1:8001
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

pause
