from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    # path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    # path('login/', views.login_user, name='login'),
    # # path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    # path('logout/', views.logout_user, name='logout'),
    path('profile/', views.ProfileDetail.as_view(), name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),

    path('my-account/', TemplateView.as_view(template_name='user/my-account.html'), name='my-account'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
