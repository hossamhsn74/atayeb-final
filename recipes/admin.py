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
        'recipe_source',
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
        'number',
        'description'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'active',
        'recipe',
        'body',
        'comment_date',
        'id'
    )


admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Instruction, InstructionAdmin)

admin.site.register(Comment, CommentAdmin)
