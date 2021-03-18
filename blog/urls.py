
from django.urls import path
from .views import *
from django.views.generic import TemplateView


app_name = 'blog'
urlpatterns = [
    path('faq/', TemplateView.as_view(template_name='blog/faq.html'), name='faq'),
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='about'),

    path('blog/', TemplateView.as_view(template_name='blog/blog.html'), name='blog'),
    path('blog-single/', TemplateView.as_view(template_name='blog/blog-single.html'),
         name='blog-single'),
    path('archive/', TemplateView.as_view(template_name='blog/archive.html'), name='archive'),
    path('contacts/', TemplateView.as_view(template_name='blog/contact.html'), name='contacts'),
]
