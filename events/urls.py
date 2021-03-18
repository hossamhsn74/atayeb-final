from django.urls import path
from .views import *
from django.views.generic import TemplateView


app_name = 'events'
urlpatterns = [
    path('event/', TemplateView.as_view(template_name='recipes/event.html'), name='event'),
    path('event-single/', TemplateView.as_view(template_name='recipes/event-single.html'),
         name='event-single'),
]