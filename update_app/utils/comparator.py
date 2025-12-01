from xmldiff import main
from lxml import etree
# from models import Layer
from django.db import transaction
from .helper import get_service_type, get_version, get_service_part
from .helper import get_layers_from_db, get_layers_from_xml
from .parser import parse_wms_capabilities

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
    # compares two xml files using xmldiff
    """
    Args: xml_file_1: "old" capabilities document from the database
          xml_file_2: "new" capabilities document for update

    Returns: edit_file: list of differences between both files
    """
    edit_file = main.diff_files(xml_file_1, xml_file_2)
    # for TESTING only
    if edit_file:
        print("update needed")
    else:
        print("ok")
    return edit_file


def compare_service_part(xml_file_1, xml_file_2):
    # check service type and version; maybe not neccessary, depending on the final structure
    """
    Args: xml_file_1: "old" capabilities document from the database
          xml_file_2: "new" capabilities document for update
    
    Returns: service_part_diff: list of service elements that are different in both files
    """
    check_service(xml_file_1, xml_file_2)
    # get service elements for both capabilities files
    service_part_1 = get_service_part(xml_file_1)
    service_part_2 = get_service_part(xml_file_2)
    # compare single service elements
    service_part_diff = []  # contains elements from service2
    for element1 in service_part_1:
        for element2 in service_part_2:
            if element1.tag == element2.tag and element1.text != element2.text:
                # entfernen der namespaces
                element2.tag = etree.QName(element2).localname
                service_part_diff.append(element2)
    return service_part_diff


def compare_layers(wms, xml_file2):
    print("inside compare_layers")
    # compare layers from database with layers from new capabilities document
    """
    Args: wms: WebMapService object from database
          xml_file2: "new" capabilities document for update

    Returns: 
    """
    # get layers for both capability files
    layers1 = get_layers_from_db(wms)
    print("LAYER DB 1: ", type(layers1), layers1)
    layers2 = parse_wms_capabilities(xml_file_2)[1]
    print("LAYER XML 2: ", type(layers2), layers2)
    # deleted layers
    layers_deleted = []
    for l1 in layers1:
        found = False
        for l2 in layers2:
            print("Layer from xml: ", l2)
            if l1.name == l2:
                found = True
                break
        if not found:
            layers_deleted.append(l1)
            print("Layer deleted: ", l1.name)
    # new layers
    layers_new = []
    for l2 in layers2:
        found = False
        for l1 in layers1:
            if l2 == l1.name:
                found = True
                break
        if not found:
            layers_new.append(l2)
            print("Layer new: ", l2)
    # modified layers: to be implemented ...
    layers_mod = []
    layers_pos = []
    for l1 in layers1:
        for l2 in layers2.items():
            if l1.name == l2[0]:
                # check other attributes ...
                title = l2[1]['title']
                abstract = l2[1]['abstract']
                if l1.title != title:
                    layers_mod.append((l1, l2[1]))
                    print("Layer modified: ", l1.name, " title: ", l1.title, " -> ", title)
                if l1.abstract != abstract:
                    layers_mod.append((l1, l2))
                    print("Layer modified: ", l1.name, " abstract: ", l1.abstract, " -> ", abstract)
                """
                if l1.lft != l2.lft:
                    layers_pos.append((l1, l2))
                    print("Layer position changed: ", l1.name, " position: ", l1.lft, " -> ", l2.lft)
                """
                pass

        
    return layers_deleted, layers_new, layers_mod, layers_pos

# for TESTING only:
check = check_service(xml_file_1, xml_file_2)
diff = compare_xml(xml_file_1, xml_file_2)
# print(diff)
service_part_diff = compare_service_part(xml_file_1, xml_file_2)
# for elem in service_part_diff:
    # local_name = etree.QName(elem.tag).localname
    # print(local_name, ": ", elem.text)
    # print(elem.tag, ": ", elem.text)
l = get_layers_from_xml(xml_file_2)
# print(l)
layer_diff = compare_layers(3, xml_file_2)  # for testing only, later this will be "self"
# print("LAYER DIFF: ", layer_diff)