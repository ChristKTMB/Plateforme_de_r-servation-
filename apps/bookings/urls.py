# apps/bookings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuration du routeur pour l'API
router = DefaultRouter()
router.register(r'api/reservations', views.ReservationViewSet, basename='api-reservation')
router.register(r'api/items', views.ReservationItemViewSet, basename='api-reservation-item')

app_name = 'bookings'

# URLs finales
urlpatterns = [
    # Routes pour les templates
    path('', views.ReservationListView.as_view(), name='reservation_list'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('create/<int:event_id>/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('<int:pk>/confirm/', views.ReservationConfirmView.as_view(), name='reservation_confirm'),
    
    # Routes pour l'API
    path('', include(router.urls)),
]
