# update_app/urls.py

from django.urls import path
from update_app import views
from update_app.views import WebFeatureServiceView

urlpatterns =[
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("wfs/", WebFeatureServiceView.as_view(), name="wfs"),
] 
