import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from user.models import Profile

from blog.models import Post, PostCategory, PostComment, Tag


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

        # handle post tags
        feature_list = re.split("', '|\['|']|''",  context['post'].tags)
        le = len(feature_list)-1
        feature_list_new = []
        for z in range(1, le):
            feature_list_new.append(feature_list[z])
        context['tags_list'] = feature_list_new

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
        tags_input = request.POST.get('tags-array')
        split_features = list(tags_input.split(','))
        post_tags = [Tag.objects.get_or_create(
            name=item)[0].name for item in split_features]

        for item in post_tags:
            Tag.objects.get_or_create(name=item)

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
            title=post_title, category=post_category, tags=[*post_tags], author=post_author, image=post_image, body=post_body)
        post.save()
        return redirect("blog:blog")

    categories = PostCategory.objects.all()
    context = {}
    context['categories'] = [*categories]
    return render(request, "blog/submit-post.html", context=context)



class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'user:login'
    model = Post
    success_url = '/'
    template_name = 'blog/confirm_delete.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user.profile == obj.author:
            return True
        return False


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'category', 'image', 'body', 'tags' ]
    template_name_suffix = '_update_form'