from django.contrib import admin
from django.urls import path
from app import views  # Importamos todas las vistas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    
    # -- CRUD SOLICITUDES (CBV) --
    path('solicitudes/', views.SolicitudListView.as_view(), name="solicitudes"),
    path('solicitudes/agregar/', views.SolicitudCreateView.as_view(), name="agregarSolicitud"),
    path('solicitudes/editar/<int:pk>/', views.SolicitudUpdateView.as_view(), name="editarSolicitud"), # 'pk' es estándar para CBV
    path('solicitudes/detalle/<int:pk>/', views.SolicitudDetailView.as_view(), name="detalleSolicitud"),
    path('solicitudes/eliminar/<int:pk>/', views.SolicitudDeleteView.as_view(), name="eliminarSolicitud"),
    
    # -- CRUD EQUIPOS (CBV) --
    path('equipos/', views.EquipoListView.as_view(), name="equipos"),
    path('equipos/agregar/', views.EquipoCreateView.as_view(), name="agregarEquipo"),
    path('equipos/editar/<int:pk>/', views.EquipoUpdateView.as_view(), name="editarEquipo"), # 'pk' es estándar para CBV
    path('equipos/detalle/<int:pk>/', views.EquipoDetailView.as_view(), name="detalleEquipo"),
    path('equipos/eliminar/<int:pk>/', views.EquipoDeleteView.as_view(), name="eliminarEquipo"),
    
    # -- CRUD MANTENCIONES (CBV) --
    path('mantenciones/', views.MantencionListView.as_view(), name="mantenciones"),
    path('mantenciones/agregar/', views.MantencionCreateView.as_view(), name="agregarMantencion"),
    path('mantenciones/editar/<int:pk>/', views.MantencionUpdateView.as_view(), name="editarMantencion"), # 'pk' es estándar para CBV
    path('mantenciones/detalle/<int:pk>/', views.MantencionDetailView.as_view(), name="detalleMantencion"),
    path('mantenciones/eliminar/<int:pk>/', views.MantencionDeleteView.as_view(), name="eliminarMantencion"),

    # -- CRUD PERFILES (CBV) --
    path('perfiles/', views.PerfilListView.as_view(), name="perfiles"),
    path('perfiles/editar/<int:pk>/', views.PerfilUpdateView.as_view(), name="editarPerfil"),
    path('perfiles/detalle/<int:pk>/', views.PerfilDetailView.as_view(), name="detallePerfil"),

    # -- CRUD PRESTAMOS (CBV) --
    path('prestamos/', views.PrestamoListView.as_view(), name="prestamos"),
    path('prestamos/agregar/', views.PrestamoCreateView.as_view(), name="agregarPrestamo"),
    path('prestamos/editar/<int:pk>/', views.PrestamoUpdateView.as_view(), name="editarPrestamo"),
    path('prestamos/detalle/<int:pk>/', views.PrestamoDetailView.as_view(), name="detallePrestamo"),
    path('prestamos/eliminar/<int:pk>/', views.PrestamoDeleteView.as_view(), name="eliminarPrestamo"),

    # -- CRUD RESERVA TALLER (FBV - se mantiene por complejidad de formset) --
    path('reservas/', views.listadoReservasTaller, name="reservas_taller"),
    path('reservas/agregar/', views.agregarReservaTaller, name="agregarReservaTaller"),
    path('reservas/editar/<int:id>/', views.editarReservaTaller, name="editarReservaTaller"), # 'id' por FBV
    path('reservas/detalle/<int:pk>/', views.ReservaTallerDetailView.as_view(), name="detalleReservaTaller"),
    path('reservas/eliminar/<int:pk>/', views.ReservaTallerDeleteView.as_view(), name="eliminarReservaTaller"),
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)