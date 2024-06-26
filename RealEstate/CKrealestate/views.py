from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Contact, Property_Status, Property_Price_Range, Property_Neighborhood, Property_Type, \
    Search_Log
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm, ProfileForm, ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.db.models import Count, Sum


def home(request):
    featured = Property.objects.filter(property_featured=True, property_active=True)

    return render(request, 'home.html', {'featured': featured})


def all_listings(request):
    global prev_sort, prev_sortDir

    sort = request.GET.get('qSortBy')
    sortDir = request.GET.get('qSortDir')
    if sort is not None:
        prev_sort = sort
        prev_sortDir = sortDir
    else:
        prev_sort = globals().get("prev_sort", "property_id")
        prev_sortDir = globals().get("prev_sortDir", "asc")

    property1 = Property.objects.filter(property_active=True).all().order_by(prev_sort)
    active_count = Property.objects.filter(property_active=True).count()

    if sort is not None:
        property1 = property1.order_by(sort)
    if sortDir == 'desc' or prev_sortDir == 'desc':
        property1 = property1.reverse()
    else:
        property1 = property1.all()
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


def omahalinks(request):
    return render(request, 'omahalinks.html')


@login_required
def siteadminlanding(request):
    global prev_sort, prev_sortDir

    status = Property_Status.objects.all().order_by('property_status_name')
    sort = request.GET.get('qSortBy')
    sortDir = request.GET.get('qSortDir')
    if sort is not None:
        prev_sort = sort
        prev_sortDir = sortDir
    else:
        prev_sort = globals().get("prev_sort", "property_id")
        prev_sortDir = globals().get("prev_sortDir", "asc")

    property1 = Property.objects.all().order_by(prev_sort)  # for all the records
    if sort is not None:
        property1 = property1.order_by(sort)
    if sortDir == 'desc' or prev_sortDir == 'desc':
        property1 = property1.reverse()
    else:
        property1 = property1.all()
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
            # Convert integer_to_check to int if needed
            price_to_check = int(obj.property_price)

            # Get all the price ranges from the database
            price_ranges = Property_Price_Range.objects.all()

            # Check if the integer falls within any of the existing price ranges
            for price_range in price_ranges:
                min_price, max_price = map(lambda x: int(x.replace(',', '').replace('+', '')), price_range.price_range_value.split(' - '))
                if min_price <= price_to_check <= max_price:
                    # Integer falls within this price range, get the price_range_id
                    price_range_id = Property_Price_Range.objects.get(price_range_id=price_range.price_range_id)
                    obj.price_range = price_range_id
                    break
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


def profile(request):
    contact = Contact.objects.all()

    return render(request, 'profile.html', {"contact": contact})


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

        message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage: {body}'
        recipient_email = 'msmwillschoolacct@gmail.com'
        send_mail('CK Real Estate Contact Form Submission', message, email, [recipient_email])
        return render(request, 'contact_success.html')
    else:
        return render(request, 'contact-realtor.html')

def contact_success(request):
    return render(request, 'contact_success.html')


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
            subject = f"{cd['name']}, requests more information on {property_title}"
            message = f"Hi,\n\n{cd['name']} has requested more information about Property Link: {base_url}property-details/{property_id} - {property_title}.\n\n" \
                      f"Message: {cd['message']}\n\nContact {cd['name']} at email: {cd['email']} or phone: {cd['phone']}."
            send_mail(subject, message, 'your_email@example.com', ['msmwillschoolacct@gmail.com'])
            return render(request, 'contact_success.html', {'property_title': property_title})
    else:
        form = ContactForm()

    return render(request, 'share-property.html',
                  dict(base_url=base_url, property_id=property_id, item=property, form=form))


