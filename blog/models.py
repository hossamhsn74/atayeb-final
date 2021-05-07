from user.models import Profile
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='اسم العلامة')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "العلامات"


class PostCategory(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='فئة المنشور')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "فئات المنشور"


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان المنشور")
    category = models.ForeignKey(
        PostCategory, on_delete=models.CASCADE, verbose_name='فئة المنشور')
    date_created = models.DateTimeField(
        default=timezone.now, verbose_name='تاريخ الإضافة')
    image = ResizedImageField(null=False, blank=False,
                              default=None,
                              upload_to='post_images/',
                              verbose_name='الصورة')
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name='الكاتب')
    body = models.TextField(verbose_name="المحتوي", blank=True, null=True)
    tags = models.CharField(max_length=300, null=True, blank=True, verbose_name="العلامات")

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "المنشورات"
        ordering = ('-date_created',)


class PostComment(models.Model):
    body = models.TextField(verbose_name='نص التعليق')
    comment_date = models.DateTimeField(
        default=timezone.now, verbose_name='تاريخ التعليق')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment_post', verbose_name='المنشور')
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comment_author', verbose_name='الكاتب')

    def __str__(self):
        return 'تعليق {} على {}.'.format(self.author, self.post)

    class Meta:
        verbose_name_plural = "التعليقات"
        ordering = ('-comment_date',)
