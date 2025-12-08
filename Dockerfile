# =============================================================================
# DANFE Generator - Dockerfile
# =============================================================================
# Multi-stage build otimizado com uv para instalação ultra-rápida
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder - Instala dependências com uv
# -----------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Configurações do uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /build

# Copia arquivos de dependência
COPY pyproject.toml README.md ./

# Instala dependências em um venv isolado
# --no-dev: Apenas dependências de produção
ENV VIRTUAL_ENV=/opt/venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv && \
    uv pip install --no-cache ".[web]"

# -----------------------------------------------------------------------------
# Stage 2: Runtime - Imagem final leve
# -----------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runtime

# Metadata
LABEL maintainer="Gabriel Ramos" \
    version="0.3.0" \
    description="DANFE Generator - Gerador de DANFE para NF-e brasileira"

# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    # Streamlit config
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_THEME_BASE=light \
    # App config
    STREAMLIT_ENV=production

WORKDIR /app

# Cria usuário não-root
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copia virtual environment do builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia código fonte
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup .streamlit/ ./.streamlit/

# Cria diretórios necessários
RUN mkdir -p /app/data /app/output && \
    chown -R appuser:appgroup /app

# Muda para usuário não-root
USER appuser

# Expõe porta
EXPOSE 8501

# Healthcheck (Python-based)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Comando de inicialização
CMD ["streamlit", "run", "src/danfe_generator/web/app.py"]
