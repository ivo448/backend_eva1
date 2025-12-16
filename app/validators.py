from rest_framework import serializers
from django.utils import timezone
from datetime import date, datetime

def validar_fecha_futura(value):
    """
    Valida que la fecha (o fecha y hora) no sea anterior al momento actual.
    Se usa para agendar Reservas o Mantenciones.
    """
    ahora = timezone.now()

    # Si el valor es datetime (Fecha y Hora)
    if isinstance(value, datetime):
        if value < ahora:
            raise serializers.ValidationError("La fecha y hora no pueden estar en el pasado.")
    
    # Si el valor es date (Solo Fecha)
    elif isinstance(value, date):
        if value < ahora.date():
            raise serializers.ValidationError("La fecha no puede ser anterior a hoy.")
    
    return value

def validar_descripcion_detallada(value):
    """
    Asegura que una descripcion tenga al menos 10 caracteres.
    Util para Requerimientos o Mantenciones.
    """
    if len(value.strip()) < 10:
        raise serializers.ValidationError("La descripción es muy corta. Debe tener al menos 10 caracteres.")
    return value