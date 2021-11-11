from django.contrib import admin
from .models import GuestChatRoom, Message

# Register your models here.

class MessaageTabularInline(admin.TabularInline):
    model = Message
    readonly_fields = ['sender', 'content', 'timestamp']
    
class GuestRoomAdmin(admin.ModelAdmin):
    model = GuestChatRoom
    list_display = ['id', 'guest', 'admin']
    inlines = [MessaageTabularInline]
    

admin.site.register(GuestChatRoom, GuestRoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['room', 'sender', 'content', 'timestamp']
    #readonly_fields = ['room', 'sender', 'receiver', 'content', 'timestamp']

admin.site.register(Message, MessageAdmin)