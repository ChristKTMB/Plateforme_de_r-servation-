from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.logoutview, name='logout'),

    path('profile/', views.UserViewSet.as_view({'get': 'profile'}), name='profile'),

    path('', include(router.urls))
]