from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import os
import pytest
from rest_framework_api_key.models import APIKey


@pytest.mark.django_db
class TestGettingNotams:
    URL_LIST = 'notams-list'

    def setup_method(self):
        self.api_key, self.key = APIKey.objects.create_key(name="test-key")

    def test_if_user_has_no_api_key_returns_403(self):
        client = APIClient()
        url = reverse(self.URL_LIST)
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_has_api_key_returns_200(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.key}')
        url = reverse(self.URL_LIST)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK