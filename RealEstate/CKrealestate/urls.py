from django.urls import path
from .views import home, siteadminlanding

urlpatterns = [
    path('', home, name='home'),
    path('siteadminlanding', siteadminlanding, name='siteadminlanding')

]
