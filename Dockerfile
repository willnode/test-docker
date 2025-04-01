# Use a lightweight Python image
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the application code
COPY *.py ./
COPY templates/ templates/

# Expose port
EXPOSE 5000

# Run the application
CMD ["/app/.venv/bin/python", "app.py"]
