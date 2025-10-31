from django.contrib import admin
from .models import WebMapService, WebFeatureService

admin.site.register(WebFeatureService)
admin.site.register(WebMapService)