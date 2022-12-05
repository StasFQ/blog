from django import forms
from django.contrib.auth.models import User

from user.models import Post, Comment


class PostCreateForm(forms.ModelForm):
    title = forms.CharField()
    text = forms.Textarea()

    class Meta:
        model = Post
        fields = ['title', 'text', 'is_published']


class CommentCreateForm(forms.ModelForm):
    comment = forms.CharField()

    class Meta:
        model = Comment
        fields = ['comment']
