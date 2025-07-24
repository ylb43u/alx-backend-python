from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For conversations: check if the user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For messages: check if the user is a participant in the related conversation
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
