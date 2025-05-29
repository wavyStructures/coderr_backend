from django.urls import path, include
from user_auth_app.views import LoginView, RegisterView, TestErrorView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('registration/', RegisterView.as_view()),
    path("test-error/", TestErrorView.as_view(), name="test-error"),
]
