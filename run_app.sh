#!/bin/bash
# Script para executar a aplicação web Streamlit

set -e

# Ativar venv se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Executar Streamlit
streamlit run src/danfe_generator/web/app.py "$@"
