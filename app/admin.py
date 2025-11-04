from django.contrib import admin
from app.models import Equipo, Solicitud, Mantencion

class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', '']

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['', '', '']

class MantencionAdmin(admin.ModelAdmin):
    list_display = ['', '', '']

# Register your models here.
admin.site.register(Equipo)
admin.site.register(Solicitud)
admin.site.register(Mantencion)