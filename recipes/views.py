import re
import json
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_renderpdf.views import PDFView
from user.models import Profile

from recipes.models import (Bookmarks, Ingredient, IngredientCategory, Recipe,
                            RecipeCategory, RecipeComment, RecipeIngredient,
                            RecipeInstruction, RecipeNutritionFacts, Tag)


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
            recipe=context['recipe'].id).order_by('ingredient__category')
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
        feature_list = re.split("', '|\['|']|''",  context['recipe'].tags)
        le = len(feature_list)-1
        feature_list_new = []
        for z in range(1, le):
            feature_list_new.append(feature_list[z])
        context['tags_list'] = feature_list_new
        return context


class ExportToPDFView(PDFView):
    template_name = 'recipes/pdf-view.html'
    prompt_download = True

    @property
    def download_name(self) -> str:
        return f"recipe{self.kwargs['pk']}.pdf"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        recipe = Recipe.objects.get(id=kwargs['pk'])
        context['recipe'] = recipe

        ingredents_qs = RecipeIngredient.objects.filter(
            recipe=context['recipe'].id).order_by('ingredient__category')
        context['ingredents'] = [*ingredents_qs]

        instructions_qs = RecipeInstruction.objects.filter(
            recipe=context['recipe'].id
        ).order_by('order')
        context['instructions'] = [*instructions_qs]

        related_nutration_facts_qs = RecipeNutritionFacts.objects.filter(
            recipe=context['recipe'].id
        )
        context['nutration_facts'] = [*related_nutration_facts_qs]
        return context


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


@login_required
def SubmitRecipeView(request):
    if request.method == 'POST':
        # author
        recipe_author = Profile.objects.get(user=request.user)
        recipe_image = request.FILES["recipeImage"]
        recipe_name = request.POST.get('name')
        recipe_feeds_up_to = request.POST.get('feeds_up_to')
        recipe_prep_time = request.POST.get('prep_time')
        recipe_description = request.POST.get('description')

        # category
        recipe_category = RecipeCategory.objects.get_or_create(
            name=request.POST['category'])[0]

        # # tags
        recipe_tags = []
        tags_input = request.POST.get('tags-array')
        split_features = list(tags_input.split(','))
        recipe_tags = [Tag.objects.get_or_create(
            name=item)[0].name for item in split_features]

        for item in recipe_tags:
            Tag.objects.get_or_create(name=item)

        # # create recipe item
        recipe = Recipe.objects.create(
            name=recipe_name, category=recipe_category,
            description=recipe_description, feeds_up_to=recipe_feeds_up_to,
            prep_time=recipe_prep_time, author=recipe_author,
            image=recipe_image, tags=[*recipe_tags])

        # create instructions
        steps_input = str(request.POST['steps-array'])
        steps_list = [x.strip() for x in steps_input.split(',')]
        order = 1
        for item in steps_list:
            RecipeInstruction.objects.create(
                order=order, description=item, recipe=recipe)
            order += 1

        # # create ingredianets
        ingredients_input = json.loads(request.POST['ing-array'])

        for item in ingredients_input:
            ingredient_cat = item[0]
            ingredient_name = item[1]
            ingredient_quantity = item[2]
            ingredient_unit = item[3]
            cat = IngredientCategory.objects.get(name=ingredient_cat)
            ing = Ingredient.objects.get_or_create(
                name=ingredient_name, category=cat)
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ing[0], quantity=ingredient_quantity, unit=ingredient_unit)

        # create nutration facts
        # if request.POST.get('totalFatA') and request.POST.get('totalFatP'):
        #     fact1 = RecipeNutritionFacts.objects.create(recipe=recipe, element="اجمالي الدهون", quantity=request.POST.get(
        #         'totalFatA'), daily_percent=request.POST.get('totalFatP'))
        #     fact1.save()

        # if request.POST.get('mealSizeA') and request.POST.get('mealSizeP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="حجم الوجبة", quantity=request.POST.get(
        #         'mealSizeA'), daily_percent=request.POST.get('mealSizeP'))

        # if request.POST.get('postaiumA') and request.POST.get('postaiumP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="البوتاسيوم", quantity=request.POST.get(
        #         'postaiumA'), daily_percent=request.POST.get('postaiumP'))

        # if request.POST.get('sugerA') and request.POST.get('sugerP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="السكر", quantity=request.POST.get(
        #         'sugerA'), daily_percent=request.POST.get('sugerP'))

        # if request.POST.get('protienA') and request.POST.get('protienP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="البروتين", quantity=request.POST.get(
        #         'protienA'), daily_percent=request.POST.get('protienP'))

        # if request.POST.get('fats3A') and request.POST.get('fats3P'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="الدهون المتحولة", quantity=request.POST.get(
        #         'fats3A'), daily_percent=request.POST.get('fats3P'))

        # if request.POST.get('carbA') and request.POST.get('carbP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="اجمالي الكربوهيدرات", quantity=request.POST.get(
        #         'carbA'), daily_percent=request.POST.get('carbP'))

        # if request.POST.get('fatsA') and request.POST.get('fatsP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="الدهون المشبعة", quantity=request.POST.get(
        #         'fatsA'), daily_percent=request.POST.get('fatsP'))

        # if request.POST.get('fats1A') and request.POST.get('fats1P'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="الدهون الأحادية غير المشبعة", quantity=request.POST.get(
        #         'fats1A'), daily_percent=request.POST.get('fats1P'))

        # if request.POST.get('fats2A') and request.POST.get('fats2P'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="دهون غير مشبعة", quantity=request.POST.get(
        #         'fats2A'), daily_percent=request.POST.get('fats2P'))

        # if request.POST.get('sodiumA') and request.POST.get('sodiumP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="صوديوم", quantity=request.POST.get(
        #         'sodiumA'), daily_percent=request.POST.get('sodiumP'))

        # if request.POST.get('fibersA') and request.POST.get('fibersP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="ألياف", quantity=request.POST.get(
        #         'cfibersAalA'), daily_percent=request.POST.get('fibersP'))

        # if request.POST.get('colestrolA') and request.POST.get('colestrolP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="الكوليسترول", quantity=request.POST.get(
        #         'colestrolA'), daily_percent=request.POST.get('colestrolP'))

        # if request.POST.get('calA') and request.POST.get('calP'):
        #     RecipeNutritionFacts.objects.create(recipe=recipe, element="سعرات حراريه", quantity=request.POST.get(
        #         'calA'), daily_percent=request.POST.get('calP'))

        return redirect("recipes:recipes")

    categories = RecipeCategory.objects.all()
    ing_categories = IngredientCategory.objects.all()
    context = {}
    context['categories'] = [*categories]
    context['ing_categories'] = [*ing_categories]
    return render(request, "recipes/submit-recipe.html", context=context)


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


class RecipeDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'user:login'
    model = Recipe
    success_url = '/'
    template_name = 'recipes/confirm_delete.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user.profile == obj.author:
            return True
        return False


class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = ['name', 'category', 'feeds_up_to',
              'prep_time', 'image', 'description', 'tags']
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse('recipes:recipe-single', kwargs={'pk': self.object.id})


class RecipeInstructionUpdateView(UpdateView):
    model = RecipeInstruction
    fields = ['order', 'description', ]
    template_name_suffix = 'steps_update_form'

    def get_success_url(self):
        return reverse('recipes:recipe-single', kwargs={'pk': self.object.recipe.id})

class RecipeIngredientsUpdateView(UpdateView):
    model = RecipeIngredient
    fields = ['ingredient', 'quantity', 'unit']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('recipes:recipe-single', kwargs={'pk': self.object.recipe.id})

