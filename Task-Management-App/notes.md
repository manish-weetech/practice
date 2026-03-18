# Task Management App — Notes

A production-ready REST API built with **FastAPI**, **SQLAlchemy (ORM)**, **PostgreSQL**, **Alembic (migrations)**, and **Docker**.

---

## Project Structure

```
Task-Management-App/
├── main.py               # App entry point (middleware, exceptions, logging)
├── Dockerfile            # Multi-stage production build
├── docker-compose.yml    # App & Database orchestration
├── alembic.ini           # Alembic config
├── migrations/           # Alembic migration files
├── requirement.txt       # Consolidated dependencies
├── .env                  # Environment variables
└── src/
    ├── tasks/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── dtos.py
    │   ├── router.py      # Path: /tasks
    │   └── service.py     # Task business logic
    ├── user/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── dtos.py
    │   ├── router.py      # Path: /user
    │   └── service.py     # User business logic
    └── utils/
        ├── __init__.py
        ├── db.py          # Database session management
        ├── settings.py    # Configuration management
        ├── helpers.py     # Auth & Password utilities
        ├── exceptions.py  # Global error handling
        └── logging_config.py
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
pip install -r requirement.txt
```

#### Key Libraries Used:
| Tool | Purpose |
|---|---|
| `FastAPI` | Web framework for building APIs |
| `SQLAlchemy` | ORM — maps Python classes to DB tables |
| `Alembic` | Database migration tool for SQLAlchemy |
| `pydantic-settings` | Reads `.env` variables into the app |
| `pwdlib[argon2]` | Secure password hashing |
| `pyjwt` | JWT token creation and validation |

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_CONNECTION=postgresql://postgres:password@localhost:5432/task_db
SECRET_KEY=your_generated_secret_key
ALGORITHM=HS256
EXP_TIME=1440  # 24 hours in minutes
```

### 4. Set Up Alembic Migrations

```bash
# Initialize alembic
alembic init migrations

# Generate first migration
alembic revision --autogenerate -m "initial migration"

# Apply to database
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

---

## Running the App

### 1. Local Development (Non-Docker)

```bash
source venv/bin/activate
uvicorn main:app --reload
```

