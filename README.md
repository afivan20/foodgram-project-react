![example workflow](https://github.com/afivan20/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Документация к проекту Foodgram(v1):

## Описание
Foodgram - это книга рецептов, здесь вы можете обмениваться кулинарными изысками, выбирать понравившиеся и сохранять их. Foodgram поможет составить вам список покупок для любого блюда. <br>
http://django-foodgram.ru

## Технологии
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)<br>
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)<br>
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)<br>
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)<br>
Документация со всеми эндпоинтами доступна здесь - http://django-foodgram.ru/api/docs/redoc.html <br>
Инфраструктура описана в <b>docker-compose</b> `/infra/docker-compose.yml`

## Как запустить проект на удаленном сервере:
### Подготовить сервер ###
```
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
```
- Установим докер
```
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
```
- Установить docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Apply executable permissions to the binary:
```
sudo chmod +x /usr/local/bin/docker-compose
```
### Настройка инфраструктуры
-  Перенести файлы `docker-compose.yaml` и `default.conf` на удаленный сервер.
- Прописать секреты:
<dl>
<dt>для удаленного сервера:</dt>
HOST<br>
USER<br>
SSH_PASSWORD<br>

<dt>для базы данных:</dt>
DB_ENGINE<br>
DB_NAME<br>
POSTGRES_USER<br>
POSTGRES_PASSWORD<br>
DB_HOST<br>
DB_PORT<br>

<dt>для логина в DockerHub:</dt>
DOCKER_USERNAME<br>
DOCKER_PASSWORD<br>

<dt>для почтового сервера</dt>
EMAIL_SMTP<br>
EMAIL<br>
EMAIL_PASSWORD<br>
</dl>

- Поднять контейнеры:
```
sudo docker-compose up -d
```
- Выполнить миграции на удаленном сервере:
```
sudo docker-compose exec backend python manage.py makemigrations; sudo docker-compose exec backend python manage.py migrate
```
- Подключить статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
- Наполнить базу данных ингредиентами:
```
docker-compose exec backend python manage.py importcsv
```
### Получить SSL сертификат
для получения серфтифика воспользоваться [certbot](https://certbot.eff.org) от Let’s Encrypt
и прописать полученнный сертификат в `default.conf`

### Дополнительные команды:
- Создать Супер Пользовтеля:
```
docker-compose exec backend python manage.py createsuperuser
```
- Посмотреть структуру проекта на сервере:
```
sudo docker-compose run backend bash
```
- Удалить запущенные контейнеры:
```
docker-compose down -v
```
- Остановить все запущенные контейнеры:
```
sudo docker stop $(sudo docker ps -a -q)
```
- Удалить все неиспользуемые контейнеры и образы:
```
docker system prune -a
```
- Скачать образы с DockerHub:
```
docker pull afivan20/foodgram_backend:latest
```
```
docker pull afivan20/foodgram_frontend:latest
```
### Автор
_Иван Афанасьев, python-devloper_