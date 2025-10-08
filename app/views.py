from django.shortcuts import render, redirect
from .models import Equipo, Solicitud, User
from .forms import EquipoForm, SolicitudForm # RegistroUsuarioForm
from django.contrib.auth.decorators import login_required

# Create your views here.
tDashboard = 'app/dashboard.html'
tSolicitudes = 'app/solicitudes.html'
tEquipos = 'app/equipos.html'
tUsuarios = 'app/usuarios.html'
tBase = 'app/base.html'
tLogin = 'app/login.html'

@login_required
def dashboard(request):
    data = {}
    return render(request, tDashboard, data)

@login_required
def login(request):
    data = {}
    return render(request, tLogin, data)

@login_required
def logout(request):
    data = {}
    return render(request, tLogin, data)

@login_required
def base(request):
    data = {}
    return render(request, tBase, data)

@login_required
def equipos(request):
    equipos = Equipo.objects.all()

    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipos')  # recarga la misma página
    else:
        form = EquipoForm()
    data = {
        "equipos": equipos,
        "form": form
    }
    return render(request, tEquipos, data)

@login_required
def solicitudes(request):
    solicitudes = Solicitud.objects.all()
    usuarios = User.objects.all()
    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('solicitudes')
    else:
        form = SolicitudForm()
        data = {
        "solicitudes": solicitudes,
        "form": form
    }
    return render(request, tSolicitudes, data)

@login_required
def usuarios(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_usuario')  # recarga la misma página
    else:
        form = RegistroUsuarioForm()
    
    usuarios = User.objects.all()  # obtenemos todos los usuarios

    return render(request, tUsuarios, {
        'form': form,
        'usuarios': usuarios
    })