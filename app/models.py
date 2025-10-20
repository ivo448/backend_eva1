from django.db import models
from django.contrib.auth.models import User  # usuarios de Django

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    nombre = models.CharField(max_length=100)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

class Mantencion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=500)
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre