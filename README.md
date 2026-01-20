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

1. У вас есть аккаунт на `github.com`
2. У вас установлен и настроен `git`
3. У вас установлен `Docker Desktop`
4. Вы установили `uv`

## Автоматическая установка

1. В корневой директории проекта (там где `Makefile`) выполните:
    ```shell
    make install
    ```
2. Заполните параметры в файле `.env`
3. В конце выполните:
    ```
    make sync
    ```