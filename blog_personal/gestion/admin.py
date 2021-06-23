from django.contrib import admin
from .models import LibroModel, UsuarioModel, PrestamoModel

class LibroAdmin(admin.ModelAdmin):
    list_display = ['libroNombre', 'libroAutor', 'libroEdicion', 'libroCantidad'] # Para modificar la lista del modelo
    search_fields = ['libroNombre', 'libroEdicion'] # Agregar un buscador al modelo y ademas hay que indicar a que columnas se realizará la busqueda cuando se tenga una 
    list_filter = ['libroAutor'] # Agrega un campo de busqueda rapido (Lista) para realizar una busqueda más generica, se recomienda utilizar campos en los cuales no contengan muchos valores
    readonly_fields = ['libroId'] # Indica si se desea ver algun campo que el usuario no puede manipular 


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'libro']    

admin.site.register(LibroModel, LibroAdmin)
admin.site.register(UsuarioModel)
admin.site.register(PrestamoModel, PrestamoAdmin)
# Register your models here.
