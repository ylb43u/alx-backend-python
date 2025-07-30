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
        root_message = get_object_or_404(
            Message.objects.select_related('sender','receiver').prefetch_related(
                Prefetch('replies',queryset=Message.objects.select_related('sender','receiver'))
            ),
            message_id=message_id
        )
        
        return Response.json({
            'root_message':root_message,
            'replies':self.get_all_replies(root_message)
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