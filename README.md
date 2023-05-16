# Сервис авторизации
## Содержание
- [Описание](#desc)
- [Используемые технологии](#techs)
- [Подготовка к запуску](#installing)
- [Запуск](#running)
- [Тесты](#tests)
- [Авторы](#authors)

## Описание проекта <a name="desc"></a>
Сервис авторизации

## Основные используемые технологии <a name="techs"></a>
* Python 3.10 + Flask 2.2.3 + Gevent
* Postgresql (хранение данных)
* SQLAlchemy (ORM)
* Redis (кэширование)
* Gunicorn (HTTP-сервер)
* Docker (контейнеризация)

## Подготовка к запуску <a name="installing"></a>
Установите <a href="https://docs.docker.com/get-docker/">docker</a>.<br>
<br>
Склонируйте репозиторий и введите переменные окружения.<br>
<br>
![install-gif](./docs/init.gif)

## Запуск <a name="running"></a>
Осуществляется командой: `make up`

## Тесты <a name="tests"></a>
О тестах можно почитать здесь: [tests readme](tests/functional/README.md)

## Авторы <a name="authors"></a>

* Николай Кириченко - тимлид проекта
* Салимов Гусейн aka Август - разработчик
* Гончарова Ольга - разработчик