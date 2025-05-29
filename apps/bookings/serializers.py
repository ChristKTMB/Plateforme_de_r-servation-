from rest_framework import serializers
from django.utils import timezone
from apps.bookings.models import Reservation, ReservationItem
from apps.events.models import TicketType

class ReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationItem
        fields = ['ticket_type', 'quantity']

class ReservationSerializer(serializers.ModelSerializer):
    items = ReservationItemSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'event', 'is_confirmed', 'reference', 'items']
        read_only_fields = ['reference', 'is_confirmed']

    def validate(self, data):
        event = data['event']
        items_data = data.get('items', [])

        # Vérification de l'événement
        if not event.is_published:
            raise serializers.ValidationError("L'événement n'est pas encore publié.")
        if event.date < timezone.now():
            raise serializers.ValidationError("L'événement est déjà passé.")

        for item in items_data:
            ticket_type = item['ticket_type']
            quantity = item['quantity']

            # Vérifie si le billet appartient à cet événement
            if ticket_type.event != event:
                raise serializers.ValidationError(f"Le type de billet {ticket_type.name} ne correspond pas à l'événement.")

            # Vérifie la quantité demandée
            if quantity > ticket_type.quantity_available:
                raise serializers.ValidationError(
                    f"Plus assez de billets disponibles pour {ticket_type.name} (restant : {ticket_type.quantity_available})."
                )
            if quantity <= 0:
                raise serializers.ValidationError("La quantité doit être strictement positive.")

        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        reservation = Reservation.objects.create(**validated_data)

        # Création des ReservationItems + mise à jour du stock
        for item_data in items_data:
            ticket_type = item_data['ticket_type']
            quantity = item_data['quantity']

            # Mise à jour de la quantité disponible
            if ticket_type.quantity_available >= quantity:
                ticket_type.quantity_available -= quantity
                ticket_type.save()
            else:
                raise serializers.ValidationError(
                    f"Billets {ticket_type.name} épuisés pendant la réservation. Veuillez réessayer."
                )

            # Enregistre l'item
            ReservationItem.objects.create(reservation=reservation, **item_data)

        return reservation
