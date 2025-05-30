from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from . import views

# Configuration du routeur DRF
router = DefaultRouter()
router.register(r'', views.EventViewSet, basename='events')

app_name = 'events'

urlpatterns = [
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),

    # Routes pour l'API et les templates, gérées par le même ViewSet
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)