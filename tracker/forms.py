# Django forms placeholder
from django import forms
from .models import Cryptocurrency

class CryptocurrencySearchForm(forms.Form):
    cryptocurrency = forms.ModelChoiceField(
        queryset=Cryptocurrency.objects.all(),
        empty_label="Select a cryptocurrency",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'cryptoSelect'
        })
    )