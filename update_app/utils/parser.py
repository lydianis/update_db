import os
# from ...update_db.settings import BASE_DIR
# from django.conf import settings
from lxml import etree
# from eulxml import xmlmap


def get_root():
    root = etree.getroot()
    # print(root.tag, ": ", root)
    return root


# old stuff; maybe check again ...
def parse_wms_capabilities(xml_file_path):
    # print("inside parse_wms_capabilities")
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    nsmap = root.nsmap
    if None in nsmap:
        nsmap['wms'] = nsmap.pop(None)

    """
    ns = {
        'wms': 'http://www.opengis.net/wms',
        'xlink': 'http://www.w3.org/1999/xlink',
    }
    """

    # SERVICE
    top_element = root.xpath('//wms:Service', namespaces=nsmap)
    # print(top_element)

    service_elements = {}

    def parse_service_elements(service_elem):
        name_elem = service_elem.find('wms:Name', namespaces=nsmap)

        name = name_elem.text
        title = service_elem.findtext('wms:Title', default='', namespaces=nsmap)
        abstract = service_elem.findtext('wms:Abstract', default='', namespaces=nsmap)

        # create json for service
        service_elements[name] = {
            'name': name,
            'title': title,
            'abstract': abstract
        }

    # start: /WMS_Capabilities/Service
    top_service_element = root.find('.//wms:Service', namespaces=nsmap)
    if top_service_element is not None:
        parse_service_elements(top_service_element)

    # LAYER
    top_layer = root.xpath('//wms:Capability/wms:Layer', namespaces=nsmap)
    # print(top_layer)

    layers = {}
    counter = 0
    
    def parse_layer(layer_elem):
        # print("inside parse_layer")
        nonlocal counter
        counter += 1
        # name_elem = layer_elem.find('wms:Name', namespaces=nsmap)
        # name = name_elem.text
        name = layer_elem.findtext('wms:Name', default='', namespaces=nsmap)
        title = layer_elem.findtext('wms:Title', default='', namespaces=nsmap)
        abstract = layer_elem.findtext('wms:Abstract', default='', namespaces=nsmap)
        left = counter
        # print("LEFT: ", left)
        # parent = layer_elem.get('parent')
        
        # create json for layer
        layers[name] = {
            'name': name,
            'title': title,
            'abstract': abstract,
            'lft': left,
            # 'parent': parent,
        }
        
        # recursive walk through sublayer
        sublayers = layer_elem.findall('wms:Layer', namespaces=nsmap)
        for sub in sublayers:
            parse_layer(sub)
        counter += 1
        layers[name]['rght'] = counter
        # print("LAYER: ", layers[name], ", " ,layers[name]['rght'])
            

    # start: /WMS_Capabilities/Capability/Layer
    top_layer = root.find('.//wms:Capability/wms:Layer', namespaces=nsmap)
    if top_layer is not None:
        parse_layer(top_layer)

    return service_elements, layers

s, l = parse_wms_capabilities('/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml')
print('SERVICE:')
print(s)
print('LAYER:')
print(l)
