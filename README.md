# Django REST API + Telegram Bot Integration

Учебный проект по курсу Python/Django: интеграция REST API и Telegram-бота через HTTP.

## О проекте

Демонстрация архитектуры, где Django REST Framework предоставляет API, а Telegram-бот выступает клиентом этого API. Компоненты запускаются как независимые процессы и общаются по HTTP.

**Технологии:**

- Django 4.2+ & Django REST Framework
- pyTelegramBotAPI (telebot)
- django-cors-headers
- Python 3.11+

## Возможности

**API:**

- Регистрация пользователя Telegram (POST)
- Получение данных пользователя (GET)
- Идемпотентная регистрация (повторный запрос не создаёт дубликат)
- CORS для браузерных клиентов

**Telegram-бот:**

- `/start` — регистрация через API
- `/myinfo` — получение своих данных из API
- Обработка ошибок (API недоступен, пользователь не найден)

## Быстрый старт (Windows 11)

### 1. Клонирование и настройка

```powershell
git clone https://github.com/ergon73/django-rest-telegram-bot-integration.git
cd django-rest-telegram-bot-integration
.\scripts\setup.ps1
```

### 2. Конфигурация

Создай `.env` в корне проекта:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
API_BASE_URL=http://127.0.0.1:8010/api
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. Запуск

**Терминал 1 — API:**

```powershell
.\scripts\run_api.ps1
```

**Терминал 2 — Бот:**

```powershell
.\scripts\run_bot.ps1
```

## API Reference

### POST /api/register/

Регистрация пользователя Telegram.

**Request:**

```json
{
  "user_id": 123456789,
  "username": "alice"
}
```

**Response 201 (Created):**

```json
{
  "user_id": 123456789,
  "username": "alice",
  "created_at": "2025-01-28T12:00:00Z"
}
```

**Response 200 (Already exists):**

```json
{
  "user_id": 123456789,
  "username": "alice",
  "created_at": "2025-01-28T12:00:00Z",
  "already_registered": true
}
```

### GET /api/user/{user_id}/

Получение данных пользователя.

**Response 200:**

```json
{
  "user_id": 123456789,
  "username": "alice",
  "created_at": "2025-01-28T12:00:00Z"
}
```

**Response 404:**

```json
{
  "message": "User not found"
}
```

## Примеры запросов

### PowerShell

```powershell
# Регистрация
Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8010/api/register/" `
  -ContentType "application/json" `
  -Body '{"user_id": 123, "username": "alice"}'

# Получение данных
Invoke-RestMethod -Uri "http://127.0.0.1:8010/api/user/123/"
```

### curl (Git Bash / WSL)

```bash
# Регистрация
curl -X POST http://127.0.0.1:8010/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123, "username": "alice"}'

# Получение данных
curl http://127.0.0.1:8010/api/user/123/
```

## Структура проекта

```text
django-rest-telegram-bot-integration/
├── djangobot/           # Django project settings
│   ├── settings.py      # DRF, CORS configuration
│   └── urls.py          # Root URL routing
├── bot/                 # Django app
│   ├── models.py        # TelegramUser model
│   ├── serializers.py   # DRF serializer
│   ├── views.py         # API endpoints
│   ├── urls.py          # API routes
│   └── tests.py         # Unit tests
├── telegram_bot/
│   └── bot_main.py      # Telegram bot client
├── scripts/             # PowerShell scripts
│   ├── setup.ps1
│   ├── run_api.ps1
│   └── run_bot.ps1
├── .env.example
├── requirements.txt
└── manage.py
```

## Тестирование

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py test
```

**Дополнительные возможности:**

**Browsable API:**
- `http://127.0.0.1:8010/api/` - корневой эндпоинт с документацией
- `http://127.0.0.1:8010/admin/` - админ-панель для управления пользователями

**Архитектура**

```text
┌─────────────────┐     HTTP POST/GET     ┌─────────────────┐
│  Telegram Bot   │ ◄──────────────────► │   Django API    │
│  (bot_main.py)  │                       │  (DRF views)    │
└─────────────────┘                       └─────────────────┘
        │                                         │
        │                                         │
        ▼                                         ▼
┌─────────────────┐                       ┌─────────────────┐
│ Telegram Servers│                       │    SQLite DB    │
└─────────────────┘                       └─────────────────┘
```

**Принцип:** бот и API — независимые процессы. Бот не встроен в Django, а является HTTP-клиентом.

## Лицензия

MIT License

## Автор

**Георгий Белянин (Georgy Belyanin)**  
georgy.belyanin@gmail.com
