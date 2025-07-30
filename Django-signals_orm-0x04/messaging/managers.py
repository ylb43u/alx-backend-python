from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self,user):
        self.get_queryset().filter(
            receiver=user,
            unread=False,
        ).only('message_id', 'content', 'sender_id', 'timestamp')