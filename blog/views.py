from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Post, Comment


class AuthRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user


class PostsView(generic.ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'entries_list'
    paginate_by = 10
    model = Post

    def get_queryset(self):
        return Post.objects.all()


class CreatePostView(AuthRequiredMixin, CreateView):
    template_name = 'blog/create_post.html'
    model = Post
    fields = ['title', 'content', 'image']

