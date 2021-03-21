from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django_renderpdf.views import PDFView
from recipes.models import (Recipe, RecipeCategory, RecipeComment,
                            RecipeIngredient, RecipeInstruction,
                            RecipeNutritionFacts)


def HomePageView(request):
    recipes = Recipe.objects.all()[0:10]
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/home.html', context)


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
            recipe=context['recipe'].id)
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


def AddCommentView(request, id):
    # print(request.POST)
    # text = request.POST['text']
    # myproduct = products.objects.get(id=id)
    # new_comment = Comment.objects.create(
    #     text=text, product_comment=myproduct, user=request.user)
    # new_comment.save()
    # return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
    pass


class RecipeIndexView(ListView):
    # model = RecipeCategory
    # template_name = "recipes/recipe-index.html"
    # context_object_name = "categories"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['info'] = [*qs]
    #     print(context)
    #     return context
    pass


def SubmitRecipeView(request):
    return render(request, "recipes/submit-recipe.html")
