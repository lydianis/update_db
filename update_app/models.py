from django.db import models
from simple_history.models import HistoricalRecords

# Metadatamodels
class Metadatacontact(models.Model):
    pass

# Servicemodels
class CommonServiceInfo(models.Model):
    pass

class OgcService(CommonServiceInfo):  # CapabilitiesDocumentModelMixin, ServiceMetadata
    pass

class WebMapService(OgcService):  # HistoricalRecordMixin
    pass

class WebFeatureService(OgcService):  # HistoricalRecordMixin
    pass

class CatalogueService(OgcService):  # HistoricalRecordMixin
    pass

class ServiceElement(CommonServiceInfo):  #CapabilitiesDocumentModelMixin
    """Abstract model class to generalize some fields and functions for layers and feature types"""
    pass

class Layer(ServiceElement):  #HistoricalRecordMixin, LayerMetadata, Node
    pass

class FeatureType(ServiceElement):  #HistoricalRecordMixin, FeatureTypeMetadata
    pass

