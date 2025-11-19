from lxml import etree
# from helper import ns

ns = {
    "ogc": "http://www.opengis.net/ogc",
    "ows": "http://www.opengis.net/ows",
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

# Funktion zum Rekursiven Extrahieren der Layer
def parse_layer(node, parent_id=None, depth=0):
    # print("inside parse_layer")
    layers = []
    for layer in node.xpath('Layer'):
        name = layer.xpath('Name/text()')[0]
        title = layer.xpath('Title/text()')[0]
        layers.append({
            'name': name,
            'title': title,
            'parent_id': parent_id,
            'depth': depth
        })
        
        # Rekursiv Sub-Layer durchsuchen
        layers.extend(parse_layer(layer, parent_id=name, depth=depth+1))
    
    return layers

# Funktion zum Rekursiven Extrahieren der Layer und Aufbau des MPTT
class MPTTNode:
    def __init__(self, name, parent_id=None, depth=0):
        self.name = name
        self.parent_id = parent_id
        self.depth = depth
        self.lft = None
        self.rgt = None
        self.children = []

    def __repr__(self):
        return f"Node(name={self.name}, parent={self.parent_id}, lft={self.lft}, rgt={self.rgt}, depth={self.depth})"


class MPTT:
    def __init__(self):
        self.nodes = []
        self.counter = 1  # Zähler für 'lft' und 'rgt'
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def assign_lft_rgt(self, node):
        """ Weist dem Knoten lft- und rgt-Werte zu """
        node.lft = self.counter
        self.counter += 1
        for child in node.children:
            self.assign_lft_rgt(child)
        node.rgt = self.counter
        self.counter += 1

    def build_tree(self, layers):
        """ Baut den Baum mit rekursiven Sub-Layern auf """
        node_map = {}
        root_node = None
        for layer in layers:
            if not layer['parent_id']:  # Root Layer
                root_node = MPTTNode(layer['name'], parent_id=None, depth=0)
                node_map[layer['name']] = root_node
                self.add_node(root_node)
            else:
                parent_node = node_map.get(layer['parent_id'])
                if parent_node is not None:
                    new_node = MPTTNode(layer['name'], parent_id=parent_node.name, depth=parent_node.depth + 1)
                    parent_node.children.append(new_node)
                    node_map[layer['name']] = new_node
                    self.add_node(new_node)
        if root_node:
            self.assign_lft_rgt(root_node)

    def get_node_by_name(self, name):
        """ Gibt den Knoten mit einem bestimmten Namen zurück """
        return next(node for node in self.nodes if node.name == name)


# for TESTING only
xml_file = "/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml"
service = etree.parse(xml_file)
strtree = etree.tostring(service)
root = etree.fromstring(strtree)
cap_layer = root.xpath('//wms:Capability/wms:Layer[1]', namespaces=ns)[0]

layers = parse_layer(cap_layer)
print(layers)
mptt =MPTT()
mptt.build_tree(layers)
for node in mptt.nodes:
    print(node)