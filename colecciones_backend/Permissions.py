from rest_framework import permissions
from django.http import Http404
from django.core import exceptions


class BasePermissions(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def get_required_object_permissions(self, method, model_cls):
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        perms = self.get_required_object_permissions(request.method, model_cls)

        if not user.has_perms(perms):
            return False

        return True

    def has_permission_model(self, request, model_cls):

        perms = self.get_required_object_permissions(
            request.method, model_cls)
        user = request.user
        if not user.has_perms(perms):
            return False
        return True
