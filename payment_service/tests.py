from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from fastapi.testclient import TestClient
from jose import jwt

from payment_service import main

client = TestClient(main.app)


def make_token(user_id=1, token_type='access'):
    return jwt.encode({'user_id': user_id, 'token_type': token_type},
                      main.SECRET_KEY, algorithm='HS256')


def mock_engine(card_found=True):
    conn = MagicMock()
    conn.execute.return_value.first.return_value = (1,) if card_found else None
    conn.execute.return_value.lastrowid = 7
    engine = MagicMock()
    engine.begin.return_value.__enter__.return_value = conn
    return engine


class PaymentTests(SimpleTestCase):
    body = {'card_id': 1, 'amount': 150.50, 'description': 'Test'}

    def test_no_token(self):
        r = client.post('/api/payments/', json=self.body)
        self.assertEqual(r.status_code, 401)

    def test_invalid_token(self):
        r = client.post('/api/payments/', json=self.body,
                        headers={'Authorization': 'Bearer abc'})
        self.assertEqual(r.status_code, 401)

    def test_negative_amount(self):
        r = client.post('/api/payments/', json={**self.body, 'amount': -5},
                        headers={'Authorization': 'Bearer ' + make_token()})
        self.assertEqual(r.status_code, 422)

    def test_card_not_found(self):
        with patch.object(main, 'engine', mock_engine(card_found=False)):
            r = client.post('/api/payments/', json=self.body,
                            headers={'Authorization': 'Bearer ' + make_token()})
        self.assertEqual(r.status_code, 404)

    def test_payment_success(self):
        with patch.object(main, 'engine', mock_engine()), \
             patch.object(main.random, 'choices', return_value=['SUCCESS']):
            r = client.post('/api/payments/', json=self.body,
                            headers={'Authorization': 'Bearer ' + make_token()})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['initial_status'], 'PENDING')
        self.assertEqual(r.json()['final_status'], 'SUCCESS')

    def test_payment_failed(self):
        with patch.object(main, 'engine', mock_engine()), \
             patch.object(main.random, 'choices', return_value=['FAILED']):
            r = client.post('/api/payments/', json=self.body,
                            headers={'Authorization': 'Bearer ' + make_token()})
        self.assertEqual(r.json()['final_status'], 'FAILED')