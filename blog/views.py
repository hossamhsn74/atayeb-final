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

        recent_posts_qs = Post.objects.all().order_by('-date_created')[:4]
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
            post=context['post'].id).order_by('-comment_date')
        context['comments'] = [*comments_qs]

        related_posts_qs = Post.objects.filter(
            category=context['post'].category).order_by('-date_created')[:3]
        context['related_posts'] = [*related_posts_qs]

        recent_posts_qs = Post.objects.all().order_by('-date_created')[:4]
        context['recent_posts'] = [*recent_posts_qs]

        data = {}
        categories = PostCategory.objects.all()
        for category in categories:
            posts = Post.objects.filter(category=category).count()
            data[category] = posts
        context["index_data"] = data

        context['tags'] = [*Tag.objects.all()]
        print("tags = ", context['post'].tags)
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


def BlogIndexView(request):
    context = {}

    recent_posts_qs = Post.objects.all().order_by('date_created')[:4]
    context['recent_posts'] = [*recent_posts_qs]

    context['tags'] = [*Tag.objects.all()]
    data = {}
    categories = PostCategory.objects.all()
    for category in categories:
        posts = Post.objects.filter(category=category).count()
        data[category] = posts
    context["index_data"] = data

    data = {}
    categories = PostCategory.objects.all()
    for category in categories:
        posts = Post.objects.filter(category=category)
        data[category] = [*posts]
    context["data"] = data
    return render(request, "blog/archive.html", context)


@login_required
def SubmitBlogPost(request):
    if request.method == 'POST':
        # author
        post_author = Profile.objects.get(user=request.user)
        post_image = request.FILES["postImage"]
        post_title = request.POST.get('title')
        post_body = request.POST.get('body')

        # tags
        post_tags = []
        tags_input = request.POST.get('tags')
        tags_list = [x.strip() for x in tags_input.split(',')]

        for item in tags_list:
            post_tags.append(Tag.objects.get_or_create(name=item))

        # category
        category_field = request.POST.get('category')

        if category_field == "other":
            other_category_field = request.POST.get('other_category')
            post_category = PostCategory.objects.get_or_create(
                name=other_category_field)[0]
        else:
            post_category = PostCategory.objects.get(
                name=request.POST.get('category'))

        # create recipe item
        post = Post.objects.create(
            title=post_title, category=post_category, author=post_author, image=post_image, body=post_body)
        post.save()

        # add tags to post
        # need to be implemented here
        for item in post_tags:
            post.tags.add(item[0].id)

        return redirect("blog:blog")

    categories = PostCategory.objects.all()
    context = {}
    context['categories'] = [*categories]
    return render(request, "blog/submit-post.html", context=context)
