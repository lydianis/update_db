from django import forms

class WMSUploadForm(forms.Form):
    wms1 = forms.FileField(label="WMS 1 (XML-Datei)")
    wms2 = forms.FileField(label="WMS 2 (XML-Datei)")

