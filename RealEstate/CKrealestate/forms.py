from django import forms
from .models import Property, Property_Photo


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_title', 'property_description', 'property_price', 'property_id', 'home_type',
                  'neighborhood', 'status', 'price_range', 'property_street_address', 'property_city', 'property_state',
                  'property_zip_code', 'property_price', 'property_description', 'property_title', 'property_area',
                  'property_year_built', 'property_bedroom_count', 'property_bathroom_count', 'property_active',
                  ]
        labels = {
            'property_title': 'Title (100 characters)',
            'property_description': 'Description',
            'property_price': 'Price',
            'property_id': 'ID',
            'home_type': 'Home Type',
            'neighborhood': 'Neighborhood',
            'status': 'Status',
            'price_range': 'Price Range',
            'property_street_address': 'Street Address',
            'property_city': 'City',
            'property_state': 'State',
            'property_zip_code': 'ZIP Code',
            'property_area': 'Area Square Footage',
            'property_year_built': 'Year Built',
            'property_bedroom_count': 'Bedrooms',
            'property_bathroom_count': 'Bathrooms',
            'property_active': 'Active'
        }


class PropertyPhotoForm(forms.ModelForm):
    class Meta:
        model = Property_Photo
        fields = ['property_photo']