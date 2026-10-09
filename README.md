# Credit Card Payment System

Django + FastAPI + MySQL project with JWT authentication.

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

## Tests
coverage run manage.py test --noinput
coverage report

## API Docs
- Django Swagger: http://127.0.0.1:8000/api/docs/
- FastAPI Swagger: http://127.0.0.1:8001/docs
- Postman collection: docs/Credit_Card_Payment_System.postman_collection.json

| Endpoint | Method | Service |
|---|---|---|
| /api/auth/register/ | POST | Django |
| /api/auth/login/ | POST | Django |
| /api/auth/logout/ | POST | Django |
| /api/auth/profile/ | GET | Django |
| /api/cards/ | GET, POST | Django |
| /api/cards/<id>/ | DELETE | Django |
| /api/payments/ | POST | FastAPI |
| /api/transactions/ | GET (filters) | Django |
| /api/transactions/export/ | GET (admin) | Django |

## DB Schema
**users_user**: id, username, email (unique), password (hashed), phone, is_staff, is_active
**cards_card**: id, user_id (FK), card_holder, card_type, masked_number, last4, expiry_month, expiry_year, created_at
**transactions_transaction**: id, user_id (FK), card_id (FK), amount, status (PENDING/SUCCESS/FAILED), description, created_at
**users_adminlog**: id, admin_id (FK), action, created_at

## Security
- No CVV or full card number stored
- Passwords hashed (Django PBKDF2)
- JWT authentication on all protected routes
- Input validation on all requests
- ORM and bound parameters prevent SQL injection

## Screenshots
See the submitted PDF (Task_Screenshots.pdf) for screenshots of every module.