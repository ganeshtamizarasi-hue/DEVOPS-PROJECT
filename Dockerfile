# ── Stage 1: Install dependencies ────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Lean runtime image ───────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="devops-team" \
      version="1.0" \
      description="FastAPI DevOps CI/CD Application"

# Non-root user
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser

WORKDIR /code

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application
COPY --chown=appuser:appgroup main.py .

USER appuser

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2"]
