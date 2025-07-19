# chats/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Expect participants list of user_ids in request.data
        participants_ids = request.data.get('participants', [])

        if not participants_ids or not isinstance(participants_ids, list):
            return Response({"error": "Participants must be a non-empty list of user IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get User objects for participant IDs
        participants = User.objects.filter(user_id__in=participants_ids)

        if participants.count() != len(participants_ids):
            return Response({"error": "One or more participant IDs are invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender = request.user

        message_body = request.data.get('message_body')
        conversation_id = request.data.get('conversation_id')

        if not message_body:
            return Response({"error": "Message body is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not conversation_id:
            return Response({"error": "Conversation ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate conversation exists
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create message
        message = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
