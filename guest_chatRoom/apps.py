from django.apps import AppConfig


class GuestChatroomConfig(AppConfig):
    name = 'guest_chatRoom'
    
    def ready(self):
        import guest_chatRoom.signals