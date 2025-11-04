from django.db import models
from django.contrib.auth.models import User  # usuarios de Django
from django.core.exceptions import ValidationError
from .validators import (
    validate_nombre_min_length,
    validate_non_negative,
    validate_image_size,
    validate_fecha_not_past,
    validate_descripcion_min_length,
)

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, validators=[validate_nombre_min_length])
    descripcion = models.CharField(max_length=250, validators=[validate_descripcion_min_length])
    cantidad = models.IntegerField(validators=[validate_non_negative])
    imagen = models.ImageField(upload_to='equipos/', null=True, blank=True, validators=[validate_image_size])

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    nombre = models.CharField(max_length=100, validators=[validate_nombre_min_length])
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(validators=[validate_fecha_not_past])
    descripcion = models.CharField(max_length=500, validators=[validate_descripcion_min_length])

    def __str__(self):
        return self.nombre

class Mantencion(models.Model):
    nombre = models.CharField(max_length=100, validators=[validate_nombre_min_length])
    fecha_inicio = models.DateField(validators=[validate_fecha_not_past])
    fecha_fin = models.DateField(validators=[validate_fecha_not_past])
    descripcion = models.CharField(max_length=500, validators=[validate_descripcion_min_length])
    responsable = models.CharField(max_length=100, validators=[validate_nombre_min_length])

    def __str__(self):
        return self.nombre

    def clean(self):
        # validación a nivel de instancia: rango de fechas
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'La fecha de fin debe ser igual o posterior a la fecha de inicio.'})