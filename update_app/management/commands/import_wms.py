from django.core.management.base import BaseCommand
from update_app.models import WebMapService, Layer
import xml.etree.ElementTree as ET

class Command(BaseCommand):
    help = "Importiere eine WMS-Capabilities XML-Datei in die DB"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Pfad zur WMS XML-Datei")
        parser.add_argument("--name", type=str, required=True, help="Name des WebMapService")
        # parser.add_argument("--url", type=str, default="", help="URL des WMS")
    

    def handle(self, *args, **options):
        file_path = options["file"]
        name = options["name"]
        # url = options["url"]

        # WMS anlegen
        wms = WebMapService.objects.get_or_create(name=name)

        # Datei parsen
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Layer sammeln
        def extract_layers(layer_elem, layers):
            """Rekursiv alle Layer extrahieren."""
            lname = layer_elem.findtext("Name")
            title = layer_elem.findtext("Title")
            if lname and title:
                layers[lname] = title
            # rekursiv alle Unter-Layer
            for child in layer_elem.findall("Layer"):
                extract_layers(child, layers)
        
        layers = {}
        # Top-Level Layer in WMS-Datei
        for top_layer in root.findall(".//Capability/Layer"):
            extract_layers(top_layer, layers)

        layers_added = 0
        # Layer in DB speichern
        for name, title in layers.items():
            Layer.objects.get_or_create(name=name, title=title, web_map_service=wms)
            layers_added += 1

        self.stdout.write(self.style.SUCCESS(f"{layers_added} Layer importiert in WMS '{name}'"))
