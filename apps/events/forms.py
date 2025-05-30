from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, TicketType
from apps.core.models import Category

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Récupérer la catégorie sport
        try:
            sport_category = Category.objects.get(name='Sport')
            self.fields['categories'].initial = [sport_category.id]
        except Category.DoesNotExist:
            pass

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'categories', 
                 'total_tickets', 'price', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'total_tickets': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.isinstance and self.instance.pk:
            total_capacity = sum(type.quantity_available for type in self.instance.ticket_types.all())
            total_tickets = cleaned_data.get('total_tickets')
            if total_tickets and total_capacity < total_tickets:
                raise ValidationError({
                'total_tickets': "La somme des billets disponibles dépasse la capacité totale"
            })
        return cleaned_data

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise ValidationError("La date de l'événement ne peut pas être dans le passé")
        return date

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise ValidationError("Le prix ne peut pas être négatif")
        return price

    def clean_total_tickets(self):
        total_tickets = self.cleaned_data.get('total_tickets')
        if total_tickets and total_tickets <= 0:
            raise ValidationError("Le nombre de billets doit être supérieur à 0")
        return total_tickets

TicketTypeFormSet = forms.models.inlineformset_factory(
    Event, 
    TicketType,
    fields=['name', 'price', 'quantity_available'],
    extra=1,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'quantity_available': forms.NumberInput(attrs={'class': 'form-control'}),
    },
    validate_min=1,  # Au moins un type de billet requis
)