from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from crucenoTrip.models import Carrito, Producto, CarritoItem

class CarritoItemSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField(read_only=True)  # Muestra nombre o __str__
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', write_only=True)
    cantidad = serializers.IntegerField(default=1)

    class Meta:
        model = CarritoItem
        fields = ['producto', 'producto_id', 'cantidad']

class CarritoSerializer(serializers.ModelSerializer):
    productos = CarritoItemSerializer(source='items', many=True)

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'productos']
        read_only_fields = ['usuario']

    def create(self, validated_data):
        productos_data = validated_data.pop('items', [])
        carrito = Carrito.objects.create(**validated_data)
        for item_data in productos_data:
            CarritoItem.objects.create(carrito=carrito, **item_data)
        return carrito

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('items', [])

        instance.items.all().delete()

        for item_data in productos_data:
            CarritoItem.objects.create(carrito=instance, **item_data)

        instance.save()
        return instance

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Carrito.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
