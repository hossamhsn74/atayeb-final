from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from .views import *

# ------------- HOME --------------

# ------ Ingredient, Recipe, RecipeCategory, RecipeIngredient, IngredientCategory

app_name = 'recipes'
urlpatterns = [
    # ---------------- HOME ------------

    path('', home, name='home'),
    path('home/', TemplateView.as_view(template_name='recipes/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='recipes/about.html'), name='about'),
    path('archive/', TemplateView.as_view(template_name='recipes/archive.html'), name='archive'),
    path('blog/', TemplateView.as_view(template_name='recipes/blog.html'), name='blog'),
    path('blog-single/', TemplateView.as_view(template_name='recipes/blog-single.html'), name='blog-single'),
    path('contacts/', TemplateView.as_view(template_name='recipes/contact.html'), name='contacts'),
    path('event/', TemplateView.as_view(template_name='recipes/event.html'), name='event'),
    path('event-single/', TemplateView.as_view(template_name='recipes/event-single.html'), name='event-single'),
    path('faq/', TemplateView.as_view(template_name='recipes/faq.html'), name='faq'),
    path('home/', TemplateView.as_view(template_name='recipes/home.html'), name='home'),
    path('recipe-index/', TemplateView.as_view(template_name='recipes/recipe-index.html'), name='recipe-index'),
    path('recipe-single/', TemplateView.as_view(template_name='recipes/recipe-single.html'), name='recipe-single'),
    path('recipes/', TemplateView.as_view(template_name='recipes/recipes.html'), name='recipes'),
    path('submit-recipe/', TemplateView.as_view(template_name='recipes/submit-recipe.html'), name='submit-recipe'),
    path('typography/', TemplateView.as_view(template_name='recipes/typography.html'), name='typography'),

    path('test/', TemplateView.as_view(template_name='user/invite_form.html'), name='test_code'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


