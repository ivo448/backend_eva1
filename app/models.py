from django.db import models
from django.contrib.auth.models import User  # usuarios de Django
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator

# --- MODELOS EXISTENTES (CON VALIDACIONES) ---

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    # Validacion a nivel de modelo: cantidad no puede ser negativa
    cantidad = models.IntegerField(validators=[MinValueValidator(0)]) 
    imagen = models.ImageField(upload_to='equipos/', null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipos_creados')

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADO_OPCIONES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes', null=True, blank=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=500)
    # Campo agregado para cumplir requisito de 5+ campos
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='PENDIENTE')

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"
    
    # Validacion a nivel de modelo: No se pueden crear solicitudes para fechas pasadas.
    def clean(self):
        if self.fecha < timezone.now().date():
            raise ValidationError('La fecha de la solicitud no puede ser en el pasado.')

class Mantencion(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenciones', null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=500)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mantenciones_responsable')

    def __str__(self):
        return self.nombre

    # Validacion a nivel de modelo: La fecha de fin no puede ser anterior a la fecha de inicio.
    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio.')

class Perfil(models.Model):
    ROL_OPCIONES = [
        ('ADMIN', 'Administrador'),
        ('PANOLERO', 'Pañolero'),
        ('PROFESOR', 'Profesor'),
        ('ESTUDIANTE', 'Estudiante'),
    ]
    # OneToOneField extiende el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil') 
    rol = models.CharField(max_length=10, choices=ROL_OPCIONES, default='ESTUDIANTE')
    rut = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_rol_display()})"

class Prestamo(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='prestamos')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_estimada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    cantidad_prestada = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Préstamo de {self.equipo.nombre} a {self.solicitud.usuario.username}"

    # Validacion a nivel de modelo
    def clean(self):
        # 1. No se puede prestar más de lo que hay en stock
        if self.cantidad_prestada > self.equipo.cantidad:
            raise ValidationError(f"No se pueden prestar {self.cantidad_prestada}. Stock disponible: {self.equipo.cantidad}")
        
        # 2. La fecha de devolución debe ser posterior a la de préstamo
        if self.fecha_devolucion_estimada <= timezone.now():
            raise ValidationError("La fecha de devolución estimada debe ser en el futuro.")

# --- Planificacion Uso/Reserva de Taller ---

class ReservaTaller(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_taller')
    proposito = models.CharField(max_length=200)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cantidad_alumnos = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.fecha_reserva} ({self.hora_inicio} - {self.hora_fin})"

    # Validacion a nivel de modelo
    def clean(self):
        # 1. Hora de fin debe ser posterior a hora de inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de finalización debe ser posterior a la hora de inicio.")
        
        # 2. No se pueden reservar fechas pasadas
        if self.fecha_reserva < timezone.now().date():
             raise ValidationError("No se puede reservar en una fecha pasada.")