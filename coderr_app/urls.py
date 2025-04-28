from django.urls import path, include
from .views import BaseInfoView
from offers_app.views import OfferDetailView, OfferDetailRetrieveView

urlpatterns = [
    path('', include('user_auth_app.urls')),
    
    path('profiles/', include('profile_app.urls')),
    
    path('offers/', include('offers_app.urls')),
    path('offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offer-detail-retrieve'), 

    
    path('orders/', include('orders_app.urls')),
    
    path('reviews/', include('reviews_app.urls')),
    
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
]

