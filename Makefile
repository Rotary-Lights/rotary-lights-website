# Define variables
DOCKER_COMPOSE_LOCAL = docker compose -f docker-compose.local.yml
DOCKER_COMPOSE_PRODUCTION = docker compose -f docker-compose.production.yml

# Define the image names
LOCAL_IMAGES = rotary_lights_website_local_django \
               rotary_lights_website_local_celeryworker \
               rotary_lights_website_local_celerybeat \
               rotary_lights_website_local_flower \
               rotary_lights_website_production_postgres

PRODUCTION_IMAGES = rotarylights/website \
                    rotarylights/postgres

# Default target
.PHONY: all
all: build_local build_production push_production

# Default production target
.PHONY: production
production: build_production push_production

# Build targets
.PHONY: build_local
build_local:
	$(DOCKER_COMPOSE_LOCAL) build

.PHONY: build_production
build_production: build_rotarylights_website build_postgres

.PHONY: build_rotarylights_website
build_rotarylights_website:
	docker build -t rotarylights/website:latest -f compose/production/django/Dockerfile .

.PHONY: build_postgres
build_postgres:
	docker build -t rotarylights/postgres:latest -f compose/production/postgres/Dockerfile .

# Push targets
.PHONY: push_production
push_production:
	@echo "Pushing production images..."
	@$(foreach image, $(PRODUCTION_IMAGES), docker push $(image);)

# Clean up
.PHONY: clean
clean:
	$(DOCKER_COMPOSE_LOCAL) down --rmi all
	$(DOCKER_COMPOSE_PRODUCTION) down --rmi all
