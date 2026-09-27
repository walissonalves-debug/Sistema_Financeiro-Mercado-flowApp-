@echo off
title MercadoFlow - Servidor
echo.
echo  ==========================================
echo   MercadoFlow - Iniciando servidor...
echo  ==========================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERRO: Python nao encontrado!
    echo  Baixe em: https://www.python.org/downloads/
    pause
    exit
)

REM Instala Flask se necessario
echo  Verificando dependencias...
python -m pip install flask -q

echo.
echo  Servidor rodando em: http://localhost:5000
echo  Para encerrar: feche esta janela ou Ctrl+C
echo.

REM Abre o navegador automaticamente
timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Inicia o servidor
python app.py

pause
