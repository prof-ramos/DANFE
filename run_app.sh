#!/bin/bash
# Script para executar a aplicação web Streamlit

set -e

# Executar Streamlit via uv run (gerencia venv automaticamente)
uv run streamlit run src/danfe_generator/web/app.py "$@"
