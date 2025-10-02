from django.db import models
from simple_history.models import HistoricalRecords
from enums import OGCServiceVersionEnum
from django.utils.functional import cached_property


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
class Licence(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255,
                                  unique=True)
    symbol_url = models.URLField(null=True)
    description = models.TextField()
    description_url = models.URLField(null=True)
    is_open_data = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.identifier, self.name)

class MetadataContact(models.Model):
    name = models.CharField(max_length=256,
                            default='',
                            verbose_name=("Name"),
                            help_text=("The name of the organization"))
    person_name = models.CharField(max_length=200,
                                   default='',
                                   verbose_name=("Contact person"))
    email = models.EmailField(max_length=100,
                              default='',
                              verbose_name=('E-Mail'))
    phone = models.CharField(max_length=100,
                             default='',
                             verbose_name=('Phone'))
    facsimile = models.CharField(max_length=100,
                                 default='',
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

    # objects = UniqueConstraintDefaultValueManager()

    class Meta:
        ordering = ["name"]
        constraints = [
            # we store only atomic contact records, identified by all fields
            # NOTE: Avoid nullable columns that are part of a unique constraint:
            # https://wladimirguerra.medium.com/only-one-null-in-unique-columns-234672fefc08
            models.UniqueConstraint(fields=['name',
                                            'person_name',
                                            'email',
                                            'phone',
                                            'facsimile',
                                            'city',
                                            'postal_code',
                                            'address_type',
                                            'address',
                                            'state_or_province',
                                            'country'],
                                    name='%(app_label)s_%(class)s_unique_together_metadata_contact')
        ]

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""

class MetadataTermsOfUse(models.Model):
    """ Abstract model class to define some fields which describes the terms of use for an metadata """
    access_constraints = models.TextField(null=True,
                                          blank=True,
                                          verbose_name=("access constraints"),
                                          help_text=("access constraints for the given resource."))
    fees = models.TextField(null=True,
                            blank=True,
                            verbose_name=("fees"),
                            help_text=("Costs and of terms of use for the given resource."))
    use_limitation = models.TextField(null=True,
                                      blank=True)
    license_source_note = models.TextField(null=True,
                                           blank=True)
    licence = models.ForeignKey(to=Licence,
                                on_delete=models.RESTRICT,
                                blank=True,
                                null=True)

    class Meta:
        abstract = True

class AbstractMetadata(MetadataDocumentModelMixin):
    """ Abstract model class to define general fields for all concrete metadata models. """
    id = models.UUIDField(primary_key=True,
                          default=uuid4,
                          editable=False)
    date_stamp = models.DateTimeField(verbose_name=_('date stamp'),
                                      help_text=_('date that the metadata was created. If this is a metadata record '
                                                  'which is parsed from remote iso metadata, the date stamp of the '
                                                  'remote iso metadata will be used.'),
                                      auto_now_add=True,
                                      editable=False,
                                      db_index=True)
    file_identifier = models.CharField(max_length=1000,
                                       editable=False,
                                       default=uuid4,
                                       db_index=True,
                                       verbose_name=_("file identifier"),
                                       help_text=_("the parsed file identifier from the iso metadata xml "
                                                   "(gmd:fileIdentifier) OR for example if it is a layer/featuretype"
                                                   "the uuid of the described layer/featuretype shall be used to "
                                                   "identify the generated iso metadata xml."))
    origin = models.CharField(max_length=20,
                              choices=MetadataOriginEnum.choices,
                              editable=False,
                              verbose_name=_("origin"),
                              help_text=_("Where the metadata record comes from."))
    origin_url = models.URLField(max_length=4096,
                                 null=True,
                                 blank=True,
                                 editable=False,
                                 verbose_name=_("origin url"),
                                 help_text=_("the url of the document where the information of this metadata record "
                                             "comes from"))
    title: str = models.CharField(max_length=1000,
                                  verbose_name=_("title"),
                                  help_text=_(
                                      "a short descriptive title for this metadata"),
                                  default="")
    abstract = models.TextField(verbose_name=_("abstract"),
                                help_text=_(
                                    "brief summary of the content of this metadata."),
                                blank=True,
                                default="")
    is_broken = models.BooleanField(default=False,
                                    editable=False,
                                    verbose_name=_("is broken"),
                                    help_text=_("TODO"))
    is_customized = models.BooleanField(default=False,
                                        editable=False,
                                        verbose_name=_("is customized"),
                                        help_text=_("If the metadata record is customized, this flag is True"))
    insufficient_quality = models.TextField(default="",
                                            blank=True,
                                            editable=False,
                                            help_text=_("TODO"))
    is_searchable = models.BooleanField(default=False,
                                        verbose_name=_("is searchable"),
                                        help_text=_("only searchable metadata will be returned from the search api"))
    hits = models.IntegerField(default=0,
                               verbose_name=_("hits"),
                               help_text=_(
                                   "how many times this metadata was requested by a client"),
                               editable=False, )
    keywords = models.ManyToManyField(to=Keyword,
                                      blank=True,
                                      related_name="%(class)s_metadata",
                                      related_query_name="%(class)s_metadata",
                                      verbose_name=_("keywords"),
                                      help_text=_("all keywords which are related to the content of this metadata."))

    language = None  # TODO
    category = None  # TODO: Inspire + iso + various

    # needed for Docuement mixin to load the backupfile into the correct xml mapper class
    xml_mapper_cls = MdMetadata

    class Meta:
        abstract = True
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title", "file_identifier"]),
        ]
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_file_identifier",
                fields=["file_identifier"]
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.pk})"

    def save(self, *args, **kwargs):
        """Custom save function to set `is_customized` on update."""
        # FIXME: if the record is updated by harvesting process, the customized flag shall not be set to True
        if not self._state.adding:
            self.is_customized = True

        return super().save(*args, **kwargs)


class ServiceMetadata(MetadataTermsOfUse, AbstractMetadata):
    """ Concrete model class to store the parsed metadata information from the capabilities document of a given layer

        OR to store the information of the parsed iso metadata which was linked in the capabilities document.

    """
    service_contact = models.ForeignKey(to=MetadataContact,
                                        on_delete=models.RESTRICT,
                                        related_name="service_contact_%(class)s_metadata",
                                        verbose_name=_("service contact"),
                                        help_text=_("This is the contact for the service provider."))
    metadata_contact = models.ForeignKey(to=MetadataContact,
                                         on_delete=models.RESTRICT,
                                         related_name="metadata_contact_%(class)s_metadata",
                                         verbose_name=_("metadata contact"),
                                         help_text=_("This is the contact for the metadata information."))
    # iso_metadata = IsoMetadataManager()

    class Meta:
        abstract = True

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

    @cached_property
    def root_layer(self):
        pass
        # return self.layers.get(mptt_parent=None)

    

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

