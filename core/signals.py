from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import PO
from .views import update_fulfillment_rate,update_on_time_delivery_rate,update_response_time,update_avg_quality_rating
from django.utils import timezone


@receiver(pre_save, sender =PO)
def capture_previous(sender,instance,**kwargs):
   try:
        instance._previous_instance = sender.objects.get(id=instance.id)
   except sender.DoesNotExist:
        instance._previous_instance = None



@receiver(post_save,sender=PO)
def update_metrics(sender,instance,created,**kwargs):
    previous_instance = getattr(instance,"_previous_instance",None)
    if previous_instance:
        if instance.status != previous_instance.status:
            print("signal fulfill")
            
        if instance.status != previous_instance.status and (instance.delivery_date > timezone.now()):
            instance.in_time_delivery =True
            print("signal on timee")
            instance.save()
            update_on_time_delivery_rate(instance.vendor)
        if instance.acknowledgement_date:
            update_fulfillment_rate(instance.vendor)
            print("signal acknow")
            update_response_time(instance.vendor)
        if instance.quality_rating != previous_instance.quality_rating:
            print("signal quality")
            update_avg_quality_rating(instance.vendor)
    



    
          
        