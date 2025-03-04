from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from seguridad.models import User_Detalle
from drf_base64.serializers import ModelSerializer
from colecciones_backend.Permissions import BasePermissions
import os
from django.conf import settings
from seguridad.models import Usuarios
from django.contrib.auth.hashers import make_password

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)
        read_only_fields = ('name',)
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


class ListaUserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    def get_id(self, obj):
        return obj.id

    class Meta:
        model = User
        fields = ('id', 'text')


class ReadUserSerializer(serializers.ModelSerializer):
    perfil = serializers.SerializerMethodField()
    texto = serializers.SerializerMethodField()
    
    def get_perfil(self, obj):
        perfiles = ""
        
        try:
            lista_perfiles = obj.groups.all().order_by('name')
            for perfil in lista_perfiles:
                if perfiles != "":
                    perfiles += ", "
                perfiles += perfil.name
            
            return perfiles
            
        except:
            return perfiles

    def get_texto(self, obj):
        if not obj.is_active:
            return '{} {} (Inactivo)'.format(obj.first_name, obj.last_name)
        return '{} {}'.format(obj.first_name, obj.last_name)
        

    class Meta:
        model = Usuarios
        fields = ('id', 'username',  'email', 'first_name', 'perfil',
                  'last_name',  'is_active', 'texto')



class UserDetalleSerializer(ModelSerializer):
    class Meta:
        model = User_Detalle
        fields = "__all__"
        extra_kwargs = {'usuario': {'required': False}}


class UserSerializer(serializers.ModelSerializer):
    detalle = UserDetalleSerializer(required=False)
    
    def validate_password(self, value):
        from django.contrib.auth.password_validation import validate_password
        validate_password(value)
        return value
    
    class Meta:
        model = User
        fields = ('id', 'username',  'email', 'first_name',
                  'last_name',  'is_active', 'groups', 'password', 'detalle')
        extra_kwargs = {'password': {'required': False}}

    def to_representation(self, obj):
        datos = super().to_representation(obj)
        if not BasePermissions().has_permission_model(self._context.get("request"), User_Detalle):
            datos.pop('detalle')
        return datos

    def create(self, datos):
        grupos_data = None
        detalle_data = None
        if 'groups' in datos:
            grupos_data = datos.pop('groups')
        if 'detalle' in datos:
            detalle_data = datos.pop('detalle')

        usuario_pass = make_password(datos['password'])
        datos['password'] = usuario_pass

        usuario = User.objects.create(**datos)
        if grupos_data:
            for item in grupos_data:
                usuario.groups.add(item)
        if detalle_data:
            empresas_data = detalle_data.pop('empresas')
            detalle = User_Detalle.objects.create(
                usuario=usuario, **detalle_data)
            if empresas_data:
                for item in empresas_data:
                    detalle.empresas.add(item)

        return usuario

    def update(self, usuario, datos):
        usuario.username = datos.get('username', usuario.username)
        usuario.first_name = datos.get('first_name', usuario.first_name)
        usuario.last_name = datos.get('last_name', usuario.last_name)
        if datos.get('password') != None:
            usuario.set_password(datos.get('password'))
        usuario.email = datos.get('email', usuario.email)
        usuario.is_active = datos.get('is_active', usuario.is_active)
        usuario.groups.set(datos.get('groups', usuario.groups))

        if 'detalle' in datos and BasePermissions().has_permission_model(self._context.get("request"), User_Detalle):
            detalle_data = datos.pop('detalle')
            empresas_data = None
            
            try:
                detalle = User_Detalle.objects.get(usuario=usuario.id)
                detalle.delete()
            except:
                pass
            
            try:
                empresas_data = detalle_data.pop("empresas")
            except:
                pass

            if 'usuario' in detalle_data:
                detalle = User_Detalle.objects.create(**detalle_data)
                if empresas_data:
                    for item in empresas_data:
                        detalle.empresas.add(item)
            else:
                detalle = User_Detalle.objects.create(
                    usuario=usuario, **detalle_data)
                if empresas_data:
                    for item in empresas_data:
                        detalle.empresas.add(item)

        usuario.save()
        return usuario
