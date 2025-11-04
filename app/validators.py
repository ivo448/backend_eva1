from django.core.exceptions import ValidationError
import datetime

def validate_nombre_min_length(value, min_len=3):
    if not value or len(value.strip()) < min_len:
        raise ValidationError(f'El nombre debe tener al menos {min_len} caracteres.')

def validate_non_negative(value):
    if value is None:
        return
    try:
        if value < 0:
            raise ValidationError('El valor no puede ser negativo.')
    except TypeError:
        raise ValidationError('Valor inválido.')

def validate_image_size(image, max_mb=2):
    if not image:
        return
    max_bytes = max_mb * 1024 * 1024
    if hasattr(image, 'size') and image.size > max_bytes:
        raise ValidationError(f'La imagen no puede superar {max_mb} MB.')
    content_type = getattr(image, 'content_type', '')
    if content_type and not content_type.startswith('image/'):
        raise ValidationError('El archivo subido no es una imagen.')

def validate_fecha_not_past(fecha):
    if fecha and fecha < datetime.date.today():
        raise ValidationError('La fecha no puede ser anterior a hoy.')

def validate_fecha_range(fecha_inicio, fecha_fin):
    if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
        raise ValidationError('La fecha de fin debe ser igual o posterior a la fecha de inicio.')

def validate_descripcion_min_length(value, min_len=5):
    if not value or len(value.strip()) < min_len:
        raise ValidationError(f'La descripción debe tener al menos {min_len} caracteres.')