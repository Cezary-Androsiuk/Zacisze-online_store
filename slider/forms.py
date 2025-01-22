from django import forms
from .models import SliderImage

class SliderImageForm(forms.ModelForm):
    class Meta:
        model = SliderImage
        fields = ['title', 'image']
