from django.db import models
from django.contrib.auth.models import User
from .producto import Producto

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carritos')
    productos = models.ManyToManyField(Producto, through='CarritoItem')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
