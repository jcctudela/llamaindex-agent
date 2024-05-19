# Makefile commands for managing a Django project with Docker Compose

# Display this help text
help:
	@echo "Available commands for this Django project managed with Docker:"
	@echo "  build             Build or rebuild services."


# Build or rebuild services
build:
	docker-compose build

run:
	docker-compose run --rm bot python main.py "$(PROMPT)"

up:
	docker-compose up

down:
	docker-compose down

.PHONY: help build
