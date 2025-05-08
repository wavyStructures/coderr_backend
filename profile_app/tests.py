from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class CustomerListTestCase(APITestCase):
    def test_customer_list_view(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
