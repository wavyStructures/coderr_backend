from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model

class OrderListViewTest(APITestCase):
    def setUp(self):
        """
        Sets up the test by creating a test user and authenticating the test client as that user.
        """
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.force_authenticate(user=self.user)
        
    def test_order_list_view(self):
        """
        Tests that the order list view returns a 200 status code when a GET
        request is made to it. 
        """
        url = reverse('order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderCountTest(APITestCase):
    def test_order_count(self):
        """
        Tests that the order count view returns a 200 status code when a GET
        request is made to it for a specific business user.
        """

        url = reverse('order-count', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
                   
                    
                    