from django.urls import path, include
from rest_framework import routers
from accounts.views import LoginAPI, UserAPI, SignUpAPI

# router = routers.DefaultRouter()
# router.register(r'user', views.login)

urlpatterns = [
    path("api/auth/signUp", SignUpAPI.as_view()),
    path("api/auth/login", LoginAPI.as_view()),
    path("api/auth/loadMe", UserAPI.as_view()),
]
