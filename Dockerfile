# Build mit uv, Laufzeit schlank – analog zu den Referenz-Servern in modelcontextprotocol/servers
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY uv.lock pyproject.toml README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev --no-editable

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM python:3.12-slim-bookworm

LABEL io.modelcontextprotocol.server.name="io.github.flawas/garmin-mcp"

WORKDIR /app
RUN useradd -rUM -s /usr/sbin/nologin app
COPY --from=uv --chown=app:app /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV GARMIN_MCP_DATA_DIR=/tmp/garmin-connect-mcp
USER app

# API-Key per -e GARMIN_PERSONAL_API_KEY=… übergeben
ENTRYPOINT ["mcp-server-garmin-connect"]
