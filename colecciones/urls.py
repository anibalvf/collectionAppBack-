from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

router = DefaultRouter()
router.register(r'colecciones', views.ColeccionViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'tipos', views.TipoViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'fotos', views.ProductoFotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
