from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import os
import pytest
from rest_framework_api_key.models import APIKey

@pytest.fixture(scope='function')
def get_auth(django_db_blocker) -> tuple[APIKey,dict] :

    with django_db_blocker.unblock():
        api_key_obj, key = APIKey.objects.create_key(name='Test')
    header_key = {'HTTP_AUTHORIZATION': f'Api-Key {key}'}

    return api_key_obj, header_key

@pytest.mark.django_db
class TestNotamsPermissions:
    LIST_URL = reverse('notams-list')

    def test_if_user_has_no_api_key_returns_403(self):
        client = APIClient()
        response = client.get(self.LIST_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_has_api_key_returns_200(self, get_auth):
        client = APIClient()
        api_key_obj, header_key = get_auth
        client.credentials(**header_key)
        response = client.get(self.LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_has_revoked_api_key_returns_403(self, get_auth):
        client = APIClient()
        api_key_obj, header_key = get_auth
        api_key_obj.revoked = True
        api_key_obj.save()
        client.credentials(**header_key)
        response = client.get(self.LIST_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN