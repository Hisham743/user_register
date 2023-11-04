from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm


def home(request):
    return render(request, 'base/home.html')


def register(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already signed in. To register a new account, please logout.')
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, 'Signed Up Successfully!')
            return redirect(reverse('profile', args=[new_user.id]))
    else:
        form = RegisterForm()

    context = {'form': form,
               'page': 'register'}
    return render(request, 'base/register_login.html', context)


def login_(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already signed in. To login with another account, please logout.')
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {data["username"]}!')
                return redirect(reverse('profile', args=[user.id]))
            else:
                messages.error(request, f'Login Failed, try again.')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'base/register_login.html', context)


def logout_(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse('profile', args=[user.id]))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_': user
    }
    return render(request, 'base/profile.html', context)
