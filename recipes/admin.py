from django.contrib import admin

from .models import *


class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id'
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'id'
    )
    list_select_related = (
        'category',
    )


class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id'
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'prep_time',
        'id'
    )
    list_select_related = (
        'category',
    )

    class Meta:
        verbose_name_plural = "الوصفات"


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'quantity',
        'id'
    )


class InstructionAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'order',
        'description'
    )


class NutrationFactsAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'element',
        'quantity',
        'daily_percent'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'recipe',
        'body',
        'comment_date',
    )


admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeInstruction, InstructionAdmin)

admin.site.register(RecipeComment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(RecipeNutritionFacts, NutrationFactsAdmin)
admin.site.register(Bookmarks)