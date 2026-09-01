FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy configuration and source files
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY examples/ ./examples/

# Upgrade pip and install package
RUN pip install --upgrade pip && \
    pip install .

ENTRYPOINT ["odc"]
CMD ["--help"]
