# apps/bookings/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.events.models import Event
from .models import Reservation, ReservationItem
from .serializers import ReservationSerializer, ReservationItemSerializer
from .forms import ReservationForm, get_reservation_item_formset

# Vues pour les templates
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'bookings/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'bookings/reservation_detail.html'
    context_object_name = 'reservation'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'bookings/reservation_form.html'
    success_url = reverse_lazy('bookings:reservation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        formset_class = get_reservation_item_formset(event=event)
        
        if self.request.POST:
            context['formset'] = formset_class(self.request.POST)
        else:
            context['formset'] = formset_class()
        
        context['event'] = event
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        event = context['event']
        
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.event = event
            self.object.save()
            
            formset.instance = self.object
            formset.save()
            
            messages.success(self.request, 'Réservation créée avec succès!')
            return redirect('bookings:reservation_detail', pk=self.object.pk)
            
        return self.render_to_response(self.get_context_data(form=form))

class ReservationConfirmView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'bookings/reservation_confirm.html'
    context_object_name = 'reservation'

    def post(self, request, *args, **kwargs):
        reservation = self.get_object()
        try:
            reservation.confirm()
            messages.success(request, 'Réservation confirmée avec succès!')
            return redirect('bookings:reservation_detail', pk=reservation.pk)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('bookings:reservation_detail', pk=reservation.pk)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

# Vues pour l'API
class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation.confirm()
            return Response({'status': 'Réservation confirmée'})
        except ValidationError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ReservationItemViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReservationItem.objects.filter(
            reservation__user=self.request.user
        )
