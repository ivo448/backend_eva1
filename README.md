>> Instalación

Clonar el repositorio:
   git clone https://github.com/tu_usuario/backend-eva1.git
   cd backend-eva1
   
Crear entorno virtual:
  python -m venv venv
  venv\Scripts\activate
  
  Instalar dependencias:
    pip install -r requirements.txt
    
  Aplicar migraciones:
    python manage.py migrate
      
  Crear superusuario (admin):
    python manage.py createsuperuser
    
  Recolectar archivos estáticos:
    python manage.py collectstatic --noinput

>> Ejecución en local

Inicia el servidor de desarrollo con:
  python manage.py runserver
  
  Accede en tu navegador a:
    http://127.0.0.1:8000/

>> Despliegue en PythonAnywhere

Subir el proyecto al servidor (repositorio Git o ZIP).

Configurar WSGI file apuntando a backend-eva1.wsgi.py.

Ejecutar migraciones en la consola de PythonAnywhere:
  python manage.py migrate
  python manage.py collectstatic --noinput
  Configurar la ruta /static/ en Static Files de PythonAnywhere.
