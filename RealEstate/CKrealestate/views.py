from django.shortcuts import render, redirect
from .models import Property, Contact, Property_Status, Property_Price_Range, Property_Neighborhood, Property_Type, \
    Search_Log
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    featured = Property.objects.filter(property_featured=True, property_active=True)

    return render(request, 'home.html', {'featured': featured})


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

    return render(request, 'profile.html', {"contact": contact})


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
