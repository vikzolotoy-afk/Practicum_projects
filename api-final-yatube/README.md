### API для социальной сети Yatube

### Описание
Проект представляет собой финальную версию API для платформы Yatube. 
Сервис позволяет пользователям публиковать посты, подписываться на авторов, оставлять комментарии и объединяться в группы. 
Аутентификация реализована с помощью JWT-токенов.

Польза проекта заключается в разделении логики хранения данных и интерфейса пользователя. 
Это делает платформу масштабируемой и доступной для интеграций через современные протоколы передачи данных (JSON) с использованием JWT-аутентификации.

### Стек технологий:
- **Python 3.12.7**
- **Django 5.1.1**
- **Django REST Framework**
- **Djoser** / **Simple JWT**
- **SQLite3**

### Как запустить проект:

Клонировать репозиторий и перейти в него:

```
git clone https://github.com/vikzolotoy-afk/Practicum_projects.git
```

```
cd Practicum_projects/api-final-yatube
```

#### Для MacOS/Linux:
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

#### Для Windows:
Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Примеры запросов к API
#### Получение JWT-токена

```
POST /api/v1/jwt/create/
```
Передайте в теле запроса username и password. В ответ придет access-токен.

#### Создание новой публикации
```
POST /api/v1/posts/
```
Запрос доступен только авторизованным пользователям (Header: Authorization Bearer )

```
json
{
  "text": "Текст нового поста",
  "group": 1
}
```

#### Подписка на автора
```
POST /api/v1/follow/
```

```
json
{
  "following": "username_автора"
}
```

#### Получение комментариев к посту
```
GET /api/v1/posts/{post_id}/comments/
```

### Автор
[vikzolotoy-afk](https://github.com/vikzolotoy-afk)
