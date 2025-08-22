# messaging/admin.py
from django.contrib import admin
from .models import Message, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'parent_message', 'edited', 'timestamp')
    list_filter = ('edited', 'timestamp', 'sender', 'receiver')
    search_fields = ('content', 'sender__username', 'receiver__username')
    readonly_fields = ('message_id', 'timestamp')
    ordering = ('-timestamp',)
    raw_id_fields = ('sender', 'receiver', 'parent_message')  # avoids dropdown issues for large datasets

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'edited_at', 'content')
    list_filter = ('edited_at',)
    search_fields = ('content', 'message__content', 'message__sender__username')
    readonly_fields = ('edited_at',)
    ordering = ('-edited_at',)
    raw_id_fields = ('message',)  # avoids dropdown issues
