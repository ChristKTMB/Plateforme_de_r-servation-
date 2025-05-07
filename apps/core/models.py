from django.db import models

class TimeStampedModel(models.Model):

    """Modele de base avec champs de timestamp"""
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True

class Category(TimeStampedModel): 
    """Catégories d'evenements"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name