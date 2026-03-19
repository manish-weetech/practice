# Task Management App — Notes

A REST API built with **FastAPI**, **SQLAlchemy (ORM)**, **PostgreSQL**, **Alembic (migrations)**, and **JWT authentication**.

---

## Project Structure

```
Task-Management-App/
├── main.py               # App entry point
├── alembic.ini           # Alembic config
├── migrations/           # Alembic migration files
│   └── env.py
├── requirement.txt
├── .env
└── src/
    ├── tasks/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── dtos.py
    │   ├── router.py
    │   └── controller.py
    ├── user/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── dtos.py
    │   ├── router.py
    │   └── controller.py
    └── utils/
        ├── __init__.py
        ├── db.py          # SQLAlchemy engine + session
        ├── settings.py    # Pydantic settings (reads .env)
        ├── helpers.py     # JWT + password helpers
        └── constent.py
```

---

## How I Created This Project

### 1. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

> `__init__.py` files are placed in each folder to define them as Python packages.

### 2. Install Dependencies

```bash
pip install fastapi uvicorn
pip install SQLAlchemy            # ORM
pip install psycopg2-binary       # PostgreSQL driver
pip install pydantic-settings     # Read .env values into app
pip install "pwdlib[argon2]"      # Password hashing
pip install pyjwt                 # JWT token generation & validation
pip install alembic               # Database migration tool
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_CONNECTION=postgresql://username:password@localhost:5432/your_db_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
EXP_TIME=3600
```

`pydantic-settings` reads these automatically via `src/utils/settings.py`.

### 4. Set Up Database Connection

`src/utils/db.py` creates the SQLAlchemy engine and session using the `DB_CONNECTION` from `.env`.

### 5. Set Up Alembic Migrations

```bash
alembic init migrations
```

Then edit `migrations/env.py` to import models and connect to the database:

```python
from src.utils.settings import settings
from src.user.models import UserModel
from src.tasks.models import TaskModel
from src.utils.db import Base

config.set_main_option("sqlalchemy.url", settings.DB_CONNECTION)
```

---

## Running the App

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Start the Server

```bash
uvicorn main:app --reload
```

App runs at: [http://localhost:8000](http://localhost:8000)  
Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Database Migrations (Alembic)

### Generate a new migration (after model changes)

```bash
alembic revision --autogenerate -m "describe your change here"
```

### Apply migrations to the database

```bash
alembic upgrade head
```

### Rollback last migration

```bash
alembic downgrade -1
```

---

## Key Concepts

| Tool | Purpose |
|---|---|
| `FastAPI` | Web framework for building APIs |
| `SQLAlchemy` | ORM — maps Python classes to DB tables |
| `Alembic` | Database migration tool for SQLAlchemy |
| `pydantic-settings` | Reads `.env` variables into the app |
| `pwdlib[argon2]` | Secure password hashing |
| `pyjwt` | JWT token creation and validation |
| `__init__.py` | Marks a folder as a Python package |
