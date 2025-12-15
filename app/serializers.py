from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipo, Categoria, Reserva, Requerimiento, Mantencion, Perfil

class UserSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(write_only=True, required=False, default='PROFESOR')
    rol_actual = serializers.CharField(source='perfil.rol', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'rol_actual']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        rol_nombre = validated_data.pop('rol', 'PROFESOR')
        user = User.objects.create_user(**validated_data)
        Perfil.objects.create(usuario=user, rol=rol_nombre)
        return user

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'marca', 'modelo', 'categoria', 'categoria_nombre', 'estado', 'fecha_ingreso', 'observaciones']

class ReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.get_full_name')
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')

    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'usuario_nombre', 'equipo', 'equipo_nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'creado_en']

class RequerimientoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.get_full_name')

    class Meta:
        model = Requerimiento
        fields = ['id', 'usuario', 'usuario_nombre', 'descripcion', 'estado', 'fecha_solicitud']

class MantencionSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')

    class Meta:
        model = Mantencion
        fields = ['id', 'equipo', 'equipo_nombre', 'fecha_programada', 'descripcion', 'estado', 'creado_en']