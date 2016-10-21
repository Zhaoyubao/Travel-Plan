from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User

def index(request):
    if 'user' in request.session:
        messages.success(request, 'Welcome back!')
        return redirect(reverse('travel:index'))
    return render(request, 'login_register/index.html')

def register(request):
    if request.method == 'POST':
        result = User.objects.validate_reg(request.POST)
        if result[0]:
            request.session['user'] = result[1].id
            messages.success(request, 'Successfully registered!')
            return redirect(reverse('travel:index'))
        print_messages(request, result[1])
    return redirect(reverse('users:index'))

def login(request):
    if request.method == 'POST':
        result = User.objects.validate_log(request.POST)
        if result[0]:
            request.session['user'] = result[1].id
            messages.success(request, 'Successfully logged in!')
            return redirect(reverse('travel:index'))
        print_messages(request, result[1])
    return redirect(reverse('users:index'))

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect(reverse('users:index'))

def print_messages(request, error_list):
     for error, tag in error_list:
        messages.error(request, error, extra_tags=tag)
