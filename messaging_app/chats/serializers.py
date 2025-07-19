from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        fields = ['__all__']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested user info
    message_body = serializers.CharField()  # explicit CharField for message body
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Example of SerializerMethodField to count messages
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()

    # Example of validation error if no participants
    def validate(self, data):
        participants = data.get('participants')
        if not participants or len(participants) == 0:
            raise serializers.ValidationError("Conversation must have at least one participant.")
        return data
