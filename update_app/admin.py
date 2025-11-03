from django.contrib import admin
from .models import MetadataContact, WebMapService, WebFeatureService, Layer

admin.site.register(WebFeatureService)
admin.site.register(WebMapService)
admin.site.register(MetadataContact)
admin.site.register(Layer)