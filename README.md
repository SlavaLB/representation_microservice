## Запуск приложения

## Предварительно добавить в сервисе backend в .env переменные окружения
```
# База данных
DB_CONNECTOR="mariadb+asyncmy"
DB_USER=""

# Пароль к БД удаленный сервер
DB_PASSWORD=""

# Подключение к хостовой бд docker-compose настроен на дистрибутив Windows 
DB_HOST="host.docker.internal:3306"

# Имя БД
DB_NAME=""

```

* В корне проекта выполнить команду
```
docker compose up --build
```

## Ссылки

* [Главная страница](http://localhost)
* [Документация Backend](http://localhost/api/docs)
* [Документация Math model](http://localhost/math/docs)
* [Документация PLC service](http://localhost/plc/docs)
