from django.contrib import admin
from .models import Equipo, Solicitud, Mantencion, Perfil, Prestamo, ReservaTaller

class EquipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cantidad', 'creado_por')
    search_fields = ('nombre', 'descripcion', 'creado_por__username')
    list_filter = ('cantidad', 'creado_por')

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'usuario', 'fecha', 'estado')
    search_fields = ('nombre', 'descripcion', 'usuario__username')
    list_filter = ('fecha', 'usuario', 'estado')

class MantencionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'equipo', 'fecha_inicio', 'fecha_fin', 'responsable')
    search_fields = ('nombre', 'descripcion', 'equipo__nombre', 'responsable__username')
    list_filter = ('equipo', 'responsable')

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'rut', 'telefono')
    search_fields = ('usuario__username', 'rut', 'rol')
    list_filter = ('rol',)

class PrestamoAdmin(admin.ModelAdmin):
    # 🚨 CAMBIO: Actualizados list_display y search_fields
    list_display = ('equipo', 'estudiante', 'registrado_por', 'cantidad_prestada', 'fecha_prestamo', 'fecha_devolucion_estimada', 'fecha_devolucion_real')
    search_fields = ('equipo__nombre', 'estudiante__username', 'registrado_por__username')
    list_filter = ('fecha_prestamo', 'fecha_devolucion_estimada', 'fecha_devolucion_real', 'estudiante')

class ReservaTallerAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'proposito', 'inicio_reserva', 'fin_reserva')
    search_fields = ('usuario__username', 'proposito')
    list_filter = ('inicio_reserva', 'fin_reserva')

admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Mantencion, MantencionAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(ReservaTaller, ReservaTallerAdmin)