from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Equipo, Solicitud, Mantencion, Perfil, Prestamo, 
    ReservaTaller, ReservaTallerEquipo
)
from app.forms import (
    FormEquipo, FormSolicitud, FormMantencion, FormPerfil, FormPrestamo, 
    FormReservaTaller, ReservaTallerEquipoFormSet
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_modal_forms.generic import BSModalDeleteView
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin

# 1. IMPORTAR LOS MIXINS Y DECORADORES CORRECTOS
from .decorators import panolero_required, profesor_required
from .decorators import PanoleroRequiredMixin, ProfesorRequiredMixin

# --- VISTAS DE AUTENTICACIÓN Y PRINCIPALES (FBV) ---
# (Se mantienen como FBV por su lógica única)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            messages.success(request, f'Bienvenido {form.get_user().username}.')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def index(request):
    data = {}
    return render(request, 'app/index.html', data)

# --- CRUD EQUIPOS (CBV) ---
# (Solo Pañoleros y Admin)

class EquipoListView(PanoleroRequiredMixin, ListView):
    model = Equipo
    template_name = 'app/equipos.html'
    context_object_name = 'equipos'

class EquipoDetailView(PanoleroRequiredMixin, DetailView):
    model = Equipo
    template_name = 'app/equipo_detail.html'
    context_object_name = 'equipo'

class EquipoCreateView(PanoleroRequiredMixin, SuccessMessageMixin, CreateView):
    model = Equipo
    form_class = FormEquipo
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('equipos')
    success_message = "Equipo agregado correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Agregar Equipo"
        return context
    
    def form_valid(self, form):
        # Asignar el usuario actual como creador
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

class EquipoUpdateView(PanoleroRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Equipo
    form_class = FormEquipo
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('equipos')
    success_message = "Equipo actualizado correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Equipo: {self.object.nombre}"
        return context

class EquipoDeleteView(PanoleroRequiredMixin, BSModalDeleteView):
    model = Equipo
    template_name = 'app/eliminarEquipo.html'
    success_message = 'Equipo eliminado correctamente.'
    success_url = reverse_lazy('equipos')


# --- CRUD SOLICITUDES (CBV) ---
# (Pañoleros, Profesores y Admin)

class SolicitudListView(ProfesorRequiredMixin, ListView):
    model = Solicitud
    template_name = 'app/solicitudes.html'
    context_object_name = 'solicitudes'

class SolicitudDetailView(ProfesorRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'app/solicitud_detail.html'
    context_object_name = 'solicitud'

class SolicitudCreateView(ProfesorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Solicitud
    form_class = FormSolicitud
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('solicitudes')
    success_message = "Solicitud agregada correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Agregar Solicitud"
        return context

    def form_valid(self, form):
        # Asignar usuario si no se seleccionó (o si el campo está oculto)
        if not form.instance.usuario:
            form.instance.usuario = self.request.user
        return super().form_valid(form)

class SolicitudUpdateView(ProfesorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Solicitud
    form_class = FormSolicitud
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('solicitudes')
    success_message = "Solicitud actualizada correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Solicitud: {self.object.nombre}"
        return context

class SolicitudDeleteView(ProfesorRequiredMixin, BSModalDeleteView):
    model = Solicitud
    template_name = 'app/eliminarSolicitud.html'
    success_message = 'Solicitud eliminada correctamente.'
    success_url = reverse_lazy('solicitudes')


# --- CRUD MANTENCIONES (CBV) ---
# (Solo Pañoleros y Admin)

class MantencionListView(PanoleroRequiredMixin, ListView):
    model = Mantencion
    template_name = 'app/mantenciones.html'
    context_object_name = 'mantenciones'

class MantencionDetailView(PanoleroRequiredMixin, DetailView):
    model = Mantencion
    template_name = 'app/mantencion_detail.html'
    context_object_name = 'mantencion'

class MantencionCreateView(PanoleroRequiredMixin, SuccessMessageMixin, CreateView):
    model = Mantencion
    form_class = FormMantencion
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('mantenciones')
    success_message = "Mantención agregada correctamente."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Agregar Mantención"
        return context

class MantencionUpdateView(PanoleroRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Mantencion
    form_class = FormMantencion
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('mantenciones')
    success_message = "Mantención actualizada correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Mantención: {self.object.nombre}"
        return context

class MantencionDeleteView(PanoleroRequiredMixin, BSModalDeleteView):
    model = Mantencion
    template_name = 'app/eliminarMantencion.html'
    success_message = 'Mantención eliminada correctamente.'
    success_url = reverse_lazy('mantenciones')


# --- CRUD PERFILES (CBV) ---

class PerfilListView(PanoleroRequiredMixin, ListView): # Permitimos a Staff ver
    model = Perfil
    template_name = 'app/perfil_list.html'
    context_object_name = 'perfiles'

class PerfilDetailView(PanoleroRequiredMixin, DetailView): # Permitimos a Staff ver
    model = Perfil
    template_name = 'app/perfil_detail.html'
    context_object_name = 'perfil'

class PerfilUpdateView(PanoleroRequiredMixin, SuccessMessageMixin, UpdateView): # Permitimos a Staff editar
    model = Perfil
    form_class = FormPerfil
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('perfiles')
    success_message = "Perfil actualizado."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Perfil de {self.object.usuario.username}"
        return context

# --- CRUD PRESTAMOS (CBV con lógica de STOCK) ---
# (Solo Pañoleros y Admin)

class PrestamoListView(PanoleroRequiredMixin, ListView):
    model = Prestamo
    template_name = 'app/prestamo_list.html'
    context_object_name = 'prestamos'
    queryset = Prestamo.objects.select_related('estudiante', 'equipo', 'registrado_por').all()

class PrestamoDetailView(PanoleroRequiredMixin, DetailView):
    model = Prestamo
    template_name = 'app/prestamo_detail.html'
    context_object_name = 'prestamo'

class PrestamoCreateView(PanoleroRequiredMixin, SuccessMessageMixin, CreateView):
    model = Prestamo
    form_class = FormPrestamo
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('prestamos')
    success_message = "Préstamo registrado. Stock actualizado."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Préstamo"
        return context

    @transaction.atomic
    def form_valid(self, form):
        prestamo = form.save(commit=False)
        
        # 🚨 NUEVO: Asignar al Pañolero logueado
        prestamo.registrado_por = self.request.user
        
        # Lógica de stock (sin cambios)
        prestamo.equipo.cantidad -= prestamo.cantidad_prestada
        prestamo.equipo.save()
        messages.success(self.request, f"Stock de {prestamo.equipo.nombre} reducido a {prestamo.equipo.cantidad}.")
        
        # Guardamos el préstamo ahora que tiene todos los datos
        prestamo.save()
        
        # Llamamos a super().form_valid() después de guardar
        # para que se establezca self.object y SuccessMessageMixin funcione.
        return super().form_valid(form)

class PrestamoUpdateView(PanoleroRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Prestamo
    form_class = FormPrestamo
    template_name = 'app/generic_form.html'
    success_url = reverse_lazy('prestamos')
    success_message = "Préstamo actualizado. Stock ajustado."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Préstamo"
        return context
    
    def get_initial(self):
        # Guardamos la cantidad original para calcular la diferencia
        self.cantidad_original = self.get_object().cantidad_prestada
        return super().get_initial()

    @transaction.atomic
    def form_valid(self, form):
        cantidad_nueva = form.cleaned_data['cantidad_prestada']
        cantidad_original = self.cantidad_original
        diferencia = cantidad_nueva - cantidad_original
        
        equipo = form.instance.equipo
        equipo.cantidad -= diferencia # Ajustar stock
        equipo.save()
        messages.info(self.request, f"Stock de {equipo.nombre} ajustado a {equipo.cantidad}.")
        return super().form_valid(form)

class PrestamoDeleteView(PanoleroRequiredMixin, BSModalDeleteView):
    model = Prestamo
    template_name = 'app/prestamo_confirm_delete.html'
    success_message = 'Préstamo eliminado.'
    success_url = reverse_lazy('prestamos')
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Lógica para restaurar stock al eliminar
        prestamo = self.get_object()
        equipo = prestamo.equipo
        cantidad_a_devolver = prestamo.cantidad_prestada
        
        # Solo devolver si el préstamo no había sido marcado como devuelto
        if not prestamo.fecha_devolucion_real: 
            equipo.cantidad += cantidad_a_devolver
            equipo.save()
            messages.success(request, f"Stock de {equipo.nombre} restaurado a {equipo.cantidad}.")
        else:
             messages.warning(request, "Préstamo eliminado (el equipo ya había sido devuelto, no se ajustó stock).")
             
        return super().post(request, *args, **kwargs)


# --- CRUD RESERVA TALLER (FBV - Complejo por FormSet) ---
# (Solo Profesores y Admin)

@login_required
@profesor_required
def listadoReservasTaller(request):
    reservas = ReservaTaller.objects.select_related('usuario').all().order_by('inicio_reserva')
    return render(request, 'app/reserva_taller_list.html', {'reservas': reservas})

@login_required
@profesor_required
@transaction.atomic
def agregarReservaTaller(request):
    if request.method == 'POST':
        form = FormReservaTaller(request.POST)
        formset = ReservaTallerEquipoFormSet(request.POST, instance=ReservaTaller())
        
        if form.is_valid():
            reserva = form.save(commit=False)
            formset = ReservaTallerEquipoFormSet(request.POST, instance=reserva)
            
            if formset.is_valid():
                reserva.save()
                formset.save()
                messages.success(request, 'Reserva de taller y equipos registrada correctamente.')
                return redirect('reservas_taller')
            else:
                messages.error(request, 'Error al reservar. Revisa los equipos solicitados y la disponibilidad.')
        else:
            messages.error(request, 'Error en los datos de la reserva. Revisa el formulario.')
    
    else: # Método GET
        form = FormReservaTaller()
        formset = ReservaTallerEquipoFormSet(instance=ReservaTaller())

    return render(request, 'app/reserva_taller_form.html', {
        'form': form, 
        'formset': formset,
        'titulo': 'Nueva Reserva de Taller'
    })

@login_required
@profesor_required
@transaction.atomic
def editarReservaTaller(request, id):
    reserva = get_object_or_404(ReservaTaller, id=id)
    
    if request.method == 'POST':
        form = FormReservaTaller(request.POST, instance=reserva)
        formset = ReservaTallerEquipoFormSet(request.POST, instance=reserva)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Reserva de taller actualizada.')
            return redirect('reservas_taller')
        else:
            messages.error(request, 'Error al actualizar. Revisa el formulario y la disponibilidad de equipos.')
            
    else: # Método GET
        form = FormReservaTaller(instance=reserva)
        formset = ReservaTallerEquipoFormSet(instance=reserva)
    
    return render(request, 'app/reserva_taller_form.html', {
        'form': form, 
        'formset': formset,
        'titulo': 'Editar Reserva de Taller'
    })

class ReservaTallerDetailView(ProfesorRequiredMixin, DetailView):
    model = ReservaTaller
    template_name = 'app/reserva_taller_detail.html'
    context_object_name = 'reserva'

class ReservaTallerDeleteView(ProfesorRequiredMixin, BSModalDeleteView):
    model = ReservaTaller
    template_name = 'app/reserva_taller_confirm_delete.html'
    success_message = 'Reserva de taller eliminada.'
    success_url = reverse_lazy('reservas_taller')