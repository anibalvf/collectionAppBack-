from rest_framework import serializers
from django.conf import settings
from .models import *


class ColeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coleccion
        fields = '__all__'

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    foto_principal = serializers.SerializerMethodField()
    coleccion_nombre = serializers.CharField(source='coleccion.nombre', read_only=True)
    tipo_nombre = serializers.CharField(source='tipo.nombre', read_only=True, allow_null=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True, allow_null=True)
    
    class Meta:
        model = Producto
        fields = '__all__'
    
    def get_foto_principal(self, obj):
        foto_principal = obj.fotos.filter(es_principal=True).first()
        if foto_principal and foto_principal.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(foto_principal.imagen.url)
            return foto_principal.imagen.url
        return None
        
    def to_representation(self, instance):
        # Asegurarse de que los objetos relacionados estén precargados
        if not hasattr(instance, '_prefetched_objects_cache') or 'coleccion' not in getattr(instance, '_prefetched_objects_cache', {}):
            instance = Producto.objects.select_related('coleccion', 'tipo', 'categoria').get(pk=instance.pk)
        return super().to_representation(instance)

class ProductoFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoFoto
        fields = '__all__'



        
        