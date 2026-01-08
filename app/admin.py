from django.contrib import admin
from .models import Proveedor, Producto, Noticia, Contacto, TipoSolicitud
from .forms import ProductoForm
# Register your models here.
# en este archivo se registran los modelos para que aparezcan en el panel de administración de Django
# Proveedor y Producto son los modelos que hemos creado en app/models.py

# acá se puede personalizar la vista del admin para los modelos
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre',)
    list_per_page = 20

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'proveedor', 'precio', 'cantidad', 'fecha_elaboracion')
    search_fields = ('nombre',)
    list_filter = ('proveedor',)
    list_editable = ('precio', 'cantidad')
    list_per_page = 20
    form = ProductoForm

admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Noticia)
admin.site.register(Contacto)
admin.site.register(TipoSolicitud)