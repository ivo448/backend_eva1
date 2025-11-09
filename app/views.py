from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Equipo, Solicitud, Mantencion, Perfil, Prestamo, 
    ReservaTaller, ReservaTallerEquipo
)
from app.forms import (
    FormEquipo, FormSolicitud, FormMantencion, FormPerfil, FormPrestamo, 
    FormReservaTaller, ReservaTallerEquipoFormSet # Importar el FormSet
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_modal_forms.generic import BSModalDeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction # Importar para transacciones atómicas

# ... (Vistas de login, logout, index, y CRUDs de Equipo, Solicitud, Mantencion, Perfil, Prestamo) ...
# (Asegúrate de que las vistas anteriores estén aquí)


# --- CRUD RESERVA TALLER (ACTUALIZADO) ---
@login_required
def listadoReservasTaller(request):
    reservas = ReservaTaller.objects.select_related('usuario').all().order_by('inicio_reserva')
    return render(request, 'app/reserva_taller_list.html', {'reservas': reservas})

@login_required
@transaction.atomic # Asegura que si el formset falla, la reserva tampoco se cree
def agregarReservaTaller(request):
    if request.method == 'POST':
        form = FormReservaTaller(request.POST)
        formset = ReservaTallerEquipoFormSet(request.POST, instance=ReservaTaller()) # Formset vacío
        
        if form.is_valid():
            # Guardar la reserva (padre) primero para obtener un ID
            reserva = form.save(commit=False)
            
            # Asignar la instancia de reserva al formset
            formset = ReservaTallerEquipoFormSet(request.POST, instance=reserva)
            
            if formset.is_valid():
                # Guardar la reserva y luego el formset (los equipos)
                reserva.save()
                formset.save()
                messages.success(request, 'Reserva de taller y equipos registrada correctamente.')
                return redirect('reservas_taller')
            else:
                # Errores de validación del formset (ej. disponibilidad)
                messages.error(request, 'Error al reservar. Revisa los equipos solicitados y la disponibilidad.')
        else:
            messages.error(request, 'Error en los datos de la reserva. Revisa el formulario.')
    
    else: # Método GET
        form = FormReservaTaller()
        # Creamos un formset vacío (con 'extra=1' formulario)
        formset = ReservaTallerEquipoFormSet(instance=ReservaTaller())

    return render(request, 'app/reserva_taller_form.html', {
        'form': form, 
        'formset': formset,
        'titulo': 'Nueva Reserva de Taller'
    })

@login_required
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

class ReservaTallerDetailView(LoginRequiredMixin, DetailView):
    model = ReservaTaller
    template_name = 'app/reserva_taller_detail.html'
    context_object_name = 'reserva'

class ReservaTallerDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ReservaTaller
    template_name = 'app/reserva_taller_confirm_delete.html'
    success_message = 'Reserva de taller eliminada.'
    success_url = reverse_lazy('reservas_taller')