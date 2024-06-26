from django.urls import path
from .views import (home, profile, siteadminlanding, omahalinks, all_listings, add_property, property_details,
                    share_property, update_profile, contact_realtor,  search_all_listings, contact_success, siteadminreports)

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('update_profile', update_profile, name='update_profile'),
    path('contact-realtor', contact_realtor, name='contact_realtor'),
    path('contact-success', contact_success, name='contact_success'),
    path('siteadminlanding', siteadminlanding, name='siteadminlanding'),
    path('omahalinks', omahalinks, name='omahalinks'),
    path('all_listings', all_listings, name='all_listings'),
    path('add_property', add_property, name='add_property'),
    path('property-details/<int:property_id>/', property_details, name='property_details'),
    path('share_property/<int:property_id>/', share_property, name='share_property'),
    path('search_all_listings', search_all_listings, name='search_all_listings'),
    path('siteadminreports', siteadminreports, name='siteadminreports'),
]
