# update_app/urls.py

from django.urls import path
from update_app import views
from update_app.views import FooView, WebMapServiceView, WebFeatureServiceView
from update_app.views import WebMapServiceShowView
from update_app.views import CompareWebMapServicesView, CompareLocalWMSView, WMSFileCompareView

urlpatterns =[
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("foo_f/", views.foo, name="foo_f"),
    path("foo_c/", FooView.as_view(), name="foo_c"),
    path("wms/", WebMapServiceView.as_view(), name="wms"),
    path("wfs/", WebFeatureServiceView.as_view(), name="wfs"),
    path("show_wms/<int:pk>/", WebMapServiceShowView.as_view(), name="show_wms"),
    path("compare/", CompareWebMapServicesView.as_view(), name="compare_wms"),
    path("compare-local/", CompareLocalWMSView.as_view(), name="compare_local_wms"),
    path("compare-upload/", WMSFileCompareView.as_view(), name="compare_wms_upload"),
] 
