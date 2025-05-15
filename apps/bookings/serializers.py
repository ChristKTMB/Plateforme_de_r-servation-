# apps/bookings/serializers.py
from rest_framework import serializers
from .models import Reservation, ReservationItem

class ReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationItem
        fields = ['id', 'ticket_type', 'quantity']

class ReservationSerializer(serializers.ModelSerializer):
    items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'event', 'is_confirmed', 'reference', 'items']
