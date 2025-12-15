from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Equipo, Categoria, Reserva, Requerimiento, Mantencion
from .serializers import (
    EquipoSerializer, CategoriaSerializer, UserSerializer, 
    ReservaSerializer, RequerimientoSerializer, MantencionSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        usuario = self.request.query_params.get('usuario')
        if usuario:
            queryset = queryset.filter(usuario_id=usuario)
        return queryset

class RequerimientoViewSet(viewsets.ModelViewSet):
    queryset = Requerimiento.objects.all()
    serializer_class = RequerimientoSerializer

class MantencionViewSet(viewsets.ModelViewSet):
    queryset = Mantencion.objects.all().order_by('fecha_programada')
    serializer_class = MantencionSerializer