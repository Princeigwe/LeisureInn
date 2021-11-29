from django.db import models
from users.models import CustomUser

# Create your models here.

# the plan is to create a chatroom that has id of both guest and superuser for private communication

class GuestChatRoom(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user', default = 1)
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='guest')
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin')
    
    def __str__(self):
        return (self.guest.email + " & " + self.admin.email)


class Message(models.Model):
    room = models.ForeignKey(GuestChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('timestamp', )
    
    def __str__(self):
        return str(self.sender.first_name + self.sender.last_name)