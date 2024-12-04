################################################################################
# Use a Python image with uv pre-installed.
FROM python:3.12-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project into `/app`.
WORKDIR /app

# Enable bytecode compilation.
# It improves startup time (at the cost of increased installation time).
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume.
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./uv.lock,target=uv.lock \
    --mount=type=bind,source=./pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it.
# Installing separately from its dependencies allows optimal layer caching.
COPY --link . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

################################################################################
# Then, use a final image without uv.
# It is important to use the image that matches the builder.
FROM python:3.12-alpine AS final

# Install the project into `/app`.
WORKDIR /app

# Copy the application from the builder.
COPY --link --from=builder /app /app

# Place executables in the environment at the front of the path.
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root group and user.
RUN addgroup -S app && adduser -S app -G app
# Set ownership and permissions.
RUN chown -R app:app /app
# Switch to the user just created.
USER app

# Expose the port inside container.
EXPOSE 5000

# Set the default command to run.
CMD [ "python", "app.py" ]
