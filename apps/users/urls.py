from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

# users/urls.py
# from django.urls import path
# from .views import RegisterView, LoginView, LogoutView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='api-register'),
#     path('login/', LoginView.as_view(), name='api-login'),
#     path('logout/', LogoutView.as_view(), name='api-logout'),
# ] 
