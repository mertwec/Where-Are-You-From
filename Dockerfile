FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и код
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Инициализация базы перед запуском сервера
CMD ["bash", "-c", "python3 _init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]