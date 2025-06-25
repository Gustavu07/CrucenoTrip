from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from crucenoTrip.models import CarritoReserva

class CarritoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoReserva
        fields = ['id', 'usuario']
        read_only_fields = ['usuario']

class CarritoReservaViewSet(viewsets.ModelViewSet):
    queryset = CarritoReserva.objects.all()
    serializer_class = CarritoReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CarritoReserva.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        if CarritoReserva.objects.filter(usuario=self.request.user).exists():
            raise serializers.ValidationError("Ya tienes un carrito de reserva.")
        serializer.save(usuario=self.request.user)
