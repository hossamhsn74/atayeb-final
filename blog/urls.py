
from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('submit-post/', SubmitBlogPost, name='submit-post'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('blog/<int:pk>', PostDetailsView.as_view(),
         name='blog-single'),

    path('blog/<int:pk>/delete', PostDeleteView.as_view(), name='blog-delete'),
    path('blog/<int:pk>/update', PostUpdateView.as_view(), name='blog-update'),
    path('blog/<int:id>/addcomment', AddPostCommentView, name='blog-comment'),
    path("search", SearchBlog, name='search'),
    path('archive/', BlogIndexView, name='archive'),
]
