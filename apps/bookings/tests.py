from django.test import TestCase

from django.utils import timezone
from decimal import Decimal

from apps.users.models import User
from apps.events.models import Event, TicketType
from .models import Reservation, ReservationItem

class ReservationModelTest(TestCase):
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            user_type="C"
        )

        # Créer un organisateur
        self.organizer = User.objects.create(
            username="organizer",
            email="organizer@example.com",
            user_type="O"
        )

        # Créer un événement
        self.event = Event.objects.create(
            title="Concert Test",
            description="Description test",
            date=timezone.now(),
            location="Lieu test",
            organizer=self.organizer,
            total_tickets=100,
            price=Decimal('50.00'),
            is_published=True
        )

        # Créer un type de billet
        self.ticket_type = TicketType.objects.create(
            event=self.event,
            name="VIP",
            price=Decimal('100.00'),
            quantity_available=50
        )

        # Créer une réservation
        self.reservation = Reservation.objects.create(
            user=self.user,
            event=self.event,
            is_confirmed=False,
            reference="RES-TEST123"
        )

    def test_reservation_creation(self):
        """Test la création d'une réservation"""
        self.assertEqual(self.reservation.user, self.user)
        self.assertEqual(self.reservation.event, self.event)
        self.assertFalse(self.reservation.is_confirmed)
        self.assertEqual(self.reservation.reference, "RES-TEST123")
        self.assertEqual(str(self.reservation), "Réservation RES-TEST123")

    def test_reservation_item_creation(self):
        """Test la création d'un item de réservation"""
        reservation_item = ReservationItem.objects.create(
            reservation=self.reservation,
            ticket_type=self.ticket_type,
            quantity=2
        )

        self.assertEqual(reservation_item.reservation, self.reservation)
        self.assertEqual(reservation_item.ticket_type, self.ticket_type)
        self.assertEqual(reservation_item.quantity, 2)
        self.assertEqual(str(reservation_item), "2x VIP")

    def test_reservation_items_relationship(self):
        """Test la relation entre réservation et items"""
        ReservationItem.objects.create(
            reservation=self.reservation,
            ticket_type=self.ticket_type,
            quantity=2
        )

        self.assertEqual(self.reservation.items.count(), 1)
        self.assertEqual(self.reservation.items.first().quantity, 2)

    def test_unique_reference(self):
        """Test l'unicité de la référence"""
        with self.assertRaises(Exception):
            Reservation.objects.create(
                user=self.user,
                event=self.event,
                reference="RES-TEST123"  # Même référence que self.reservation
            )
