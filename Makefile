include .env
# Define default action when make is called without arguments
.PHONY: all
all: up

# Directory where docker-compose.yml is located
COMPOSE_DIR := .build

# Path to the docker-compose file
COMPOSE_FILE := $(COMPOSE_DIR)/docker-compose.yml

# Docker Compose Project Name
PROJECT_NAME := todoapp

# Path to env file
ENV_FILE := ./.env

# Commands
.PHONY: build up down restart logs ps shell psql

# Build services
build:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d --build

# Start services
up:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d

# Stop services
down:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down

# Restart services
restart: down up

# View output from containers
logs:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) logs

# List containers
ps:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) ps

# Open a shell in the 'web' service container
shell:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec web /bin/sh

drop-db:
	@echo "Terminating all active database connections ${POSTGRES_DB}..."
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T database psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '${POSTGRES_DB}' AND pid <> pg_backend_pid();"
	@echo "Droping the ${POSTGRES_DB} database..."
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T database psql -U postgres -c "DROP DATABASE ${POSTGRES_DB};"

django_shell:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec web python manage.py shell

django_manage:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec web python manage.py $(cmd)

demo:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d --build
	# sleep 10
	@echo "Creating a role and database..."
	- docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec database psql -U postgres -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
	- docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec database psql -U postgres -c "CREATE DATABASE ${POSTGRES_DB} WITH OWNER ${POSTGRES_USER};"
	@echo "Applying migrations to the database..."
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME)  exec web python manage.py migrate
	@echo "Filling the database with the initial data..."
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec web python manage.py populate_database
