#Create Django signals to trigger a notification when a new Message instance is created

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message


@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    if created:
        print(f"New message created from {instance.sender} to {instance.receiver}: {instance.content}")