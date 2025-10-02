from django.shortcuts import render
from django.http import HttpResponse

"""
def home(request):
    return(HttpResponse("MrMap - Database Update"))
"""

def home(request):
    return render(request, "update_app/home.html")

def about(request):
    return(render(request, "update_app/about.html"))

