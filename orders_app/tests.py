from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class OrderListViewTest(APITestCase):
    def test_order_list_view(self):
        url = reverse('order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrderCountTest(APITestCase):
    def test_order_count(self):
        url = reverse('order-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
                   
                    
                    