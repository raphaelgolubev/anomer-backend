<p align="center">
  <img src="docs/images/logo.svg" width="128" height="128">
  <h1 align="center">Anomer (backend)</h1>
  <p align="center"> Another New Online MEssengeR</p>
</p>

<p align="center">
  <img alt="Static Badge" src="https://img.shields.io/badge/raphael_golubev-anomer-5ad1e6">
  <img alt="GitHub Created At" src="https://img.shields.io/github/created-at/raphaelgolubev/anomer-backend">
  <img alt="GitHub" src="https://img.shields.io/github/license/raphaelgolubev/anomer-backend?color=white">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/raphaelgolubev/anomer-backend">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/t/raphaelgolubev/anomer-backend?color=green">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/raphaelgolubev/anomer-backend?color=black">
</p>

# Описание
**Anomer** - это просто еще один мессенджер.

Frontend - https://github.com/raphaelgolubev/anomer-web

# Установка

## Подготовка

Убедитесь, что:

- У вас есть аккаунт на `github.com`
- У вас установлен и настроен `git`
- У вас установлен `Docker Desktop`
- Вы установили `uv`

## Автоматическая установка

В корневой директории проекта (там где `Makefile`) выполните:
```shell
make install
```

>ОБЯЗАТЕЛЬНО: Перед следующим шагом заполните параметры в файле `.env`

После чего выполните:
```shell
make configs
```

Затем запустите `Docker Desktop`, соберите и поднимите контейнеры, выполнив:
```shell
make upb
```

Готово! Теперь, когда первичная установка и настройка проекта завершена, можете запустить его:
```shell
make start
```

# Дополнительная информация

## Makefile

`Makefile` содержит в себе множество полезных команд, которые я добавил для своего удобства. Вот некоторые из них:

### Docker

- `make build` - выполнит сборку контейнеров из образов.
- `make clean` - останавливает и удаляет все контейнеры, а также их `volumes`.
- `make full-clean` - удаляет все образы и контейнеры.
- `make logs` - выводит все логи контейнеров за последние 10 минут.
- `make up` - запускает контейнеры из файла `compose.yaml`.
- `make upb` - запускает и пересобирает контейнеры из файла `compose.yaml`.


### Utils
- `make configs` - создаст или перезапишет служебные файлы (compose.yaml, redis.conf и тд). Рекомендую вызывать команду после каждого изменения значений в `.env` файле.
- `make env-example` - создаст или перезапишет файл .env.example

### Security
- `make keys` - сгенерирует новые публичный и приватный ключи.

...и многое другое

---
Вы можете просмотреть все доступные команды `make`:
```shell
make help
```
или просто введите `make` - справка отобразится в любом из этих случаев.

## Скрипты из папки build_scripts

### envex.py

Этот скрипт выполняет анализ всех `BaseSettings` классов и создает файл `.env.example` на основе их содержимого. Например:

```python
class MailSettings(BaseSettings):
    """
    Настройки подключения почтового сервера. (Gmail)
    """

    port: int = 465
    """ Порт почтового сервера """

    hostname: str | None = None
    """ Имя хоста почтового сервера """

    password: str | None = None
    """ Пароль пользователя """

    sender: str | None = None
    """ Отправитель. Например, `ivan.ivanov@gmail.com` """

    templates_path: Path | None = None
    """ Путь к HTML-шаблонам оформления исходящих писем """

    # env-example-ignore
    test_feature_flag: bool = False

    model_config = ModelConfig(env_prefix="MAIL__")
```

На основе этого класса в файле `.env.example` появится следующая секция:
```shell
# ---+ MailSettings +---
# Настройки подключения почтового сервера. (Gmail)
# ----------------------
	# Порт почтового сервера. По умолчанию: '465'
	# [int]
	MAIL__PORT = 0
	# Имя хоста почтового сервера.
	# [str | None]
	MAIL__HOSTNAME = "<какая-то строка>"
	# Пароль пользователя.
	# [str | None]
	MAIL__PASSWORD = "<какая-то строка>"
	# Отправитель. Например, `ivan.ivanov@gmail.com`.
	# [str | None]
	MAIL__SENDER = "<какая-то строка>"
	# Путь к HTML-шаблонам оформления исходящих писем.
	# [Path | None]
	MAIL__TEMPLATES_PATH = "<путь>"
```

Обратите внимание, что свойство `test_feature_flag` не попало в конечный файл, потому что перед ним указан комментарий `env-example-ignore`, который заставляет игнорировать свойство при анализе класса.

В каждом `BaseSettings` классе обязательно нужно указать `model_config` с параметром `env_prefix` для того, чтобы скрипт знал какой префикс добавлять к свойствам в `.env` файл.

```python
model_config = ModelConfig(env_prefix="MAIL__")
```

`ModelConfig` - это небольшая надстройка над `SettingsConfigDict` из pydantic_settings.

В конечный файл попадают свойства:
- только аннотированные свойства
- свойства только с простыми типами `str`, `int`, `bool`, `Path`.

> Всякий раз, когда я меняю структуру настроек в проекте, я запускаю этот скрипт для обновления `.env.example` в репозитории.
---
### replacer.py

Позволяет подставлять значения переменных из `.env` внутри указанного файла.
Просто укажите название переменной в формате`*{ПЕРЕМЕННАЯ}` и запустите скрипт, указав путь `.env` файлу и путь к вашему файлу.
Например:

файл `/configs/.env`:
```shell
APP__NAME="Anomer"
REDIS__HOST="localhost"
REDIS__PORT=3000
```

файл `/configs/redis.conf`:
```shell
# Redis конфигурация для *{APP__NAME}

# Основные настройки
bind *{REDIS__HOST}
port *{REDIS__PORT}
timeout 0
tcp-keepalive 300
```

Запуск скрипта:
```shell
uv run replacer.py configs/.env data/redis.conf -o result/redis_test.conf
```

- `uv run replacer.py` - запуск скрипта в контексте `uv`.
- `configs/.env` - путь до `.env` файла.
- `data/redis.conf` - файл, который нужно обработать.
- `result/redis_test.conf` - место, куда нужно сохранить результат

Таким образом, конечный файл `redis_test.conf` будет иметь следующее содержимое:
```shell
# Redis конфигурация для Anomer <---- [значение APP__NAME]

# Основные настройки
bind localhost    <---- [значение REDIS__HOST]
port 3000         <---- [значение REDIS__PORT]
timeout 0
tcp-keepalive 300
```

> Это очень простой, но также очень полезный скрипт, который я использую в `Makefile` для генерации различных файлов. В частности для таргета `make configs`.