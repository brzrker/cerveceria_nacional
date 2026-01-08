from django.db import models

# Create your models here.
# Aquí se definen los modelos de la aplicación
# Un modelo es una representación de una tabla en la base de datos


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    #descripcion = models.TextField()
    para = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField()
    volumen_litros = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_cerveza = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_elaboracion = models.DateField()

    def __str__(self):
        return self.nombre
    
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class TipoSolicitud(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.SET_NULL, null=True)
    mensaje = models.TextField()
    avisos = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
