from django.shortcuts import render

from recipes.models import Recipe


# ------------- HOME --------------
def home(request):
    recipes = Recipe.objects.all()[0:2]
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/home.html', context)
