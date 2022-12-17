
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib import messages


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


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk, is_published=True)
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'user/post.html', {'contacts': contacts, 'post': post})


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
        else:
            data['form_is_valid'] = False
    else:
        form = ContactUs()
    context = {'form': form}
    data['html_form'] = render_to_string('user/includes/feedback_create.html', context, request=request)
    return JsonResponse(data)
