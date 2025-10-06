from django.db import models
from .enums import OGCServiceVersionEnum

def xml_backup_file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/xml_documents/<id>/<filename>
    return 'xml_documents/{0}/{1}'.format(instance.pk, filename)


class WebFeatureService(models.Model):
    """Model for WFS capabilities document."""
    """TODO: combine with WMS to inherit from OgcService"""

    xml_backup_file = models.FileField(verbose_name=("xml backup"),
                                       help_text=(
                                           "the original xml as backup to restore the xml field."),
                                       upload_to=xml_backup_file_path,
                                       editable=False,
                                       )

    version: str = models.CharField(
        max_length=10,
        choices=OGCServiceVersionEnum.choices,
        editable=False,
        verbose_name=("version"),
        help_text=("the version of the service type as sem version"),
    )
    pass