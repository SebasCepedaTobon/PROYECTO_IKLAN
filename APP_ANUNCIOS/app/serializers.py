from .models import Marca, Producto, Marca
from rest_framework import serializers


class MarcaSerialize(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(read_only=True, source="marca.nombre")
    marca = MarcaSerialize(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all(), source="marca")
    nombre = serializers.CharField(required=True, min_length=3)
    precio = serializers.ImageField(required=False)


  #  def validate_nombre(self, value):
   #     existe = Producto.objects.filter(nombre__iexact=value).exists()

    #    if existe:
     #       raise serializers.ValidationError("Este producto ya existe")
        
      #  return value

    class Meta:
        model = Producto
        fields = '__all__'