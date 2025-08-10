Install uv for project https://docs.astral.sh/uv/getting-started/installation/

Init repo

```
uv sync
```

Create DB -> postgresql -> using psql

```
create database swida;
create user swida with encrypted password 'swida';
grant all privileges on database swida to swida;
```

Seed db

```
python manage.py migrate
python manage.py seed_demo
```

Run server

```
python manage.py runserver
```

Server available at http://localhost:8000/

Docs available at

```
http://localhost:8000//api/schema/swagger/
```

or

```
http://localhost:8000/api/schema/redoc/
```