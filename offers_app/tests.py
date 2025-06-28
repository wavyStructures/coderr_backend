from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Offer

class OfferListViewTest(APITestCase):
    def test_offer_list_view(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class OfferDetailsViewTest(APITestCase):
    def setUp(self):
        def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.offer = Offer.objects.create(title="Test Offer", description="Test", user=self.user)

    def test_offer_detail_view(self):
        url = reverse('offer-details-view', args=[self.offer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
