import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Puppy
from ..serializers import PuppySerializer


# initialize the APIClient app
client = Client()

class TestHomeAPIView(APITestCase):
    def setUp(self):
        self.url = reverse("api:home_view") # use the view url
        self.home = factories.HomeFactory()
        user = factories.UserFactory()
        self.client.force_authenticate(user=user)

    def test_get(self):
        response = self.client.get(self.url)
        response.render()
        self.assertEquals(200, response.status_code)
        expected_content = {
                "id": str(self.home.id),
                "address_line_1": self.home.address_line_1,
                "address_line_2": self.home.address_line_2,
                "city": str(self.home.city),
                "state_province": str(self.home.state_province),
                "zip_code_postal_code": str(self.home.zip_code_postal_code),
                "country": str(self.home.country),
            }
        self.assertListEqual(expected_content, json.loads(response.content))