from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from crucenoTrip.models import CarritoItem, Producto, Carrito


class CarritoItemSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = CarritoItem
        fields = ['id', 'producto', 'cantidad']

# ViewSet para CarritoItem
class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = CarritoItem.objects.all()
    serializer_class = CarritoItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CarritoItem.objects.filter(carrito__usuario=self.request.user)

    def perform_create(self, serializer):
        usuario = self.request.user
        producto = serializer.validated_data['producto']

        carrito, created = Carrito.objects.get_or_create(usuario=usuario)

        item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto,
                                                               defaults={'cantidad': serializer.validated_data['cantidad']})

        if not item_created:
            item.cantidad += serializer.validated_data['cantidad']
            item.save()

            raise serializers.ValidationError({'detail': 'Producto ya en el carrito, cantidad actualizada.'})

        else:
            serializer.save(carrito=carrito)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
