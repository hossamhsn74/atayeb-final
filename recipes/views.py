from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView
# from django_renderpdf.views import PDFView
from recipes.models import (Recipe, RecipeCategory, RecipeComment,
                            RecipeIngredient, RecipeInstruction,
                            RecipeNutritionFacts, Bookmarks, Tag)
from django.contrib.auth.decorators import login_required
from user.models import Profile


class RecipeListView(ListView):
    paginate_by = 16
    model = Recipe
    template_name = "recipes/recipes.html"
    context_object_name = "recipes"


class RecipeDetailsView(DetailView):
    model = Recipe
    template_name = "recipes/recipe-single.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailsView, self).get_context_data(**kwargs)

        ingredents_qs = RecipeIngredient.objects.filter(
            recipe=context['recipe'].id)
        context['ingredents'] = [*ingredents_qs]

        instructions_qs = RecipeInstruction.objects.filter(
            recipe=context['recipe'].id
        ).order_by('order')
        context['instructions'] = [*instructions_qs]

        comments_qs = RecipeComment.objects.filter(
            recipe=context['recipe'].id).order_by('comment_date')
        context['comments'] = [*comments_qs]

        related_products_qs = Recipe.objects.filter(
            category=context['recipe'].category).order_by('date_created')[:5]
        context['related_recipes'] = [*related_products_qs]

        related_nutration_facts_qs = RecipeNutritionFacts.objects.filter(
            recipe=context['recipe'].id
        )
        context['nutration_facts'] = [*related_nutration_facts_qs]
        return context


# class ExportToPDFView(PDFView):
#     template_name = 'recipes/pdf-view.html'
#     prompt_download = True

#     @property
#     def download_name(self) -> str:
#         return f"recipe{self.kwargs['pk']}.pdf"

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)

#         recipe = Recipe.objects.get(id=kwargs['pk'])
#         context['recipe'] = recipe

#         ingredents_qs = RecipeIngredient.objects.filter(
#             recipe=context['recipe'].id)
#         context['ingredents'] = [*ingredents_qs]

#         instructions_qs = RecipeInstruction.objects.filter(
#             recipe=context['recipe'].id
#         ).order_by('order')
#         context['instructions'] = [*instructions_qs]

#         related_nutration_facts_qs = RecipeNutritionFacts.objects.filter(
#             recipe=context['recipe'].id
#         )
#         context['nutration_facts'] = [*related_nutration_facts_qs]
#         return context


@login_required
def AddCommentView(request, id):
    comment = request.POST['comment']
    recipe = Recipe.objects.get(id=id)
    author = Profile.objects.get(user=request.user)
    new_comment = RecipeComment.objects.create(
        body=comment, recipe=recipe, author=author)
    new_comment.save()
    return redirect("recipes:recipe-single", pk=recipe.id)


def RecipeIndexView(request):
    context = {}
    data = {}
    categories = RecipeCategory.objects.all()
    for category in categories:
        recipes = Recipe.objects.filter(category=category)
        data[category] = [*recipes]
    context["data"] = data
    return render(request, "recipes/recipe-index.html", context)


# @login_required
# def SubmitRecipeView(request):
#     categories = RecipeCategory.objects.all()
#     context = {}
#     context['categories'] = [*categories]
#     return render(request, "recipes/submit-recipe.html", context=context)


# def AddRecipeView(request):
#     category_field = request.POST['category']
#     if category_field == "other":
#         other_category_field = request.POST['other_category']
#         recipe_category = RecipeCategory.objects.get_or_create(
#             name=other_category_field)
#     else:
#         recipe_category = RecipeCategory.objects.get(
#             name=request.POST['category'])

#     recipe_name = request.POST['name']
#     recipe_image = request.POST['image']
#     recipe_feeds_up_to = request.POST['feeds_up_to']
#     recipe_prep_time = request.POST['prep_time']
#     recipe_description = request.POST['description']

#     # author
#     recipe_author = Profile.objects.get(user=request.user)

#     # tags
#     recipe_tags = []
#     tags_input = request.POST['tags']
#     tags_list = [x.strip() for x in tags_input.split(',')]

#     for item in tags_list:
#         recipe_tags.append(Tag.objects.get_or_create(name=item))

#     # create recipe item
#     recipe = Recipe.objects.create(
#         name=recipe_name, category=recipe_category,
#         description=recipe_description, feeds_up_to=recipe_feeds_up_to,
#         prep_time=recipe_prep_time, author=recipe_author,
#         image=recipe_image)

#     for item in recipe_tags:
#         recipe.tags.add(item[0].id)

    # create instructions
    # recipe_instructions = []
    # instructions_input = request.POST['instructions']
    # instructions_list = [x.strip() for x in tags_input.split(',')]

    # for item in instructions_list:
    #     recipe_instructions.append(RecipeInstruction.objects.get_or_create(
    #         recipe=recipe, description=description, order=order))

    # create ingredianets
    # ingredients_input = request.POST['ingredients']

    # create nutration facts

    # return redirect("recipes:recipes")


def SearchRecipes(request):
    keyword = request.GET.get('keyword')
    myrecipes = Recipe.objects.filter(name__icontains=keyword)
    return render(request, "recipes/recipes.html", {'recipes': myrecipes})


@login_required
def BookmarkRecipeView(request, id):
    recipe = Recipe.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    bookmarks_pool = Bookmarks.objects.get_or_create(profile=profile)
    bookmarks_pool[0].recipes.add(recipe)
    BookmarkedFlag = True
    return redirect("recipes:recipe-single", pk=recipe.id)
