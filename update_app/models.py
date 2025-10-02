from django.db import models
from simple_history.models import HistoricalRecords
from enums import OGCServiceVersionEnum


# Helpermodels
class HistoricalRecordMixin:

    def save(self, without_historical: bool = False, *args, **kwargs):
        if without_historical:
            self.skip_history_when_saving = True
        try:
            ret = super().save(*args, **kwargs)
        finally:
            if without_historical:
                del self.skip_history_when_saving
        return ret

# Metadatamodels
class Metadatacontact(models.Model):
    pass

# Servicemodels
class CommonServiceInfo(models.Model):

    class Meta:
        abstract = True

class OgcService(CommonServiceInfo):  # CapabilitiesDocumentModelMixin, ServiceMetadata
    """Abstract Service model to store OGC service."""

    version: str = models.CharField(
        max_length=10,
        choices=OGCServiceVersionEnum.choices,
        editable=False,
        verbose_name=_("version"),
        help_text=_("the version of the service type as sem version"),
    )
    service_url: str = models.URLField(
        max_length=4096,
        editable=False,
        verbose_name=_("url"),
        help_text=_("the base url of the service"),
    )

    def get_service_type(self):
        """ only available in Python >= 3.10 
        match(self.__class__.__name__):
            case "WebMapService":
                return "WMS"
            case "WebFeatureService":
                return "WFS"
            case "CatalogueService":
                return "CSW"
            case _:
                return None
        """
        """ alternative: """
        if (self.__class__.__name__ == "WebMapService"):
            return "WMS"
        elif (self.__class__.__name__ == "WebFeatureService"):
            return "WFS"
        elif (self.__class__.__name__ == "CatalogueService"):
            return "CSW"
        else:
            return None

    class Meta:
        abstract = True

class WebMapService(HistoricalRecordMixin, OgcService):
    change_log = HistoricalRecords(
        related_name="change_logs",
        excluded_fields="search_vector",
        # bases=[AdditionalTimeFieldsHistoricalModel,],
    )

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

