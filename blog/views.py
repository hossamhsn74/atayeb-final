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

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        recent_posts_qs = Post.objects.all().order_by('date_created')[:4]
        context['recent_posts'] = [*recent_posts_qs]

        data = {}
        categories = PostCategory.objects.all()
        for category in categories:
            posts = Post.objects.filter(category=category).count()
            data[category] = posts
        context["index_data"] = data

        context['tags'] = [*Tag.objects.all()]
        return context


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

        recent_posts_qs = Post.objects.all().order_by('date_created')[:4]
        context['recent_posts'] = [*recent_posts_qs]

        data = {}
        categories = PostCategory.objects.all()
        for category in categories:
            posts = Post.objects.filter(category=category).count()
            data[category] = posts
        context["index_data"] = data

        context['tags'] = [*Tag.objects.all()]
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


def SearchBlog(request):
    keyword = request.GET.get('keyword')
    myposts = Post.objects.filter(title__icontains=keyword)
    return render(request, "blog/blog.html", {'posts': myposts})
