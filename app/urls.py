from django.urls import path, include
from .views import home, catalogo, noticias, contacto, galeria, agregar_producto, nosotros, perfil_usuario, editar_perfil, \
    listar_productos, product, modificar_producto, eliminar_producto, registro_usuario, \
    agregar_proveedor, listar_proveedores, modificar_proveedor, eliminar_proveedor,\
    agregar_trabajador, listar_trabajadores, \
    ProductoViewSet, ProveedorViewSet
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'productos', ProductoViewSet)
routers.register(r'proveedores', ProveedorViewSet)

# Se definen las URLs de la aplicación
# Cada URL se asocia a una vista específica

# El primer home es el nombre de la URL, 
# el segundo es el nombre de la vista y 
# el tercero es el nombre que se le da a la URL para referenciarla en otras partes del código

urlpatterns = [
    path('', home, name='home'), # El path '' y 'home/' llevan a la misma vista
    path('home/', home, name='home'), 
    path('catalogo/', catalogo, name='catalogo'),
    path('noticias/', noticias, name='noticias'),
    path('contacto/', contacto, name='contacto'),
    path('galeria/', galeria, name='galeria'),
    path('nosotros/', nosotros, name='nosotros'),
    path('product/<id>/', product, name='product'),
    path('registro-usuario/', registro_usuario, name='registro'),
    # PERFIL USUARIO
    path('perfil-usuario/', perfil_usuario, name='perfil_usuario'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    # PRODUCTOS
    path('agregar-producto/', agregar_producto, name='agregar_producto'),
    path('listar-productos/', listar_productos, name='listar_productos'),
    path('modificar-producto/<id>/', modificar_producto, name='modificar_producto'),
    path('eliminar-producto/<id>/', eliminar_producto, name='eliminar_producto'),
    # PROVEEDORES
    path('agregar-proveedor/', agregar_proveedor, name='agregar_proveedor'),
    path('listar-proveedores/', listar_proveedores, name='listar_proveedores'),
    path('modificar-proveedor/<id>/', modificar_proveedor, name='modificar_proveedor'),
    path('eliminar-proveedor/<id>/', eliminar_proveedor, name='eliminar_proveedor'),
    # TRABAJADORES
    path('agregar-trabajador/', agregar_trabajador, name='agregar_trabajador'),
    path('listar-trabajadores/', listar_trabajadores, name='listar_trabajadores'),
    # API REST
    path('api/', include(routers.urls)),  # Incluye las URLs del API REST
]
