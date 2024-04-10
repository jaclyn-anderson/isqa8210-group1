from django.shortcuts import render, redirect
from .models import Property, Contact, Property_Status
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
    status = Property_Status.objects.all().order_by('property_status_name')

    if request.method == 'POST':
        # Get the ID of the record being updated
        record_id = request.POST.get('property_id')

        # Retrieve the specific record
        obj = Property.objects.get(property_id=record_id)
        # Update only if the form is submitted
        if 'price' in request.POST:
            obj.property_price = request.POST.get('price').replace(',', '')
        if 'status' in request.POST:
            status_id = request.POST.get('status')
            status = Property_Status.objects.get(property_status_id=status_id)
            obj.status = status
        if 'featured' in request.POST:
            Property.objects.exclude(property_id=record_id).update(property_featured=False)
            obj.property_featured = 'True'
        else:
            obj.property_featured = 'False'
        if 'active' in request.POST:
            obj.property_active = 'True'
        else:
            obj.property_active = 'False'

        # Mark other fields as read-only
        obj.editable = False
        obj.save()
        return redirect('siteadminlanding')

    return render(request, 'siteadminlanding.html', {'property': property, 'status': status})


def add_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)

        if property_form.is_valid():
            property = property_form.save()
            return redirect('property-details', property_id=property.property_id)
    else:
        property_form = PropertyForm()

    return render(request, 'add-property.html', {
        'property_form': property_form
    })



