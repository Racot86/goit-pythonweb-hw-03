# Dockerfile
FROM python:3.10-slim

# Створюємо робочий каталог
WORKDIR /app

# Копіюємо файли
COPY . .

# Встановлюємо залежності, якщо вони є (опціонально)
# RUN pip install -r requirements.txt

# Відкриваємо порт
EXPOSE 3000

# Команда запуску
CMD ["python", "main.py"]