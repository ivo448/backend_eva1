"""
URL configuration for backend_eva1 project.
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    
    # -- CRUD SOLICITUDES --
    path('solicitudes/', views.listadoSolicitudes, name="solicitudes"),
    path('solicitudes/agregar/', views.agregarSolicitud, name="agregarSolicitud"),
    path('solicitudes/editar/<int:id>/', views.editarSolicitud, name="editarSolicitud"),
    path('solicitudes/detalle/<int:pk>/', views.SolicitudDetailView.as_view(), name="detalleSolicitud"),
    path('solicitudes/eliminar/<int:pk>/', views.SolicitudDeleteView.as_view(), name="eliminarSolicitud"),
    
    # -- CRUD EQUIPOS --
    path('equipos/', views.listadoEquipos, name="equipos"),
    path('equipos/agregar/', views.agregarEquipo, name="agregarEquipo"),
    path('equipos/editar/<int:id>/', views.editarEquipo, name="editarEquipo"),
    path('equipos/detalle/<int:pk>/', views.EquipoDetailView.as_view(), name="detalleEquipo"),
    path('equipos/eliminar/<int:pk>/', views.EquipoDeleteView.as_view(), name="eliminarEquipo"),
    
    # -- CRUD MANTENCIONES --
    path('mantenciones/', views.listadoMantenciones, name="mantenciones"),
    path('mantenciones/agregar/', views.agregarMantencion, name="agregarMantencion"),
    path('mantenciones/editar/<int:id>/', views.editarMantencion, name="editarMantencion"),
    path('mantenciones/detalle/<int:pk>/', views.MantencionDetailView.as_view(), name="detalleMantencion"),
    path('mantenciones/eliminar/<int:pk>/', views.MantencionDeleteView.as_view(), name="eliminarMantencion"),

    # -- CRUD PERFILES (USUARIOS) --
    path('perfiles/', views.listadoPerfiles, name="perfiles"),
    path('perfiles/editar/<int:id>/', views.editarPerfil, name="editarPerfil"),
    path('perfiles/detalle/<int:pk>/', views.PerfilDetailView.as_view(), name="detallePerfil"),
    # (Generalmente no se elimina un perfil/usuario directamente, pero se puede añadir)

    # -- CRUD PRESTAMOS --
    path('prestamos/', views.listadoPrestamos, name="prestamos"),
    path('prestamos/agregar/', views.agregarPrestamo, name="agregarPrestamo"),
    path('prestamos/editar/<int:id>/', views.editarPrestamo, name="editarPrestamo"),
    path('prestamos/detalle/<int:pk>/', views.PrestamoDetailView.as_view(), name="detallePrestamo"),
    path('prestamos/eliminar/<int:pk>/', views.PrestamoDeleteView.as_view(), name="eliminarPrestamo"),

    # -- CRUD RESERVA TALLER --
    path('reservas/', views.listadoReservasTaller, name="reservas_taller"),
    path('reservas/agregar/', views.agregarReservaTaller, name="agregarReservaTaller"),
    path('reservas/editar/<int:id>/', views.editarReservaTaller, name="editarReservaTaller"),
    path('reservas/detalle/<int:pk>/', views.ReservaTallerDetailView.as_view(), name="detalleReservaTaller"),
    path('reservas/eliminar/<int:pk>/', views.ReservaTallerDeleteView.as_view(), name="eliminarReservaTaller"),
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)