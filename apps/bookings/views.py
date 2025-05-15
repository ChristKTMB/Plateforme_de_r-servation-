# apps/bookings/views.py
from rest_framework import viewsets
from .models import Reservation, ReservationItem
from .serializers import ReservationSerializer, ReservationItemSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationItemViewSet(viewsets.ModelViewSet):
    queryset = ReservationItem.objects.all()
    serializer_class = ReservationItemSerializer
