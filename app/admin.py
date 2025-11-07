from django.contrib import admin
from .models import Equipo, Solicitud, Mantencion


class EquipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cantidad', 'creado_por')
    search_fields = ('nombre', 'descripcion', 'creado_por__username')
    list_filter = ('cantidad', 'creado_por')


class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'usuario', 'fecha')
    search_fields = ('nombre', 'descripcion', 'usuario__username')
    list_filter = ('fecha', 'usuario')


class MantencionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'equipo', 'fecha_inicio', 'fecha_fin', 'responsable')
    search_fields = ('nombre', 'descripcion', 'equipo__nombre', 'responsable__username')
    list_filter = ('equipo', 'responsable')


admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Mantencion, MantencionAdmin)