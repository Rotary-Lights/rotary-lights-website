# Base stage for building the application
FROM python:3.12-slim-bullseye AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.7.1 \
  APP_HOME=/app \
  PATH="$PATH:/home/app-user/.local/bin" \
  DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  python3-dev \
  curl \
  ca-certificates \
  gnupg2 \
  git \
  && curl -fsSL https://deb.nodesource.com/setup_21.x | bash - \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 app-user \
  && useradd --uid 1000 --gid app-user --shell /bin/bash --create-home app-user

# Install npm global packages as root user
RUN npm install --global gulp-cli

# Set ownership of the application directory and required subdirectories
RUN mkdir -p /app/staticfiles /app/media /app/media/original_images /app/node_modules \
  && chown -R app-user:app-user /app

# Switch to non-root user
USER app-user

# Install poetry for the non-root user
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

# Copy application code and poetry files
COPY --chown=app-user:app-user pyproject.toml poetry.lock ./
COPY --chown=app-user:app-user . .

# Configure Poetry to create the virtual environment inside the project directory
RUN poetry config virtualenvs.in-project true

# Install frontend dependencies
RUN npm install

# Install Python dependencies including dev dependencies
RUN poetry self add "poetry-dynamic-versioning[plugin]" \
  && poetry dynamic-versioning enable \
  && poetry install --without dev

# Production stage
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  APP_HOME=/app \
  PATH="$PATH:/home/app-user/.local/bin:/app/.venv/bin" \
  DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR ${APP_HOME}

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  curl \
  ca-certificates \
  gnupg2 \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 app-user \
  && useradd --uid 1000 --gid app-user --shell /bin/bash --create-home app-user

# Switch to non-root user
USER app-user

# Copy the application code and virtual environment from the builder stage
COPY --chown=app-user:app-user --from=builder ${APP_HOME} ${APP_HOME}
COPY --chown=app-user:app-user --from=builder /home/app-user/.local /home/app-user/.local

# Set the entrypoint scripts with proper permissions
COPY --chown=app-user:app-user ./compose/production/django/entrypoint /entrypoint
COPY --chown=app-user:app-user ./compose/production/django/start /start
RUN chmod +x /entrypoint /start

COPY --chown=app-user:app-user ./compose/production/django/celery/beat/start /start-celerybeat
COPY --chown=app-user:app-user ./compose/production/django/celery/flower/start /start-flower
COPY --chown=app-user:app-user ./compose/production/django/celery/worker/start /start-celeryworker
RUN chmod +x /start-celerybeat /start-flower /start-celeryworker

# Ensure wait-for-it is executable
RUN chmod +x ./wait-for-it.sh

# Ensure the staticfiles and media directories are available and accessible
RUN mkdir -p /app/staticfiles /app/media /app/media/original_images

# Ensure git trusts the project
RUN git config --global --add safe.directory "*"

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
