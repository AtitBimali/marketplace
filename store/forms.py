from django import forms
from .models import Search

class SearchForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': "form-control mr-sm-2", 'placeholder': 'Search Products'
    }))
    class Meta:
        model = Search
        fields = ['name']
