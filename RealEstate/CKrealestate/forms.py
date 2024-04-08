from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_title', 'property_description', 'property_price', 'property_id', 'home_type',
                  'neighborhood', 'status', 'price_range', 'property_street_address', 'property_city', 'property_state',
                  'property_zip_code', 'property_price', 'property_description', 'property_title', 'property_area',
                  'property_year_built', 'property_bedroom_count', 'property_bathroom_count','property_featured',
                  'property_active'
                  ]
