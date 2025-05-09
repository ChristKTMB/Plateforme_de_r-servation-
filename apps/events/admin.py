from django.contrib import admin
from .models import Event, TicketType

class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 1
    min_num = 1  # Require at least one ticket type

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer', 'total_tickets', 'price', 'is_published')
    list_filter = ('is_published', 'date', 'categories')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    filter_horizontal = ('categories',)
    inlines = [TicketTypeInline]
    
    # Fields grouping for better organization
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'date', 'location')
        }),
        ('Organization', {
            'fields': ('organizer', 'categories')
        }),
        ('Ticket Information', {
            'fields': ('total_tickets', 'price')
        }),
        ('Media & Status', {
            'fields': ('image', 'is_published')
        })
    )

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'price', 'quantity_available')
    list_filter = ('event',)
    search_fields = ('name', 'event__title')