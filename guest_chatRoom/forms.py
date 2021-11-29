from django import forms
from .models import GuestChatRoom, Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)