from django.conf import settings
from django.contrib import admin, auth
from django.contrib.auth import get_user_model

from user.models import Post, Comment, Profile


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'is_published']
    list_filter = ['is_published']
    search_fields = ['title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'username', 'comment', 'is_published']
    search_fields = ['username']


admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
