from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', views.EventViewSet)

app_name = 'events'

urlpatterns = [
    # Routes pour l'API
    path('api/', include(router.urls)),
    
    # Routes pour les templates
    path('create/', views.create_event, name='create_event'),
    path('detail/<int:pk>/', views.event_detail, name='event_detail'),
    path('list/', views.event_list, name='event_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)