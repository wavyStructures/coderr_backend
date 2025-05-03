from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView, order_count, completed_order_count

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', order_count, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', completed_order_count, name='completed-order')
]


