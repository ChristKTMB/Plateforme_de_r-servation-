from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

from .forms import UserRegistrationForm, LoginForm
# from .models import UserProfile

# from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .serializers import UserSerializer, LoginSerializer
from .forms import UserRegistrationForm

class RegisterView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = [AllowAny]
    template_name = 'users/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return Response({'form': form})

    def post(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            form = UserRegistrationForm(request.data)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
            return Response({'form': form})
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'users/login.html'

    def get(self, request):
        form = LoginForm()
        return Response({'form': form})

    def post(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    return redirect('home')
                messages.error(request, 'Identifiants invalides')
            return Response({'form': form})

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response({
                    'status': 'success',
                    'data': {'user': UserSerializer(user).data},
                    'message': 'Connexion réussie'
                })
            return Response({'error': 'Identifiants invalides'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            logout(request)
            return redirect('login')
        logout(request)
        return Response({'status': 'success', 'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)