
from django.urls import path

from user.views import create_posts, PostList, Profile, PostDetail, comment_view

urlpatterns = [
    path('create_post/', create_posts, name='create_posts'),
    path('post_list/', PostList.as_view(), name='PostList'),
    path('profile/<int:pk>', Profile.as_view(), name='Profile'),
    path('post_detail/<int:pk>', PostDetail.as_view(), name='PostDetail'),
    path('comment/<int:pk>', comment_view, name='comment_view')
]
