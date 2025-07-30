from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from django.contrib.auth.models import User

class delete_user(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self,request):
        user = request.user
        user.delete()
        return Response({"message": "User account deleted."}, status=status.HTTP_204_NO_CONTENT)
