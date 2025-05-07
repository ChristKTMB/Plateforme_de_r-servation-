from django.db import models

from django.db import models
from apps.users.models import User
from apps.events.models import Event, TicketType
from apps.core.models import TimeStampedModel

class Reservation(TimeStampedModel):
    """Réservation utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    is_confirmed = models.BooleanField(default=False)
    reference = models.CharField(max_length=12, unique=True)  # Ex: RES-ABC123

    def __str__(self):
        return f"Réservation {self.reference}"

class ReservationItem(models.Model):
    """Détails des billets réservés"""
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.ticket_type.name}"
