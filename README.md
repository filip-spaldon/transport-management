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

