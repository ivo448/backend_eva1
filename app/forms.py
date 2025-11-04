from django import forms
from .models import Equipo, Solicitud, Mantencion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import (
    validate_nombre_min_length,
    validate_non_negative,
    validate_image_size,
    validate_fecha_not_past,
    validate_fecha_range,
    validate_descripcion_min_length,
)

class FormEquipo(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'descripcion', 'cantidad', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        validate_nombre_min_length(nombre)
        return nombre

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        validate_non_negative(cantidad)
        return cantidad

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        validate_image_size(imagen)
        return imagen

class FormSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre', 'fecha', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        validate_nombre_min_length(nombre)
        return nombre

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        validate_fecha_not_past(fecha)
        return fecha

    def clean_descripcion(self):
        descripcion = (self.cleaned_data.get('descripcion') or '').strip()
        validate_descripcion_min_length(descripcion)
        return descripcion

class FormMantencion(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'descripcion', 'responsable']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        validate_nombre_min_length(nombre)
        return nombre

    def clean_responsable(self):
        responsable = (self.cleaned_data.get('responsable') or '').strip()
        validate_nombre_min_length(responsable, min_len=1)
        return responsable

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        try:
            validate_fecha_not_past(inicio)
            validate_fecha_not_past(fin)
            validate_fecha_range(inicio, fin)
        except forms.ValidationError as e:
            # forms.ValidationError vs django.core.exceptions.ValidationError handled alike here
            self.add_error('fecha_fin', e)
        return cleaned
