from django.urls import include, re_path

from rest_framework.routers import DefaultRouter
from seguridad import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'permisos', views.PermisosViewSet)
router.register(r'detalle', views.UserDetalleViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
