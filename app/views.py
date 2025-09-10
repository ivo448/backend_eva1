from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def logout(request):
    logoutView = auth_views.LogoutView.as_view(next_page='login')
    return logoutView(request)

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
    solicitudes = Solicitud.objects.all().order_by('-fecha')
    usuarios = User.objects.all()
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        usuario_id = request.POST.get('usuario')
        descripcion = request.POST.get('descripcion')
        if nombre and usuario_id and descripcion:
            usuario = User.objects.get(pk=usuario_id)
            Solicitud.objects.create(
                nombre=nombre,
                usuario=usuario,
                descripcion=descripcion
            )
            return redirect('solicitudes')
        else:
            return render(request, tSolicitudes, {
                "solicitudes": solicitudes,
                "usuarios": usuarios,
                "error": "Todos los campos son obligatorios."
            })
    return render(request, tSolicitudes, {
        "solicitudes": solicitudes,
        "usuarios": usuarios,
        "title": "Solicitudes"
    })

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