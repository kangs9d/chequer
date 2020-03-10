from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from user.forms import UserForm
from django.contrib import messages


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('main')
        else:
            messages.info(request, 'Write proper e-Mail, or this user name is already taken.')
            return HttpResponseRedirect('/user/signup')
    else:
        return render(request, 'user/signup.html')


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.info(request, 'User is not identified. Please give us proper ID or password.')
            return HttpResponseRedirect('/user/signin')
        return redirect('main')
    else:
        return render(request, 'user/signin.html')


def log_out(request):
    logout(request)
    return redirect('main')
