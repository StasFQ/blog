from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import LoginForm, RegisterForm


class RegisterFormPage(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('RegisterFormPage')

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(RegisterFormPage, self).form_valid(form)


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login_page')
            else:
                return 'Fail'
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('RegisterFormPage')





