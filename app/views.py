from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Proveedor, Noticia
from .forms import ContactoForm, ProductoForm, RegistroUsuarioForm, ProveedorForm, TrabajadorForm
from django.contrib.auth.models import User, Group # Para el registro de usuarios
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import login, authenticate # Para autenticar y loguear usuarios
from django.contrib.auth.decorators import login_required, permission_required # Para proteger vistas
from rest_framework import viewsets
from .serializers import ProductoSerializer, ProveedorSerializer

# Create your views here.
# Aca se definen las paginas que se van a utilizar en la aplicación
# cada función representa una vista que se va a renderizar en la aplicación

# Para filtrar los productos por el nombre, se debe escribir el nombre en la URL, por ejemplo: /productos/?nombre=cerveza

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def get_queryset(self):
        proveedores = Proveedor.objects.all()

        nombre = self.request.GET.get('nombre')
        if nombre:
            proveedores = proveedores.filter(nombre__icontains=nombre)
        return proveedores

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        productos = Producto.objects.all()

        nombre = self.request.GET.get('nombre') 
        #El primer nombre es el que viene en la URL, el segundo es el nombre del campo en el modelo
        #El primer get es el metodo de django para obtener datos por get y el segundo es el metodo de python para obtener datos de un diccionario
        if nombre:
            productos = productos.filter(nombre__icontains=nombre) #El icontains es para que no sea exacto y no importe mayusculas o minusculas
        return productos

    # def perform_create(self, serializer):
    #     serializer.save()

    # def perform_update(self, serializer):
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     instance.delete()

#---------------------------------------------------------------------------
# Definición de las vistas

def home(request):
    return render(request, 'app/home.html')

def catalogo(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/catalogo.html', data)

def noticias(request):
    noticias = Noticia.objects.all()  # Asegúrate de tener un modelo Noticia definido
    data = {
        'noticias': noticias
    }
    return render(request, 'app/noticias.html', data)

def contacto(request):
    data = {
        'form': ContactoForm()
    }
    return render(request, 'app/contacto.html', data)

def galeria(request):
    return render(request, 'app/galeria.html')

#---------------------------------------------------------------------------
# PRODUCTOS

@login_required
@permission_required('app.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data = messages.success(request, 'Producto agregado correctamente')
            return redirect('listar_productos')
        else:
            data ["form"] = formulario

    return render(request, 'app/productos/agregar_producto.html', data)

@login_required
@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 10)  # 12 productos por página
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }
    return render(request, 'app/productos/listar_producto.html', data)

@login_required
@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto modificado correctamente')
            return redirect('listar_productos')
        else:
            data["form"] = formulario

    return render(request, 'app/productos/modificar_producto.html', data)

@login_required
@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('listar_productos')

def registro_usuario(request):

    data = {
        'form': RegistroUsuarioForm()
    }

    if request.method == 'POST':
        formulario = RegistroUsuarioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            grupo_clientes = Group.objects.get(name='Cliente')
            user.groups.add(grupo_clientes)
            login(request, user)

            messages.success(request, f'Usuario {user} registrado correctamente')
            return redirect(to='home')
        else:
            data["form"] = formulario
            

    return render(request, 'registration/registro_usuario.html', data)


def product(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'producto': producto
    }
    return render(request, 'app/productos/product.html', data)

def nosotros(request):
    return render(request, 'app/nosotros.html')

#---------------------------------------------------------------------------
# PROVEEDORES

@login_required
@permission_required('app.add_proveedor')
def agregar_proveedor(request):
    data = {
        'form': ProveedorForm()
    }
    if request.method == 'POST':
        formulario = ProveedorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Proveedor agregado correctamente')
            return redirect('listar_proveedores')
        else:
            data["form"] = formulario
    
    return render(request, 'app/proveedores/agregar_proveedor.html', data)

@login_required
@permission_required('app.view_producto')
def listar_proveedores(request):
    proveedor = Proveedor.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(proveedor, 10)  # 10 proveedores por página
        proveedor = paginator.page(page)
    except:
        raise Http404
    data = {
        'entity': proveedor,
        'paginator': paginator
    }
    return render(request, 'app/proveedores/listar_proveedor.html', data)

@login_required
@permission_required('app.change_proveedor')
def modificar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    data = {
        'form': ProveedorForm(instance=proveedor)
    }
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor modificado correctamente')
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'app/proveedores/modificar_proveedor.html', data)

@login_required
@permission_required('app.delete_proveedor')
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado correctamente')
    return redirect('listar_proveedores')

#---------------------------------------------------------------------------
# TRABAJADORES

@login_required
@permission_required('auth.add_user')
def agregar_trabajador(request):
    # Aquí deberías implementar la lógica para agregar un trabajador
    # Por ejemplo, podrías crear un formulario similar a los de Producto y Proveedor
    data = {
        'form': TrabajadorForm()
    }
    if request.method == 'POST':
        formulario = TrabajadorForm(request.POST)
        if formulario.is_valid():
            # Aquí deberías guardar el trabajador en la base de datos
            # Por ejemplo, podrías crear un nuevo usuario y asignarle un grupo de trabajadores
            username = formulario.cleaned_data['user_name']
            first_name = formulario.cleaned_data['first_name']
            last_name = formulario.cleaned_data['last_name']
            email = formulario.cleaned_data['email']
            password = formulario.cleaned_data['password1']

            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            #grupo_trabajadores, created = Group.objects.get_or_create(name='Trabajadores')
            #user.groups.add(grupo_trabajadores)
            user.save()

            messages.success(request, f'Trabajador {user} agregado correctamente')
            return redirect('listar_trabajadores')
        else:
            data["form"] = formulario
    return render(request, 'app/trabajadores/agregar_trabajador.html', data)

@login_required
@permission_required('app.view_user')
def listar_trabajadores(request):
    # Aquí deberías implementar la lógica para listar los trabajadores
    # Por ejemplo, podrías usar un modelo Trabajador y un template similar a los de Producto y Proveedor
    return render(request, 'app/trabajadores/listar_trabajador.html')


@login_required
def perfil_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfil')
    else:
        form = RegistroUsuarioForm(instance=request.user)

    data = {
        'form': form
    }
    return render(request, 'app/perfil/perfil_usuario.html', data)

@login_required
def editar_perfil(request):
    return render(request, 'app/perfil/editar_perfil.html')