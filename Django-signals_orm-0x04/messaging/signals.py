from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from . models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save,sender=Message)
def message_created_handler(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        print(f"✅ New message sent from {instance.sender} to {instance.receiver} at {instance.timestamp}")
        # You can send notifications, emails, or update other models here.
        
@receiver(post_delete,sender=User)
def  user_delete(sender,instance,**kwargs):
    print(f"User {instance.username} deleted. Cleaning up related data.")
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()


# messaging/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only log edits if the message already exists (not on creation)
    if instance.pk:  # pk exists → object is being updated
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            # Should not happen, but safe guard
            pass
