
FROM ghcr.io/astral-sh/uv:python3.11-bookworm

RUN mkdir /backend
WORKDIR /backend

ENV UV_COMPILE_BYTECODE=1
ENV PATH="/backend/.venv/bin:$PATH"

RUN apt update && \
    apt install -y postgresql-client

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/backend/.venv/bin:$PATH"
ENTRYPOINT []

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]
