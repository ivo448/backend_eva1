from django.shortcuts import render, redirect
from .models import Equipo, Solicitud, User
from .forms import EquipoForm, SolicitudForm, RegistroUsuarioForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

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

def login(request):
    data = {}
    loginView = auth_views.LoginView.as_view(template_name=tLogin)
    return loginView(request)

def logout(request):
    logoutView = auth_views.LogoutView.as_view(next_page='login')
    return logoutView(request)

def base(request):
    data = {}
    return render(request, tBase, data)

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
        "usuarios": usuarios,
        "form": form
    }
    return render(request, tSolicitudes, data)

@login_required
@permission_required('auth.view_user', raise_exception=True)
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