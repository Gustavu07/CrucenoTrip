from django.urls import path, include
from rest_framework import routers

from crucenoTrip.apis import (
    ProductoViewSet, CarritoViewSet, CarritoItemViewSet, CarritoReservaViewSet,
    ReservaViewSet, ExperienciaViewSet, CategoriaExperienciaViewSet, CategoriaProductoViewSet,UserViewSet, AuthViewSet
)

router = routers.DefaultRouter()

# Tienda
router.register('productos', ProductoViewSet)
router.register('carrito-productos', CarritoItemViewSet)
router.register('carrito', CarritoViewSet)

# Reservas
router.register('carrito-reserva', CarritoReservaViewSet)
router.register('reservas', ReservaViewSet)

# Experiencias
router.register('experiencias', ExperienciaViewSet)
router.register('categorias-experiencia', CategoriaExperienciaViewSet)

router.register('categorias-producto', CategoriaProductoViewSet)

router.register('usuarios', UserViewSet, basename='usuarios')
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
