# fastapi-auth: A Modular Authentication & Authorization System

A production-ready, modular, and configurable authentication and authorization (RBAC) system for FastAPI. This repository provides a solid foundation for any project that requires secure user management.

## Features

- **JWT Authentication:** Stateless and secure token-based authentication using `python-jose`.
- **Role-Based Access Control (RBAC):** Protect endpoints based on user roles with simple, reusable dependencies.
- **Secure Password Hashing:** Uses `passlib` with `bcrypt`.
- **Modular Structure:** Cleanly separated layers for API, database, security, and configuration.
- **Configuration-Driven:** Manage all settings via a `.env` file using `pydantic-settings`.
- **Database Ready:** Uses SQLAlchemy for ORM, easily adaptable from SQLite to PostgreSQL.
- **Bootstrap Support:** Includes a command-line script to initialize the system with default roles and a super user.

---

## 1. Project Setup

Follow these steps to get the application running locally.

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (or pip)
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/imp-joshi/fastapi-auth.git
    cd fastapi-auth
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows PowerShell: .\.venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

4. **Configure environment variables:**
    Create a `.env` file in the project root by copying the example:

```bash
# (On Windows, use 'copy .env.example .env')
cp .env.example .env 
```

---

## 2. System Initialization (One-Time Setup)

Before running the API for the first time, you must initialize the database with the necessary roles and create the first super user.

**Run the bootstrap script:**

```bash
python scripts/bootstrap.py
```

This will create a `fastapi_auth.db` file and populate it. You can configure the default admin credentials in the script or via environment variables.

---

## 3. Running the Application

To start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

---

## 4. How to Use (For Developers)

Integrating this auth system into new endpoints is the primary goal of this repository. It's designed to be plug-and-play.

#### Location of Security Tools

All security dependencies are located in `app/api/deps.py`.

#### Scenario 1: Require a User to be Logged In

To protect an endpoint so that only authenticated users can access it, add `Depends(deps.get_current_user)` to your path operation function.

**Example:**

```python
# in any new router file, e.g., app/api/routers/chatbot.py
from fastapi import APIRouter, Depends
from app.api import deps
from app.db import models

router = APIRouter()

@router.get("/profile")
def get_user_profile(
    current_user: models.User = Depends(deps.get_current_user)
):
    # If the token is invalid or missing, the code below will never run.
    # The dependency will raise a 401 Unauthorized error automatically.
    return {"username": current_user.username, "roles": [role.name for role in current_user.roles]}
```

#### Scenario 2: Require a Specific Role

To protect an endpoint so that only users with a specific role (e.g., `admin-Super User`) can access it, use the `require_role` dependency.

**Example:**

```python
from fastapi import APIRouter, Depends
from app.api import deps

router = APIRouter()

# The dependency is added to the router to protect the endpoint
@router.get("/admin/settings", dependencies=[Depends(deps.require_role("admin-Super User"))])
def get_admin_settings():
    # This code will only execute if the user is authenticated AND has the "admin-Super User" role.
    # Otherwise, a 403 Forbidden error is automatically returned.
    return {"setting": "value", "message": "Welcome, Admin!"}
```

This provides a powerful, declarative way to secure your application's endpoints.