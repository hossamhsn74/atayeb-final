from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = 'recipes'
urlpatterns = [

    path('', HomePageView, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/<int:pk>', RecipeDetailsView.as_view(), name='recipe-single'),
    path('recipe-index/', RecipeIndexView, name='recipe-index'),
    path('submit-recipe/', SubmitRecipeView, name='submit-recipe'),
#     path('pdf/', ExportToPdf.as_view()),

    path('faq/', TemplateView.as_view(template_name='recipes/faq.html'), name='faq'),
    path('about/', TemplateView.as_view(template_name='recipes/about.html'), name='about'),
    
    path('typography/', TemplateView.as_view(template_name='recipes/typography.html'),
         name='typography'),

    path('blog/', TemplateView.as_view(template_name='recipes/blog.html'), name='blog'),
    path('blog-single/', TemplateView.as_view(template_name='recipes/blog-single.html'),
         name='blog-single'),
    path('archive/', TemplateView.as_view(template_name='recipes/archive.html'), name='archive'),
    path('contacts/', TemplateView.as_view(template_name='recipes/contact.html'), name='contacts'),

    path('event/', TemplateView.as_view(template_name='recipes/event.html'), name='event'),
    path('event-single/', TemplateView.as_view(template_name='recipes/event-single.html'),
         name='event-single'),


]
