from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from recipes.models import Recipe, RecipeIngredient, RecipeInstruction, RecipeComment, RecipeNutritionFacts, RecipeCategory
from django.db.models import Count

# for pdf
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch


from django_renderpdf.views import PDFView
from django.contrib.auth.mixins import LoginRequiredMixin


# class ExportToPdf(PDFView):
#     model = Recipe
#     template_name = "recipes/recipe-single.html"
#     context_object_name = "recipe"

#     def get_context_data(self, **kwargs):
#         context = super(RecipeDetailsView, self).get_context_data(**kwargs)

#         ingredents_qs = RecipeIngredient.objects.filter(
#             recipe=context['recipe'].id)
#         context['ingredents'] = [*ingredents_qs]

#         instructions_qs = RecipeInstruction.objects.filter(
#             recipe=context['recipe'].id
#         ).order_by('order')
#         context['instructions'] = [*instructions_qs]

#         comments_qs = RecipeComment.objects.filter(
#             recipe=context['recipe'].id).order_by('comment_date')
#         context['comments'] = [*comments_qs]

#         related_products_qs = Recipe.objects.filter(
#             category=context['recipe'].category).order_by('date_created')[:5]
#         context['related_recipes'] = [*related_products_qs]

#         print("context", context)
#         return context


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
        print("context", context)
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

# def search_product(request):
#     keyword=request.GET.get('keyword')
#     myproducts=products.objects.filter(Q(name__icontains=keyword)|Q(descreption__icontains=keyword)|Q(category__icontains=keyword))
#     return render(request,"search.html",{'products':myproducts})


# def comment_product(request,id):
#     print("hey-------")
#     text=request.POST['text']
#     print(text)
#     myproduct=products.objects.get(id=id)
#     new_comment=Comment.objects.create(text=text,product_comment=myproduct, user=request.user)
#     new_comment.save()
#     return HttpResponseRedirect(reverse("details",kwargs={'id':id}))


# def ExportToPdf(request):
#     doc = SimpleDocTemplate("/tmp/recipe.pdf")
#     styles = getSampleStyleSheet()
#     Story = [Spacer(1, 2*inch)]
#     style = styles["Normal"]
#     for i in range(2):
#         bogustext = ("This is Paragraph number %s.  " % i) * 20
#         p = Paragraph(bogustext, style)
#         Story.append(p)
#         Story.append(Spacer(1, 0.2*inch))
#     doc.build(Story)

#     fs = FileSystemStorage("/tmp")
#     with fs.open("somefilename.pdf") as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#         return response

#     return response
