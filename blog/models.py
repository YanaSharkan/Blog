from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField()
    is_published = models.BooleanField()
    is_moderated = models.BooleanField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_moderated = models.BooleanField()

    def __str__(self):
        return self.content
