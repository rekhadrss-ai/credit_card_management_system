from fastapi.middleware.cors import CORSMiddleware
import os
import random
from decimal import Decimal
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DB_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD'))}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DB_URL)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

app = FastAPI(title="Payment Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
bearer = HTTPBearer()


def get_current_user_id(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if payload.get("token_type") != "access":
        raise HTTPException(status_code=401, detail="Not an access token")
    return int(payload["user_id"])


class PaymentRequest(BaseModel):
    card_id: int
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    description: str = ""

@app.get("/", tags=["home"], summary="Home")
def home():
    return {
        "message": "Credit Card Payment API is running",
        "service": "FastAPI Payment Service",
        "version": "1.0.0",
        "docs": "/docs",
    }

@app.get("/health", tags=["home"], summary="Health check")
def health():
    return {"status": "ok"}


@app.post("/api/payments/")
def make_payment(data: PaymentRequest, user_id: int = Depends(get_current_user_id)):
    # Step 1: check the card belongs to this user, then save as PENDING
    with engine.begin() as conn:
        card = conn.execute(
            text("SELECT id FROM cards_card WHERE id = :cid AND user_id = :uid"),
            {"cid": data.card_id, "uid": user_id},
        ).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        result = conn.execute(
            text(
                "INSERT INTO transactions_transaction "
                "(user_id, card_id, amount, status, description, created_at) "
                "VALUES (:uid, :cid, :amt, 'PENDING', :desc, UTC_TIMESTAMP(6))"
            ),
            {"uid": user_id, "cid": data.card_id, "amt": data.amount, "desc": data.description},
        )
        txn_id = result.lastrowid

    # Step 2: simulate the payment (70% success, 30% failure)
    final_status = random.choices(["SUCCESS", "FAILED"], weights=[70, 30])[0]

    # Step 3: update the status
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE transactions_transaction SET status = :s WHERE id = :id"),
            {"s": final_status, "id": txn_id},
        )

    return {
        "transaction_id": txn_id,
        "card_id": data.card_id,
        "amount": str(data.amount),
        "initial_status": "PENDING",
        "final_status": final_status,
    }