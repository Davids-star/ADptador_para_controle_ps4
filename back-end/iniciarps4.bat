@echo off
title Servidor de Controle PS4

echo ==============================================================
echo      INICIANDO O SERVIDOR
echo ==============================================================
echo.

IF EXIST ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo Verificando dependencias do Python...
pip install vgamepad websockets python-dotenv qrcode colorama psutil >nul 2>&1

echo.
echo Concluido! Iniciando Motor do Roteador...
echo.

python back-end\serve.py

pause
