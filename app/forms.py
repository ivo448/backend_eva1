from django import forms
from .models import Equipo, Solicitud, Mantencion, Perfil, Prestamo, ReservaTaller
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    # 1. Validacion Cantidad positiva
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        return cantidad

class FormSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre', 'fecha', 'descripcion', 'usuario', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    # 1. Validacion Fecha no puede ser en el pasado
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < timezone.now().date():
            raise ValidationError("La fecha de la solicitud no puede ser en el pasado.")
        return fecha

    # 2. Validacion Descripcion minima
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) < 10:
            raise ValidationError("La descripción debe tener al menos 10 caracteres.")
        return descripcion

class FormMantencion(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ['nombre', 'equipo', 'fecha_inicio', 'fecha_fin', 'descripcion', 'responsable']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
        }

    # 1. Validacion Fechas congruentes
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            # Lanza error en el campo 'fecha_fin'
            self.add_error('fecha_fin', "La fecha de finalización no puede ser anterior a la fecha de inicio.")
        
        return cleaned_data

    # 2. Validacion Responsable es requerido
    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')
        if not responsable:
            raise ValidationError("Se debe asignar un responsable para la mantención.")
        return responsable

# --- FORMS PARA NUEVOS MODELOS ---

class FormPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['rol', 'rut', 'telefono', 'direccion']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    # Validacion Formato de RUT
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut and (len(rut) < 8 or '-' not in rut):
            raise ValidationError("Ingrese un RUT válido (ej: 12.345.678-9).")
        return rut

class FormPrestamo(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['solicitud', 'equipo', 'fecha_devolucion_estimada', 'cantidad_prestada']
        widgets = {
            'solicitud': forms.Select(attrs={'class': 'form-select'}),
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_devolucion_estimada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'cantidad_prestada': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    # Validacion No prestar más de lo disponible
    def clean(self):
        cleaned_data = super().clean()
        equipo = cleaned_data.get('equipo')
        cantidad = cleaned_data.get('cantidad_prestada')

        if equipo and cantidad:
            if cantidad > equipo.cantidad:
                self.add_error('cantidad_prestada', f"No se pueden prestar {cantidad}. Stock disponible: {equipo.cantidad}")
        return cleaned_data

class FormReservaTaller(forms.ModelForm):
    class Meta:
        model = ReservaTaller
        fields = ['usuario', 'proposito', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'cantidad_alumnos']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'proposito': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_reserva': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'cantidad_alumnos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Validacion Conflicto de horarios
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha_reserva')
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')

        if not (fecha and inicio and fin):
            return cleaned_data # No se puede validar si faltan datos

        # 1. Validar que hora_fin > hora_inicio
        if fin <= inicio:
            self.add_error('hora_fin', "La hora de finalización debe ser posterior a la de inicio.")

        # 2. Validar que no se topen las reservas
        # Excluye la reserva actual si se está editando (self.instance.pk)
        reservas_existentes = ReservaTaller.objects.filter(fecha_reserva=fecha).exclude(pk=self.instance.pk)
        
        conflicto = reservas_existentes.filter(
            hora_inicio__lt=fin,
            hora_fin__gt=inicio
        ).exists()

        if conflicto:
            raise ValidationError("Existe un tope de horario con otra reserva. Por favor, elija otro bloque.")

        return cleaned_data