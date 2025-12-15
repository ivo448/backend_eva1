from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Categoria, Equipo, Perfil, Reserva, Requerimiento, Mantencion

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil (Rol)'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo', 'categoria', 'estado')
    list_filter = ('estado', 'categoria')
    search_fields = ('nombre', 'modelo')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'equipo', 'fecha_inicio', 'estado')
    list_filter = ('estado', 'fecha_inicio')

@admin.register(Requerimiento)
class RequerimientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descripcion', 'estado', 'fecha_solicitud')
    list_filter = ('estado',)

@admin.register(Mantencion)
class MantencionAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'fecha_programada', 'estado')
    list_filter = ('estado', 'fecha_programada')