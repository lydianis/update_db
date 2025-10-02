# update_app/urls.py

from django.urls import path
from update_app import views

urlpatterns =[
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
] 
