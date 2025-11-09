from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipo, Solicitud, Mantencion, Perfil, Prestamo, ReservaTaller
from app.forms import FormEquipo, FormSolicitud, FormMantencion, FormPerfil, FormPrestamo, FormReservaTaller
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_modal_forms.generic import BSModalDeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib import messages # Importar mensajes

# ... Vistas de login, logout, index (sin cambios) ...
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            messages.success(request, f'Bienvenido {form.get_user().username}.') # Mensaje de bienvenida
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.') # Mensaje de logout
    return redirect('login')

@login_required
def index(request):
    # Renombrado de 'dashboard' a 'index' para coincidir con urls.py
    data = {}
    return render(request, 'app/index.html', data)


# -- CRUD EQUIPOS --
@login_required
def listadoEquipos(request):
    equipos = Equipo.objects.all()
    data = {'equipos': equipos}
    return render(request, 'app/equipos.html', data)

@login_required
def agregarEquipo(request):
    form = FormEquipo()
    if request.method == "POST":
        form = FormEquipo(request.POST, request.FILES)
        if form.is_valid():
            equipo = form.save(commit=False)
            if request.user.is_authenticated:
                equipo.creado_por = request.user
            equipo.save()
            messages.success(request, 'Equipo agregado correctamente.') # Mensaje
            return redirect('equipos')
        else:
            messages.error(request, 'Error al agregar el equipo. Revisa el formulario.')
    data = {"form": form, "titulo": "Agregar Equipo"}
    return render(request, 'app/equipo_form.html', data)

