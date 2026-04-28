#!/usr/bin/env bash
# NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 20:49

# Interrompe a execução caso ocorra algum erro
set -o errexit

# 1. Instala as bibliotecas do Python
pip install -r requirements.txt

# 2. Baixa e instala APENAS o navegador Chromium no nível do usuário
# A remoção do '--with-deps' evita o bloqueio de permissão root (sudo) do Render
playwright install chromium
