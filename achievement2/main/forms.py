from .models import Number
from django.forms import ModelForm, NumberInput


class NumberForm(ModelForm):
    class Meta:
        model = Number
        fields = ['number']
        widgets = {'number': NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите число',
            'id': 'number'
        }),
        }
