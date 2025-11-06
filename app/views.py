from django.shortcuts import render, redirect
from .models import Equipo, Solicitud, Mantencion
from app.forms import FormEquipo, FormSolicitud, FormMantencion
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def index(request):
    data = {}
    return render(request, 'app/index.html', data)

# -- CRUD EQUIPOS --
@login_required
def listadoEquipos(request):
    equipos = Equipo.objects.all()
    data = {
        'equipos': equipos
    }
    return render(request, 'app/equipos.html', data)

@login_required
def agregarEquipo(request):
    form = FormEquipo()
    if request.method == "POST":
        form = FormEquipo(request.POST, request.FILES)
        if form.is_valid():
            equipo = form.save(commit=False)
            # asignar creador automáticamente si hay usuario autenticado
            if request.user.is_authenticated:
                equipo.creado_por = request.user
            equipo.save()
            return redirect('equipos')
    data = {
        "form": form
    }
    return render(request, 'app/agregarEquipo.html', data)

# Vista basada en clase para eliminar con modal
class EquipoDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Equipo
    template_name = 'app/eliminarEquipo.html'
    success_message = 'Equipo eliminado correctamente.'
    success_url = reverse_lazy('equipos')

# -- CRUD SOLICITUDES --
@login_required
def listadoSolicitudes(request):
    solicitudes = Solicitud.objects.all()
    data = {
        'solicitudes': solicitudes
    }
    return render(request, 'app/solicitudes.html', data)

@login_required
def agregarSolicitud(request):
    form = FormSolicitud()
    if request.method == "POST":
        form = FormSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('solicitudes')
    data = {
        "form": form
    }
    return render(request, 'app/agregarSolicitud.html', data)

# Vista basada en clase para eliminar con modal
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
            return redirect('mantenciones')
    data = {'form': form}
    return render(request, 'app/agregarMantencion.html', data)

@login_required
def editarMantencion(request, id):
    mantencion = Mantencion.objects.get(id=id)
    form = FormMantencion(instance=mantencion)
    if request.method == "POST":
        form = FormMantencion(request.POST, instance=mantencion)
        if form.is_valid():
            form.save()
            return redirect('mantenciones')
    data = {'form': form, 'id': id}
    return render(request, 'app/agregarMantencion.html', data)

# Vista basada en clase para eliminar con modal
class MantencionDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Mantencion
    template_name = 'app/eliminarMantencion.html'
    success_message = 'Mantención eliminada correctamente.'
    success_url = reverse_lazy('mantenciones')