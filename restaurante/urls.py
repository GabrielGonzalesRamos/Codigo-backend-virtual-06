#from django.contrib import admin
from django.urls import path, include
# settings => Sirve para acceder a todas las variables definidas en el archivo settings
from django.conf import settings
# static => Sirve para cargar un grupo de rutas estaticas
from django.conf.urls.static import static
# Vista predeterminada que sirve para generar la JWT
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('cms/', include('cms.urls')),
    path('login', TokenObtainPairView.as_view())
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #El metodo static retornará una lista de URL PATTERNS y se pasa dos parámetros
# 1 . La URL (El prefijo) con el cual se accedará a esa ruta
# 2. doucmento_root => El contenido que se renderizará cuando se llame a esa ruta
# Esto sirve para renderizar archivos alojados en el backend
