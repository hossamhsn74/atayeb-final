
from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('blog/', PostListView.as_view(), name='blog'),
    path('blog/<int:pk>', PostDetailsView.as_view(),
         name='blog-single'),
    path('blog/<int:id>/addcomment', AddPostCommentView, name='blog-comment'),
    path("search",SearchBlog,name='search'),

    path('archive/', TemplateView.as_view(template_name='blog/archive.html'), name='archive'),
]
