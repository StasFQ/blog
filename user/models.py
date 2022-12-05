from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=35)
    comment = models.CharField(max_length=120)

    def __str__(self):
        return self.comment



