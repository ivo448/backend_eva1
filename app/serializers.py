from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipo, Categoria, Reserva, Requerimiento, Mantencion, Perfil
from .validators import validar_fecha_futura, validar_descripcion_detallada
from django.db.models import Q

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
    fecha_inicio = serializers.DateTimeField(validators=[validar_fecha_futura])

    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'usuario_nombre', 'equipo', 'equipo_nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'creado_en']

    def validate(self, data):
        # 1. Validar coherencia de fechas (Inicio < Fin)
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise serializers.ValidationError({"fecha_fin": "La fecha de término debe ser posterior a la de inicio."})

        # 2. Validar que el equipo esté DISPONIBLE (no en mantención o prestado)
        # Nota: Usamos 'instance' para saber si estamos editando o creando.
        equipo = data.get('equipo')
        if equipo and equipo.estado != 'DISPONIBLE':
            raise serializers.ValidationError({"equipo": f"El equipo '{equipo.nombre}' no está disponible para reserva (Estado: {equipo.estado})."})

        # 3. Validar TOPE DE HORARIO (Solapamiento)
        # Buscamos reservas que choquen con el horario solicitado para ESTE equipo
        reservas_chocan = Reserva.objects.filter(
            equipo=data['equipo'],
            estado__in=['PENDIENTE', 'CONFIRMADA'], # Solo nos importan las activas
        ).filter(
            # Lógica de solapamiento:
            # (Inicio existente < Fin nuevo) Y (Fin existente > Inicio nuevo)
            Q(fecha_inicio__lt=data['fecha_fin']) & Q(fecha_fin__gt=data['fecha_inicio'])
        )

        # Si estamos editando una reserva existente, la excluimos de la búsqueda para que no choque consigo misma
        if self.instance:
            reservas_chocan = reservas_chocan.exclude(id=self.instance.id)

        if reservas_chocan.exists():
             raise serializers.ValidationError("Ya existe una reserva para este equipo en el horario seleccionado.")

        return data

class RequerimientoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.get_full_name')
    # 3. Aplicamos validacion de texto
    descripcion = serializers.CharField(validators=[validar_descripcion_detallada])

    class Meta:
        model = Requerimiento
        fields = ['id', 'usuario', 'usuario_nombre', 'descripcion', 'estado', 'fecha_solicitud']

class MantencionSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.ReadOnlyField(source='equipo.nombre')
    # 4. Aplicamos validacion de fecha futura
    fecha_programada = serializers.DateField(validators=[validar_fecha_futura])

    class Meta:
        model = Mantencion
        fields = ['id', 'equipo', 'equipo_nombre', 'fecha_programada', 'descripcion', 'estado', 'creado_en']