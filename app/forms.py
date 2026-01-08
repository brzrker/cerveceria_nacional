#para crear un formulario para los modelos
from django import forms
from .models import Contacto, TipoSolicitud, Producto, Proveedor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator
from django.forms import ValidationError


class ContactoForm(forms.ModelForm):

    nombre = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Juan Topo", "id": "card-body"}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control border border-dark", "placeholder": "juan.topo@gmail.com", "id": "card-body"}))
    tipo_solicitud = forms.ModelChoiceField(queryset=TipoSolicitud.objects.all(), widget=forms.Select(attrs={"class": "form-control border border-dark", "id": "card-body"}),empty_label="Seleccione una opción")
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control border border-dark", "placeholder": "Escribe tu mensaje aquí", "id": "card-body"}))
    avisos = forms.BooleanField(required=False, initial=False, label="Deseo recibir avisos y novedades", widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    

    class Meta:
        model = Contacto
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre del producto", "id": "card-body"}))
    sabor = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Descripción del producto", "id": "card-body"}))
    para = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Para quién es el producto", "id": "card-body"}))
    precio = forms.DecimalField(widget=forms.NumberInput(attrs={"class": "form-control border border-dark", "placeholder": "Precio del producto", "id": "card-body"}))
    volumen_litros = forms.DecimalField(widget=forms.NumberInput(attrs={"class": "form-control border border-dark", "placeholder": "Volumen en litros", "id": "card-body"}))
    tipo_cerveza = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Tipo de cerveza", "id": "card-body"}))
    imagen = forms.ImageField(required=False, validators=[MaxSizeFileValidator(max_file_size=2)], widget=forms.FileInput(attrs={"class": "form-control-file", "id": "card-body"}))
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=forms.Select(attrs={"class": "form-control border border-dark", "id": "card-body"}), empty_label="Seleccione un proveedor")
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control border border-dark", "placeholder": "Cantidad", "id": "card-body"}))
    fecha_elaboracion = forms.DateField(
    widget=forms.DateInput(attrs={
        "class": "form-control border border-dark",
        "placeholder": "Fecha de elaboración",
        "type": "date",  # Este es el truco: HTML5 calendar picker
        "id": "card-body"
    })
)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()
        if existe:
            raise ValidationError("Ya existe un producto con este nombre.")
        return nombre    

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'fecha_elaboracion': forms.SelectDateWidget()
        }

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre de usuario", "id": "card-body"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre", "id": "card-body"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Apellido", "id": "card-body"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control border border-dark", "placeholder": "Correo electrónico", "id": "card-body"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control border border-dark", "placeholder": "Contraseña", "id": "card-body"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control border border-dark", "placeholder": "Confirma tu contraseña", "id": "card-body"}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class NoticiaForm(forms.ModelForm):
    # titulo = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Título de la noticia", "id": "card-body"}))
    # contenido = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control border border-dark", "placeholder": "Contenido de la noticia", "id": "card-body"}))
    # fecha_publicacion = forms.DateField(
    #     widget=forms.DateInput(attrs={
    #         "class": "form-control border border-dark",
    #         "placeholder": "Fecha de publicación",
    #         "type": "date",  # HTML5 calendar picker
    #         "id": "card-body"
    #     })
    # )

    class Meta:
        #model = Noticia
        fields = '__all__'

class ProveedorForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre del proveedor", "id": "card-body"}))
    rut = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "RUT del proveedor", "id": "card-body"}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control border border-dark", "placeholder": "Correo electrónico del proveedor", "id": "card-body"}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Dirección del proveedor", "id": "card-body"}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Teléfono del proveedor", "id": "card-body"}))
    
    class Meta:
        model = Proveedor
        fields = '__all__'

class TrabajadorForm(forms.ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre de usuario", "id": "card-body"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre", "id": "card-body"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Apellido", "id": "card-body"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control border border-dark", "placeholder": "Correo electrónico", "id": "card-body"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control border border-dark", "placeholder": "Contraseña", "id": "card-body"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control border border-dark", "placeholder": "Confirma tu contraseña", "id": "card-body"}))
    #group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select(attrs={"class": "form-control border border-dark", "id": "card-body"}), empty_label="Seleccione un grupo")
    fecha_contratacion = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control border border-dark",
            "placeholder": "Fecha de contratación",
            "type": "date",  # HTML5 calendar picker
            "id": "card-body"
        })
    )

    class Meta:
        model = User
        fields = ['user_name', 'first_name', 'last_name', 'email', 'password1', 'password2', 'fecha_contratacion']
        #fields = '__all__'  # Si tienes más campos en el modelo Trabajador, puedes usar esto

class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Nombre", "id": "card-body"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border border-dark", "placeholder": "Apellido", "id": "card-body"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control border border-dark", "placeholder": "Correo electrónico", "id": "card-body"}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']