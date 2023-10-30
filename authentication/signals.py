from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from core.helpers import reffer_id



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.reffer_code = reffer_id()
        instance.save()
    
    