from django import forms


class ClientErrorForm(forms.Form):
    msg = forms.CharField(max_length=1024, required=False)
    url = forms.CharField(max_length=256, required=False)
    line = forms.CharField(max_length=4, required=False)
