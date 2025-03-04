from django.shortcuts import render
from colecciones_backend.Permissions import BasePermissions
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ColeccionViewSet(viewsets.ModelViewSet):
    
    queryset = Coleccion.objects.all()
    serializer_class = ColeccionSerializer
    permission_classes = (BasePermissions,)

    @action(detail=True, methods=['get'], url_path='productos')
    def productos_por_coleccion(self, request, pk=None):
        productos = Producto.objects.filter(coleccion_id=pk)
        serializer = ProductoSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data) 
    
    
class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
    permission_classes = (BasePermissions,) 
    
    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (BasePermissions,)     
    
    
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = (BasePermissions,)

    @action(detail=True, methods=['get'], url_path='fotos')
    def fotos_por_producto(self, request, pk=None):
        fotos = ProductoFoto.objects.filter(producto_id=pk)
        serializer = ProductoFotoSerializer(fotos, many=True, context={'request': request})
        return Response(serializer.data) 
    
class ProductoFotoViewSet(viewsets.ModelViewSet):
    queryset = ProductoFoto.objects.all()
    serializer_class = ProductoFotoSerializer
    permission_classes = (BasePermissions,)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        data = request.data.copy()

        if 'producto' not in data:
            data['producto'] = instance.producto.id

        if data.get('es_principal') == True:
            ProductoFoto.objects.filter(producto=instance.producto).update(es_principal=False)
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    
    

