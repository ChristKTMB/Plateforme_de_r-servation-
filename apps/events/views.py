from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .serializer import EventSerializer, TicketTypeSerializer
from .permissions import IsOrganizerOrReadOnly
from .forms import EventForm, TicketTypeFormSet
from .models import Event

@login_required
def create_event(request):
    # Vérifier si l'utilisateur est un organisateur
    if request.user.user_type != 'O':
        raise PermissionDenied("Seuls les organisateurs peuvent créer des événements.")
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        formset = TicketTypeFormSet(request.POST)
        
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()
            
            formset = TicketTypeFormSet(request.POST, instance=event)
            if formset.is_valid():
                formset.save()
                messages.success(request, "L'événement a été créé avec succès!")
                return redirect('events:event_detail', pk=event.pk)
            else:
                event.delete()
    else:
        form = EventForm()
        formset = TicketTypeFormSet()
    
    return render(request, 'events/create_event.html', {
        'form': form,
        'formset': formset
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    ticket_types = event.ticket_types.all()
    
    context = {
        'event': event,
        'ticket_types': ticket_types,
    }
    return render(request, 'events/event_detail.html', context)

def event_list(request):
    events = Event.objects.filter(is_published=True).order_by('-date')

    paginator = Paginator(events, 10)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    return render(request, 'events/event_list.html', {'events': events})

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_published=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'events/event_list.html'

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Pour le rendu template
            events = self.get_queryset()
            paginator = Paginator(events, 10)
            page = request.GET.get('page')
            events = paginator.get_page(page)
            return Response({'events': events})
        # Pour l'API
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.accepted_renderer.format == 'html':
            return Response({
                'event': instance,
                'ticket_types': instance.ticket_types.all()
            }, template_name='events/event_detail.html')
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            if request.method == 'GET':
                form = EventForm()
                formset = TicketTypeFormSet()
                return Response({
                    'form': form,
                    'formset': formset
                }, template_name='events/create_event.html')
            
            form = EventForm(request.POST, request.FILES)
            formset = TicketTypeFormSet(request.POST)
            if form.is_valid() and formset.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user
                event.save()
                form.save_m2m()
                formset.instance = event
                formset.save()
                return redirect('events:event_detail', pk=event.pk)
            return Response({
                'form': form,
                'formset': formset
            }, template_name='events/create_event.html')
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def add_ticket_type(self, request, pk=None):
        event = self.get_object()
        serializer = TicketTypeSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)