def search_all_listings(request):
    global selected_price_range, selected_neighborhood, selected_home_type, prev_sort, prev_sortDir
    property_price_range = Property_Price_Range.objects.all().order_by('price_range_id')
    property_neighborhood = Property_Neighborhood.objects.all().order_by('neighborhood_name')
    property_home_type = Property_Type.objects.all().order_by('property_type_name')
    sort = request.GET.get('qSortBy')
    sortDir = request.GET.get('qSortDir')
    if sort is not None:
        prev_sort = sort
        prev_sortDir = sortDir
    else:
        prev_sort = globals().get("prev_sort", "property_id")
        prev_sortDir = globals().get("prev_sortDir", "asc")
        selected_home_type = None
        selected_neighborhood = None
        selected_price_range = None

    propertySearch = Property.objects.filter(property_active=True).all().order_by(prev_sort)
    if selected_home_type is not None:
        propertySearch = propertySearch.filter(home_type=selected_home_type)
    if selected_neighborhood is not None:
        propertySearch = propertySearch.filter(neighborhood=selected_neighborhood)
    if selected_price_range is not None:
        propertySearch = propertySearch.filter(price_range=selected_price_range)
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

    if sort is not None:
        propertySearch = propertySearch.order_by(sort)

    if sortDir == 'desc' or prev_sortDir == 'desc':
        propertySearch = propertySearch.reverse()
    else:
        propertySearch = propertySearch.all()

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

@login_required()
def siteadminreports(request):
    property_price_range = Property_Price_Range.objects.all()
    property_neighborhood = Property_Neighborhood.objects.all()
    property_home_type = Property_Type.objects.all()
    property = Property.objects.all()
    selected_month_year = request.GET.get('selected_month_year')
    search_log_count = 0


    if selected_month_year:
        selected_date = datetime.strptime(selected_month_year, '%Y-%m')
        year = selected_date.year
        month = selected_date.month
        start_date = datetime(year, month, 1).date()
        end_date = (datetime(year, month, 1) + timedelta(days=32)).date()

        search_logs = Search_Log.objects.filter(search_date__gte=start_date, search_date__lt=end_date)

        search_log_count = search_logs.count()

        price_range_counts = search_logs.values('search_price_range__price_range_value').annotate(count=Count('search_price_range__price_range_value')).order_by('search_price_range')
        home_type_counts = Search_Log.objects.values('search_home_type__property_type_name').annotate(count=Count('search_home_type__property_type_name')).order_by('search_home_type')
        neighborhood_counts = Search_Log.objects.values('search_neighborhood__neighborhood_name').annotate(count=Count('search_neighborhood__neighborhood_name')).order_by('search_neighborhood')

        # Only calculate counts if there are search logs
    if search_log_count > 0:
       price_range_counts = search_logs.values('search_price_range__price_range_value').annotate(
       count=Count('search_price_range__price_range_value')).order_by('search_price_range')
       home_type_counts = search_logs.values('search_home_type__property_type_name').annotate(
       count=Count('search_home_type__property_type_name')).order_by('search_home_type')
       neighborhood_counts = search_logs.values('search_neighborhood__neighborhood_name').annotate(
       count=Count('search_neighborhood__neighborhood_name')).order_by('search_neighborhood')
       # Calculate subtotal counts for each category
       subtotal_price_range_count = price_range_counts.aggregate(subtotal=Sum('count'))[
           'subtotal'] if search_log_count > 0 else 0
       subtotal_home_type_count = home_type_counts.aggregate(subtotal=Sum('count'))[
           'subtotal'] if search_log_count > 0 else 0
       subtotal_neighborhood_count = neighborhood_counts.aggregate(subtotal=Sum('count'))[
           'subtotal'] if search_log_count > 0 else 0
       # Calculate overall total count
       overall_total_count = subtotal_price_range_count + subtotal_home_type_count + subtotal_neighborhood_count

       return render(request, 'siteadminreports.html', {
            'property': property,
            'property_price_range': property_price_range,
            'property_neighborhood': property_neighborhood,
            'property_home_type': property_home_type,
            'search_logs': search_logs,
            'price_range_counts': price_range_counts,
            'home_type_counts': home_type_counts,
            'neighborhood_counts': neighborhood_counts,
            'selected_month_year': selected_month_year,
            'search_log_count': search_log_count,
            'subtotal_price_range_count': subtotal_price_range_count,
            'subtotal_home_type_count': subtotal_home_type_count,
            'subtotal_neighborhood_count': subtotal_neighborhood_count,
            'overall_total_count': overall_total_count,
        })
    else:
        if selected_month_year:
            message = "Please try again, no results for your inquiry for: " + str(month) + "/" + str(year) + "!"
        else:
            message = "Please select Month and Year!"
        return render(request, 'siteadminreports.html', {'message': message})

