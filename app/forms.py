from django import forms
from .models import Equipo, Solicitud
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'descripcion', 'cantidad']

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre', 'fecha', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            #'usuario': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

# class RegistroUsuarioForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
