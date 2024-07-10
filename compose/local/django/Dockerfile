FROM python:3.12-slim-bullseye

# Set environment variables to non-interactive
ENV PYTHONDONTWRITEBYTECODE=1               \
  PYTHONUNBUFFERED=1                      \
  POETRY_VERSION=1.7.1                    \
  APP_HOME=/app                           \
  PATH="$PATH:/home/dev-user/.local/bin"  \
  DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y  \
  build-essential                                                 \
  python3-dev                                                     \
  gnupg2                                                          \
  gcc                                                             \
  sudo                                                            \
  git                                                             \
  bash-completion                                                 \
  nano                                                            \
  ssh                                                             \
  curl                                                            \
  ca-certificates

# Add Docker's official GPG key and repository
RUN install -m 0755 -d /etc/apt/keyrings                         \
  && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
  && chmod a+r /etc/apt/keyrings/docker.asc                       \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
  && apt-get update                                               \
  && apt-get install -y                                           \
     docker-ce                                                    \
     docker-ce-cli                                                \
     containerd.io                                                \
     docker-buildx-plugin                                         \
     docker-compose-plugin

# Install NodeJS and npm
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | sudo -E bash - \
  && apt-get install -y nodejs

# Clean up unused files to reduce image size
RUN apt-get clean                                                \
  && rm -rf /var/lib/apt/lists/*


# Create non-root user
RUN groupadd --gid 1000 dev-user                                                    \
  && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user     \
  && echo "dev-user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/dev-user              \
  && chmod 0440 /etc/sudoers.d/dev-user                                             \
  && usermod -aG docker dev-user

# Set owner of $APP_HOME
RUN chown dev-user:dev-user ${APP_HOME}

# For testing purposes:
RUN chmod 777 /run

# For npm:
RUN chmod 777 /usr/bin
RUN chmod 777 /usr/local/lib
RUN chmod 777 /usr/lib/node_modules
RUN chmod 777 /usr/share/man/man1

# Switch to non-root user
USER dev-user

# Install poetry for the non-root user
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

# Copy application code and poetry files
COPY --chown=dev-user:dev-user . .

# Set the entrypoint scripts with proper permissions
COPY --chown=dev-user:dev-user ./compose/local/django/entrypoint   /entrypoint
COPY --chown=dev-user:dev-user ./compose/local/django/start        /start
RUN chmod +x /entrypoint /start

COPY --chown=dev-user:dev-user ./compose/local/django/celery/beat/start        /start-celerybeat
COPY --chown=dev-user:dev-user ./compose/local/django/celery/flower/start      /start-flower
COPY --chown=dev-user:dev-user ./compose/local/django/celery/worker/start      /start-celeryworker
RUN chmod +x /start-celerybeat /start-flower /start-celeryworker

# Ensure git trusts the project
RUN git config --global --add safe.directory "*"

# Install frontend dependencies
RUN npm install --global gulp-cli
RUN npm install

# Install Python dependencies including dev dependencies
RUN poetry self add "poetry-dynamic-versioning[plugin]"
RUN poetry dynamic-versioning enable
RUN poetry install --with dev

ENTRYPOINT [ "/entrypoint" ]
CMD [ "/start" ]
