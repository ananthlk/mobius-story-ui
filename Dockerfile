# syntax=docker/dockerfile:1.7
#
# mobius-story-ui — Cloud Run image
#
# Simple two-stage build: install deps in builder, copy to slim runtime.
# No sibling packages, no editable installs — this service is self-contained.

# ── Builder ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Non-root user
RUN useradd -m -u 1000 story
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application
COPY server/ ./server/
COPY public/ ./public/

USER story

# Cloud Run sets PORT; server/main.py reads UI_PORT (default 8020).
# We expose 8080 to match Cloud Run conventions — the env var overrides.
ENV UI_PORT=8080
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8080"]
