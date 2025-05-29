from rest_framework import serializers
from .models import Event, TicketType
from apps.users.serializers import UserSerializer

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'name', 'price', 'quantity_available']

class EventSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'location',
            'categories', 'organizer', 'total_tickets', 'price',
            'image', 'is_published', 'ticket_types'
        ]
        read_only_foelds = ['organizer']

