from django.shortcuts import render, redirect
from .models import Property, Contact, Property_Status
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm, ProfileForm
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
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('siteadminlanding')
    else:
        form = ProfileForm()

    return render(request, 'update-profile.html', {'form': form})


def contact_realtor(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')

        # Perform basic validation
        if not (name and email and subject):
            return render(request, 'contact-realtor.html', {'error_message': 'Please fill in all required fields.'})

        message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\n{subject}'
        recipient_email = 'janderson052024@gmail.com'
        send_mail('Contact Form Submission', message, email, [recipient_email])
        return render(request, 'profile.html', {'success_message': 'Your email was sent successfully!'})
    else:
        return render(request, 'contact-realtor.html')

def property_details(request, property_id):
    property_details = Property.objects.filter(property_id=property_id)
    return render(request, 'property-details.html', {'property_details': property_details})


def share_property(request, pk):
    # Retrieve property post by id
    property = get_object_or_404(Post, pk=pk, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            property_url = request.build_absolute_uri(
                property.get_absolute_url())
            subject = f"{cd['name']} requests more information on " \
                      f"{property.title}"
            message = f"Read {property.title} at {property_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, {cd['email_from']},
                      [cd['email_to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share-property.html', {'property': property,
                                                    'form': form,
                                                    'sent': sent})






