from django.urls import path
from .views import ProfileDetailView, CustomerListView, BusinessListView

urlpatterns = [
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]