App runs at: [http://localhost:8000](http://localhost:8000)  
Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Production Ready (Docker)

```bash
# Start all services (App + PostgreSQL)
# This will now automatically run migrations on startup!
docker compose up -d --build
```

---

## Key Features & Improvements

- **Service Layer Architecture**: Business logic is separated into `service.py`, keeping routers clean.
- **Global Error Handling**: Custom exceptions in `src/utils/exceptions.py` handle all errors consistently.
- **Structured Logging**: Unified logging configuration for debugging and monitoring.
- **Standardized Auth**: Secure JWT handling integrated with FastAPI's `OAuth2PasswordBearer`.
- **Dockerized**: Multi-stage build for efficient production deployment.

---

## Project Flow (Request Lifecycle)

When a request (e.g., `POST /tasks/`) hits the API, it follows this flow:

1.  **`main.py`**: The request enters, passing through **CORS middleware** and **logging**.
2.  **`src/utils/helpers.py`**: If the route is protected, `get_current_user` extracts and validates the JWT.
3.  **`router.py`**: The router receives the validated request and calls the appropriate method in `service.py`.
4.  **`service.py`**: Business logic is executed here. It interacts with the **`models.py`** and performs database operations via SQLAlchemy.
5.  **`exceptions.py`**: If anything goes wrong (e.g., Task Not Found), a custom exception is raised and caught by the global handler to return a clean error response.
6.  **Response**: The result is returned as a JSON object, validated against the **`dtos.py`** (Pydantic models).

---

## Summary of Refactoring Changes

| From (Prototype) | To (Production Ready) | Why? |
|---|---|---|
| `controller.py` | `service.py` | Better separation of concerns and testability. |
| Manual Token Parsing | `OAuth2PasswordBearer` | Industry standard security and Swagger support. |
| In-line Exception handling | Global Exception Handler | Dry code and consistent API error responses. |
| Simple Print/None | Structured Logging | Easier monitoring and debugging in production. |
| Manual DB setup | Docker + Alembic | Reliable, reproducible environments and schema versioning. |

---

## Detailed Concepts & Logic

### 1. Global Exception Handlers (`main.py`)
Instead of `try-except` blocks everywhere, we use a global safety net:
- **`AppException`**: Catches errors we expect (e.g., "User not found"). It returns a clean JSON response with the correct status code.
- **`Exception`**: A catch-all for unexpected bugs. It logs the full error for developers but sends a generic "Internal Server Error" to the user for security.

### 2. API Tags (`tags=["Tasks"]`)
Used in `app.include_router`. It groups your endpoints in the **Swagger UI (/docs)**. Without tags, all routes are in one long list; with tags, they are organized into collapsible sections (e.g., "Tasks", "Users").

### 3. `@staticmethod` (Service Layer)
Used for methods that don't need to access "state" (`self`). 
- **Purpose**: It allows us to call `UserService.register()` directly without creating an instance `service = UserService()`. 
- **Benefit**: It's more memory-efficient and keeps related logic organized inside a class.

### 4. OAuth2 & JWT Mechanics (`src/utils/helpers.py`)
- **`OAuth2PasswordBearer(tokenUrl="user/login")`**: 
    - **Mechanic**: Acts as a gatekeeper. It automatically looks for the `Authorization: Bearer <token>` header. If missing, it returns a `401 Unauthorized` before your code even runs.
    - **Documentation**: The `tokenUrl` tells Swagger where to send credentials when you click the "Authorize" button.
- **`get_current_user`**: 
    - This is a **Dependency**. When a route uses `Depends(get_current_user)`, FastAPI automatically extracts the token, decodes it, verifies the user in the DB, and passes the `User` object directly into your function.

### 5. SQLAlchemy Session Management (Updates)
In the refactored `update_task`, we removed `db.add()`. This is because SQLAlchemy uses **Dirty Tracking**:
- When you fetch an object (e.g., `db.query(...).first()`), it is already attached to the session.
- Any changes you make to that object are tracked automatically.
- Calling `db.commit()` is enough for SQLAlchemy to detect the changes and run the `UPDATE` query. 
- `db.add()` is only strictly necessary for **new** records that haven't been saved yet.

### 6. Multi-Stage Dockerfile
The project uses a **Multi-Stage Build** to ensure the production image is small and secure:
- **`builder` stage**: Installs compilers (`gcc`) and system libraries needed to build dependencies.
- **Run stage**: Starts with a fresh image. It only copies the *final* installed packages from the builder.
- **Result**: You get a production image that doesn't contain heavy build tools, making it faster to deploy and more secure against attackers.
- **`ENV PYTHONUNBUFFERED 1`**: Ensures your Python logs are sent straight to the container logs without buffering, which is critical for real-time monitoring.

### 7. Docker Compose (`docker-compose.yml`)
Docker Compose is an **orchestration tool** that allows you to run multiple containers (e.g., your App and your Database) together with a single command. 

- **`services`**: Defines the different containers in your stack.
    - **`db`**: Runs the official PostgreSQL image. It's the persistent storage for your app.
    - **`app`**: Builds and runs your FastAPI application using the `Dockerfile`.
- **`depends_on`**: Tells Docker to start the `db` *before* starting the `app`. This ensures the database is ready when the app tries to connect.
- **`volumes`**: We use a named volume (`postgres_data`) to ensure that even if you stop or delete your containers, your **database data is not lost**. It is stored safely on your host machine.
- **`environment`**: This is where we securely pass settings like `DB_CONNECTION` and `SECRET_KEY` into the containers. Note that for the `app`, the database host is simply `db` (the name of the service), not `localhost`.

> [!IMPORTANT]
> **Is it okay to hardcode ENV values?** 
> For **local development**, it's okay for convenience. But for **production**, you should **never** hardcode secrets (passwords, JWT keys) in `docker-compose.yml`. Instead, use the `${VARIABLE}` syntax. Docker Compose will automatically look for these values in your `.env` file (locally) or your **system environment/secrets manager** (in production).

### 8. Production Env Injection (No .env file!)
In production, we don't use `.env` files for security. Variables are injected via:
- **CI/CD Secrets**: Stored in GitHub/GitLab settings and injected during deployment.
- **Cloud Vaults**: Services like AWS Secrets Manager or GCP Secret Manager.
- **Orchestrators**: Kubernetes Secrets or Docker Swarm Secrets.
- **System Exports**: Variables set directly on the production host machine using `export VAR=value`.

#### GitHub Actions Example:
In your CI/CD workflow, you map your secrets to environment variables that Docker Compose can read:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Server
        run: |
          # We pass the secret to the server/docker environment
          export POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}
          docker-compose up -d --build
```

Docker Compose then sees `${POSTGRES_PASSWORD}` in the system environment and injects it into the container.


### 9. Automated Migrations in Production
We use a `start.sh` script to run `alembic upgrade head` on every startup.

**Is this good for production?**
- **Pros**: Highly convenient, guarantees code/DB sync, prevents "missing column" errors.
- **Cons**: Can cause issues if 10+ instances start at once; long migrations can block app startup.
- **Verdict**: Excellent for small-to-mid scale. For high-scale, run migrations as a separate step in your CI/CD pipeline (e.g., a "Job") *before* the app deploy.