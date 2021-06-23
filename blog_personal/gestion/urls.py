from django.urls import path
from .views import (LibrosController, LibroController, PrestamosController, busqueda_libros, buscador_edicion, UsuariosController, PrestamoController, UsuarioController)


urlpatterns = [
    path('libros', LibrosController.as_view()),
    path('libros/<int:id>', LibroController.as_view()),
    path('busqueda_libros', busqueda_libros),
    path('busqueda_libros_edicion', buscador_edicion),
    path('usuarios', UsuariosController.as_view()),
    path('prestamos', PrestamosController.as_view()),
    path('prestamos/<int:id>', PrestamoController.as_view()),
    path('usuarios/<int:id>', UsuarioController.as_view())  
]