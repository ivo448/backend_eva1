from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = [
        ('PROFESOR', 'Profesor'),
        ('PANOLERO', 'Pañolero'),
        ('ADMIN', 'Administrador'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='PROFESOR')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('PRESTAMO', 'En Préstamo'),
        ('MANTENCION', 'En Mantención'),
        ('BAJA', 'De Baja'),
    ]
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='equipos')
    estado = models.CharField(max_length=50, choices=ESTADOS, default='DISPONIBLE')
    fecha_ingreso = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"

class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada')
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva: {self.equipo} para {self.usuario}"

class Requerimiento(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('RECHAZADO', 'Rechazado')
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requerimientos')
    descripcion = models.TextField(help_text="Descripción del material faltante")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Req: {self.usuario} - {self.estado}"

class Mantencion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada')
    ]
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenciones')
    fecha_programada = models.DateField()
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mantención {self.equipo} - {self.fecha_programada}"