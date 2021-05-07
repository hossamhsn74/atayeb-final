from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


app_name = 'recipes'
urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/<int:pk>', RecipeDetailsView.as_view(), name='recipe-single'),
    path('recipes/<int:pk>/update', RecipeUpdateView, name='recipe-update'),
    path('recipes/<int:pk>/steps/update', RecipeInstructionUpdateView.as_view(), name='recipe-steps-update'),
    path('recipes/<int:pk>/ingredient/update', RecipeIngredientsUpdateView.as_view(), name='recipe-ingredient-update'),
    path('recipes/<int:pk>/delete', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipes/<int:pk>/pdf/', ExportToPDFView.as_view(), name='recipe-pdf'),
    path('recipes/<int:id>/addcomment', AddCommentView, name='recipe-comment'),
    path('recipes/<int:id>/bookmark', BookmarkRecipeView, name='recipe-bookmark'),
    path('submit-recipe/', SubmitRecipeView, name='submit-recipe'),
    # path('add-recipe/', AddRecipeView, name='add-recipe'),
    path('recipe-index/', RecipeIndexView, name='recipe-index'),
    path("search", SearchRecipes, name='search'),
]
