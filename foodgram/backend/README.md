### Как запустить проект:

1. Клонировать репозиторий и перейти в папку бэкенда:

```bash
git clone https://github.com/vikzolotoy-afk/foodgram.git
cd foodgram/backend
```

2. Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```
* **Если у вас Linux/macOS:**
  ```bash
  source env/bin/activate
  ```
* **Если у вас Windows (Git Bash / CMD):**
  ```bash
  source env/Scripts/activate
  ```

3. Обновить pip и установить зависимости:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Подготовка окружения (`.env`)
Поскольку проект настроен на работу с PostgreSQL, перед запуском создайте файл `.env` в папке `backend/` (рядом с `manage.py`) и укажите доступы к вашей локальной или тестовой базе данных.

5. Выполнить миграции:

```bash
python manage.py migrate
```

6. Запустить локальный сервер:

```bash
python manage.py runserver
```
