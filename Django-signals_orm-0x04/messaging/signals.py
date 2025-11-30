#Create Django signals to trigger a notification when a new Message instance is created

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, User, MessageHistory
from django.contrib.auth import get_user_model


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

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only run if message already exists (i.e., being updated)
    if instance.pk is None:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content changed
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )

        # Mark message as edited
        instance.edited = True

        print(
            f"Message {instance.pk} edited. "
            f"Old content saved to history."
        )

# Signal to handle user deletion and cascade delete related data 

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """Delete all messages, notifications, and message histories of the user."""

    # DELETE MESSAGES SENT BY THE USER
    sent_messages = Message.objects.filter(sender=instance.username)
    sent_count = sent_messages.count()
    sent_messages.delete()

    # DELETE NOTIFICATIONS
    notifications = Notification.objects.filter(user=instance)
    notif_count = notifications.count()
    notifications.delete()

    # DELETE MESSAGE HISTORY
    histories = MessageHistory.objects.filter(message__sender=instance.username)
    hist_count = histories.count()
    histories.delete()

    print(
        f"User '{instance.username}' deleted → "
        f"{sent_count} sent messages, "
        f"{notif_count} notifications, "
        f"{hist_count} histories removed."
    )
