from django.urls import path, include

urlpatterns = [
    path('', include('user_auth_app.urls')),
    
    path('profiles/', include('profile_app.urls')),
    
    path('offers/', include('offers_app.urls')),
    
    path('orders/', include('orders_app.urls')),
    
    path('reviews/', include('reviews_app.urls')),
    
    # path('base-info/', BaseInfoView.as_view(), name='base-info'),
]