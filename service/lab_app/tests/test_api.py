from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LabAppAPITestCase(APITestCase):
    def test_negative_unauthorized_user(self):
        url = reverse('results-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_positive_authorized_user(self):
        user = User.objects.create(username='User1')
        url = reverse('results-list')
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
