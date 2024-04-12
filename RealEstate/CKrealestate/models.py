from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver



class Property_Type(models.Model):
    property_type_id = models.AutoField(primary_key=True, unique=True)
    property_type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.property_type_name


class Property_Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True, unique=True)
    neighborhood_name = models.CharField(max_length=100)

    def __str__(self):
        return self.neighborhood_name


class Property_Status(models.Model):
    property_status_id = models.AutoField(primary_key=True)
    property_status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.property_status_name


class Property_Price_Range(models.Model):
    price_range_id = models.AutoField(primary_key=True, unique=True)
    price_range_value = models.CharField(max_length=100)

    def __str__(self):
        return self.price_range_value


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Property(models.Model):
    property_id = models.AutoField(primary_key=True, unique=True)
    home_type = models.ForeignKey(Property_Type, on_delete=models.CASCADE, blank=False, null=False)
    neighborhood = models.ForeignKey(Property_Neighborhood, on_delete=models.CASCADE, blank=False, null=False)
    status = models.ForeignKey(Property_Status, on_delete=models.CASCADE, blank=False, null=False)
    price_range = models.ForeignKey(Property_Price_Range, on_delete=models.CASCADE,  blank=False, null=False)
    property_street_address = models.CharField(max_length=100,  blank=False, null=False)
    property_city = models.CharField(max_length=100,  blank=False, null=False)
    property_state = models.CharField(max_length=2,  blank=False, null=False)
    property_zip_code = models.CharField(max_length=10, default='00000',  blank=False, null=False)
    property_price = models.BigIntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    property_description = models.TextField(max_length=800,  blank=False, null=False)
    property_title = models.CharField(max_length=200,  blank=False, null=False)
    property_area = models.PositiveIntegerField(null=False, blank=False)
    property_year_built = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1900), max_value_current_year])
    property_bedroom_count = models.PositiveIntegerField(null=False, blank=False, default=0)
    property_bathroom_count = models.PositiveIntegerField(null=False, blank=False, default=0)
    property_featured = models.BooleanField(default=False)
    property_active = models.BooleanField(default=True)
    property_photo1 = models.ImageField(upload_to='uploads/')
    property_photo2 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    property_photo3 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    property_photo4 = models.ImageField(upload_to='uploads/', null=True, blank=True)

    def __int__(self):
        return self.property_id


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True, unique=True)
    contact_first_name = models.CharField(max_length=100)
    contact_last_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20,default='(402)000-0000')
    contact_email = models.EmailField
    contact_website_link = models.CharField(max_length=200)
    contact_office_street_address = models.CharField(max_length=100)
    contact_office_city = models.CharField(max_length=100)
    contact_office_state = models.CharField(max_length=2)
    contact_office_zip_code = models.CharField(max_length=10, default='00000')
    contact_profile_image = models.ImageField(upload_to='uploads/')
    contact_profile_description = models.TextField(max_length=800)


class Search_Log(models.Model):
    search_log_id = models.AutoField(primary_key=True, unique=True)
    search_date = models.DateField(auto_now_add=True)
    search_home_type = models.ForeignKey(Property_Type, on_delete=models.CASCADE)
    search_neighborhood = models.ForeignKey(Property_Neighborhood, on_delete=models.CASCADE)
    search_price_range = models.ForeignKey(Property_Price_Range, on_delete=models.CASCADE)
















