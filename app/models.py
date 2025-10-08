from django.db import models
from django.contrib.auth.models import User  # usuarios de Django

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    nombre = models.CharField(max_length=100)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# class Perfil(models.Model):
#     # Relación uno a uno con el modelo User de Django
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE) 
#     telefono = models.CharField(max_length=15, blank=True)
#     bio = models.TextField(blank=True)
#     fecha_nacimiento = models.DateField(null=True, blank=True)
    
#     def __str__(self):
#         return f'Perfil de {self.usuario.username}'
    
class Mantencion():
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField()
    responsable = models.CharField()