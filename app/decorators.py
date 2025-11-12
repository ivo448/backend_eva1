# app/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test

# --- DECORADORES (Para Vistas-Funciones como las de ReservaTaller) ---

def role_required(allowed_roles=[]):
    """
    Decorador para vistas-funciones que solo permite acceso a roles específicos.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                # Permitir Superadmin siempre
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                
                # Verificar rol de Perfil
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
panolero_required = role_required(allowed_roles=['PANOLERO', 'ADMIN'])
profesor_required = role_required(allowed_roles=['PROFESOR', 'ADMIN'])


# --- MIXINS ---

class PanoleroRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo Pañoleros y Admins"""
    def test_func(self):
        try:
            return self.request.user.perfil.rol in ['PANOLERO', 'ADMIN']
        except ObjectDoesNotExist:
            return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acceso denegado. Solo personal de Pañol.')
        return redirect('index')

class ProfesorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo Profesores y Admins"""
    def test_func(self):
        try:
            return self.request.user.perfil.rol in ['PROFESOR', 'ADMIN']
        except ObjectDoesNotExist:
            return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acceso denegado. Solo Profesores.')
        return redirect('index')