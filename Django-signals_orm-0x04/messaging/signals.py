from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Message

@receiver(post_save,sender=Message)
def message_created_handler(sender,instance,created,**kwargs):
    if created:
        print(f"✅ New message sent from {instance.sender} to {instance.receiver} at {instance.sent_at}")
        # You can send notifications, emails, or update other models here.