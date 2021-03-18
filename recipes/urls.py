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

    # path('recipes/<int:pk>/addcomment', AddCommentView, name='recipe-single'),
    path('recipe-index/', RecipeIndexView.as_view(), name='recipe-index'),
    path('submit-recipe/', SubmitRecipeView, name='submit-recipe'),
    #     path('pdf/', ExportToPdf.as_view()),

    # to be deleted
    #     path('typography/', TemplateView.as_view(template_name='recipes/typography.html'),
    #          name='typography'),



]
