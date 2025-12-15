from django.contrib import admin
from django.urls import path, include  # <--- Asegúrate de importar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta línea conecta el proyecto principal con tu app de inventario
    path('api/', include('app.urls')), 
]