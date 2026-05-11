COMPOSE = docker-compose

build:
	$(COMPOSE) build
up:
	$(COMPOSE) up -d
down:
	$(COMPOSE) down
migrate:
	$(COMPOSE) up -d
	$(COMPOSE) exec web python manage.py migrate
