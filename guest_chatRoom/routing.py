from django.urls import re_path
from . import consumers


"""the urls for websocket connetions"""
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<roomId>\w+)/$', consumers.ChatConsumer.as_asgi())
]

