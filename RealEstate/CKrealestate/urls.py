from django.urls import path
from .views import home, profile, siteadminlanding

urlpatterns = [
    path('', home, name='home'),
    path('profile', profile, name='profile'),
    path('siteadminlanding', siteadminlanding, name='siteadminlanding'),

]
