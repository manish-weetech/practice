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

This project uses a decoupled React Frontend and FastAPI Backend architecture. You will need two terminal windows.

### 1. Start the Backend (FastAPI)

Open your first terminal and start the Uvicorn server:

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

The Backend API runs at: [http://localhost:8000](http://localhost:8000)  
Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the Frontend (React Dashboard)

Open a second terminal and start the Vite development server:

```bash
cd frontend
npm run dev
```

The Web Dashboard runs at: [http://localhost:5173](http://localhost:5173)

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
| `__init__.py` | Marks a folder as a Python package |

---

## Retrieval-Augmented Generation (RAG) Flow

This application is equipped with RAG capabilities using **LangChain**, **Google Generative AI**, and **ChromaDB**. 

### RAG Architecture & Technologies
- **Document Loading & Processing**: Uses `langchain_community.document_loaders` (`PyPDFLoader` and `Docx2txtLoader`) to read text from `.pdf` and `.docx` files.
- **Text Splitting**: Uses `RecursiveCharacterTextSplitter` to divide large documents into smaller semantic chunks (1000 characters with 200 overlap).
- **Embeddings**: Uses `GoogleGenerativeAIEmbeddings` (`models/embedding-001`) from Google AI Studio to convert text chunks into dense vector embeddings.
- **Vector Database**: Uses `Chroma`, a local DB stored in `./chroma_db`, to save the embeddings for subsequent similarity search.
- **LLM**: Uses `ChatGoogleGenerativeAI` (`gemini-1.5-flash`) as the brain for question answering.

### API Endpoints
These endpoints are protected by the JWT authentication layer. You must pass `Authorization: Bearer <TOKEN>` in the headers.

#### 1. Upload a Document
- **Endpoint**: `POST /rag/upload`
- **Payload**: `multipart/form-data` with key `file`.
- **Flow**: The file temporarily saves to `./temp_files`, gets parsed by the relevant LangChain loader, split into chunks, embedded by Gemini, and stored in the local ChromaDB. The temporary file is then deleted.

#### 2. Ask a Question
- **Endpoint**: `POST /rag/ask`
- **Payload**: JSON `{ "question": "your question details here" }`
- **Flow**: The system converts the asked question into an embedding, performs a similarity search over ChromaDB to retrieve the most relevant chunks (top 5), injects them into a predefined prompt context, and queries the `ChatGoogleGenerativeAI` model to answer based solely on those contexts.
