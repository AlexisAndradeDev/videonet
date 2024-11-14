from django.urls import path
from .views import register, login_view, delete_account, logout_view

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("delete_account/", delete_account, name="delete_account"),
    path("logout/", logout_view, name="logout"),
]