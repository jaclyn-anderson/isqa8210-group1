from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Contact, Property_Status, Property_Price_Range, Property_Neighborhood, Property_Type, \
    Search_Log
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm, ProfileForm, ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.http import HttpResponseRedirect


def home(request):
    featured = Property.objects.filter(property_featured=True, property_active=True)

    return render(request, 'home.html', {'featured': featured})


def featured(request, pk):
    featured = Property.objects.filter(property_featured=True, property_active=True)
    property_details = Property.objects.all()
    return render(request, 'featured.html', {'featured': featured})


def all_listings(request):
    property1 = Property.objects.filter(property_active=True).all().order_by('property_id')
    active_count = Property.objects.filter(property_active=True).count()
    paginator = Paginator(property1, 5)  # 1 items per page

    page = request.GET.get('page')

    try:
        property = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        property = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        property = paginator.page(paginator.num_pages)

    return render(request, 'all-listings.html', {'property': property, 'active_count': active_count})


def profile(request):
    contact = Contact.objects.all()
    success_message = None
    if request.GET.get('success_message') == 'true':
        success_message = 'Your email was sent successfully!'
        # Remove the 'success_message' query parameter from the URL
        return HttpResponseRedirect(request.path)

    return render(request, 'profile.html', {"contact": contact,
                                            "success_message": success_message})

  #  return render(request, 'profile.html', {"contact": contact})


def omahalinks(request):
    return render(request, 'omahalinks.html')


@login_required
def siteadminlanding(request):
    property1 = Property.objects.all().order_by('property_id')  # for all the records
    status = Property_Status.objects.all().order_by('property_status_name')
    paginator = Paginator(property1, 5)  # 1 items per page

    page = request.GET.get('page')
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

        return redirect(request.META.get('HTTP_REFERER', '/'))


    try:
        property = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        property = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        property = paginator.page(paginator.num_pages)

    return render(request, 'siteadminlanding.html', {'property': property, 'status': status})


@login_required
def add_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)

        if property_form.is_valid():
            property = property_form.save()
            return redirect('siteadminlanding')
    else:
        property_form = PropertyForm()

    return render(request, 'add-property.html', {
        'property_form': property_form
    })


@login_required
def update_profile(request):
    profile = Contact.objects.first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('siteadminlanding')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update-profile.html', {'form': form})


def contact_realtor(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        body = request.POST.get('body', '')

        # Perform basic validation
        if not (name and email and body and phone):
            return render(request, 'contact-realtor.html', {
                'error_message': 'Please fill in all required fields.',
                'name': name,
                'email': email,
                'phone': phone,
                'body': body
            })

        message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\n{body}'
        recipient_email = 'janderson052024@gmail.com'
        send_mail('CK Real Estate Contact Form Submission', message, email, [recipient_email])
        return render(request, 'profile.html', {'success_message': 'Your email was sent successfully!'})
    else:
        return render(request, 'contact-realtor.html')

def property_details(request, property_id):
    property_details = Property.objects.filter(property_id=property_id)
    return render(request, 'property-details.html', {'property_details': property_details})


def share_property(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    base_url = request.build_absolute_uri('/')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Retrieve property details
            property_title = property.property_title
            # Compose email message
            subject = f"{cd['name']} requests more information on {property_title}"
            message = f"Hi,\n\n{cd['name']} has requested more information about {property_title}.\n\n" \
                      f"Message: {cd['message']}\n\nContact them at: {cd['email']}"
            send_mail(subject, message, 'your_email@example.com', ['realtor_email@example.com'])
            return render(request, 'contact_success.html', {'property_title': property_title})
    else:
        form = ContactForm()

    return render(request, 'share-property.html',
                  dict(base_url=base_url, property_id=property_id, item=property, form=form))



def search_all_listings(request):
    global selected_price_range, selected_neighborhood, selected_home_type
    selected_home_type = None
    selected_neighborhood = None
    selected_price_range = None
    property_price_range = Property_Price_Range.objects.all().order_by('price_range_id')
    property_neighborhood = Property_Neighborhood.objects.all().order_by('neighborhood_name')
    property_home_type = Property_Type.objects.all().order_by('property_type_name')
    propertySearch = Property.objects.filter(property_active=True).all().order_by('property_id')

    if request.method == 'POST':
        allowed_filters = ['price_range_id', 'neighborhood_id', 'home_type_id']
        if request.POST.get('home_type_id'):
            selected_home_type = Property_Type.objects.filter(property_type_id=request.POST.get('home_type_id')).get()
        else:
            selected_home_type = None
        if request.POST.get('neighborhood_id'):
            selected_neighborhood = Property_Neighborhood.objects.filter(neighborhood_id=request.POST.get('neighborhood_id')).get()
        else:
            selected_neighborhood = None
        if request.POST.get('price_range_id'):
            selected_price_range = Property_Price_Range.objects.filter(price_range_id=request.POST.get('price_range_id')).get()
        else:
            selected_price_range = None
        search_log = Search_Log(search_home_type=selected_home_type,
                                search_neighborhood=selected_neighborhood,
                                search_price_range=selected_price_range)
        search_log.save()
        for f in allowed_filters:
            if request.POST.get(f):
                propertySearch = propertySearch.filter(**{f: request.POST.get(f)})

    active_count = propertySearch.filter(property_active=True).count()
    paginator = Paginator(propertySearch, 5)  # 1 items per page
    page = request.GET.get('page')
    try:
        property = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        property = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        property = paginator.page(paginator.num_pages)

    return render(request, 'search-all-listings.html', {'property': property, 'active_count': active_count,
                                                        'property_price_range': property_price_range,
                                                        'property_neighborhood': property_neighborhood,
                                                        'property_home_type': property_home_type,
                                                        'selected_price_range': selected_price_range,
                                                        'selected_neighborhood': selected_neighborhood,
                                                        'selected_home_type': selected_home_type
                                                        })
