@echo off
title GPU VRAM Monitor - RTX 3060 12GB
color 0A
echo ╔═══════════════════════════════════════╗
echo ║     GPU VRAM MONITORING TOOL          ║
echo ║     Press Ctrl+C to stop              ║
echo ╚═══════════════════════════════════════╝
echo.
nvidia-smi --query-gpu=timestamp,memory.used,memory.total,temperature.gpu --format=csv -l 1
pause