@login_required
def editarEquipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    form = FormEquipo(instance=equipo)
    if request.method == "POST":
        form = FormEquipo(request.POST, request.FILES, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipo actualizado correctamente.') # Mensaje
            return redirect('equipos')
        else:
            messages.error(request, 'Error al actualizar. Revisa el formulario.')
    data = {'form': form, 'titulo': 'Editar Equipo'}
    return render(request, 'app/equipo_form.html', data)

class EquipoDetailView(LoginRequiredMixin, DetailView):
    model = Equipo
    template_name = 'app/equipo_detail.html'
    context_object_name = 'equipo'

class EquipoDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Equipo
    template_name = 'app/eliminarEquipo.html'
    success_message = 'Equipo eliminado correctamente.'
    success_url = reverse_lazy('equipos')

# -- CRUD SOLICITUDES --
@login_required
def listadoSolicitudes(request):
    solicitudes = Solicitud.objects.all()
    data = {'solicitudes': solicitudes}
    return render(request, 'app/solicitudes.html', data)

@login_required
def agregarSolicitud(request):
    form = FormSolicitud()
    if request.method == "POST":
        form = FormSolicitud(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            if not solicitud.usuario:
                solicitud.usuario = request.user
            solicitud.save()
            messages.success(request, 'Solicitud agregada correctamente.') # Mensaje
            return redirect('solicitudes')
        else:
            messages.error(request, 'Error al agregar la solicitud.')
    data = {"form": form, "titulo": "Agregar Solicitud"}
    return render(request, 'app/solicitud_form.html', data)

@login_required
def editarSolicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    form = FormSolicitud(instance=solicitud)
    if request.method == "POST":
        form = FormSolicitud(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud actualizada correctamente.') # Mensaje
            return redirect('solicitudes')
        else:
            messages.error(request, 'Error al actualizar la solicitud.')
    data = {'form': form, 'titulo': 'Editar Solicitud'}
    return render(request, 'app/solicitud_form.html', data)

class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'app/solicitud_detail.html'
    context_object_name = 'solicitud'

class SolicitudDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Solicitud
    template_name = 'app/eliminarSolicitud.html'
    success_message = 'Solicitud eliminada correctamente.'
    success_url = reverse_lazy('solicitudes')

# -- CRUD MANTENCIONES --
@login_required
def listadoMantenciones(request):
    mantenciones = Mantencion.objects.all()
    data = {'mantenciones': mantenciones}
    return render(request, 'app/mantenciones.html', data)

@login_required
def agregarMantencion(request):
    form = FormMantencion()
    if request.method == "POST":
        form = FormMantencion(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantención agregada correctamente.') # Mensaje
            return redirect('mantenciones')
        else:
            messages.error(request, 'Error al agregar la mantención.')
    data = {'form': form, 'titulo': 'Agregar Mantención'}
    return render(request, 'app/mantencion_form.html', data)

@login_required
def editarMantencion(request, id):
    mantencion = get_object_or_404(Mantencion, id=id)
    form = FormMantencion(instance=mantencion)
    if request.method == "POST":
        form = FormMantencion(request.POST, instance=mantencion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantención actualizada correctamente.') # Mensaje
            return redirect('mantenciones')
        else:
            messages.error(request, 'Error al actualizar la mantención.')
    data = {'form': form, 'titulo': f'Editar Mantención: {mantencion.nombre}'}
    return render(request, 'app/mantencion_form.html', data)

class MantencionDetailView(LoginRequiredMixin, DetailView):
    model = Mantencion
    template_name = 'app/mantencion_detail.html'
    context_object_name = 'mantencion'

class MantencionDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Mantencion
    template_name = 'app/eliminarMantencion.html'
    success_message = 'Mantención eliminada correctamente.'
    success_url = reverse_lazy('mantenciones')

# --- CRUD PERFILES ---
@login_required
def listadoPerfiles(request):
    perfiles = Perfil.objects.all()
    return render(request, 'app/perfil_list.html', {'perfiles': perfiles})

@login_required
def editarPerfil(request, id):
    perfil = get_object_or_404(Perfil, id=id)
    if request.method == 'POST':
        form = FormPerfil(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('perfiles')
    else:
        form = FormPerfil(instance=perfil)
    return render(request, 'app/perfil_form.html', {'form': form, 'titulo': f'Editar Perfil de {perfil.usuario.username}'})

class PerfilDetailView(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = 'app/perfil_detail.html'
    context_object_name = 'perfil'

# --- CRUD PRESTAMOS ---
@login_required
def listadoPrestamos(request):
    prestamos = Prestamo.objects.select_related('solicitud', 'equipo').all()
    return render(request, 'app/prestamo_list.html', {'prestamos': prestamos})

@login_required
def agregarPrestamo(request):
    if request.method == 'POST':
        form = FormPrestamo(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            # Restar del stock
            prestamo.equipo.cantidad -= prestamo.cantidad_prestada
            prestamo.equipo.save()
            prestamo.save()
            messages.success(request, 'Préstamo registrado. Stock actualizado.')
            return redirect('prestamos')
    else:
        form = FormPrestamo()
    return render(request, 'app/prestamo_form.html', {'form': form, 'titulo': 'Registrar Préstamo'})

@login_required
def editarPrestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    # Guardar cantidad original por si se modifica
    cantidad_original = prestamo.cantidad_prestada 
    
    if request.method == 'POST':
        form = FormPrestamo(request.POST, instance=prestamo)
        if form.is_valid():
            # Ajustar stock al editar
            cantidad_nueva = form.cleaned_data['cantidad_prestada']
            diferencia = cantidad_nueva - cantidad_original
            
            prestamo.equipo.cantidad -= diferencia # Ajustar stock
            prestamo.equipo.save()
            
            form.save()
            messages.success(request, 'Préstamo actualizado.')
            return redirect('prestamos')
    else:
        form = FormPrestamo(instance=prestamo)
    return render(request, 'app/prestamo_form.html', {'form': form, 'titulo': 'Editar Préstamo'})

class PrestamoDetailView(LoginRequiredMixin, DetailView):
    model = Prestamo
    template_name = 'app/prestamo_detail.html'
    context_object_name = 'prestamo'

class PrestamoDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Prestamo
    template_name = 'app/prestamo_confirm_delete.html'
    success_message = 'Préstamo eliminado. (Stock no fue restaurado automáticamente).'
    success_url = reverse_lazy('prestamos')

# --- CRUD RESERVA TALLER ---
@login_required
def listadoReservasTaller(request):
    reservas = ReservaTaller.objects.select_related('usuario').all().order_by('fecha_reserva', 'hora_inicio')
    return render(request, 'app/reserva_taller_list.html', {'reservas': reservas})

@login_required
def agregarReservaTaller(request):
    if request.method == 'POST':
        form = FormReservaTaller(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva de taller registrada.')
            return redirect('reservas_taller')
    else:
        form = FormReservaTaller()
    return render(request, 'app/reserva_taller_form.html', {'form': form, 'titulo': 'Nueva Reserva de Taller'})

@login_required
def editarReservaTaller(request, id):
    reserva = get_object_or_404(ReservaTaller, id=id)
    if request.method == 'POST':
        form = FormReservaTaller(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva de taller actualizada.')
            return redirect('reservas_taller')
    else:
        form = FormReservaTaller(instance=reserva)
    return render(request, 'app/reserva_taller_form.html', {'form': form, 'titulo': 'Editar Reserva'})

class ReservaTallerDetailView(LoginRequiredMixin, DetailView):
    model = ReservaTaller
    template_name = 'app/reserva_taller_detail.html'
    context_object_name = 'reserva'

class ReservaTallerDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ReservaTaller
    template_name = 'app/reserva_taller_confirm_delete.html'
    success_message = 'Reserva de taller eliminada.'
    success_url = reverse_lazy('reservas_taller')