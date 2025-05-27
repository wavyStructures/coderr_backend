from django.urls import path
from .views import ProfileDetailView, CustomerListView, BusinessListView

urlpatterns = [
    path('customer/', CustomerListView.as_view(), name='customer-list'),
    path('business/', BusinessListView.as_view(), name='business-list'),
]

