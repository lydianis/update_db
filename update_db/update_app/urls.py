from django.urls import path
from update_app import views

urlpatterns = [
    path("", views.home, name="home"),
]
