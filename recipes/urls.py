from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = 'recipes'
urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/<int:pk>', RecipeDetailsView.as_view(), name='recipe-single'),
    path('recipes/<int:pk>/pdf/', ExportToPDFView.as_view(), name='recipe-pdf'),
    path('recipe-index/', RecipeIndexView, name='recipe-index'),

    # path('recipes/<int:pk>/addcomment', AddCommentView, name='recipe-single'),
    path('submit-recipe/', SubmitRecipeView, name='submit-recipe'),

    # to be deleted
    #     path('typography/', TemplateView.as_view(template_name='recipes/typography.html'),
    #          name='typography'),



]
