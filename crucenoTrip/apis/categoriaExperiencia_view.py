from rest_framework import viewsets,serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from crucenoTrip.models import CategoriaExperiencia


class CategoriaExperienciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaExperiencia
        fields = ['id', 'nombre']

class CategoriaExperienciaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaExperiencia.objects.all()
    serializer_class = CategoriaExperienciaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Solo los administradores pueden crear categorías.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Solo los administradores pueden modificar categorías.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Solo los administradores pueden eliminar categorías.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
