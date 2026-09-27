#!/bin/bash
echo ""
echo "=========================================="
echo "  MercadoFlow - Iniciando servidor..."
echo "=========================================="
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não encontrado!"
    echo "Instale com: sudo apt install python3 (Linux)"
    echo "Ou baixe em: https://www.python.org/downloads/ (Mac)"
    exit 1
fi

# Instala Flask se necessário
echo "Verificando dependências..."
python3 -m pip install flask -q

echo ""
echo "Servidor rodando em: http://localhost:5000"
echo "Para encerrar: Ctrl+C"
echo ""

# Abre o navegador (tenta diferentes comandos)
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 &
elif command -v open &> /dev/null; then
    open http://localhost:5000 &
fi

# Inicia servidor
python3 app.py
