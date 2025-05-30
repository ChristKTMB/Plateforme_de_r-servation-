from rest_framework import serializers
from .models import Reservation, ReservationItem

class ReservationItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = ReservationItem
        fields = ['id', 'ticket_type', 'quantity', 'total_price']

class ReservationSerializer(serializers.ModelSerializer):
    items = ReservationItemSerializer(many=True)
    total_amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = Reservation
        fields = ['id', 'reference', 'event', 'is_confirmed', 'items', 'total_amount']
        read_only_fields = ['reference', 'is_confirmed']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        reservation = Reservation.objects.create(**validated_data)
        
        for item_data in items_data:
            ReservationItem.objects.create(
                reservation=reservation,
                **item_data
            )
        return reservation
