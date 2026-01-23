# содержит имя операционной системы (ядра)
# регистр важен!!!
# macOS вернет "Darwin"
# Linux вернет "Linux" (включая WSL)
UNAME_S := $(shell uname -s)

# переменная OS для винды всегда возвращает Windows_NT
ifeq ($(OS), Windows_NT)
    UNAME_S := Windows
else
# если операционная система macOS, то используем zsh
	ifeq ($(UNAME_S),Darwin)
		SHELL := /bin/zsh
	endif
# иначе используем bash
	ifeq ($(UNAME_S),Linux)
		SHELL := /bin/bash
	endif
endif

# если юзер просто написал make, то вызвать таргет help
.DEFAULT_GOAL := help

ENV_FILE := ./configs/.env
COMPOSE_FILE := ./configs/compose.yaml
REPLACER_FILE := ./build_scripts/replacer.py
ENV_CREATE_FILE := ./build_scripts/envex_creator.py

REPLACE := uv run ${REPLACER_FILE}
CREATE_ENV_EXAMPLE := uv run ${ENV_CREATE_FILE}

COMPOSE := docker-compose -f $(COMPOSE_FILE)

# ============
# === HELP ===
# ============
help: ## Отобразить это справочное сообщение
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# ===============
# === INSTALL ===
# ===============
.PHONY: install env-copy

install: ## первичная установка и настройка проекта
# создаем папку certs
	@mkdir -p certs
	@echo "✅ Папка certs создана"
# генерируем в эту папку ключи
	@$(MAKE) -s keys
	@echo "✅ Ключи созданы"
# перед uv sync лучше указать версию питончика
	@echo "3.13" > .python-version
	@echo "✅ Версия Python указана"
# создаст окружение с нужной версией питухона
	@uv sync
	@echo "✅ Окружение создано, зависимости обновлены"
# генерим .env.example
	@$(MAKE) -s env-example
# создаем файл .env (это будет копия .env.example)
	@$(MAKE) -s env-copy
# завершаем установку
	@echo "🚀 Установка завершена!"
	@echo "📋 Следующие шаги:"
	@echo "👉 заполните файл .env своими значениями"
	@echo "👉 выполните make sync"

env-copy: ## копируем .env.example в .env
	@if [ -f configs/.env ]; then \
		echo "⚠️  Внимание: файл .env уже существует, пропускаю копирование."; \
	else \
		mv -n configs/.env.example configs/.env && echo "✅ Файл .env создан."; \
	fi

# ==============
# === SERVER ===
# ==============
.PHONY: start

start: ## запускаем локальный сервер
	uv run main.py

# ==============
# === DOCKER ===
# ==============
.PHONY: build up upb down logs clean full-clean

build: ## собираем контейнеры
	$(COMPOSE) build

up: ## поднимаем контейнеры
	${COMPOSE} up

upb: ## пересобираем и поднимаем контейнеры
	${COMPOSE} up --build

down: ## останавливаем контейнеры
	$(COMPOSE) down

logs: ## выводим логи docker за последние 10 минут
	${COMPOSE} logs --since=10m

clean: ## удаляем контейнеры и их вольюмы 
	$(COMPOSE) down -v --remove-orphans

full-clean: ## удаляем все подчистую
	docker system prune -a

# ==============
# === UTILS ===
# ==============
.PHONY: echo env-example cfg-compose cfg-mongo-js cfg-redis configs

echo: ## Показать все переменные
	@$(foreach v, $(.VARIABLES), $(if $(filter file,$(origin $(v))), echo "🟦 $(v) = $($(v))";))

env-example: ## создаем файл .env.example на основе классов BaseSettings
	${CREATE_ENV_EXAMPLE} -o configs/.env.example

cfg-compose: ## создаем файл compose.yaml подставляя переменные из .env
	${REPLACE} ${ENV_FILE} configs/compose.example.yaml -o configs/compose.yaml 

cfg-mongo-js: ## создаем файл mongo-init.js подставляя переменные из .env
	${REPLACE} ${ENV_FILE} configs/mongo-init.example.js -o configs/mongo-init.js

cfg-redis: ## создаем файл redis.conf подставляя переменные из .env
	${REPLACE} ${ENV_FILE} configs/redis.conf.example -o configs/redis.conf

configs: cfg-compose cfg-mongo-js cfg-redis ## создаем/обновляем конфиги

# ================
# === SECURITY ===
# ================
.PHONY: secret-key public-key keys

secret-key: ## генерация приватного ключа
ifeq ($(UNAME_S),Windows)
	@echo "🥀 для винды ниче еще не готово"
	@echo "❌ ПРИВАТНЫЙ КЛЮЧ НЕ СГЕНЕРИРОВАН"
else
	@echo "-- используем способ для macOS/Linux..."
	@openssl genrsa -out certs/jwt-private.pem 2048
endif

public-key: ## генерация публичного ключа
ifeq ($(UNAME_S),Windows)
	@echo "🥀 для винды ниче еще не готово"
	@echo "❌ ПУБЛИЧНЫЙ КЛЮЧ НЕ СГЕНЕРИРОВАН"
else
	@echo "-- используем способ для macOS/Linux..."
	@openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
endif

keys: secret-key public-key ## генерируем приватный и публичный ключи