# Foodgram — Продуктовый помощник

🌐 **Сайт проекта:** [foodgrameda.ru](https://foodgrameda.ru)  
📖 **Документация API:** [foodgrameda.ru/api/docs/](https://foodgrameda.ru)

---

## Технологии
* Python / Django
* Django Rest Framework (DRF)
* PostgreSQL
* Nginx
* Docker / Docker Compose

---

## Запуск проекта через Docker

### 1. Подготовка окружения
Перед запуском создайте файл `.env` в папке `infra/` и заполните его вашими данными. Пример наполнения:

```env
# Настройки Django
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=foodgrameda.ru,www.foodgrameda.ru,158.160.247.104,localhost,127.0.0.1

# Настройки базы данных PostgreSQL
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
```

### 2. Сборка и запуск контейнеров
Перейдите в папку с конфигурационными файлами Docker:
```bash
cd infra
```

Запустите сборку и контейнеры в фоновом режиме:
```bash
docker compose up -d --build
```
*При выполнении этой команды контейнер `frontend` подготовит файлы, необходимые для работы фронтенд-приложения, а затем успешно завершит работу. Остальные сервисы (бэкенд, база данных PostgreSQL и прокси-сервер Nginx) останутся запущенными.*

### 3. Миграции, сборка статики и создание суперпользователя
Выполните миграции внутри контейнера бэкенда:
```bash
docker compose exec backend python manage.py migrate
```

Соберите статичные файлы:
```bash
docker compose exec backend python manage.py collectstatic --no-input
```

Создайте учетную запись администратора (суперпользователя):
```bash
docker compose exec backend python manage.py createsuperuser
```

---

## Запуск проекта без контейнеров (Локально)

Для разработки и тестирования бэкенда вы можете запустить проект локально, используя SQLite (или локальный PostgreSQL) и встроенный сервер Django.

### 1. Клонирование репозитория и настройка окружения
Перейдите в папку `backend/` и создайте виртуальное окружение:
```bash
cd backend
python -m venv venv
```

Активируйте виртуальное окружение:
* **Windows:** `source venv/Scripts/activate`
* **Linux/macOS:** `source venv/bin/activate`

Установите все зависимости проекта:
```bash
pip install -r requirements.txt
```

### 2. Подготовка базы данных локально
Выполните миграции:
```bash
python manage.py migrate
```

Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

### 3. Запуск сервера разработки
```bash
python manage.py runserver
```
Проект будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Импорт ингредиентов в базу данных

В проекте реализована кастомная management-команда для первоначального наполнения базы данных ингредиентами из приложенного JSON-файла.

* **Если проект запущен в Docker:**
  ```bash
  docker compose exec backend python manage.py load_ingredients
  ```

* **Если проект запущен локально (без Docker):**
  ```bash
  python manage.py load_ingredients
  ```

---

## Примеры запросов к API

Полная документация со всеми эндпоинтами доступна по адресу http://127.0.0.1:8000/. Ниже приведены основные запросы:

### 1. Получение списка рецептов (GET)
* **Эндпоинт:** `/api/recipes/`
* **Пример ответа (JSON):**
```json
[
  {
    "id": 50,
    "tags": [
      {
        "id": 2,
        "name": "Обед",
        "slug": "lunch"
      }
    ],
    "author": {
      "email": "vivanov@yandex.ru",
      "id": 21,
      "username": "vasya.ivanov",
      "first_name": "Вася",
      "last_name": "Иванов",
      "is_subscribed": false,
      "avatar": null
    },
    "ingredients": [
      {
        "id": 1195,
        "name": "Панифарин",
        "measurement_unit": "г",
        "amount": 20
      }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Варёное нечто",
    "image": "http://127.0.0.1:8000/media/recipes/images/temp_DGkTo87.png",
    "text": "Варить 20 минут",
    "cooking_time": 25
  }
]
```

### 2. Создание токена авторизации (POST)
* **Эндпоинт:** `/api/auth/token/login/`
* **Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```
* **Ответ (`200 OK`):**
```json
{
  "auth_token": "ab34dce5495122a050693176c7089a8745656950"
}
```

### 3. Добавление рецепта в избранное (POST)
* **Эндпоинт:** `/api/recipes/{id}/favorite/`
* **Ответ при отсутствии авторизации (`401 Unauthorized`):**
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

## Автор проекта
Разработчик бэкенда и API: **vikzolotoy-afk** ([@vikzolotoy-afk](https://github.com))
