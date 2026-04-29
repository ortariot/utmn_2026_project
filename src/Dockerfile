FROM python:3.14-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv


COPY pyproject.toml uv.lock ./


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev -v

RUN cp /usr/local/bin/uv /tmp/

FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /app/.venv /app/.venv


COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:/app/.venv/lib/python3.14/site-packages"


RUN useradd -m -u 1000 appuser && \
    chmod +x /app/src/entrypoint.sh && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

WORKDIR /app/src

CMD ["/app/src/entrypoint.sh"]

