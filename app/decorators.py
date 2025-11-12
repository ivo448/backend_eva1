# app/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test

# --- DECORADORES (Para Vistas-Funciones como las de ReservaTaller) ---

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if request.user.perfil.rol in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'Acceso denegado. No tienes los permisos necesarios.')
                    return redirect('index')
            except ObjectDoesNotExist:
                messages.error(request, 'Error: Tu usuario no tiene un perfil asignado.')
                return redirect('index')
        return wrapper
    return decorator

# Decoradores específicos
panolero_required = role_required(allowed_roles=['PANOLERO', 'ADMIN', 'DIRECTORCARRERA'])
profesor_required = role_required(allowed_roles=['PROFESOR', 'ADMIN', 'DIRECTORCARRERA'])

# --- MIXINS (Para Vistas-Clases) ---

class PanoleroRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo Pañoleros, Director de Carrera y Admins"""
    def test_func(self):
        try:
            return self.request.user.perfil.rol in ['PANOLERO', 'ADMIN', 'DIRECTORCARRERA']
        except ObjectDoesNotExist:
            return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acceso denegado. Solo personal de Pañol.')
        return redirect('index')

class ProfesorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo Profesores, Director de Carrera y Admins"""
    def test_func(self):
        try:
            return self.request.user.perfil.rol in ['PROFESOR', 'ADMIN', 'DIRECTORCARRERA']
        except ObjectDoesNotExist:
            return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acceso denegado. Solo Profesores.')
        return redirect('index')

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Todos los roles de staff (Pañoleros, Profesores, Director, Admin)"""
    def test_func(self):
        try:
            # Incluye a todos excepto 'ESTUDIANTE'
            return self.request.user.perfil.rol in ['PANOLERO', 'PROFESOR', 'ADMIN', 'DIRECTORCARRERA']
        except ObjectDoesNotExist:
            return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acceso denegado. No tienes permisos suficientes.')
        return redirect('index')