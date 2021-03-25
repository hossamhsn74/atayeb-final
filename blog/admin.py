from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
    )
    list_select_related = (
        'category',
    )

    class Meta:
        verbose_name_plural = "المنشورات"


class PostCommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'post',
        'body',
        'comment_date',
    )


admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(PostCategory)
