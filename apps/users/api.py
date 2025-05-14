# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token  # Optional if you're using DRF Token Auth
from .serializers import UserSerializer, LoginSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        # Optional: If using DRF Token Authentication
        # token, created = Token.objects.get_or_create(user=user)
        # return Response({'token': token.key})

        return Response({'message': 'Connexion réussie.'}, status=status.HTTP_200_OK)
    
    class LogoutView(APIView):
        permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        # Optional: If using DRF Token Authentication
        # request.user.auth_token.delete()

        return Response({'message': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)

