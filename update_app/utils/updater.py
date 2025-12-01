from django.db import transaction
from lxml import etree

# use explicit app imports
from update_app.models import WebMapService, Layer
from update_app.utils.helper import get_service_part
from update_app.utils.parser import parse_wms_capabilities
from update_app.utils.helper import get_layers_from_db, get_layers_from_xml
from update_app.utils.comparator import compare_xml


@transaction.atomic
def update_service_part(wms, xml_file_new):
    """Update service metadata for a stored WebMapService from a new capabilities XML.

    Args:
        wms: either a WebMapService instance or its PK (int).
        xml_file_new: path to the new WMS capabilities XML file.

    Behaviour:
        - parses the <Service> part of the capabilities document
        - maps common elements to fields on the WebMapService model
        - saves the WebMapService instance
    """
    # resolve instance
    if isinstance(wms, WebMapService):
        wms_obj = wms
    else:
        wms_obj = WebMapService.objects.get(pk=wms)

    # get the list of service elements (lxml Elements)
    elements = get_service_part(xml_file_new)

    # helper to get localname
    def localname(elem):
        return etree.QName(elem).localname

    # iterate and map values
    for elem in elements:
        tag = localname(elem)
        text = elem.text or ''

        if tag == 'Name':
            # service name / identifier
            wms_obj.name = text
        elif tag == 'Title':
            wms_obj.title = text
        elif tag == 'Abstract':
            wms_obj.abstract = text
        elif tag == 'ContactOrganization':
            wms_obj.contact_name = text
        elif tag == 'ContactPerson':
            wms_obj.person_name = text
        elif tag == 'ContactElectronicMailAddress':
            wms_obj.email = text
        elif tag == 'ContactVoiceTelephone':
            wms_obj.phone = text
        elif tag == 'ContactFacsimileTelephone':
            wms_obj.facsimile = text
        elif tag == 'Address':
            wms_obj.address = text
        elif tag == 'City':
            wms_obj.city = text
        elif tag in ('PostCode', 'PostalCode'):
            wms_obj.postal_code = text
        elif tag in ('StateOrProvince', 'State'):
            wms_obj.state_or_province = text
        elif tag == 'Country':
            wms_obj.country = text
        # Fees, AccessConstraints, OnlineResource, KeywordList etc. are ignored for now

    # persist changes
    wms_obj.save()
    return wms_obj


def update_layers():
    # placeholder: implementation depends on chosen synchronization strategy
    pass


