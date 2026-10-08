from django.test import TestCase
from rest_framework.test import APIClient

from .models import User


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {'username': 'john', 'email': 'john@example.com',
                     'phone': '9876543210', 'password': 'john1234'}

    def test_register(self):
        r = self.client.post('/api/auth/register/', self.data, format='json')
        self.assertEqual(r.status_code, 201)

    def test_password_is_hashed(self):
        self.client.post('/api/auth/register/', self.data, format='json')
        user = User.objects.get(username='john')
        self.assertNotEqual(user.password, 'john1234')

    def test_login_success(self):
        User.objects.create_user(username='john', password='john1234')
        r = self.client.post('/api/auth/login/',
                             {'username': 'john', 'password': 'john1234'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertIn('access', r.data)

    def test_login_wrong_password(self):
        User.objects.create_user(username='john', password='john1234')
        r = self.client.post('/api/auth/login/',
                             {'username': 'john', 'password': 'wrong'}, format='json')
        self.assertEqual(r.status_code, 401)

    def test_profile_without_token(self):
        r = self.client.get('/api/auth/profile/')
        self.assertEqual(r.status_code, 401)

    def test_profile_with_token(self):
        User.objects.create_user(username='john', password='john1234')
        login = self.client.post('/api/auth/login/',
                                 {'username': 'john', 'password': 'john1234'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login.data['access'])
        r = self.client.get('/api/auth/profile/')
        self.assertEqual(r.status_code, 200)