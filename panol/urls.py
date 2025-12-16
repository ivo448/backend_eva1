from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views as token_views # Vista para login

# Configuración de Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Pañol INACAP",
      default_version='v1',
      description="Documentación de API para sistema de pañol",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@inacap.cl"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    
    # Endpoint para Login (Obtener Token)
    path('api-token-auth/', token_views.obtain_auth_token, name='api_token_auth'),

    # Endpoints para Documentación
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]