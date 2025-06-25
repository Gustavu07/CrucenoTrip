from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from crucenoTrip.models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    experiencia_titulo = serializers.CharField(source='experiencia.titulo', read_only=True)
    usuario = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'carrito', 'experiencia', 'experiencia_titulo', 'fecha_reservada',
            'estado_pago', 'comprobante_pago', 'usuario'
        ]

    def get_usuario(self, obj):
        return obj.carrito.usuario.username

    def validate(self, attrs):
        experiencia = attrs.get('experiencia')
        fecha = attrs.get('fecha_reservada')

        if experiencia and fecha:
            if Reserva.objects.filter(experiencia=experiencia, fecha_reservada=fecha).exists():
                raise serializers.ValidationError("Ya existe una reserva para esa experiencia en esa fecha.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        carrito = validated_data.get('carrito')
        if carrito.usuario != user:
            raise serializers.ValidationError("No puedes agregar reservas a carritos de otros usuarios.")
        return super().create(validated_data)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reserva.objects.filter(carrito__usuario=self.request.user)

    def destroy(self, request, *args, **kwargs):
        reserva = self.get_object()
        if reserva.carrito.usuario != request.user:
            return Response({'detail': 'No puedes eliminar reservas de otro usuario.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
