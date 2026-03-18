# Project Development Steps

This document outlines the steps taken to create this production-grade FastAPI backend.

## 1. Project Initialization
- Created the folder structure following the "Production Code" pattern.
- Initialized `requirements.txt` with essential libraries:
  - `fastapi`, `uvicorn`: Framework and Server.
  - `pydantic-settings`: Configuration management.
  - `sqlalchemy`, `psycopg2-binary`: Database ORM and driver.
  - `alembic`: Database migrations.
  - `python-jose`, `passlib`: Security and JWT.
- Created `.env.example` for environment variable management.

## 2. Folder Structure
```text
RBAC/
├── app/
│   ├── api/             # API Router and Endpoints
│   │   ├── api_v1/      # Versioned API routes
│   │   └── deps.py      # Dependency Injection
│   ├── core/            # Core config and security
│   ├── db/              # Database session and base
│   ├── crud/            # CRUD operations
│   ├── models/          # SQLAlchemy Models
│   ├── schemas/         # Pydantic Schemas
│   ├── main.py          # Application entry point
│   └── tests/           # Unit and Integration tests
├── alembic/             # Database migrations
├── .env                 # Environment variables
├── alembic.ini         # Alembic configuration
├── Dockerfile           # Docker configuration
└── requirements.txt     # Dependencies
```

## 3. Implementation Details
- **Core Config**: Uses `pydantic-settings` for type-safe environment variables.
- **Security**: JWT tokens for auth and `bcrypt` for password hashing.
- **RBAC**: Implemented via a `RoleChecker` dependency class that can be injected into any route.
- **CRUD**: Generic-style CRUD operations for Users and Items.
- **DTO Pattern**: Uses Pydantic schemas as Data Transfer Objects, with clear naming conventions:
  - `*Schema`: Used for request data (e.g., creation).
  - `*UpdateSchema`: Used for updating existing records.
  - `*ResponseSchema`: Used for returning data to the client.
- **API**: Versioned routes (`/api/v1`) with logical separation.
- **Migrations & Seeding**: Database schema and initial admin user are handled via Alembic migrations.
- **Registration**: Added a public `/api/v1/auth/register` endpoint for new users.

## 4. How to Run

### Initial Setup (Database Migrations)
Before running the server, you need to run the migrations to create the tables and the initial admin user:
```bash
./venv/bin/alembic upgrade head
```
Default Admin Credentials (created via migration):
- **Email**: `admin@example.com`
- **Password**: `adminpassword`

### Option 1: Using Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Local Development
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`.
4. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## 5. Directory Structure (Final)
```text
RBAC/
├── app/
│   ├── api/
│   │   ├── api_v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── items.py
│   │   │   │   └── users.py
│   │   │   └── api.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── crud_item.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── base.py
│   │   ├── base_class.py
│   │   └── session.py
│   ├── models/
│   │   ├── item.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── item.py
│   │   ├── msg.py
│   │   ├── token.py
│   │   └── user.py
│   └── main.py
├── alembic/
├── tests/
├── .env
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── notes.md
└── requirements.txt
```
