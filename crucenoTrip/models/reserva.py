from django.db import models
from .carrito_reserva import CarritoReserva
from .experiencia import Experiencia

class Reserva(models.Model):
    carrito = models.ForeignKey(CarritoReserva, on_delete=models.CASCADE, related_name='reservas')
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE)
    fecha_reservada = models.DateField()
    estado_pago = models.CharField(max_length=20, default='pendiente')
    comprobante_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)

    def __str__(self):
        return f"{self.experiencia.titulo} para {self.carrito.usuario.username}"
