from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=230, default='Post')
    text = models.TextField()
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='img')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=35)
    comment = models.CharField(max_length=120)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.comment


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
