from django.urls import path
from .views import HomePageView, FaqPageView, AboutUsPageView, ContacUsView, SendContactMessageView, NewsLetterSubscribe

app_name = 'core'

urlpatterns = [
    path('', HomePageView, name='home'),
    path('faq/', FaqPageView, name='faq'),
    path('about/', AboutUsPageView, name='about'),
    path('contacts/', ContacUsView, name='contacts'),
    path('contacts/sent', SendContactMessageView, name='send-contact-message'),
    path('subscribe', NewsLetterSubscribe, name='subscribe'),

]
