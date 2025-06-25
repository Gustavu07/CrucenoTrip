from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROL_CHOICES = [
        ('usuario', 'Usuario'),
        ('guia', 'Guía Turístico'),
        ('admin', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='usuario')
    licencias = models.FileField(upload_to='licencias/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"
