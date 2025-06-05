from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import action

from .serializers import UserSerializer, LoginSerializer
from .forms import UserRegistrationForm, LoginForm
from .models import User

from apps.events.serializer import EventSerializer
from apps.bookings.serializers import ReservationSerializer

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            messages.success(self.request, "Inscription réussie ! Bienvenue.")
            return redirect('home')
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    return redirect('home')
                messages.error(request, 'Identifiants invalides')
            return render(request, self.template_name, {'form': form})

def logoutview(request):
    logout(request)
    return redirect('home')

class UserViewSet(viewsets.ModelViewSet):
    """Vue pour API"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    template_name = 'users/profile.html'  # Default template

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Affiche le profil de l'utilisateur connecté"""
        if not request.user.is_authenticated:
            messages.error(request, "Veuillez vous connecter pour accéder à votre profil.")
            return redirect('login')

        if request.accepted_renderer.format == 'html':
            return Response({
                'user': request.user,
                'reservations': request.user.reservations.all().order_by('-created_at'),
                'events': request.user.events.all().order_by('-date') if request.user.user_type == 'O' else None
            }, template_name='users/profile.html')

        # Pour l'API
        return Response({
            'user': UserSerializer(request.user).data,
            'reservations': ReservationSerializer(request.user.reservations.all().order_by('-created_at'), many=True).data,
            'events': EventSerializer(request.user.events.all().order_by('-date'), many=True).data if request.user.user_type == 'O' else []
        })

    def create(self, request, *args, **kwargs):
        """Gestion de l'inscription"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'data': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post', 'get'])
    def login(self, request):
        """Gestion de la connexion"""
        if request.method == 'GET':
            return Response(self.get_renderer_context())
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response({
                    'status': 'success',
                    'data': UserSerializer(user).data,
                    'message': 'Connexion réussi'
                })
            return Response(
                {'error': 'Identifiants invalides'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout()
        return Response({
            'status': 'success',
            'message': 'Deconnexion réussie'
        })
    
    def def_permissions(self):
        """Gestion des persmissions"""
        if self.action in ['create', 'login', 'logout']:
            return [AllowAny()]
        return super().get_permissions()

    def get_template_names(self):
        """Return template names based on the action"""
        if self.action == 'profile':
            return ['users/profile.html']
        elif self.action == 'login':
            return ['users/login.html']
        return super().get_template_names()