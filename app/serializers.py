from .models import Producto, Proveedor, Noticia, Contacto
from rest_framework import serializers

# Serializers define la representación JSON de los modelos
# Un serializer convierte un queryset o instancia de modelo en datos nativos de Python
# que luego pueden ser renderizados en JSON o XML.

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    nombre_proveedor = serializers.CharField(source='proveedor.nombre', read_only=True)
    proveedor = ProveedorSerializer(read_only=True)
    proveedor_id = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all(), source='proveedor', write_only=True)
    nombre = serializers.CharField(max_length=100, min_length=3, required=True)

    def validate(self, attrs):
        existe = Producto.objects.filter(nombre__iexact=attrs.get('nombre')).exists()
        if existe:
            raise serializers.ValidationError("Ya existe un producto con este nombre.")
        return super().validate(attrs)
    class Meta:
        model = Producto
        fields = '__all__'
    #     extra_kwargs = {
    #         'imagen': {'required': False}  # Hacer el campo imagen opcional
    #     }
    
    # def validate_nombre(self, value):
    #     if Producto.objects.filter(nombre__iexact=value).exists():
    #         raise serializers.ValidationError("Ya existe un producto con este nombre.")
    #     return value