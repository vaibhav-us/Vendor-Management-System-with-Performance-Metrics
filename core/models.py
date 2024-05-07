from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField(max_length=500)
    address = models.TextField(max_length=500)
    vendor_code = models.CharField(max_length=50) #  unique identifier for the vendor
    on_time_delivery_rate = models.FloatField(null=True,blank=True,default=0.0)
    quality_rating_avg = models.FloatField(null=True,blank=True,default=0.0)
    avg_response_time = models.FloatField(null=True,blank=True,default=0.0)
    fulfillment_rate = models.FloatField(null=True,blank=True,default=0.0)

    def __str__(self):
        return self.name


class PO(models.Model):
    po_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True,blank=True)
    in_time_delivery = models.BooleanField(default=False)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100,default="pending")
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgement_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.po_number
    

class Performance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    avg_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.vendor.name
