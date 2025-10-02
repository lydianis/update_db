from django.db.models.enums import TextChoices


class OGCServiceVersionEnum(TextChoices):
    """ Defines all supported versions

    """
    V_1_0_0 = "1.0.0"
    V_1_1_0 = "1.1.0"
    V_1_1_1 = "1.1.1"
    V_1_3_0 = "1.3.0"

    # wfs specific
    V_2_0_0 = "2.0.0"
    V_2_0_2 = "2.0.2"


class OGCServiceEnum(TextChoices):
    """ Defines all supported service types

    """
    ALL = "all"
    WMS = "wms"
    WFS = "wfs"
    WMC = "wmc"
    DATASET = "dataset"
    CSW = "csw"