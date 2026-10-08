# Credit Card Payment System

Django + FastAPI + MySQL project with JWT authentication.

## Modules
1. User Authentication (Django): register, login (JWT), logout, protected routes
2. Card Management (Django): add, view, delete cards (masked, last 4 digits only)
3. Payment Processing (FastAPI): PENDING, then SUCCESS or FAILED
4. Transactions (Django): history, filters, admin CSV export
5. Admin Panel (Django): users, cards, transactions, daily summary
6. Database (MySQL): users, cards, transactions, admin logs

## Setup
1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r requirements.txt
4. Create MySQL database: credit_card_db
5. Create .env with DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DJANGO_SECRET_KEY
6. python manage.py migrate
7. python manage.py createsuperuser

## Run
- Django: python manage.py runserver (port 8000)
- FastAPI: uvicorn payment_service.main:app --port 8001

## API Endpoints
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/logout/
- GET /api/auth/profile/
- GET, POST /api/cards/
- DELETE /api/cards/<id>/
- POST /api/payments/ (FastAPI, port 8001)
- GET /api/transactions/?status=&min_amount=&max_amount=&start_date=&end_date=
- GET /api/transactions/export/ (admin only)