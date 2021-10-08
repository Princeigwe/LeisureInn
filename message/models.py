from django.db import models
from guest_chatRoom.models import GuestChatRoom
from users.models import CustomUser

# Create your models here.

class Message(models.Model):
    room = models.ForeignKey(GuestChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-timestamp', )
    
    def __str__(self):
        return str(self.sender.first_name + self.sender.last_name)