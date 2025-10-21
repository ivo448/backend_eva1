"""
URL configuration for backend_eva1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    path('agregarSolicitud/', views.agregarSolicitud, name="agregarSolicitud"),
    path('eliminarSolicitud/<int:pk>/', views.SolicitudDeleteView.as_view(), name="eliminarSolicitud"),
    # -- CRUD EQUIPOS --
    path('equipos/', views.listadoEquipos, name="equipos"),
    path('agregarEquipo/', views.agregarEquipo, name="agregarEquipo"),
    path('eliminarEquipo/<int:pk>/', views.EquipoDeleteView.as_view(), name="eliminarEquipo"),
    # -- CRUD MANTENCIONES --
    path('mantenciones/', views.listadoMantenciones, name="mantenciones"),
    path('agregarMantencion/', views.agregarMantencion, name="agregarMantencion"),
    path('editarMantencion/<int:id>/', views.editarMantencion, name="editarMantencion"),
    path('eliminarMantencion/<int:pk>/', views.MantencionDeleteView.as_view(), name="eliminarMantencion"),
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)