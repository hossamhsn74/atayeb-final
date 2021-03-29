
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('invitations/', include('invitations.urls', namespace='invitations')),

    path('', include('core.urls')),
    path('', include('blog.urls')),
    path('', include('events.urls')),
    path('', include('recipes.urls')),
    path('', include('user.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
