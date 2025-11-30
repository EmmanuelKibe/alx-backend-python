#Create Django signals to trigger a notification when a new Message instance is created

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, User


@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    if created:
        print(f"New message created from {instance.sender} to {instance.receiver}: {instance.content}")

#Create a signal that listens for new messages and creates a notification for receivers
        try:
            receiver_user = User.objects.get(username=instance.receiver)
            Notification.objects.create(user=receiver_user, message=instance)
            print(f"Notification created for user {receiver_user.username} about new message ID {instance.id}")
        except User.DoesNotExist:
            print(f"Receiver user {instance.receiver} does not exist. No notification created.")

