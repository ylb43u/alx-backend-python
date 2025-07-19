from django.urls import path, include              # ✅ required import
from rest_framework.routers import DefaultRouter   # ✅ DefaultRouter()

from .views import ConversationViewSet             # or MessageViewSet too if needed

router = DefaultRouter()                           # ✅ routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
# router.register(r'messages', MessageViewSet, basename='message')  # Optional if you created this

urlpatterns = [
    path('', include(router.urls)),                # ✅ include and path
]
