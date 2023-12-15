from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from MusicStore.serializers import CustomUserSerializer
from .views import RegisterView

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_registration_success(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'password_confirm': 'testpassword'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_failure(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'password_confirm': 'wrongpassword'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CustomCheckTests(TestCase):
    def test_is_admin_check(self):
        from musicstore.checks import IsAdmin
        user = User.objects.create(username='admin', is_staff=True)
        self.assertTrue(IsAdmin().has_permission(None, None, user))

    def test_is_admin_check_failure(self):
        from musicstore.checks import IsAdmin
        user = User.objects.create(username='regular_user', is_staff=False)
        self.assertFalse(IsAdmin().has_permission(None, None, user))

class SerializerValidationTests(TestCase):
    def test_email_validation(self):
        data = {'username': 'testuser', 'email': 'invalidemail', 'password': 'testpassword', 'password_confirm': 'testpassword'}
        serializer = CustomUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_username_uniqueness(self):
        user = User.objects.create(username='existing_user', email='test@example.com', password='testpassword')
        data = {'username': 'existing_user', 'email': 'newuser@example.com', 'password': 'testpassword', 'password_confirm': 'testpassword'}
        serializer = CustomUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
