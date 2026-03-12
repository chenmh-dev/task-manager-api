# Task Manager API

A small but structured backend API for a task management system built with **Flask** and **SQLite**.

This project is designed to demonstrate **backend engineering practices**, including layered architecture, authentication, validation, resource-level authorization, and modular API design.

The goal of this project is not to build a production-ready product, but to implement a **clean and extensible backend architecture** for a real-world style system.

---

# Tech Stack

* Python 3.13
* Flask
* SQLite
* itsdangerous (token signing)
* Werkzeug password hashing

---

# Features

## Authentication

* User registration
* User login
* Token-based authentication
* Protected routes using `Bearer Token`

Endpoints:

```
POST /register
POST /login
GET  /me
```

---

## Projects

Users can manage their own projects.

Features:

* Create project
* List projects with pagination
* Get a single project
* Update project
* Delete project

Endpoints:

```
POST   /projects
GET    /projects
GET    /projects/<project_id>
PATCH  /projects/<project_id>
DELETE /projects/<project_id>
```

All project resources are **owned by the authenticated user**.

---

## Tasks

Each project can contain multiple tasks.

Features:

* Create task under a project
* List tasks within a project
* Get a task
* Update task
* Delete task
* Task status management

Task statuses:

```
todo
in_progress
done
```

Endpoints:

```
POST   /projects/<project_id>/tasks
GET    /projects/<project_id>/tasks
GET    /tasks/<task_id>
PATCH  /tasks/<task_id>
DELETE /tasks/<task_id>
```

Tasks are accessible only if the user owns the parent project.

---

## Task Comments

Users can add comments to tasks.

Features:

* Create comment on a task
* List comments of a task
* Delete own comment

Endpoints:

```
POST   /tasks/<task_id>/comments
GET    /tasks/<task_id>/comments
DELETE /task-comments/<comment_id>
```

Rules:

* A user can comment only on tasks within their own projects
* A user can delete **only their own comments**

---

# API Capabilities

Many list endpoints support:

* Pagination
* Sorting
* Keyword filtering

Example:

```
GET /projects?page=1&page_size=5&sort=created_at&order=desc
```

---

# Project Structure

```
app/
│
├── __init__.py        # Application factory
├── db.py              # Database connection and lifecycle
├── utils.py           # Unified API response helpers
├── errors.py          # Global error handlers
├── exceptions.py      # Custom API exceptions
├── validators.py      # Request validation utilities
├── decorators.py      # Authentication decorators
├── auth.py            # Token generation & verification
│
├── services/          # Business logic layer
│   ├── auth_service.py
│   ├── project_service.py
│   ├── task_service.py
│   └── task_comment_service.py
│
└── blueprints/        # API route modules
    ├── auth_routes.py
    ├── project_routes.py
    ├── task_routes.py
    └── task_comment_routes.py
```

---

# Architecture

The project follows a **layered backend architecture**:

```
Route Layer
    ↓
Service Layer
    ↓
Database
```

### Route Layer

Responsible for:

* HTTP request handling
* Parameter parsing
* Validation
* Calling services

Routes remain **thin and focused**.

---

### Service Layer

Responsible for:

* Business logic
* Database operations
* Resource-level authorization
* Domain rules

This separation keeps the code **maintainable and testable**.

---

# Design Principles

### Resource Ownership

Resources are scoped by ownership.

Examples:

* A user can only access **their own projects**
* Tasks must belong to a project owned by the user
* Comments can only be deleted by the author

---

### Token Payload Minimalism

Authentication tokens contain only minimal identity information:

```
user_id
```

The server **never trusts token payload alone** and always verifies data against the database.

---

### Unified API Responses

Successful responses:

```
{
  "success": true,
  "data": ...,
  "message": "..."
}
```

Error responses:

```
{
  "success": false,
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

---

### Validation Layer

All request validation is handled in `validators.py`, including:

* JSON parsing
* Required fields
* Optional fields
* Pagination
* Sorting
* Keyword filtering

---

# Running the Project

## 1. Clone the repository

```
git clone <repo_url>
cd task-manager-api
```

---

## 2. Install dependencies

```
pip install flask itsdangerous werkzeug
```

---

## 3. Run the server

```
python run.py
```

The API will start locally.

---

# Future Improvements

Possible extensions:

* Automated tests (pytest)
* PostgreSQL support
* SQLAlchemy ORM
* Docker support
* OpenAPI / Swagger documentation
* Role-based access control
* Refresh tokens
* Deployment setup

---

# Purpose of This Project

This project is built to demonstrate **backend engineering thinking**, including:

* API design
* layered architecture
* validation and error handling
* resource-level authorization
* modular code organization

It serves as a **learning and portfolio project** for backend development.
