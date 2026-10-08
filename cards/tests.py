from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User
from .models import Card


class CardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john', email='john@example.com', password='john1234')
        self.other = User.objects.create_user(
            username='mary', email='mary@example.com', password='mary1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.card = {'card_holder': 'john', 'card_type': 'CREDIT',
                     'card_number': '4111111111111111',
                     'expiry_month': 12, 'expiry_year': 2028}

    def test_add_card_stores_only_masked(self):
        r = self.client.post('/api/cards/', self.card, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['last4'], '1111')
        self.assertEqual(r.data['masked_number'], '**** **** **** 1111')
        self.assertNotIn('card_number', r.data)

    def test_cvv_rejected(self):
        r = self.client.post('/api/cards/', {**self.card, 'cvv': '123'}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_invalid_card_number(self):
        r = self.client.post('/api/cards/', {**self.card, 'card_number': '123'}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_invalid_month(self):
        r = self.client.post('/api/cards/', {**self.card, 'expiry_month': 13}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_view_only_own_cards(self):
        Card.objects.create(user=self.other, card_holder='mary', card_type='DEBIT',
                            masked_number='**** **** **** 9999', last4='9999',
                            expiry_month=1, expiry_year=2029)
        self.client.post('/api/cards/', self.card, format='json')
        r = self.client.get('/api/cards/')
        self.assertEqual(len(r.data), 1)

    def test_delete_card(self):
        r = self.client.post('/api/cards/', self.card, format='json')
        d = self.client.delete(f"/api/cards/{r.data['id']}/")
        self.assertEqual(d.status_code, 204)

    def test_cannot_delete_other_users_card(self):
        c = Card.objects.create(user=self.other, card_holder='mary', card_type='DEBIT',
                                masked_number='**** **** **** 9999', last4='9999',
                                expiry_month=1, expiry_year=2029)
        d = self.client.delete(f'/api/cards/{c.id}/')
        self.assertEqual(d.status_code, 404)