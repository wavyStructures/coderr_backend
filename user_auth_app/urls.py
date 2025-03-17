from django.urls import path, include
from user_auth_app.views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('registration/', RegisterView.as_view()),
]
