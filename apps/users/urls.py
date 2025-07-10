from django.urls import path, include
from . import views
from .views import RegisterClientView, RegisterOrganisateurView, RegisterAdminView, UserProfileView, UserDetailView, ChangePasswordView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.logoutview, name='logout'),
    path('profile/', views.UserViewSet.as_view({'get': 'profile'}), name='profile'),
    path('', include(router.urls)),
    
    path('register/client/', RegisterClientView.as_view(), name='register-client'),
    path('register/organisateur/', RegisterOrganisateurView.as_view(), name='register-organisateur'),
    path('register/admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('profil/', UserProfileView.as_view(), name='user-profile'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),    
]