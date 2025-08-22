from django.contrib import admin
from django.urls import path
from messaging.views import delete_user, ConversationMessagesView, retreive_message_history

urlpatterns = [
    path("admin/", admin.site.urls),

    # If delete_user is a class-based APIView, use .as_view()
    path('api/delete-user/', delete_user.as_view(), name='delete_user'),

    # ThreadedConversationView is class-based → use .as_view()
    path('show_messages/', ConversationMessagesView.as_view(), name='show_messages'),

    # retreive_message_history is a function view → pass directly
    path('api/message-history/<uuid:message_id>/', retreive_message_history, name='message_history'),
]
