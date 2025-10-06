from django.shortcuts import render
from django.http import HttpResponse
from update_app.models import WebFeatureService
from django.views import View
import requests


PROXIES ={
    'http_proxy': 'http://xxx:8080',
    'https_proxy': 'http://xxx:8080',
} 

"""
def home(request):
    return(HttpResponse("MrMap - Database Update"))
"""

def home(request):
    return render(request, "update_app/home.html")

def about(request):
    return(render(request, "update_app/about.html"))


class WebFeatureServiceView(View):
    def get(self, request):
        print("WFS")
        return HttpResponse("result")
