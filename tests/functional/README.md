## Используемые технологии
* Python 3.10 + Pytest-asyncio==0.21.0
* Allure (для отчетов)
* Aiohttp (для запросов)
* Aiofiles (для асинхронной работы с файлами)
* Docker (контейнеризация)

## Как запустить?
Можно запустить внутри контейнера.<br>
<br>
Вне контейнера запускается командой: `pytest src` внутри директории, где находится dockerfile.<br>
Также можно сгенерировать allure отчет:<br>
Установите сам <a href="https://docs.qameta.io/allure-report/#_installing_a_commandline">allure</a>.<br>
А дальше можно запустить коммандами:
```
pytest src
allure serve allure-results
```