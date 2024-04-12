from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_title', 'property_description', 'property_price', 'property_id', 'home_type',
                  'neighborhood', 'status', 'price_range', 'property_street_address', 'property_city', 'property_state',
                  'property_zip_code', 'property_price', 'property_description', 'property_title', 'property_area',
                  'property_year_built', 'property_bedroom_count', 'property_bathroom_count', 'property_active',
                  'property_photo1', 'property_photo2', 'property_photo3', 'property_photo4',
                  ]
        labels = {
            'property_title': 'Property Title (100 characters)',
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
            'property_active': 'Active',
            'property_photo1': 'Photo 1',
            'property_photo2': 'Photo 2',
            'property_photo3': 'Photo 3',
            'property_photo4': 'Photo 4'
        }
        widgets = {
            'property_description': forms.Textarea(attrs={'rows': 5, 'cols': 150}),
            'property_title': forms.TextInput(attrs={'style': 'width: 700px;'}),  # Adjust width as neede
        }
