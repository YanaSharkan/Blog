from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from blog.forms import RegisterForm, FeedbackForm
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page


from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Post, Comment, Profile
from .tasks import send_feedback, send_content_notification

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
            if self.request.user.id:
                return Post.objects.filter(author=self.request.user) | Post.objects.filter(is_published=True,
                                                                                           is_moderated=True).all()
            else:
                return Post.objects.filter(is_published=True, is_moderated=True).all()


def leave_feedback(request):
    params = dict()
    params["form"] = FeedbackForm()

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            superusers_emails = User.objects.filter(is_superuser=True).values_list('email').first()
            send_feedback.apply_async((superusers_emails, form.cleaned_data['text']))
            messages.success(request, 'Feedback was sent')
            return redirect(reverse_lazy("blog:posts"))

    return render(request, "blog/feedback.html", params)


class CreatePostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('blog:login')
    template_name = 'blog/create_post.html'
    model = Post
    success_url = reverse_lazy('blog:posts')
    fields = ['title', 'brief_content', 'content', 'image', 'is_published']
    success_message = "Post created"

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        superusers_emails = User.objects.filter(is_superuser=True).values_list('email').first()
        send_content_notification.apply_async((superusers_emails,
                                               'New Post Was Created', 'Post ID is {}'.format(post.id)))
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
        comment = form.save()
        superusers_emails = User.objects.filter(is_superuser=True).values_list('email').first()
        send_content_notification.apply_async((superusers_emails,
                                               'New Comment Was Created', 'Comment ID is {}'.format(comment.id)))
        return super(CreateCommentView, self).form_valid(form)


class EditPostView(SuccessMessageMixin, AuthorRequiredMixin, generic.UpdateView):
    model = Post
    fields = ["title", 'brief_content', "content", "image", "is_published"]
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
    model = Profile
    fields = ["full_name", "age", "about"]
    template_name = "blog/update_profile.html"
    login_url = reverse_lazy('blog:login')
    success_url = reverse_lazy("blog:posts")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateProfile, self).form_valid(form)


class ViewProfile(generic.DetailView):
    model = User
    context_object_name = 'entry'
    template_name = "blog/profile.html"


@method_decorator(cache_page(60), name='dispatch')
class PostView(generic.DetailView):
    model = Post
    context_object_name = 'entry'
    template_name = "blog/post.html"

    def get_object(self, queryset=None):
        post = Post.objects.get(id=self.kwargs["pk"])
        return post
