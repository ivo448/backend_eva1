from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipoViewSet, CategoriaViewSet, UserViewSet, 
    ReservaViewSet, RequerimientoViewSet, MantencionViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'requerimientos', RequerimientoViewSet)
router.register(r'mantenciones', MantencionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]