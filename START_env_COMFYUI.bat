@echo off
title ComfyUI Virtual Environment
cd /d C:\ComfyUI
call C:\ComfyUI\.venv\Scripts\activate.bat
echo.
echo ====================================
echo   ComfyUI Environment - READY!
echo ====================================
echo.
echo Python: 
python --version
echo.
cmd /k