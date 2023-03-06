from django.contrib.messages.views import SuccessMessageMixin
from blog.forms import RegisterForm
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Post, Comment

User = get_user_model()


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostsView(generic.ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'entries_list'
    paginate_by = 10
    model = Post

    def get_queryset(self):
        if 'author' in self.kwargs:
            return Post.objects.filter(is_published=True, is_moderated=True, author__id=self.kwargs["author"]).all()
        else:
            return Post.objects.filter(is_published=True, is_moderated=True).all()


class CreatePostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('blog:login')
    template_name = 'blog/create_post.html'
    model = Post
    success_url = reverse_lazy('blog:posts')
    fields = ['title', 'brief_content', 'content', 'image', 'is_published']
    success_message = "Post created"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CreatePostView, self).form_valid(form)


class CreateCommentView(SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('blog:login')
    template_name = 'blog/create_comment.html'
    model = Comment
    success_url = reverse_lazy('blog:posts')
    fields = ['content', 'image']
    success_message = "Comment created"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs["pk"])
        form.save()
        return super(CreateCommentView, self).form_valid(form)


class EditPostView(SuccessMessageMixin, AuthorRequiredMixin, generic.UpdateView):
    model = Post
    fields = ["title", 'brief_content', "content", "image"]
    template_name = "blog/update_post.html"
    success_url = reverse_lazy("blog:posts")
    success_message = "Post updated"


class RegisterFormView(SuccessMessageMixin, generic.FormView):
    template_name = "blog/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("blog:posts")
    success_message = "User created"

    def form_valid(self, form):
        user = form.save()
        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "blog/update_profile.html"
    success_url = reverse_lazy("blog:posts")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class Profile(generic.DetailView):
    model = User
    context_object_name = 'entry'
    template_name = "blog/profile.html"


class PostView(generic.DetailView):
    model = Post
    context_object_name = 'entry'
    template_name = "blog/post.html"

    def get_object(self, queryset=None):
        post = Post.objects.get(id=self.kwargs["pk"])
        return post
