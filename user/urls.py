from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'user'
urlpatterns = [

    path('profile_update/', profile_update, name='profile_update'),

    path('my-account/', TemplateView.as_view(template_name='user/my-account.html'), name='my-account'),

    path('invite-form/', TemplateView.as_view(template_name='user/invite_form.html'), name='invite_form'),

    path('invite/', invite_friend, name='invite_friend'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
