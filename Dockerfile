# ── Stage 1: dependency builder ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: lean runtime image ──────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="devops@greenstechnology.com" \
      version="1.0" \
      description="FastAPI application – Green's Technology"

# Non-root user for security (no privilege escalation)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /code

# Copy only installed packages from builder (keeps image small)
COPY --from=builder /install /usr/local

# Copy application source
COPY --chown=appuser:appgroup main.py     .
COPY --chown=appuser:appgroup form.html   .

USER appuser

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2"]
