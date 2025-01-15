from django import forms
from django.forms.models import modelformset_factory
from .models import Slider

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['order']

SliderFormSet = modelformset_factory(Slider, form=SliderForm, extra=0)
