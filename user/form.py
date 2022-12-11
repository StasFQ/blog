from django import forms
from django.contrib.auth.models import User
from user.models import Post, Comment, Profile


class PostCreateForm(forms.ModelForm):
    title = forms.CharField()
    short_description = forms.CharField()
    text = forms.Textarea()

    class Meta:
        model = Post
        fields = ['title', 'short_description', 'text', 'is_published', 'image']


class CommentCreateForm(forms.ModelForm):
    comment = forms.CharField()

    class Meta:
        model = Comment
        fields = ['comment']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class ContactUs(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=230)
    text = forms.CharField(widget=forms.Textarea)
