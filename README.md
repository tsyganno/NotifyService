***
# Notify Service
Микросервис для управления уведомлениями с аутентификацией JWT и кешированием Redis.
***
## 🚀 Возможности
* **Аутентификация** - JWT-based аутентификация пользователей
* **Управление уведомлениями** - Создание, получение, удаление уведомлений
* **Пагинация** - Постраничное получение уведомлений
* **Кеширование** - Redis для повышения производительности
* **Безопасность** - Хеширование паролей, защищенные endpoints
***
## 🛠 Технологии
* **FastAPI** - Веб-фреймворк
* **PostgreSQL** - Основная база данных
* **Redis** - Кеширование и сессии
* **Tortoise ORM** - Асинхронный ORM
* **JWT** - Аутентификация
* **Docker** - Контейнеризация
* **Pytest** - Тестирование
***
## 📦 Установка и запуск
### 1. Клонирование репозитория
```bash
git clone https://github.com/tsyganno/NotifyService.git
cd NotifyService
```
### 2. Настройка окружения
* Создайте файл .env на основе .env.example в директории проекта
* Файл .env должен содержать:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=notifications
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=replace_this_with_secure_random_key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://redis:6379/0
CACHE_EXPIRE_SECONDS=300
```
### 3. Запуск через Docker
```bash
docker compose up -d
```
### 4. Проверить
* API: [http://localhost:8000/health](http://localhost:8000/health)
***
## 📚 API Документация
После запуска сервиса документация доступна по адресам:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
***
## 📁 Структура проекта
```
app/
├── core/                     # Основные настройки
│   ├── config.py             # Конфигурация приложения
│   ├── logging.py            # Логирование
│   ├── security.py           # JWT и хеширование
│   └── redis.py              # Redis клиент
├── db_services/              # Работа с БД
│   ├── database.py           # Настройка Tortoise ORM
│   └── crud.py               # CRUD операции
├── exception_handlers/       # Обработка исключений
│   └── exception_handlers.py # Кастомные исключения
├── models/                   # Модели данных
│   └── models.py             # User, Notification
├── rest_models/              # Pydantic схемы
│   └── rest_models.py        # Схемы для API
├── routers/                  # API endpoints
│   ├── users.py              # Аутентификация
│   └── notifications.py      # Уведомления
├── services/                 # Бизнес-логика
│   ├── cache_service.py      # Сервис кеширования
│   └── other_functions.py    # Вспомогательные функции
└── main.py                   # Точка входа
```
***
## 🔐 Аутентификация
* Регистрация пользователя
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpassword123"
}
```
* Вход в систему
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
    "username": "testuser", 
    "password": "testpassword123"
}
```
* Ответ:
```bash
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```
## 📨 Работа с уведомлениями
* Создание уведомления
```bash
POST /api/v1/notifications
Authorization: Bearer {token}
Content-Type: application/json

{
    "type": "like",
    "text": "Ваш пост понравился пользователю"
}
```
* Получение уведомлений
```bash
GET /api/v1/notifications
Authorization: Bearer {token}
```
* Удаление уведомления
```bash
DELETE /api/v1/notifications/{notification_id}
Authorization: Bearer {token}
```
***
## 🧪 Тестирование
Запуск тестов:
```bash
# Запуск всех тестов
docker-compose exec app pytest -v
```
***