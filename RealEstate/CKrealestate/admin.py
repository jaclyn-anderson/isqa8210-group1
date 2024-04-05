from .models import Property_Status, Property_Type, Property_Neighborhood, Property_Price_Range, Property, Contact, Property_Photo
from django.contrib import admin


@admin.register(Property_Status)
class Property_StatusAdmin(admin.ModelAdmin):
    list_display = ('property_status_id', 'property_status_name', )
    search_fields = ('property_status_name', )


@admin.register(Property_Type)
class Property_TypeAdmin(admin.ModelAdmin):
    list_display = ('property_type_id', 'property_type_name', )
    search_fields = ('property_type_name', )


@admin.register(Property_Neighborhood)
class Property_NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('neighborhood_id', 'neighborhood_name', )
    search_fields = ('neighborhood_name', )


@admin.register(Property_Price_Range)
class Property_Price_RangeAdmin(admin.ModelAdmin):
    list_display = ('price_range_id', 'price_range_value', )
    search_fields = ('price_range_value', )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'home_type', 'neighborhood', 'status', 'price_range', 'property_street_address',
                    'property_city', 'property_state', 'property_zip_code', 'property_price', 'property_description',
                    'property_title', 'property_area', 'property_year_built', 'property_bedroom_count',
                    'property_bathroom_count', 'property_featured', 'property_active', )
    search_fields = ('property_id', 'property_title', )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'contact_first_name', 'contact_last_name', 'contact_email', 'contact_phone',
                    'contact_office_street_address', 'contact_office_city', 'contact_office_state', 'contact_office_zip_code',
                    'contact_website_link', 'contact_profile_description', 'contact_profile_image', )


@admin.register(Property_Photo)
class Property_PhotoAdmin(admin.ModelAdmin):
    list_display = ('property_photo_id', 'property_photo', 'property')
    search_fields = ('property_photo_id', 'property', )

