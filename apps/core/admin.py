from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Remove created and modified if they don't exist in the model
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 20