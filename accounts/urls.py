from django.urls import path

from accounts.views import login_page, RegisterFormPage, logout_view, create_posts

appname = 'accounts'
urlpatterns = [
    path('register/', RegisterFormPage.as_view(), name='RegisterFormPage'),
]
