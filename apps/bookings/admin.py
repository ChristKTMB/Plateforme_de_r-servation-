
from django.contrib import admin
from .models import Reservation, ReservationItem

class ReservationItemInline(admin.TabularInline):
    model = ReservationItem
    extra = 1

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reference', 'user', 'event', 'is_confirmed')
    search_fields = ('reference', 'user__username', 'event__title')
    list_filter = ('is_confirmed',)
    inlines = [ReservationItemInline]
    readonly_fields = ('reference',) 

@admin.register(ReservationItem)
class ReservationItemAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'ticket_type', 'quantity')
