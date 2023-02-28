# Minimal async FastAPI + PostgreSQL template

## Features

- [x] Postgresql database under `asyncpg`
- [x] [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations
- [x] Very minimal project structure yet ready for quick start building new apps
- [x] Refresh token endpoint (not only access like in official template)
- [x] Two databases in docker-compose.yml (second one for tests) and ready to go Dockerfile with [Uvicorn](https://www.uvicorn.org/) webserver
- [x] [Poetry](https://python-poetry.org/docs/) and Python 3.11 based


## Quickstart

### 1. Install cookiecutter globally and cookiecutter this project

```bash
pip install cookiecutter

# And cookiecutter this project :)
cookiecutter https://github.com/8thgencore/fastapi-postgres-async-template

```

### 2. Install dependecies with poetry or without it

```bash
cd project_slug

## Poetry install (python3.11)
poetry install

## Optionally there is also `requirements-dev.txt` file
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```
