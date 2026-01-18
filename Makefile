# содержит имя операционной системы (ядра)
UNAME_S := $(shell uname -s)

# регистр важен!!!
# macOS вернет "Darwin"
# Linux вернет "Linux" (включая WSL)

ifeq ($(UNAME_S),Darwin)
# если операционная система macOS, то используем zsh
	SHELL := /bin/zsh
else
# иначе используем bash
	SHELL := /usr/bin/bash
endif

ENV_FILE := ./configs/.env
COMPOSE_FILE := ./configs/compose.yaml
REPLACER_FILE := ./build_scripts/replacer.py
ENV_CREATE_FILE := ./build_scripts/env_creator.py

REPLACE := uv run ${REPLACER_FILE}
CREATE_ENV_EXAMPLE := uv run ${ENV_CREATE_FILE}

COMPOSE := docker-compose -f $(COMPOSE_FILE)

.PHONY: start build up upb logs clean env-example sync-compose sync-mongo-js

# ==============
# === SERVER ===
# ==============

# запускаем локальный сервер
start:
	uv run main.py

# ==============
# === DOCKER ===
# ==============

# собираем контейнеры
build:
	$(COMPOSE) build

# поднимаем контейнеры
up:
	${COMPOSE} up

# пересобираем и поднимаем контейнеры
upb:
	${COMPOSE} up --build

# выводим логи за последние 10 минут
logs:
	${COMPOSE} logs --since=10m

# удаляем контейнеры и их вольюмы 
clean:
	$(COMPOSE) down -v --remove-orphans

# удаляем все подчистую
full-clean:
	docker system prune -a


# ==============
# === UTILS ===
# ==============

# создаем файл .env.example на основе классов BaseSettings
env-example:
	${CREATE_ENV_EXAMPLE} -o configs/.env.example

# создаем файл compose.yaml подставляя переменные из .env
sync-compose:
	${REPLACE} ${ENV_FILE} configs/compose.example.yaml -o configs/compose.yaml 

# создаем файл mongo-init.js подставляя переменные из .env
sync-mongo-js:
	${REPLACE} ${ENV_FILE} configs/mongo-init.example.js -o configs/mongo-init.js
