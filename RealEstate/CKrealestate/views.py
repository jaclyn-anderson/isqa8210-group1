from django.shortcuts import render
from .models import Property
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def all_listings(request):
    property = Property.objects.all()

    return render(request, 'all-listings.html', {'property': property})


def profile(request):
    return render(request, 'profile.html')


def omahalinks(request):
    return render(request, 'omahalinks.html')


@login_required
def siteadminlanding(request):
    property = Property.objects.all()  # for all the records

    return render(request, 'siteadminlanding.html', {'property': property})



