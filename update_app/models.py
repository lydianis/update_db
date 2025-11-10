from uuid import uuid4

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from .enums import OGCServiceVersionEnum

def xml_backup_file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/xml_documents/<id>/<filename>
    return 'xml_documents/{0}/{1}'.format(instance.pk, filename)


class MetadataContact(models.Model):
    contact_name = models.CharField(max_length=256,
                            default='',
                            verbose_name=("Name"),
                            help_text=("The name of the organization"))
    person_name = models.CharField(max_length=200,
                                   default='',
                                   blank=True,
                                   verbose_name=("Contact person"))
    email = models.EmailField(max_length=100,
                              default='',
                              verbose_name=('E-Mail'))
    phone = models.CharField(max_length=100,
                             default='',
                             blank=True,
                             verbose_name=('Phone'))
    facsimile = models.CharField(max_length=100,
                                 default='',
                                 blank=True,
                                 verbose_name=("Facsimile"))
    city = models.CharField(max_length=100,
                            default='',
                            verbose_name=("City"))
    postal_code = models.CharField(max_length=100,
                                   default='',
                                   verbose_name=("Postal code"))
    address_type = models.CharField(max_length=100,
                                    default='',
                                    verbose_name=("Address type"))
    address = models.CharField(max_length=100,
                               default='',
                               verbose_name=("Address"))
    state_or_province = models.CharField(max_length=100,
                                         default='',
                                         verbose_name=("State or province"))
    country = models.CharField(max_length=100,
                               default='',
                               verbose_name=("Country"))


class WebMapService(models.Model):
    """Model for WMS capabilities document."""

    xml_backup_file = models.FileField(verbose_name=("xml backup"),
                                       help_text=(
                                           "the original xml as backup to restore the xml field."),
                                       upload_to=xml_backup_file_path,
                                       # editable=False,
                                       )
    
    history = HistoricalRecords()

    version: str = models.CharField(
        max_length=10,
        choices=OGCServiceVersionEnum.choices,
        editable=False,
        verbose_name=("version"),
        help_text=("the version of the service type as sem version"),
        default=""
    )

    name =  models.CharField(max_length=200,
                             default="")

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
    
    # contact_metadata    
    contact_name = models.CharField(max_length=256,
                            default='',
                            verbose_name=("Name"),
                            help_text=("The name of the organization"))
    person_name = models.CharField(max_length=200,
                                   default='',
                                   blank=True,
                                   verbose_name=("Contact person"))
    email = models.EmailField(max_length=100,
                              default='',
                              verbose_name=('E-Mail'))
    phone = models.CharField(max_length=100,
                             default='',
                             blank=True,
                             verbose_name=('Phone'))
    facsimile = models.CharField(max_length=100,
                                 default='',
                                 blank=True,
                                 verbose_name=("Facsimile"))
    city = models.CharField(max_length=100,
                            default='',
                            verbose_name=("City"))
    postal_code = models.CharField(max_length=100,
                                   default='',
                                   verbose_name=("Postal code"))
    address_type = models.CharField(max_length=100,
                                    default='',
                                    verbose_name=("Address type"))
    address = models.CharField(max_length=100,
                               default='',
                               verbose_name=("Address"))
    state_or_province = models.CharField(max_length=100,
                                         default='',
                                         verbose_name=("State or province"))
    country = models.CharField(max_length=100,
                               default='',
                               verbose_name=("Country"))
    
    def __str__(self):
        return self.title
    
    

class Layer(MPTTModel):
    """Model for single WMS Layers"""
    name = models.CharField(max_length=200, unique=True)
    WebMapService = models.ForeignKey(
        to=WebMapService,
        on_delete=models.CASCADE,
        editable=False,
        verbose_name="service",
        help_text="the WMS where this layer is part of",
    )
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

    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children')
    sort_order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['sort_order']


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