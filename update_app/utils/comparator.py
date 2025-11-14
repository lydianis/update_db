from xmldiff import main
from lxml import etree
# from parser import parse_wms_capabilities
# from models import Layer
from django.db import transaction
from .helper import get_service_type, get_version, get_service_part
from .helper import get_layers_from_db, get_layers_from_xml

xml_file_1 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml'
# xml_file_2 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_2.0.0.xml'
xml_file_2 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0_modified.xml'

def check_service(xml_file_1, xml_file_2):
    # check whether both xml files have the same service type and version; maybe move to helper?
    """
    Args: xml_file_1: "old" capabilities document from the database
          xml_file_2: "new" capabilities document for update
    
    Returns: True, if service type is the same
             False if service type is different
    """
    if get_service_type(xml_file_1) == get_service_type(xml_file_2):
        print("service types match")
        if get_version(xml_file_1) == get_version(xml_file_2):
            print("verions match")
            return True
        else:
            print("versions do not match")
    else:
        print("service types do not match")
        return False


def compare_xml(xml_file_1, xml_file_2):
    
    edit_file = main.diff_files(xml_file_1, xml_file_2)
    # for TESTING only
    if edit_file:
        print("update needed")
    else:
        print("ok")
    return edit_file


def compare_service_part(xml_file_1, xml_file_2):
    # check service type and version; maybe not neccessary, depending on the final structure
    check_service(xml_file_1, xml_file_2)
    # get service elements for both capabilities files
    service_part_1 = get_service_part(xml_file_1)
    service_part_2 = get_service_part(xml_file_2)
    # compare single service elements
    service_part_diff_dict = []  # contains elements from service2
    for element1 in service_part_1:
        for element2 in service_part_2:
            if element1.tag == element2.tag and element1.text != element2.text:
                # entfernen der namespaces
                element2.tag = etree.QName(element2).localname
                service_part_diff_dict.append(element2)
    return service_part_diff_dict


def compare_layers(wms, xml_file2):
    # get layers for both capability files
    layers1 = get_layers_from_db(wms)
    layers2 = get_layers_from_xml(xml_file2)
    pass

# for TESTING only:
check = check_service(xml_file_1, xml_file_2)
diff = compare_xml(xml_file_1, xml_file_2)
print(diff)
service_part_diff = compare_service_part(xml_file_1, xml_file_2)
for elem in service_part_diff:
    # local_name = etree.QName(elem.tag).localname
    # print(local_name, ": ", elem.text)
    print(elem.tag, ": ", elem.text)
