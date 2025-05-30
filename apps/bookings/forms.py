from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, ReservationItem
from apps.events.models import Event, TicketType

class ReservationForm(forms.ModelForm):
    """Formulaire pour créer une réservation"""
    class Meta:
        model = Reservation
        fields = []

class ReservationItemForm(forms.ModelForm):
    """Formulaire pour les éléments de réservation"""
    ticket_type = forms.ModelChoiceField(
        queryset=TicketType.objects.none(),
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = ReservationItem
        fields = ['ticket_type', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        ticket_type = self.cleaned_data.get('ticket_type')

        if not ticket_type:
            return quantity

        if quantity > ticket_type.quantity_available:
            raise ValidationError(
                f"Il ne reste que {ticket_type.quantity_available} billets disponibles"
            )

        if quantity < 1:
            raise ValidationError("La quantité doit être supérieure à 0")

        return quantity

def get_reservation_item_formset(event=None):
    """Factory function pour créer un formset avec l'événement"""
    class BaseReservationItemFormSetWithEvent(forms.BaseInlineFormSet):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for form in self.forms:
                form.fields['ticket_type'].queryset = TicketType.objects.filter(event=event)

    return forms.inlineformset_factory(
        Reservation,
        ReservationItem,
        form=ReservationItemForm,
        formset=BaseReservationItemFormSetWithEvent,
        extra=1,
        can_delete=True,
        validate_min=1,
        fields=['ticket_type', 'quantity'],
    )

class BaseReservationItemFormSet(forms.BaseInlineFormSet):
    """Formset personnalisé pour gérer la validation globale"""
    def clean(self):
        super().clean()
        if not self.is_valid():
            return

        total_quantity = sum(
            form.cleaned_data.get('quantity', 0) 
            for form in self.forms 
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        )

        if total_quantity == 0:
            raise ValidationError("Vous devez sélectionner au moins un billet")

# Formset pour gérer plusieurs ReservationItem
ReservationItemFormSet = forms.inlineformset_factory(
    Reservation,
    ReservationItem,
    form=ReservationItemForm,
    extra=1,
    can_delete=True,
    validate_min=1,
    fields=['ticket_type', 'quantity'],
)

class ReservationConfirmForm(forms.Form):
    """Formulaire de confirmation de réservation"""
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Je confirme ma réservation"
    )