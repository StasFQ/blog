from django.urls import path

from accounts.views import RegisterFormPage

appname = 'accounts'
urlpatterns = [
    path('register/', RegisterFormPage.as_view(), name='RegisterFormPage'),
]
