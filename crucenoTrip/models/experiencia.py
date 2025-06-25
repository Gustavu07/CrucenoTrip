from django.db import models
from django.contrib.auth.models import User
from .categoria_experiencia import CategoriaExperiencia

class Experiencia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_por_persona = models.DecimalField(max_digits=8, decimal_places=2)
    guia = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias')
    categorias = models.ManyToManyField(CategoriaExperiencia, related_name='experiencias')
    ubicacion = models.CharField(max_length=255)
    duracion = models.CharField(max_length=50)
    idiomas = models.CharField(max_length=100)
    imagen_experiencia = models.ImageField(upload_to='experiencias/')
    validada = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
