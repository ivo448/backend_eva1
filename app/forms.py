from django import forms
from .models import (
    Equipo, Solicitud, Mantencion, Perfil, Prestamo, 
    ReservaTaller, ReservaTallerEquipo
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.db.models import Sum

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

    # 1. Validacion de Formulario: Cantidad positiva
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    # 2. Validacion de Formulario: Nombre no puede ser "Test"
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and 'test' in nombre.lower():
            raise ValidationError("El nombre no puede contener la palabra 'test'.")
        return nombre

class FormSolicitud(forms.ModelForm):
    
    usuario = forms.ModelChoiceField(
        queryset=User.objects.filter(perfil__rol__in=['PROFESOR', 'ADMIN', 'DIRECTORCARRERA', 'PANOLERO']),
        required=False, # Es Falso por defecto, la lógica __init__ lo hace requerido si es Pañolero
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Solicitud
        fields = ['nombre', 'fecha', 'descripcion', 'usuario', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    # LÓGICA DE ROLES
    def __init__(self, *args, **kwargs):
        # Recibimos el 'user' logueado desde la vista
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

        if self.user and hasattr(self.user, 'perfil'):
            user_rol = self.user.perfil.rol
            
            # REGLA: Si es Profesor, ocultamos el campo 'usuario'
            if user_rol == 'PROFESOR':
                if 'usuario' in self.fields:
                    self.fields['usuario'].widget = forms.HiddenInput()
                if 'estado' in self.fields:
                    self.fields['estado'].widget = forms.HiddenInput()
            
            # REGLA: Si es Pañolero/Admin/Director, el campo 'usuario' (profesor) es obligatorio
            elif user_rol in ['PANOLERO', 'ADMIN', 'DIRECTORCARRERA']:
                if 'usuario' in self.fields:
                    self.fields['usuario'].required = True
                    self.fields['usuario'].label = "Profesor Solicitante"
                
                if 'estado' in self.fields:
                    self.fields['estado'].widget = forms.Select(attrs={'class': 'form-select'})
        
        elif self.user and self.user.is_superuser:
             # Caso para Superadmin sin perfil
             if 'usuario' in self.fields:
                self.fields['usuario'].required = True
                self.fields['usuario'].label = "Profesor Solicitante (Admin)"

    # 1. Validacion de Formulario: Fecha no puede ser en el pasado
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < timezone.now().date():
            raise ValidationError("La fecha de la solicitud no puede ser en el pasado.")
        return fecha

    # 2. Validacion de Formulario: Descripcion minima
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

    # 1. Validacion de Formulario: Fechas congruentes
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            # Lanza error en el campo 'fecha_fin'
            self.add_error('fecha_fin', "La fecha de finalización no puede ser anterior a la fecha de inicio.")
        
        return cleaned_data

    # 2. Validacion de Formulario: Responsable es requerido
    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')
        if not responsable:
            raise ValidationError("Se debe asignar un responsable para la mantención.")
        return responsable

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
    
    # Validacion: Formato de RUT
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut and (len(rut) < 8 or '-' not in rut):
            raise ValidationError("Ingrese un RUT válido (ej: 12.345.678-9).")
        return rut

class FormPrestamo(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['rut_estudiante', 'nombre_estudiante', 'equipo', 'fecha_devolucion_estimada', 'cantidad_prestada']
        widgets = {
            'rut_estudiante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'nombre_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_devolucion_estimada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'cantidad_prestada': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_rut_estudiante(self):
        rut = self.cleaned_data.get('rut_estudiante')
        if not rut:
            raise ValidationError("El RUT del estudiante es obligatorio.")
        return rut
    
    def clean(self):
        cleaned_data = super().clean()
        equipo = cleaned_data.get('equipo')
        cantidad = cleaned_data.get('cantidad_prestada')

        if equipo and cantidad:
            # (Verificamos si estamos editando para no contarnos a nosotros mismos)
            cantidad_original = 0
            if self.instance and self.instance.pk:
                cantidad_original = self.instance.cantidad_prestada
            
            stock_disponible = equipo.cantidad + cantidad_original

            if cantidad > stock_disponible:
                self.add_error('cantidad_prestada', f"No se pueden prestar {cantidad}. Stock disponible: {stock_disponible}")
        
        return cleaned_data

class FormReservaTaller(forms.ModelForm):
    class Meta:
        model = ReservaTaller
        fields = ['proposito', 'inicio_reserva', 'fin_reserva', 'cantidad_alumnos']
        widgets = {
            'proposito': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'inicio_reserva': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fin_reserva': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'cantidad_alumnos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicio_reserva')
        fin = cleaned_data.get('fin_reserva')

        if inicio and fin:
            if fin <= inicio:
                self.add_error('fin_reserva', "La hora de finalización debe ser posterior a la de inicio.")
            if inicio < timezone.now():
                self.add_error('inicio_reserva', "No se puede reservar en una fecha/hora pasada.")
        return cleaned_data


class FormReservaTallerEquipo(forms.ModelForm):
    """Formulario para la línea de equipo en la reserva."""
    class Meta:
        model = ReservaTallerEquipo
        fields = ['equipo', 'cantidad']
        widgets = {
            'equipo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': '1'}),
        }


class BaseReservaTallerEquipoFormSet(BaseInlineFormSet):
    """FormSet Base que contiene la lógica de validación de disponibilidad."""

    def clean(self):
        super().clean()
        
        if any(self.errors):
            # No procesar si hay errores de formulario individuales
            return

        # 1. Obtener la data del formulario "padre" (ReservaTaller)
        # self.instance es la instancia de ReservaTaller
        if not self.instance.inicio_reserva or not self.instance.fin_reserva:
             raise ValidationError("Debes proveer una fecha/hora de inicio y fin para la reserva.")
        
        inicio = self.instance.inicio_reserva
        fin = self.instance.fin_reserva

        equipos_solicitados = {}      # ahora guardará (cantidad, form)

        # 2. Validar duplicados y recolectar cantidades y form referencia
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            equipo = form.cleaned_data.get('equipo')
            cantidad = form.cleaned_data.get('cantidad')

            if not equipo or not cantidad:
                continue

            if equipo.pk in equipos_solicitados:
                form.add_error('equipo', 'Este equipo ya fue seleccionado en esta reserva.')
                raise ValidationError("No puedes reservar el mismo equipo dos veces.")

            # guardo por pk para evitar problemas de identidad y conservar el form
            equipos_solicitados[equipo.pk] = {
                'equipo': equipo,
                'cantidad': cantidad,
                'form': form
            }

        # 3. Validar disponibilidad de stock para cada equipo solicitado
        for equipo, cantidad_solicitada in equipos_solicitados.items():
            stock_total = equipo.cantidad
            
            # --- CALCULAR EQUIPOS OCUPADOS EN ESE HORARIO ---
            
            # A. Ocupados por otras reservas de taller
            reservado_taller = ReservaTallerEquipo.objects.filter(
                equipo=equipo,
                reserva__fin_reserva__gt=inicio,  # Termina después de que yo empiezo
                reserva__inicio_reserva__lt=fin # Empieza antes de que yo termine
            ).exclude(reserva=self.instance).aggregate(total=Sum('cantidad'))['total'] or 0
            
            # B. Ocupados por préstamos activos
            prestado = Prestamo.objects.filter(
                equipo=equipo,
                fecha_devolucion_real__isnull=True, # Aún no devuelto
                fecha_devolucion_estimada__gt=inicio, # Se devuelve después de que yo empiezo
                fecha_prestamo__lt=fin # Se prestó antes de que yo termine
            ).aggregate(total=Sum('cantidad_prestada'))['total'] or 0

            # C. Ocupados por mantenciones
            en_mantencion = Mantencion.objects.filter(
                equipo=equipo,
                fecha_fin__gte=inicio.date(), # Termina después de que yo empiezo
                fecha_inicio__lte=fin.date() # Empieza antes de que yo termine
            ).count()

            # --- CÁLCULO FINAL ---
            cantidad_ocupada = reservado_taller + prestado + en_mantencion
            disponible = stock_total - cantidad_ocupada
            
            if cantidad_solicitada > disponible:
                # Error si se pide más de lo disponible
                error_msg = f"Disponibilidad excedida. Solo quedan {disponible} unidades de '{equipo.nombre}' en ese horario (Ocupadas: {cantidad_ocupada})."
                # obtengo el form directo de la estructura
                form_con_error = equipos_solicitados[equipo.pk]['form']
                form_con_error.add_error('cantidad', error_msg)
                raise ValidationError("No hay suficiente stock para uno o más equipos en el horario seleccionado.")

# 4. Crear el Factory del FormSet
ReservaTallerEquipoFormSet = inlineformset_factory(
    ReservaTaller,                  # Modelo Padre
    ReservaTallerEquipo,            # Modelo Hijo (Through)
    form=FormReservaTallerEquipo,   # Formulario para cada línea
    formset=BaseReservaTallerEquipoFormSet, # Clase con la lógica de validación
    extra=1,                        # Empezar con 1 formulario de equipo vacío
    can_delete=True                 # Permitir eliminar equipos de la reserva
)