# apps/bookings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, ReservationItemViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)
router.register(r'reservation-items', ReservationItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
