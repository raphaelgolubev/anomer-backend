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

ENV_FILE := ./configs/.env
COMPOSE_FILE := ./configs/compose.yaml
REPLACER_FILE := ./build_scripts/replacer.py
ENV_CREATE_FILE := ./build_scripts/env_creator.py

REPLACE := uv run ${REPLACER_FILE}
CREATE_ENV_EXAMPLE := uv run ${ENV_CREATE_FILE}

COMPOSE := docker-compose -f $(COMPOSE_FILE)

# ===============
# === INSTALL ===
# ===============
.PHONY: install env-copy

install:
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


env-copy:
	@if [ -f configs/.env ]; then \
		echo "⚠️  Внимание: файл .env уже существует, пропускаю копирование."; \
	else \
		mv -n configs/.env.example configs/.env && echo "✅ Файл .env создан."; \
	fi

# ==============
# === SERVER ===
# ==============
.PHONY: start

# запускаем локальный сервер
start:
	uv run main.py

# ==============
# === DOCKER ===
# ==============
.PHONY: build up upb logs clean full-clean

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
.PHONY: echo env-example sync-compose sync-mongo-js sync

echo:
	@echo "🟦 UNAME_S 				= ${UNAME_S}"
	@echo "🟦 ENV_FILE 				= ${ENV_FILE}"
	@echo "🟦 COMPOSE_FILE 			= ${COMPOSE_FILE}"
	@echo "🟦 REPLACER_FILE			= ${REPLACER_FILE}"
	@echo "🟦 ENV_CREATE_FILE		= ${ENV_CREATE_FILE}"
	@echo "🟦 REPLACE				= ${REPLACE}"
	@echo "🟦 CREATE_ENV_EXAMPLE	= ${CREATE_ENV_EXAMPLE}"
	@echo "🟦 COMPOSE				= ${COMPOSE}"

# создаем файл .env.example на основе классов BaseSettings
env-example:
	${CREATE_ENV_EXAMPLE} -o configs/.env.example

# создаем файл compose.yaml подставляя переменные из .env
sync-compose:
	${REPLACE} ${ENV_FILE} configs/compose.example.yaml -o configs/compose.yaml 

# создаем файл mongo-init.js подставляя переменные из .env
sync-mongo-js:
	${REPLACE} ${ENV_FILE} configs/mongo-init.example.js -o configs/mongo-init.js

# синхронизируем все
sync: sync-compose sync-mongo-js


# ================
# === SECURITY ===
# ================
.PHONY: secret-key public-key keys

# генерация приватного ключа
secret-key:
ifeq ($(UNAME_S),Windows)
	@echo "🥀 для винды ниче еще не готово"
	@echo "❌ ПРИВАТНЫЙ КЛЮЧ НЕ СГЕНЕРИРОВАН"
else
	@echo "-- используем способ для macOS/Linux..."
	@openssl genrsa -out certs/jwt-private.pem 2048
endif

public-key:
ifeq ($(UNAME_S),Windows)
	@echo "🥀 для винды ниче еще не готово"
	@echo "❌ ПУБЛИЧНЫЙ КЛЮЧ НЕ СГЕНЕРИРОВАН"
else
	@echo "-- используем способ для macOS/Linux..."
	@openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
endif

# можно просто вызвать "keys"
keys: secret-key public-key