from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_root, name="api_root"),
    path("register/", views.register_user, name="register_user"),
    path("user/<int:user_id>/", views.get_user, name="get_user"),
]
