# 📝 FastAPI Project Setup Notes (Manish)

## 🔹 1. System Setup (Ubuntu)

* Python already installed as:

```bash
python3 --version
```

👉 Output:

```bash
Python 3.12.3
```

* `python` command was not available by default (Ubuntu behavior)

---

## 🔹 2. Virtual Environment Setup

### Install venv package

```bash
sudo apt install python3.12-venv -y
```

---

### Create virtual environment

```bash
python3 -m venv venv
```

---

### Activate virtual environment

```bash
source venv/bin/activate
```

👉 After activation:

```bash
(venv) manish@manish:...$
```

---

### Verify environment

```bash
which python
```

👉 Output:

```bash
.../venv/bin/python
```

---

## 🔹 3. Install Dependencies

```bash
pip install fastapi uvicorn
```

---

## 🔹 4. Project Structure

```bash
Fast-API/
│
├── venv/          # Virtual environment
├── main.py        # Entry file
```

---

## 🔹 5. Basic FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Manish 🚀"}
```

---

## 🔹 6. Run Application

### Option A – uvicorn (recommended)

```bash
uvicorn main:app --reload
```

👉 Meaning:

* `main` → file name (`main.py`)
* `app` → FastAPI instance

### Option B – fastapi CLI (alternative)

```bash
fastapi dev main.py --reload
```

> This uses FastAPI's built-in CLI wrapper around Uvicorn.

---

## 🔹 7. Access Application

* API:

```
http://127.0.0.1:8000
```

* Swagger Docs:

```
http://127.0.0.1:8000/docs
```

---

## 🔹 8. Errors Faced & Fixes

### ❌ Error: `python not found`

👉 Fix:

* Use `python3`
* Or install:

```bash
sudo apt install python-is-python3
```

---

### ❌ Error: `ensurepip is not available`

👉 Fix:

```bash
sudo apt install python3.12-venv
```

---

### ❌ Error: `No module named fastapi`

👉 Reason:

* Virtual environment not activated

👉 Fix:

```bash
source venv/bin/activate
pip install fastapi
```

---

### ❌ Error: `Attribute "app" not found`

👉 Reason:

* `app = FastAPI()` missing or wrong name

👉 Fix:

```python
app = FastAPI()
```

---

## 🔹 9. Key Concepts Learned

### ✅ Virtual Environment

* Isolated environment per project
* Avoids dependency conflicts

---

### ✅ Python Commands

| Command | Meaning          |
| ------- | ---------------- |
| python3 | Python 3 version |
| python  | optional alias   |
| pip     | package manager  |

---

### ✅ FastAPI Run Concept

* Cannot run using `python main.py`
* Must use ASGI server (`uvicorn`)

---

## 🔹 10. Standard Workflow

```bash
cd Fast-API
source venv/bin/activate
uvicorn main:app --reload
```

---

# 🔥 Interview Summary

👉 You can say:

> I set up a FastAPI project using Python 3.12 on Ubuntu. I created a virtual environment using `venv`, installed dependencies like FastAPI and Uvicorn, and ran the app using Uvicorn as an ASGI server. I also handled common issues like missing venv packages and environment activation.

---

If you want next level 🚀
👉 I’ll convert this into **NestJS-like structure (routers, services, dependency injection)** which will match your backend experience perfectly.
