from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView
from blog.models import (Post, PostCategory, PostComment, Tag)
from django.contrib.auth.decorators import login_required
from user.models import Profile


class PostListView(ListView):
    paginate_by = 10
    model = Post
    template_name = "blog/blog.html"
    context_object_name = "posts"


class PostDetailsView(DetailView):
    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super(PostDetailsView, self).get_context_data(**kwargs)

        comments_qs = PostComment.objects.filter(
            post=context['post'].id).order_by('comment_date')
        context['comments'] = [*comments_qs]

        related_posts_qs = Post.objects.filter(
            category=context['post'].category).order_by('date_created')[:3]
        context['related_posts'] = [*related_posts_qs]
        return context


@login_required
def AddPostCommentView(request, id):
    comment = request.POST['comment']
    post = Post.objects.get(id=id)
    author = Profile.objects.get(user=request.user)
    new_comment = PostComment.objects.create(
        body=comment, post=post, author=author)
    new_comment.save()
    return redirect("blog:blog-single", pk=post.id)
