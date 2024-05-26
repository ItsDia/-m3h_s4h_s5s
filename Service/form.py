from django import forms

class ServiceNameForm(forms.Form):
    service_name = forms.CharField(label='Service Name')
