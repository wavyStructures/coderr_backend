from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ReviewListTest(APITestCase):
    def test_review_list(self):
        url = reverse('review-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

