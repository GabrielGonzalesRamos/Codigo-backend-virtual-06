from django.urls import path
from .views import ArchivosController, PlatosController

urlpatterns = [
    path('platos', PlatosController.as_view()),
    path('subirImagen', ArchivosController.as_view())
]