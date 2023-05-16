# Запуск сервиса ETL локально
## Подготовка окружения
1) Убедитесь что у вас установлен Docker выполнив команду:

    `$ docker -v`

    если в результате вы получили сообщение `docker: command not found`, установите приложение согласно [официальной инструкции](https://docs.docker.com/engine/install/)

2) настройка Postgres:
    ```
    $ docker run -d --name postgres -p 5432:5432 -v $HOME/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=<password> -e POSTGRES_USER=<user> -e POSTGRES_DB=<db_name> postgres:13

    $ docker exec -it postgres pg_restore -U <user> -P <password> -d <db_name> < movies_database.dump
    (db_dump вынайдёте в списке файлов)

    $ docker container stop postgres
    ```

3) Настройка Elasticsearch:
    ```
    $ docker run -d --name elastic -p 9200:9200 -v $HOME/elasticsearch/data:/usr/share/elasticsearch/data -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms2g -Xmx2g" elasticsearch:7.7.0

    $ curl -XPUT http://127.0.0.1:9200/{index_name} -H 'Content-Type: application/json' -d @index_scheme.json (index_name - имя создаваемого вами индекса)

    $ docker container stop elastic
    ```

4) Запустите docker-compose файл:
    ```
    $ docker-compose.yml up
    ```
