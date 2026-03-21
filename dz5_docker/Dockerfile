FROM python:3.13-trixie
WORKDIR /var/app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/
COPY . .
RUN uv sync --locked --no-install-project
ENV PATH="/var/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uv", "run", "main.py", "--host", "0.0.0.0"]