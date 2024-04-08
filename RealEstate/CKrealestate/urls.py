from django.urls import path
from .views import home, profile, siteadminlanding, omahalinks, all_listings, add_property

urlpatterns = [
    path('', home, name='home'),
    path('profile', profile, name='profile'),
    path('siteadminlanding', siteadminlanding, name='siteadminlanding'),
    path('omahalinks', omahalinks, name='omahalinks'),
    path('all_listings', all_listings, name='all_listings'),
    path('add_property', add_property, name='add_property'),

]
