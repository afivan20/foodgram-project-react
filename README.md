# praktikum_new_diplom

## Запуск проекта

В папке ```infra``` выполните команду ```docker-compose up```
При выполнении этой команде сервис frontend, описанный в ```docker-compose.yml``` подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/

### выполнить миграции
```
python manage.py makemigrations
python manage.py migrate
```
### добавить в базу данных ингредиенты
```
python manage.py importcsv
```