from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from user.views import AcceptInviteView

from .views import *

app_name = 'user'
urlpatterns = [
    path('my-account/', MyProfileView, name='my-account'),

    path('profile_update/', profile_update, name='profile_update'),


    path('invite-form/', TemplateView.as_view(template_name='user/invite_form.html'),
         name='invite_form'),

    path('invite/', invite_friend, name='invite_friend'),
    path(r'^invitations/accept-invite/(?P<key>\w+)/?$',
         AcceptInviteView.as_view(), name='accept-invite'),

]
