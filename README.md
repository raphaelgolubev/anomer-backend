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
**Anomer** - это просто еще один мессенджер без нагружающих деталей и усложненного функционала.

# Установка

## Подготовка

Убедитесь, что:

1. У вас есть аккаунт на `github.com`
2. В системе установлен и настроен `git`
3. У вас установлен `Docker Desktop`
4. Вы установили `uv`

## Ручная установка
### для Windows
~~установите Linux как вторую систему или купите макбук и не парьтесь~~ 

пока что этот раздел не готов.

### для MacOS или Linux

1. Создайте папку для хранения сертификатов `certs`:

    ```shell
    mkdir certs
    ```

    <sub> Команда создаст папку `"certs"` в текущей директории. </sub>

2. Сгенерируйте приватный ключ (RSA):

    ```shell
    openssl genrsa -out certs/jwt-private.pem 2048
    ```

    <sub> Команда сгенерирует приватный ключ и сохранит его содержимое в папку "certs" в файл `"jwt-private.pem"`. </sub>

3. Получите публичный ключ:
    ```shell
    openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
    ```

    <sub> Команда сгенерирует публичный ключ и сохранит его содержимое в папку "certs" в файл `"jwt-public.pem"`. </sub>

4. Создайте файл `.python-version`:
    ```shell
    echo "3.13" > .python-version
    ```

    <sub> Это необходимо для того, чтобы `uv` установил локальный экземпляр Python версии 3.13 </sub>

5. Инициализируйте проект:
    ```shell
    uv sync
    ```

    <sub> Команда создаст виртуальное окружение в текущей директории, а также скачает и установит необходимые зависимости. </sub>

6. Создайте файл переменных окружения:
    ```shell
    mv .env.example .env
    ```

7. Заполните параметры в файле `.env`