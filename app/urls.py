from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    EquipoViewSet, 
    CategoriaViewSet, 
    ReservaViewSet, 
    MantencionViewSet, 
    RequerimientoViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'equipos', EquipoViewSet, basename='equipo')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'mantenciones', MantencionViewSet, basename='mantencion')
router.register(r'requerimientos', RequerimientoViewSet, basename='requerimiento')

urlpatterns = [
    path('', include(router.urls)),
]