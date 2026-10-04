
# forms.py
from django import forms

class HateSpeechForm(forms.Form):
    sentence = forms.CharField(label='Enter sentence', max_length=1000, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
