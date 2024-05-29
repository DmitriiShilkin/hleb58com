# исходный образ, на основе которого создается образ
FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

# Здесь можно добавлять пакеты, которые необходимы для работы приложения
# RUN apt update && apt install -y python3-dev

# Рабочая директория
WORKDIR /app

# Копируем всё содержимое текущей папки в /app
COPY . /app

# Создаем виртуальное окружение:
RUN python -m venv /venv

# Активируем venv
ENV PATH="/venv/bin:$PATH"

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Даем право на выполнение скрипта
RUN chmod +x /app/run.sh

EXPOSE 8000
