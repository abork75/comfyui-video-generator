@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   QUICK GIT PUSH
echo ========================================
echo.

REM Sprawdź status
git status

echo.
echo ========================================
echo   Dodawanie zmian...
echo ========================================

REM Dodaj wszystkie zmiany
git add .

echo.
set /p commit_msg="Commit message: "

REM Commit z wiadomością
git commit -m "%commit_msg%"

echo.
echo ========================================
echo   Wysyłanie na GitHub...
echo ========================================

REM Push
git push

echo.
echo ========================================
echo   ✓ GOTOWE!
echo ========================================
echo.
pause