from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import User
from datetime import date

# Importamos tus modelos
from .models import Equipo, Categoria, Reserva, Requerimiento, Mantencion

# Importamos los Serializers
from .serializers import (
    EquipoSerializer, CategoriaSerializer, UserSerializer, 
    ReservaSerializer, RequerimientoSerializer, MantencionSerializer
)

# Importamos el permiso custom SOLO para Reservas (Lógica de Dueño)
from .permissions import IsOwnerOrAdminGroup

class UserViewSet(viewsets.ModelViewSet):
    """
    Controlador de Usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Solo los que tengan permiso 'view_user' (Admins) pueden ver la lista completa
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    # Endpoint especial: /api/users/me/
    # Este es vital para que React sepa qué permisos tiene el usuario logueado
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Gestión de Categorías.
    - GET: Requiere permiso 'app.view_categoria'
    - POST/PUT/DELETE: Requiere permisos 'add', 'change', 'delete'
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class EquipoViewSet(viewsets.ModelViewSet):
    """
    Gestión de Equipos (Inventario).
    """
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    # --- Al crear equipo ---
    def perform_create(self, serializer):
        # 1. Guardamos el equipo nuevo
        instance = serializer.save()

        # Si se crea en mantencion crear mantencion
        if instance.estado == 'MANTENCION':
            Mantencion.objects.create(
                equipo=instance,
                fecha_programada=date.today(), # Se agenda para hoy
                descripcion="Mantención inicial generada automáticamente al crear el equipo.",
                estado='PENDIENTE'
            )

    # --- Al editar equipo ---
    def perform_update(self, serializer):
        # 1. Obtenemos el estado ANTERIOR antes de guardar
        previous_status = self.get_object().estado
        
        # 2. Guardamos los cambios nuevos
        instance = serializer.save()

        # 3. Si cambió a "MANTENCION"
        if instance.estado == 'MANTENCION' and previous_status != 'MANTENCION':
            Mantencion.objects.create(
                equipo=instance,
                fecha_programada=date.today(),
                descripcion="Equipo enviado a mantención desde el inventario.",
                estado='PENDIENTE'
            )

class ReservaViewSet(viewsets.ModelViewSet):
    """
    Gestión de Reservas
    Se usa IsOwnerOrAdminGroup para que el profesor pueda cancelar SU reserva
    sin tener permiso de 'borrar todas las reservas'
    """
    queryset = Reserva.objects.all().order_by('-fecha_inicio')
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminGroup]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si soy Admin/Pañolero veo todo
        # Si soy usuario normal, Django solo me devuelve MIS reservas
        can_manage_all = user.has_perm('app.view_reserva') or user.groups.filter(name__in=['admin', 'panolero']).exists()
        
        if not can_manage_all:
            queryset = queryset.filter(usuario=user)
            
        return queryset

    # Al crear, el dueño es el usuario logueado automáticamente
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class MantencionViewSet(viewsets.ModelViewSet):
    queryset = Mantencion.objects.all().order_by('fecha_programada')
    serializer_class = MantencionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def perform_update(self, serializer):
        # 1. Guardamos la actualización de la mantención actual
        instance = serializer.save()

        # 2. Si se marca como FINALIZADA, ejecutamos la lógica automática
        if instance.estado == 'FINALIZADA':
            # A. Liberar el equipo
            equipo = instance.equipo
            equipo.estado = 'DISPONIBLE'
            equipo.save()

            # B. CREAR LA SIGUIENTE MANTENCIÓN (Ciclo)
            # Buscamos si el Frontend nos mandó una fecha futura
            proxima_fecha = self.request.data.get('nueva_fecha_programada')
            
            if proxima_fecha:
                Mantencion.objects.create(
                    equipo=equipo,
                    fecha_programada=proxima_fecha,
                    descripcion=f"Mantención preventiva programada (Continuación de #{instance.id})",
                    estado='PENDIENTE'
                )
        
        # Si se pone EN_PROCESO, bloqueamos el equipo
        elif instance.estado == 'EN_PROCESO':
            instance.equipo.estado = 'MANTENCION'
            instance.equipo.save()

        def perform_create(self, serializer):
            instance = serializer.save()
            # Si se crea directamente como EN_PROCESO, bloqueamos el equipo
            if instance.estado == 'EN_PROCESO':
                instance.equipo.estado = 'MANTENCION'
                instance.equipo.save()

class RequerimientoViewSet(viewsets.ModelViewSet):
    """
    Solicitudes de nuevos equipos.
    """
    queryset = Requerimiento.objects.all().order_by('-fecha_solicitud')
    serializer_class = RequerimientoSerializer
    
    # Aquí usamos DjangoModelPermissions.
    # RECUERDA: Darle permiso 'add_requerimiento' al grupo PROFESOR en el Admin.
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)