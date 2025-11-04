from rest_framework import serializers
from .models import Equipo, Solicitud, Mantencion
from .validators import validate_fecha_range, validate_fecha_not_past

class EquipoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'descripcion', 'cantidad', 'imagen', 'imagen_url']
        read_only_fields = ['id', 'imagen_url']

    def get_imagen_url(self, obj):
        if obj.imagen:
            return self.context['request'].build_absolute_uri(obj.imagen.url)
        return None

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'nombre', 'fecha', 'descripcion']
        read_only_fields = ['id']

    def validate_fecha(self, value):
        validate_fecha_not_past(value)
        return value

class MantencionSerializer(serializers.ModelSerializer):
    dias_mantencion = serializers.SerializerMethodField()
    
    class Meta:
        model = Mantencion
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'descripcion', 
                 'responsable', 'dias_mantencion']
        read_only_fields = ['id', 'dias_mantencion']

    def get_dias_mantencion(self, obj):
        if obj.fecha_fin and obj.fecha_inicio:
            return (obj.fecha_fin - obj.fecha_inicio).days
        return 0

    def validate(self, data):
        # Validación de fechas
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio:
            validate_fecha_not_past(fecha_inicio)
        if fecha_fin:
            validate_fecha_not_past(fecha_fin)
            
        if fecha_inicio and fecha_fin:
            validate_fecha_range(fecha_inicio, fecha_fin)
            
        return data