from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


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
    home_type = models.ForeignKey(Property_Type, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Property_Neighborhood, on_delete=models.CASCADE)
    status = models.ForeignKey(Property_Status, on_delete=models.CASCADE)
    price_range = models.ForeignKey(Property_Price_Range, on_delete=models.CASCADE)
    property_street_address = models.CharField(max_length=100)
    property_city = models.CharField(max_length=100)
    property_state = models.CharField(max_length=2)
    property_zip_code = models.CharField(max_length=10, default='00000')
    property_price = models.DecimalField(max_digits=12, decimal_places=0)
    property_description = models.TextField(max_length=800)
    property_title = models.CharField(max_length=200)
    property_area = models.PositiveIntegerField(max_length=9)
    property_year_built = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1900), max_value_current_year])
    property_bedroom_count = models.PositiveIntegerField(max_length=2)
    property_bathroom_count = models.PositiveIntegerField(max_length=2)
    property_featured = models.BooleanField(default=False)
    property_active = models.BooleanField(default=True)

    def __int__(self):
        return self.property_id

    # If the property is being marked as featured, ensure no other property is featured
    def save(self, *args, **kwargs):
        if self.property_featured:
            # If property_feature is being set to True,
            # set all other properties' property_feature to False
            Property.objects.exclude(property_id=self.property_id).update(property_featured=False)
            super(Property, self).save(*args, **kwargs)
        else:
            # If property_feature is being set to False,
            # only update itself
            Property.objects.get(property_id=self.property_id).update(property_featured=False)
            super(Property, self).save(*args, **kwargs)


class Property_Photo(models.Model):
    property_photo_id = models.AutoField(primary_key=True, unique=True)
    property_photo = models.ImageField(upload_to='static/images')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)


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
    contact_profile_image = models.ImageField(upload_to='static/images')
    contact_profile_description = models.TextField(max_length=800)


class Search_Log(models.Model):
    search_log_id = models.AutoField(primary_key=True, unique=True)
    search_date = models.DateField(auto_now_add=True)
    search_home_type = models.ForeignKey(Property_Type, on_delete=models.CASCADE)
    search_neighborhood = models.ForeignKey(Property_Neighborhood, on_delete=models.CASCADE)
    search_price_range = models.ForeignKey(Property_Price_Range, on_delete=models.CASCADE)
















