from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


@login_required(login_url='home')
def siteadminlanding(request):
    return render(request, 'siteadminlanding.html')


def profile(request):
    return render(request, 'profile.html')
    