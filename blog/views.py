from blog.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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


class RegisterFormView(generic.FormView):
    template_name = "blog/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("blog:posts")

    def form_valid(self, form):
        user = form.save()
        # form.cleaned_data.get("password1")

        # username = self.request.POST["username"]
        # password = self.request.POST["password1"]

        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)

