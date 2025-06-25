from django.db import models
from .categoria_producto import CategoriaProducto

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre
