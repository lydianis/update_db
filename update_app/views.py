from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from update_app.models import WebMapService, WebFeatureService
from update_app.services import WebMapServiceComparator, parse_wms_file, compare_parsed_wms, import_wms_to_db
from .utils.parser import parse_wms_capabilities
from .utils import comparator, helper, parser
from .utils.foo_service import parse_foo
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from .forms import WMSUploadForm
from django.template import loader
from pathlib import Path
from update_app.utils.reset import reset_db
from update_app.utils.updater import update_service_part


import requests
# import json


PROXIES ={
    'http_proxy': 'http://xxx:8080',
    'https_proxy': 'http://xxx:8080',
} 

"""
def home(request):
    return(HttpResponse("MrMap - Database Update"))
"""

def home(request):
    return (render(request, "update_app/home.html"))

def about(request):
    return(render(request, "update_app/about.html"))

def foo(request):
    return(render(request, "update_app/foo_f.html"))

def reset_database(request):
    """Setzt die Datenbank zurück und leitet zur Home-Seite weiter."""
    reset_db()
    return redirect('home')


def update_service(request, wms_id=None):
    """View to update service metadata from a new capabilities XML and show changes.

    Usage:
      /wms/update/<wms_id>/?xml=/path/to/file.xml

    If no xml param is provided, uses the test fixture `fixture_1.3.0_modified.xml`.
    """
    from update_app.models import WebMapService
    from pathlib import Path

    # resolve WMS id (fallback to 3 for local testing if not provided)
    if wms_id is None:
        wms_id = request.GET.get('wms_id') or 3

    wms_obj = get_object_or_404(WebMapService, pk=wms_id)

    # xml file to use
    xml_file = request.GET.get('xml')
    if not xml_file:
        base = Path(__file__).resolve().parent / 'files'
        xml_file = str(base / 'fixture_1.3.0_modified.xml')

    # record old values for fields we care about
    fields = [
        'name', 'title', 'abstract',
        'contact_name', 'person_name', 'email', 'phone', 'facsimile',
        'address', 'city', 'postal_code', 'state_or_province', 'country',
    ]
    old_values = {f: getattr(wms_obj, f, '') for f in fields}

    # perform update
    updated = update_service_part(wms_obj, xml_file)

    # compute changed fields
    changes = []
    for f in fields:
        old = old_values.get(f) or ''
        new = getattr(updated, f) or ''
        if str(old) != str(new):
            changes.append({'field': f, 'old': old, 'new': new})

    context = {
        'wms_id': wms_id,
        'wms': updated,
        'xml_file': xml_file,
        'changes': changes,
    }

    return render(request, 'update_app/service_update_result.html', context)

class FooView(TemplateView):
    # template_name = "update_app/foo_c.html"
    def get(self, request):
        baz1 = parse_foo()
        context ={
            "baz1": baz1,
        }
        return render(request, "update_app/foo_c.html", context)


class WebMapServiceView(TemplateView):
    # template_name = "update_app/wms.html"
    
    def get(self, request):

        xml_file_1 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml'
        # TODO: xml_file_1 should be the one persisted for the service in the DB
        xml_file_2 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0_modified.xml'

        xml_name_1 = Path(xml_file_1).name
        xml_name_2 = Path(xml_file_2).name

        edit_file = comparator.compare_xml(xml_file_1, xml_file_2)

        # service1, layers1 = parse_wms_capabilities(xml_file_1)
        # service2, layers2 = parse_wms_capabilities(xml_file_2)
        service1 = helper.get_service_part(xml_file_1)[0]
        service2 = helper.get_service_part(xml_file_2)[0]

        check = comparator.check_service(xml_file_1, xml_file_2)
        diff = comparator.compare_xml(xml_file_1, xml_file_2)
        service_part_diff = comparator.compare_service_part(xml_file_1, xml_file_2)
        
        # service1_id = WebMapService.objects.get(name=service1.findtext('wms:Name', default='', namespaces=helper.ns)).id
        service1_id = 3  # for testing only, later this will be "self"
        layer_db_1 = helper.get_layers_from_db(service1_id)
        print("LAYER DB 1: ", type(layer_db_1), layer_db_1)
        # layer_xml_2 = helper.get_layers_from_xml(xml_file_2)
        layer_xml_2 = parser.parse_wms_capabilities(xml_file_2)[1]
        print("LAYER XML 2: ", type(layer_xml_2), layer_xml_2)
        layer_del, layer_new, layer_mod, layer_pos = comparator.compare_layers(service1_id, xml_file_2)
        print("LAYER DIFF: ", layer_del, layer_new)
        print("LAYER MOD: ", layer_mod)
        
        context = { 
            "xml_file_1": xml_file_1,
            "xml_file_2": xml_file_2,
            "xml_name_1": xml_name_1,
            "xml_name_2": xml_name_2,
            "edit_file": edit_file,
            "wms1_service": service1,
            "wms2_service": service2,
            "check": check,
            "diff": diff,
            "service_part_diff": service_part_diff,
            "layer_db_1": layer_db_1,
            "layer_xml_2": layer_xml_2,
            "layer_del": layer_del,
            "layer_new": layer_new,
            "layer_mod": layer_mod,
            "layer_pos": layer_pos,
        }

        return render(request, "update_app/wms.html", context)


