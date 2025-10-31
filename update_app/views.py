from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from update_app.models import WebMapService, WebFeatureService
from update_app.services import WebMapServiceComparator, parse_wms_file, compare_parsed_wms, import_wms_to_db
from .utils import comparator, parser
from django.views import View
from django.views.generic import TemplateView, FormView
from .forms import WMSUploadForm
from django.template import loader
from pathlib import Path
import requests


PROXIES ={
    'http_proxy': 'http://xxx:8080',
    'https_proxy': 'http://xxx:8080',
} 

"""
def home(request):
    return(HttpResponse("MrMap - Database Update"))
"""

def home(request):
    return render(request, "update_app/home.html")

def about(request):
    return(render(request, "update_app/about.html"))

def show_wms(request):
    template = loader.get_template('update_app/wms.html')
    context ={
    } 
    return HttpResponse(template.render())


class WebMapServiceView(TemplateView):
    # template_name = "update_app/wms.html"
    
    def get(self, request):

        edit_file = comparator.compare_xml()
        context = { 
            "edit_file": edit_file,
        }

        return render(request, "update_app/wms.html", context)


class CompareWebMapServicesView(TemplateView):
    template_name = "compare_wms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wms1_id = self.request.GET.get("wms1")
        wms2_id = self.request.GET.get("wms2")
        # sync = self.request.GET.get("sync")  # optionaler Parameter zum Synchronisieren
        

        wms1 = get_object_or_404(WebMapService, pk=wms1_id)
        wms2 = get_object_or_404(WebMapService, pk=wms2_id)

        comparator = WebMapServiceComparator(wms1, wms2)

        # if sync:
        #     diffs = comparator.synchronize()
        # else:
        diffs = comparator.compare()

        context.update({
            "wms1": wms1,
            "wms2": wms2,
            "added_layers": diffs["added"],
            "removed_layers": diffs["removed"],
            "changed_layers": diffs["changed"],
            # "synchronized": bool(sync),
        })
        return context
    
class CompareLocalWMSView(TemplateView):
    template_name = "compare_wms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_path = Path(__file__).resolve().parent / "files"
        wms1_file = base_path / "fixture_1.3.0.xml"
        wms2_file = base_path / "fixture_1.3.0_modified.xml"

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
