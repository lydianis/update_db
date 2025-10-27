from lxml import etree

def parse_wms_capabilities(xml_file_path):
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    nsmap = root.nsmap
    if None in nsmap:
        nsmap['wms'] = nsmap.pop(None)

    """
    ns ={
        'wms': 'http://www.opengis.net/wms',
        'xlink': 'http://www.w3.org/1999/xlink',
    }
    """

    top_layer = root.xpath('//wms:Capability/wms:Layer', namespaces=nsmap)

    layers ={}

    def parse_layer(layer_elem):
        name_elem = layer_elem.find('wms:Name', namespaces=nsmap)

        name = name_elem.text
        title = layer_elem.findtext('wms:Title', default='', namespaces=nsmap)
        abstract = layer_elem.findtext('wms:Abstract', default='', namespaces=nsmap)

        # create json for layer
        layers[name] = {
            'name': name,
            'title': title,
            'abstract': abstract
        }

        # recursiv walk through sublayer
        sublayers = layer_elem.findall('wms:Layer', namespaces=nsmap)
        for sub in sublayers:
            parse_layer(sub)

    # start: /WMS_Capabilities/Capability/Layer
    top_layer = root.find('.//wms:Capability/wms:Layer', namespaces=nsmap)
    if top_layer is not None:
        parse_layer(top_layer)

    return layers



