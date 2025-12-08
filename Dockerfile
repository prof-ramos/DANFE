# Use Python 3.12
FROM python:3.12-slim

# Set up user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies if needed (e.g. for some python packages)
# USER root
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*
# USER user

# Copy requirements
COPY --chown=user ./requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY --chown=user . /app

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Run Streamlit
# Note: server.address=0.0.0.0 is crucial for Docker
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
