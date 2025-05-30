from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

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
    
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = "RES-" + get_random_string(6).upper()
        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())
    
    def confirm(self):
        for item in self.items.all():
            ticket_type = item.ticket_type
            if item.quantity > ticket_type.quantity_available:
                raise ValidationError(
                    f"Plus assez de billets disponibles pour {ticket_type.name}"
                )
            ticket_type.quantity_available -= item.quantity
            ticket_type.save()
        self.is_confirmed = True
        self.save()

class ReservationItem(models.Model):
    """Détails des billets réservés"""
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.ticket_type.name}"

    def clean(self):
        if not self.ticket_type:
            raise ValidationError({
                'ticket_type': _("Le type de billet est requis.")
            })
        
        if not self.quantity:
            raise ValidationError({
                'quantity': _("La quantité est requise.")
            })

        if self.ticket_type and self.quantity:
            if self.quantity > self.ticket_type.quantity_available:
                raise ValidationError({
                    'quantity': _(
                        f"Il ne reste que {self.ticket_type.quantity_available} "
                        f"billets disponibles pour {self.ticket_type.name}"
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.ticket_type.price * self.quantity if self.ticket_type and self.quantity else 0
