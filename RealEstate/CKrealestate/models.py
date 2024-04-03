from django.db import models


class Property_Type(models.Model):
    property_type_id = models.AutoField(primary_key=True)
    property_type_name = models.CharField(max_length=100)


class Property_Neighborhood(models.Model):
    neighborhood_id = models.AutoField(primary_key=True)
    neighborhood_name = models.CharField(max_length=100)


class Property_Status(models.Model):
    property_status_id = models.AutoField(primary_key=True)
    property_status_name = models.CharField(max_length=100)


class Property_Price_Range(models.Model):
    price_range_id = models.AutoField(primary_key=True)
    price_range_value = models.CharField(max_length=100)
