from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Message
from django.db.models import Prefetch

class delete_user(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self,request):
        user = request.user
        user.delete()
        return Response({"message": "User account deleted."}, status=status.HTTP_204_NO_CONTENT)

class ThreadedConversationView(viewsets.views):
    def get(self,request,message_id):
        root_qs = Message.objects.filter(
                message_id=message_id,
                sender=request.user
            ).select_related('sender','receiver').prefetch_related(
                Prefetch('replies',queryset=Message.objects.select_related('sender','receiver'))
            )
                    
        if not root_qs.exists():
                        return Response({'error': 'Message not found or access denied'}, status=404)

        root_message = root_qs.first()

        # Step 2: Build threaded replies
        replies = self.get_all_replies(root_message)

        # Step 3: Return data
        return Response({
            'root_message': {
                'id': str(root_message.message_id),
                'sender': root_message.sender.username,
                'receiver': root_message.receiver.username,
                'content': root_message.content,
                'timestamp': root_message.sent_at
            },
            'replies': replies
        })
        
    def get_all_replies(self, message):
        replies = []
        def _collect_replies(msg,level = 0):
            reps = msg.replies.all().select_related('sender','receiver')
            for child in reps:
                replies.append({'message': child, 'level': level})
                _collect_replies(child,level+1)
                
        _collect_replies(message)
        return replies
    
class UnreadInboxView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unread_messages = Message.unread.for_user(request.user)

        data = [
            {
                'id': msg.id,
                'sender': msg.sender.username,
                'content': msg.content,
                'sent_at': msg.sent_at
            }
            for msg in unread_messages
        ]

        return Response({'unread_messages': data})