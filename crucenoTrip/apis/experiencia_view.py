from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from crucenoTrip.models import Experiencia, CategoriaExperiencia

class ExperienciaSerializer(serializers.ModelSerializer):
    categorias_ids = serializers.PrimaryKeyRelatedField(
        queryset=CategoriaExperiencia.objects.all(),
        source='categorias',
        many=True,
        write_only=True
    )
    categorias = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Experiencia
        fields = [
            'id', 'titulo', 'descripcion', 'precio_por_persona', 'guia',
            'categorias', 'categorias_ids', 'ubicacion', 'duracion', 'idiomas',
            'imagen_experiencia', 'validada'
        ]
        read_only_fields = ['guia', 'validada']

# ViewSet para Experiencia
class ExperienciaViewSet(viewsets.ModelViewSet):
    queryset = Experiencia.objects.all()
    serializer_class = ExperienciaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(guia=self.request.user)

    def update(self, request, *args, **kwargs):
        experiencia = self.get_object()
        if experiencia.guia != request.user and not request.user.is_staff:
            return Response({'detail': 'No tienes permiso para modificar esta experiencia.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        experiencia = self.get_object()
        if experiencia.guia != request.user and not request.user.is_staff:
            return Response({'detail': 'No tienes permiso para eliminar esta experiencia.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
