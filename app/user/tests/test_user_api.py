from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**param):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    # test public user API
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # tests creating user with valid payload is successful
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Testy McTesterson'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password[payload['password']])
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        # Tests creating user that already exists fails
        payload = {'email': 'test@test.com', 'password': 'test123'}
        create_user(**payload)
