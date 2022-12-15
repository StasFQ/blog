from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from user.views import create_posts, PostList, PostDetail, comment_view, profile, update_post, UpdateData, \
    public_profile, not_published_posts, contact_us

urlpatterns = [
    path('create_post/', create_posts, name='create_posts'),
    path('post_list/', PostList.as_view(), name='PostList'),
    path('profile/', profile, name='Profile'),
    path('post_detail/<int:pk>', PostDetail.as_view(), name='PostDetail'),
    path('comment/<int:pk>', comment_view, name='comment_view'),
    path('update_post/<int:post_id>', update_post, name='update_post'),
    path('update_data/', UpdateData.as_view(), name='UpdateData'),
    path('public_profile/<int:pk>', public_profile, name='public_profile'),
    path('not_published_posts/', not_published_posts, name='not_published_posts'),
    path('contact_us/', contact_us, name='contact_us')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
