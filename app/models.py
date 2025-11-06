from django.db import models
from django.contrib.auth.models import User  # usuarios de Django

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='equipos/', null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipos_creados')

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes', null=True, blank=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

class Mantencion(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenciones', null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=500)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mantenciones_responsable')

    def __str__(self):
        return self.nombre