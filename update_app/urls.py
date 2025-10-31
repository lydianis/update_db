# update_app/urls.py

from django.urls import path
from update_app import views
from update_app.views import WebMapServiceView, WebFeatureServiceView
from update_app.views import CompareWebMapServicesView, CompareLocalWMSView, WMSFileCompareView

urlpatterns =[
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("wms/", WebMapServiceView.as_view(), name="wms"),
    path("wfs/", WebFeatureServiceView.as_view(), name="wfs"),
    path("show_wms/", views.show_wms, name="show_wms"),
    path("compare/", CompareWebMapServicesView.as_view(), name="compare_wms"),
    path("compare-local/", CompareLocalWMSView.as_view(), name="compare_local_wms"),
    path("compare-upload/", WMSFileCompareView.as_view(), name="compare_wms_upload"),
] 
