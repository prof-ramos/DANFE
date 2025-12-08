# =============================================================================
# DANFE Generator - Dockerfile
# =============================================================================
# Multi-stage build otimizado para aplicação Streamlit
# Imagem final ~300MB com todas as dependências necessárias
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder - Instala dependências em ambiente isolado
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS builder

# Evita prompts interativos e define encoding
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Instala dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas arquivos necessários para instalação
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Cria virtual environment e instala dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instala o pacote com dependências web
RUN pip install --no-cache-dir ".[web]"

# -----------------------------------------------------------------------------
# Stage 2: Runtime - Imagem final otimizada
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

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

# Cria usuário não-root para segurança
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copia virtual environment do builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia código fonte
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup .streamlit/ ./.streamlit/

# Cria diretórios para dados e outputs
RUN mkdir -p /app/data /app/output && \
    chown -R appuser:appgroup /app

# Muda para usuário não-root
USER appuser

# Expõe porta do Streamlit
EXPOSE 8501

# Healthcheck para orquestradores como K8s/Docker Compose
# Usa Python em vez de curl (não disponível na imagem slim)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Comando de inicialização com graceful shutdown
# Usa exec para que sinais sejam propagados corretamente
# Flags de servidor configuradas via ENV acima (STREAMLIT_SERVER_*)
CMD ["streamlit", "run", "src/danfe_generator/web/app.py"]
