from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import EventForm, TicketTypeFormSet
from .models import Event
from django.core.paginator import Paginator

@login_required
def create_event(request):
    # Vérifier si l'utilisateur est un organisateur
    if request.user.user_type != 'O':
        raise PermissionDenied("Seuls les organisateurs peuvent créer des événements.")
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        formset = TicketTypeFormSet(request.POST)  # Initialize formset here
        
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()  # Sauvegarde des catégories (ManyToMany)
            
            formset = TicketTypeFormSet(request.POST, instance=event)
            if formset.is_valid():
                formset.save()
                messages.success(request, "L'événement a été créé avec succès!")
                return redirect('events:event_detail', pk=event.pk)
            else:
                event.delete()  # Delete the event if formset is invalid
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

    paginator = Paginator(events, 10)  # 10 événements par page
    page = request.GET.get('page')
    events = paginator.get_page(page)

    return render(request, 'events/event_list.html', {'events': events})