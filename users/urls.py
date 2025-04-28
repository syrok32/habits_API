from django.urls import path

from .views import CreateUser, MyTokenObtainPairView

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", CreateUser.as_view(), name="register"),
]
