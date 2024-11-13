from django import forms
from .models import Advertisement, Response


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'content',
            'category',
        ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'response_text',
        ]
