from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import send_mail
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.views.generic.list import MultipleObjectMixin
from django.contrib import messages

from accounts.forms import LoginForm
from user.form import PostCreateForm, CommentCreateForm, UpdateUserForm, UpdateProfileForm, ContactUs
from user.models import Post, Comment, Profile

#User = settings.AUTH_USER_MODEL


class PostList(generic.ListView):
    template_name = 'user/post_list.html'
    model = Post
    queryset = Post.objects.filter(is_published=True)
    context_object_name = 'Post'
    paginate_by = 5


@login_required
def create_posts(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            send_mail('Post Create', 'Someone create post', 'admin1@example.com', ['admin@example.com'])
            messages.add_message(request, messages.SUCCESS, 'Post Create!')
            return redirect('PostList')
    return render(request, 'user/create_post.html', {'form': form})


@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostCreateForm(instance=post)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Post Update!')
            return redirect('Profile')
    else:
        form = PostCreateForm(instance=post)
    return render(request, 'user/update_post.html', {'form': form})


class PostDetail(generic.DetailView):
    template_name = 'user/post.html'
    model = Post


def not_published_posts(request):
    posts = Post.objects.filter(author=request.user, is_published=False)
    return render(request, 'user/not_published_posts.html', {'posts': posts})


def comment_view(request, pk):
    form = CommentCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            username = request.user
            comment = form.cleaned_data['comment']
            Comment.objects.create(username=username, comment=comment, post_id=pk)
            send_mail('Comment Create', 'Someone leave comment', 'admin@example.com', ['admin@example.com'])
            send_mail('Commet', 'Someone leave comment undr your post', 'admin@example.com', [])
            messages.add_message(request, messages.SUCCESS, 'Comment sent')
            return redirect('PostDetail', pk)
    return render(request, 'user/comment_view.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    post = Post.objects.filter(author=user.id, is_published=True)
    return render(request, 'user/profile.html', {'user': user, 'post': post})


def public_profile(request, pk):
    user_profile = User.objects.get(id=pk)
    post = Post.objects.filter(author=user_profile.id, is_published=True)
    return render(request, 'user/public_profile.html', {'profile': user_profile, 'post': post})


class UpdateData(UpdateView):
    template_name = 'user/update_data.html'
    model = User
    fields = ['username', 'email']
    success_url = reverse_lazy('Profile')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


def contact_us(request):
    form = ContactUs()
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            send_mail(subject, text, email, ['admin@example.com'])
            messages.add_message(request, messages.SUCCESS, 'Message sent')
            return redirect('PostList')
    return render(request, 'registration/contact_us.html', {'form': form})
