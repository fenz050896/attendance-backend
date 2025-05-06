# Attendance Backend

A backend project used by Attendance Frontend

## Requirements
- Python v3.12.10
- Poetry v2.1.2
- MySQL v8.0
## Tech Stack
**Dependency Manager:** Poetry

**Backend:**
- Python: Flask, Flask-Alembic, Flask-SQLAlchemy, Flask-JWT-Extended


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- `JWT_SECRET_KEY`
- `DB_HOST`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_NAME`
- `DB_PORT`


## Installation
If you want to make virtual environment inside your project you can set it in poetry configuration:
```bash
  poetry config virtualenvs.in-project true
```

Install dependency using poetry

```bash
  poetry install
```
    
## Run the Project
Migrate the database:
```bash
  poetry run flask db upgrade
```

Run server (development):
```bash
  poetry run flask run --debug
```
