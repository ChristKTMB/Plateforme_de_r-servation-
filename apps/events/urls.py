from django.urls import path
from django.conf.urls.static import static
from . import views

from django.conf import settings

app_name = 'events'

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('detail/<int:pk>/', views.event_detail, name='event_detail'),
    path('list/', views.event_list, name='event_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)