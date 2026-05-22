# Запуск проекта

## Сбилдить образ проекта
```console
sudo docker compose build
```

## Создать файл .env в корне проекта
```console
touch .env
```
Заполнить его данными, которые пришлю

## В корне проекта запустить контейнеры
```console
sudo docker compose up
```

## Backend
Взаимодействие с приложенем реализовано через swagger по адресу [localhost:8000/docs](http://localhost:8000/docs)

## Очистить базу и выключиь контейнеры
```console
sudo docker compose down -v
```
Или нажав ctrl+c

# Основная структура проекта

## ./src/route
Фалы-эндпоинты:
- department.py - эндпоинты для работы с подразделениями
### model
- department.py - pydantic модели запроса/ответы подразделений
- employee.py - pydantic модели запроса/ответы сотрудников

## ./src/db
Директория для работы с БД
### config
- engine.py - движок для создания асинхронных сессий
- url.py - формирование url для подключения к БД
### model
- base.py - базовая модель таблиц
- department.py - модель таблицы "department"
- employee.py - модель таблицы "employee"
### service
- department.py - класс для работы с таблицей "department"
- employee.py - класс для работы с таблицей "employee"
### sql
- department_tree.postgresql.sql - запрос для получения дерева подразделений для PostgreSQL
- department_tree.sqllite.sql - запрос для получения дерева подразделений для SQLLite

## ./src/tests
Файлы для тестов
- conftest.py - конфиг для тестов
- test_departments.py - тесты для эндпоинтов подразделений

## ./sql
- init.py - базовая структура БД при первом запуске контейнера PostgreSQL

# Тесты

## Создайте и активируйте виртуальное окружение в корне проекта
```console
python3 -m venv venv
source ./venv/bin/activate
```
## Установить зависимости для тестов внутри папки src
```console
pip install -r requirements-test.txt -r requirements.txt
```
## Запустите тесты
```console
pytest tests/ -v -s
```


