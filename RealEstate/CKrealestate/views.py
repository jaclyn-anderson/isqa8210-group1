from django.shortcuts import render, redirect
from .models import Property, Contact
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm, PropertyPhotoForm


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
    if request.method == 'POST':
        # Get the ID of the record being updated
        record_id = request.POST.get('property_id')

        # Retrieve the specific record
        obj = Property.objects.get(property_id=record_id)
        # Update only if the form is submitted
        if 'price' in request.POST:
            obj.property_price = request.POST.get('price')
        if 'status' in request.POST:
            obj.status = request.POST.get('status')
        if 'featured' in request.POST:
            if request.POST.get('featured') == 'on':
                obj.property_featured = True
            else:
                obj.property_featured = False

        # Mark other fields as read-only
        obj.editable = False
        obj.save()
        return redirect('siteadminlanding')

    return render(request, 'siteadminlanding.html', {'property': property})


def add_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        photo_form = PropertyPhotoForm(request.POST, request.FILES)
        if property_form.is_valid() and photo_form.is_valid():
            property = property_form.save()
            photo = photo_form.save(commit=False)
            photo.property = property
            photo.save()
            return redirect('property-details', property_id=property.property_id)
    else:
        property_form = PropertyForm()
        photo_form = PropertyPhotoForm()

    return render(request, 'add-property.html', {
        'property_form': property_form,
        'photo_form': photo_form
    })



