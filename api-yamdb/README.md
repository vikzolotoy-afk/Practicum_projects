# API_YAMDB

Финальный проект блока про API в Яндекс Практикум.

---

## Как запустить проект

1. Клонировать репозиторий и перейти в него:

```bash
git clone git@github.com:Kondratebayo/api_yamdb.git
cd api_yamdb
```

2. Создать и активировать виртуальное окружение:

```bash
python3 -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```
3. Обновить pip и установить зависимости:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Выполнить миграции базы данных:

```bash
python3 manage.py migrate
```

5. Запустить проект:

```bash
python3 manage.py runserver
```

Проект будет доступен по адресу: http://127.0.0.1:8000/

---

## API Endpoints

Все эндпоинты и возможные ответы доступны по:
http://127.0.0.1:8000/redoc/

.yaml лежит по пути api_yamdb/api_yamdb/static/redoc.yaml

---

## Tech stack

- Python 3.12
- Django
- Django REST Framework
- SQLite3 (для разработки)

## Author's
[Kondratebayo](https://github.com/Kondratebayo)
[vikzolotoy-afk](https://github.com/vikzolotoy-afk)
[ffgpa2](https://github.com/ffgpa2)