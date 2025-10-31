import xml.etree.ElementTree as ET
from io import BytesIO
from .models import WebMapService, Layer

class WebMapServiceComparator:
    """
    Vergleicht zwei WMS-Instanzen
    """

    def __init__(self, wms1: WebMapService, wms2: WebMapService):
        self.wms1 = wms1
        self.wms2 = wms2
    
    def compare(self):
        """
        Vergleicht Layer von wms1 und wms2
        Args: wms1, wms2
        Return: diff_dict
        """

        layers1 = {layer.name: layer for layer in self.wms1.layers.all()}
        layers2 = {layer.name: layer for layer in self.wms2.layers.all()}

        added = [layers2[name] for name in layers2 if name not in layers1]
        removed = [layers1[name] for name in layers1 if name not in layers2]
        changed = [
            (layers1[name], layers2[name])
            for name in layers1.keys() & layers2.keys()
            if layers1[name].title != layers2[name].title
        ]

        return {
            "added": added,
            "removed": removed,
            "changed": changed,
        }

# services.py
import xml.etree.ElementTree as ET
from pathlib import Path

class ParsedWebMapService:
    """Repräsentiert einen eingelesenen WMS (nicht aus der DB)."""

    def __init__(self, name, layers):
        self.name = name
        self.layers = layers  # dict {layer_name: layer_title}

"""
# für fest codierte XML-Dateien
def parse_wms_file(filepath: Path) -> ParsedWebMapService:
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Beispielhafte XML-Struktur (je nach WMS-Version evtl. anpassen)
    service_title = root.findtext(".//Service/Title", default="Unbekannter WMS")

    layers = {}
    for layer in root.findall(".//Layer"):
        name = layer.findtext("Name")
        title = layer.findtext("Title")
        if name and title:
            layers[name] = title

    return ParsedWebMapService(name=service_title, layers=layers)
    """

def parse_wms_file(uploaded_file) -> ParsedWebMapService:
    """
    Liest eine hochgeladene XML-Datei aus (InMemoryUploadedFile oder TemporaryUploadedFile).
    """
    tree = ET.parse(uploaded_file)
    root = tree.getroot()
    for layer_elem in root.findall(".//Layer"):
        print(layer_elem.findtext("Name"), layer_elem.findtext("Title"))

    service_title = root.findtext(".//Service/Title", default="Unbekannter WMS")

    layers = {}
    for layer in root.findall(".//Layer"):
        name = layer.findtext("Name")
        title = layer.findtext("Title")
        if name and title:
            layers[name] = title

    return ParsedWebMapService(name=service_title, layers=layers)


def import_wms_to_db(filepath: Path) -> WebMapService:
    parsed = parse_wms_file(filepath)
    wms = WebMapService.objects.create(name=parsed.name, url=f"file://{filepath.name}")
    for name, title in parsed.layers.items():
        Layer.objects.create(name=name, title=title, web_map_service=wms)
    return wms


def compare_parsed_wms(wms1: ParsedWebMapService, wms2: ParsedWebMapService):
    added = [name for name in wms2.layers if name not in wms1.layers]
    removed = [name for name in wms1.layers if name not in wms2.layers]
    changed = [
        (name, wms1.layers[name], wms2.layers[name])
        for name in wms1.layers.keys() & wms2.layers.keys()
        if wms1.layers[name] != wms2.layers[name]
    ]

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
    }

def extract_layers(layer_elem, layers):
    """Rekursiv alle Layer extrahieren."""
    name = layer_elem.findtext("Name")
    title = layer_elem.findtext("Title")
    if name and title:
        layers[name] = title
    # rekursiv alle Unter-Layer
    for child in layer_elem.findall("Layer"):
        extract_layers(child, layers)

# Beispiel im Import-Script:
tree = ET.parse("/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml")
root = tree.getroot()

layers = {}
for top_layer in root.findall(".//Capability/Layer"):  # oft so in WMS
    extract_layers(top_layer, layers)

for name, title in layers.items():
    Layer.objects.get_or_create(name=name, title=title, web_map_service=wms)
