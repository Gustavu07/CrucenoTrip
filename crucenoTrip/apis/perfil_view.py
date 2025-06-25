from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from crucenoTrip.models import Perfil

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']


class PerfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'user', 'telefono', 'rol', 'licencias']


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        user = request.user
        perfil = getattr(user, 'perfil', None)

        user_data = UserSerializer(user).data
        perfil_data = PerfilSerializer(perfil).data if perfil else {}

        return Response({'user': user_data, 'perfil': perfil_data})

    @action(methods=['get'], detail=False, url_path='all')
    def get_all_users(self, request):
        if not request.user.is_staff:
            return Response({'error': 'No tienes permiso para ver todos los usuarios'}, status=403)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class AuthViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido')
        telefono = request.data.get('telefono')
        rol = request.data.get('rol', 'usuario')

        if not all([username, email, password, nombre, apellido, telefono]):
            return Response({'error': 'Todos los campos son requeridos'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Nombre de usuario ya registrado'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Correo ya registrado'}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido
        )

        Perfil.objects.create(
            user=user,
            telefono=telefono,
            rol=rol,
            licencias=request.FILES.get('licencias') if rol == 'guia' else None
        )

        return Response({'id': user.id, 'email': user.email}, status=201)

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Debes proporcionar email y contraseña'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=401)

        user = authenticate(username=user.username, password=password)

        if not user:
            return Response({'error': 'Credenciales inválidas'}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'nombre': user.first_name,
                'apellido': user.last_name,
                'rol': user.perfil.rol if hasattr(user, 'perfil') else None
            }
        })

    # @action(detail=False, methods=['post'], url_path='crear-perfil')
    # def crear_perfil(self, request):
    #     if not request.user.is_staff:
    #         return Response({'error': 'No autorizado'}, status=403)
    #
    #     user_id = request.data.get('user_id')
    #     telefono = request.data.get('telefono')
    #     rol = request.data.get('rol')
    #
    #     try:
    #         user = User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         return Response({'error': 'Usuario no encontrado'}, status=404)
    #
    #     if hasattr(user, 'perfil'):
    #         return Response({'error': 'El perfil ya existe'}, status=400)
    #
    #     perfil = Perfil.objects.create(user=user, telefono=telefono, rol=rol)
    #     return Response({'perfil_id': perfil.id}, status=201)



