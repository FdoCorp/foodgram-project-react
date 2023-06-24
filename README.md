![example workflow](https://github.com/FdoCorp/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Foodgram-project-react

Проект развёрнут по адресу: http://62.84.114.202/

## Описание

Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на 
публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин
скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии и их версии
В проекте использовались такие технологии, как:
- Python 3.11
- Django 4.0
- Django REST framework 3.14
- Nginx
- Docker
- Postgres

## Как запустить проект 
Загрузите проект с помощью SSH (на самом деле вам нужна только папка 'infra/)
```commandline
git clone git@github.com:FdoCorp/foodgram-project-react.git
```
Подключитесь ск своем серверу:
```bash
ssh <server_username>@<IP server>
```
Установите Docker на свой сервер

```bash
sudo apt install docker.io
```

Установить Docker Compose (for Linux)
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Создайте папку проекта и перейдите в неё
```bash
mkdir foodgram 
cd foodgram
```

Создайте env файл 
```bash
touch .env
```

Заполните файл .evn
```bash
DEBUG=False
SECRET_KEY=<ваш секретный ключ>
ALLOWED_HOSTS=<адрес сервера>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<пароль от базы>
DB_HOST=foodgram-db
DB_PORT=5432
```

Скопируйте файлы из папки infra на ваш удалённый сервер
```bash
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```

Запустите dokcer-compose
```bash
sudo docker-compose up -d
```

Создайте админскую учётку с помощью команды:
```bash
sudo docker exec -it app python manage.py createsuperuser
```

Заполните базу данных с помощью команды:
```bash
sudo docker exec -it foodgram-app python manage.py loaddata data/dump.json
```

## Автор
+ [Дмитрий Емельянов](https://github.com/FdoCorp)