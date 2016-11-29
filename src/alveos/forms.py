from django import forms

class ConnectForm(forms.Form):
    nickname = forms.CharField(min_length=1, max_length=15, strip=True)

