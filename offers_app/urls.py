from django.urls import path
from .views import OfferListView, OfferSingleView

urlpatterns = [
    path('', OfferListView.as_view(), name='offer-list'), 
    path('<int:pk>/', OfferSingleView.as_view(), name='offer-single-view'),
] 



