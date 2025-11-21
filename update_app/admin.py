from django.contrib import admin
from .models import MetadataContact, WebMapService, WebFeatureService, Layer

@admin.register(WebMapService)
class WebMapServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'WebMapService')

admin.site.register(WebFeatureService)
admin.site.register(MetadataContact)