class WebMapServiceShowView(TemplateView):
    model = WebMapService
    template_name = 'update_app/show_wms.html'
    context_object_name = 'wms'


class CompareWebMapServicesView(TemplateView):
    # template_name = "compare_wms.html"
    # template_name = "update_app/wms.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # wms1_id = self.request.GET.get("wms1")
        # wms2_id = self.request.GET.get("wms2")
        # sync = self.request.GET.get("sync")  # optionaler Parameter zum Synchronisieren
        
        # wms1 = get_object_or_404(WebMapService, pk=wms1_id)
        # wms2 = get_object_or_404(WebMapService, pk=wms2_id)
        xml_file_1 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml'
        xml_file_2 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0_modified.xml'

        wms1_file = parse_wms_file(xml_file_1)
        wms2_file = parse_wms_file(xml_file_2)
        print("WMS1_FILE: ", wms1_file)
        # print("WMS2_FILE: ", wms2_file)

        comparator = WebMapServiceComparator(wms1_file, wms2_file)

        # if sync:
        #     diffs = comparator.synchronize()
        # else:
        diffs = comparator.compare()
        print("DIFFS: ", diffs)

        context.update({
            "wms1": wms1_file,
            "wms2": wms2_file,
            "added_layers": diffs["added"],
            "removed_layers": diffs["removed"],
            "changed_layers": diffs["changed"],
            # "synchronized": bool(sync),
        })
        
        return context
    
class CompareLocalWMSView(TemplateView):
    template_name = "update_app/compare_wms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_path = Path(__file__).resolve().parent / "files"
        wms1_file = base_path / "fixture_1.3.0.xml"
        wms2_file = base_path / "fixture_1.3.0_modified.xml"
        print("1: ", wms1_file )
        print("2: ", wms2_file)

        wms1 = parse_wms_file(wms1_file)
        wms2 = parse_wms_file(wms2_file)

        diffs = compare_parsed_wms(wms1, wms2)

        context.update({
            "wms1": wms1,
            "wms2": wms2,
            "added_layers": diffs["added"],
            "removed_layers": diffs["removed"],
            "changed_layers": diffs["changed"],
        })
        return context

class CompareImportedWMSView(TemplateView):
    template_name = "compare_wms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_path = Path(__file__).resolve().parent / "files"

        wms1 = import_wms_to_db(base_path / "wms1.xml")
        wms2 = import_wms_to_db(base_path / "wms2.xml")

        comparator = WebMapServiceComparator(wms1, wms2)
        diffs = comparator.compare()

        context.update({
            "wms1": wms1,
            "wms2": wms2,
            "added_layers": diffs["added"],
            "removed_layers": diffs["removed"],
            "changed_layers": diffs["changed"],
        })
        return context

class WMSFileCompareView(FormView):
    template_name = "update_app/compare_wms_upload.html"
    form_class = WMSUploadForm

    def form_valid(self, form):
        wms1_file = form.cleaned_data["wms1"]
        wms2_file = form.cleaned_data["wms2"]

        # Parsen & Vergleichen
        wms1 = parse_wms_file(wms1_file)
        wms2 = parse_wms_file(wms2_file)
        diffs = compare_parsed_wms(wms1, wms2)

        # Ergebnis anzeigen
        return render(self.request, self.template_name, {
            "form": form,
            "wms1": wms1,
            "wms2": wms2,
            "added_layers": diffs["added"],
            "removed_layers": diffs["removed"],
            "changed_layers": diffs["changed"],
            "has_result": True,
        })

class WebFeatureServiceView(View):
    def get(self, request):
        print("WFS")
        return HttpResponse("result")
