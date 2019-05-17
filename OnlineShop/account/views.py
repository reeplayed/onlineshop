from django.shortcuts import render, redirect
from .forms import UserRegistration


def login(request):
    return render(request, 'account/login.html')


def registration(request):

    form = UserRegistration(request.POST or None)
    if form.is_valid():
        form = UserRegistration(request.POST)
        form.save()
        return redirect('login')
    context = {
        'form': form
    }

    return render(request, 'account/registration.html', context)


def home(request):
    return render(request, 'account/base.html')


