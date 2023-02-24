# BACKEND

### Init migrations

```
alembic init -t async migrations
```

### Create migrations

```
alembic revicions --autogenerate -m 'revision message'
```

### Run migrations

```
alembic upgrade heads
```

### Downgrade

```
alembic downgrade <hash or 'base'>
```

### runtests (don't forget about database env)

```
pytest -v
```

### run app (don't forget about database env)

```
python -m backend
```

### run app with gunicorn (don't forget about database env)

```
gunicorn --bind 0.0.0.0:80 --workers 2 --worker-class uvicorn.workers.UvicornWorker --access-logfile=/var/log/access.log backend.app:app
```

### run app in docker container

```
/root/.local/bin/poetry run gunicorn --bind 0.0.0.0:80 --workers 2 --worker-class uvicorn.workers.UvicornWorker --access-logfile=/var/log/access.log backend.app:app
```
