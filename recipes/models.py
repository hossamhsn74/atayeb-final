from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .my_functions import get_resized_image


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='الفئة')

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='فئة الوصفة')
    image = models.ImageField(null=True, blank=True,
                              default='static/recipes/images/assets/default_no_pic.png.png',
                              upload_to='recipes_pics',
                              verbose_name='الصورة')
    description = models.TextField(null=True, blank=True, verbose_name='الوصف')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = get_resized_image(self, req_width=300, req_height=300)
        img.save(self.image.path)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "فئات الوصفات"


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name='اسم الوصفة')
    category = models.ForeignKey(
        RecipeCategory, on_delete=models.CASCADE, verbose_name='فئة الوصفة')
    recipe_source = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='مصدر الوصفة')
    feeds_up_to = models.SmallIntegerField(
        default=1, verbose_name='تكفي لإطعام')
    prep_time = models.CharField(max_length=50, verbose_name='وقت التحضير')
    date_created = models.DateTimeField(
        default=timezone.now, verbose_name='تاريخ الإضافة')
    image = models.ImageField(null=True, blank=True,
                              default='static/recipes/images/assets/default_no_pic.png',
                              upload_to='recipes_pics',
                              verbose_name='الصورة')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='الكاتب')
    description = models.TextField(verbose_name="الوصف", blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = get_resized_image(self, req_width=600, req_height=600)
        img.save(self.image.path)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "الوصفات"
        ordering = ('name',)


class IngredientCategory(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='فئة المكون')
    # image = models.ImageField(null=True, blank=True,
    #                           default='static/recipes/images/assets/default_no_pic.png.jpg',
    #                           upload_to='recipes_pics',
    #                           verbose_name='الصورة')

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = get_resized_image(self, req_width=300, req_height=300)
    #     img.save(self.image.path)

    class Meta:
        verbose_name_plural = "فئات المكونات"


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='المكون')
    category = models.ForeignKey(IngredientCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name='فئة المكون')
    # image = models.ImageField(null=True, blank=True,
    #                           default='static/recipes/images/assets/default_no_pic.png.jpg',
    #                           upload_to='recipes_pics',
    #                           verbose_name='الصورة')

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = get_resized_image(self, req_width=300, req_height=300)
    #     img.save(self.image.path)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "المكونات"


class RecipeComment(models.Model):
    body = models.TextField(verbose_name='نص التعليق')
    comment_date = models.DateTimeField(
        default=timezone.now, verbose_name='تاريخ التعليق')
    active = models.BooleanField(default=False)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='الوصفة')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='الكاتب')

    def __str__(self):
        return 'تعليق {} على {}.'.format(self.author, self.recipe)

    class Meta:
        verbose_name_plural = "التعليقات"
        ordering = ('-comment_date',)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='الوصفة')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='المكون')
    quantity = models.CharField(max_length=255, verbose_name='المقادير')

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name_plural = "مكونات الوصفة"
        unique_together = ('recipe', 'ingredient')


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='الوصفة')
    order = models.PositiveSmallIntegerField(verbose_name='الترتيب')
    description = models.TextField(verbose_name='الشرح')

    class Meta:
        verbose_name_plural = "الخطوات"
        ordering = ('order',)

NUTRITION_ELEMENTS_CHOICES = (
    ('اجمالي الدهون','اجمالي الدهون'),
    ('حجم الوجبة','حجم الوجبة'),
    ('سعرات حراريه','سعرات حراريه'),
    ('الدهون المشبعة','الدهون المشبعة'),
    ('دهون غير مشبعة','دهون غير مشبعة'),
    ('الدهون الأحادية غير المشبعة','الدهون الأحادية غير المشبعة'),
    ('صوديوم','صوديوم'),
    ('ألياف','ألياف'),
    ('الكوليسترول', 'الكوليسترول'),
    ('الدهون المتحولة','الدهون المتحولة'),
    ('اجمالي الكربوهيدرات','اجمالي الكربوهيدرات'),
    ('البروتين','البروتين'),
    ('سكر','سكر')
)


class RecipeNutritionFacts(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='الوصفة')
    element = models.CharField(max_length=128,
        choices=NUTRITION_ELEMENTS_CHOICES, verbose_name='العنصر')
    quantity = models.CharField(max_length=255, verbose_name='الكمية')
    daily_percent = models.PositiveSmallIntegerField(
        verbose_name='نسبة المقادير اليومية')

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name_plural = "الحقائق الغذائية للوصفة"
        unique_together = ('recipe', 'element')
