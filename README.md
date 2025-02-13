# tracklift

## Local Set Up

### Prerequisites

- Python >= 3.13
- PostgreSQL running locally with a `tracklift` database and `tracklift` user
  ```sql
  postgres=# CREATE USER tracklift WITH ENCRYPTED PASSWORD 'your_password';
  CREATE ROLE
  postgres=# CREATE DATABASE tracklift;
  CREATE DATABASE
  postgres=# GRANT ALL PRIVILEGES ON DATABASE tracklift TO tracklift;
  GRANT
  postgres=# ALTER DATABASE tracklift OWNER TO tracklift;
  ALTER DATABASE
  ```

### Set Up Commands

```sh
$ cd <TRACKLIFT_DIR>
$ python3 -m venv ./venv && source ./venv/bin/activate
$ pip3 install -r requirements.txt
$ export FLASK_APP=tracklift
$ export SECRET_KEY='your_secret_key'
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask run
```
