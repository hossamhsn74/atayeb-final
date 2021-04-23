from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


app_name = 'recipes'
urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/<int:pk>', RecipeDetailsView.as_view(), name='recipe-single'),
    path('recipes/<int:pk>/pdf/', RecipeDetailsView.as_view(), name='recipe-pdf'),
    path('recipes/<int:id>/addcomment', AddCommentView, name='recipe-comment'),
    path('recipes/<int:id>/bookmark', BookmarkRecipeView, name='recipe-bookmark'),
    path('submit-recipe/', SubmitRecipeView, name='submit-recipe'),
    # path('add-recipe/', AddRecipeView, name='add-recipe'),
    path('recipe-index/', RecipeIndexView, name='recipe-index'),
    path("search", SearchRecipes, name='search'),
]
