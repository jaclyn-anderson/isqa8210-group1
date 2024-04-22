from django import forms
from .models import Property, Contact


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
            'property_title': 'Property Title (max 100 characters)',
            'property_description': 'Description (max 800 characters)',
            'property_price': 'Price',
            'property_id': 'ID',
            'home_type': 'Home Type',
            'neighborhood': 'Neighborhood',
            'status': 'Status',
            'price_range': 'Price Range',
            'property_street_address': 'Street Address',
            'property_city': 'City',
            'property_state': 'State',
            'property_zip_code': 'Zip Code',
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
            'property_description': forms.Textarea(attrs={'rows': 5, 'cols': 140}),
            'property_street_address': forms.TextInput(attrs={'style': 'width: 300px;'}),
            'property_state': forms.TextInput(attrs={'style': 'width: 30px;'}),
            'property_zip_code': forms.TextInput(attrs={'style': 'width: 80px;'}),
            'property_title': forms.TextInput(attrs={'style': 'width: 700px;'}),
            'property_area': forms.NumberInput(attrs={'style': 'width: 100px;'}),
            'property_year_built': forms.NumberInput(attrs={'style': 'width: 100px;'}),
            'property_bedroom_count':  forms.NumberInput(attrs={'style': 'width: 50px;'}),
            'property_bathroom_count': forms.NumberInput(attrs={'style': 'width: 50px;'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_first_name', 'contact_last_name', 'contact_phone', 'contact_email',
                  'contact_office_street_address', 'contact_office_city', 'contact_office_state',
                  'contact_office_zip_code', 'contact_website_link', 'contact_profile_description',
                  'contact_profile_image',
                  ]

        labels = {'contact_first_name': 'First Name',
                  'contact_last_name': 'Last Name',
                  'contact_phone': 'Phone',
                  'contact_email': 'Email',
                  'contact_office_street_address': 'Office Street Address',
                  'contact_office_city': 'Office City',
                  'contact_office_state': 'Office State',
                  'contact_office_zip_code': 'Office Zip Code',
                  'contact_website_link': 'Office Website Link',
                  'contact_profile_description': 'Profile Bio',
                  'contact_profile_image': 'Profile Image'
                  }

        widgets = {
            'contact_profile_description': forms.Textarea(attrs={'rows': 5, 'cols': 140}),
            'contact_website_link': forms.TextInput(attrs={'style': 'width: 700px;'}),  # Adjust width as needed
        }


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)
    phone = forms.CharField(label='Phone')
    property_id = forms.IntegerField(widget=forms.HiddenInput())
