# 🌍 Where Are You From

Mini-сервис, который определяет вероятную страну происхождения человека по его имени, используя внешние API и сохраняет агрегированные данные в локальную базу. Подходит для использования исследователями, маркетологами и аналитиками.

---

## 🚀 Технологии

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker + Docker Compose
- Pytest
- Ruff (линтинг и автоформатирование)
- OpenAPI/Swagger
- Nationalize.io + REST Countries API

---

## 🔧 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/mertwec/Where-Are-You-From.git
cd Where-Are-You-From
```

### 2. Запуск в Docker
bash
```docker-compose up --build```
Приложение будет доступно по адресу:
📍 http://localhost:8000

📋 Примеры API
GET /names/?name=Maria
Возвращает список стран и вероятностей происхождения для указанного имени.

Если данные уже есть в базе и не старше суток — возвращается кэш.

Иначе — выполняется запрос к Nationalize и REST Countries.

GET /popular-names/?country=US
Возвращает топ-5 самых частых имен, связанных со страной.

🧪 Тестирование
Для запуска unit-тестов:

bash
Копіювати
Редагувати
pytest
Тестовая БД используется автоматически при запуске тестов (SQLite).

🔐 Аутентификация
Для доступа к защищённым эндпоинтам используется JWT-авторизация.
Токен можно получить через /auth/token.

🌱 Переменные окружения
Создайте .env файл на основе .env.example:

env
Копіювати
Редагувати
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=whereyoufrom
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://admin:admin@db:5432/whereyoufrom
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
🛠 Архитектура и структура
bash
Копіювати
Редагувати
app/
├── api/              # маршруты FastAPI
├── models/           # SQLAlchemy модели
├── schemas/          # Pydantic-схемы
├── crud/             # логика работы с БД
├── services/         # обёртки над внешними API
├── core/             # настройки, зависимости
tests/
docker-compose.yml
📌 Возможные улучшения
✅ Кэширование с Redis

✅ Асинхронные запросы к внешним API

✅ CI/CD через GitHub Actions

✅ Автоматическое форматирование и линтинг с Ruff

📚 Документация API
Swagger доступен по адресу:
🔗 http://localhost:8000/docs
ReDoc:
🔗 http://localhost:8000/redoc

