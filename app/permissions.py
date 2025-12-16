from rest_framework import permissions

class IsOwnerOrAdminGroup(permissions.BasePermission):
    """
    Permiso personalizado para control a nivel de objeto.
    
    Reglas:
    1. Si el usuario pertenece a los grupos de gestión ('ADMIN', 'PANOLERO'), 
       tiene permiso total sobre cualquier objeto.
    2. Si es un usuario normal (ej: 'PROFESOR', 'ALUMNO'), 
       solo tiene permiso si el objeto le pertenece (obj.usuario == request.user).
    """
    
    def has_object_permission(self, request, view, obj):
        # 1. Verificación básica de autenticación
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Verificar si es Staff (ADMIN o PANOLERO)
        # Usamos filter().exists() porque es la forma más eficiente de consultar la BD
        is_staff = request.user.groups.filter(name__in=['ADMIN', 'PANOLERO']).exists()
        
        if is_staff:
            return True

        # 3. Verificar si es el Dueño del objeto
        # Asumimos que el modelo (Reserva) tiene un campo llamado 'usuario'
        # que es una ForeignKey al modelo User.
        return obj.usuario == request.user