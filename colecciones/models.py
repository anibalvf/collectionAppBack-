from django.db import models
from django.utils import timezone

class Coleccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"

    def __str__(self):
        return self.nombre

class Tipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE, related_name='productos')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    fecha_incorporacion = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.coleccion.nombre}"

class ProductoFoto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    es_principal = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Foto de producto"
        verbose_name_plural = "Fotos de productos"
        ordering = ['orden']
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
    
    def save(self, *args, **kwargs):
        # Si es una nueva foto y no hay otras fotos para este producto, establecerla como principal
        if not self.pk and not ProductoFoto.objects.filter(producto=self.producto).exists():
            self.es_principal = True
        
        # Si estamos estableciendo esta foto como principal, asegurarse de que las demás no lo sean
        if self.es_principal:
            # Actualizar otras fotos solo si esta foto ya existe en la base de datos
            if self.pk:
                ProductoFoto.objects.filter(producto=self.producto).exclude(pk=self.pk).update(es_principal=False)
        
        super().save(*args, **kwargs)


