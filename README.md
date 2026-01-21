<p align="center">
  <img src="docs/images/logo.png" width="128" height="128">
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
**Anomer** - это просто еще один мессенджер без нагружающих деталей и усложненного функционала.

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

>ОБЯЗАТЕЛЬНО: Заполните параметры в файле `.env`

После чего выполните:
```shell
make configs
```

Готово! Теперь, когда первичная установка и настройка проекта завершена, можете запустить его:
```shell
make start
```

# Дополнительная информация

## Makefile

`Makefile` содержит в себе множество полезных команд, которые были добавлены для удобства разработчика. Вот некоторые из них:

### Docker

- `make build` - выполнит сборку контейнеров из образов.
- `make clean` - останавливает и удаляет все контейнеры, а также их `volumes`.
- `make full-clean` - удаляет все образы и контейнеры.
- `make logs` - выводит все логи контейнеров за последние 10 минут.
- `make up` - запускает контейнеры из файла `compose.yaml`.
- `make upb` - запускает и пересобирате контейнеры из файла `compose.yaml`.
---
Вы можете просмотреть все доступные команды `make`:
```shell
make help
```
или просто введите `make` - справка отобразится в любом из этих случаев.

## Скрипты из папки build_scripts

### env_creator.py

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

