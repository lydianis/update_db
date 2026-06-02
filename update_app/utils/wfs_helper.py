from lxml import etree


def get_root():
    root = etree.getroot()
    print(root.tag, ": ", root)
    return root

# Defines xml namespaces used for xml parsing and creating
ns = {
    "ogc": "http://www.opengis.net/ogc",
    "ows": "http://www.opengis.net/ows/1.1",
    "wfs": "http://www.opengis.net/wfs",
    "wms": "http://www.opengis.net/wms",
    "xlink": "http://www.w3.org/1999/xlink",
    "gml": "http://www.opengis.net/gml",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "srv": "http://www.isotc211.org/2005/srv",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "ave": "http://repository.gdi-de.org/schemas/adv/produkt/alkis-vereinfacht/1.0",
    "inspire_common": "http://inspire.ec.europa.eu/schemas/common/1.0",
    "inspire_com": "http://inspire.ec.europa.eu/schemas/common/1.0",
    "inspire_vs": "http://inspire.ec.europa.eu/schemas/inspire_vs/1.0",
    "inspire_ds": "http://inspire.ec.europa.eu/schemas/inspire_ds/1.0",
    "inspire_dls": "http://inspire.ec.europa.eu/schemas/inspire_dls/1.0",
    "epsg": "urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset",
    "ms": "http://mapserver.gis.umn.edu/mapserver",
    "se": "http://www.opengis.net/se",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "sld": "http://www.opengis.net/sld",
    "fes": "http://www.opengis.net/fes/2.0",
    "csw": "http://www.opengis.net/cat/csw/2.0.2",
}


def get_service_type(xml_file):
    service = etree.parse(xml_file)
    service_root = service.getroot()
    service_type = service_root[0][0].text  # geht so für wms
    if "wfs" in service_root:
        service_type = service_root.xpath("//ows:ServiceType")[0].text
        print("Service Type: ", service_type)
    return service_type


def get_version(xml_file):
    service = etree.parse(xml_file)
    service_root = service.getroot()
    version = service_root.get("version")
    return version

def get_service_part(xml_file):
    print("inside get_service_part")
    service = etree.parse(xml_file)
    service_root = service.getroot()
    service_elements = service_root.xpath("//ows:ServiceIdentification/descendant::*", namespaces=ns)
    service_elements.extend(service_root.xpath("//ows:ServiceProvider/descendant::*", namespaces=ns))
    # print("WFS: ", service_elements)
    elements = []
    for element in service_elements:
        local_name = etree.QName(element).localname
        text = (element.text or "").strip()
        print(local_name, ":", text)
        elements.extend(element)
        # print(element.tag, ": ", element.text)
    return elements
    

# for TESTING only
xml_file = "/home/nisius/python/update_db/update_app/files/fixture_2.0.0.xml"
print("ServiceType: ", get_service_type(xml_file))
print("Version: ", get_version(xml_file))
get_service_part(xml_file)
