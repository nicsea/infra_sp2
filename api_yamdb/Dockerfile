FROM python:3.7-slim

# Создать директорию вашего приложения.
RUN mkdir /app

# Скопировать содержимое директории / c локального компьютера
# в директорию /app.
COPY . /app

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r /app/requirements.txt --no-cache-dir

# Сделать директорию /app рабочей директорией. 
WORKDIR /app

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]