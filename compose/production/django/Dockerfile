FROM python:3.12-slim-bullseye

# Set environment variables to non-interactive
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
  git

# Install NodeJS and npm
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | bash - \
  && apt-get install -y nodejs

# Create non-root user
RUN groupadd --gid 1000 app-user \
  && useradd --uid 1000 --gid app-user --shell /bin/bash --create-home app-user

# Set owner of $APP_HOME
RUN chown app-user:app-user ${APP_HOME}

# For npm:
RUN chmod 777 /usr/bin /usr/local/lib /usr/lib/node_modules /usr/share/man/man1

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
RUN npm install --global gulp-cli \
  && npm install

# Install Python dependencies including dev dependencies
RUN poetry self add "poetry-dynamic-versioning[plugin]" \
  && poetry dynamic-versioning enable \
  && poetry add gunicorn \
  && poetry install --without dev

# Set the entrypoint scripts with proper permissions
COPY --chown=app-user:app-user ./compose/production/django/entrypoint /entrypoint
COPY --chown=app-user:app-user ./compose/production/django/start /start
RUN chmod +x /entrypoint /start

COPY --chown=app-user:app-user ./compose/production/django/celery/beat/start /start-celerybeat
COPY --chown=app-user:app-user ./compose/production/django/celery/flower/start /start-flower
COPY --chown=app-user:app-user ./compose/production/django/celery/worker/start /start-celeryworker
RUN chmod +x /start-celerybeat /start-flower /start-celeryworker

# Ensure git trusts the project
RUN git config --global --add safe.directory "*"

# Ensure Poetry and virtual environment are in the PATH
ENV PATH="/home/app-user/.local/bin:/app/.venv/bin:$PATH"

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
