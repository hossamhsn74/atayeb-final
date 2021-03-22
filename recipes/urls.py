from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


app_name = 'recipes'
urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/<int:pk>', RecipeDetailsView.as_view(), name='recipe-single'),
    path('recipes/<int:pk>/pdf/', ExportToPDFView.as_view(), name='recipe-pdf'),
    path('recipe-index/', RecipeIndexView, name='recipe-index'),

    path('submit-recipe/', SubmitRecipeView, name='submit-recipe'),
    # path('recipes/<int:pk>/addcomment', AddCommentView, name='recipe-single'),
    # path('recipes/<int:pk>/bookmark', AddCommentView, name='recipe-single'),
]
