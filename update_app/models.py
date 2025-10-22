from uuid import uuid4

from django.db import models
from simple_history.models import HistoricalRecords
from .enums import OGCServiceVersionEnum

def xml_backup_file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/xml_documents/<id>/<filename>
    return 'xml_documents/{0}/{1}'.format(instance.pk, filename)

class WebMapService(models.Model):
    """Model for WMS capabilities document."""

    xml_backup_file = models.FileField(verbose_name=("xml backup"),
                                       help_text=(
                                           "the original xml as backup to restore the xml field."),
                                       upload_to=xml_backup_file_path,
                                       editable=False,
                                       )
    
    history = HistoricalRecords()

    version: str = models.CharField(
        max_length=10,
        choices=OGCServiceVersionEnum.choices,
        editable=False,
        verbose_name=("version"),
        help_text=("the version of the service type as sem version"),
    )

    # name =  id or identifier or name ???

    title: str = models.CharField(max_length=1000,
                                  verbose_name=("title"),
                                  help_text=(
                                      "a short descriptive title for this service"),
                                  default="")
    abstract = models.TextField(verbose_name=("abstract"),
                                help_text=(
                                    "brief summary of the content of this service"),
                                blank=True,
                                default="")


class Layer(models.Model):
    """Model for single WMS Layers"""
    name = models.Charfield(max_length=200, unique=True)
    title: str = models.CharField(max_length=1000,
                                  verbose_name=("title"),
                                  help_text=(
                                      "a short descriptive title for this metadata"),
                                  default="")
    abstract = models.TextField(verbose_name=("abstract"),
                                help_text=(
                                    "brief summary of the content of this metadata."),
                                blank=True,
                                default="")
    
    def __str__(self):
        return self.name


class WebFeatureService(models.Model):
    """Model for WFS capabilities document."""
    """TODO: combine with WMS to inherit from OgcService"""

    xml_backup_file = models.FileField(verbose_name=("xml backup"),
                                       help_text=(
                                           "the original xml as backup to restore the xml field."),
                                       upload_to=xml_backup_file_path,
                                       editable=False,
                                       )
    
    history = HistoricalRecords()

    version: str = models.CharField(
        max_length=10,
        choices=OGCServiceVersionEnum.choices,
        editable=False,
        verbose_name=("version"),
        help_text=("the version of the service type as sem version"),
    )

    # name =  id or identifier or name ???

    title: str = models.CharField(max_length=1000,
                                  verbose_name=("title"),
                                  help_text=(
                                      "a short descriptive title for this service"),
                                  default="")
    abstract = models.TextField(verbose_name=("abstract"),
                                help_text=(
                                    "brief summary of the content of this service"),
                                blank=True,
                                default="")


class FeatureType(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid4,
                          editable=False)
    
    title: str = models.CharField(max_length=1000,
                                  verbose_name=("title"),
                                  help_text=(
                                      "a short descriptive title for this metadata"),
                                  default="")
    abstract = models.TextField(verbose_name=("abstract"),
                                help_text=(
                                    "brief summary of the content of this metadata."),
                                blank=True,
                                default="")