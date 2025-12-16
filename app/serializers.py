from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipo, Categoria, Reserva, Requerimiento, Mantencion

# --- SERIALIZER DE USUARIO ---
class UserSerializer(serializers.ModelSerializer):
    # Devuelve una lista de strings con TODOS los permisos efectivos
    # Ej: {'app.add_equipo', 'app.view_reserva', 'app.delete_mantencion'}
    permissions = serializers.SerializerMethodField()
    
    # Nombre completo
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'permissions']

    def get_permissions(self, obj):
        # busca permisos directos + permisos de grupos
        return obj.get_all_permissions()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

# --- CATEGORÍAS ---
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# --- EQUIPOS ---
class EquipoSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre de la categoría en lugar del ID
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Equipo
        fields = '__all__'

# --- RESERVAS ---
class ReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')

    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ('usuario',) # El usuario se asigna automáticamente en el ViewSet

# --- MANTENCIONES ---
class MantencionSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')

    class Meta:
        model = Mantencion
        fields = '__all__'

# --- REQUERIMIENTOS ---
class RequerimientoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Requerimiento
        fields = '__all__'
        read_only_fields = ('usuario', 'fecha_solicitud')