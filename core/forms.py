from django import forms

from .models import LugarPatrimonial


class LugarForm(forms.ModelForm):
    class Meta:
        model = LugarPatrimonial
        fields = ['nombre', 'categoria', 'descripcion', 'ubicacion', 'anio_construccion', 'imagen']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 5})}
