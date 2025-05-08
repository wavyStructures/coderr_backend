from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class BaseInfoViewTest(APITestCase):
        def test_base_info_view(self):

        url = reverse('base-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



# class BaseInfoViewTest(APITestCase):
#     def test_base_info_view(self):
#         url = reverse('base-info')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

