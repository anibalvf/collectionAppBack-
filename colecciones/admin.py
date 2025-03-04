from django.contrib import admin
from .models import Coleccion, Tipo, Categoria, Producto

admin.site.register(Coleccion)
admin.site.register(Tipo)
admin.site.register(Categoria)
admin.site.register(Producto)
