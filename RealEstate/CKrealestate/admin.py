from .models import Property_Status, Property_Type, Property_Neighborhood, Property_Price_Range
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
    search_fields =('neighborhood_name', )


@admin.register(Property_Price_Range)
class Property_Price_RangeAdmin(admin.ModelAdmin):
    list_display = ('price_range_id', 'price_range_value', )
    search_fields = ('price_range_value', )
