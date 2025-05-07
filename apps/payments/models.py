from django.db import models

from apps.bookings.models import Reservation
from apps.core.models import TimeStampedModel

class Transaction(TimeStampedModel):
    """Transactions de paiement"""
    STATUS_CHOICES = (
        ('P', 'En attente'),
        ('S', 'Réussi'),
        ('F', 'Échoué'),
        ('R', 'Remboursé'),
    )
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50)  # Mpesa, OrangeMoney
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Paiement {self.transaction_id}"

class Coupon(TimeStampedModel):
    """Codes promotionnels"""
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # 10.00 = 10€
    valid_until = models.DateTimeField()
    max_uses = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Coupon {self.code} (-{self.discount}€)"
