from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .my_functions import get_resized_image


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='الفئة')

    def __str__(self):
        return self.name


class PostCategory(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='فئة المنشور')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "فئات المنشورات"


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='العنوان')
    category = models.ForeignKey(
        RecipeCategory, on_delete=models.CASCADE, verbose_name='فئة الوصفة')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='الكاتب')
    date_created = models.DateTimeField(
        default=timezone.now, verbose_name='تاريخ الإضافة')
    image = models.ImageField(null=True, blank=True,
                              default='static/recipes/images/assets/default_no_pic.png',
                              upload_to='post_pics/',
                              verbose_name='الصورة')
    body = models.TextField(verbose_name="المحتوي", blank=True, null=True)
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
        verbose_name_plural = "المنشورات"
        ordering = ('name',)


class PostComment(models.Model):
    body = models.TextField(verbose_name='نص التعليق')
    comment_date = models.DateTimeField(
        default=timezone.now, verbose_name='تاريخ التعليق')
    active = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name='المنشور')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='الكاتب')

    def __str__(self):
        return 'تعليق {} على {}.'.format(self.author, self.recipe)

    class Meta:
        verbose_name_plural = "التعليقات"
        ordering = ('-comment_date',)
