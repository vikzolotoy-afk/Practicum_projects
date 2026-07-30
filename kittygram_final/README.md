# Kittygram (Инфраструктура & CI/CD)

Проект по настройке контейнеризации и автоматического развертывания (CI/CD) для многокомпонентного веб-приложения Kittygram

## 🛠️ Технологический стек инфраструктуры
* **Контейнеризация**: Docker, Docker Compose
* **CI/CD**: GitHub Actions
* **Веб-сервер**: Nginx (обратный прокси-сервер)
* **Уведомления**: Telegram Bot API

## 🚀 Что было реализовано
* **Docker Compose**: Написана конфигурация для оркестрации трех контейнеров (Бэкенд, Фронтенд, База данных) с изоляцией сети и постоянным хранением данных (Volumes).
* **CI/CD Pipeline**: Настроен рабочий процесс (`kittygram_workflow.yml`), который при пуше в ветку `main` автоматически:
  1. Запускает тесты кода.
  2. Собирает Docker-образы и пушит их на Docker Hub.
  3. Деплоит проект на удаленный сервер.
  4. Отправляет отчет о статусе деплоя в Telegram-чат.
* **Nginx**: Сконфигурирован роутинг запросов, раздача статики Django/React и настройка проксирования.

## 📦 Локальный запуск через Docker Compose

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/vikzolotoy-afk/Practicum_projects.git
   cd Practicum_projects/kittygram_final
   ```
2. Запустите проект в фоновом режиме:
   ```bash
   docker compose up -d --build
   ```
3. Выполните миграции и соберите статику:
   ```bash
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py collectstatic --no-input
   ```

## 🧑‍💻 Автор инфраструктуры
* DevOps & CI/CD: [@vikzolotoy-afk](https://github.com/vikzolotoy-afk)
