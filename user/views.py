
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib import messages

from user import tasks
from user.form import PostCreateForm, CommentCreateForm, ContactUs
from user.models import Post, Comment


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
            subject = 'Post create'
            text = 'I create post'
            email = request.user.email
            tasks.send_mail.delay(subject, text, email)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['pk'], is_published=True)
        return context


def not_published_posts(request):
    posts = Post.objects.filter(author=request.user, is_published=False)
    return render(request, 'user/not_published_posts.html', {'posts': posts})


def comment_view(request, pk):
    form = CommentCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user
            obj.post_id = pk
            obj.save()
            url = request.build_absolute_uri(reverse('PostDetail', kwargs={'pk': pk}))
            subject = 'Comment create'
            text = 'I create comment ' + url
            email_sender = request.user.email
            email_receiver = obj.post.author.email  # захардкодил что получатель будет один,так как у поста 1 владелец
            tasks.send_mail_with_comments.delay(subject, text, email_sender, email_receiver)
            messages.add_message(request, messages.SUCCESS, 'Comment sent')
            return redirect('PostDetail', pk)
    return render(request, 'user/comment_view.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    post = Post.objects.filter(author=user.id, is_published=True)
    comments = Comment.objects.filter(username=request.user).aggregate(Count('id'))
    return render(request, 'user/profile.html', {'user': user, 'post': post, 'comments': comments['id__count']})


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


@login_required
def contact_us(request):
    data = dict()
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            data['form_is_valid'] = True
            email = request.user.email
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            tasks.send_mail.delay(subject, text, email)
            messages.add_message(request, messages.SUCCESS, 'Message sent')
        else:
            data['form_is_valid'] = False
    else:
        form = ContactUs()
    context = {'form': form}
    data['html_form'] = render_to_string('user/includes/feedback_create.html', context, request=request)
    return JsonResponse(data)
