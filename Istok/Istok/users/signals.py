from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, LoyaltyProgram


@receiver(post_save, sender=User)
def create_loyalty_program(sender, instance, created, **kwargs):
    if created:
        LoyaltyProgram.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_loyalty_program(sender, instance, **kwargs):
    if not hasattr(instance, 'loyaltyprogram'):
        LoyaltyProgram.objects.create(user=instance)
    instance.loyaltyprogram.save()
