from django.shortcuts import render, redirect
from .models import Property, Contact
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm


def home(request):
    featured = Property.objects.filter(property_featured=True)

    return render(request, 'home.html', {'featured': featured})


def all_listings(request):
    property = Property.objects.all().order_by('property_id')

    return render(request, 'all-listings.html', {'property': property})


def profile(request):
    contact = Contact.objects.all()

    return render(request, 'profile.html', {"contact": contact})


def omahalinks(request):
    return render(request, 'omahalinks.html')


@login_required
def siteadminlanding(request):
    property = Property.objects.all()  # for all the records

    return render(request, 'siteadminlanding.html', {'property': property})

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property_added')
    else:
        form = PropertyForm()

    return render(request, 'add_property.html', {'form': form})



