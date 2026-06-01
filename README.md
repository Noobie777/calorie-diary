# Calorie Diary API

A production-oriented calorie tracking backend built with FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, refresh token rotation, rate limiting, automated testing, and CI/CD.

## Features

### Authentication

- User registration
- JWT access tokens
- Refresh token support
- Refresh token rotation
- Token revocation
- Logout functionality

### Food Logging

- Create food logs
- Retrieve food logs
- User-specific log isolation

### Query Features

- Filtering
- Sorting
- Pagination

### Security

- Password hashing with bcrypt
- JWT authentication
- Refresh token rotation
- Login rate limiting
- Signup rate limiting

### Database

- PostgreSQL (Neon)
- SQLAlchemy ORM
- Alembic migrations
- Optimized indexing

### Testing

- Authentication tests
- Refresh token tests
- Logout tests
- Log CRUD tests
- Filtering tests
- Sorting tests

### DevOps

- Docker support
- GitHub Actions CI
- Automated test execution on push

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic

### Authentication

- JWT
- Passlib
- OAuth2 Password Flow

### Testing

- Pytest
- FastAPI TestClient

### Infrastructure

- Docker
- GitHub Actions
- Neon PostgreSQL

---

## Project Structure
```text
calorie-diary/
├── routes/
│   ├── users.py
│   └── logs.py
├── tests/
├── alembic/
├── models.py
├── schemas.py
├── crud.py
├── auth.py
├── database.py
├── config.py
├── limiter.py
├── main.py
└── requirements.txt 
```
---

## Authentication Flow

```text
Signup
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
Authenticated Requests
   ↓
Access Token Expires
   ↓
Refresh Endpoint
   ↓
New Access Token + New Refresh Token
   ↓
Old Refresh Token Revoked
``` 

---

## Running Locally

### Clone repository

```bash 
git clone https://github.com/Noobie777/calorie-diary.git 
cd calorie-diary
``` 

### Create virtual environment

```bash 
python -m venv venv 
source venv/bin/activate
``` 

### Install dependencies

```bash 
pip install -r requirements.txt
``` 

### Configure environment variables

Create a .env file:

```env 
DATABASE_URL=your_database_url 
SECRET_KEY=your_secret_key
``` 

### Run migrations

```bash 
alembic upgrade head
``` 

### Start server

```bash 
uvicorn main:app --reload 
```
Swagger UI:

```text 
http://127.0.0.1:8000/docs
``` 

---

## Running Tests

```bash 
pytest
``` 

Current Status:

```text 
All automated tests passing
``` 

---

## Future Improvements

- React frontend
- Dashboard analytics
- AI-assisted calorie estimation
- Natural language food logging
- Meal image analysis
- Production deployment
- Monitoring and observability
