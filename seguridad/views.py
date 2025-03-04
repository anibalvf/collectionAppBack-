from django.contrib.auth.models import User, Group, Permission
from rest_framework import viewsets

from seguridad.serializers import UserSerializer, GroupSerializer, ReadUserSerializer, UserDetalleSerializer
from django.conf import settings
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
from colecciones_backend.Permissions import BasePermissions
from seguridad.models import User_Detalle
from django.db.models import Q
from colecciones_backend.CustomError import CustomError
from django.utils.translation import gettext_lazy as _
from seguridad.util import ofuscarDatosUsuario,es_admin
from seguridad.models import Usuarios
from django.contrib.auth.hashers import check_password
import json
from oauth2_provider.views.base import TokenView
from oauth2_provider.models import AccessToken
from django.http import JsonResponse, HttpResponse

from seguridad.util import registra_session,finaliza_session
from rest_framework.renderers import JSONRenderer
class UserDetalleViewSet(viewsets.ModelViewSet):
    """
    Endpoint que permite editar y visualizar los usuarios
    """
    queryset = User_Detalle.objects.all()
    serializer_class = UserDetalleSerializer
    permission_classes = (BasePermissions,)
    

class PermisosViewSet (viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = UserSerializer
    
    def list(self, *args, **kwargs):
        permissions = self.request.user.get_all_permissions()

        # Se muestran los grupos como parte de los permisos
        usuario = self.request.user
        lista_grupos = usuario.groups.all()
        for grupo in lista_grupos:
            permissions.add(grupo.name)

        return Response(permissions)


class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoint que permite editar y visualizar los usuarios
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (BasePermissions,)

    def list(self, request, *args, **kwargs):
        #queryset = Usuarios.objects.all().prefetch_related("groups").order_by("username")
        if es_admin(request):
            queryset = Usuarios.objects.all().prefetch_related("groups").order_by("username")
        else :
            queryset = Usuarios.objects.filter( detalle__empresas__in=request.user.detalle.empresas.all()).prefetch_related("groups").order_by("username")
                 
        
        serializer = ReadUserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False,
            url_path='detalle', url_name='detalle')
    def getDetalle(self, request):
        usuario = request.user
        try:
            serializer = UserDetalleSerializer(
                User_Detalle.objects.get(usuario=usuario.id), many=False)
            return Response(serializer.data)
        except:
            userdetalle = User_Detalle(usuario=usuario, avatar=None)
            serializer = UserDetalleSerializer(userdetalle)
            return Response(serializer.data)
        

    @action(methods=['post'], detail=False, url_path='comprobar_password', url_name='comprobar_password')
    def comprobar_password(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"detail": "Se requieren 'username' y 'password'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return Response({"detail": "Contraseña correcta."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Contraseña incorrecta."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path='gpdrbaja', url_name='gpdrbaja')
    def getGDPR(self, request, pk):

        if ofuscarDatosUsuario():
            return Response(status=status.HTTP_200_OK)
        else:
            raise CustomError(_("No se pueden eliminar los datos del cliente al tener una reserva activa"), _(
                "Cliente"), status_code=status.HTTP_409_CONFLICT)

    def create(self, request):
        # # comprueba que no puedan darse de alta mas usuarios que los contratados
        numero_usuarios = settings.MAX_NUM_USERS
        totalactual = User.objects.all().count()

        if totalactual >= numero_usuarios:
            return HttpResponseForbidden()
        # llama al servicio para crear el usuario
        return super().create(request)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()

        try:
            User_Detalle.objects.get(usuario=usuario.id).delete()
        except:
            pass

        return super().destroy(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    """
    Endpoint que permite editar y visualizar los grupos
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (BasePermissions,)

class CustomTokenView(TokenView):
    def get_allowed_grant_types(self):
        return ['password']  # Esto es importante

class CustomRevokeTokenView(TokenView):

    def post(self, request, *args, **kwargs):
        token = request.POST.get('token')
        if token:
            finaliza_session(token)

        return HttpResponse(status=200)
