from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from django.core.mail import send_mail
from user.form import PostCreateForm, CommentCreateForm
from user.models import Post, Comment

User = settings.AUTH_USER_MODEL


class PostList(generic.ListView):
    template_name = 'user/post_list.html'
    model = Post
    queryset = Post.objects.filter(is_published=True)
    context_object_name = 'Post'


@login_required
def create_posts(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            send_mail('Post Create', 'Someone create post', 'admin1@example.com', ['admin@example.com'])
            return redirect('PostList')
    return render(request, 'user/create_post.html', {'form': form})


class PostDetail(generic.DetailView):
    template_name = 'user/post.html'
    model = Post


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
            return redirect('PostList')
    return render(request, 'user/comment_view.html', {'form': form})


class Profile(generic.DetailView):
    model = Post
    template_name = 'user/profile.html'

    def get_queryset(self):
        return Post.objects.filter()




