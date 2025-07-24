# chats/permissions.py

from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        return request.user in obj.participants.all()


class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only if the user is part of the conversation that owns the message.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        return request.user in obj.conversation.participants.all()
