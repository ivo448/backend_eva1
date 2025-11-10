from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil

# pre_save, post_save, pre_delete, post_delete
@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crea un Perfil automáticamente cuando un User es creado.
    """
    if created:
        Perfil.objects.create(usuario=instance)