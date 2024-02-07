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

django_shell:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec web python manage.py shell

django_manage:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec web python manage.py $(cmd)
