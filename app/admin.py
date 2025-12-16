from django.contrib import admin
from .models import Categoria, Equipo, Reserva, Mantencion, Requerimiento

# --- PERSONALIZACIÓN DEL HEADER ---
# Esto cambia el título azul de "Django Administration" por el nombre de tu proyecto
admin.site.site_header = "Administración Pañol INACAP"
admin.site.site_title = "Portal de Pañol"
admin.site.index_title = "Bienvenido al Sistema de Gestión de Activos"

# --- CATEGORÍAS ---
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

# --- EQUIPOS ---
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista
    list_display = ('nombre', 'marca', 'modelo', 'estado', 'categoria')
    # Filtros laterales (muy útiles)
    list_filter = ('estado', 'categoria', 'marca')
    # Barra de búsqueda (busca por nombre o marca)
    search_fields = ('nombre', 'marca', 'modelo')
    # Paginación
    list_per_page = 20

# --- RESERVAS ---
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipo', 'usuario', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio')
    # Para buscar por nombre de usuario o nombre de equipo (usando __)
    search_fields = ('usuario__username', 'usuario__first_name', 'equipo__nombre')
    
    # Acción rápida para marcar devoluciones masivas
    actions = ['marcar_finalizada']

    @admin.action(description='Marcar reservas seleccionadas como FINALIZADA')
    def marcar_finalizada(self, request, queryset):
        queryset.update(estado='FINALIZADA')

# --- MANTENCIONES ---
@admin.register(Mantencion)
class MantencionAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'fecha_programada', 'estado', 'descripcion_corta')
    list_filter = ('estado', 'fecha_programada')
    search_fields = ('equipo__nombre', 'descripcion')

    # Truco para acortar descripciones largas en la tabla
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

# --- REQUERIMIENTOS ---
@admin.register(Requerimiento)
class RequerimientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descripcion_corta', 'fecha_solicitud', 'prioridad', 'estado')
    list_filter = ('estado', 'prioridad', 'fecha_solicitud')
    search_fields = ('usuario__username', 'descripcion')

    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Solicitud'