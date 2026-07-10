FROM python:3.13.9-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

ENV UV_COPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

ENV UV_TOOL_BIN_DIR=/usr/local/bin

WORKDIR /var/app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev

COPY job-app ./

RUN chmod +x /var/app/entrypoint.sh

ENV PATH="/var/app/.venv/bin:$PATH"

ENTRYPOINT ["/var/app/entrypoint.sh"]

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]