from django.urls import path
from .views import ProfileDetailView, CustomerListView, BusinessListView

urlpatterns = [
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('customer/', CustomerListView.as_view(), name='customer-list'),
    path('business/', BusinessListView.as_view(), name='business-list'),
]

