from django.urls import path
from .views import home, profile, siteadminlanding, omahalinks, all_listings, add_property, property_details, share_property

urlpatterns = [
    path('', home, name='home'),
    path('profile', profile, name='profile'),
    path('siteadminlanding', siteadminlanding, name='siteadminlanding'),
    path('omahalinks', omahalinks, name='omahalinks'),
    path('all_listings', all_listings, name='all_listings'),
    path('add_property', add_property, name='add_property'),
    path('property_details', property_details, name='property_details'),
    path('share_property', share_property, name='share_property'),
]
