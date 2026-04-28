#!/usr/bin/env bash
# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 20:41

# Interrompe a execução caso ocorra algum erro
set -o errexit

# 1. Instala as bibliotecas do Python
pip install -r requirements.txt

# 2. Baixa e instala o navegador Chromium e suas dependências no servidor
playwright install chromium --with-deps
