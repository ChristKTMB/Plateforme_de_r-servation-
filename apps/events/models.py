from django.db import models
from apps.core.models import TimeStampedModel, Category
from apps.users.models import User

class Event(TimeStampedModel): 
    """Modèle pour les événement"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    total_tickets = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='events/')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d/%m/%Y')}"

class TicketType(TimeStampedModel):
    """Types de billets (VIP, standard...)"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"