from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView, order_count, completed_order_count

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail')
    ]

