from django.db import models
from django.contrib.auth.models import User

class CarritoReserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrito_reserva')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
