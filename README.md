# repmate

A self-hosted fitness web app that tracks workouts.

## Set Up

> For both Docker Compose and Native, copy `.env.example` to a `.env` file and replace the values

### Docker Compose Set Up

#### Prerequisites

- Docker

#### Set Up

```sh
# from the root of the repmate project
$ docker-compose up --build
# navigate to http://localhost:8000
```

### Native Local Set Up

#### Prerequisites

- Python >= 3.13
- PostgreSQL running locally with a `repmate` database and `repmate` user
  ```sql
  postgres=# CREATE USER repmate WITH ENCRYPTED PASSWORD 'your_password';
  postgres=# CREATE DATABASE repmate;
  postgres=# GRANT ALL PRIVILEGES ON DATABASE repmate TO repmate;
  postgres=# ALTER DATABASE repmate OWNER TO repmate;
  ```

#### Set Up

```sh
$ python3 -m venv ./venv && source ./venv/bin/activate
$ pip3 install -r requirements.txt
$ export FLASK_APP=repmate
$ flask db migrate
$ flask db upgrade
$ flask run
# navigate to http://127.0.0.1:5000
```
