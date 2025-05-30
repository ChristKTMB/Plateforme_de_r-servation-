from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .serializer import EventSerializer, TicketTypeSerializer
from .permissions import IsOrganizerOrReadOnly
from .forms import EventForm, TicketTypeFormSet
from .models import Event

# @login_required
# def create_event(request):
#     # Vérifier si l'utilisateur est un organisateur
#     if request.user.user_type != 'O':
#         raise PermissionDenied("Seuls les organisateurs peuvent créer des événements.")
    
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)
#         formset = TicketTypeFormSet(request.POST)
        
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.organizer = request.user
#             event.save()
#             form.save_m2m()
            
#             formset = TicketTypeFormSet(request.POST, instance=event)
#             if formset.is_valid():
#                 formset.save()
#                 messages.success(request, "L'événement a été créé avec succès!")
#                 return redirect('events:event_detail', pk=event.pk)
#             else:
#                 event.delete()
#     else:
#         form = EventForm()
#         formset = TicketTypeFormSet()
    
#     return render(request, 'events/create_event.html', {
#         'form': form,
#         'formset': formset
#     })

# def event_detail(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     ticket_types = event.ticket_types.all()
    
#     context = {
#         'event': event,
#         'ticket_types': ticket_types,
#     }
#     return render(request, 'events/event_detail.html', context)

# def event_list(request):
#     events = Event.objects.filter(is_published=True).order_by('-date')

#     paginator = Paginator(events, 10)
#     page = request.GET.get('page')
#     events = paginator.get_page(page)

#     return render(request, 'events/event_list.html', {'events': events})

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    queryset = Event.objects.filter(is_published=True)
    paginate_by = 10

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_types'] = self.object.ticket_types.all()
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TicketTypeFormSet(self.request.POST)
        else:
            context['formset'] = TicketTypeFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.organizer = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_published=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get_template_names(self):
        """Retourne le template approprié selon l'action"""
        templates = {
            'list': 'events/event_list.html',
            'retrieve': 'events/event_detail.html',
            'create': 'events/create_event.html',
        }
        return [templates.get(self.action, 'events/event_list.html')]

    def get_renderer_context(self):
        """Prépare le contexte pour le rendu"""
        context = super().get_renderer_context()
        if self.request.accepted_renderer.format == 'html':
            if self.action == 'create':
                context.update({
                    'form': EventForm(),
                    'formset': TicketTypeFormSet()
                })
            elif self.action == 'list':
                events = self.paginate_queryset(self.get_queryset())
                context['events'] = events
            elif self.action == 'retrieve':
                context.update({
                    'event': self.get_object(),
                    'ticket_types': self.get_object().ticket_types.all()
                })
        return context

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return self._handle_html_create(request)
        return self._handle_api_create(request)

    def _handle_html_create(self, request):
        """Gestion de la création via formulaire HTML"""
        if request.method == 'GET':
            return Response(self.get_renderer_context())
        
        form = EventForm(request.POST, request.FILES)
        formset = TicketTypeFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            event = self._save_event(form, formset)
            messages.success(request, "L'événement a été créé avec succès!")
            return redirect('events:event_detail', pk=event.pk)
        
        return Response({'form': form, 'formset': formset})

    def _save_event(self, form, formset):
        """Sauvegarde l'événement et ses tickets"""
        event = form.save(commit=False)
        event.organizer = self.request.user
        event.save()
        form.save_m2m()
        formset.instance = event
        formset.save()
        return event

    def _handle_api_create(self, request):
        """Gestion de la création via l'API"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Personnalisation de la création d'un événement"""
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def add_ticket_type(self, request, pk=None):
        """Ajoute un type de ticket à un événement"""
        event = self.get_object()
        serializer = TicketTypeSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)