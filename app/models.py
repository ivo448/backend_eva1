from django.db import models
from django.contrib.auth.models import User  # usuarios de Django
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator

# --- MODELOS ---

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
        ('DIRECTORCARRERA', 'Director de Carrera'),
        ('PANOLERO', 'Pañolero'),
        ('PROFESOR', 'Profesor'),
        ('ESTUDIANTE', 'Estudiante'),
    ]
    # OneToOneField extiende el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil') 
    rol = models.CharField(max_length=19, choices=ROL_OPCIONES, default='ESTUDIANTE')
    rut = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_rol_display()})"

class Prestamo(models.Model):
    estudiante = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='prestamos_recibidos',
        # Filtra el dropdown para mostrar solo usuarios con el rol de Estudiante
        limit_choices_to={'perfil__rol': 'ESTUDIANTE'}
    )
    
    registrado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='prestamos_registrados',
        limit_choices_to={'perfil__rol__in': ['PANOLERO', 'ADMIN']}
    )
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_estimada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    cantidad_prestada = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Préstamo de {self.equipo.nombre} a {self.estudiante.username}"

    def clean(self):
        if self.cantidad_prestada > self.equipo.cantidad:
            raise ValidationError(f"No se pueden prestar {self.cantidad_prestada}. Stock disponible: {self.equipo.cantidad}")
        
        if self.fecha_devolucion_estimada <= timezone.now():
            raise ValidationError("La fecha de devolución estimada debe ser en el futuro.")

class ReservaTaller(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_taller')
    proposito = models.CharField(max_length=200)
    inicio_reserva = models.DateTimeField()
    fin_reserva = models.DateTimeField()
    cantidad_alumnos = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Relación ManyToMany con Equipos, usando un modelo 'through'
    equipos = models.ManyToManyField(
        Equipo,
        through='ReservaTallerEquipo',
        related_name='reservas_taller'
    )

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.inicio_reserva.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        # 1. Hora de fin debe ser posterior a hora de inicio
        if self.fin_reserva <= self.inicio_reserva:
            raise ValidationError("La hora de finalización debe ser posterior a la hora de inicio.")
        
        # 2. No se pueden reservar fechas pasadas
        if self.inicio_reserva < timezone.now():
             raise ValidationError("No se puede reservar en una fecha/hora pasada.")
        
# Este modelo conecta la Reserva con el Equipo y almacena la CANTIDAD
class ReservaTallerEquipo(models.Model):
    reserva = models.ForeignKey(ReservaTaller, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        # Asegura que no se pueda añadir el mismo equipo dos veces en la misma reserva
        unique_together = ('reserva', 'equipo')

    def __str__(self):
        return f"{self.cantidad} x {self.equipo.nombre} para {self.reserva.proposito}"