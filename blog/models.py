from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    brief_content = models.TextField(null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='comments/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    is_moderated = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    about = models.TextField(null=True)
    full_name = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.full_name
