# YaMDb REST API v.1.1

Проект YaMDb собирает отзывы пользователей на различные произведения.
API предназначено для работы с проектом YaMDb. Через API доступно:

- Просмотр/добавление/редактирование/удаление произведений
- Просмотр/добавление/удаление жанров и категорий
- Просмотр/добавление/редактирование/удаление отзывов и комментариев
- Подписка на авторов, просмотр актуальных подписок
- Регистрация и управление пользователями
- Реализован импорт в базу данных из CSV-файлов

## Особенности

- Для авторизации используется JWT-токен, получаемый на основании кода подтверждения, направляемого на email пользователя

## Используемые технологии

- [Python]
- [Django REST framework]

## Локальная установка

Клонирование репозитория:
```sh
git clone git@github.com:gitgub_username/api_final_yatube.git
```

Переход в директорию проекта:
```sh
cd api_yamdb
```

Создание и активация виртуального окружения:
```sh
python3 -m venv env
```
```sh
source env/bin/activate
```

Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```

Для корректной работы в директории `infra` должен быть размещен файл `.env` с переменными окружения. Пример файла:

```python
SECRET_KEY=XXXXXXXXXXXXXXXXXXXXX 
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432  # порт для подключения к БД 
```

Выполнить миграции:
```sh
python3 manage.py migrate
```

Запустить проект:
```sh
python3 manage.py runserver
```

### Примеры запросов

Получение списка постов:
```http
GET /api/v1/titles/ HTTP/1.1
Host: 127.0.0.1:8000
```

Самостоятельная регистрация пользователя:
```http
POST /api/v1/auth/signup/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Content-Length: 66

{
    "username": "user1",
    "email": "example@example.com"
}
```
Получение JWT-токена
```http
POST /api/v1/auth/token/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Content-Length: 98

{
    "username": "user1",
    "confirmation_code": "bjx55v-32c5440acfa88214c8d8804a29ba2cc9"
}
```

Редактирование информации о произведении:
```http
PATCH /api/v1/titles/1/ HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer ****************
Content-Type: application/json
Content-Length: 150

{
    "name": "Мост через реку Квай",
    "genre": ["drama", "thriller"],
    "category": "movie",
    "description": "Рон Свонсон рекомендует"
}
```

Для импорта информации в базу данных из файлов CSV -файлов используется команда:
```sh
python3 manage.py import_csv all
```

## Создание контейнера Docker

Для создания контейнера нужно:
- перейти в директорию `infra`
- создать файл `.env`, указав данные переменных окружения (пример файла - выше)
- находясь в директории `infra`, где находится файл `docker-compose.yaml`, выполнить команду
``` sh
docker-compose up
```

Далее нужно выполнить следующие команды:
```sh
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

   [Python]: <https://www.python.org/>
   [Django REST framework]: <https://www.django-rest-framework.org/>